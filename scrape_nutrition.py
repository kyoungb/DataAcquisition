import requests
import pandas as pd

URL = "https://en.wikipedia.org/wiki/List_of_countries_by_maternal_mortality_ratio"

resp = requests.get(URL)
resp.raise_for_status()

tables = pd.read_html(resp.text)
len(tables), type(tables[0])

mmr_raw = tables[0]  # adjust after inspecting
mmr = (
    mmr_raw
    .rename(columns={
        "Country or territory": "country",
        "Maternal mortality ratio (MMR, deaths per 100,000 live births)": "maternal_mortality_per_100k"
        # adjust names to whatever the table actually uses
    })
)

# Clean country names, remove footnote markers, drop aggregates, cast numeric
mmr["country"] = mmr["country"].str.replace(r"\[.*\]", "", regex=True).str.strip()
mmr["maternal_mortality_per_100k"] = (
    mmr["maternal_mortality_per_100k"]
    .replace("—", pd.NA)
    .astype("float")
)

mmr.to_csv("data/raw/maternal_mortality_raw.csv", index=False)
