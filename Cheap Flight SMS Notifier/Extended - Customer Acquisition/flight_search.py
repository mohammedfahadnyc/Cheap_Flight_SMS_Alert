from flight_data import FlightData
import os
import requests
tequila_api_key = os.environ.get("OWN-TEQUILA-API-KEY")
tequila_end_point = "https://tequila-api.kiwi.com/locations/query"
header = {
            "apikey" : tequila_api_key
        }
FLY_FROM  = "JFK"
kiwi_flight_search_endpoint = "https://tequila-api.kiwi.com/v2/search"

class FlightSearch:
    def __init__(self):
        #This class is responsible for talking to the Flight Search API.
        pass


    def get_destination_code(self,sheet_data):
        city_list_from_sheets = [city["city"] for city in sheet_data["prices"]]
        iata_list = []
        for city in city_list_from_sheets :
            parameters = {
                    "term" : f"{city}",
                    "limit" : "1",
                    "location_types" : "city"
                }

            response = requests.get(url=tequila_end_point,headers=header,params=parameters)
            response.raise_for_status()
            response = response.json()
            iata_list.append(response["locations"][0]["code"])
        return iata_list


    def search_cheap_flights(self,fly_to,date_from,date_to):

        params = {
            "fly_from": "LHR",
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"

        }
        response = requests.get(url=kiwi_flight_search_endpoint,params=params,headers=header)
        try:
            data = response.json()["data"][0]
        except :
            params["max_stopovers"] = 1
            response = requests.get(url=kiwi_flight_search_endpoint,params=params,headers=header)
            data = response.json()["data"][0]
            flight_data = FlightData()
            flight_data.from_city = data["route"][0]["cityFrom"]
            flight_data.to_city = (data["cityTo"])
            flight_data.price = data["price"]
            flight_data.from_airport_code = data["route"][0]["flyFrom"]
            flight_data.to_airport_code = data["route"][1]["cityTo"]
            flight_data.from_date = data["route"][0]["local_departure"].split("T")[0]
            flight_data.to_date = data["route"][2]["local_departure"].split("T")[0]
            flight_data.via_city = via_city=data["route"][0]["cityTo"]
            flight_data.stop_over = 1
            return flight_data

        else :
            flight_data = FlightData()
            flight_data.from_city = (data["cityFrom"])
            flight_data.to_city = (data["cityTo"])
            flight_data.price = (data["fare"]["adults"])
            flight_data.from_airport_code = (data["flyFrom"])
            flight_data.to_airport_code = (data["flyTo"])
            flight_data.from_date = (data["route"][0]["local_departure"].split("T")[0])
            flight_data.to_date = (data["route"][1]["local_departure"].split("T")[0])
            return flight_data












