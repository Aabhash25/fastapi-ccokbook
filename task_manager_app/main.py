from fastapi import FastAPI, HTTPException
from models import(
    Task,
    TaskWithID
)
from operations import read_all_tasks

app = FastAPI()
@app.get("/tasks",response_model=list[TaskWithID])
def get_tasks():
    tasks=read_all_tasks()
    return tasks