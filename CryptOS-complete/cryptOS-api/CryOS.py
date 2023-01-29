#################s#########
# << CryOS RPC SERVER >> #
##########################
import random
import smtplib
import base64
import logging
import decimal
import http.client as httplib
import urllib.parse as urlparse
import json
import socket
import urllib.request
from bitcoinrpc.authproxy import AuthServiceProxy
import sys
import time
import pickle
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps
from flask_mysqldb import MySQL
from passlib.context import CryptContext
from flask_bootstrap import Bootstrap


########################
# <<Keys For Password>>#
########################
keys_password_generation = {}
keys_password_generation['0'] = 'a'
keys_password_generation['1'] = 'b'
keys_password_generation['2'] = 'c'
keys_password_generation['3'] = 'd'
keys_password_generation['4'] = 'e'
keys_password_generation['5'] = 'f'
keys_password_generation['6'] = 'g'
keys_password_generation['7'] = 'h'
keys_password_generation['8'] = 'i'
keys_password_generation['9'] = 'j'
keys_password_generation['10'] = 'k'
keys_password_generation['11'] = 'l'
keys_password_generation['12'] = 'm'
keys_password_generation['13'] = 'n'
keys_password_generation['14'] = 'o'
keys_password_generation['15'] = 'p'
keys_password_generation['16'] = 'q'
keys_password_generation['17'] = 'r'
keys_password_generation['18'] = 's'
keys_password_generation['19'] = 't'
keys_password_generation['20'] = 'u'
keys_password_generation['21'] = 'v'
keys_password_generation['22'] = 'w'
keys_password_generation['23'] = 'x'
keys_password_generation['24'] = 'y'
keys_password_generation['25'] = 'z'

keys_password_generation['26'] = 'A'
keys_password_generation['27'] = 'B'
keys_password_generation['28'] = 'C'
keys_password_generation['29'] = 'D'
keys_password_generation['30'] = 'E'
keys_password_generation['31'] = 'F'
keys_password_generation['32'] = 'G'
keys_password_generation['33'] = 'H'
keys_password_generation['34'] = 'I'
keys_password_generation['35'] = 'J'
keys_password_generation['36'] = 'K'
keys_password_generation['37'] = 'L'
keys_password_generation['38'] = 'M'
keys_password_generation['39'] = 'N'
keys_password_generation['40'] = 'O'
keys_password_generation['41'] = 'P'
keys_password_generation['42'] = 'Q'
keys_password_generation['43'] = 'R'
keys_password_generation['44'] = 'S'
keys_password_generation['45'] = 'T'
keys_password_generation['46'] = 'U'
keys_password_generation['47'] = 'V'
keys_password_generation['48'] = 'W'
keys_password_generation['49'] = 'X'
keys_password_generation['50'] = 'Y'
keys_password_generation['51'] = 'Z'


development_site = "development.html"
production_site = "index.html"

app = Flask(__name__)
Bootstrap(app)

########################
# <<Global Variables>> #
########################
btc_cost = 5000000
rvn_cost = 250

coinsale_bitcoin_address = "3MQfs9rmSaPqeBgfj3Gyb2TmMwYz4YV4et"
coinsale_ravencoin_address = "RKqL3K1P2xijzHaxhmmmaoxrS7jou3GWj2"


########################
# <<   Encryption   >> #
########################
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

########################
# <<  MySQL config  >> #
########################
mysql = MySQL()
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cryptos'
app.config['MYSQL_HOST'] = 'localhost'

mysql.init_app(app)

