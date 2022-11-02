from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


# Database "indexed" by username
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):  # Notice it's a model that inherits from another model
    hashed_password: str


app = FastAPI()

#################################################
# LOGIN MECHANISM IN PLACE
# ./start_main main3
#################################################


def fake_hash_password(password: str):
    r"""In the database, replace the password with a hash"""
    return "fakehashed" + password


# when called, oauth2_scheme will redirect to http://127.0.0.1:8042/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    r"""Present a login form, and generate a token"""
    # verify the user is in the database and retrieve content
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)

    # verify the entered password agrees with what's stored in the database
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username,  # very crappy token-generator (Jason Web Tokens available)
            "token_type": "bearer"}


def get_user_from_token(token: str):
    r"""Query the database for a User"""
    username = token  # the inverse of our crappy token-generator
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    r"""Get User content from database, requires login for authentication"""
    user = get_user_from_token(token)  # the login steps gives us a token we can use to query the database
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    r"""Check the user is active"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    r"""get a user if the user exists, is correctly authenticated, and is active"""
    return current_user
