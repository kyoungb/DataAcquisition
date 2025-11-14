# src/clean_merge.py

import glob
import pandas as pd


def load_nutrition(pattern="data/raw/nutrition_*.csv") -> pd.DataFrame:
    files = glob.glob(pattern)
    dfs = [pd.read_csv(f) for f in files]
    return pd.concat(dfs, ignore_index=True)


def load_prices(pattern="data/raw/prices_*.csv") -> pd.DataFrame:
    files = glob.glob(pattern)
    dfs = [pd.read_csv(f) for f in files]
    return pd.concat(dfs, ignore_index=True)


def make_master(out_path="data/processed/restaurant_nutrition_prices.csv"):
    nut = load_nutrition()
    prices = load_prices()

    # Basic inner join on chain + item_key
    merged = pd.merge(
        nut,
        prices[["chain", "item_key", "price_usd"]],
        on=["chain", "item_key"],
        how="left",
        validate="m:1",
    )

    # Derived features
    merged["cal_per_dollar"] = merged["calories"] / merged["price_usd"]
    merged["protein_per_dollar"] = merged["protein_g"] / merged["price_usd"]
    merged["protein_density"] = merged["protein_g"] / (merged["calories"] / 100)

    # Simple sanity filters
    merged = merged[merged["calories"].between(10, 3000, inclusive="both")]
    merged = merged[merged["price_usd"].between(0.5, 50, inclusive="both") | merged["price_usd"].isna()]

    merged.to_csv(out_path, index=False)
    print(f"Saved master dataset with {len(merged)} rows to {out_path}")


if __name__ == "__main__":
    make_master()
