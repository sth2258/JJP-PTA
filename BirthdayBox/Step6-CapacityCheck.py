import httplib2
import os
from apiclient import discovery
from google.oauth2 import service_account
import datetime
import dotenv
from dotenv import set_key
from dotenv import dotenv_values
from collections import defaultdict

envFile = "mount/.env"
config = dotenv_values(envFile)
ignoredDateItems = []

class Order: 
    pass
    def __str__(self):
            return self.childFirstName + ";" + self.childLastName + ";" + self.parentName+ ";" + self.parentEmail+ ";" + self.parentPhone+ ";" + self.childTeacher+ ";" + self.deliveryDate+ ";" + self.snack

class IgnoreItems:
    pass
    def __str__(self):
        return self.date + ";" + "^".join(self.items)

def alreadyExcluded(deliveryDate, snack):
    #print("Checking: "+deliveryDate + " for items " + str(snack))
    for ignore in ignoredDateItems:
        if(deliveryDate == ignore.date):
            if(snack in ignore.items):
                #print("  It's already been excluded. ")
                return True
    #print("  Not already excluded")
    return False

def addExcludedItem(deliveryDate, snack):
    dateFound=False
    for ignore in ignoredDateItems:
        if(deliveryDate == ignore.date):
            dateFound=True
            ignore.items.append(snack)
            #print("date was found, snack added to array")
    if not dateFound:
        ignore1 = IgnoreItems()
        ignore1.date = deliveryDate
        ignore1.items = [snack]
        ignoredDateItems.append(ignore1)
        #print("date not found and snack not found -- adding")






#Step6.PreIgnoredData=9/16/2024;Original Oreos^Rice Krispies$1/17/2024;Original Oreos

preIgnoredDataStr=config.get("Step6.PreIgnoredData","")
preIgnoredData = preIgnoredDataStr.split("$")
if preIgnoredDataStr != "":
    for ignore in preIgnoredData:
        ignore1 = IgnoreItems()
        ignore1.date = ignore.split(";")[0]
        ignore1.items = ignore.split(";")[1].split("^")
        ignoredDateItems.append(ignore1)
        #print(ignore1)



scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
secret_file = os.path.join(os.getcwd(), config["StepX.GSheetsAPIKeyPath"])

spreadsheet_id = config["Step6.spreadsheet_id"]

credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
service = discovery.build('sheets', 'v4', credentials=credentials)

data = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=config["Step6.TableRange"]).execute()

orders = []

for value in data["values"]:
    order1 = Order()
    order1.childTeacher=value[0]
    order1.childFirstName=value[1]
    order1.childLastName=value[2]
    order1.parentName=value[3]
    order1.parentEmail=value[4]
    order1.parentPhone=value[5]
    order1.deliveryDate=value[6]
    order1.snack=value[7]
    orders.append(order1)

# Create a dictionary to count snacks grouped by date
snack_count_by_date = defaultdict(lambda: defaultdict(int))

# Iterate through the orders and count snacks grouped by date
for order in orders:
    snack_count_by_date[order.deliveryDate][order.snack] += 1

# Before the check
#for item in ignoredDateItems:
#    print(item)

# Find instances where snack occurs more than once on the same date
for deliveryDate, snacks in snack_count_by_date.items():
    #print(f"Date: {deliveryDate}")
    for snack, count in snacks.items():
        if count > int(config["Step6.MaxItemsOrderedPerDate"]):
            alreadyExcludedDateItem = alreadyExcluded(deliveryDate, snack)
            if(not alreadyExcludedDateItem):
                print(str(datetime.datetime.now()) + " "+"New exclusion:"+deliveryDate+", "+snack )
                addExcludedItem(deliveryDate,snack)

                #also add to the row
            #else:
            #    print("  Date has already been excluded")
            #print(f"  Snack: {snack} occurs {count} times")


outputStrArr = []
for item in ignoredDateItems:
    outputStrArr.append(item)
set_key(envFile, key_to_set="Step6.PreIgnoredData", value_to_set="$".join(str(objRow) for objRow in ignoredDateItems))





print(str(datetime.datetime.now()) + " "+ __file__ + " completed")