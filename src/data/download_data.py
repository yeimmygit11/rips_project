import requests
import pandas as pd
import os

API_URL = "https://www.datos.gov.co/resource/4k9h-8qiu.json"
PAGE_SIZE = 1000  # maximum number of rows you can request per page
OFFSET = 0
MAX_ROWS = 50000  # maximum number of rows to download

all_data = []

print("📡 Connecting to the API and downloading data...")

while True:
    params = {
        "$limit": PAGE_SIZE,
        "$offset": OFFSET
    }

    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        print(f"❌ Request error: {response.status_code}")
        print(response.text)
        break

    page_data = response.json()

    if not page_data:
        print("✅ Download complete: no more data available.")
        break

    all_data.extend(page_data)
    print(f"📄 Page downloaded: {OFFSET} - {OFFSET + PAGE_SIZE} ({len(page_data)} rows)")

    OFFSET += PAGE_SIZE

    if OFFSET >= MAX_ROWS:
        print("⚠️ Row limit reached (MAX_ROWS)")
        break

# Save the data
if all_data:
    df = pd.DataFrame(all_data)

    # Create the folder if it doesn't exist
    os.makedirs("data/raw", exist_ok=True)

    df.to_csv("data/raw/raw_data.csv", index=False)
    print(f"✅ File saved to data/raw/raw_data.csv ({len(df)} rows)")
