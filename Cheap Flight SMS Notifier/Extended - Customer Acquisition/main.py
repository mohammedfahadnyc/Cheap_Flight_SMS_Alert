
import datetime
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
sheet_data = data_manager.get_sheet_data()
notification_manager = NotificationManager()
print(sheet_data)
if sheet_data["prices"][0]["iataCode"] == "" :
    iata_list = flight_search.get_destination_code(sheet_data)
    data_manager.update_google_sheet(iata_list)
    sheet_data = data_manager.get_sheet_data()

tomorrow = datetime.datetime.now()+datetime.timedelta(days=1)
tomorrow = tomorrow.strftime("%d/%m/%Y")
six_months_from_tomorrow = datetime.datetime.now()+datetime.timedelta(days=181)
six_months_from_tomorrow = six_months_from_tomorrow.strftime("%d/%m/%Y")

customer_data = {'sheet1': [{'firstName': 'a', 'lastName': 'b', 'id': 2}, {'firstName': 'a', 'lastName': 'a', 'id': 3}]}


customer_acquisition = data_manager.customer_acquisition()
f_name = customer_acquisition[0]
l_name = customer_acquisition[1]
email = customer_acquisition[2]
data_manager.update_customer_data_sheet(f_name,l_name,email)
customers_mailing_data = data_manager.find_customer_mailing_data()

for city in sheet_data["prices"] :
    flightdata = flight_search.search_cheap_flights(
                fly_to = city['iataCode'],
                date_from = tomorrow,
                date_to = six_months_from_tomorrow,
                )
    if flightdata:
        if flightdata.price < city["lowestPrice"]:
            for row in customers_mailing_data["sheet1"]:
                first_name = (row["firstName"])
                last_name = row["lastName"]
                email = row["phoneNumber"]
                # notification_manager.send_message(flight_data=flightdata)
                notification_manager.send_email(first_name,last_name,email,flight_data=flightdata)
        else :
            print(f"Prices are higher right now: {flightdata.to_city},{flightdata.price}")
    else :
        print("Seatch Later!")









