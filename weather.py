#!/usr/bin/env python3
"""Pune weather watch — free, no-key weather via Open-Meteo.

Fetches the current weather for Pune (18.52, 73.85) from Open-Meteo, a
free weather API that requires no API key and no account.

Fallback, stated plainly: if the API is unreachable, this script does NOT
invent weather numbers. It prints a clear fallback message and exits 0
with no forecast, so a caller can retry later. No cached or fake forecast
is ever presented as live weather.

Usage:
  python3 weather.py
  python3 weather.py --json
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

URL = ("https://api.open-meteo.com/v1/forecast?"
       "latitude=18.52&longitude=73.85&current="
       "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
       "&timezone=Asia%2FKolkata")

CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Drizzle",
    55: "Dense drizzle", 61: "Slight rain", 63: "Rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Snow", 75: "Heavy snow", 80: "Slight rain showers",
    81: "Rain showers", 82: "Violent rain showers", 95: "Thunderstorm",
    96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "sahil-pune-weather-watch"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def main(argv=None):
    p = argparse.ArgumentParser(description="Current weather for Pune (Open-Meteo, no key).")
    p.add_argument("--json", action="store_true", help="Print raw current-weather JSON instead of a summary")
    args = p.parse_args(argv)
    try:
        data = fetch()
    except urllib.error.HTTPError as e:
        print(f"FALLBACK: Open-Meteo returned HTTP {e.code} — live weather unavailable. "
              "No forecast is shown, because no real data was received. Please retry later.")
        return 0
    except Exception as e:
        print(f"FALLBACK: Could not reach Open-Meteo ({e}) — live weather unavailable. "
              "No forecast is shown, because no real data was received. Please retry later.")
        return 0
    cur = data.get("current", {})
    if args.json:
        print(json.dumps(cur, indent=2))
        return 0
    print("Pune — current weather (Open-Meteo, no key)")
    print(f"  Time:        {cur.get('time', '—')}")
    print(f"  Temperature: {cur.get('temperature_2m', '—')} °C")
    print(f"  Humidity:    {cur.get('relative_humidity_2m', '—')}%")
    print(f"  Condition:   {CODES.get(cur.get('weather_code'), '—')} (code {cur.get('weather_code', '—')})")
    print(f"  Wind:        {cur.get('wind_speed_10m', '—')} km/h")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
