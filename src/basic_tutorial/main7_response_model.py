from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

##################################
# DECLARE THE RESPONSE BODY
# uvicorn --port 8042 main7_response_model:app --reload
##################################


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


class SecretItem(Item):
    secret: str


secret_items = {
    "foo": {"name": "Foo", "secret": "asrr", "price": 50.2},
    "bar": {"name": "Bar", "secret": "Bs#$r", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "secret": "?FE%", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}",
         response_model=Union[Item, str],  # Will drop the secret
         response_model_exclude_unset=True)
async def read_item(item_id: str):
    # Conversions dict --> Item --> JSON
    return secret_items.get(item_id,
                            f"Item '{item_id}' not found")
