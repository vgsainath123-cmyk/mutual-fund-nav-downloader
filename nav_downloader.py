
print("NAV download job started...")

import pandas as pd
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------- SETTINGS ---------------- #
MAX_WORKERS = 8          # 8–10 is safe
SAVE_FOLDER = "data/raw_nav"
RETRIES = 3

os.makedirs(SAVE_FOLDER, exist_ok=True)

# ---------------- LOAD FILTERED SCHEMES ---------------- #
schemes = pd.read_csv("data/filtered_schemes.csv")

scheme_codes = schemes["schemeCode"].astype(str).tolist()

print("Total schemes to download:", len(scheme_codes))

# ---------------- SESSION WITH HEADERS ---------------- #
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
})

# ---------------- DOWNLOAD FUNCTION ---------------- #
def fetch_nav(code):
    file_path = f"{SAVE_FOLDER}/{code}.csv"

    # ⭐ Skip if already downloaded (resume support)
    if os.path.exists(file_path):
        return f"Skipped {code}"

    url = f"https://api.mfapi.in/mf/{code}"

    for attempt in range(RETRIES):
        try:
            r = session.get(url, timeout=20)

            if r.status_code != 200:
                raise Exception("Bad response")

            data = r.json()

            if "data" not in data:
                raise Exception("No NAV data")

            df = pd.DataFrame(data["data"])
            df["scheme_code"] = code

            df.to_csv(file_path, index=False)
            return f"Downloaded {code}"

        except Exception:
            time.sleep(2)

    return f"Failed {code}"

# ---------------- PARALLEL EXECUTION ---------------- #
start = time.time()

results = []
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(fetch_nav, code) for code in scheme_codes]

    for i, f in enumerate(as_completed(futures), 1):
        result = f.result()
        print(f"[{i}/{len(scheme_codes)}] {result}")

print("\nDownload finished in %.2f minutes" % ((time.time()-start)/60))


print("NAV download completed!")