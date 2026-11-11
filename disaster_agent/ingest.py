"""Step 1 - INGEST: live wind, cloud and heat signal for every watched region.

This is deliberately **not** a scrape of the Windy iframes on the analyst
dashboard. Windy's embed is a cross-origin canvas - there is no pixel or DOM
access to "read wind direction off the map" even in principle. Instead this
adapter goes to Open-Meteo (the same class of open numerical-weather-model
data Windy's own temperature/wind, satellite and fire-danger layers are
rendered from), keyless and free, for the fields that matter to the three
panels:

  * live temperature map / wind        -> wind_speed_10m, wind_direction_10m
  * live satellite view (clouds)       -> cloud_cover, precipitation
  * fire danger map                    -> Fosberg Fire Weather Index, derived
                                           from temperature, humidity and wind

One HTTP call covers every region: Open-Meteo accepts comma-separated
lat/lon lists in a single request.
"""

import math
import time

import requests

from . import config as agent_config
from .regions import as_dicts

CURRENT_FIELDS = (
    'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,'
    'cloud_cover,precipitation,surface_pressure,weather_code'
)

# Same list minus weather_code, which has no part in any hazard score.
HOURLY_FIELDS = (
    'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,'
    'cloud_cover,precipitation,surface_pressure'
)


# Last fetch's coverage. A partial fetch and a complete one used to be
# indistinguishable downstream: the panel said "watching 400 districts" and
# looked perfectly healthy while 394 were missing because the upstream free
# tier had been exhausted. The shortfall is now reported, not swallowed.
_COVERAGE = {'requested': 0, 'received': 0, 'error': None}


def last_coverage():
    return dict(_COVERAGE)


def fetch_region_signals(regions=None, timeout=None):
    """One live signal dict per watched point. Never raises - a failed HTTP

    call degrades to an empty list, and the caller (the projection step)
    treats no signal as no hotspot rather than crashing the cycle.

    Batched: the grid is ~800 districts now, and Open-Meteo's multi-point
    request is capped by URI length - measured directly, 200 points answered
    in 1.4s and 400 returned HTTP 414. One failed batch loses its own points,
    not the whole cycle.
    """
    if regions is None:
        from .districts import monitoring_grid
        regions = monitoring_grid()
    if not regions:
        return []

    batch = max(1, agent_config.INGEST_BATCH_SIZE)
    if len(regions) > batch:
        _COVERAGE.update({'requested': len(regions), 'received': 0, 'error': None})
        signals = []
        for start in range(0, len(regions), batch):
            chunk = regions[start:start + batch]
            # Open-Meteo rate-limits a rapid burst of batches. Without a retry
            # this silently returned only the first two batches of six - and
            # because the grid is ordered by state, that looked like "every
            # hazard in India is in Chhattisgarh" rather than like a failure.
            got = None
            for attempt in range(3):
                got = fetch_region_signals(chunk, timeout=timeout)
                if got:
                    break
                time.sleep(agent_config.INGEST_RETRY_BACKOFF_S * (attempt + 1))
            signals.extend(got or [])
            # Space the batches. Open-Meteo throttles a rapid burst far more
            # readily than it throttles the same number of calls spread out,
            # and the whole grid only has to be fetched once per cycle.
            time.sleep(agent_config.INGEST_BATCH_PAUSE_S)
        _COVERAGE['received'] = len(signals)
        if len(signals) < len(regions):
            _COVERAGE['error'] = (
                'Only %d of %d watched points returned data. The weather API '
                'refused the rest - usually its hourly free-tier limit. The '
                'ranking below covers the points that answered, not the whole '
                'grid.' % (len(signals), len(regions)))
        return signals

    params = {
        'latitude': ','.join('%.4f' % r['lat'] for r in regions),
        'longitude': ','.join('%.4f' % r['lon'] for r in regions),
        'current': CURRENT_FIELDS,
        # Every field `advect.source_strengths()` reads, not just the two the
        # 3-hour rain look-ahead needed. window.py re-runs that same scoring
        # function over these hours to work out when a hazard starts, peaks
        # and eases - which it cannot do from rain and cloud alone.
        'hourly': HOURLY_FIELDS,
        'forecast_days': agent_config.FORECAST_DAYS,
        'timezone': 'UTC',
    }

    try:
        response = requests.get(
            agent_config.FORECAST_URL, params=params,
            timeout=timeout or agent_config.HTTP_TIMEOUT_S)
        response.raise_for_status()
        payload = response.json()
    except Exception:  # noqa: BLE001 - a bad ingest must never kill the cycle
        return []

    entries = payload if isinstance(payload, list) else [payload]
    signals = []
    for region, entry in zip(regions, entries):
        signal = _parse_entry(region, entry)
        if signal is not None:
            signals.append(signal)

    # One FIRMS fetch for the whole country, reused across every point in this
    # batch - not one request per district against a rate-limited API.
    try:
        from . import firms

        rows = firms.detections()
        if rows:
            for signal in signals:
                signal['fire_detections'] = firms.summarise_near(
                    signal['lat'], signal['lon'], rows=rows)
    except Exception:  # noqa: BLE001 - observed fire is an enhancement, never a blocker
        pass

    return signals


