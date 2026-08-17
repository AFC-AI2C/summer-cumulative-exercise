"""The main web app for my cool new service"""

import json
import os
from datetime import datetime, timezone

import requests
from fastapi import FastAPI
from pydantic import BaseModel

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


# ----------- Written for Day 1 - Afternoon ----------- #


@app.get("/comments")
def get_comments():
    """Retrieve all comments on the website"""
    if not "comments.json" in os.listdir():
        return []
    with open("comments.json", "r", encoding="utf-8") as in_file:
        return json.loads(in_file.read())


class Comment(BaseModel):  # pylint: disable=too-few-public-methods
    """Base comment model"""

    comment: str
    created: datetime | None = None


@app.post("/comments", status_code=201)
def post_comment(comment: Comment):
    """Add a new comment to the website"""

    # need to handle concurrency here for a bigger app....
    comments = []

    # read the existing comments
    if "comments.json" in os.listdir():
        try:
            with open("comments.json", "r", encoding="utf-8") as in_file:
                comments.extend(json.load(in_file))
        except json.JSONDecodeError:
            # Corrupted file, start fresh
            comments = []

    # add our new comments to the list
    with open("comments.json", "w", encoding="utf-8") as out_file:
        comment.created = datetime.now(timezone.utc)
        comments.append(comment.model_dump(mode="json"))
        json.dump(comments, out_file)

    return {"created": comment}
