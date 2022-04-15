import asyncio
from pickle import FALSE
from xml.dom.minidom import Element
from models import PlantBox
import os
import shutil
import jsonpickle
from datetime import datetime
import schedule
import time
import re
import RPi.GPIO as GPIO




class BackgroundRunner:
    def __init__(self):

        self.plant_boxes = {
            1: PlantBox(1),
            2: PlantBox(2),
            3: PlantBox(3),
            4: PlantBox(4)
        }

    def run_main(self):

        self.time_pump_safety = 0.5
        self.time_pump_prime = 0

        self.lamp_1_pin = 1
        self.lamp_2_pin = 7
        self.lamp_3_pin = 8
        self.lamp_4_pin = 25
        self.valve_1_pin = 0
        self.valve_2_pin = 5
        self.valve_3_pin = 6
        self.valve_4_pin = 13
        self.pump_pin = 19

        self.lamppin_array = [self.lamp_1_pin, self.lamp_2_pin, self.lamp_3_pin, self.lamp_4_pin]
        self.valvepin_array = [self.valve_1_pin, self.valve_2_pin, self.valve_3_pin, self.valve_4_pin]
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        chan_list = [self.lamp_1_pin, self.lamp_2_pin, self.lamp_3_pin,  self.lamp_4_pin, self.valve_1_pin, self.valve_2_pin, self.valve_3_pin, self.valve_4_pin, self.pump_pin]  
        GPIO.setup(chan_list, GPIO.OUT)

        while True:
            time.sleep(1)
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
        for i in range(1, 5):
            self.reschedule(i)

    # Saving data to locally saved file

    async def save_data(self):
        print("Saving data")
        with open('data.json', 'w') as json_file:
            json_file.write(jsonpickle.encode(self.plant_boxes))

# nog de lampen zelf aan en uit doen, daarom de if

    def lamp(self, id: int, status: int):
        if status == 1:
            self.plant_boxes[str(id)].light_status = 1  
        elif status == 0:
            self.plant_boxes[str(id)].light_status = 0
        else:
            print("given status is not a valid status for lamp")

        GPIO.output(self.lamppin_array[id-1], status)
        print("Turning " + str(id) + " " + str(status) + " gedoe")




    # als deze gecalled wordt via test spray runned die niet in een aparte thread en dan staat alles stil voor spraytime aantal seconde
    def spray(self, id: int, spraytime: int):
        now = datetime.now()
        self.plant_boxes[str(id)].last_spray = now.strftime("%H:%M:%S")
        print("Spraying at " + str(id) + " for: " + str(spraytime) + " seconds")

        # Valve open
        GPIO.output(self.valvepin_array[id-1], True)
        # Small safety time, to open valve fully
        time.sleep(self.time_pump_safety)
        # Turn on pump
        GPIO.output(self.pump_pin, True)
        # Let pump run for spraytime + a priming time
        time.sleep(spraytime + self.time_pump_prime)
        # Turn of pump
        GPIO.output(self.pump_pin, False)
        # Wait for safety
        time.sleep(self.time_pump_safety)
        # Close valves
        GPIO.output(self.valvepin_array[id-1], False)
        print("Spray done")


    async def getwaterlevel():
        return 0.30

    def reschedule(self, id):
        plantbox = self.plant_boxes[str(id)]
        schedule.clear(str(id))
        schedule.every().day.at(plantbox.lona).do(
            lambda: self.lamp(id, 1)).tag(str(id))
        schedule.every().day.at(plantbox.lofa).do(
            lambda: self.lamp(id, 0)).tag(str(id))

        schedulearray = plantbox.schedule.split("\n")
        for i in schedulearray:
            if i.strip() == "":
                continue
            scoop = re.match("[0-2][0-9]:[0-5][0-9]", i)
            if scoop:
                schedule.every().day.at(i).do(lambda: self.spray(id,plantbox.spraytime)).tag(str(id))
            


    def loop(self):
        schedule.run_pending()
        pass
