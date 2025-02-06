#Get collection
#url: https://docs.opensea.io/reference/get_collection

"""
purpose of this file: 
Make the request to the API returning data about the collection overview, 
creating a CSV file that will be used within the project in Power BI.
"""
import requests
import json 
import time 
from dotenv import load_dotenv
import os 
import re 
import pandas as pd

load_dotenv()

slug_collection = 'boredape-baseclub'


url = f"https://api.opensea.io/api/v2/collections/{slug_collection}"
api_key = os.getenv('api_key')

headers = {
    "accept" : "application/json",
    "x-api-key": api_key
}


try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response.json()
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
    
data = response.json()

if isinstance(data, dict):
    df = pd.json_normalize(data)
else:
    df = pd.DataFrame(data)

def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|]', '', name)

safe_slug = sanitize_filename(slug_collection)

datasource_dir = "datasource"

if not os.path.exists(datasource_dir):
    os.makedirs(datasource_dir)

file_path = os.path.join(datasource_dir,f"overview-collection_{safe_slug}.csv")

df.to_csv(file_path, index=False, encoding="utf-8")

