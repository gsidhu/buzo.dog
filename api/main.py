from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional
from pydantic import BaseModel

import db_manager

app = FastAPI()

origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "http://192.168.1.41:8080",
    "https://buzo.xyz"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "buzo.xyz API",
        "version": "1.1.0",
        "author": "Gurjot Sidhu",
        "contact": "contact@thatgurjot.com"
    }

# Pull info
@app.get("/api/v1/resources/links")
async def main(count: Optional[int] = 1, source: Optional[str] = None,
             link: Optional[str] = None):
    result = db_manager.read(count=count, source=source, link=link)
    return result

# Add item to DB
@app.post("/api/v1/storage/add")
async def store(link: str):
    response = db_manager.read(link=link,short=1)
    # if it's a new link, add it to db
    if response == []:
        response = db_manager.add(link)
    else:
        response = response[0]
        response['exists'] = True
    return response

# Delete item from DB
@app.delete("/api/v1/storage/purge")
async def delete(link: str):
    response = db_manager.delete(link)
    return {"deleted": response['response']}

# Update item in DB
@app.post("/api/v1/storage/update")
async def update(link: str, likes: int):
    response = db_manager.update(link, likes)
    return response