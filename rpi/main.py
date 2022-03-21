from datetime import datetime
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import asyncio
import jsonpickle
from models import PlantBox
from models import PlantBoxDataReceive
from runner import BackgroundRunner
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import threading



app = FastAPI()
runner = BackgroundRunner()


@app.on_event('startup')
async def app_startup():
    await runner.load_data()
    # asyncio.create_task(runner.run_main())
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
    return runner.getwaterlevel()


@app.get("/getdata")
async def read_getdata():
    await runner.load_data()
    payload = runner.plant_boxes
    return payload


@app.post("/upall") 
async def update_plantbox_name(plantbox_data: PlantBoxDataReceive, id: int):
    
    #Validate
    if str(id) not in runner.plant_boxes:
        return JSONResponse(status_code=404, content={"error": "Plantbox not found"})

    stored_box = runner.plant_boxes[str(id)]
    stored_box.user_update(plantbox_data)
    await runner.save_data()
    runner.reschedule(id)

    return Response(status_code=200)


@app.get("/lamp")
async def lamp(id: int, status: int):
    #Validate
    if str(id) not in runner.plant_boxes:
        return JSONResponse(status_code=404, content={"error": "Plantbox not found"})
    runner.lamp(id,status)
    await runner.save_data()
    return Response(status_code=200)


@app.get("/spraytest")
async def spraytest(id: int):
    #Validate
    if str(id) not in runner.plant_boxes:
        return JSONResponse(status_code=404, content={"error": "Plantbox not found"})
    await runner.spray(id,runner.plant_boxes[str(id)].spraytime)


    