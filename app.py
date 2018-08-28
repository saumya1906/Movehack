import datetime
import os
import json
from openpyxl import load_workbook
import json
from Main import Main
from pyqrcode import QRCode# [...] QRcode(app) # [...] 
from flask import Flask, render_template, request, json, jsonify, redirect
import stripe
import png

x = 'sk_test_Un4q8w9hizeHGD8EJ5Vyv0cd'
y =  'pk_test_dmUeD6ibTYHZa2iViOK3F7Gj'
stripe_keys = {

  'secret_key': x,
  'publishable_key': y
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__, template_folder='template', static_url_path='/static')

global key_qr
global cost_amount
global ans
main = Main()


@app.route('/pay_cost_time', methods=['GET', 'POST'])
def paym():
	global key_qr
	global cost_amount
	global ans
	# cost_amount = 500*100
	key_qr = ans["timeRoute"]["randomString"]
	cost_amount = 100*ans["timeRoute"]["totalCost"]
	tot_time = ans["timeRoute"]["totalTime"]
	# key_qr = "usdfyf"
	return render_template('payment.html',  key=stripe_keys['publishable_key'], amount = cost_amount)
@app.route('/pay_cost_cost', methods=['GET', 'POST'])
def paym1():
	global key_qr
	global cost_amount
	global ans
	# cost_amount = 500*100
	key_qr = ans["costRoute"]["randomString"]
	cost_amount = 100*ans["costRoute"]["totalCost"]
	tot_time = ans["costRoute"]["totalTime"]
	# key_qr = "usdfyf"
	return render_template('payment.html',  key=stripe_keys['publishable_key'], amount = cost_amount)
@app.route('/pay_cost_comfort', methods=['GET', 'POST'])
def paym2():
	global key_qr
	global cost_amount
	global ans
	# cost_amount = 500*100
	key_qr = ans["comfort"]["randomString"]
	cost_amount = 100*ans["comfort"]["totalCost"]
	tot_time = ans["comfort"]["totalTime"]
	# key_qr = "usdfyf"
	return render_template('payment.html',  key=stripe_keys['publishable_key'], amount = cost_amount)
@app.route('/', methods=['GET'])
def home():
	return render_template('traffic.html')

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    # amount = 500*100
    global key_qr
    global cost_amount
    customer = stripe.Customer.create(
        email= request.form['custemail'],
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=cost_amount,
        currency='usd',
        description='Flask Charge'
    )
    # key_qr = "dsguik"
    qr_file_name = None
    
    qr_code = QRCode(key_qr, encoding='utf-8')
    qr_file_name = 'static/images/rand.png'
    qr_code.png(qr_file_name, scale=5)
    fname ="/static/images/rand.png" 
    return render_template('final.html', amount=cost_amount, link=fname)




@app.route('/report', methods=['GET', 'POST'])
def report():
	global ans
	ans = dict()
	if request.method == 'POST':
		# print("herehehe")
		source = request.form['source']
		# print(busroute)
		destination = request.form['destination']
		# print(date)
		# ans = dict()
		ans['dest'] = destination
		ans['src'] = source
		print("source: ", ans['src'])
		print("destination: ", ans['dest'])
		ans = main.solve(ans['src'], ans['dest'])

	
	return render_template('report/425.html',ans = ans)

 

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run()
# app.run(host='0.0.0.0',port=5000)
