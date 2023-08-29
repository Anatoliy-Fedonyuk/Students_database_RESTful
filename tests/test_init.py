import unittest
from app.init import create_app


class TestInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            from app.models import db
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            from app.models import db
            db.drop_all()

    def test_index_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_students_list_resource(self):
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
