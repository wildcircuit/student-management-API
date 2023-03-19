from ..utilities import db

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Float)
    course_id = db.Column(db.Integer,db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer,db.ForeignKey('students.id'),nullable=False)
    def __repr__(self) -> str:
        return f"<Grade{self.id}>"