from fastapi import FastAPI, Query, Path

app = FastAPI()

##################################
# PARAMETERS MISSING FROM THE GET DECORATOR ARE IMPLICITLY ASSUME TO BE QUERIES
# uvicorn --port 8042 main3_query_params:app --reload
##################################


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int,
    item_id: str = Path(title="The ID of the item to get"),
    short: bool = False,
    short_query: int = Query(default=0, ge=0)
):
    r"""
    :param user_id: an implicit Path parameter
    :param item_id: an explicit Path parameter
    :param short:   an implicit Query parameter
    :param short_query: an explicit Query parameter
    """
    if short or short_query:
        return "amen"
    else:
        return """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent porttitor hendrerit lacus vel
bibendum. Mauris a libero mi. Donec mattis urna sit amet sapien maximus semper. Etiam sed elit sed metus ultrices
porttitor. Pellentesque condimentum, odio in consectetur facilisis, dolor elit luctus dui, nec tempus ligula nisi
sed ligula. Pellentesque semper justo ut libero gravida condimentum. Aliquam porta tellus felis, nec fringilla arcu
faucibus eu."""
