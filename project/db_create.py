# project/db_create.py



#below two lines are for importing a package from parent.
import sys
sys.path.insert(0, '..')

from project.views import db
from project.models import Task
from datetime import date

db.create_all()

db.session.add(Task("Finish this tutorial", date(2020, 6, 21), 10, 1))
db.session.add(Task("Finish Real Python", date(2020, 6, 30), 10, 1))

db.session.commit()

