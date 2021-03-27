import os
import requests

_headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'token ' + os.environ['GITHUB_TOKEN']
}

def get(url):
    res = requests.get(url, headers=_headers)
    res.raise_for_status()
    return res.json()

def get_paginated(url):
    pages = []
    next_url = url
    while (next_url):
        res = requests.get(next_url, headers=_headers)
        res.raise_for_status()
        pages.append(res.json())
        next_link = [link for link in res.links if link.get('rel') == 'next']
        next_url = next_link[0]['url'] if len(next_link) else None
    return [item for page in pages for item in page]

def patch(url, body):
    res = requests.patch(url, json=body, headers=_headers)
    res.raise_for_status()
    return res.json() if res.text else None