########################
#    << Website >>     #
########################
class Statistics(Resource):
	@app.route('/Statistics')
	def disply_stats():
		#(username, password, email, rvnaddr, btcaddr, cryosaddr)
		usernames = {}
		emails = {}
		btc_balances = {}
		rvn_balances = {}
		btc = AuthServiceProxy('http://user:password@127.0.0.1:8332')
		rvn = AuthServiceProxy('http://user:password@127.0.0.1:8766')

		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_core''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			usr = data[i]['username']
			rcv_label = str(btc.getreceivedbylabel(usr))
			rcv_label_f = float(rcv_label)
			btc_balance = rcv_label_f
			spent = data[i]['btcspent']
			btc_balances[str(i)] = str(btc_balance - float(spent))
		for i in range(0, len(data)):
			username = data[i]['username']
			rvn_balance = str(rvn.getbalance(username))
			if rvn_balance == "0E-8":
				rvn_balance = "0.0"
			rvn_balances[str(i)] = rvn_balance
		result = 'BITCOIN : '
		for i in range(0, len(btc_balances)):
			result += str(btc_balances[str(i)]) + ' , '
		result += '\n'
		result += 'RAVENCOIN : '
		for i in range(0, len(rvn_balances)):
			result += str(rvn_balances[str(i)]) + ' , '
		return(result)

class Home(Resource):
	@app.route('/')
	@app.route('/Home')
	def Home():
		return render_template(production_site)
class Agb(Resource):
	@app.route('/agb')
	def AGB():
		return render_template("agb.html")

class ResetPassword(Resource):
	@app.route('/ResetPassword/<email>')
	def ResetMyPassword(email):
		success = False;
		first_key = keys_password_generation[str(random.randint(0, len(keys_password_generation) - 1))]
		second_key = keys_password_generation[str(random.randint(0, len(keys_password_generation) - 1))]
		third_key = keys_password_generation[str(random.randint(0, len(keys_password_generation) - 1))]
		fourth_key = keys_password_generation[str(random.randint(0, len(keys_password_generation) - 1))]
		fifth_key = keys_password_generation[str(random.randint(0, len(keys_password_generation) - 1))]
		sixth_key = keys_password_generation[str(random.randint(0, len(keys_password_generation) - 1))]
		mailserver = smtplib.SMTP('smtp.gmail.com', 587)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
		mailserver.login('cryptos.platform.supp@gmail.com', 'CryosSmtp2019service')
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			if data[i]['email'] == email:
				username = data[i]['username']
				btc_address = data[i]['btcaddr']
				cryos_address = data[i]['cryosaddr']
				rvn_address = data[i]['rvnaddr']
				generated_password = first_key + str(random.randint(0, 9)) + second_key + third_key + str(random.randint(0, 9)) + fourth_key + fifth_key + str(random.randint(0, 9)) + sixth_key
				generated_password_encrypted = pwd_context.encrypt(generated_password)
				success = True;
			else:
				i += 1
		if success == False:
			return("Password Reset Failed !")
		else:
			msg = 'Your Password Reset has been successfull.' + '\n' + 'username : ' + str(username) + '\n' + 'new password : ' + str(generated_password) + '\n' + 'You can now Log in.'
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO cryos_db (username, password, email, rvnaddr, btcaddr, cryosaddr) VALUES (%s, %s, %s, %s, %s, %s)", (username, generated_password_encrypted, email, rvn_address, btc_address, cryos_address))
			mysql.connection.commit()
			cur.close()
			mailserver.sendmail('cryptos.platform.supp@gmail.com', email, msg)
			return("Password Reset Success !")


###############################
# #####  #####  #####   ##### #
# #      #   #  #   #   #     #
# #      #   #  #####   ####  #
# #      #   #  #    #  #     #
# #####  #####  # 	  # ##### #
###############################

################################################################################################
# << CRYPTOS CORE >> #																		   #
################################################################################################
class Balance(Resource):
	@app.route('/Balance/<username>')
	def balance(username):
		access = AuthServiceProxy("http://user:password@127.0.0.1:19000")
		bal = str(access.getbalance(username))
		if float(bal) < 0.00:
			bal = "0.00"
		return(bal)

class Address(Resource):
	@app.route('/Address/<username>')
	def address(username):
		access = AuthServiceProxy("http://user:password@127.0.0.1:19000")
		return(str(access.getaccountaddress(username)))
