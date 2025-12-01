from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import Task, TaskWithId
from operations import (
    read_all_tasks,
    read_task,
    create_task,
    modify_task,
    remove_task,
    read_all_tasks_v2,
)
from typing import Optional

app = FastAPI(
    title="Task Manager API", description="This is a task manager Api", version="0.1.0"
)


@app.get("/tasks", response_model=list[TaskWithId])
def get_tasks(status: Optional[str] = None, title: Optional[str] = None):
    tasks = read_all_tasks()
    if status:
        task = [task for task in tasks if task.status == status]
        if title:
            tasks = [task for task in tasks if task.title == title]
    return tasks


@app.get("/tasks/search", response_model=list[TaskWithId])
def search_tasks(keyword: str):
    tasks = read_all_tasks()
    filtered_tasks = [
        task
        for task in tasks
        if keyword.lower() in (task.title + task.description).lower()
    ]
    return filtered_tasks


@app.get("/task/{task_id}")
def get_task(task_id: int):
    task = read_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/task", response_model=TaskWithId)
def add_task(task: Task):
    return create_task(task)


class UdpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


@app.put("/task/{task_id}", response_model=TaskWithId)
def update_task(task_id: int, task_update: UdpdateTask):
    modified = modify_task(task_id, task_update.model_dump(exclude_unset=True))
    if not modified:
        raise HTTPException(status_code=404, detail="task not found")
    return modified


@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id: int):
    removed_task = remove_task(task_id)
    if not removed_task:
        raise HTTPException(status_code=404, detail="task not found")
    return removed_task


from models import TaskV2WithID


@app.get("/v2/tasks", response_model=list[TaskV2WithID])
def get_tasks_v2():
    tasks = read_all_tasks_v2()
    return tasks


from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from security import (
    UserInDB,
    fake_token_generator,
    fakely_hash_password,
    fake_usersa_db,
)


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_usersa_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = fakely_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = fake_token_generator(user)
    return {"access_token": token, "token_type": "bearer"}


from security import get_user_from_token, User


@app.get("/users/me", response_model=User)
def read_users_me(
    current_user: User = Depends(get_user_from_token),
):
    return current_user
