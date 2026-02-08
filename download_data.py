import os, gdown

DATA_PATH = "data/processed/master_nav_database.csv"

def download_database():
    if os.path.exists(DATA_PATH) and os.path.getsize(DATA_PATH) > 1000:
        print("✅ Database already exists")
        return True

    os.makedirs("data/processed", exist_ok=True)
    file_id = "1i0inzT1JH5zGE3-WCjMc4BD0RdkXVI_A"
    url = f"https://drive.google.com/uc?id={file_id}"

    print("⬇️ Downloading NAV database...")
    gdown.download(url, DATA_PATH, quiet=False)

    return os.path.exists(DATA_PATH)
