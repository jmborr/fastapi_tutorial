# third party imports
from fastapi import FastAPI

app = FastAPI()

##################################
# READING & WRITING to the filesystem
# uvicorn --port 8042 main2_path_file:app --reload
##################################


@app.put("/files{file_path:path}")
async def read_file(file_path: str):
    r"""Creates a text file with fixed content"""
    with open(file_path, 'w') as f:
        f.write("I can write")


@app.get("/files{file_path:path}")
async def read_file(file_path: str):
    r"""Read the contents of a file"""
    with open(file_path, 'r') as f:
        content = f.read()
    return {"content": content}
