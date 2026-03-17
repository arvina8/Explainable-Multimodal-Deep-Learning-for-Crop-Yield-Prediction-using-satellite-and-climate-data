# src/data/preprocess_climate.py

import pandas as pd
import os

RAW_PATH = "data/raw/climate/all_states_climate.csv"
OUTPUT_DIR = "data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess_climate(raw_path):
    df = pd.read_csv(raw_path)

    # Ensure 'year' is integer
    df["year"] = df["year"].astype(str).str.strip()

    # Extract year and month from YYYYMM
    df["year_num"] = df["year"].str[:4].astype(int)
    df["month"] = df["year"].str[4:].astype(int)

    # Aggregate monthly → annual summaries
    annual = df.groupby(["state", "year_num"]).agg({
        "temp_mean_c": "mean",
        "temp_max_c": "mean",
        "temp_min_c": "mean",
        "precipitation_mm": "sum",   # precipitation summed over months
        "humidity_pct": "mean",
        "solar_radiation": "mean",
        "wind_speed_ms": "mean"
    }).reset_index()

    # Save processed dataset
    out_path = os.path.join(OUTPUT_DIR, "climate_annual.csv")
    annual.to_csv(out_path, index=False)
    print(f"✓ Annual climate dataset saved to {out_path}")
    print(f" Records: {len(annual)} | States: {annual['state'].nunique()} | Years: {annual['year_num'].nunique()}")

if __name__ == "__main__":
    preprocess_climate(RAW_PATH)
