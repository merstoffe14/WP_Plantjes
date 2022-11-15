
# Scientific project: Automated watering system.

For our course "Scientific project" we had to work out a system that automatically waters plants. While my colleague Wolf worked on the Mechanical side of the project, I developed the in-depth control interface (A website) on which the user is able to read out and set different parameters for each individual row of plants. 

With this website, you could also make different watering schedules (time of day, amount, ...) for each individual row of plants.

To realize this I used: Python, FastAPI, HTML, css, javascript, bootstrap, RPi.GPIO, Adafruit_GPIO.SPI, Adafruit_MCP3008

## File explanation

/WP_Plantjes/extra_docs
* RPI_pins_and_commands.txt : A file I used to remember some important commands and the * pins used on the RPI
* WP_Code dikke lijnen.pdf  : A pdf with the code flowchart
* WP_Water flow chart.pdf   : A pdf with the water flowchart
* user_manual_g1.pdf        : [The user manual](https://github.com/merstoffe14/WP_Plantjes/blob/main/extra_docs/user_manual_g1.pdf)


/WP_Plantjes/code/rpi:
* data.json        : the file where the rpi saves its data
* howto.html       : the webpage that shows when you press the how to button.
* index.html       : the homepage of the system
* init_data.json   : when there is no data.json, it copies this one. it is filled with placeholder data.
* main.py          : The main code, receives and sends everything to and from the web interface and communicates the data to the runner.py
* models.py        : Define different objects
* requirements.txt : The packages needed for the software to work (not all of these are needed, there are unused packages.)
* runner.py        : receives data from main.py. calculates and schedules everything. 

/WP_Plantjes/3d
* kast_schets.ipt  : A 3d model of the first idea.

/WP_Plantjes/images
* a couple of images of the finished/WIP project.

## User manual
We also had to make a user manual [user manual](https://github.com/merstoffe14/WP_Plantjes/blob/main/extra_docs/user_manual_g1.pdf)


## Pictures
Front view            |  Side view
:-------------------------:|:-------------------------:
![The front view](https://github.com/merstoffe14/WP_Plantjes/blob/main/images/frontview.jpg?raw=true)|![The side view](https://github.com/merstoffe14/WP_Plantjes/blob/main/images/SideView.jpg?raw=true)

Control circuitry            |  Power supply/management
:-------------------------:|:-------------------------:
![Control circuits](https://github.com/merstoffe14/WP_Plantjes/blob/main/images/control.jpg?raw=true)|![Power](https://github.com/merstoffe14/WP_Plantjes/blob/main/images/power.jpg?raw=true)

Pump and valves            |  Website
:-------------------------:|:-------------------------:
![Pump and valves](https://github.com/merstoffe14/WP_Plantjes/blob/main/images/pumpnvalves.jpg?raw=true)|![Website](https://github.com/merstoffe14/WP_Plantjes/blob/main/images/website.jpg?raw=true)







