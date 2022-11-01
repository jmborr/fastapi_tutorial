from typing import Optional, Union

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


#############################################
# MODEL ATTRIBUTES CAN HAVE VALIDATORS
# uvicorn --port 8042 main4_model_validation:app --reload
#############################################

class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(default=None,
                                          title="The description of the item",
                                          max_length=300)
    price: float = Field(gt=0,
                         description="The price must be greater than zero")
    image: Optional[Image] = None  # NESTED MODEL


@app.put("/items/{item_id}")
async def update_item(item_id: int,
                      item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results