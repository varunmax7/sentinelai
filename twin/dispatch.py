"""The ONLY path from a flag to a real person's phone.

The twin owns no users - it never queries `User` directly, so it cannot
reach anyone on its own. At startup the host registers three callables with
`register_alert_channel(...)`, mirroring `security.py::adopt_login_required`'s
registration pattern:

    recipients_near(lat, lon, radius_km) -> [
        {'user_id': int, 'distance_km': float, 'username': str,
         'whatsapp_number': str or None}, ...
    ]
    notify(user_id, message) -> None            # in-app notification
    send_whatsapp(number, body) -> None          # raises on failure

Two invariants, both load-bearing:

  * **No automatic path.** Nothing in this module, `jobs.py` or the agent
    graphs calls `send()`. It is reached from exactly one place: the
    `POST /flags/<id>/dispatch` route, which only exists behind
    `twin_access_required(admin=True)`. An analyst's click is the only way a
    flag becomes a message on someone's phone.
  * **Every send is audited.** `TwinDispatch` gets a row before the function
    returns, success or partial failure - "who sent what, to how many
    people, when" must never depend on parsing a log line.
"""

from datetime import datetime

from . import config as twin_config
from .geo import haversine_m

_CHANNEL = {}


def register_alert_channel(recipients_near, notify, send_whatsapp, report_model=None):
    """Wire the host's user/notification/WhatsApp machinery into the twin.

    `report_model` is optional and used only to find a citizen photo from
    inside the alert area to attach - the twin still never queries it for
    anything else.
    """
    _CHANNEL['recipients_near'] = recipients_near
    _CHANNEL['notify'] = notify
    _CHANNEL['send_whatsapp'] = send_whatsapp
    _CHANNEL['report_model'] = report_model


def channel_available():
    return bool(_CHANNEL.get('recipients_near') and _CHANNEL.get('notify'))


class DispatchError(Exception):
    """Raised for a request-level problem (unknown flag, no footprint, ...).

    The route catches this and returns 4xx; it is not the same thing as an
    individual WhatsApp send failing, which is counted, not raised.
    """


# --- footprint ---------------------------------------------------------------
def flag_footprint(models, flag):
    """(center_lat, center_lon, radius_km) covering every cell in the flag's

    cluster, or None if the flag has no known footprint at all. Falls back to
    the flag's single `h3_index` for flags filed before `TwinFlagCell` existed,
    or for a cluster that somehow resolved to zero cells.
    """
    cell_rows = (models.TwinCell.query
                 .join(models.TwinFlagCell, models.TwinFlagCell.h3_index == models.TwinCell.h3_index)
                 .filter(models.TwinFlagCell.flag_id == flag.id)
                 .all())

    if not cell_rows and flag.h3_index:
        cell_rows = models.TwinCell.query.filter_by(h3_index=flag.h3_index).all()

    if not cell_rows:
        return None

    center_lat = sum(c.center_latitude for c in cell_rows) / len(cell_rows)
    center_lon = sum(c.center_longitude for c in cell_rows) / len(cell_rows)
    spread_km = max(
        (haversine_m(center_lat, center_lon, c.center_latitude, c.center_longitude) / 1000.0
         for c in cell_rows),
        default=0.0,
    )
    radius_km = min(spread_km + twin_config.DISPATCH_BUFFER_KM, twin_config.DISPATCH_MAX_RADIUS_KM)
    return center_lat, center_lon, radius_km


# --- imagery attached to an alert -----------------------------------------------
# Twilio fetches a media URL from its own servers, so anything it is handed must
# be publicly reachable. A `/static/uploads/...` path on localhost is not, and
# handing one over produces a silently image-less message - so a local URL is
# skipped rather than sent and hoped for.
_LOCAL_HOSTS = ('localhost', '127.0.0.1', '0.0.0.0', '192.168.', '10.0.', '::1')


def _is_public_url(url):
    if not url or not str(url).lower().startswith(('http://', 'https://')):
        return False
    return not any(h in str(url) for h in _LOCAL_HOSTS)


