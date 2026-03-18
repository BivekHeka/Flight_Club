
class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.stops = stops
        """
        Constructor for initializing a new flight data instance with specific travel details.

        Parameters:
        - price: The cost of the flight.
        - origin_airport: The IATA code for the flight's origin airport.
        - destination_airport: The IATA code for the flight's destination airport.
        - out_date: The departure date for the flight.
        - return_date: The return date for the flight.
        """
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

def find_cheapest_flight(data):
    if data is None or not data.get('data'):
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", stops=0)

    # Data from the first flight
    first_flight = data['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    segments = first_flight["itineraries"][0]["segments"]
    stops = len(segments) - 1  # 0 = direct, 1 or 2 = stopovers
    origin = segments[0]["departure"]["iataCode"]
    destination = segments[-1]["arrival"]["iataCode"]
    out_date = segments[0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, stops)

    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        segments = flight["itineraries"][0]["segments"]
        stops = len(segments) - 1
        origin = segments[0]["departure"]["iataCode"]
        destination = segments[-1]["arrival"]["iataCode"]
        out_date = segments[0]["departure"]["at"].split("T")[0]
        return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

        if price < lowest_price:
            lowest_price = price
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, stops)
            print(f"Lowest price to {destination} is £{lowest_price} (Stops: {stops})")

    return cheapest_flight

