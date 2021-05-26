from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional

from pydantic import BaseModel

import crud
import json 

app = FastAPI()

origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "http://192.168.1.60:8080",
    "https://buzo.dog"
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
        "name": "Buzo.Dog API",
        "version": "1.0.0",
        "author": "Gurjot Sidhu",
        "contact": "contact@thatgurjot.com"
    }

# Pull info
@app.get("/api/v1/resources/links")
async def main(count: Optional[int] = None, source: Optional[str] = None,
             iD: Optional[str] = None, link: Optional[str] = None):
    if source is None:
        if iD is None:
            if link is None:
                result = crud.read(count=count)
            else:
                result = crud.read(link=link)
        else:
            result = crud.read(id=iD)
    else:
        result = crud.read(count=count, source=source)
    return result

# Fetch link details
@app.get("/api/v1/storage/add")
async def store(link: str):
    response = crud.fetch(link)
    # if it's a new link, add it to db
    if 'exists' not in response.keys():
        location = crud.add(response)
        response['_id'] = location
    
    del response['text']
    del response['html']
    del response['image']
    del response['pubdate']
    return response

## should insert in db on fetch; submit should only make updates if any changes.

# Push info
@app.post("/api/v1/storage/update")
async def update(iD: str, title: Optional[str] = None, source: Optional[str] = None,
                description: Optional[str] = None, tags: Optional[str] = None,
                language: Optional[str] = None, author: Optional[str] = None,
                likes: Optional[str] = None):
                queries = {
                    '_id': iD,
                    'title': title,
                    'source': source,
                    'description': description,
                    'tags': tags,
                    'language': language,
                    'author': author,
                    'likes': likes
                }
                collection = {}
                for k in queries.keys():
                    if queries[k] != None:
                        if k == 'likes':
                            collection[k] = int(queries[k])
                        else:
                            collection[k] = queries[k]

                response = crud.update(collection)
                
                if response:
                    return {"success": 1}
                else:
                    return {"success": 0}

# Delete item from DB
@app.delete("/api/v1/storage/purge")
async def delete(iD: str):
    response = crud.delete(iD)
    return {"deleted": response}