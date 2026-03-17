# src/data/merge_climate_yield.py

import pandas as pd
import os

CLIMATE_PATH = "data/processed/climate_annual.csv"
YIELD_PATH = "data/processed/yield_annual.csv"
OUTPUT_DIR = "data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def merge_datasets(climate_path, yield_path):
    climate = pd.read_csv(climate_path)
    yield_data = pd.read_csv(yield_path)

    # Rename climate year column
    climate = climate.rename(columns={"year_num": "year"})

    # Normalize state names (upper case for both)
    climate["state"] = climate["state"].str.upper()
    yield_data["state"] = yield_data["state"].str.upper()

    # Merge on state + year
    merged = pd.merge(
        yield_data,
        climate,
        on=["state", "year"],
        how="inner"
    )

    out_path = os.path.join(OUTPUT_DIR, "climate_yield_merged.csv")
    merged.to_csv(out_path, index=False)
    print(f"✓ Merged dataset saved to {out_path}")
    print(f" Records: {len(merged)} | States: {merged['state'].nunique()} | Years: {merged['year'].nunique()} | Crops: {merged['crop'].nunique()}")

if __name__ == "__main__":
    merge_datasets(CLIMATE_PATH, YIELD_PATH)
