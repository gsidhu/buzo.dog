from fastapi import FastAPI, HTTPException
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
@app.get("/api/v1/storage/fetch")
async def fetch(link: str):
    response = crud.fetch(link)
    return response

## should insert in db on fetch; submit should only make updates if any changes.

# Push info
@app.put("/api/v1/storage/add")
async def store(link: str, title: Optional[str] = None, source: Optional[str] = None,
                description: Optional[str] = None, tags: Optional[str] = None,
                language: Optional[str] = None, author: Optional[str] = None,
                html: Optional[str] = None, text: Optional[str] = None, 
                pubdate: Optional[str] = None):
                collection = {
                    'link': link,
                    'title': title,
                    'source': source,
                    'description': description,
                    'tags': tags,
                    'language': language,
                    'author': author,
                    'text': text,
                    'html': html,
                    'pubdate': pubdate
                }
                if pubdate == None:
                    collection['pubdate'] = ''

                response = crud.add(collection)
                
                if response:
                    return "Success"
                else:
                    return "Fail"
