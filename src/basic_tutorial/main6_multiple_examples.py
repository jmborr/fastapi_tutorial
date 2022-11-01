from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

##################################
# MULTIPLE EXAMPLES FOR INTERACTIVE DOCUMENTATION
# uvicorn --port 8042 main6_multiple_examples:app --reload
##################################

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "description": "We need a valid value for the price!",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

