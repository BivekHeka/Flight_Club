import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


USER_ENDPOINT = os.getenv("USER_ENDPOINT")
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN")
SHEETY_USER = os.getenv("SHEETY_USER")
SHEETY_PASS = os.getenv("SHEETY_PASS")
PRICES_ENDPOINT = os.getenv("PRICES_ENDPOINT")
class DataManager:

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {SHEETY_TOKEN}"
        }
        self.destination_data = {}

    def get_destination_data(self):
        # Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=PRICES_ENDPOINT, headers=self.headers)
        data = response.json()
        print("DEBUG: Sheety response →", data)  # optional, for debugging
        # automatically pick the first key if sheet name changes
        self.destination_data = data[list(data.keys())[0]]
        return self.destination_data

    # In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{PRICES_ENDPOINT}/{city['id']}",
                headers=self.headers,
                json=new_data
            )
            print(response.text)
