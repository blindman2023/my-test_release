from datetime import datetime
from app import db


class ExerciseAttempt(db.Model):
    __tablename__ = 'exercise_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False, index=True)
    answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean)
    points_earned = db.Column(db.Integer, default=0)
    time_spent_seconds = db.Column(db.Integer)
    attempt_number = db.Column(db.Integer, default=1)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    user = db.relationship('User', back_populates='exercise_attempts')
    exercise = db.relationship('Exercise', back_populates='attempts')
    
    __table_args__ = (
        db.Index('idx_user_exercise', 'user_id', 'exercise_id'),
    )
    
    def __repr__(self):
        return f'<ExerciseAttempt user_id={self.user_id} exercise_id={self.exercise_id}>'
