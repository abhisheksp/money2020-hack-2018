import cobrand
import requests


class Account:
    def __init__(self, id_, name, number):
        self._id = id_
        self._name = name
        self._number = number

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    def __repr__(self):
        return 'Account({}, {})'.format(self._id, self._name)


def accounts(user_session):
    accounts_url = cobrand.host + '/accounts'
    headers = {
        'Content-Type': 'application/json',
        'Api-Version': '1.1',
        'Cobrand-Name': cobrand.name,
        'Authorization': 'cobSession={},userSession={}'.format(cobrand.session, user_session)
    }
    response = requests.get(accounts_url, headers=headers)

    response_json = response.json()
    accounts_raw = response_json['account']
    accounts_dict = {}
    for account in accounts_raw:
        accounts_dict[account['id']] = Account(account['id'], account['providerName'], account['accountNumber'])
    return accounts_dict
