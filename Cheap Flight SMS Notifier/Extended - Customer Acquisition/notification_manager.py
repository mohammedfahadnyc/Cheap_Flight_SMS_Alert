import os
from twilio.rest import Client
import smtplib
from flight_data import  FlightData
ACCOUNT_SID = os.environ.get("OWN_TWILLO_SID")
AUTH_TOKEN = os.environ.get("OWN_TWILLO_AUTH_TOKEN")
FROM_PHONE_NUMBER = os.environ.get("OWN_TWILLO_FROM_PHONE")
TO_PHONE_NUMBER = os.environ.get("OWN_TWILLO_TO_PHONE")
google_email = "pysmpt15@gmail.com"
google_password = "123456Ab"

class NotificationManager:
    def __init__(self):
        pass

    def send_message(self,flight_data:FlightData):
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        client = Client(account_sid, auth_token)
        if flight_data.stop_over > 0:
            message = client.messages \
                .create(
                body=f"Heads Up! Flight from {flight_data.from_city} - {flight_data.from_airport_code} to {flight_data.to_city}-{flight_data.to_airport_code} via {flight_data.via_city}, Stepover {flight_data.step_over} . Price lower now,currently selling at {flight_data.price}",
                from_=FROM_PHONE_NUMBER,
                to=TO_PHONE_NUMBER
            )
        else:
            message = client.messages \
                .create(
                body=f"Heads Up! Flight from {flight_data.from_city} - {flight_data.from_airport_code} to {flight_data.to_city}-{flight_data.to_airport_code} ,No Stepover, Price  is lower now,currently selling at {flight_data.price}",
                from_=FROM_PHONE_NUMBER,
                to=TO_PHONE_NUMBER
            )
        print(message.status)

    def send_email(self,first_name,last_name,email,flight_data : FlightData):
        with smtplib.SMTP("smtp.gmail.com",587) as connection :
            connection.starttls()
            connection.login(user=google_email, password=google_password)
            if flight_data.stop_over > 0 :
                connection.sendmail(from_addr=google_email,
                                to_addrs="fahadbiznes@gmail.com",
                                msg=f"Heads Up! Flight from {flight_data.from_city} - {flight_data.from_airport_code} to {flight_data.to_city}-{flight_data.to_airport_code} via {flight_data.via_city}, Stepover {flight_data.step_over} . Price lower now,currently selling at {flight_data.price}")
                print("Success")
            else :
                connection.sendmail(from_addr=google_email,
                                    to_addrs="fahadbiznes@gmail.com",
                                    msg=f"Heads Up! Flight from {flight_data.from_city} - {flight_data.from_airport_code} to {flight_data.to_city}-{flight_data.to_airport_code} ,No Stepover, Price  is lower now,currently selling at {flight_data.price}")
                print("Success")
