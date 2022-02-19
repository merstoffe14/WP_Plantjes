import asyncio
from models import PlantBox



class BackgroundRunner:
    def __init__(self):
        self.water_requested = False

        self.plant_boxes = {
            1: PlantBox(1)#,
            #2: PlantBox(2),
            #3: PlantBox(3),
            #4: PlantBox(4)
        }

    async def run_main(self):
       
       while True:
            await asyncio.sleep(1)
            self.loop()


    def loop(self):
        pass
