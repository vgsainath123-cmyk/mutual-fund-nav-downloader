import os
import gdown

DATA_PATH = "data/processed/master_nav_database.csv"

def download_database():
    if os.path.exists(DATA_PATH):
        print("✅ Database already exists")
        return

    print("⬇️ Downloading NAV database from Google Drive...")

    os.makedirs("data/processed", exist_ok=True)

    file_id = "1i0inzT1JH5zGE3-WCjMc4BD0RdkXVI_A"

    url = f"https://drive.google.com/uc?id={file_id}"

    gdown.download(url, DATA_PATH, quiet=False)

    print("✅ Download complete")
