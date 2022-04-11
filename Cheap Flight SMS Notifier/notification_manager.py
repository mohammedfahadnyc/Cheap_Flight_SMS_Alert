import os
from twilio.rest import Client
from flight_data import  FlightData
ACCOUNT_SID = os.environ.get("OWN_TWILLO_SID")
AUTH_TOKEN = os.environ.get("OWN_TWILLO_AUTH_TOKEN")
FROM_PHONE_NUMBER = os.environ.get("OWN_TWILLO_FROM_PHONE")
TO_PHONE_NUMBER = os.environ.get("OWN_TWILLO_TO_PHONE")

class NotificationManager:
    def __init__(self,flight_data : FlightData):
        account_sid = ACCOUNT_SID
        auth_token =AUTH_TOKEN
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"Heads Up! Flight from {flight_data.from_city} - {flight_data.from_airport_code} to {flight_data.to_city}-{flight_data.to_airport_code} is lower now,currently selling at {flight_data.price}",
            from_=FROM_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        print(message.status)