def alert_image(city, lat, lon, base_url=None):
    """The best publicly-fetchable picture of this place, and an honest caption.

    Returns `(url, caption)` - or `(None, None)` when nothing usable exists.

    Ordered by what actually helps someone who has just been told to evacuate:
    a frame from right now beats a photo of the right street from 2019, and
    both beat nothing. Every option carries a caption naming what it is and how
    old it is, because an archival photo attached to an emergency alert reads
    as "this is happening now" unless it explicitly says otherwise.
    """
    candidates = []

    # 1. A live webcam frame. Genuinely current, though usually elsewhere in
    #    the city - the caption says how far.
    try:
        from .ground import _WebcamAdapter

        result = _WebcamAdapter().run(lat=city.center_latitude, lon=city.center_longitude,
                                      radius_m=twin_config.WEBCAM_RADIUS_M)
        for row in ((result.data or {}).get('rows') or []):
            if not _is_public_url(row.get('thumb_url')):
                continue
            distance_km = haversine_m(lat, lon, row['lat'], row['lon']) / 1000.0
            candidates.append((0, row['thumb_url'],
                               'Live city webcam, %.1f km from the alert area.' % distance_km))
            break
    except Exception:  # noqa: BLE001 - imagery must never block an alert
        pass

    # 2. A citizen's own photo from inside the alert area, if this deployment
    #    is reachable from the internet at all.
    if base_url and _is_public_url(base_url):
        try:
            from urllib.parse import quote

            from .ingest.internal_reports import LOOKBACK_HOURS  # noqa: F401  (documented bound)
            report_model = _CHANNEL.get('report_model')
            if report_model is not None:
                span = twin_config.DISPATCH_IMAGE_RADIUS_KM / 111.0
                rows = (report_model.query
                        .filter(report_model.image_file.isnot(None),
                                report_model.image_file != '',
                                report_model.latitude.between(lat - span, lat + span),
                                report_model.longitude.between(lon - span, lon + span))
                        .order_by(report_model.timestamp.desc())
                        .limit(10).all())
                for report in rows:
                    distance_km = haversine_m(lat, lon, report.latitude, report.longitude) / 1000.0
                    if distance_km > twin_config.DISPATCH_IMAGE_RADIUS_KM:
                        continue
                    url = '%s/static/uploads/%s' % (base_url.rstrip('/'), quote(report.image_file))
                    when = report.timestamp.strftime('%d %b %H:%M') if report.timestamp else 'unknown time'
                    candidates.append((1, url,
                                       'Photo from a citizen report %.1f km away, %s UTC.'
                                       % (distance_km, when)))
                    break
        except Exception:  # noqa: BLE001
            pass

    # 3. Satellite view of the alert area. Always exists, always this place -
    #    the floor under "show them where".
    try:
        from . import aerial

        url = aerial.crop_url(lat, lon, span_m=twin_config.DISPATCH_IMAGE_SPAN_M)
        if _is_public_url(url):
            candidates.append((2, url, 'Satellite view of the alert area (Esri World Imagery).'))
    except Exception:  # noqa: BLE001
        pass

    if not candidates:
        return None, None
    candidates.sort(key=lambda c: c[0])
    _rank, url, caption = candidates[0]
    return url, caption


# --- cooldown ------------------------------------------------------------------
def _cooldown(models, flag_id):
    """(is_active, minutes_remaining) - a DB-backed cooldown, unlike the

    in-memory one `/api/flood_station_alert` uses, so it survives a restart
    and shows up in the same audit trail as the sends it is guarding.
    """
    last = (models.TwinDispatch.query
            .filter_by(flag_id=flag_id)
            .order_by(models.TwinDispatch.created_at.desc())
            .first())
    if last is None:
        return False, 0
    elapsed_min = (datetime.utcnow() - last.created_at).total_seconds() / 60.0
    remaining = twin_config.DISPATCH_COOLDOWN_MIN - elapsed_min
    return (remaining > 0), max(0, round(remaining))


# --- preview -------------------------------------------------------------------
def preview(models, flag):
    """How many people a dispatch would reach right now, before anything sends."""
    if not channel_available():
        raise DispatchError('No alert channel registered on this host')

    footprint = flag_footprint(models, flag)
    if footprint is None:
        raise DispatchError('This flag has no known cell footprint to alert around')

    lat, lon, radius_km = footprint
    recipients = _CHANNEL['recipients_near'](lat, lon, radius_km)
    cooldown_active, cooldown_remaining = _cooldown(models, flag.id)

    return {
        'center': {'lat': lat, 'lon': lon},
        'radius_km': round(radius_km, 2),
        'recipients': len(recipients),
        'whatsapp_reachable': sum(1 for r in recipients if r.get('whatsapp_number')),
        'nearest': [
            {'username': r.get('username'), 'distance_km': round(r.get('distance_km', 0.0), 1)}
            for r in sorted(recipients, key=lambda r: r.get('distance_km', 0.0))[:5]
        ],
        'cooldown_active': cooldown_active,
        'cooldown_remaining_minutes': cooldown_remaining,
    }


