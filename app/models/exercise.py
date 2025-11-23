from datetime import datetime
from app import db
from app.models.enums import ExerciseType, DifficultyLevel


class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    question = db.Column(db.Text, nullable=False)
    exercise_type = db.Column(db.Enum(ExerciseType), default=ExerciseType.MULTIPLE_CHOICE, nullable=False)
    difficulty = db.Column(db.Enum(DifficultyLevel), default=DifficultyLevel.BEGINNER, nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    points = db.Column(db.Integer, default=10)
    options = db.Column(db.JSON)
    correct_answer = db.Column(db.Text)
    hint = db.Column(db.Text)
    explanation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    lesson = db.relationship('Lesson', back_populates='exercises')
    attempts = db.relationship('ExerciseAttempt', back_populates='exercise', lazy='dynamic')
    
    def __repr__(self):
        return f'<Exercise {self.title}>'
    
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
