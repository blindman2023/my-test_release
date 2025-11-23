import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import (
    User, Course, Lesson, Exercise, ExerciseAttempt,
    ProgressSnapshot, ChatMessage,
    DifficultyLevel, ExerciseType
)
from tests.factories import (
    UserFactory, CourseFactory, LessonFactory,
    ExerciseFactory, ExerciseAttemptFactory,
    ProgressSnapshotFactory, ChatMessageFactory
)


class TestUserModel:
    def test_create_user(self, app):
        with app.app_context():
            user = UserFactory(
                email='test@example.com',
                username='testuser'
            )
            
            assert user.id is not None
            assert user.email == 'test@example.com'
            assert user.username == 'testuser'
            assert user.is_active is True
            assert user.deleted_at is None
    
    def test_unique_email_constraint(self, app):
        with app.app_context():
            UserFactory(email='duplicate@example.com')
            
            with pytest.raises(IntegrityError):
                UserFactory(email='duplicate@example.com')
                db.session.flush()
    
    def test_unique_username_constraint(self, app):
        with app.app_context():
            UserFactory(username='duplicate')
            
            with pytest.raises(IntegrityError):
                UserFactory(username='duplicate')
                db.session.flush()
    
    def test_soft_delete_user(self, app):
        with app.app_context():
            user = UserFactory()
            assert user.deleted_at is None
            assert user.is_active is True
            
            user.soft_delete()
            db.session.commit()
            
            assert user.deleted_at is not None
            assert user.is_active is False
    
    def test_user_relationships(self, app):
        with app.app_context():
            user = UserFactory()
            exercise = ExerciseFactory()
            
            attempt = ExerciseAttemptFactory(user=user, exercise=exercise)
            
            assert attempt in user.exercise_attempts
            assert user.exercise_attempts.count() == 1


class TestCourseModel:
    def test_create_course(self, app):
        with app.app_context():
            course = CourseFactory(
                title='Python 101',
                difficulty=DifficultyLevel.BEGINNER
            )
            
            assert course.id is not None
            assert course.title == 'Python 101'
            assert course.difficulty == DifficultyLevel.BEGINNER
            assert course.is_published is True
    
    def test_course_with_lessons(self, app):
        with app.app_context():
            course = CourseFactory()
            lesson1 = LessonFactory(course=course, order_index=1)
            lesson2 = LessonFactory(course=course, order_index=2)
            
            lessons = course.lessons.all()
            assert len(lessons) == 2
            assert lessons[0].order_index < lessons[1].order_index
    
    def test_soft_delete_course(self, app):
        with app.app_context():
            course = CourseFactory(is_published=True)
            
            course.soft_delete()
            db.session.commit()
            
            assert course.deleted_at is not None
            assert course.is_published is False


class TestLessonModel:
    def test_create_lesson(self, app):
        with app.app_context():
            course = CourseFactory()
            lesson = LessonFactory(
                course=course,
                title='Introduction',
                order_index=1
            )
            
            assert lesson.id is not None
            assert lesson.course_id == course.id
            assert lesson.title == 'Introduction'
            assert lesson.order_index == 1
    
    def test_lesson_foreign_key(self, app):
        with app.app_context():
            course = CourseFactory()
            lesson = LessonFactory(course=course)
            
            assert lesson.course == course
            assert lesson in course.lessons.all()
    
    def test_lesson_with_exercises(self, app):
        with app.app_context():
            lesson = LessonFactory()
            exercise1 = ExerciseFactory(lesson=lesson, order_index=1)
            exercise2 = ExerciseFactory(lesson=lesson, order_index=2)
            
            exercises = lesson.exercises.all()
            assert len(exercises) == 2


