import requests
import json
import pandas as pd
import time
from dotenv import load_dotenv
import os
import re

"""
File responsible for collect all NFTs from collection and save as JSON file for Power BI project
"""

load_dotenv() #add external request for user access

slug_collection = 'boredapeyachtclub'
initial_token = 'LXBrPTIzMTQzNzAz'

url = f'https://api.opensea.io/api/v2/collection/{slug_collection}/nfts?limit=200'
api_key = os.getenv('api_key')


headers = {
    "accept": "application/json",
    "x-api-key": api_key
}


# main_request = Function responsible for got all paginations avaliable 
def main_request(url, pagination_token, headers): 
    try:
        response = requests.get(url + f'&next={pagination_token}', headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

def fetch_all_paginations(initial_token, url, headers, max_requests=100, delay=10):
    pagination_tokens = [initial_token]
    current_token = initial_token
    request_count = 0

    while True:
        data = main_request(url,current_token, headers)

        if not data or 'next' not in data:
            break

        next_token = data['next']

        if not next_token or next_token == current_token:
            break

        pagination_tokens.append(next_token)
        current_token = next_token
        request_count +=1

        if request_count % max_requests == 0:
            print(f"Pausa de {delay} segundos após {max_requests} requisições")
            time.sleep(delay)

    return pagination_tokens


all_tokens = fetch_all_paginations(
    initial_token = initial_token,
    url = url,
    headers= headers,
    max_requests=100,
    delay=10
)

#fetch_nfts = Function responsible for create request for each pagination avaliable at fetch_all_paginations function
def fetch_nfts(all_tokens, url, headers, max_requests=100, delay=10):
    all_nfts=[]
    request_count = 0

    for index, token in enumerate(all_tokens):
        try:
            data = main_request(url, token, headers)

            if data and 'nfts' in data:
                all_nfts.extend(data['nfts'])
                print(f"Página {index + 1}/{len(all_tokens)}: {len(data['nfts'])} NFTs coletados")

            request_count +=1

            if request_count % max_requests == 0 and request_count != 0:
                print(f"⏸ Pausa de {delay} segundos após {request_count} requisições")
                time.sleep(delay)

        except Exception as e:
            print(f"Erro na página {index + 1}: {str(e)}")
    
    return all_nfts


nfts_data = fetch_nfts(
    all_tokens=all_tokens,
    url=url,
    headers=headers,
    max_requests=100,
    delay=10
)

#sanitize_filename: Funcion used for use de slug_collection as file name replacing all special character
def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|]', '', name)

safe_slug = sanitize_filename(slug_collection)

datasource_dir = "datasource"

if not os.path.exists(datasource_dir):
    os.makedirs(datasource_dir)

file_path = os.path.join(datasource_dir, f"{safe_slug}.json")

with open(file_path,'w') as file:
    json.dump(nfts_data, file, indent=4)

print(f"Total de páginas coletadas: {len(all_tokens)}")
print("Tokens:", all_tokens[0])
print(f"Total de NFTs coletadas: {len(nfts_data)}")
print(f"Arquivo salvo em: {file_path}")

