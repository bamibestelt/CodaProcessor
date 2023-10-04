from typing import List

import requests
import json


from constant import CODA_API_TOKEN, CODA_BASE_URL


def fetch_coda_links() -> List[str]:
    coda_ids = fetch_coda_doc(f"{CODA_BASE_URL}/docs")
    links = []
    for doc_id in coda_ids:
        temp_links = fetch_coda_pages(f"{CODA_BASE_URL}/docs/{doc_id}/pages")
        links.extend(temp_links)
    return links


def fetch_coda_pages(api_url: str) -> List[str]:
    response = http_client_request(api_url)
    if not response:
        return []
    else:
        json_object = json.loads(response)
        json_array = json_object['items']
        page_links = [item['browserLink'] for item in json_array]
        return page_links


def fetch_coda_doc(api_url: str) -> List[str]:
    response = http_client_request(api_url)
    if not response:
        return []
    else:
        json_object = json.loads(response)
        json_array = json_object['items']
        ids = [item['id'] for item in json_array]
        return ids


def http_client_request(api_url: str) -> str:
    response = requests.get(api_url, headers={'Authorization': f'Bearer {CODA_API_TOKEN}'})
    if response.ok:
        return response.text
    else:
        return ''
