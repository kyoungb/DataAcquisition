import pandas as pd

mmr = pd.read_csv("data/raw/maternal_mortality_raw.csv")
contracept = pd.read_csv("data/raw/contraceptive_prevalence_raw.csv")
teen = pd.read_csv("data/raw/adolescent_birth_raw.csv")
lifeexp = pd.read_csv("data/raw/female_life_expectancy_raw.csv")
gdp = pd.read_csv("data/raw/gdp_per_capita_latest.csv")

country_fix = {
    "United States of America": "United States",
    "Russian Federation": "Russia",
    # add more as needed
}

for df in [mmr, contracept, teen, lifeexp, gdp]:
    df["country"] = df["country"].replace(country_fix)
    df["country"] = df["country"].str.strip()

df = mmr.merge(contracept[["country", "contraceptive_prevalence_pct"]],
               on="country", how="inner")

df = df.merge(teen[["country", "adolescent_birth_rate_per_1000"]],
              on="country", how="inner")

df = df.merge(lifeexp[["country", "female_life_expectancy"]],
              on="country", how="inner")

df = df.merge(gdp[["country", "gdp_per_capita_usd"]],
              on="country", how="inner")

df.shape  # should be (>=200, >=6)

region_map = {
    # small dict mapping country to region (you can hand-build or pull from another API)
    "United States": "North America",
    # ...
}
df["region"] = df["country"].map(region_map)

df.to_csv("data/processed/womens_health_econ.csv", index=False)
