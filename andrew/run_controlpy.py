#Note for this to be able to run on school wifi, this needs to be on a vpn

#All this is is a simple webserver that will:
#Take the input google forms
#Display what everyone's assigned role and seat number is
#For debugging purposes, have the clients ack back.
#This will likely not be used in production


#pip install gspread
#pip install oauth2client
#pip install flask-bootstrap

from __future__ import print_function
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import pandas as pd
import json

from flask import Flask
from flask_bootstrap import Bootstrap

#Will use bootstrap for frontend

def _init():

	SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
	SECRETS_FILE = "API_key.json"
	SPREADSHEET = "EE180DA Google Sheet"

	json_key = json.load(open(SECRETS_FILE))
	# Authenticate using the signed key
	credentials = SignedJwtAssertionCredentials(json_key['client_email'],
												json_key['private_key'], SCOPE)
	gc = gspread.authorize(credentials)
	#Get google sheets information, which is passed from the google form
	
	print("The following sheets are available")
	for sheet in gc.openall():
		print("{} - {}".format(sheet.title, sheet.id))


	workbook = gc.open(SPREADSHEET)
	sheet = workbook.sheet1



	#We now have our row, column, and role_index of each person!
	data = pd.DataFrame(sheet.get_all_records())
	column_names = {'What role number (printed label) on your Raspberry Pi do you have?': 'role_id',
				'What row number are you in, from front to back, starting from 0? (MAKE SURE TO COUNT CLOSELY)': 'row',
				'What column number are you in, from left to right, starting from 0? (MAKE SURE TO COUNT CLOSELY)': 'col',
				}

	data.rename(columns=column_names, inplace=True)
	#data.timestamp = pd.to_datetime(data.timestamp)
	print(data)
	data.drop_duplicates(subset='role_id', keep='first', inplace=False)
	return data


'''
app = Flask(__name__)

@app.route("/")
def hello():
	data = _init()
	return "Hello, World!"
'''

if __name__ == "__main__":
	data = _init()