import json
import requests

with open('cobrand.json') as f:
    data = json.load(f)
    host = data['host']
    name = data['cobrand_name']
    cobrand_login = data['cobrand_login']
    cobrand_password = data['cobrand_password']

    cobrand_login_url = host + '/cobrand/login'
    headers = {
        'Content-Type': 'application/json',
        'Api-Version': '1.1',
        'Cobrand-Name': name
    }
    payload = {
        "cobrand": {
            "cobrandLogin": cobrand_login,
            "cobrandPassword": cobrand_password,
            "locale": "en_US"
        }
    }
    response = requests.post(cobrand_login_url, headers=headers, json=payload)
    response_json = response.json()
    session = response_json['session']['cobSession']
