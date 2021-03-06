import os
import unittest

from project import app, db, bcrypt
from config import basedir
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

    # helper function
    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True
        )
    
    def register(self, name, email, password, confirm):
        return self.app.post('register/', data=dict(
            name=name, email=email, password=password, confirm=confirm), follow_redirects=True
        )

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=bcrypt.generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data = dict(
            name = 'Go to the Bank',
            due_date = '10/08/2016',
            priority = '1',
            posted_date = '10/08/2016',
            status = '1'
        ), follow_redirects = True)

    def create_admin_user(self):
        new_user = User('Superman', 'admin@admin.com', bcrypt.generate_password_hash('admin'), 'admin')
        db.session.add(new_user)
        db.session.commit()

    def test_unregistered_users_cannot_login(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password', response.data)
    
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
    
    def test_users_can_add_task(self):
        self.create_user('Nauman', 'nauman@nauman.com', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'New entry was successfully posted.', response.data)

    def test_users_cannot_add_tasks_when_error(self):
        self.create_user('Nauman', 'nauman@nauman.com', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
            name = 'Go to the Bank',
            due_date = '',
            priority = '1',
            posted_date = '10/08/2016',
            status = '1'
        ), follow_redirects = True)
        self.assertIn(b'This field is required', response.data)

    def test_users_can_complete_tasks(self):
        self.create_user('Nauman', 'nauman@nauman.com', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b'The task is complete', response.data)

    def test_users_can_delete_tasks(self):
        self.create_user('Nauman', 'nauman@nauman.com', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b'The task was deleted', response.data)
    
    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('Nauman', 'nauman@nauman.com', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('Mayesha', 'mayesha@mayesha.com', 'python')
        self.login('Mayesha', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertNotIn(
            b'The task is complete.', response.data)
        self.assertIn(b'You can only update tasks that belong to you.', response.data)
    
    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.create_user('Nauman', 'Nauman@Nauman.com', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('Mayesha', 'Mayesha@Mayesha.com', 'python')
        self.login('Mayesha', 'python')
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b'You can only delete tasks that belong to you.', response.data)

    def test_admin_users_can_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('Nauman', 'Nauman@Nauman.com', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'admin')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertNotIn(b'You can only update tasks that belong to you', response.data)
    
    def test_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
        self.create_user('Nauman', 'Nauman@Nauman.com', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'admin')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertNotIn(b'You can only delete tasks that belong to you', response.data)

    def test_task_template_displays_logged_in_user_name(self):
        self.register('Nauman', 'Nauman@Nauman.com', 'python', 'python')
        self.login('Nauman', 'python')
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'Nauman', response.data)
    
    def test_users_cannot_see_task_modify_links_for_tasks_not_created_by_them(self):
        self.register('Nauman', 'nauman@realpython.com', 'python', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.register('Mayesha', 'mayesha@realpython.com', 'python', 'python')
        self.login('Mayesha', 'python')
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertNotIn(b'Mark as complete', response.data)
        self.assertNotIn(b'Delete', response.data)

    def test_users_can_see_task_modify_links_for_tasks_created_by_them(self):
        self.register('Nauman', 'nauman@realpython.com', 'python', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.register('Mayesha', 'mayesha@realpython.com', 'python', 'python')
        self.login('Mayesha', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'delete/2/', response.data)
    
    def test_admin_users_can_see_task_modify_links_for_all_tasks(self):
        self.register('Nauman', 'nauman@realpython.com', 'python', 'python')
        self.login('Nauman', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'admin')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'complete/1/', response.data)
        self.assertIn(b'delete/1/', response.data)
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'delete/2/', response.data)

if __name__ == "__main__":
    unittest.main()