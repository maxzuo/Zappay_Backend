from flask import Flask, flash, request, redirect, url_for, escape, render_template
import requests
import json
import random
from datetime import datetime


valid = "abcdefghijklmnopqrstuvwxyz0123456789"
apiKey = "7eef02ee968ed07e8f2b15b969e927f5"
live_transactions = dict()

app = Flask(__name__)

@app.route("/generate_transfer", methods=["GET"])
def generate_transfer():
	firstName = request.args.get("first_name", None)
	lastName = request.args.get("last_name", None)
	payee_id = request.args.get("customer_id", None)

	amount = int(request.args.get("amount", None))
	key = None
	while key is None or key in live_transactions.keys():
		key = ''.join(random.choice(valid) for _ in range(20))

	current_transaction = {
		"amount": amount,
		"name": "%s %s" % (firstName, lastName),
		"payee_id": payee_id
	}
	live_transactions[key] = current_transaction ##### NEED TO CREATE CURRENT_TRANSACTION, THAT'S SOMETHING WE NEED THE API TO BE ABLE TO DO
	return {"transfer_id": key}
	# elif request.method == "GET":
	# 	information = live_transactions.pop(request.form.get("transfer_id", None), None)
	# 	return information

@app.route("/check_transfer", methods=["GET"])
def check_transfer():
	uid = request.args.get("uid", "null")

	transaction = live_transactions.get(uid, None)
	if None:
		return {"ERROR": "no transfer associated with that uid"}
	return {"payee": transaction['name'], "amount": transaction["amount"]}



@app.route("/accept_transfer", methods=["GET"])
def accept_transfer():
	payer_id = request.args.get("customer_id", None)
	uid = request.args.get("uid", "null")
	transaction = live_transactions.get(uid, None)
	if None:
		return {"ERROR": "no transfer associated with that uid"}

	data = {
		"medium": "balance",
		"payee_id": transaction["payee_id"],
		"transaction_date": datetime.today().strftime("%Y-%m-%d"),
		"status": "pending",
		"description": "string"
	}

	url = "http://api.reimaginebanking.com/accounts/{}/transfers?key={}".format(payer_id, apiKey)
	res = requests.post(url, json=data)

	return res.json()


@app.route("/get_balance", methods=["GET"])
def get_balance():
	customerId = request.args.get("customerID", None)
	print(request.args.to_dict().keys())
	print(customerId)
	url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId, apiKey)
	account = requests.get(url).json()[0]
	print(account)
	balance = account.get('balance', None)
	return {"balance":balance}

@app.route("/create_account", methods=["GET"])
def create_account():
	firstName = request.args.get("first_name", None)
	lastName = request.args.get("last_name", None)
	b = {
		"street_number": "string",
		"street_name": "string",
		"city": "string",
	    "state": "MA",
	    "zip": "01775"
	}
	user_data = {
		"first_name": firstName,
		"last_name": lastName,
		"address": {
			"street_number": "string",
			"street_name": "string",
			"city": "string",
		    "state": "MA",
		    "zip": "01775"
		}
	}

	url = "http://api.reimaginebanking.com/customers?key={}".format(apiKey)
	customer = requests.post(url, json=json.loads(json.dumps(user_data)))
	print(customer.json())
	# input()
	customer_id = customer.json().get("objectCreated", None)
	if customer_id is None:
		return {"error": "did not successfully create customer"}
	customer_id = customer_id.get('_id')
	if customer_id is None:
		return {"error": "did not successfully create customer"}
	url = "http://api.reimaginebanking.com/customers/{}/accounts?key={}".format(customer_id, apiKey)
	account_data = {
		"type": "Credit Card",
		"nickname": "%s %s" % (firstName, lastName),
		"rewards": 0,
		"balance": int(request.args.get("balance", "0", type=str))
	}

	account = requests.post(url, json=account_data)
	print(account.json())
	account_id = account.json().get("objectCreated").get("_id")
	print(customer_id, account_id)
	return {"customer_id": customer_id, "account_id": account_id}



# @app.route("/get_customers", methods=["GET"])
# def get_customers():
# 	url = 'http://api.reimaginebanking.com/customers?key={}'.format(customerId,apiKey)
# 	customers = request.get(url)
# 	return {"account": account}




if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True, debug=True)
