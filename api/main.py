from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional

from pydantic import BaseModel

from helper_code import activity_puller, db_search
import json 

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "http://192.168.1.7:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

langs = ['hi', 'en', 'pb', 'gj', 'od', 'ma', 'ta', 'ur']

@app.get("/")
async def root():
    return {
        "name": "Chachi API",
        "version": "1.0.0",
        "author": "Gurjot Sidhu",
        "contact": "hello@thatgurjot.com",
        "support": "contact@chachi.app"
    }

# Regular functioning
@app.get("/v1/bank/{lang}/random")
async def main(lang: str):
    if lang not in langs:
        raise HTTPException(status_code=404, detail="Invalid language input.")

    act_array, meta = get_acts(lang=lang)
    current_act_array = {'ids': list(act_array.keys())}

    response = {
        "act_list": current_act_array,
        "acts": act_array,
        "meta": meta
    }

    return response

def get_acts(lang='hi'):
    act_array = activity_puller.give_act_array(lang)
    metadata = {}
    ids = list(act_array.keys())
    for i in ids:
        metadata[i] = activity_puller.pull_meta(id=i,lang=lang)

    return act_array, metadata

# Tags response
@app.get("/v1/bank/{lang}/tags-list")
async def tags(lang: str):
    if lang not in langs:
        raise HTTPException(status_code=404, detail="Invalid language input.")

    tag_counts = db_search.create_counts_dict(lang)
    tags = list(tag_counts.keys())
    tag_list = []
    for i in range(len(tags)):
        tag_object = {"id": i, "title": tags[i], "search": tags[i].replace(' ', '-')}
        tag_list.append(tag_object)
    # tag_list = list(tag_counts.keys())
    response = {
            "tag_counts": tag_counts,
            "tag_list": tag_list
        }

    return response

@app.get("/v1/bank/{lang}/tags/{tag_search}")
async def tag_response(lang: str, tag_search: str):
    
    if lang not in langs:
        raise HTTPException(status_code=404, detail="Invalid language input.")

    requested_tags = tag_search.split('+')
    current_tags = (', ').join(requested_tags)

    try:
        act_array, meta = get_acts_for_tags(tags=requested_tags, lang=lang)
    except IndexError:
        return HTTPException(status_code=404, detail="Invalid tags input.")

    current_act_array = {'ids': list(act_array.keys())}

    # if unrelated tags are passed
    if len(current_act_array['ids']) == 0:
        return HTTPException(status_code=404, detail="Incompatible tags input.")
    # otherwise, normal operation
    else:
        response = {
            "act_list": current_act_array,
            "acts": act_array,
            "meta": meta,
            "current_tags": current_tags
        }
        return response

def get_acts_for_tags(tags, lang='hi'):
    act_array = db_search.give_act_array(tags=tags, lang=lang)
    metadata = {}
    ids = list(act_array.keys())
    for i in ids:
        metadata[i] = activity_puller.pull_meta(id=i,lang=lang)
    return act_array, metadata

########################################
# Insider business ## 4 sexy eyes only #
########################################
@app.get("/v1/bank/{lang}/specific/sauce/ingredient/{code}")
async def sexy(lang: str, code: str):
    if lang not in langs:
        raise HTTPException(status_code=404, detail="Invalid language input.")

    act_array = activity_puller.generate_activity([code],lang=lang)
    current_act_array = {'ids': [code]}
    meta = activity_puller.pull_meta(id=code, lang=lang)

    response = {
        "act_list": current_act_array,
        "acts": act_array,
        "meta": meta
    }

    return response