from datetime import datetime
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
    await runner.load_data()
    asyncio.create_task(runner.run_main())


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


@app.get("/getdata")
async def read_getdata():
    await runner.load_data()
    payload = runner.plant_boxes
    return payload


@app.post("/updatename")
async def update_plantbox_name(value: str, id: int):
    print(id,value)
    await runner.load_data()
    #Validate
    if id not in runner.plant_boxes:
        return JSONResponse(status_code=404, content={"error": "Plantbox not found"})
    runner.update_name(id, value)
    return Response(status_code=200)


@app.post("/updatedate")
async def update_plantbox_date(value: str, id: int):
    await runner.load_data()
    # Validate
    if id not in runner.plant_boxes:
        return JSONResponse(status_code=404, content={"error": "Plantbox not found"})

    runner.update_date(id, value)
    return Response(status_code=200)


    