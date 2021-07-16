from datetime import datetime
from fastapi import FastAPI, Body
from starlette.responses import Response
from database.object import db

from utils.coords import coords_data
app = FastAPI()

@app.on_event("startup")
async def connect_db():
    await db.connect()


@app.on_event("shutdown")
async def disconnect_db():
    await db.disconnect()()

@app.get("/zone", tags=['zipcode', 'categories'])
#async def check_zone(response: Response, lat: float=Body(..., embed=True), lon:float=Body(...,embed=True)):
async def check_zone(response: Response, lat: float, lon:float):
    """Returns if the zone is:
        0: not know, unavailable for service
        1: Available for service
        2: Available and the company has an interest on it
        3: Inside the available limits but forbidden for work in"""
    name = '> Alberto Ortiz test | '
    name += str(datetime.now())
    name += ' <'
    print("# ~ " * 13)
    print(name)
    print("# ~ " * 13)
    response = await coords_data(lat, lon, name)

    return response