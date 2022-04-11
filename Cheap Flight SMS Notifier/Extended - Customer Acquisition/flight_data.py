
class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self) :
        self.to_city : str
        self.from_city  : str
        self.from_airport_code : str
        self.to_airport_code : str
        self.from_date : str
        self.to_date :str
        self.price : str
        self.via_city : str
        self.stop_over = 0