from ..utilities import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    date_registered = db.Column(db.DateTime(),default=datetime.utcnow)
    password_hash = db.Column(db.Text(), nullable=False)
    grades = db.Relationship('Grade', backref='student',lazy=True)
    courses = db.Relationship('Course', backref='student', lazy=True)
    def __repr__(self) -> str:
        return f"<Student{self.name}>"