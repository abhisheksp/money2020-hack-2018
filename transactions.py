import datetime
from functools import partial
from operator import is_not

import requests

import account
import cobrand
import user


def transform(username, transaction_entries, accounts_dict):
    def transform_transaction(t):
        account_id = t['accountId']
        if 'runningBalance' not in t:
            return
        balance = t['runningBalance']['amount']
        timestamp = timestamp_transform(t['lastUpdated'])
        amount = '{}$'.format(t['amount']['amount'])
        account_name = accounts_dict[account_id].name
        return {
            "userId": username,
            "account": "whatever",
            "type": t['baseType'],
            "bank": account_name,
            "balance": balance,
            "amount": amount,
            "timeStamp": timestamp,
            "date": timestamp.day,
            "month": timestamp.month,
            "year": timestamp.year
        }

    timestamp_transform = lambda t: datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
    transformed_transactions = filter(partial(is_not, None), map(transform_transaction, transaction_entries))
    return list(transformed_transactions)


def transactions(username, password, from_date):
    user_session = user.session(username, password)
    accounts_dict = account.accounts(user_session)
    transactions_url = '{}/transactions'.format(cobrand.host)
    headers = {
        'Content-Type': 'application/json',
        'Api-Version': '1.1',
        'Cobrand-Name': cobrand.name,
        'Authorization': 'cobSession={},userSession={}'.format(cobrand.session, user_session)
    }
    query_string = {"fromDate": from_date}
    response = requests.get(transactions_url, headers=headers, params=query_string)
    response_json = response.json()
    transaction_entries = response_json['transaction']
    return transform(username, transaction_entries, accounts_dict)
