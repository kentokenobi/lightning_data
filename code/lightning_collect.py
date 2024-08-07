import pandas as pd
import geopandas as gpd
import requests
import datetime
from io import BytesIO

# UK time
uk_time = datetime.datetime.now() - datetime.timedelta(hours=9)
today = f'{uk_time.year}' + f'{uk_time.month:02}' + f'{uk_time.day:02}'
today_csv = f'./data/lightning_{today}.csv'

# Exist file
try:
    df_base = pd.read_csv(today_csv)
except FileNotFoundError:
    df_base = pd.DataFrame()

# Fetch new data
five_min = (uk_time.minute // 5) * 5 - 5
if five_min < 0:
    five_min = 55
    uk_time = uk_time - datetime.timedelta(hours=1)
    
current_time = f'{uk_time.year}' + f'{uk_time.month:02}' + f'{uk_time.day:02}' + f'{uk_time.hour:02}' + f'{five_min:02}'
url = f'https://www.jma.go.jp/bosai/jmatile/data/nowc/{current_time}00/none/{current_time}00/surf/liden/data.geojson?id=liden'
response = requests.get(url)
gdf = gpd.read_file(BytesIO(response.content))

# Concatenate the data
if not gdf.empty:
    df_base = pd.concat([df_base, gdf], axis=0)

# Save the file
df_base.to_csv(today_csv, index=False)