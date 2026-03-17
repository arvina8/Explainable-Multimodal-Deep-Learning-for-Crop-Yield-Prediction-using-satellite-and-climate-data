# src/data/collect_climate.py
# NASA POWER Climate Data Collector (fixed)

import requests
import pandas as pd
import os
import time

# Output directory
OUTPUT_DIR = "data/raw/climate"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Year range
START_YEAR = 2010
END_YEAR = 2023

# Climate parameters to collect
PARAMETERS = [
    "T2M",                # Mean Temperature at 2m (°C)
    "T2M_MAX",            # Max Temperature
    "T2M_MIN",            # Min Temperature
    "PRECTOTCORR",        # Precipitation (mm/day)
    "RH2M",               # Relative Humidity (%)
    "ALLSKY_SFC_SW_DWN",  # Solar Radiation
    "WS2M"                # Wind Speed (m/s)
]

# Major agricultural US states with lat/lon (note negative longitudes!)
LOCATIONS = {
    "Iowa": (41.878, -93.097),
    "Illinois": (40.633, -89.398),
    "Nebraska": (41.492, -99.901),
    "Indiana": (40.267, -86.134),
    "Minnesota": (46.729, -94.685),
    "Kansas": (38.526, -96.726),
    "Ohio": (40.417, -82.907),
    "SouthDakota": (43.969, -99.901),
    "NorthDakota": (47.551, -101.002),
    "Missouri": (38.573, -92.603),
}

def fetch_climate(location_name, lat, lon, start_year, end_year):
    """Fetch climate data from NASA POWER for a given location."""
    print(f"Fetching climate data for {location_name} ... ")

    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    params = {
        "parameters": ",".join(PARAMETERS),
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_year,
        "end": end_year,
        "format": "JSON",
    }

    response = requests.get(url, params=params, timeout=60)

    if response.status_code != 200:
        print(f" ✗ Failed for {location_name}: {response.status_code}")
        return pd.DataFrame()

    data = response.json()
    param_data = data["properties"]["parameter"]

    # Build dataframe
    rows = []
    years = list(param_data[PARAMETERS[0]].keys())
    for year in years:
        row = {
            "year": int(year),
            "state": location_name,
            "latitude": lat,
            "longitude": lon,
        }
        for param in PARAMETERS:
            row[param] = param_data[param].get(year, None)
        rows.append(row)

    df = pd.DataFrame(rows)

    # Rename columns
    df = df.rename(columns={
        "T2M": "temp_mean_c",
        "T2M_MAX": "temp_max_c",
        "T2M_MIN": "temp_min_c",
        "PRECTOTCORR": "precipitation_mm",
        "RH2M": "humidity_pct",
        "ALLSKY_SFC_SW_DWN": "solar_radiation",
        "WS2M": "wind_speed_ms",
    })

    print(f" ✓ {len(df)} monthly records fetched for {location_name}")
    return df

if __name__ == "__main__":
    all_data = []

    for location, (lat, lon) in LOCATIONS.items():
        df = fetch_climate(location, lat, lon, START_YEAR, END_YEAR)
        if not df.empty:
            out_path = os.path.join(OUTPUT_DIR, f"{location.lower()}_climate.csv")
            df.to_csv(out_path, index=False)
            all_data.append(df)
        time.sleep(1)  # polite delay for API

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined.to_csv(os.path.join(OUTPUT_DIR, "all_states_climate.csv"), index=False)
        print(f"\n✓ Combined climate dataset saved!")
        print(f" Total records: {len(combined)}")
        print(f" States covered: {combined['state'].nunique()}")
        print(f" Year range: {combined['year'].min()}-{combined['year'].max()}")
        print(f" Features: {list(combined.columns)}")
