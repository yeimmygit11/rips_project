import pandas as pd
from pathlib import Path
import ftfy

# Function to fix encoding issues using ftfy
def fix_text(text):
    if pd.isna(text):
        return text
    return ftfy.fix_text(str(text))

# Set safe relative paths assuming this script is inside a subfolder of the project
BASE_DIR = Path(__file__).resolve().parents[2]  # Go up two levels to project root
raw_file = BASE_DIR / 'data' / 'raw' / '05_-_Antioquia_2021.csv'
output_path = BASE_DIR / 'data' / 'interim' / '05_-_Antioquia_2021_clean.csv'

# Read the CSV (latin1 works better for your data)
df = pd.read_csv(raw_file, encoding='latin1')

# Normalize column names: lowercase, strip spaces, replace spaces with underscores
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Split composite columns into separate code and name columns
df[['codigo_departamento', 'nombre_departamento']] = df['departamento'].str.extract(r'^(\d+)\s*-\s*(.+)$')
df.drop(columns=['departamento'], inplace=True)

df[['codigo_municipio', 'nombre_municipio']] = df['municipio'].str.extract(r'^(\d+)\s*-\s*(.+)$')
df.drop(columns=['municipio'], inplace=True)

df[['codigo_diagnostico', 'n_diagnostico']] = df['diagnostico'].str.extract(r'^([A-Z0-9]+)\s*-\s*(.+)$')
df.drop(columns=['diagnostico'], inplace=True)

# Fix encoding issues in extracted name columns using ftfy
df['nombre_departamento'] = df['nombre_departamento'].apply(fix_text)
df['nombre_municipio'] = df['nombre_municipio'].apply(fix_text)
df['n_diagnostico'] = df['n_diagnostico'].apply(fix_text)

# Optional: if you want to remove accents, you can still use unicodedata.normalize here
import unicodedata

def clean_text(text):
    if pd.isna(text):
        return text
    text = str(text)
    text = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in text if not unicodedata.combining(c)])

df['nombre_departamento'] = df['nombre_departamento'].apply(clean_text)
df['nombre_municipio'] = df['nombre_municipio'].apply(clean_text)
df['n_diagnostico'] = df['n_diagnostico'].apply(clean_text)

# Check if there are still encoding errors (looking for typical corrupted characters)
errors = df[df['nombre_municipio'].str.contains(r'[Ã�]|\\x', na=False)]
if not errors.empty:
    print("⚠️ Encoding issues found in the following municipalities:")
    print(errors['nombre_municipio'].unique())
else:
    print("✅ All municipality names appear correctly encoded.")

# Save the cleaned file with UTF-8 encoding
df.to_csv(output_path, index=False, encoding='utf-8')
print(f"\n✅ Cleaned file saved at:\n{output_path}")
