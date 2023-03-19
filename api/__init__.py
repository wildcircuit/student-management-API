from flask import Flask
from flask_restx import Api
from .courses.views import course_namespace
from .students.views import stud_namespace
from .config.config import config_dict
from .utilities import db
from .models.courses import Course
from .models.grades import Grade
from .models.students import Student
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound,MethodNotAllowed

def create_app(config=config_dict['dev']):
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app,db)

    api=Api(app, titile='Student Management API',
    description='A basic Student Mnagement Rest API',
    version='1.0')
    api.add_namespace(course_namespace)
    api.add_namespace(stud_namespace)

    @api.errorhandler(NotFound)
    def not_found(error):
        return {'error': 'Not Found'},404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {'error': 'Method Not Allowed'},404

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db' : db,
            'Student' : Student,
            'Course' : Course,
            'Grade': Grade
        }
    return app