import pandas as pd

mmr = pd.read_csv("maternal_mortality_mmr.csv")
contracept = pd.read_csv("contraceptive_prevalence_clean.csv")
gdp = pd.read_csv("gdp_per_capita_latest.csv")

country_fix = {
    "United States of America": "United States",
    "Russian Federation": "Russia",
    "Bahamas, The": "Bahamas",
    "Brunei Darussalam": "Brunei",
    "Cabo Verde": "Cape Verde",
    "Congo, Rep.": "Congo",
    "Congo, Dem. Rep.": "DR Congo",
    "Czechia": "Czech Republic",
    "Egypt, Arab Rep.": "Egypt",
    "Gambia, The": "Gambia",
    "Iran, Islamic Rep.": "Iran",
    "Cote d'Ivoire": "Ivory Coast",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Lao PDR": "Laos",
    "Micronesia, Fed. Sts.": "Micronesia",
    "West Bank and Gaza": "Palestine",
    "Puerto Rico (US)": "Puerto Rico",
    "St. Lucia": "Saint Lucia",
    "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "Slovak Republic": "Slovakia",
    "Somalia, Fed. Rep.": "Somalia",
    "Korea, Rep.": "South Korea",
    "Syrian Arab Republic": "Syria",
    "Sao Tome and Principe": "São Tomé and Príncipe",
    "Turkiye": "Turkey",
    "Venezuela, RB": "Venezuela",
    "Viet Nam": "Vietnam",
    "Yemen, Rep.": "Yemen",
}


for df in [mmr, contracept, gdp]:
    df["country"] = df["country"].replace(country_fix)
    df["country"] = df["country"].str.strip()

df = mmr.merge(contracept[["country", "contraceptive_prevalence_pct"]],
               on="country", how="inner")

df = df.merge(gdp[["country", "gdp_per_capita_usd"]],
              on="country", how="inner")

df.shape  # should be (>=200, >=6)

region_map = {
    # Americas
    "United States": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    "Brazil": "South America",
    "Argentina": "South America",
    "Chile": "South America",
    "Colombia": "South America",
    "Peru": "South America",
    "Venezuela": "South America",

    # Europe
    "United Kingdom": "Europe",
    "France": "Europe",
    "Germany": "Europe",
    "Italy": "Europe",
    "Spain": "Europe",
    "Portugal": "Europe",
    "Netherlands": "Europe",
    "Belgium": "Europe",
    "Sweden": "Europe",
    "Norway": "Europe",
    "Denmark": "Europe",
    "Finland": "Europe",
    "Switzerland": "Europe",
    "Austria": "Europe",
    "Czech Republic": "Europe",
    "Slovakia": "Europe",
    "Russia": "Europe/Asia",

    # Africa
    "South Africa": "Africa",
    "Nigeria": "Africa",
    "Egypt": "Africa",
    "Kenya": "Africa",
    "Ghana": "Africa",
    "Ethiopia": "Africa",
    "Somalia": "Africa",
    "Congo": "Africa",
    "DR Congo": "Africa",

    # Asia
    "China": "Asia",
    "India": "Asia",
    "Japan": "Asia",
    "South Korea": "Asia",
    "North Korea": "Asia",
    "Vietnam": "Asia",
    "Thailand": "Asia",
    "Laos": "Asia",
    "Cambodia": "Asia",
    "Iran": "Asia",
    "Iraq": "Asia",
    "Yemen": "Asia",
    "Saudi Arabia": "Asia",
    "Turkey": "Asia/Europe",

    # Oceania
    "Australia": "Oceania",
    "New Zealand": "Oceania",
    "Micronesia": "Oceania",
    "Papua New Guinea": "Oceania",
}

df["region"] = df["country"].map(region_map)

df.to_csv("womens_health_econ.csv", index=False)
