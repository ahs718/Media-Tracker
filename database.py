import sqlite3
from typing import List
import datetime
from model import Todo

conn = sqlite3.connect("todos.db")
c = conn.cursor()


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS todos (
        task text,
        category text,
        date_added text,
        date_completed text,
        status integer,
        position integer
        )""")


create_table()


def insert_todo(todo: Todo):
    c.execute("select count(*) FROM todos")
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        # using parameter subsitution syntax prevents sql injection attacks
        c.execute("INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :position)",
                  {"task": todo.task, "category": todo.category, "date_added": todo.date_added, "date_completed": todo.date_completed, "status": todo.status, "position": todo.position})


def get_all_todos() -> List[Todo]:
    c.execute("select * from todos")
    results = c.fetchall()
    todos = []
    for result in results:
        # unpacks all arguments and puts them into contructor for Todo class
        todos.append(Todo(*result))
    return todos
