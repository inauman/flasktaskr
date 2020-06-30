# db_create.py



from project import db
from project.models import Task, User
from datetime import date

db.create_all()

# insert data
db.session.add(User("admin", "ad@min.com", "admin", "admin"))
db.session.add(Task("Finish this tutorial", date(2020, 6, 21), 10, 1))
db.session.add(Task("Finish Real Python", date(2020, 6, 30), 10, 1))

db.session.commit()

