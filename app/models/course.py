from datetime import datetime
from app import db
from app.models.enums import DifficultyLevel


class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.Enum(DifficultyLevel), default=DifficultyLevel.BEGINNER, nullable=False)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    lessons = db.relationship('Lesson', back_populates='course', lazy='dynamic', order_by='Lesson.order_index')
    progress_snapshots = db.relationship('ProgressSnapshot', back_populates='course', lazy='dynamic')
    
    def __repr__(self):
        return f'<Course {self.title}>'
    
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
        self.is_published = False
