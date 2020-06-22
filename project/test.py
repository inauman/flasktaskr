import os
import unittest

import sys
sys.path.insert(0,'..')

from project.views import app, db
from project._config import basedir
from project.models import User

TEST_DB='test.db'

class AllTests(unittest.TestCase):
    ##############################
    ####  setup and teardown  ####
    ##############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +\
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    

    def test_user_setup(self):
        new_user = User("michael", "michael@cycle.org", "michaelherman")
        db.session.add(new_user)
        db.session.commit()

        test =  db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "michael"

    def test_form_is_present(self):     # login form
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to access your task list', response.data)

    # helper function
    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True
        )
    
    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password', response.data)

    # helper function
    def register(self, name, email, password, confirm):
        return self.app.post('register/', data=dict(
            name=name, email=email, password=password, confirm=confirm), follow_redirects=True
        )
    
    def test_registered_users_can_login(self):
        self.register('Nauman', 'Nauman@Zorigs.Com', 'python', 'python')
        response = self.login('Nauman', 'python')
        self.assertIn(b'Welcome', response.data)

if __name__ == "__main__":
    unittest.main()