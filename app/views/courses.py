from flask_restful import Resource
from ..models import Courses


class CoursesResource(Resource):
    def get(self):
        pass