from typing import Union

from fastapi import Depends, FastAPI, Path
from fastapi.encoders import jsonable_encoder

app = FastAPI()

##################################
# ENCAPSULATE PATH, QUERY, AND BODY PARAMETERS IN A (REUSABLE) CALLABLE
# uvicorn --port 8042 main8_dependency_injection:app --reload
##################################


# A function being called
async def like_kwargs(item_id: int = Path(default=0),
                      name: Union[str, None] = None):
    return {"item_id": item_id, "name": name}


@app.get("/items/{item_id}")
async def read_items(item: dict = Depends(like_kwargs)):
    if item["name"] is None:
        item["name"] = "unknown"
    return item


# A class being instantiated
class LikeKwargs:
    def __init__(self,
                 item_id: int = Path(default=0),
                 name: Union[str, None] = None):
        self.item_id = item_id
        self.name = name


@app.put("/items/{item_id}")
async def read_items(item: LikeKwargs = Depends(LikeKwargs)):
    if item.name is None:
        item.name = "unknown"
    return jsonable_encoder(item)  # vars(item) is OK too


r"""
Depedencies can be stacked
Example: 
  class LikeKwargs:
    def __init__(self,
                 item_id: int = Path(default=0),
                 name: Union[str, None] = None):
        self.item_id = item_id
        self.name = name
"""