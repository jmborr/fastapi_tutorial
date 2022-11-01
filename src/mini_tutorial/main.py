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
@app.get("/")  # the "view URL" or "route" is next to the response by the server
@app.get("/greetings")  # routes can be piled on
async def read_root():
    return {"Hello": "World"}  # The response is serialized as a JSON string


#############
# GET HTTP request at http://127.0.0.1:8000/items/42
#############
@app.get("/items/{item_id}")  # "route", "endpoint", or "path" (in FastAPI jargon)
async def read_item(item_id: int,
                    q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


#############################################################

from pydantic import BaseModel
from random import random
import subprocess


#######################
# 1. Like a Django model.
# 2. The class is to a JSON schema what the instance is to a JSON data (type hints are required)
# 3. Instance knows how to (de)serialize itself into a JSON string (parsing & validation of Requests and Responses)
#######################
class Item(BaseModel):
    r"""User makes an offer for an item"""
    name: str
    price: float
    is_offer: Union[bool, None] = None


#############
# PUT HTTP request
# can be tested via http://127.0.0.1:8000/items/docs
# runtime validation, with informative Error responses
#############
async def _ponder_on_offer(is_offer: bool, wait: int = 5):
    subprocess.call(f"sleep {wait}s", shell=True)  # I'm a slow thinker!
    return True if is_offer and random() < 0.5 else False


@app.put("/items/{item_id}")
async def update_item(item_id: int,
                      item: Item):  # Item sent as serialized JSON string
    r"""
    :param item_id: automatically resolved as a path parameter
    :param item: automatically resolved as the Request Body (curl ... -d {JSON(item)})
    :return:
    """
    accept_offer = await _ponder_on_offer(item.is_offer)
    return {"item_name": item.name, "item_id": item_id, "accept_offer": accept_offer}

r"""
All "path operation decorators" implementing a different "HTTP Request Method"

HTTP-REQUEST    DATA-OPERATION
@app.get()         read
@app.post()        create
@app.put()         update
@app.delete()      delete
@app.options()
@app.head()
@app.patch()
@app.trace()
"""