from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(255))
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    exercise_attempts = db.relationship('ExerciseAttempt', back_populates='user', lazy='dynamic')
    progress_snapshots = db.relationship('ProgressSnapshot', back_populates='user', lazy='dynamic')
    chat_messages = db.relationship('ChatMessage', back_populates='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
        self.is_active = False
