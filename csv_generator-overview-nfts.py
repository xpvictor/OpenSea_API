import requests
import json
import pandas as pd
import time
from dotenv import load_dotenv
import os
import re

load_dotenv()

slug_collection = 'boredape-baseclub'
initial_token = 'LXBrPTE4ODI3MTg3NTQ='

url = f'https://api.opensea.io/api/v2/collection/{slug_collection}/nfts?limit=200'
api_key = os.getenv('api_key')


headers = {
    "accept": "application/json",
    "x-api-key": api_key
}

response = requests.get(url,headers= headers).json()
#response.raise_for_status() <-- used for make a validation about status 
df_start = pd.json_normalize(response['nfts'])


df_boredape_baseclub = pd.read_json("./datasource/boredape-baseclub.json")

df_boredape_baseclub = pd.concat([df_start,df_boredape_baseclub])
df_boredape_baseclub['identifier'] = df_boredape_baseclub['identifier'].astype(str)
df_boredape_baseclub.sort_values(by=['identifier'], ascending=False)

df_boredape_baseclub.to_csv("boredape_baseclue_overview_datasourcePBI.csv", index=False)
