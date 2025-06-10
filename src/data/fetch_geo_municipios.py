import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # Go up two levels to project root
raw_file = BASE_DIR / 'data' / 'raw' / 'raw_geo_municipios.csv'


# Endpoint
url = "https://www.datos.gov.co/resource/vafm-j2df.json"

params = {
    "$limit": 5000,
    "$$app_token": ""
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    print(f"Got {len(df) } records.")
    
    # Save CSV
    df.to_csv(raw_file, index=False)
else:
    print(f"Error requesting the API: {response.status_code}")
