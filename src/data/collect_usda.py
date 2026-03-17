# src/data/collect_usda.py
# USDA NASS Crop Yield Data Collector

import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("USDA_API_KEY")

def fetch_usda_yield_data(api_key, crop="CORN", year_start=2010, year_end=2023):
    """
    Fetch crop yield data from USDA NASS API
    Crops: CORN, SOYBEANS, WHEAT, RICE, COTTON
    """
    base_url = "https://quickstats.nass.usda.gov/api/api_GET/"
    params = {
        "key"              : api_key,
        "commodity_desc"   : crop,
        "statisticcat_desc": "YIELD",
        "agg_level_desc"   : "COUNTY",
        "year__GE"         : year_start,
        "year__LE"         : year_end,
        "format"           : "JSON"
    }

    print(f"Fetching {crop} yield data from USDA NASS...")
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        df   = pd.DataFrame(data["data"])
        print(f"✅ Fetched {len(df)} records for {crop}")
        return df
    else:
        print(f"❌ Error: {response.status_code}")
        return None


def save_yield_data(df, crop):
    """Save yield data to raw data folder"""
    os.makedirs("data/raw/yield", exist_ok=True)
    path = f"data/raw/yield/{crop.lower()}_yield.csv"
    df.to_csv(path, index=False)
    print(f"✅ Saved to {path}")


if __name__ == "__main__":
    crops = ["CORN", "SOYBEANS", "WHEAT"]

    for crop in crops:
        df = fetch_usda_yield_data(API_KEY, crop=crop)
        if df is not None:
            save_yield_data(df, crop)