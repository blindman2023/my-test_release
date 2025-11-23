from datetime import datetime
from app import db


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    context = db.Column(db.JSON)
    is_helpful = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    user = db.relationship('User', back_populates='chat_messages')
    
    def __repr__(self):
        return f'<ChatMessage user_id={self.user_id} at {self.created_at}>'
