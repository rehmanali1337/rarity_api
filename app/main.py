from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api import routes
from api import store
from api.rarity import connect_drivers
import requests
import asyncio


app = FastAPI()

allowed_origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"status": 200}


def is_hub_ready():
    valid_messages = ["No spare hub capacity", "Hub has capacity"]
    try:
        res = requests.get("http://selenium-hub:4444/status").json()
        if res["status"] == 0:
            return res['value']["message"] in valid_messages
        return False
    except Exception as e:
        return False


@app.on_event('startup')
async def startup():
    while not is_hub_ready():
        print('Hub is not ready')
        await asyncio.sleep(1)

    print('Connecting the drivers...')
    connect_drivers()
    print('All drivers connected!')

app.include_router(routes.router)
