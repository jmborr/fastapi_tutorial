# third party imports
from fastapi import FastAPI

# standard imports
from typing import Union

app = FastAPI()

##################################
# PATH's ORDER RESOLUTION
# uvicorn --port 8042 main1_path_resolution:app --reload
##################################

r"""
@app.get("/items/special")
async def special():
    return "I am special"
"""


@app.get("/items/{item_id}")
async def read_item(item_id: int,
                    q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/items/special")
async def special():
    return "I am special"