#Transaction from username to username
class Transaction(Resource):
	#Encrypt password & upgrade to MySQL
	@app.route('/Transaction/<sender>/<recipient>/<amount>/<password>')
	def transaction(sender, recipient, amount, password):
		print(sender)
		print(recipient)
		print(amount)
		print(password)
		access = AuthServiceProxy("http://user:password@127.0.0.1:19000")
		address = access.getaccountaddress(str(recipient))
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]

		if recipient in str(data):
			for i in range(0, len(data)):
				print(data)
				if data[i]['username'] == sender and pwd_context.verify(password, data[i]['password']) == True:
					return(str(access.sendfrom(str(sender), str(address), str(amount)) + ' Success !'))
				else:
					i += 1
		return('Transaction Failed !')
#Transaction from username to address
class Tx(Resource):
	@app.route('/Tx/<sender>/<address>/<amount>/<password>')
	def transaction2(sender, address, amount, password):
		access = AuthServiceProxy("http://user:password@127.0.0.1:19000")
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			print(data)
			if data[i]['username'] == sender and pwd_context.verify(password, data[i]['password']) == True:
				return(str(access.sendfrom(str(sender), str(address), str(amount)) + ' Success !'))
			else:
				i += 1
		return('Tx Failed !')
class History(Resource):
	@app.route('/History/<username>')
	def history(username):
		######################################CONTAINS##########################################
		#"account", "address", "category", "amount", "confirmations", "blockhash", "time"(unix)#
		########################################################################################
		#																					   #
		########################################################################################
		access = AuthServiceProxy("http://user:password@127.0.0.1:19000")
		history_dict = access.listtransactions(username)
		history_short = history_dict[0 : len(history_dict) - 1]
		history_info = {}
		history_info['category'] = []
		history_info['amount'] = []
		for i in range (0, 10):
			history_info['category'].append(i)
			history_info['amount'].append(i)
			history_info['category'][i] = history_dict[i]['category']
			history_info['amount'][i] = str(history_dict[i]['amount'])
		return(str(history_info))
################################################################################################
# << BITCOIN CORE >> 																		   #
################################################################################################
#address
class BtcAddress(Resource):
	@app.route('/BtcAddress/<username>')
	def btcaddress(username):
		btc_address = ""
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			if data[i]['username'] == username:
				btc_address = str(data[i]['btcaddr'])
				return(btc_address)
			else:
				i += 1
		return('Address not found !')
#balance
class BtcBalance(Resource):
	@app.route('/BtcBalance/<username>')
	def btcbalance(username):
		btc = AuthServiceProxy('http://user:password@127.0.0.1:8332')
		rcv_label = str(btc.getreceivedbylabel(username))
		rcv_label_f = float(rcv_label)
		btc_balance = rcv_label_f
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_core''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			if data[i]['username'] == username:
				btc_balance -= float(data[i]['btcspent'])
				print(str(data[i]['btcspent']))
			else:
				i += 1
		if btc_balance < 0.00:
			return("0.00")
		else:
			return(str(btc_balance))
#transaction
class Btctransaction(Resource):
	@app.route('/BtcTransaction/<username>/<password>/<recipient>/<amount>')
	def btctransaction(username, password, recipient, amount):
		tx_fee = 0.0001
		spent_btc = 0.0000
		amount_spent = 0.0000
		validation = False
		btc = AuthServiceProxy('http://user:password@127.0.0.1:8332')
		rcv_label = str(btc.getreceivedbylabel(username))
		rcv_label_f = float(rcv_label)
		#Read Mysql Database "cryos_core" To Find Available Balance
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_core''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			if data[i]['username'] == username:
				btc_spent = float(data[i]['btcspent'])
			else:
				i += 1
		#Read Mysql Database "cryos_db" To Compare Password
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			if data[i]['username'] == username and pwd_context.verify(password, data[i]['password']) == True:
				validation = True
			else:
				i += 1
		if (rcv_label_f - btc_spent - tx_fee) >= 0.0000 and validation == True:
			try:
				btc.sendtoaddress(recipient, amount)
				amount_spent = float(amount) + tx_fee
				total_spent = float(amount_spent) + btc_spent
			except Exception as e:
				return('Transaction Failed' + ' || ' + 'e = ' + str(e))
		else:
			return("Transaction Failed !")
		#Insert Into Mysql Database "cryos_core"
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO cryos_core (username, btcspent) VALUES (%s, %s)", (username, str(total_spent)))
		mysql.connection.commit()
		cur.close()
		return('Transaction Success' + '  ||  ' + 'SPENT TOTAL : ' + str(total_spent) + '  ||  ' + 'LAST TRANSACTION : ' + str(amount_spent))
