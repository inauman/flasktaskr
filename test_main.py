import os
import unittest

from project import app, db
from config import basedir
from project.models import User

TEST_DB = "test.db"

class MainTests(unittest.TestCase):

    ###############################
    ##### setup and teardown ######
    ###############################
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ###############################
    ####### helper methods ########
    ###############################
    
    def login(self, username, password):
        return self.app.post('/', data=dict(
            name=username, password=password), follow_redirects=True
        )

    ###############################
    ############ tests ############
    ###############################

    def test_404_error(self):
        response = self.app.get('/this-route-does-not-exist/')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b'Sorry. There\'s nothing here.', response.data)
    
    def test_500_error(self):
        bad_user = User(
            name='Jeremy', 
            email='jeremy@jeremy.com',
            password='python'
        )
        db.session.add(bad_user)
        db.session.commit()
        self.assertRaises(ValueError, self.login, 'Jeremy', 'python')
        try:
            response = self.login('Jeremy', 'python')
            self.assertEquals(response.status_code, 500)
        except ValueError:
            pass
    
    def test_index(self):
        """ Ensure Flask was setup correctly. """
        response = self.app.get("/", content_type='html/text')
        self.assetEqual(response.status_code, 200)

    if __name__ == "__main__":
        unittest.main()
