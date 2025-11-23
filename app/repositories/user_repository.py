from typing import Optional
from app import db
from app.models import User


class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return db.session.get(User, user_id)
    
    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email, deleted_at=None).first()
    
    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        return User.query.filter_by(username=username, deleted_at=None).first()
    
    @staticmethod
    def get_active_users():
        return User.query.filter_by(is_active=True, deleted_at=None).all()
    
    @staticmethod
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update(user: User) -> User:
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user: User) -> None:
        user.soft_delete()
        db.session.commit()
