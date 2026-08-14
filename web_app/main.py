"""The main web app for my cool new service"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main():
    """The root endpoint as a testbed"""
    return {"hello": "world"}
