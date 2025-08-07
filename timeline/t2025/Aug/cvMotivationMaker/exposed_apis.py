from .CVMotivationMaker import generateCV, generateSummary, generateMotivation
from fastapi import FastAPI
from pydantic import BaseModel
from .db import addData, deleteDataWithId, deleteDataWhere, readAllWithPagination, \
    readAsDic, readWhere, updateData, readAll
app = FastAPI()
import inspect

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Command(BaseModel):
    name: str
    params: list | None = None

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/run/")
def run_cmd(command: Command):
    params = command.params
    if params is None:
        params = []
    return eval(command.name)(*params)

@app.post("/async/run/")
async def run_cmd(command: Command):
    params = command.params
    if inspect.iscoroutinefunction(eval(command.name)):
        return await eval(command.name)(*params)
    else:
        return eval(command.name)(*params)

    

def get_app():
    return app
def run_app():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn main:app --reload

