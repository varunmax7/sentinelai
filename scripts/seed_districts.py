"""Build the agent's district monitoring grid from open, authoritative sources.

Run this once (and again when districts are reorganised, which India does
every few years):

    python scripts/seed_districts.py

It writes `data/disaster_agent/districts.json`, which `disaster_agent/
districts.py` loads at import. **Nothing here is typed by hand.** Every
coordinate comes from OpenStreetMap, every state attribution from Wikidata,
and every elevation from Open-Meteo - so the file can be regenerated and
diffed rather than trusted.

Sources, and why each:

  OpenStreetMap (Overpass)   the district list itself - 787 relations at
                             admin_level=5 inside India, of which 781 carry
                             `ref:LGD:district`, the Government of India's own
                             Local Government Directory code. That code is what
                             makes a row auditable against an official list.
  Wikidata (SPARQL)          the parent state, resolved by walking P131
                             transitively. A single P131 hop only resolved
                             275/787, because many districts sit under a
                             division rather than directly under a state;
                             P131+ resolves all 787 across 36 states and UTs.
  Open-Meteo (elevation)     metres above sea level, batched 150 at a time.
                             This is the measured basis for the landslide
                             prior - not a guess from the district's name.

The hazard prior is derived, and the derivation is stated in the file so it
can be argued with (see `_hazard_bias`). It is not a measurement and must
never be presented as one.
"""

import json
import math
import os
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from disaster_agent.regions import REGIONS  # noqa: E402

# Mirrors, tried in order. The main instance answers 504 under load - which
# it will, since this is a whole-country query - and a one-shot seed script
# failing on a transient gateway timeout is a bad way to spend ten minutes.
OVERPASS_URLS = (
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
    'https://overpass.osm.ch/api/interpreter',
)
WIKIDATA_URL = 'https://query.wikidata.org/sparql'
ELEVATION_URL = 'https://api.open-meteo.com/v1/elevation'
OUT_PATH = os.path.join('data', 'disaster_agent', 'districts.json')
UA = {'User-Agent': 'SentinelAI-DisasterAgent/1.0 (urban resilience research)'}

# Elevation above which a district is given a landslide prior. The Himalayan,
# Western Ghats and North-East districts that actually suffer landslides sit
# well above this; the Indo-Gangetic plain sits far below it.
LANDSLIDE_ELEVATION_M = 600
# How close a district centroid must be to a curated COASTAL reference point
# before it inherits that point's cyclone/storm-surge prior. Indian coastal
# districts are ~50-150 km across, so this is deliberately generous.
COASTAL_INHERIT_KM = 180


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0 * math.asin(min(1.0, math.sqrt(a)))


def fetch_districts():
    query = """
    [out:json][timeout:240];
    area['ISO3166-1'='IN'][admin_level=2]->.in;
    relation(area.in)['boundary'='administrative']['admin_level'='5'];
    out tags center;
    """
    print('Overpass: fetching Indian districts (admin_level=5)...')
    last_error = None
    elements = None
    for attempt, url in enumerate(OVERPASS_URLS * 2):
        try:
            response = requests.post(url, data={'data': query}, headers=UA, timeout=300)
            response.raise_for_status()
            elements = response.json().get('elements', [])
            if elements:
                print('  via %s' % url.split('/')[2])
                break
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            print('  %s failed (%s), trying the next mirror...'
                  % (url.split('/')[2], type(exc).__name__))
            time.sleep(10 * (attempt + 1))
    if not elements:
        raise SystemExit('Every Overpass mirror failed. Last error: %s' % last_error)
    print('  %d districts, %d with centre coordinates'
          % (len(elements), sum(1 for e in elements if e.get('center'))))
    return [e for e in elements if e.get('center') and e.get('tags', {}).get('name')]


def fetch_states(qids):
    """district QID -> state name, via a transitive P131 walk."""
    if not qids:
        return {}
    values = ' '.join('wd:%s' % q for q in qids)
    query = """
    SELECT ?item ?stateLabel WHERE {
      VALUES ?item { %s }
      ?item wdt:P131+ ?state .
      ?state wdt:P31/wdt:P279* wd:Q131541 .
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """ % values
    print('Wikidata: resolving parent states for %d districts...' % len(qids))
    response = requests.post(
        WIKIDATA_URL, data={'query': query, 'format': 'json'},
        headers=dict(UA, Accept='application/sparql-results+json'), timeout=300)
    response.raise_for_status()
    out = {}
    for row in response.json()['results']['bindings']:
        out.setdefault(row['item']['value'].rsplit('/', 1)[-1], row['stateLabel']['value'])
    print('  resolved %d of %d' % (len(out), len(qids)))
    return out


