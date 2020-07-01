# db_create.py

from project import db, bcrypt
from project.models import Task, User
from datetime import date

# create the database and the db table
db.create_all()

# # insert data
# db.session.add(
#     User("admin", "ad@min.com", bcrypt.generate_password_hash("admin"), "admin")
# )
# db.session.add(
#     Task("Finish this tutorial", date(2015, 3, 13), 10, date(2015, 2, 13), 1, 1)
# )
# db.session.add(
# Task("Finish Real Python", date(2015, 3, 13), 10, date(2015, 2, 13), 1, 1)
# )
db.session.commit()

