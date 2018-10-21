import requests
import json


def get_access_token(client_id, client_secret):
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    payload = "grant_type=client_credentials"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'cache-control': 'no-cache',
        'Accept-Language': 'en_US'
    }

    response = requests.post(url, data=payload, headers=headers, auth=(client_id, client_secret))
    response_json = response.json()
    return response_json['access_token']


with open('paypal.json') as f:
    data = json.load(f)
    access_token = get_access_token(data['client_id'], data['client_secret'])


def personal_payment_url(email, amount):
    url = "https://api.sandbox.paypal.com/v1/payments/personal-payment-tokens"
    payload = {
        "amount": {
            "value": amount,
            "currency": "USD"
        },
        "payee": {
            "id": email,
            "type": "EMAIL"
        },
        "payment_type": "PERSONAL"
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept-Language': 'en_US',
        'Authorization': 'Bearer {}'.format(access_token)
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    payment_url = response_json['links'][0]['href']
    return payment_url


def append_callback(url):
    host = 'https://money2020-2018.appspot.com/paymentcallback'
    return '{}&return_url={}'.format(url, host)


def pay(email, amount):
    payment_url = personal_payment_url(email, amount)
    callback_payment_url = append_callback(payment_url)
    return callback_payment_url
