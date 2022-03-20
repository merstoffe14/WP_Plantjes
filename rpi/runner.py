import asyncio
from models import PlantBox
import os,shutil,jsonpickle
from datetime import datetime


class BackgroundRunner:
    def __init__(self):

        self.plant_boxes = {
             1: PlantBox(1),
             2: PlantBox(2),
             3: PlantBox(3),
             4: PlantBox(4)
        }

        
    async def run_main(self):

        while True:
            await asyncio.sleep(1)
            self.loop()

    
    # Loading data from locally saved file
    async def load_data(self):
        print("Loading data")

    # Check if data.json exists, if not copy from hardcoded initial template.
        try:
            if not os.path.exists('data.json'):
                shutil.copyfile('init_data.json', 'data.json')
        except Exception as e:
            raise Exception("Initial data json is missing!") from e

    # Read database in memory.
        with open('data.json', 'r') as json_file:
            json_data = json_file.read()
            self.plant_boxes = jsonpickle.decode(json_data)
            
    # Saving data to locally saved file
    async def save_data(self):
        print("Saving data")
        with open('data.json', 'w') as json_file:
            json_file.write(jsonpickle.encode(self.plant_boxes))

#nog de lampen zelf aan en uit doen, daarom de if
    async def lamp(self, id: int, status: int):
        if status == 1:
            self.plant_boxes[str(id)].light_status = 1
        elif status == 0:  
            self.plant_boxes[str(id)].light_status = 0
        else:
            print("given status is not a valid status for lamp") 
        pass

    async def spray(self, id:int, spraytime:int):
        now = datetime.now()
        self.plant_boxes[str(id)].last_spray = now.strftime("%H:%M:%S")
        print("Spraying at " + str(id) + " for: " + str(spraytime) + " seconds")
        #pomp aan, valve open, pomp uit, valve toe.
    
    async def getwaterlevel():
        return 0.30

    def loop(self):
        pass
