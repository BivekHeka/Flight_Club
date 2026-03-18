import random

class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(data, base_price=100):
    """
    Picks the cheapest flight from data, or generates a random demo price if using mock data.
    
    Args:
        data (dict): Flight data from Amadeus API (or None if using mock).
        base_price (float): The base price to generate random demo prices.

    Returns:
        FlightData: Flight info including randomized price.
    """

    # If no real data is available, create a mock flight with random price
    if data is None or not data.get("data"):
        price = round(random.uniform(base_price * 0.8, base_price * 1.2), 2)  # ±20% variation
        return FlightData(
            price=price,
            origin_airport="LON",
            destination_airport="N/A",
            out_date="2026-03-19",
            return_date="2026-09-14",
            stops=0
        )

    # Take the first flight as cheapest (or real API data)
    first_flight = data["data"][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
    stops = len(first_flight["itineraries"][0]["segments"]) - 1

    # Add small random variation for demo
    lowest_price = round(random.uniform(lowest_price * 0.8, lowest_price * 1.2), 2)

    return FlightData(lowest_price, origin, destination, out_date, return_date, stops)