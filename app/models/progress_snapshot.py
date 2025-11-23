from datetime import datetime
from app import db


class ProgressSnapshot(db.Model):
    __tablename__ = 'progress_snapshots'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True, index=True)
    current_lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)
    lessons_completed = db.Column(db.Integer, default=0)
    exercises_completed = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    completion_percentage = db.Column(db.Float, default=0.0)
    last_activity_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    user = db.relationship('User', back_populates='progress_snapshots')
    course = db.relationship('Course', back_populates='progress_snapshots')
    lesson = db.relationship('Lesson', back_populates='progress_snapshots', foreign_keys=[lesson_id])
    current_lesson = db.relationship('Lesson', foreign_keys=[current_lesson_id])
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', name='uq_user_course_progress'),
        db.Index('idx_user_course', 'user_id', 'course_id'),
    )
    
    def __repr__(self):
        return f'<ProgressSnapshot user_id={self.user_id} course_id={self.course_id}>'
