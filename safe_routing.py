"""Safe-place lookup and evacuation-navigation links for hazard alerts.

Given an approved hazard report, this finds a real nearby safe public
building via OpenStreetMap (Overpass) - a shelter, community hall,
government building or school - preferring ones that sit outside the
hazard's own danger radius, so the destination recommended to evacuees is
not itself inside the zone they are being told to leave.

When Overpass has nothing mapped nearby (rate-limited, offline, or a data
desert for that area), this falls back to a computed "keep moving away from
the hazard" point along the recipient's own bearing. That fallback is
labelled honestly as a direction, not a named shelter, since it is a
heuristic rather than a verified building.

No API key is required anywhere in this module: Overpass is a free public
OSM service (same data source already used elsewhere in this app, see
twin/ingest/overpass.py), and the Google Maps link below is a plain deep
link into the Maps app/website, not a billed Maps Platform API call.
"""

import math
import time

import requests

from utils import calculate_distance

OVERPASS_ENDPOINTS = (
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
)
# This runs synchronously on an official's "approve" click (fanned out once
# per report, not once per recipient - see the cache below), not on a
# background job, so it gets a short leash rather than Overpass's usual
# tens-of-seconds city-query budget.
OVERPASS_TIMEOUT_S = 8
SAFE_PLACE_SEARCH_RADIUS_M = 20000  # 20km search ring around the hazard

# Candidate OSM tags, ranked by how fit-for-purpose they are as an
# evacuation destination (1 = best). Shelters/assembly points are
# purpose-built; community halls, town halls and government buildings are
# large public buildings commonly opened as relief camps in India; schools
# and colleges are the most common real-world fallback shelter. Hospitals
# rank last - useful as "somewhere official and populated" but not
# somewhere you want evacuees filling up.
SAFE_PLACE_TAGS = (
    ('amenity', 'shelter', 1, 'Shelter'),
    ('emergency', 'assembly_point', 1, 'Assembly Point'),
    ('amenity', 'community_centre', 2, 'Community Centre'),
    ('amenity', 'townhall', 2, 'Town Hall'),
    ('building', 'government', 2, 'Government Building'),
    ('amenity', 'school', 3, 'School'),
    ('amenity', 'college', 3, 'College'),
    ('amenity', 'hospital', 4, 'Hospital'),
)

# Keyed on a ~1km-rounded (lat, lon); OSM safe-building data does not change
# within the lifetime of a single incident, so a fan-out of many alert
# recipients for one report costs at most one Overpass round trip, not one
# per recipient.
_CACHE = {}
_CACHE_TTL_S = 3600


def _cache_key(lat, lon):
    return (round(lat, 2), round(lon, 2))


def _query_overpass(lat, lon, radius_m):
    clauses = []
    for key, value, _rank, _label in SAFE_PLACE_TAGS:
        clauses.append('node["%s"="%s"](around:%d,%f,%f);' % (key, value, radius_m, lat, lon))
    ql = "[out:json][timeout:%d];(%s);out center tags;" % (max(OVERPASS_TIMEOUT_S - 2, 1), ''.join(clauses))

    last_error = None
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            response = requests.post(endpoint, data={'data': ql}, timeout=OVERPASS_TIMEOUT_S)
            if response.status_code == 200:
                return response.json()
            last_error = 'HTTP %s' % response.status_code
        except Exception as exc:  # noqa: BLE001 - a safe-place lookup must never raise into an alert send
            last_error = str(exc)
    print(f"⚠️ Safe-place lookup: Overpass unavailable ({last_error})")
    return None


