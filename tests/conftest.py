# import pytest
# from app.init import create_app
#
#
# @pytest.fixture(scope='module')
# def app():
#     app = create_app('testing')
#     with app.app_context():
#         yield app
#
#
# @pytest.fixture(scope='module')
# def client(app):
#     with app.test_client() as client:
#         yield client
#
#
# @pytest.fixture(scope='module')
# def db(app):
#     with app.app_context():
#         db.create_all()
#         yield db
#         db.drop_all()
#
#
# if __name__ == '__main__':
#     pytest.main()
