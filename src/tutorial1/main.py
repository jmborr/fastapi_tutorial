# third party imports
from fastapi import FastAPI

# standard imports
from typing import Union

##############
# Fire up with `uvicorn main:app --reload
##############
app = FastAPI()


#############
# GET HTTP request at http://127.0.0.1:8000/
#############
@app.get("/")  # the view URL is next to the response by the server
async def read_root():
    return {"Hello": "World"}  # The response is serialized as a JSON string


#############
# GET HTTP request at http://127.0.0.1:8000/items/42
#############
@app.get("/items/{item_id}")
async def read_item(item_id: int,
                    q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


#############################################################

from pydantic import BaseModel
from random import random


#######################
# Like a Django model.
# Knows how to (de)serialize itself into a JSON string
#######################
class Item(BaseModel):
    r"""User makes an offer for an item"""
    name: str
    price: float
    is_offer: Union[bool, None] = None


#############
# PUT HTTP request
# can be tested via http://127.0.0.1:8000/items/docs
#############
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):  # Item sent as serialized JSON string
    accept_offer = True if item.is_offer and random() < 0.5 else False
    return {"item_name": item.name, "item_id": item_id, "accept_offer": accept_offer}
