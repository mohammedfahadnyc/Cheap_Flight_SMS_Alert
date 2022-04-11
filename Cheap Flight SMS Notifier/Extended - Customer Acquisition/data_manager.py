import os
import requests
Customer_acuisition_sheety_endpoint = "https://api.sheety.co/6d265cf17d9cad6aa4d01c8acd566dc2/customerAquisition/sheet1"
google_sheet_api_token = os.environ.get("OWN_API_KEY")
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


    def customer_acquisition(self):
        print("Welcome to Flight Club \n")
        f_name = input("Please Enter Your First Name\n")
        l_name = input("Please Enter Your Last Name\n")
        email = input("Please Enter Your Email\n")
        email_confirm = input("Please Enter Your Email Again\n")

        if email == email_confirm:
            print(f"Welcome To The Club {f_name} {l_name}")
        else:
            print(f"Email Error! Please Enter Again Fresh Data")
            self.customer_acquisition()
        return (f_name,l_name,email)

    def update_customer_data_sheet(self,f_name,l_name,email):

        params = {
            "sheet1" : {
            "firstName" : f_name,
            "lastName" : l_name,
            "phoneNumber" : email}
        }
        response = requests.post(url=Customer_acuisition_sheety_endpoint,json=params)

    def find_customer_mailing_data(self):
        response = requests.get(url=Customer_acuisition_sheety_endpoint)
        customers_mailing_data = {'sheet1': [{'firstName': 'a', 'lastName': 'b', 'id': 2}, {'firstName': 'a', 'lastName': 'a', 'id': 3}]}
        return customers_mailing_data