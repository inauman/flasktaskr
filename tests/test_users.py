import os
import unittest

from project import app, db
from project._config import basedir
from project.models import Task, User

TEST_DB='test.db'

class AllTests(unittest.TestCase):
    ##############################
    ####  setup and teardown  ####
    ##############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +\
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.assertEquals(app.debug, False)
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

    def test_login_form_is_present(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please sign in to access your task list', response.data)

    # helper function
    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True
        )
    
    def test_unregistered_users_cannot_login(self):
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

    def test_invalid_login_form_data(self):
        self.register('Nauman', 'Nauman@Zorigs.Com', 'python', 'python')
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list', response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register(
            'Mayesha', 'mayesha@mayesha.com', 'python', 'python'
        )
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register('Mayesha', 'mayesha@mayesha.com', 'python', 'python')
        self.app.get('register/', follow_redirects=True)
        response = self.register('Mayesha', 'mayesha@mayesha.com', 'python', 'python')
        self.assertIn(b'That username and/or email already exist', response.data)

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)
    
    def test_logged_in_users_can_logout(self):
        self.register('Mayesha', 'mayesha@mayesha.com', 'python', 'python')
        self.login('Mayesha', 'python')
        response = self.logout()
        self.assertIn(b'Goodbye', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye', response.data)

    def test_logged_in_users_can_access_tasks_age(self):
        self.register('Mayesha', 'mayesha@mayesha.com', 'python', 'python')
        self.login('Mayesha', 'python01')
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You need to login first', response.data)

    def test_default_user_role(self):
        db.session.add(
            User('Nauman', 'Nauman@Nauman.com', 'python')
        )
        db.session.commit()
        users = db.session.query(User).all()
        print('************')
        print(users)
        for user in users:
            self.assertEquals(user.role, 'user')

if __name__ == "__main__":
    unittest.main()