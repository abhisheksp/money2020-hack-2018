from flask import Flask, jsonify, request, redirect
import transactions
import paypal

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


@app.route('/pay', methods=['GET'])
def pay_handler():
    email = request.args.get('email')
    amount = request.args.get('amount')
    payment_url = paypal.pay(email, amount)
    return redirect(payment_url)


@app.route('/paymentcallback', methods=['GET'])
def payment_callback_handler():
    status = request.args.get('status')
    transaction_id = request.args.get('transactionId')
    if status == 'failure':
        return '<h1>Payment Failed!</h1>'
    return '<h1>Status : Success</h1><h1>Transaction ID: {}</h1>'.format(transaction_id)


if __name__ == '__main__':
    app.run()
