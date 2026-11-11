"""District-level monitoring grid, loaded from a seeded file.

`regions.py` watches 26 curated city-scale points. That is the right
resolution for projecting a signal *between* cities, and the wrong one for an
analyst asking "which district is in trouble" - a watch list that only ever
names Lucknow, Patna and Bengaluru cannot answer that, however accurate each
row is.

This module loads `data/disaster_agent/districts.json`, built by
`scripts/seed_districts.py` from OpenStreetMap (the district list and its
centroids, 781 of 787 carrying the Government of India's own LGD district
code), Wikidata (the parent state) and Open-Meteo (elevation). No coordinate
here was typed by hand, and the file can be regenerated and diffed.

The two grids coexist deliberately. Districts are what the watch list shows;
the curated regions remain the projection anchors, because their hazard
priors are hand-reviewed rather than derived.
"""

import json
import os

from . import config as agent_config

_CACHE = {'mtime': None, 'rows': None}


def _path():
    return agent_config.DISTRICTS_FILE


def load():
    """Every seeded district, or `[]` when the file is absent.

    An absent file is a supported state, not an error: the agent falls back to
    the 26 curated regions and says so, rather than refusing to run because a
    seed script has not been executed yet.
    """
    path = _path()
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return []
    if _CACHE['mtime'] != mtime:
        try:
            with open(path, 'r', encoding='utf-8') as handle:
                payload = json.load(handle)
        except (OSError, ValueError):
            return []
        rows = []
        for row in (payload.get('districts') or []):
            if row.get('lat') is None or row.get('lon') is None or not row.get('name'):
                continue
            rows.append({
                'slug': row['slug'],
                'name': row['name'],
                'state': row.get('state'),
                'lat': float(row['lat']),
                'lon': float(row['lon']),
                'elevation_m': row.get('elevation_m'),
                'lgd_code': row.get('lgd_code'),
                'hazard_bias': tuple(row.get('hazard_bias') or ()),
                'terrain': 'district',
                'scale': 'district',
            })
        _CACHE['rows'] = rows
        _CACHE['mtime'] = mtime
    return _CACHE['rows'] or []


def available():
    return bool(load())


def as_dicts():
    """Districts when seeded, else the curated regions - never nothing."""
    rows = load()
    if rows:
        return rows
    from .regions import as_dicts as region_dicts
    return region_dicts()


def monitoring_grid():
    """What the agent actually watches.

    Districts plus the curated regions, de-duplicated by proximity: a curated
    city point sitting inside its own district would otherwise produce two
    near-identical rows in the watch list for the same weather.
    """
    from .regions import as_dicts as region_dicts

    districts = load()
    regions = region_dicts()
    if not districts:
        return regions

    from .advect import _haversine_km

    grid = list(districts)
    for region in regions:
        too_close = any(
            _haversine_km(region['lat'], region['lon'], d['lat'], d['lon'])
            <= agent_config.DISTRICT_DEDUPE_KM
            for d in districts)
        if not too_close:
            grid.append(dict(region, scale='region'))
    return grid
