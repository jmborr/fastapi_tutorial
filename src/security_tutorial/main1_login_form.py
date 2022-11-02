from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
import subprocess
import os
app = FastAPI()

#################################################
# ADDS A FORM FOR ENTERING USERNAME AND PASSWORD
# ./start_main main1
#################################################


# URL http://127.0.0.1:8000/token will call its associated Path Operation Function
# and generate an authorization token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):  # oauth2_scheme receives an HTTPRequest
    return {"token": token}

