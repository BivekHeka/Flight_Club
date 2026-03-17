import requests
from datetime import datetime
import os 
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

USER_ENDPOINT = os.getenv("USER_ENDPOINT")
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN")

headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

response = requests.get(USER_ENDPOINT, headers=headers)
data = response.json()

users = data[list(data.keys())[0]]

print(data)
