# pune-weather-watch

New work built for Sahil Sah's profile (2026-10-30). Not copied from another project.

A Python script that shows the current weather for Pune using Open-Meteo,
a free weather API that needs no API key and no account.

## What it actually does

- Fetches current temperature, humidity, weather condition and wind speed for Pune (18.52, 73.85)
- Prints a plain summary, or `--json` for the raw current-weather object

## Fallback (honest)

If Open-Meteo is unreachable or returns an error, the script prints a clear
fallback message and shows **no forecast**. It never invents weather numbers
and never presents cached data as live.

## How to run

Requires Python 3.10+ (standard library only).

```bash
cd pune-weather-watch
python3 weather.py
python3 weather.py --json
```
