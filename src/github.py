import os
import requests

_headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'token ' + os.environ['GITHUB_TOKEN']
}

def get(url):
    req = requests.get(url, headers=_headers)
    req.raise_for_status()
    return req.json()

def post(url, body):
    req = requests.post(url, json=body, headers=_headers)
    req.raise_for_status()
    return req.json() if req.text else None
