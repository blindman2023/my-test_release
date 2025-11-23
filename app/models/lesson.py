from datetime import datetime
from app import db


class Lesson(db.Model):
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    duration_minutes = db.Column(db.Integer)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    course = db.relationship('Course', back_populates='lessons')
    exercises = db.relationship('Exercise', back_populates='lesson', lazy='dynamic', order_by='Exercise.order_index')
    progress_snapshots = db.relationship('ProgressSnapshot', back_populates='lesson', lazy='dynamic', foreign_keys='ProgressSnapshot.lesson_id')
    
    def __repr__(self):
        return f'<Lesson {self.title}>'
    
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
        self.is_published = False
