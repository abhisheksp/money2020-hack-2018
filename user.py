import cobrand
import requests


def session(username, password):
    user_login_url = cobrand.host + '/user/login'
    headers = {
        'Content-Type': 'application/json',
        'Api-Version': '1.1',
        'Cobrand-Name': cobrand.name,
        'Authorization': 'cobSession={}'.format(cobrand.session)
    }
    payload = {
        "user": {
            "loginName": username,
            "password": password,
            "locale": "en_US"
        }
    }
    response = requests.post(user_login_url, headers=headers, json=payload)
    response_json = response.json()
    user_session = response_json['user']['session']['userSession']
    return user_session
