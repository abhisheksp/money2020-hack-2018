from pymongo import MongoClient
import json

with open('mongo.json') as f:
    data = json.load(f)
    uri = data['uri']
    port = int(data['port'])
    client = MongoClient(uri, port)
    db = client.data
    transactions_collection = db.raw


def save_transactions(transaction_entries):
    new_result = transactions_collection.insert_many(transaction_entries)
    print('Inserted {} entries'.format(len(new_result.inserted_ids)))
    print('New IDs: {}'.format(new_result.inserted_ids))
