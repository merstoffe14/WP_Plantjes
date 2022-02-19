from datetime import date, datetime
from pickle import FALSE

class PlantBox:
    def __init__(self, id: int):
        self.id = id
        self.name = ""
        self.date: datetime = datetime(2022, 1, 1)
        self.days_planted = 0
        self.humidity: float = 0
        self.light_status = False
        self.last_spray: datetime = datetime(2022, 1, 1)


