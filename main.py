# import requests
# from datetime import datetime
# import os 
# from dotenv import load_dotenv

# # Load variables from .env
# load_dotenv()

# USER_ENDPOINT = os.getenv("USER_ENDPOINT")
# SHEETY_TOKEN = os.getenv("SHEETY_TOKEN")

# headers = {
#     "Authorization": f"Bearer {SHEETY_TOKEN}"
# }

# response = requests.get(USER_ENDPOINT, headers=headers)
# data = response.json()

# users = data[list(data.keys())[0]]

# print(data)



# import time
# from datetime import datetime, timedelta
# from data_manager import DataManager
# from flight_search import FlightSearch
# from flight_data import find_cheapest_flight
# from notification_manager import NotificationManager

# # ==================== Set up the Flight Search ====================

# data_manager = DataManager()
# sheet_data = data_manager.get_destination_data()
# flight_search = FlightSearch()
# notification_manager = NotificationManager()

# # Set your origin airport
# ORIGIN_CITY_IATA = "LON"

# # ==================== Update the Airport Codes in Google Sheet ====================

# for row in sheet_data:
#     if row["iataCode"] == "":
#         row["iataCode"] = flight_search.get_destination_code(row["city"])
#         # slowing down requests to avoid rate limit
#         time.sleep(2)
# print(f"sheet_data:\n {sheet_data}")

# data_manager.destination_data = sheet_data
# data_manager.update_destination_codes()

# # ==================== Search for Flights and Send Notifications ====================

# tomorrow = datetime.now() + timedelta(days=1)
# six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# for destination in sheet_data:
#     print(f"Getting flights for {destination['city']}...")
#     flights = flight_search.check_flights(
#         ORIGIN_CITY_IATA,
#         destination["iataCode"],
#         from_time=tomorrow,
#         to_time=six_month_from_today,
#         is_direct = True
#     )

#     # 🔁 If no direct flights → try indirect
#     if flights is None:
#         print(f"No direct flights to {destination['city']}. Trying indirect flights...")
        
#         flights = flight_search.check_flights(
#             ORIGIN_CITY_IATA,
#             destination["iataCode"],
#             from_time=tomorrow,
#             to_time=six_month_from_today,
#             is_direct=False
#         )

#     # ❌ If still nothing → skip
#     if flights is None:
#         print(f"No flights found for {destination['city']}")
#         continue

#     cheapest_flight = find_cheapest_flight(flights)
#     print(f"{destination['city']}: £{cheapest_flight.price}")
#     # Slowing down requests to avoid rate limit
#     time.sleep(2)

#     if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
#         print(f"Lower price flight found to {destination['city']}!")
#         # notification_manager.send_sms(
#         #     message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
#         #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
#         #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
#         # )
#         # SMS not working? Try whatsapp instead.
#         notification_manager.send_whatsapp(
#             message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
#                          f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
#                          f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
#         )





import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData, find_cheapest_flight
from notification_manager import NotificationManager

# ==================== Setup ====================
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "LON"

# ==================== Update IATA Codes ====================
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(2)  # avoid API rate limit

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# ==================== Flight Search & Notifications ====================
tomorrow = datetime.now() + timedelta(days=1)
six_months = datetime.now() + timedelta(days=6*30)

print("\n🚀 Starting flight deal search...\n")

# Hold all flight deals to sort later
all_flight_deals = []

for dest in sheet_data:
    city = dest["city"]
    print(f"🔍 Checking flights to {city}...")

    # Direct flights first
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA, dest["iataCode"], from_time=tomorrow, to_time=six_months, is_direct=True
    )

    # If no direct flights, try indirect
    if flights is None:
        print(f"⚠️ No direct flights to {city}. Searching for flights with stopovers...")
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA, dest["iataCode"], from_time=tomorrow, to_time=six_months, is_direct=False
        )

    if flights is None:
        print(f"❌ No flights found for {city}\n")
        continue

    cheapest_flight = find_cheapest_flight(flights, base_price=dest["lowestPrice"])
    stops_text = "Direct ✈️" if cheapest_flight.stops == 0 else f"{cheapest_flight.stops} stop(s) 🛬"

    # Add to all deals list
    all_flight_deals.append({
        "city": city,
        "price": cheapest_flight.price,
        "stops": stops_text,
        "out_date": cheapest_flight.out_date,
        "return_date": cheapest_flight.return_date
    })

    # Notify if cheaper than sheet price
    if cheapest_flight.price != "N/A" and cheapest_flight.price < dest["lowestPrice"]:
        print(f"🎉 DEAL ALERT! Cheaper flight to {city} found! Sending notification...\n")
        message = (f"🔥 *Low price alert!* £{cheapest_flight.price} to fly from "
                   f"*{cheapest_flight.origin_airport} → {cheapest_flight.destination_airport}* "
                   f"({stops_text})\n🛫 Depart: {cheapest_flight.out_date}\n🛬 Return: {cheapest_flight.return_date}")
        notification_manager.send_whatsapp(message_body=message)

    time.sleep(2)

# ==================== Print Dashboard ====================
print("\n📊 Flight Deals Dashboard (sorted by price) 📊\n")
sorted_deals = sorted(all_flight_deals, key=lambda x: x["price"])
for deal in sorted_deals:
    print(f"{deal['city']}: £{deal['price']} | {deal['stops']} | {deal['out_date']} → {deal['return_date']}")