def find_nearby_safe_places(lat, lon, radius_m=SAFE_PLACE_SEARCH_RADIUS_M):
    """Candidate safe public buildings near (lat, lon), each tagged with a rank.

    Cached per hazard location/TTL (see module docstring) so this is safe to
    call once per alert recipient without multiplying network calls.
    """
    key = _cache_key(lat, lon)
    cached = _CACHE.get(key)
    if cached and (time.monotonic() - cached[0]) < _CACHE_TTL_S:
        return cached[1]

    rank_by_tag = {(k, v): (rank, label) for k, v, rank, label in SAFE_PLACE_TAGS}
    payload = _query_overpass(lat, lon, radius_m)
    places = []
    if payload:
        for element in payload.get('elements', []):
            tags = element.get('tags') or {}
            place_lat = element.get('lat')
            place_lon = element.get('lon')
            if place_lat is None or place_lon is None:
                continue
            for (k, v), (rank, label) in rank_by_tag.items():
                if tags.get(k) == v:
                    places.append({
                        'name': tags.get('name') or label,
                        'type': label,
                        'rank': rank,
                        'lat': place_lat,
                        'lon': place_lon,
                    })
                    break

    _CACHE[key] = (time.monotonic(), places)
    return places


def _bearing_deg(lat1, lon1, lat2, lon2):
    """Initial compass bearing (degrees, 0-360) from point 1 to point 2."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlambda = math.radians(lon2 - lon1)
    x = math.sin(dlambda) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlambda)
    return math.degrees(math.atan2(x, y)) % 360.0


def _destination_point(lat, lon, bearing_deg, distance_km):
    """Point `distance_km` away from (lat, lon) along `bearing_deg`."""
    earth_radius_km = 6371.0
    d_r = distance_km / earth_radius_km
    br = math.radians(bearing_deg)
    phi1, lam1 = math.radians(lat), math.radians(lon)
    phi2 = math.asin(math.sin(phi1) * math.cos(d_r) + math.cos(phi1) * math.sin(d_r) * math.cos(br))
    lam2 = lam1 + math.atan2(math.sin(br) * math.sin(d_r) * math.cos(phi1),
                              math.cos(d_r) - math.sin(phi1) * math.sin(phi2))
    return math.degrees(phi2), math.degrees(lam2)


def get_safe_destination(hazard_lat, hazard_lon, hazard_radius_km, user_lat, user_lon):
    """The safest place to point one alert recipient toward.

    Returns a dict: {'lat', 'lon', 'name', 'place_type', 'is_named_shelter'}.

    Prefers a real OSM-mapped shelter/community hall/school that is outside
    the hazard's own danger radius (so the recommended destination is not
    itself inside the zone being evacuated). Falls back to a computed point
    along the recipient's own bearing away from the hazard - a "keep moving
    away" heuristic, not a verified building - when nothing suitable is
    mapped nearby or Overpass could not be reached.
    """
    candidates = find_nearby_safe_places(hazard_lat, hazard_lon)
    best = None
    for place in sorted(candidates, key=lambda p: p['rank']):
        distance_from_hazard = calculate_distance(hazard_lat, hazard_lon, place['lat'], place['lon'])
        if distance_from_hazard < hazard_radius_km:
            continue  # inside the danger zone itself - not actually safe
        if best is None or place['rank'] < best['rank']:
            best = place
            if best['rank'] == 1:
                break  # a purpose-built shelter/assembly point wins outright

    if best:
        return {
            'lat': best['lat'],
            'lon': best['lon'],
            'name': best['name'],
            'place_type': best['type'],
            'is_named_shelter': True,
        }

    # No mapped shelter clear of the zone - fall back to directional
    # guidance: keep moving along the same bearing the recipient is already
    # offset from the hazard, just far enough to clear the danger radius
    # with a small safety margin - not an arbitrary multiple of it. A fixed
    # 1.5x radius sent someone standing at the hazard 22.5km away for a
    # 15km-radius tsunami zone; all that distance actually buys is clearing
    # the boundary by an extra 7.5km for no reason.
    #
    # If the recipient is already further from the hazard than that minimum
    # clearance distance, they are already outside the danger zone, so the
    # destination is their own current distance along the same bearing
    # (effectively "stay where you are") instead of pulling them backward
    # toward a point closer to the hazard than they currently are.
    clearance_km = min(2.0, max(0.5, hazard_radius_km * 0.1))
    min_safe_distance_km = hazard_radius_km + clearance_km
    distance_from_hazard_km = calculate_distance(hazard_lat, hazard_lon, user_lat, user_lon)
    bearing = _bearing_deg(hazard_lat, hazard_lon, user_lat, user_lon)
    target_distance_km = max(distance_from_hazard_km, min_safe_distance_km)
    safe_lat, safe_lon = _destination_point(hazard_lat, hazard_lon, bearing, target_distance_km)
    return {
        'lat': safe_lat,
        'lon': safe_lon,
        'name': None,
        'place_type': None,
        'is_named_shelter': False,
    }


# Two short, concrete precautions per hazard type - kept deliberately small
# (this rides inside an already-long WhatsApp alert) and action-oriented
# rather than descriptive, to complement the navigation link rather than
# repeat what the hazard-type banner above it already says.
HAZARD_PRECAUTIONS = {
    'tsunami': [
        "Do not go to the coast to watch the waves.",
        "Stay away from rivers/creeks connected to the sea - they carry the surge inland too.",
    ],
    'storm_surge': [
        "Avoid low-lying coastal roads and basements.",
        "Keep away from loose debris and downed power lines.",
    ],
    'high_waves': [
        "Stay off beaches, piers and rocks.",
        "Avoid swimming or boating until the alert clears.",
    ],
    'swell_surge': [
        "Keep clear of the surf zone and wet/slippery rocks.",
        "Avoid walking close to the shoreline.",
    ],
    'coastal_flooding': [
        "Never drive or walk through flooded roads.",
        "Switch off electrical mains if water starts entering your home.",
    ],
    'abnormal_tide': [
        "Keep clear of jetties, harbours and low sea walls.",
        "Secure boats and belongings left near the shore.",
    ],
    'other': [
        "Follow official instructions and keep clear of the hazard area.",
        "Keep your phone charged and emergency contacts handy.",
    ],
}


def _precautions_block(hazard_type):
    tips = HAZARD_PRECAUTIONS.get(hazard_type, HAZARD_PRECAUTIONS['other'])
    return "⚠️ *Precautions:*\n" + "\n".join(f"• {tip}" for tip in tips)


def navigation_link(user_lat, user_lon, dest_lat, dest_lon):
    """A turn-by-turn Google Maps link from the recipient's own location.

    This is a plain web deep link (`/maps/dir/?api=1`), not a Maps Platform
    API call, so it needs no API key and works by just being opened on the
    recipient's phone.
    """
    return (
        f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lon}"
        f"&destination={dest_lat},{dest_lon}&travelmode=driving"
    )


def safe_place_whatsapp_section(hazard_type, hazard_lat, hazard_lon, hazard_radius_km, user_lat, user_lon):
    """The ready-to-append WhatsApp message block for one recipient.

    Wraps the lookup + link generation so a failure here (bad Overpass
    response, network hiccup) degrades to an empty string instead of ever
    blocking or breaking the hazard alert it is attached to.
    """
    try:
        destination = get_safe_destination(hazard_lat, hazard_lon, hazard_radius_km, user_lat, user_lon)
        link = navigation_link(user_lat, user_lon, destination['lat'], destination['lon'])
        if destination['is_named_shelter']:
            nav_block = (
                f"\n🧭 *Nearest Safe Place:* {destination['name']} ({destination['place_type']})\n"
                f"🗺️ *Navigate there:* {link}\n"
            )
        else:
            nav_block = (
                f"\n🧭 *Safe Direction:* Move away from the hazard toward higher/inland ground.\n"
                f"🗺️ *Navigate there:* {link}\n"
            )
        return nav_block + _precautions_block(hazard_type) + "\n"
    except Exception as exc:  # noqa: BLE001 - never let safe-routing block an alert send
        print(f"⚠️ Safe-place navigation unavailable: {exc}")
        return ""