#coinsale
class BuyWithBtc(Resource):
	@app.route('/BitcoinPurchase/<username>/<password>/<amount>')
	def Bitcoinpurchase(username, password, amount):
		tx_fee = 0.0001
		validation = False
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			if data[i]['username'] == username and pwd_context.verify(password, data[i]['password']) == True:
				validation = True
			else:
				i += 1
		#cryosaddr
		address = '';
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			if data[i]['username'] == username and pwd_context.verify(password, data[i]['password']) == True:
				address = str(data[i]['cryosaddr'])
			else:
				i+= 1

		btc = AuthServiceProxy('http://user:password@127.0.0.1:8332')
		access = AuthServiceProxy('http://user:password@127.0.0.1:19000')
		btc_balance = float(btc.getreceivedbylabel(username))
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_core''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			if data[i]['username'] == username:
				btc_spent = float(data[i]['btcspent'])
				btc_balance -= float(data[i]['btcspent'])
			else:
				i += 1
		if btc_balance >= float(amount) + tx_fee and validation == True:
			try:
				btc.sendtoaddress(coinsale_bitcoin_address, str(amount))
				amount_spent = float(amount) + tx_fee
				total_spent = float(amount_spent) + btc_spent
				bought_value = float(amount) * float(btc_cost)
				access.sendfrom('premine', str(address), str(bought_value))
			except Exception as e:
				print(str(e))
				return('Unknown Transaction Failure' + ' || ' + 'e = ' + str(e))
		else:
			return("Transaction Failed, Balance Too Low !")
		#Insert Into Mysql Database "cryos_core"
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO cryos_core (username, btcspent) VALUES (%s, %s)", (username, str(total_spent)))
		mysql.connection.commit()
		cur.close()

		return('Transaction Success ! || Btc/CryOS : ' + str(amount) + ' BTC || ' + str(float(amount) * btc_cost) + ' CryOS !')

################################################################################################
# << RAVENCOIN CORE >> 																		   #
################################################################################################
#balance
class RvnBalance(Resource):
	@app.route('/RvnBalance/<username>')
	def rvnbalance(username):
		rvn = AuthServiceProxy('http://user:password@127.0.0.1:8766')
		rvn_balance = str(rvn.getbalance(username))
		if rvn_balance == "0E-8":
			rvn_balance = "0.0"
		elif float(rvn_balance) < 0.00:
			rvn_balance = "0.00"
		return(rvn_balance)
#address
class RvnAddress(Resource):
	@app.route('/RvnAddress/<username>')
	def rvnaddress(username):
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range (0, len(data)):
			print(data)
			if data[i]['username'] == username:
				your_rvn_address = str(data[i]['rvnaddr'])
				return(your_rvn_address)
			else:
				i += 1
#transaction
class RvnTransaction(Resource):
	@app.route('/RvnTransaction/<username>/<password>/<recipient>/<amount>')
	def rvntransaction(username, password, recipient, amount):
		rvn = AuthServiceProxy('http://user:password@127.0.0.1:8766')
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			print(data)
			if data[i]['username'] == username and pwd_context.verify(password, data[i]['password']) == True:
				return(str(rvn.sendfrom(username, recipient, amount)) + '\n' +' success !')
			else:
				i += 1
		return('Transaction failed !')