#Data returned by tequila search API :
# data = {'all_airlines': [],
        #         'all_stopover_airports': [],
        #         'connections': [],
        #         'currency': 'USD',
        #         'currency_rate': 0.9194134142417137,
        #         'data': [{'airlines': ['VS', 'DL'],
        #                   'availability': {'seats': 1},
        #                   'baglimit': {'hand_height': 36,
        #                                'hand_length': 56,
        #                                'hand_weight': 10,
        #                                'hand_width': 23,
        #                                'hold_dimensions_sum': 208,
        #                                'hold_height': 75,
        #                                'hold_length': 90,
        #                                'hold_weight': 23,
        #                                'hold_width': 43,
        #                                'personal_item_height': 30,
        #                                'personal_item_length': 40,
        #                                'personal_item_weight': 2,
        #                                'personal_item_width': 15},
        #                   'bags_price': {'1': 155.805, '2': 358.345},
        #                   'booking_token': 'D1vIRXzJyTlhd-BHHTyC2eYUL7oZeQ_pfA0sPp25uj-_RYXvLxkpR-DdtrxEelcviuunY3mzqXe3T9nVpmHiNxECzZq88YhUWyNM6DUckOjFs_aKBjalWZDuzZBvKFNp6rqi0-dZVVUYbn5po3xCZ8Dn5YEOX5EDzcwHMN862TbAs0b02qE6Xun8doaNM92gBPYEi7dVXei2xCbZqi191mUSPdF8NIWmMHArADABrnTSJa6C28CDJjIrs19n2xuxUTHOfd3qZ9eaggG5jC0p71jrg_5fSYMmtWmmV2bdxW6LqsbS1jD8ggyvfZsWuX3Nt2NPQADLAoT9GuZ7qdKwrnZzZpw3IZYnXGy_ocyuY4FQAlL0nRE6S29PlYZ1GlETHqjPjbYkDeeIpteE_py-WfMc3Au3dnmSiFGpxajeFhijQArfMt9IWWAxyw4gOhW32-DNVQekJ14EgJEJ5eBNRre7yntcZGt3REGTdWJIExfxl-ETilZuUHSaFTZeDdgIZ',
        #                   'cityCodeFrom': 'NYC',
        #                   'cityCodeTo': 'LON',
        #                   'cityFrom': 'New York',
        #                   'cityTo': 'London',
        #                   'conversion': {'EUR': 476.256149, 'USD': 518},
        #                   'countryFrom': {'code': 'US', 'name': 'United States'},
        #                   'countryTo': {'code': 'GB', 'name': 'United Kingdom'},
        #                   'deep_link': 'https://www.kiwi.com/deep?from=JFK&to=LHR&flightsId=20a10f644b294b376d5b9679_0%7C20a10f644b294b376d5b9679_1&passengers=1&affilid=kukuflightdeals&lang=en&currency=USD&booking_token=D1vIRXzJyTlhd-BHHTyC2eYUL7oZeQ_pfA0sPp25uj-_RYXvLxkpR-DdtrxEelcviuunY3mzqXe3T9nVpmHiNxECzZq88YhUWyNM6DUckOjFs_aKBjalWZDuzZBvKFNp6rqi0-dZVVUYbn5po3xCZ8Dn5YEOX5EDzcwHMN862TbAs0b02qE6Xun8doaNM92gBPYEi7dVXei2xCbZqi191mUSPdF8NIWmMHArADABrnTSJa6C28CDJjIrs19n2xuxUTHOfd3qZ9eaggG5jC0p71jrg_5fSYMmtWmmV2bdxW6LqsbS1jD8ggyvfZsWuX3Nt2NPQADLAoT9GuZ7qdKwrnZzZpw3IZYnXGy_ocyuY4FQAlL0nRE6S29PlYZ1GlETHqjPjbYkDeeIpteE_py-WfMc3Au3dnmSiFGpxajeFhijQArfMt9IWWAxyw4gOhW32-DNVQekJ14EgJEJ5eBNRre7yntcZGt3REGTdWJIExfxl-ETilZuUHSaFTZeDdgIZ',
        #                   'distance': 5545.54,
        #                   'duration': {'departure': 24300, 'return': 27900, 'total': 52200},
        #                   'facilitated_booking_available': True,
        #                   'fare': {'adults': 518, 'children': 518, 'infants': 518},
        #                   'flyFrom': 'JFK',
        #                   'flyTo': 'LHR',
        #                   'has_airport_change': False,
        #                   'hidden_city_ticketing': False,
        #                   'id': '20a10f644b294b376d5b9679_0|20a10f644b294b376d5b9679_1',
        #                   'local_arrival': '2022-09-06T20:00:00.000Z',
        #                   'local_departure': '2022-09-06T08:15:00.000Z',
        #                   'nightsInDest': 14,
        #                   'pnr_count': 1,
        #                   'price': 518,
        #                   'quality': 616.255799,
        #                   'route': [{'airline': 'VS',
        #                              'bags_recheck_required': False,
        #                              'cityCodeFrom': 'NYC',
        #                              'cityCodeTo': 'LON',
        #                              'cityFrom': 'New York',
        #                              'cityTo': 'London',
        #                              'combination_id': '20a10f644b294b376d5b9679',
        #                              'equipment': None,
        #                              'fare_basis': 'OK3X46B2',
        #                              'fare_category': 'M',
        #                              'fare_classes': 'T',
        #                              'fare_family': '',
        #                              'flight_no': 26,
        #                              'flyFrom': 'JFK',
        #                              'flyTo': 'LHR',
        #                              'guarantee': False,
        #                              'id': '20a10f644b294b376d5b9679_0',
        #                              'last_seen': '2022-04-08T14:28:37.000Z',
        #                              'local_arrival': '2022-09-06T20:00:00.000Z',
        #                              'local_departure': '2022-09-06T08:15:00.000Z',
        #                              'operating_carrier': 'VS',
        #                              'operating_flight_no': '26',
        #                              'refresh_timestamp': '1970-01-01T00:00:00.000Z',
        #                              'return': 0,
        #                              'utc_arrival': '2022-09-06T19:00:00.000Z',
        #                              'utc_departure': '2022-09-06T12:15:00.000Z',
        #                              'vehicle_type': 'aircraft',
        #                              'vi_connection': False},
        #                             {'airline': 'DL',
        #                              'bags_recheck_required': False,
        #                              'cityCodeFrom': 'LON',
        #                              'cityCodeTo': 'NYC',
        #                              'cityFrom': 'London',
        #                              'cityTo': 'New York',
        #                              'combination_id': '20a10f644b294b376d5b9679',
        #                              'equipment': None,
        #                              'fare_basis': 'VL3X46B2',
        #                              'fare_category': 'M',
        #                              'fare_classes': 'E',
        #                              'fare_family': '',
        #                              'flight_no': 5993,
        #                              'flyFrom': 'LHR',
        #                              'flyTo': 'JFK',
        #                              'guarantee': False,
        #                              'id': '20a10f644b294b376d5b9679_1',
        #                              'last_seen': '2022-04-08T14:28:37.000Z',
        #                              'local_arrival': '2022-09-20T17:25:00.000Z',
        #                              'local_departure': '2022-09-20T14:40:00.000Z',
        #                              'operating_carrier': 'VS',
        #                              'operating_flight_no': '9',
        #                              'refresh_timestamp': '1970-01-01T00:00:00.000Z',
        #                              'return': 1,
        #                              'utc_arrival': '2022-09-20T21:25:00.000Z',
        #                              'utc_departure': '2022-09-20T13:40:00.000Z',
        #                              'vehicle_type': 'aircraft',
        #                              'vi_connection': False}],
        #                   'routes': [['JFK', 'LHR'], ['LHR', 'JFK']],
        #                   'technical_stops': 0,
        #                   'throw_away_ticketing': False,
        #                   'transfers': [],
        #                   'type_flights': ['deprecated'],
        #                   'utc_arrival': '2022-09-06T19:00:00.000Z',
        #                   'utc_departure': '2022-09-06T12:15:00.000Z',
        #                   'virtual_interlining': False}],
        #         'del': 0,
        #         'fx_rate': 1.08765,
        #         'ref_tasks': [],
        #         'refresh': [],
        #         'search_id': 'fabe34ea-dbbd-8fb2-a768-6490fd37a371',
        #         'search_params': {'flyFrom_type': 'airport',
        #                           'seats': {'adults': 1,
        #                                     'children': 0,
        #                                     'infants': 0,
        #                                     'passengers': 1},
        #                           'to_type': 'airport'},
        #         'sort_version': 0,
        #         'time': 1}