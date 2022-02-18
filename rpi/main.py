from asyncore import loop
from datetime import datetime
import string
from turtle import delay
from typing import Optional
from fastapi import FastAPI,logger
from fastapi.responses import HTMLResponse
import asyncio
from runner import BackgroundRunner


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

@app.get("/requestwater")
async def read_requestwater():
    runner.water_requested = True
    

