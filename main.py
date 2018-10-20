from flask import Flask, jsonify, request
import transactions

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '<h1>Works!</h1>'


@app.route('/transactions', methods=['POST'])
def transactions_handler():
    request_body = request.get_json()
    username = request_body['username']
    password = request_body['password']
    from_date = request_body['from_date']
    transaction_entries = transactions.transactions(username, password, from_date)
    return jsonify(transaction_entries)


if __name__ == '__main__':
    app.run()
