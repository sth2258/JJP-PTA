import datetime
import json
import requests
import dotenv
from dotenv import set_key
from dotenv import dotenv_values

envFile = "mount/.env"
config = dotenv_values(envFile)

class Order: 
    pass
    def __str__(self):
            return self.childFirstName + ";" + self.childLastName + ";" + self.parentName+ ";" + self.parentEmail+ ";" + self.parentPhone+ ";" + self.childTeacher+ ";" + self.deliveryDate+ ";" + self.snack

def obj_dict(obj):
    return obj.__dict__

# Define the URL with query parameters
url = config["StepX.GivebacksAPIURL"]



def get_params(offset):
    params = {
        'cause_id': config["StepX.CauseID"],
        'offset': offset,
        'limit': 50,
        'search[carts.status][value]': 'purchased',
        'search[store_items.uuid][value]':config["Step4.StoreItemID"],
        'search[store_items.uuid][by]': 'in',
        #'search[carts.purchased_at][value]': '2024-09-01T00:00:00.000-04:00|2024-09-01T23:59:59.999-04:00',
        'search[carts.purchased_at][value]': config['startTime'] + '|' + config['endTime'],
        'search[carts.purchased_at][by]': 'between',
        'join': 'AND'
    }
    return params

def parseResponse(output1):
    responseItems = []
    for item in output1["cart_items"]:
        order1 = Order()
        order1.childTeacher=item["options"]["Child's Teacher"]
        order1.childFirstName=item["options"]["Chid's First Name"]
        order1.childLastName=item["options"]["Child's Last Name"]
        order1.parentName=item["options"]["Parent/Guardian Name"]
        order1.parentEmail=item["options"]["Parent/Guardian Email"]
        order1.parentPhone=item["options"]["Parent/Guardian Phone #"]
        order1.deliveryDate=item["options"]["Birthday Box Delivery Date"]
        order1.snack=item["options"]["Birthday Box Snack Selection"]
        responseItems.append(order1)
    return responseItems


# Define the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Authentication-Session-Secret': config['secret'],
    'Authentication-Session-Token': config['token'],
    'Origin': config["StepX.GivebacksURL"],
    'Connection': 'keep-alive',
    'Referer': config["StepX.GivebacksURL"],
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'DNT': '1',
    'Sec-GPC': '1',
    'If-None-Match': 'W/"55414897eb276af2340685370caa9fa8"',
    'Priority': 'u=0',
    'TE': 'trailers'
}

offset = 0
orders = []
cont = True
while(cont == True):
    
    response = requests.get(url, headers=headers, params=get_params(offset))
    resp = response.json()

    #print("Offset: "+ str(offset) + ", Has more? "+ str(resp["meta"]["has_more"])+ ", Count:"+str(resp["meta"]["count"]))
    orders+=parseResponse(resp)
    cont=resp["meta"]["has_more"]
    offset += 50

output = {}
output["orders"] = "$".join(str(objRow) for objRow in orders)

set_key(envFile, key_to_set="orders", value_to_set=output["orders"])

#json_string = json.dumps(orders, default=obj_dict)
#output = json_string
#output["orders"] = json_string

# Print the response status code and content
#print(response.status_code)
#print(response.json())
print(str(datetime.datetime.now()) + " "+ __file__ + " completed")