from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List
import requests
import random
import math

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class TodoItem(BaseModel):
    id: int
    task: str
    completed: bool = False

todos: List[TodoItem] = []
id_counter = 1


@app.get("/")
async def get_todos(request: Request):
    cats = requests.get("https://api.thecatapi.com/v1/images/search?limit=10")
    cats = cats.json()
    cats = [cat["url"] for cat in cats]
    cat = random.choice(cats)
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos, "cat": cat })

@app.post("/add")
async def create_todo(task: str = Form(...)):
    global id_counter
    todo = TodoItem(id=id_counter, task=task)
    id_counter += 1
    todos.append(todo)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{todo_id}")
async def delete_todo(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo.id != todo_id]
    return RedirectResponse(url="/", status_code=303)
