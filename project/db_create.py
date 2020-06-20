# project/db_create.py

import sqlite3

#below two lines are for importing a package from parent.
import sys
sys.path.insert(0, '..')

# Above two lines are required for importing _config from root (parent) folder
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()

    query_create = """
    CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL,
    status INTEGER NOT NULL)
    """

    c.execute(query_create)

    c.execute(
        'INSERT INTO tasks(name, due_date, priority, status)'
        'VALUES("Finish this tutorial", "06/25/2020", 10, 1)'
    )

    c.execute(
        'INSERT INTO tasks(name, due_date, priority, status)'
        'VALUES("Finish Django tutorial", "06/31/2020", 10, 1)'
    )