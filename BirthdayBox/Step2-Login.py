import datetime
import requests
import json
import time
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

max_retries = 3
for i in range(max_retries):
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        print(str(datetime.datetime.now()) + " "+ __file__ + " Response code: "+str(response.status_code))
        break  # Break out of loop if request is successful
    except requests.exceptions.RequestException as e:
        print(str(datetime.datetime.now()) + " "+ __file__ + " "+ f"Attempt {i+1} failed: {e}")
        if i < max_retries - 1:
            time.sleep(5)  # Wait for 5 seconds before retrying
        else:
            print(str(datetime.datetime.now()) + " "+ __file__ + " Max retries reached, request failed.")

# Make the POST request

output = {}
output['token'] = response.json()['user']['session']['token']
output['secret'] = response.json()['user']['session']['secret']
set_key(envFile, key_to_set="token", value_to_set=output['token'])
set_key(envFile, key_to_set="secret", value_to_set=output['secret'])
print(str(datetime.datetime.now()) + " "+ __file__ + " completed")
