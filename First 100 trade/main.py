import requests
import time
import base64
from cryptography.hazmat.primitives.asymmetric import ed25519
import json

base_url = 'https://api.backpack.exchange/'
key = '' # YOUR API KEY
secret = '' #YOUR PRIVATE KEY

def generate_signature(timestamp, secret, instruction, window=5000, params=None):
    private_key_obj = ed25519.Ed25519PrivateKey.from_private_bytes(
        base64.b64decode(secret)
    )
    if params is None:
        params = {}
    if 'postOnly' in params:
        params = params.copy()
        params['postOnly'] = str(params['postOnly']).lower()
    param_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    if not param_str:
        param_str = ''
    sign_str = f"instruction={instruction}&timestamp={timestamp}&window={window}"
    signature = base64.b64encode(
        private_key_obj.sign(sign_str.encode())).decode()
    return {
        "X-API-Key": key,
        "X-Signature": signature,
        "X-Timestamp": str(timestamp),
        "X-Window": str(window),
        "Content-Type": "application/json; charset=utf-8",
    }

def request_api(method, endpoint, instruction, params=None):
    url = f'{base_url}{endpoint}'
    timestamp = int(time.time() * 1e3)
    headers = generate_signature(timestamp, secret, instruction, params=params)
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=params)
    else:
        raise ValueError("Unsupported HTTP method")
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    return response.json()

fill_history_data = request_api(method='GET', endpoint='wapi/v1/history/fills', instruction='fillHistoryQueryAll')
balance_data = request_api(method='GET', endpoint='api/v1/capital', instruction='balanceQuery')
deposit_address_data = request_api(method='GET', endpoint='wapi/v1/capital/deposits', instruction='depositQueryAll')

all_data = {
    "fill_history_data": fill_history_data,
    "balance_data": balance_data,
    "deposit_address_data": deposit_address_data
}

with open("data.json", "w") as f:
    json.dump(all_data, f, indent=4)

print("Данные сохранены в файл data.json")
