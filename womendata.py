import requests
import pandas as pd
from io import StringIO

URL = "https://en.wikipedia.org/wiki/List_of_countries_by_maternal_mortality_ratio"

HEADERS = {
    "User-Agent": "Stat386Project/1.0 (contact: kyoungb@byu.edu)"
}

# 1. Get the HTML
resp = requests.get(URL, headers=HEADERS)
resp.raise_for_status()

# 2. Parse all tables from the HTML
tables = pd.read_html(StringIO(resp.text))
print(f"Found {len(tables)} tables")

# 3. Take the first table (the one you printed)
mmr = tables[0].copy()
print(mmr.head())

# 4. Standardize column names: Location -> country
mmr = mmr.rename(columns={"Location": "country"})

# 5. Clean country names (remove footnote markers like [a], *, etc.)
mmr["country"] = (
    mmr["country"]
    .str.replace(r"\[.*\]", "", regex=True)   # remove [..] footnotes
    .str.replace("\u202f*", "", regex=False)  # remove narrow no-break space + *
    .str.strip()
)

# 6. Convert year columns to numeric
year_cols = ["2020", "2010", "2000", "1985"]
for col in year_cols:
    if col in mmr.columns:
        mmr[col] = pd.to_numeric(mmr[col], errors="coerce")

# 7. (Optional) Drop regional aggregates like "Africa (WHO)"
mmr = mmr[~mmr["country"].str.contains(r"\(WHO\)", na=False)]

print("Cleaned MMR data:")
print(mmr.head())
print(mmr.shape)

# 8. Save to CSV
mmr.to_csv("maternal_mortality_mmr.csv", index=False)
print("Saved to maternal_mortality_mmr.csv")

