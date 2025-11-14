# src/scrape_prices.py

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

from src.scrape_nutrition import standardize_item_name

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (stat386 student project; contact: your_email@byu.edu)"
}
REQUEST_DELAY = 2.0


def fetch_html(url: str) -> str:
    time.sleep(REQUEST_DELAY)
    resp = requests.get(url, headers=BASE_HEADERS)
    resp.raise_for_status()
    return resp.text


def parse_price_table(html: str, chain_name: str, city: str = None) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("No price table found")

    rows = table.find_all("tr")
    data = []

    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if len(cells) < 2:
            continue

        item = cells[0].get_text(strip=True)
        price_text = cells[1].get_text(strip=True)

        price_text = price_text.replace("$", "").strip()
        try:
            price = float(price_text)
        except ValueError:
            continue

        data.append(
            {
                "chain": chain_name,
                "city": city,
                "item": item,
                "item_key": standardize_item_name(item),
                "price_usd": price,
            }
        )

    return pd.DataFrame(data)


def scrape_chain_prices(url: str, chain_name: str, city: str, out_path: str):
    html = fetch_html(url)
    df = parse_price_table(html, chain_name, city)
    df["scrape_timestamp"] = pd.Timestamp.utcnow()
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows for {chain_name} ({city}) to {out_path}")


if __name__ == "__main__":
    # Example placeholder
    example_url = "https://www.example.com/mcdonalds-prices-city"
    scrape_chain_prices(example_url, "McDonalds", "Salt Lake City", "data/raw/prices_mcd_slc.csv")
