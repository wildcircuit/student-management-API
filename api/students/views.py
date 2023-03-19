from flask import request
from flask_restx import Namespace,Resource, fields
from ..models.students import Student
from ..models.courses import Course
from werkzeug.security import generate_password_hash, check_password_hash
from ..utilities import db
from http import HTTPStatus
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity

stud_namespace = Namespace('student', description='operation for student')

@stud_namespace.route('/')
class HelloStud(Resource):
    def get(self):
        return {'message':'hello stud'}

"""this model puts your input/object in a JSON format for your API"""
student_model = stud_namespace.model(
    'Student',{
    'name': fields.String(required=True, description='hhhhh'),
    'email': fields.String(required=True, description='ooooo'),
    'password': fields.String(required=True, description='ppppp')
    }
)

response_model = stud_namespace.model(
    'Response',{
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    'password_hash': fields.String(required=True),
    'date_registered': fields.DateTime()
    # 'grades':
    # 'courses': fields.String()
})

courses_model = stud_namespace.model(
    'StudentsOfCourse',{
        # 'id': fields.Integer(),
        # 'name': fields.String(required=True),
        # 'email': fields.String(required=True)
        'students': fields.Integer()
    }
)

login_model = stud_namespace.model(
    'Login',{
    'email': fields.String(required=True, description='ooooo'),
    'password': fields.String(required=True, description='ppppp')
    }
)

@stud_namespace.route('/signup')
class CreateStudent(Resource):
    @stud_namespace.expect(student_model)
    @stud_namespace.marshal_with(response_model)
    def post(self):
        data = request.get_json()
        new_student = Student(
            name = data.get('name'),
            email = data.get('email'),
            password_hash =  generate_password_hash(data.get('password'))
        )
        db.session.add(new_student)
        db.session.commit()
        # return {'message':'you have been signed in'}
        return new_student, HTTPStatus.CREATED

@stud_namespace.route('/login')
class Login(Resource):
    @stud_namespace.expect(student_model)
    def post(self):
        details = request.get_json()
        email = details.get('email')
        password = details.get('password')
        student = Student.query.filter_by(email=email).first()
        if (student is not None) and check_password_hash(student.password_hash, password):
            access_token = create_access_token(identity=student.name)
            refresh_token = create_refresh_token(identity=student.name)
            return {'access_token': access_token, 'refresh_token':refresh_token}, HTTPStatus.CREATED


@stud_namespace.route('/allstudents')
class AllStudents(Resource):
    # @stud_namespace.expect(student_model)
    @stud_namespace.marshal_with(student_model)
    def get(self):
        """Retrieve all students"""
        registered_students= Student.query.all()
        return registered_students

@stud_namespace.route('/student/<int:student_id>')
class StudentById(Resource):
    # @stud_namespace.expect(student_model)
    @stud_namespace.marshal_with(student_model)
    def get(self,student_id):
        """"get student by ID"""
        student = Student.query.get_or_404(student_id)
        return student, HTTPStatus.OK

@stud_namespace.route('/student/<int:student_id>')
class UpdateAndDeleteStudent(Resource):
    @stud_namespace.expect(student_model)
    @stud_namespace.marshal_with(student_model)
    @jwt_required()
    def put(self,student_id):
        """update a student by id"""
        student = Student.query.get_or_404(student_id)
        data = stud_namespace.payload
        student.name = data['name']
        # student.name = data.quantity
        student.email = data['email']
        # student.email = data.email
        db.session.commit()
        return student, HTTPStatus.OK

    @jwt_required()
    def delete(self,student_id):
        """delete a student by ID"""
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return {'message':'student with ID {{students.id}} is deleted'}

@stud_namespace.route('/course/<int:course_id>/students/<int:student_id>')
class StudentsofCourse(Resource):
    @stud_namespace.marshal_list_with(courses_model)
    # @jwt_required()
    def get(self,course_id,student_id):
        """ all the students registered in a particular course"""
        student =Student.query.get_or_404(student_id)
        students_of_course = Course.query.filter_by(id=course_id).filter_by(students=student)
        return students_of_course, 200



@stud_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        student_name = get_jwt_identity
        access_token = create_access_token(identity=student_name)
        return {'student name':student_name, 'access token': access_token}