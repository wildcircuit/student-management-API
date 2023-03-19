import unittest
from .. import create_app
from ..config.config import config_dict
from ..utilities import db
from werkzeug.security import generate_password_hash
# from ..models.students import Student

class StudentTestCase(unittest.TestCase):
    def SetUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app=None
        self.client=None

    def test_student_signup(self):
        data = {
            'name': 'baller',
            'email': 'bigtime@flex',
            'password': 'thankyou'
        }
        response = self.client.post('/student/signup', json=data)

        assert response.status_code==201