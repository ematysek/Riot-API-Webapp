import os
import unittest

from app import create_app, db
from app.default_conf import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    DEBUG = False
    FLASK_ENV = 'testing'


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.testapp = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_set_up(self):
        self.assertEqual(self.app.debug, False)


class RiotConnectorCase(BaseCase):
    def test_api_key_exists(self):
        self.assertTrue(os.environ.get('API_KEy') is not None)


class RouteCase(BaseCase):
    def test_main_page(self):
        response = self.testapp.get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_page_post(self):
        response = self.testapp.post('/')
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.testapp.get('/index')
        self.assertEqual(response.status_code, 200)

    def test_index_post(self):
        response = self.testapp.post('/index')
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main(verbosity=2)
