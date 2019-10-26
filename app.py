from flask import Flask, flash, request, redirect, url_for, escape, render_template
import requests
import json
import random


valid = "abcdefghijklmnopqrstuvwxyz0123456789"
apiKey = "7eef02ee968ed07e8f2b15b969e927f5"
live_transactions = dict()

app = Flask(__name__)

@app.route("/transfer_id", methods=["POST", "GET"])
def transfer_id():
	if request.method == "POST":
		key = None
		while key is None or key in live_transactions.keys():
			key = ''.join(random.choice(valid) for _ in range(20))

		live_transactions[key] = current_transaction ##### NEED TO CREATE CURRENT_TRANSACTION, THAT'S SOMETHING WE NEED THE API TO BE ABLE TO DO
		return {"transfer_id": key}
	elif request.method == "GET":
		information = live_transactions.pop(request.form.get("transfer_id", None), None)
		return information


@app.route("/get_balance", methods=["GET"])
def get_balance():
	customerId = request.args.get("customerID", None)
	print(request.args.to_dict().keys())
	print(customerId)
	url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
	account = requests.get(url)
	return account.json()[0]

@app.route("/get_customers", methods=["GET"])
def get_customers():
	url = 'http://api.reimaginebanking.com/customers?key={}'.format(customerId,apiKey)
	customers = request.get(url)
	return {"account": account}




if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True, debug=True)
