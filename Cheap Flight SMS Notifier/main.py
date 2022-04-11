
import datetime
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
sheet_data = data_manager.get_sheet_data()


if sheet_data["prices"][0]["iataCode"] == "" :
    iata_list = flight_search.get_destination_code(sheet_data)
    data_manager.update_google_sheet(iata_list)
    sheet_data = data_manager.get_sheet_data()

tomorrow = datetime.datetime.now()+datetime.timedelta(days=1)
tomorrow = tomorrow.strftime("%d/%m/%Y")
six_months_from_tomorrow = datetime.datetime.now()+datetime.timedelta(days=181)
six_months_from_tomorrow = six_months_from_tomorrow.strftime("%d/%m/%Y")



for city in sheet_data["prices"] :
    flightdata = flight_search.search_cheap_flights(
                fly_to = city['iataCode'],
                date_from = tomorrow,
                date_to = six_months_from_tomorrow,
                )
    if flightdata:
        if flightdata.price <  city["lowestPrice"]:
            NotificationManager(flight_data=flightdata)
        else :
            print(f"Prices are higher right now: {flightdata.to_city},{flightdata.price}")
    else :
        print("Seatch Later!")








