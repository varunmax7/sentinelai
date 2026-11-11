"""Real satellite fire detections, folded into the wildfire signal.

The agent's wildfire score has so far been the Fosberg Fire Weather Index
alone - temperature, humidity and wind arranged into "how readily would fire
spread here if there were one". That is a *forecast of conditions*, and it
says nothing at all about whether anything is actually burning. A district can
sit at FFWI 26 all week with no fire, and a district at FFWI 8 can have an
active burn scar.

NASA FIRMS publishes the other half: VIIRS and MODIS thermal anomalies from
the last 24-48 hours, which is the same feed behind the dashboard's fire-danger
panel. This module counts detections near each watched point and lets them
raise the wildfire score.

**The two are kept distinguishable, never averaged into an anonymous number.**
`source_strengths` returns the combined figure the projection uses, and the
signal carries `fire_detections` and `fire_observed` alongside it so the UI can
say "conditions are dangerous" and "something is burning" as the different
claims they are.

Needs a free MAP_KEY from firms.modaps.eosdis.nasa.gov/api/map_key. Without
one this module contributes nothing and reports that it is unconfigured - it
never guesses, and the agent runs exactly as before.
"""

import math
import time

_CACHE = {'at': 0.0, 'rows': None, 'error': None}


def available():
    from twin import config as twin_config
    return bool(twin_config.FIRMS_MAP_KEY)


def _india_bbox():
    # Whole-country box. One request per cycle covers every watched point,
    # rather than 800 per-district requests against a rate-limited API.
    return (68.0, 6.0, 98.0, 37.5)


def detections(force=False):
    """Every thermal anomaly over India in the FIRMS window.

    `[]` when unconfigured or unavailable - the caller treats that as "no
    observation", never as "no fire".
    """
    from twin import config as twin_config
    from . import config as agent_config

    if not available():
        _CACHE['error'] = ('FIRMS_MAP_KEY is not set, so the wildfire score is '
                           'fire-weather conditions only, with no satellite '
                           'confirmation that anything is burning.')
        return []

    age = time.time() - _CACHE['at']
    if not force and _CACHE['rows'] is not None and age < agent_config.FIRMS_TTL_S:
        return _CACHE['rows']

    import csv
    import io

    import requests

    min_lon, min_lat, max_lon, max_lat = _india_bbox()
    url = ('https://firms.modaps.eosdis.nasa.gov/api/area/csv/%s/%s/%f,%f,%f,%f/%d'
           % (twin_config.FIRMS_MAP_KEY, twin_config.FIRMS_PRODUCT,
              min_lon, min_lat, max_lon, max_lat, agent_config.FIRMS_DAYS))
    try:
        response = requests.get(url, timeout=agent_config.HTTP_TIMEOUT_S * 3,
                                headers={'User-Agent': 'SentinelAI-DisasterAgent/1.0'})
        response.raise_for_status()
        body = response.text
        # FIRMS answers a bad key with HTTP 200 and a plain-text body, not a
        # 4xx with CSV - so a key problem would otherwise parse as "zero fires"
        # and read as "nothing is burning anywhere in India".
        if 'Invalid MAP_KEY' in body or not body.strip().lower().startswith('country_id,'):
            raise ValueError(body.strip()[:120] or 'FIRMS returned no CSV header')
        rows = []
        for row in csv.DictReader(io.StringIO(body)):
            try:
                rows.append((float(row['latitude']), float(row['longitude']),
                             _confidence(row.get('confidence')),
                             float(row.get('frp') or 0.0)))
            except (TypeError, ValueError, KeyError):
                continue
    except Exception as exc:  # noqa: BLE001 - a bad ingest must never kill the cycle
        _CACHE['error'] = '%s: %s' % (type(exc).__name__, str(exc)[:160])
        return _CACHE['rows'] or []

    _CACHE['rows'] = rows
    _CACHE['at'] = time.time()
    _CACHE['error'] = None
    return rows


def last_error():
    return _CACHE.get('error')


def _confidence(value):
    """FIRMS reports confidence as 0-100 (MODIS) or l/n/h (VIIRS)."""
    text = str(value or '').strip().lower()
    if text in ('l', 'low'):
        return 30.0
    if text in ('n', 'nominal'):
        return 65.0
    if text in ('h', 'high'):
        return 90.0
    try:
        return max(0.0, min(100.0, float(text)))
    except ValueError:
        return 50.0


def _haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0 * math.asin(min(1.0, math.sqrt(a)))


def summarise_near(lat, lon, rows=None, radius_km=None):
    """{'count', 'max_frp_mw', 'max_confidence'} for detections near a point."""
    from . import config as agent_config

    rows = detections() if rows is None else rows
    radius_km = radius_km or agent_config.FIRMS_RADIUS_KM
    if not rows:
        return {'count': 0, 'max_frp_mw': 0.0, 'max_confidence': 0.0}

    count = 0
    max_frp = max_conf = 0.0
    # Cheap degree pre-filter before the trig, so 800 points x N detections
    # stays affordable.
    span = radius_km / 100.0
    for flat, flon, conf, frp in rows:
        if abs(flat - lat) > span or abs(flon - lon) > span:
            continue
        if _haversine_km(lat, lon, flat, flon) > radius_km:
            continue
        count += 1
        max_frp = max(max_frp, frp)
        max_conf = max(max_conf, conf)
    return {'count': count, 'max_frp_mw': round(max_frp, 1),
            'max_confidence': round(max_conf, 1)}


def observed_boost(summary):
    """0-100 from observed fire, to combine with the modelled FFWI.

    Deliberately shallow and declared, in the same "named threshold"
    convention as every other sub-score here: one confirmed detection nearby
    is already meaningful, and ten is not ten times worse. A single
    high-confidence detection with real radiative power lands around 70.
    """
    from . import config as agent_config

    count = summary.get('count') or 0
    if not count:
        return 0.0
    # Saturates quickly - the difference between 1 and 4 fires matters far
    # more than between 40 and 80.
    density = min(1.0, math.log1p(count) / math.log1p(agent_config.FIRMS_SATURATION_COUNT))
    confidence = (summary.get('max_confidence') or 0.0) / 100.0
    power = min(1.0, (summary.get('max_frp_mw') or 0.0) / agent_config.FIRMS_FRP_MAX_MW)
    return max(0.0, min(100.0, 100.0 * (0.5 * density + 0.3 * confidence + 0.2 * power)))
