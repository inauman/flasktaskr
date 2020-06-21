#below two lines are for importing a package from parent or sibling.
import sys
sys.path.insert(0, '..')
from project.views import db
from project._config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()

    # bkup the old table
    c.execute(
        """
        ALTER TABLE tasks RENAME to old_tasks
        """
    )

    # create a new table
    db.create_all()

    # retrieve data from old task table

    c.execute(
        """
        SELECT name, due_date, priority, status FROM old_tasks ORDER BY task_id ASC
        """
    )

    data = [(r[0], r[1], r[2], r[3], datetime.now(), 1) for r in c.fetchall()]

    c.executemany(
        """
        INSERT INTO tasks (name, due_date, priority, status, posted_date, user_id) VALUES(?, ?, ?, ?, ?, ?)
        """, data
    )

    c.execute("DROP TABLE old_tasks")
