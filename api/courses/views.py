from flask import request
from flask_restx import Namespace,Resource,fields
from ..models.courses import Course
from ..models.students import Student
from ..utilities import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

course_namespace = Namespace('course', description='operation for course')

course_model = course_namespace.model(
    'Course', {
        'id' : fields.Integer(description='an Id'),
        'name' : fields.String(required=True),
        'teacher' :fields.String(required=True)
        # 'students': fields.String(),
        # 'grades': fields.Float(),
        # 'date_registered': fields.DateTime

    }
)


@course_namespace.route('/register')
class CourseReg(Resource):
    @course_namespace.expect(course_model)
    @jwt_required()
    @course_namespace.marshal_with(course_model)
    def post(self,):
        """Register for a course"""
        details = course_namespace.payload
        current_student = Student.query.filter_by(name=get_jwt_identity()).first()
        # current_grade = Grade.query.filter_by(name=get_jwt_identity()).first()
        
        course_registered = Course(
            name = details.get('name'),
            teacher = details.get('teacher')
            # date_registered = request.get_json('date_registered')
            # grades = 
            # students = 
        )
        course_registered.student = current_student
        db.session.add(course_registered)
        db.session.commit()
        return course_registered, HTTPStatus.CREATED

@course_namespace.route('/allcourses')
class SeeCourses(Resource):
    # @jwt_required()
    # @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    def get(self):
        """Retrieve all courses"""
        all_courses = Course.query.all()
        return all_courses

@course_namespace.route('/<int:course_id>')
class SeeCourseId(Resource):
    @course_namespace.marshal_with(course_model)
    def get(self,course_id):
        """Retrieving a course by id"""
        course = Course.query.get_or_404(course_id)
        return course, HTTPStatus.OK

@course_namespace.route('/student/<int:student_id>/courses')
class CoursesofStudent(Resource):
    @course_namespace.marshal_list_with(course_model)
    @jwt_required()
    def get(self,student_id):
        """get student and all the courses enrolled"""
        student = Student.query.get_or_404(student_id)
        courses = student.courses
        return courses, 200

"""retrieve grade for each student in each course"""

# @course_namespace.route('/grades')
# class StudentGPA(Resource):
#     def get(self,student_id):
#         grades = Course.query.get_or_404(student_id)
#         total_credit_hours = 7
#         total_quality_points = 20
#         for grades in Course.grades:
#             if Student.grades:
#                 total_credit_hours += 5
#                 total_quality_points += Grades.grades *3
#         gpa = round(total_quality_points / total_credit_hours)