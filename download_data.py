import os
import gdown

DATA_PATH = "data/processed/master_nav_database.csv"
FILE_ID = "1i0inzT1JH5zGE3-WCjMc4BD0RdkXVI_A"

def download_database():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    if os.path.exists(DATA_PATH):
        print("✅ Database already exists")
        return DATA_PATH

    print("⬇️ Downloading NAV database from Google Drive...")

    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, DATA_PATH, quiet=False)

    if not os.path.exists(DATA_PATH):
        raise RuntimeError("❌ Database download failed")

    print("✅ Download complete")
    return DATA_PATH