class TestExerciseModel:
    def test_create_exercise(self, app):
        with app.app_context():
            lesson = LessonFactory()
            exercise = ExerciseFactory(
                lesson=lesson,
                title='Quiz 1',
                exercise_type=ExerciseType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.BEGINNER
            )
            
            assert exercise.id is not None
            assert exercise.lesson_id == lesson.id
            assert exercise.exercise_type == ExerciseType.MULTIPLE_CHOICE
            assert exercise.difficulty == DifficultyLevel.BEGINNER
    
    def test_exercise_types(self, app):
        with app.app_context():
            lesson = LessonFactory()
            
            mc_exercise = ExerciseFactory(
                lesson=lesson,
                exercise_type=ExerciseType.MULTIPLE_CHOICE
            )
            code_exercise = ExerciseFactory(
                lesson=lesson,
                exercise_type=ExerciseType.CODE_COMPLETION
            )
            
            assert mc_exercise.exercise_type == ExerciseType.MULTIPLE_CHOICE
            assert code_exercise.exercise_type == ExerciseType.CODE_COMPLETION
    
    def test_exercise_json_options(self, app):
        with app.app_context():
            exercise = ExerciseFactory(
                options=['A', 'B', 'C', 'D']
            )
            
            assert isinstance(exercise.options, list)
            assert len(exercise.options) == 4


class TestExerciseAttemptModel:
    def test_create_attempt(self, app):
        with app.app_context():
            user = UserFactory()
            exercise = ExerciseFactory()
            
            attempt = ExerciseAttemptFactory(
                user=user,
                exercise=exercise,
                answer='Option A',
                is_correct=True,
                points_earned=10
            )
            
            assert attempt.id is not None
            assert attempt.user_id == user.id
            assert attempt.exercise_id == exercise.id
            assert attempt.is_correct is True
    
    def test_attempt_foreign_keys(self, app):
        with app.app_context():
            user = UserFactory()
            exercise = ExerciseFactory()
            attempt = ExerciseAttemptFactory(user=user, exercise=exercise)
            
            assert attempt.user == user
            assert attempt.exercise == exercise
    
    def test_multiple_attempts(self, app):
        with app.app_context():
            user = UserFactory()
            exercise = ExerciseFactory()
            
            attempt1 = ExerciseAttemptFactory(
                user=user,
                exercise=exercise,
                attempt_number=1,
                is_correct=False
            )
            attempt2 = ExerciseAttemptFactory(
                user=user,
                exercise=exercise,
                attempt_number=2,
                is_correct=True
            )
            
            attempts = ExerciseAttempt.query.filter_by(
                user_id=user.id,
                exercise_id=exercise.id
            ).all()
            
            assert len(attempts) == 2


class TestProgressSnapshotModel:
    def test_create_progress(self, app):
        with app.app_context():
            user = UserFactory()
            course = CourseFactory()
            lesson = LessonFactory(course=course)
            
            progress = ProgressSnapshotFactory(
                user=user,
                course=course,
                lesson=lesson,
                lessons_completed=1,
                total_points=50
            )
            
            assert progress.id is not None
            assert progress.user_id == user.id
            assert progress.course_id == course.id
            assert progress.lessons_completed == 1
    
    def test_unique_user_course_constraint(self, app):
        with app.app_context():
            user = UserFactory()
            course = CourseFactory()
            
            ProgressSnapshotFactory(user=user, course=course)
            
            with pytest.raises(IntegrityError):
                ProgressSnapshotFactory(user=user, course=course)
                db.session.flush()
    
    def test_progress_relationships(self, app):
        with app.app_context():
            user = UserFactory()
            course = CourseFactory()
            lesson = LessonFactory(course=course)
            
            progress = ProgressSnapshotFactory(
                user=user,
                course=course,
                lesson=lesson
            )
            
            assert progress.user == user
            assert progress.course == course
            assert progress.lesson == lesson


class TestChatMessageModel:
    def test_create_chat_message(self, app):
        with app.app_context():
            user = UserFactory()
            
            message = ChatMessageFactory(
                user=user,
                message='How do I use loops?',
                response='Loops allow you to repeat code...'
            )
            
            assert message.id is not None
            assert message.user_id == user.id
            assert 'loops' in message.message.lower()
    
    def test_chat_message_context(self, app):
        with app.app_context():
            message = ChatMessageFactory(
                context={'topic': 'loops', 'language': 'python'}
            )
            
            assert isinstance(message.context, dict)
            assert message.context['topic'] == 'loops'
