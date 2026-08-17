"""The main web app for my cool new service"""

import requests
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def main():
    """The root endpoint as a testbed"""
    return {"hello": "world"}


@app.post("/convert/{state}/{city}")
def convert(state, city):
    """Converts a city/state combo to lat/long"""
    data = {"api_key": "6a7f57138e04b429290986wxia11d90", "city": city, "state": state}
    response = requests.get("https://geocode.maps.co/search", params=data, timeout=3)
    print(response.json())
    return {"lat": response.json()[0]["lat"], "long": response.json()[0]["lon"]}
