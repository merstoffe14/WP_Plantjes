from asyncore import loop
from datetime import datetime
import string
from turtle import delay
from typing import Optional
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import asyncio
from models import PlantBox
from runner import BackgroundRunner
from fastapi.responses import JSONResponse


app = FastAPI()
runner = BackgroundRunner()


@app.on_event('startup')
async def app_startup():
    asyncio.create_task(runner.run_main())


@app.get("/", response_class=HTMLResponse)
async def read_root():
    f = open("index.html", "r")
    html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/gettime")
async def read_gettime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    return current_time

@app.get("/getdata")
async def read_getdata():
    payload = runner.plant_boxes
    return payload


@app.post("/updatename")
def update_plantbox_name(value: str, id: int):
    # Validate
    if id not in runner.plant_boxes:
        return JSONResponse(status_code=404, content={"error": "Plantbox not found"})

    runner.plant_boxes[id].name = value
    return Response(status_code=200)
    

