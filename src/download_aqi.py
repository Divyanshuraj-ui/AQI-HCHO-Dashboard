import pandas as pd

url = "https://api.openaq.org/v3/locations?country_id=IN&limit=10"

try:
    df = pd.read_json(url)
    print(df.head())
except Exception as e:
    print(e)
