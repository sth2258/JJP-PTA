import httplib2
import os
import time
from apiclient import discovery
from google.oauth2 import service_account
import datetime
import dotenv
from dotenv import set_key
from dotenv import dotenv_values

envFile = "mount/.env"
config = dotenv_values(envFile)

if ";" in config["orders"]: 
    orders = config["orders"].split("$")

    for order in orders:
        attr = order.split(";")
        print(str(datetime.datetime.now()) + " "+ __file__ + " " + order)
        scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
        secret_file = os.path.join(os.getcwd(), config["StepX.GSheetsAPIKeyPath"])

        spreadsheet_id = config["Step5.spreadsheet_id"]

        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
        service = discovery.build('sheets', 'v4', credentials=credentials)

        values = [
            [attr[0], attr[1],attr[2],attr[3],attr[4],attr[5],attr[6],attr[7]]
        ]

        data = {
            'values' : values 
        }
        while True:
            try:
                service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, body=data, range=config["Step5.SheetName"], valueInputOption='USER_ENTERED').execute()
                break  # Break out of the loop if the request is successful
            except Exception as e:
                print(str(datetime.datetime.now()) + " "+ __file__ + f" Request failed: {e}")
                print(str(datetime.datetime.now()) + " "+ __file__ + " Retrying in 20 seconds...")
                time.sleep(20)  # Wait for 20 seconds before retrying        
else:
    print(str(datetime.datetime.now()) + " "+ __file__ + " No orders found")


set_key(envFile, key_to_set="startTime", value_to_set="")
set_key(envFile, key_to_set="endTime", value_to_set="")
set_key(envFile, key_to_set="orders", value_to_set="")

print(str(datetime.datetime.now()) + " "+ __file__ + " completed")