import unittest
from app.init import create_app

app, db = create_app('testing')


class TestInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def test_index_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_students_list_resource(self):
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
