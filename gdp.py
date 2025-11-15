import requests
import pandas as pd

INDICATOR = "NY.GDP.PCAP.CD"  # GDP per capita (current US$)
URL = f"http://api.worldbank.org/v2/country/all/indicator/{INDICATOR}?format=json&per_page=20000"

resp = requests.get(URL)
resp.raise_for_status()
data = resp.json()

meta, records = data[0], data[1]
gdp_df = pd.json_normalize(records)

# Keep the latest year for each country
gdp_df = gdp_df.rename(columns={
    "country.value": "country",
    "value": "gdp_per_capita_usd",
    "date": "year"
})

# Drop non-countries, missing values, etc.
gdp_df = gdp_df[gdp_df["gdp_per_capita_usd"].notna()]
gdp_df["gdp_per_capita_usd"] = gdp_df["gdp_per_capita_usd"].astype(float)


gdp_latest = (
    gdp_df.sort_values(["country", "year"], ascending=[True, False])
          .drop_duplicates(subset=["country"])
)

gdp_latest.to_csv("gdp_per_capita_latest.csv", index=False)
