import datetime
import requests
import json

import dotenv
from dotenv import set_key
from dotenv import dotenv_values
envFile = "mount/.env"
config = dotenv_values(envFile)

# Define the URL and headers
url = config["Step2.GivebacksAPILoginURL"]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'Origin': config["StepX.GivebacksURL"],
    'Connection': 'keep-alive',
    'Referer': config["StepX.GivebacksURL"],
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'DNT': '1',
    'Sec-GPC': '1',
    'Priority': 'u=0',
    'TE': 'trailers'
}

# Define the payload
payload = {
    'user': {
        'email': config["Step2.EMAIL"],
        'password': config["Step2.PASSWORD"]
    }
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

output = {}
output['token'] = response.json()['user']['session']['token']
output['secret'] = response.json()['user']['session']['secret']
set_key(envFile, key_to_set="token", value_to_set=output['token'])
set_key(envFile, key_to_set="secret", value_to_set=output['secret'])
print(str(datetime.datetime.now()) + " "+ __file__ + " completed")
#print(config)