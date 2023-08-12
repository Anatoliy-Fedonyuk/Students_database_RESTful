from flask_restful import Resource
from ..models import Students


class StudentsResource(Resource):
    def get(self):
        pass