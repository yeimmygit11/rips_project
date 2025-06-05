import requests
import pandas as pd
import os
import time

API_URL = "https://www.datos.gov.co/resource/4k9h-8qiu.json"
PAGE_SIZE = 1000
MAX_ROWS = 10_000_000
DEPARTMENT = "05 - Antioquia"
YEARS = [2021]


year_filter = " OR ".join([f"a_o='{year}'" for year in YEARS])
where_clause = f"Departamento='{DEPARTMENT}' AND ({year_filter})"

all_data = []
offset = 0

print(f"\n📡 Downloading data for Departamento: {DEPARTMENT} and Years: {YEARS}")

while True:
    params = {
        "$limit": PAGE_SIZE,
        "$offset": offset,
        "$where": where_clause
    }

    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        print(f"❌ Request error: {response.status_code}")
        print(response.text)
        break

    page_data = response.json()
    if not page_data:
        print("✅ Download complete: no more data.")
        break

    all_data.extend(page_data)
    print(f"📄 Rows downloaded: {offset} - {offset + PAGE_SIZE} ({len(page_data)} rows)")
    offset += PAGE_SIZE
    time.sleep(0.3)  # delay to avoid API throttling

    if offset >= MAX_ROWS:
        print("⚠️ Row limit reached.")
        break

# Guardar resultados
if all_data:
    df = pd.DataFrame(all_data)
    os.makedirs("data/raw", exist_ok=True)
    department_filename = DEPARTMENT.replace(" ", "_")
    filename = f"data/raw/{department_filename}_{'_'.join(map(str, YEARS))}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ File saved: {filename} ({len(df)} rows)")
