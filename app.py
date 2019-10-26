from flask import Flask, flash, request, redirect, url_for, escape, render_template
import json
import random


valid = "abcdefghijklmnopqrstuvwxyz0123456789"
live_transactions = dict()

app = Flask(__name__)

@app.route("/transfer_id", methods=["POST", "GET"])
def transfer_id():
	if request.method == "POST":
		key = None
		while key is None or key in live_transactions.keySet():
			key = ''.join(random.choice(valid) for _ in range(20))

		live_transactions[key] = current_transaction ##### NEED TO CREATE CURRENT_TRANSACTION, THAT'S SOMETHING WE NEED THE API TO BE ABLE TO DO
		return {"transfer_id": key}
	elif request.method == "GET":
		information = live_transactions.pop(request.form.get("transfer_id", None), None)
		return information


if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True)