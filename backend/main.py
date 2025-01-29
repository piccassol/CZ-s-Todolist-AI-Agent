from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3

app = FastAPI()

# Database setup
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    category TEXT,
                    priority INTEGER,
                    due_date TEXT,
                    status TEXT
                )""")
conn.commit()

# Task Model
class Task(BaseModel):
    task: str
    category: str
    priority: int
    due_date: str

# Add Task
@app.post("/add_task/")
def add_task(task: Task):
    cursor.execute("INSERT INTO tasks (task, category, priority, due_date, status) VALUES (?, ?, ?, ?, ?)",
                   (task.task, task.category, task.priority, task.due_date, "pending"))
    conn.commit()
    return {"message": "Task added successfully"}

# Get Tasks
@app.get("/tasks/")
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return {"tasks": tasks}

# Update Task Status
@app.put("/update_task/{task_id}")
def update_task(task_id: int, status: str):
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    return {"message": "Task updated"}

# Delete Task
@app.delete("/delete_task/{task_id}")
def delete_task(task_id: int):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return {"message": "Task deleted"}
