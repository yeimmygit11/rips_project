import pandas as pd
import os
import re
import ftfy
import chardet
import unicodedata


#Code to verify the codification
""" with open('data/raw/05_-_Antioquia_2021.csv', 'rb') as f:
    print(chardet.detect(f.read(10000))) """


#clean function
def clean_text(text):
    if pd.isna(text):
        return text
    text = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in text if not unicodedata.combining(c)])


#File path
raw_file = 'data/raw/05_-_Antioquia_2021.csv'


df = pd.read_csv(raw_file, encoding="utf-8")


df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Split compound columns
df[['codigo_departamento', 'nombre_departamento']] = df['departamento'].str.extract(r'^(\d+)\s*-\s*(.+)$')
df.drop(columns=['departamento'], inplace=True)

df[['codigo_municipio', 'nombre_municipio']] = df['municipio'].str.extract(r'^(\d+)\s*-\s*(.+)$')
df.drop(columns=['municipio'], inplace=True)

df[['codigo_diagnostico', 'n_diagnostico']] = df['diagnostico'].str.extract(r'^([A-Z0-9]+)\s*-\s*(.+)$')
df.drop(columns=['diagnostico'], inplace=True)

# clean text fields
df['nombre_departamento'] = df['nombre_departamento'].apply(clean_text)
df['nombre_municipio'] = df['nombre_municipio'].apply(clean_text)
df['n_diagnostico'] = df['n_diagnostico'].apply(clean_text)

# verify errors
pattern = re.compile(r'[Ã�]')
malos = df[df['nombre_municipio'].str.contains(pattern, na=False)]

print(f"Rows with errores in characters: {len(malos)}")
if not malos.empty:
    print("Values:")
    print(malos['nombre_municipio'].unique())
else:
    print("No errors in characters.")

# Save clean csv
output_path = 'data/interim/05_-_Antioquia_2021_clean.csv'
df.to_csv(output_path, index=False, encoding='utf-8')