# --- send ------------------------------------------------------------------------
def send(db, models, flag, actor_user_id, note=None, force=False, base_url=None):
    """Dispatch a flag. Returns a summary dict, or raises `DispatchError`

    for a request-level problem. An individual WhatsApp failure is counted
    in the result, not raised - one bad phone number must not roll back
    notifications that already went out to everyone else.
    """
    if not channel_available():
        raise DispatchError('No alert channel registered on this host')
    if flag.status != 'approved':
        raise DispatchError('Only an approved flag can be dispatched')

    footprint = flag_footprint(models, flag)
    if footprint is None:
        raise DispatchError('This flag has no known cell footprint to alert around')
    lat, lon, radius_km = footprint

    cooldown_active, cooldown_remaining = _cooldown(models, flag.id)
    if cooldown_active and not force:
        raise DispatchError(
            'This flag was already dispatched in the last %d minutes. '
            'Retry in %d min, or resend with force.'
            % (twin_config.DISPATCH_COOLDOWN_MIN, cooldown_remaining))

    recipients = _CHANNEL['recipients_near'](lat, lon, radius_km)

    # Picture of the place, chosen and captioned before the loop so every
    # recipient gets the same one and it is looked up once, not once per phone.
    city = models.TwinCity.query.get(flag.city_id) if flag.city_id else None
    image_url = image_caption = None
    if city is not None and twin_config.DISPATCH_ATTACH_IMAGE:
        try:
            image_url, image_caption = alert_image(city, lat, lon, base_url=base_url)
        except Exception:  # noqa: BLE001 - imagery must never block an alert
            image_url = image_caption = None

    message = _message_for(flag, note, image_caption)

    whatsapp_sent = whatsapp_failed = 0
    for recipient in recipients:
        _CHANNEL['notify'](recipient['user_id'], message)
        number = recipient.get('whatsapp_number')
        if number:
            try:
                # Older hosts registered a two-argument sender; an image is an
                # enhancement, never a reason for an alert not to go out.
                if image_url:
                    try:
                        _CHANNEL['send_whatsapp'](number, message, image_url)
                    except TypeError:
                        _CHANNEL['send_whatsapp'](number, message)
                else:
                    _CHANNEL['send_whatsapp'](number, message)
                whatsapp_sent += 1
            except Exception:  # noqa: BLE001 - one bad number must not break the rest
                whatsapp_failed += 1

    row = models.TwinDispatch(
        flag_id=flag.id, dispatched_by=actor_user_id,
        center_latitude=lat, center_longitude=lon, radius_km=round(radius_km, 2),
        note=note, recipients=len(recipients),
        whatsapp_sent=whatsapp_sent, whatsapp_failed=whatsapp_failed,
    )
    db.session.add(row)
    db.session.commit()

    return {
        'flag_id': flag.id, 'recipients': len(recipients),
        'whatsapp_sent': whatsapp_sent, 'whatsapp_failed': whatsapp_failed,
        'radius_km': round(radius_km, 2), 'dispatch_id': row.id,
        'image_url': image_url, 'image_caption': image_caption,
    }


def _message_for(flag, note, image_caption=None):
    parts = ['SENTINEL AI ALERT']
    if flag.title:
        parts.append(flag.title)
    if flag.hazard_type:
        parts.append('(%s)' % flag.hazard_type)
    body = [' '.join(parts)]
    if note:
        body.append(note)
    if image_caption:
        # Said in the text, not left to the picture. An image attached to an
        # emergency message reads as "this is happening now" unless the words
        # say what it actually is.
        body.append('\U0001F4F7 %s' % image_caption)
    return '\n\n'.join(body)


def dispatch_history(models, flag_id, limit=20):
    rows = (models.TwinDispatch.query.filter_by(flag_id=flag_id)
            .order_by(models.TwinDispatch.created_at.desc()).limit(limit).all())
    return [{
        'id': r.id, 'dispatched_by': r.dispatched_by,
        'recipients': r.recipients, 'whatsapp_sent': r.whatsapp_sent,
        'whatsapp_failed': r.whatsapp_failed, 'radius_km': r.radius_km,
        'created_at': r.created_at.isoformat() + 'Z' if r.created_at else None,
    } for r in rows]