#coinsale purchase
class BuyWithRvn(Resource):
	@app.route('/RavenPurchase/<username>/<password>/<amount>')
	def Ravenpurchase(username, password, amount):
		rvn = AuthServiceProxy('http://user:password@127.0.0.1:8766')
		access = AuthServiceProxy('http://user:password@127.0.0.1:19000')
		address = '';
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			if data[i]['username'] == username and pwd_context.verify(password, data[i]['password']) == True:
				address = str(data[i]['cryosaddr'])
			else:
				i+= 1
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range(0, len(data)):
			print(data)
			if data[i]['username'] == username and pwd_context.verify(password, data[i]['password']) == True:
				try:
					rvn.sendfrom(username, coinsale_ravencoin_address, amount)
					access.sendfrom('premine', address, str(float(amount) * rvn_cost))
					return("Transaction Success !")
				except Exception as e:
					print('Buying process failed =>' + str(e))
			else:
				i += 1
		return("Transaction Failed !")
#history
########################
# << User data area >> #
########################
class Login(Resource):
	#Encrypt password & upgrade to MySQL
	@app.route('/Login/<username>/<password>')
	def login(username, password):
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		for i in range (0, len(data)):
			print(data)
			if data[i]['username'] == username and pwd_context.verify(password, data[i]['password']) == True:
				print('Login valid !')
				msg = "Member Login !" + "\n" + str(username)
				mailserver = smtplib.SMTP('smtp.gmail.com', 587)
				mailserver.ehlo()
				mailserver.starttls()
				mailserver.ehlo()
				mailserver.login('cryptos.platform.supp@gmail.com', 'CryosSmtp2019service')
				mailserver.sendmail('cryptos.platform.supp@gmail.com', 'cryptos.platform.supp@gmail.com', msg)
				return('Login valid !')
			else:
				i += 1
		print('Login failed !')
		return('Login failed !')
class Registration(Resource):
	#Encrypt password & upgrade to MySQL
	@app.route('/Registration/<username>/<password>/<email>')
	def registration(username, password, email):
		access = AuthServiceProxy("http://user:password@127.0.0.1:19000")
		rvn = AuthServiceProxy("http://user:password@127.0.0.1:8766")
		btc = AuthServiceProxy("http://user:password@127.0.0.1:8332")
		cur = mysql.connection.cursor()
		cur.execute('''select * from cryptos.cryos_db''')
		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]
		if username in str(data):
			return('Registration failed !  <> USERNAME TAKEN <>')
		try:
			btc_address = btc.getnewaddress(username)
			rvn_address = rvn.getnewaddress(username)
			cryos_address = access.getnewaddress(username)
			encrypted_password = pwd_context.encrypt(password)
			
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO cryos_db (username, password, email, rvnaddr, btcaddr, cryosaddr) VALUES (%s, %s, %s, %s, %s, %s)", (username, encrypted_password, email, rvn_address, btc_address, cryos_address))
			mysql.connection.commit()
			cur.close()
			btcspent = str(0.00)
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO cryos_core (username, btcspent) VALUES (%s, %s)", (username, btcspent))
			mysql.connection.commit()
			cur.close()
			msg = "New Member !" + "\n" + str(username)
			mailserver = smtplib.SMTP('smtp.gmail.com', 587)
			mailserver.ehlo()
			mailserver.starttls()
			mailserver.ehlo()
			mailserver.login('cryptos.platform.supp@gmail.com', 'CryosSmtp2019service')
			mailserver.sendmail('cryptos.platform.supp@gmail.com', 'cryptos.platform.supp@gmail.com', msg)
			return('Registration valid !')
		except Exception as e:
			return('Registration failed !' + ' Exception: ' + str(e))

########################
# << Sale functions >> #
########################
class Supply(Resource):
	@app.route('/Supply')
	def supply():
		access = AuthServiceProxy("http://user:password@127.0.0.1:19000")
		return(str(access.getbalance('premine')))

if __name__ == '__main__':
	app.run(host='0.0.0.0')

