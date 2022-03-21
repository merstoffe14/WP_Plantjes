from datetime import date, datetime
from pickle import FALSE
from sqlite3 import Time
from time import time

from pydantic import BaseModel


class PlantBoxDataReceive(BaseModel):
    name: str
    date: datetime = datetime(2022, 1, 1)
    lona: str
    lofa: str
    spraytime: int
    crithumid: float
    schedule: str

class PlantBox:
    def __init__(self, id: int):
        self.id = id
        self.name = ""
        self.date: datetime = datetime(2022, 1, 1)
        self.lona: str
        self.lofa: str
        self.spraytime = 0
        self.crithumid: float = 0
        self.schedule = "" 
        self.days_planted = 0
        self.humidity: float = 0
        self.light_status = 0
        self.last_spray: datetime = datetime(2022, 1, 1)

    def user_update(self, update: PlantBoxDataReceive):
        self.name = update.name
        self.date = update.date
        self.lona = update.lona
        self.lofa = update.lofa
        self.spraytime = update.spraytime 
        self.crithumid = update.crithumid
        self.schedule = update.schedule

    


        
   


