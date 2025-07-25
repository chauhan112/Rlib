from fastapi import FastAPI
from pydantic import BaseModel
from .ExposedCommands import Controller
app = FastAPI()
ctrl = Controller()

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
    return ctrl.handlers.runCommand(command.name, *params)

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str | None = None):
    return {"item_id": item_id, "query_param": query_param}
def get_app():
    return app
def run_app():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn main:app --reload