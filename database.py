import sqlite3
from typing import List
import datetime
from model import Entry

conn = sqlite3.connect("entries.db")
c = conn.cursor()


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS entries (
        title text,
        category text,
        date_added text,
        date_completed text,
        status integer,
        position integer
        )""")


create_table()


def insert_entry(entry: Entry):
    c.execute("select count(*) FROM entries")
    count = c.fetchone()[0]  # gets number of items in table
    entry.position = count if count else 0
    with conn:
        # using parameter subsitution syntax prevents sql injection attacks
        c.execute("INSERT INTO entries VALUES (:title, :category, :date_added, :date_completed, :status, :position)",
                  {"title": entry.title, "category": entry.category, "date_added": entry.date_added, "date_completed": entry.date_completed, "status": entry.status, "position": entry.position})


def get_all_entries() -> List[Entry]:
    c.execute("select * from entries")
    results = c.fetchall()
    entries = []
    for result in results:
        # unpacks all arguments and puts them into contructor for Entry class
        entries.append(Entry(*result))
    return entries


def delete_entry(position):
    c.execute("select count(*) from entries")
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE from entries WHERE position=:position",
                  {"position": position})
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)


def change_position(old_position: int, new_position: int, commit=True):
    c.execute("UPDATE entries SET position = :position_new WHERE position = :position_old",
              {"position_old": old_position, "position_new": new_position})
    if commit:
        conn.commit()


def update_entry(position: int, title: str, category: str):
    with conn:
        if title is not None and category is not None:
            c.execute("UPDATE entries SET title = :title, category = :category WHERE position = :position",
                      {"position": position, "title": title, "category": category})
        elif title is not None:
            c.execute("UPDATE entries SET title = :title WHERE position = :position",
                      {"position": position, "title": title})
        elif category is not None:
            c.execute("UPDATE entries SET category = :category WHERE position = :position",
                      {"position": position, "category": category})


def complete_entry(position: int):
    with conn:
        c.execute("UPDATE entries SET status = 2, date_completed = :date_completed WHERE position = :position",
                  {"position": position, "date_completed": datetime.datetime.now().isoformat()})
