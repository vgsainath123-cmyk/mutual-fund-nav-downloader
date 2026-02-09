import pandas as pd

CSV_PATH = "data/processed/master_nav_database.csv"
OUT_PATH = "data/processed/schemes.json"

print("📂 Reading CSV...")
df = pd.read_csv(CSV_PATH, usecols=["scheme_code", "scheme_name"])

print("🧹 Dropping duplicates...")
df = df.drop_duplicates()

print("💾 Saving schemes.json ...")
df.to_json(OUT_PATH, orient="records")

print("✅ schemes.json created successfully")
