import asyncio
from models import PlantBox
import os,shutil,jsonpickle


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
            
           


    # SAVE READ PROBLEEM CHECKEN
    # Saving data to locally saved file
    async def save_data(self):
        print("Saving data")
        with open('data.json', 'w') as json_file:
            json_file.write(jsonpickle.encode(self.plant_boxes))


    def loop(self):
        pass
