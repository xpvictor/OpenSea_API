import requests
import json
import pandas as pd
import time
from dotenv import load_dotenv
import os
import re

'''
Python file responsible for collect overview information about NFTs and transform to CSV file for Power BI project
'''

load_dotenv()

#'boredapeyachtclub'
slug_collection = 'boredapeyachtclub'

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

df_boredape_baseclub.to_csv(f"{slug_collection}_overview_datasourcePBI.csv", index=False)

