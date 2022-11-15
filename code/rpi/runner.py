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
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008




class BackgroundRunner:
    def __init__(self):

        self.plant_boxes = {
            1: PlantBox(1),
            2: PlantBox(2),
            3: PlantBox(3),
            4: PlantBox(4)
        }

    def run_main(self):

        # Define all pins:

        self.moistPower_pin = 26 

        self.trigger_pin = 3
        self.echo_pin = 17

        self.lamp_1_pin = 24
        self.lamp_2_pin = 25
        self.lamp_3_pin = 7
        self.lamp_4_pin = 1 
        self.valve_1_pin = 5
        self.valve_2_pin = 6
        self.valve_3_pin = 13
        self.valve_4_pin = 0
        self.pump_pin = 19

        # Put pins in pinarrays (for ease of use in loops)

        self.lamppin_array = [self.lamp_1_pin, self.lamp_2_pin, self.lamp_3_pin, self.lamp_4_pin]
        self.valvepin_array = [self.valve_1_pin, self.valve_2_pin, self.valve_3_pin, self.valve_4_pin]

        # Define various settings
        self.time_pump_safety = 0.5 # [s]
        self.time_pump_prime = 0 # [s]
        self.TANK_FULL = 3 # [cm]
        self.TANK_EMPTY = 30 # [cm]
        self.MOISTURE_MAX = 750 # [ul]
        self.MOISTURE_MIN = 220 # [ul]
        
        # Set GPIO modes
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        chan_list = [self.lamp_1_pin, self.lamp_2_pin, self.lamp_3_pin,  self.lamp_4_pin, self.valve_1_pin, self.valve_2_pin, self.valve_3_pin, self.valve_4_pin, self.pump_pin]  
        GPIO.setup(chan_list, GPIO.OUT)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.moistPower_pin, GPIO.OUT)
        GPIO.output(self.trigger_pin, GPIO.LOW)

        # Set up ADC mcp3008 (Hardware mode)
        HW_SPI_PORT = 0  # Set the SPI Port. Raspi has two.
        HW_SPI_DEV = 0  # Set the SPI Device
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(HW_SPI_PORT, HW_SPI_DEV))


        # Run the loop, I planned on using this loop more but in the end I only used it to run the scheduler
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

# It would have been easier if status was of type BOOL, but I had some problems with that.
    def lamp(self, id: int, status: int):
        # Setting the light_status var for the shelf
        if status == 1:
            self.plant_boxes[str(id)].light_status = 1
        elif status == 0:
            self.plant_boxes[str(id)].light_status = 0
        else:
            print("given status is not a valid status for lamp")

        # Actually turning the lamp on/off
        GPIO.output(self.lamppin_array[id-1], status)
        print("Turning lamp " + str(id) + " to " + str(status))

        
    # if this function is called via test spray it does not run in a separate thread and then everything stops for a spraytime number of seconds (Notice the clock on the web interface)
    # A solution would be to make this function async, but then I get problems in the scheduler with lambda.
    # The save_data is not called async either. This causes a warning in the console.
    def spray(self, id: int, spraytime: int):
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

        self.save_data()

    # The logic for this sensor is from: https://www.freva.com/nl/hc-sr04-ultrasone-sensor-gebruiken-met-raspberry-pi/
    async def getwaterlevel(self):

        print("Measuring water distance")
        distance = []
        for i in range(5):
            time.sleep(0.1)
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001) 
            GPIO.output(self.trigger_pin, GPIO.LOW)

            while GPIO.input(self.echo_pin) == 0:

                    pulse_start_time = time.time()
            while GPIO.input(self.echo_pin)==1:

                    pulse_end_time = time.time()

            pulse_duration = pulse_end_time - pulse_start_time
            distance.append(round(pulse_duration * 17150, 2))
            

        # Take average of 5 measurements. This is an attempt at decreasing the constant small updates to the progress bar, if this is not sufficient, I will use a rolling avg.
        avg = sum(distance)/len(distance)
        print("Distance:",avg,"cm")
        tank_level = 1 - (avg-self.TANK_FULL)/(self.TANK_EMPTY-self.TANK_FULL)
        if (tank_level > 1):
            tank_level = 1
        elif (tank_level < 0):
            tank_level = 0

        print(tank_level)
        return tank_level

    async def all_lamps(self, status):
        for x in range(4):
            GPIO.output(self.lamppin_array[x], status)

    # This function exsists to get some water in the lines.
    async def prime(self):
        for x in range(4):
            GPIO.output(self.valvepin_array[x], True)
        time.sleep(self.time_pump_safety)
        GPIO.output(self.pump_pin, True)
        time.sleep(0.5)
        GPIO.output(self.pump_pin, False)
        for x in range(4):
            GPIO.output(self.valvepin_array[x], False)


    # This function can be way more efficient.
    # It takes 10 measurments per sensor and takes the avg.
    async def getMoisture(self):
        GPIO.output(self.moistPower_pin, GPIO.HIGH)
        moistlist = [[],[],[],[]]
        moistval = []
        moistperc = []

        for i in range(10):
            time.sleep(0.1)
            print("moist sensing loop: " + str(i))
            moistlist[3].append(self.mcp.read_adc(0))
            moistlist[2].append(self.mcp.read_adc(1))
            moistlist[1].append(self.mcp.read_adc(2))
            moistlist[0].append(self.mcp.read_adc(3))

        print(moistlist)

        for i in range(4):
            plantbox = self.plant_boxes[str(i+1)]
            moistval.append(sum(moistlist[i])/len(moistlist[i]))
            moistperc.append((moistval[i] - self.MOISTURE_MIN)/(self.MOISTURE_MAX-self.MOISTURE_MIN))
            calcHumid = round((1 - moistperc[i]), 2)
            if (calcHumid > 1):
                calcHumid = 1
            if (calcHumid < 0):
                calcHumid = 0
            plantbox.humidity = calcHumid
            print(plantbox.humidity)

        GPIO.output(self.moistPower_pin, GPIO.LOW)
        await self.save_data()

    async def critMoist(self):
        for i in range(4):
            plantbox = self.plant_boxes[str(i+1)]
            if (plantbox.humidity < plantbox.crithumid):
                self.spray(i+1,plantbox.spraytime)


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
        # This is a debug print
        print(schedule.get_jobs('1'))
        pass
