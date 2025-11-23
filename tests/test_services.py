import pytest
from app.services import ProgressService
from app.models import ProgressSnapshot, ExerciseAttempt
from tests.factories import (
    UserFactory, CourseFactory, LessonFactory,
    ExerciseFactory, ExerciseAttemptFactory,
    ProgressSnapshotFactory
)


class TestProgressService:
    def test_get_current_lesson(self, app):
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
            
            progress = ProgressSnapshotFactory(
                user=user,
                course=course,
                current_lesson_id=lesson2.id
            )
            
            current = ProgressService.get_current_lesson(user.id, course.id)
            
            assert current is not None
            assert current.id == lesson2.id
    
    def test_save_progress_new(self, app):
        with app.app_context():
            user = UserFactory()
            course = CourseFactory()
            lesson = LessonFactory(course=course, is_published=True)
            
            progress = ProgressService.save_progress(
                user.id,
                course.id,
                lesson.id
            )
            
            assert progress is not None
            assert progress.user_id == user.id
            assert progress.course_id == course.id
            assert progress.current_lesson_id == lesson.id
    
    def test_save_progress_updates_completion(self, app):
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
            
            exercise1 = ExerciseFactory(lesson=lesson1, points=10)
            exercise2 = ExerciseFactory(lesson=lesson1, points=15)
            
            attempt1 = ExerciseAttemptFactory(
                user=user,
                exercise=exercise1,
                is_correct=True,
                points_earned=10
            )
            attempt2 = ExerciseAttemptFactory(
                user=user,
                exercise=exercise2,
                is_correct=True,
                points_earned=15
            )
            
            progress = ProgressService.save_progress(
                user.id,
                course.id,
                lesson1.id
            )
            
            assert progress.total_points == 25
            assert progress.exercises_completed == 2
    
    def test_save_progress_calculates_percentage(self, app):
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
            lesson3 = LessonFactory(
                course=course,
                order_index=3,
                is_published=True
            )
            
            exercise1 = ExerciseFactory(lesson=lesson1)
            exercise2 = ExerciseFactory(lesson=lesson2)
            
            ExerciseAttemptFactory(
                user=user,
                exercise=exercise1,
                is_correct=True
            )
            ExerciseAttemptFactory(
                user=user,
                exercise=exercise2,
                is_correct=True
            )
            
            progress = ProgressService.save_progress(user.id, course.id)
            
            assert progress.lessons_completed == 2
            assert progress.completion_percentage == pytest.approx(66.67, rel=0.1)
    
    def test_advance_to_next_lesson(self, app):
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
            lesson3 = LessonFactory(
                course=course,
                order_index=3,
                is_published=True
            )
            
            ProgressSnapshotFactory(
                user=user,
                course=course,
                current_lesson_id=lesson1.id
            )
            
            next_lesson = ProgressService.advance_to_next_lesson(
                user.id,
                course.id,
                lesson1.id
            )
            
            assert next_lesson is not None
            assert next_lesson.id == lesson2.id
            
            progress = ProgressSnapshot.query.filter_by(
                user_id=user.id,
                course_id=course.id
            ).first()
            
            assert progress.current_lesson_id == lesson2.id
    
    def test_advance_to_next_lesson_last_lesson(self, app):
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
            
            next_lesson = ProgressService.advance_to_next_lesson(
                user.id,
                course.id,
                lesson2.id
            )
            
            assert next_lesson is None
    
    def test_save_progress_invalid_course(self, app):
        with app.app_context():
            user = UserFactory()
            
            with pytest.raises(ValueError, match="Course with id 9999 not found"):
                ProgressService.save_progress(user.id, 9999)
