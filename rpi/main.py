from datetime import datetime
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import asyncio
from models import PlantBox
from models import PlantBoxDataReceive
from runner import BackgroundRunner
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import threading


"""
Code for 4-Scientific-project.
By Merlijn Stoffels

If I had more time, I would rewrite a big part of this program to make things more efficient.
"""


app = FastAPI()
# The idea was that most of the logic is handled by runner.py and the javascript. main.py is just a "Bridge" (?) between the two.
runner = BackgroundRunner()

# All of these endpoints are simple and understandable (I hope?) so there is no extra explanation


@app.on_event('startup')
async def app_startup():
    await runner.load_data()
    thread = threading.Thread(target=runner.run_main)
    thread.start()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/howto", response_class=HTMLResponse)
async def read_howto():
    with open("howto.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/gettime")
async def read_gettime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


@app.get("/getwaterlevel")
async def read_getwaterlevel():
    percentage = await runner.getwaterlevel()
    return percentage


@app.get("/getdata")
async def read_getdata():
    await runner.load_data()
    payload = runner.plant_boxes
    return payload


@app.post("/upall")
async def update_plantbox_name(plantbox_data: PlantBoxDataReceive, id: int):

    # Validate
    if str(id) not in runner.plant_boxes:
        return JSONResponse(status_code=404, content={"error": "Plantbox not found"})

    stored_box = runner.plant_boxes[str(id)]
    stored_box.user_update(plantbox_data)
    await runner.save_data()
    runner.reschedule(id)

    return Response(status_code=200)


@app.get("/lamp")
async def lamp(id: int, status: int):
    # Validate
    if str(id) not in runner.plant_boxes:
        return JSONResponse(status_code=404, content={"error": "Plantbox not found"})
    runner.lamp(id, status)
    await runner.save_data()
    return Response(status_code=200)


@app.get("/spraytest")
def spraytest(id: int):
    # Validate
    if str(id) not in runner.plant_boxes:
        return JSONResponse(status_code=404, content={"error": "Plantbox not found"})
    runner.spray(id, runner.plant_boxes[str(id)].spraytime)


@app.get("/prime")
async def prime():
    await runner.prime()


@app.get("/alllamps")
async def alllamps(status: int):
    await runner.all_lamps(status)


@app.get("/getmoisture")
async def getmoisture():
    await runner.getMoisture()


@app.get("/critmoist")
async def critmoist():
    await runner.critMoist()
