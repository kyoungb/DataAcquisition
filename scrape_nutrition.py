# src/scrape_nutrition.py

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (stat386 student project; contact: your_email@byu.edu)"
}

REQUEST_DELAY = 2.0  # seconds


def fetch_html(url: str) -> str:
    """Fetch HTML for a given URL with a polite delay."""
    time.sleep(REQUEST_DELAY)
    resp = requests.get(url, headers=BASE_HEADERS)
    resp.raise_for_status()
    return resp.text


def standardize_item_name(name: str) -> str:
    """Create a simplified key for joining across sources."""
    import re

    s = name.lower()
    s = re.sub(r"\b(small|medium|large|regular)\b", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = " ".join(s.split())
    return s


def parse_fastfoodnutrition_table(html: str, chain_name: str) -> pd.DataFrame:
    """
    Parse a typical nutrition table from fastfoodnutrition.org-style pages.

    Returns a DataFrame with columns:
    chain, item, category, size, calories, protein_g, fat_g, carbs_g
    """
    soup = BeautifulSoup(html, "html.parser")

    # You will likely need to tweak this selector after you inspect the page.
    table = soup.find("table")
    if table is None:
        raise ValueError("No table found on page")

    rows = table.find_all("tr")
    data = []

    # Assume first row is header
    header_cells = [c.get_text(strip=True).lower() for c in rows[0].find_all(["th", "td"])]

    # helper to get index safely
    def idx(colname, default=None):
        for i, h in enumerate(header_cells):
            if colname in h:
                return i
        return default

    idx_item = idx("item")
    idx_cal = idx("cal")
    idx_protein = idx("protein")
    idx_fat = idx("fat")
    idx_carb = idx("carb")
    idx_size = idx("size")
    # category may come from elsewhere – leave as None or infer later

    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue

        def get(i):
            if i is None or i >= len(cells):
                return ""
            return cells[i].get_text(strip=True)

        item = get(idx_item)
        if not item:
            continue

        def to_float(x):
            x = x.replace("g", "").replace("mg", "").strip()
            if x in ("", "-", "—"):
                return None
            try:
                return float(x)
            except ValueError:
                return None

        calories = to_float(get(idx_cal))
        protein_g = to_float(get(idx_protein))
        fat_g = to_float(get(idx_fat))
        carbs_g = to_float(get(idx_carb))
        size = get(idx_size) if idx_size is not None else ""

        data.append(
            {
                "chain": chain_name,
                "item": item,
                "item_key": standardize_item_name(item),
                "category": None,  # you can fill this later if available
                "size": size,
                "calories": calories,
                "protein_g": protein_g,
                "fat_g": fat_g,
                "carbs_g": carbs_g,
            }
        )

    df = pd.DataFrame(data)
    return df


def scrape_chain_nutrition(url: str, chain_name: str, out_path: str):
    html = fetch_html(url)
    df = parse_fastfoodnutrition_table(html, chain_name)
    df["scrape_timestamp"] = pd.Timestamp.utcnow()
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows for {chain_name} to {out_path}")


if __name__ == "__main__":
    # Example usage – you will replace this with a real URL
    example_url = "https://www.example.com/mcdonalds-nutrition"
    scrape_chain_nutrition(example_url, chain_name="McDonalds", out_path="data/raw/nutrition_mcdonalds.csv")
