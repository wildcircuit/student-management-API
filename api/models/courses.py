from ..utilities import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    teacher = db.Column(db.String(),nullable=False)
    date_registered = db.Column(db.DateTime(), default=datetime.utcnow)
    students =db.Column(db.Integer(), db.ForeignKey('students.id'))
    grades =db.Column(db.Float(), db.ForeignKey('grades.id'),default=None) 
    def __repr__(self) -> str:
        return f"<Course{self.id}>"



