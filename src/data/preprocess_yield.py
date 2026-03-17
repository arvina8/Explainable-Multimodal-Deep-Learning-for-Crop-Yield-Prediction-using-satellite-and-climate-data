# src/data/preprocess_yield.py
# Preprocess USDA yield data into annual summaries

import pandas as pd
import os
import glob

RAW_DIR = "data/raw/yield"
OUTPUT_DIR = "data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess_yield(raw_dir):
    files = glob.glob(os.path.join(raw_dir, "*_yield.csv"))
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)

    # Rename columns to standard names
    combined = combined.rename(columns={
        "state_name": "state",
        "county_name": "county",
        "commodity_desc": "crop",
        "Value": "yield_bu_acre"
    })

    # Keep only relevant columns
    combined = combined[["year", "state", "county", "crop", "yield_bu_acre"]]

    # Convert year and yield to numeric
    combined["year"] = combined["year"].astype(int)
    combined["yield_bu_acre"] = pd.to_numeric(combined["yield_bu_acre"], errors="coerce")
    combined = combined.dropna(subset=["yield_bu_acre"])

    # Aggregate county → state annual averages
    annual = combined.groupby(["state", "year", "crop"]).agg({
        "yield_bu_acre": "mean"
    }).reset_index()

    out_path = os.path.join(OUTPUT_DIR, "yield_annual.csv")
    annual.to_csv(out_path, index=False)
    print(f"✓ Annual yield dataset saved to {out_path}")
    print(f" Records: {len(annual)} | States: {annual['state'].nunique()} | Years: {annual['year'].nunique()} | Crops: {annual['crop'].nunique()}")

if __name__ == "__main__":
    preprocess_yield(RAW_DIR)