def _parse_entry(region, entry):
    current = entry.get('current') or {}
    if not current:
        return None

    temperature_c = current.get('temperature_2m')
    humidity_pct = current.get('relative_humidity_2m')
    wind_speed_kmh = current.get('wind_speed_10m')
    wind_dir_deg = current.get('wind_direction_10m')
    cloud_cover_pct = current.get('cloud_cover')
    precipitation_mm = current.get('precipitation') or 0.0
    surface_pressure_hpa = current.get('surface_pressure')

    signal = dict(region)
    signal.update({
        'temperature_c': temperature_c,
        'humidity_pct': humidity_pct,
        'wind_speed_kmh': wind_speed_kmh,
        'wind_dir_deg': wind_dir_deg,
        'cloud_cover_pct': cloud_cover_pct,
        'precipitation_mm': precipitation_mm,
        'surface_pressure_hpa': surface_pressure_hpa,
        'weather_code': current.get('weather_code'),
        'rain_forecast_3h_mm': _rain_ahead(entry, hours=3),
        'fire_weather_index': fosberg_fire_weather_index(
            temperature_c, humidity_pct, wind_speed_kmh),
        # Observed fire, kept separate from the modelled index above. One is
        # "how readily would fire spread here", the other is "something is
        # burning here" - they must stay distinguishable in the payload even
        # though the score combines them.
        'fire_detections': None,
        # Carried through untouched so window.py can re-score each hour with
        # the same function that produced the headline number above.
        'hourly': entry.get('hourly') or {},
        'observed_at': current.get('time'),
    })
    return signal


def _rain_ahead(entry, hours):
    hourly = (entry.get('hourly') or {})
    values = hourly.get('precipitation') or []
    times = hourly.get('time') or []
    current_time = (entry.get('current') or {}).get('time')
    start = 0
    if current_time and times:
        prefix = current_time[:13]
        for i, stamp in enumerate(times):
            if stamp[:13] == prefix:
                start = i
                break
    window = values[start:start + hours]
    return float(sum(v or 0.0 for v in window))


# --- Fosberg Fire Weather Index -----------------------------------------------
# Fosberg (1970), the standard US fire-weather formula: moisture content from
# temperature + relative humidity, combined with wind speed. Raw FFWI rarely
# exceeds ~110 in extreme conditions, so it is rescaled to a 0-100 sub-score
# the same way every other sub-score in this app is (a declared assumption,
# named here so it can be argued with).
FFWI_RAW_MAX = 100.0


def fosberg_fire_weather_index(temperature_c, humidity_pct, wind_speed_kmh):
    """0-100 fire-danger sub-score, or None if inputs are missing."""
    if temperature_c is None or humidity_pct is None or wind_speed_kmh is None:
        return None

    temp_f = temperature_c * 9.0 / 5.0 + 32.0
    rh = max(0.0, min(100.0, humidity_pct))
    wind_mph = wind_speed_kmh * 0.621371

    if rh < 10.0:
        m = 0.03229 + 0.281073 * rh - 0.000578 * rh * temp_f
    elif rh < 50.0:
        m = 2.22749 + 0.160107 * rh - 0.014784 * temp_f
    else:
        m = 21.0606 + 0.005565 * (rh ** 2) - 0.00035 * rh * temp_f - 0.483199 * rh

    m_ratio = m / 30.0
    n = 1.0 - 2.0 * m_ratio + 1.5 * (m_ratio ** 2) - 0.5 * (m_ratio ** 3)
    n = max(0.0, n)

    raw = n * math.sqrt(1.0 + wind_mph ** 2) / 0.3002
    return max(0.0, min(100.0, raw / FFWI_RAW_MAX * 100.0))