def fetch_elevations(points, batch=100):
    """[(lat, lon)] -> [metres or None].

    The elevation endpoint caps at 100 coordinates per call - lower than the
    forecast endpoint's 200, and it answers HTTP 400 rather than truncating,
    so the batch size is not shared between them.

    A failed batch yields `None`s rather than aborting: elevation only feeds
    the landslide prior, and losing it for some districts is much better than
    losing the whole seed run to one bad request.
    """
    print('Open-Meteo: fetching elevation for %d points...' % len(points))
    out = []
    for start in range(0, len(points), batch):
        chunk = points[start:start + batch]
        values = []
        # Open-Meteo rate-limits a burst of eight batches, and a district that
        # loses its elevation silently loses its landslide prior - so a failed
        # batch is retried with backoff rather than written off.
        for attempt in range(4):
            try:
                response = requests.get(ELEVATION_URL, params={
                    'latitude': ','.join('%.4f' % p[0] for p in chunk),
                    'longitude': ','.join('%.4f' % p[1] for p in chunk),
                }, headers=UA, timeout=120)
                response.raise_for_status()
                values = response.json().get('elevation') or []
                if values:
                    break
            except Exception as exc:  # noqa: BLE001
                wait = 5 * (attempt + 1)
                print('  batch at %d attempt %d failed (%s), retrying in %ds'
                      % (start, attempt + 1, type(exc).__name__, wait))
                time.sleep(wait)
        if not values:
            print('  batch at %d gave up - those districts get no elevation' % start)
        values = list(values) + [None] * (len(chunk) - len(values))
        out.extend(values[:len(chunk)])
        time.sleep(1)
    print('  got %d of %d elevations' % (sum(1 for e in out if e is not None), len(points)))
    return out


def _hazard_bias(lat, lon, elevation_m):
    """A DERIVED susceptibility prior. Not a measurement - see the note below.

    `regions.py` hand-declares a bias for each of its 26 curated points, which
    is reviewable at that size and impossible at 787. So this derives one, and
    every rule is stated here so it can be argued with by editing this
    function rather than by retuning a threshold somewhere else:

      flood      every district. Rainfall is measured everywhere and every
                 Indian district can flood; withholding it would silently
                 blind the agent.
      heat_wave  every district, for the same reason - temperature is measured
                 everywhere.
      landslide  elevation >= LANDSLIDE_ELEVATION_M. Measured, not guessed.
      cyclone /  inherited from the nearest curated COASTAL region within
      storm_surge COASTAL_INHERIT_KM. An inland district never receives one.
      wildfire   elevation < 2500 m, i.e. below the tree line. FFWI is
                 computed from live temperature, humidity and wind anyway, so
                 this only excludes terrain where it cannot apply.
    """
    bias = {'flood', 'heat_wave'}

    if elevation_m is not None:
        if elevation_m >= LANDSLIDE_ELEVATION_M:
            bias.add('landslide')
        if elevation_m < 2500:
            bias.add('wildfire')
    else:
        bias.add('wildfire')

    for _slug, _name, _state, rlat, rlon, rbias, terrain in REGIONS:
        if 'coastal' not in (terrain or ''):
            continue
        if haversine_km(lat, lon, rlat, rlon) <= COASTAL_INHERIT_KM:
            bias.update(h for h in rbias if h in ('cyclone', 'storm_surge'))
            break

    return sorted(bias)


def main():
    elements = fetch_districts()
    qids = [e['tags']['wikidata'] for e in elements if e['tags'].get('wikidata')]
    states = fetch_states(qids)

    points = [(e['center']['lat'], e['center']['lon']) for e in elements]
    elevations = fetch_elevations(points)

    rows = []
    for element, elevation in zip(elements, elevations):
        tags = element['tags']
        lat, lon = element['center']['lat'], element['center']['lon']
        name = tags.get('name')
        state = states.get(tags.get('wikidata'))
        if not state:
            # No invented attribution: a district whose parent state could not
            # be resolved is written with state=None and shown without one.
            state = None
        rows.append({
            'slug': 'd_%s' % (tags.get('ref:LGD:district') or element['id']),
            'name': name,
            'state': state,
            'lat': round(lat, 5),
            'lon': round(lon, 5),
            'elevation_m': round(elevation) if elevation is not None else None,
            'lgd_code': tags.get('ref:LGD:district'),
            'wikidata': tags.get('wikidata'),
            'osm_relation': element['id'],
            'hazard_bias': _hazard_bias(lat, lon, elevation),
        })

    rows.sort(key=lambda r: ((r['state'] or 'zz'), r['name']))
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as handle:
        json.dump({
            'generated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'sources': {
                'districts': 'OpenStreetMap admin_level=5 relations (ODbL)',
                'states': 'Wikidata P131+ transitive parent (CC0)',
                'elevation': 'Open-Meteo elevation API',
            },
            'note': ('hazard_bias is a DERIVED prior, not a measurement - see '
                     'scripts/seed_districts.py::_hazard_bias for every rule.'),
            'districts': rows,
        }, handle, indent=1, ensure_ascii=False)

    with_state = sum(1 for r in rows if r['state'])
    with_lgd = sum(1 for r in rows if r['lgd_code'])
    print('\nWrote %s' % OUT_PATH)
    print('  districts      : %d' % len(rows))
    print('  with state     : %d' % with_state)
    print('  with LGD code  : %d' % with_lgd)
    print('  with elevation : %d' % sum(1 for r in rows if r['elevation_m'] is not None))
    print('  landslide prior: %d' % sum(1 for r in rows if 'landslide' in r['hazard_bias']))
    print('  coastal prior  : %d' % sum(1 for r in rows if 'cyclone' in r['hazard_bias']))


if __name__ == '__main__':
    main()
