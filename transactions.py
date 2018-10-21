import datetime
from functools import partial
from operator import is_not
import copy
import requests

import account
import cobrand
import user
from database import save_transactions


def transform(username, transaction_entries, accounts_dict):
    def transform_transaction(t):
        account_id = t['accountId']
        if 'runningBalance' not in t:
            return
        balance = '{}$'.format(t['runningBalance']['amount'])
        timestamp = timestamp_transform(t['lastUpdated'])
        amount = '{}$'.format(t['amount']['amount'])
        account_name = accounts_dict[account_id].name
        account_number = accounts_dict[account_id].number
        transaction_type = t['baseType'].lower()
        return {
            "userId": username,
            "account": account_number,
            "type": transaction_type,
            "bank": account_name,
            "balance": balance,
            "amount": amount,
            "timeStamp": timestamp.strftime('%Y-%m-%d %H-%M-%S'),
            "date": str(timestamp.day),
            "month": str(timestamp.month),
            "year": str(timestamp.year)
        }

    timestamp_transform = lambda t: datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
    transformed_transactions = list(filter(partial(is_not, None), map(transform_transaction, transaction_entries)))
    save_transactions(copy.deepcopy(transformed_transactions))
    return transformed_transactions


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
