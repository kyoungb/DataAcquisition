import pandas as pd
import requests
from pathlib import Path

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------


DOWNLOAD_URL = None  # e.g. "https://data.un.org/Handlers/DownloadHandler.ashx?..."

RAW_PATH = Path("contraceptive_prevalence_raw.csv")
CLEAN_PATH = Path("contraceptive_prevalence_clean.csv")

# ------------------------------------------------------------------
# (A) Optional: download CSV from UNdata if URL is provided
# ------------------------------------------------------------------

if DOWNLOAD_URL is not None:
    print("Downloading contraception CSV from UNdata...")
    resp = requests.get(DOWNLOAD_URL)
    resp.raise_for_status()
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_bytes(resp.content)
    print(f"Saved raw CSV to {RAW_PATH}")
else:
    print("SKIPPING download (DOWNLOAD_URL is None). "
          "Assuming you already saved the CSV to data/raw/contraceptive_prevalence_raw.csv")

print(f"Loading raw contraception data from {RAW_PATH} ...")
cpr_raw = pd.read_csv(RAW_PATH)

print("Raw columns:", list(cpr_raw.columns))
print(cpr_raw.head())

# Keep only female reproductive-age rows
female_mask = cpr_raw["Subgroup"].astype(str).str.contains("Female", case=False, na=False)
cpr = cpr_raw.loc[female_mask].copy()

# Keep the most relevant columns
cpr = cpr[["Country or Area", "Subgroup", "Year", "Value"]]

cpr = cpr.rename(columns={
    "Country or Area": "country",
    "Value": "contraceptive_prevalence_pct"
})

# Clean country strings
cpr["country"] = (
    cpr["country"]
    .str.replace(r"\[.*?\]", "", regex=True)   # remove any footnote markers
    .str.strip()
)

# Convert numeric
cpr["contraceptive_prevalence_pct"] = pd.to_numeric(
    cpr["contraceptive_prevalence_pct"], errors="coerce"
)

# Drop rows with no country or no value
cpr = cpr.dropna(subset=["country", "contraceptive_prevalence_pct"])

print("After cleaning:")
print(cpr.head())
print("Rows:", len(cpr))

country_fix = {
    "United States of America": "United States",
    "Russian Federation": "Russia",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Iran (Islamic Republic of)": "Iran",
    "Lao People's Democratic Republic": "Laos",
    "Micronesia (Federated States of)": "Micronesia",
    "Republic of Korea": "South Korea",
    "United Republic of Tanzania": "Tanzania",
    "Viet Nam": "Vietnam",
    "State of Palestine": "Palestine",

}

cpr["country"] = cpr["country"].replace(country_fix)

cpr = cpr[["country", "contraceptive_prevalence_pct"]]

CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
cpr.to_csv(CLEAN_PATH, index=False)
print(f"Saved cleaned contraception data to {CLEAN_PATH}")