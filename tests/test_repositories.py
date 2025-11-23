import pytest
from app.repositories import UserRepository, ProgressRepository
from app.models import Lesson
from tests.factories import (
    UserFactory, CourseFactory, LessonFactory,
    ProgressSnapshotFactory
)


class TestUserRepository:
    def test_get_by_id(self, app):
        with app.app_context():
            user = UserFactory()
            
            found_user = UserRepository.get_by_id(user.id)
            
            assert found_user is not None
            assert found_user.id == user.id
    
    def test_get_by_email(self, app):
        with app.app_context():
            user = UserFactory(email='test@example.com')
            
            found_user = UserRepository.get_by_email('test@example.com')
            
            assert found_user is not None
            assert found_user.email == 'test@example.com'
    
    def test_get_by_username(self, app):
        with app.app_context():
            user = UserFactory(username='testuser')
            
            found_user = UserRepository.get_by_username('testuser')
            
            assert found_user is not None
            assert found_user.username == 'testuser'
    
    def test_get_active_users(self, app):
        with app.app_context():
            active_user = UserFactory(is_active=True)
            inactive_user = UserFactory(is_active=False)
            
            active_users = UserRepository.get_active_users()
            
            assert active_user in active_users
            assert inactive_user not in active_users
    
    def test_create_user(self, app):
        with app.app_context():
            from app.models import User
            user = User(
                email='new@example.com',
                username='newuser',
                password_hash='hashed'
            )
            
            created_user = UserRepository.create(user)
            
            assert created_user.id is not None
            assert created_user.email == 'new@example.com'
    
    def test_soft_delete_user(self, app):
        with app.app_context():
            user = UserFactory()
            
            UserRepository.delete(user)
            
            assert user.deleted_at is not None
            assert user.is_active is False


class TestProgressRepository:
    def test_get_user_progress(self, app):
        with app.app_context():
            user = UserFactory()
            course = CourseFactory()
            progress = ProgressSnapshotFactory(user=user, course=course)
            
            found_progress = ProgressRepository.get_user_progress(
                user.id,
                course.id
            )
            
            assert found_progress is not None
            assert found_progress.user_id == user.id
            assert found_progress.course_id == course.id
    
    def test_get_all_user_progress(self, app):
        with app.app_context():
            user = UserFactory()
            course1 = CourseFactory()
            course2 = CourseFactory()
            
            progress1 = ProgressSnapshotFactory(user=user, course=course1)
            progress2 = ProgressSnapshotFactory(user=user, course=course2)
            
            all_progress = ProgressRepository.get_all_user_progress(user.id)
            
            assert len(all_progress) == 2
            assert progress1 in all_progress
            assert progress2 in all_progress
    
    def test_create_or_update_new_progress(self, app):
        with app.app_context():
            from app.models import ProgressSnapshot
            user = UserFactory()
            course = CourseFactory()
            
            progress = ProgressSnapshot(
                user_id=user.id,
                course_id=course.id,
                lessons_completed=1,
                total_points=50
            )
            
            result = ProgressRepository.create_or_update(progress)
            
            assert result.id is not None
            assert result.lessons_completed == 1
            assert result.total_points == 50
    
    def test_create_or_update_existing_progress(self, app):
        with app.app_context():
            from app.models import ProgressSnapshot
            user = UserFactory()
            course = CourseFactory()
            
            existing = ProgressSnapshotFactory(
                user=user,
                course=course,
                lessons_completed=1,
                total_points=50
            )
            
            updated = ProgressSnapshot(
                user_id=user.id,
                course_id=course.id,
                lessons_completed=2,
                total_points=100
            )
            
            result = ProgressRepository.create_or_update(updated)
            
            assert result.id == existing.id
            assert result.lessons_completed == 2
            assert result.total_points == 100
    
    def test_get_current_lesson_with_progress(self, app):
        with app.app_context():
            user = UserFactory()
            course = CourseFactory()
            lesson1 = LessonFactory(course=course, order_index=1)
            lesson2 = LessonFactory(course=course, order_index=2)
            
            progress = ProgressSnapshotFactory(
                user=user,
                course=course,
                current_lesson_id=lesson2.id
            )
            
            current_lesson = ProgressRepository.get_current_lesson(
                user.id,
                course.id
            )
            
            assert current_lesson is not None
            assert current_lesson.id == lesson2.id
    
    def test_get_current_lesson_first_lesson(self, app):
        with app.app_context():
            user = UserFactory()
            course = CourseFactory()
            lesson1 = LessonFactory(
                course=course,
                order_index=1,
                is_published=True
            )
            lesson2 = LessonFactory(
                course=course,
                order_index=2,
                is_published=True
            )
            
            current_lesson = ProgressRepository.get_current_lesson(
                user.id,
                course.id
            )
            
            assert current_lesson is not None
            assert current_lesson.id == lesson1.id
