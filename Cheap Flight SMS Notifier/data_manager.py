import os
import requests
google_sheet_api_token = os.environ.get("OWN_GOOGLE_SHEETY_API_TOKEN")
google_sheet_api_endpoint= "https://api.sheety.co/6d265cf17d9cad6aa4d01c8acd566dc2/cheapFlightDeals/prices"
google_sheet_put_endpoint = "https://api.sheety.co/6d265cf17d9cad6aa4d01c8acd566dc2/cheapFlightDeals/prices/2"
headers ={
    "Authorization" : f"Bearer {google_sheet_api_token}"
        }


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}


    def get_sheet_data(self):
        sheet_data = requests.get(url=google_sheet_api_endpoint,headers=headers)
        sheet_data = sheet_data.json()
        return sheet_data


    def update_google_sheet(self,iata_list):
        for i in range(len(iata_list)):
            params = {
                "price":
                    {
                        "iataCode" : iata_list[i]
                    }
            }
            response = requests.put(url=f"https://api.sheety.co/6d265cf17d9cad6aa4d01c8acd566dc2/cheapFlightDeals/prices/{i+2}",headers=headers,json=params)


