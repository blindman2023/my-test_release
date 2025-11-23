from datetime import datetime
from typing import Optional
from app import db
from app.models import ProgressSnapshot, Lesson, Course, ExerciseAttempt
from app.repositories import ProgressRepository


class ProgressService:
    @staticmethod
    def get_current_lesson(user_id: int, course_id: int) -> Optional[Lesson]:
        return ProgressRepository.get_current_lesson(user_id, course_id)
    
    @staticmethod
    def save_progress(user_id: int, course_id: int, lesson_id: Optional[int] = None) -> ProgressSnapshot:
        course = db.session.get(Course, course_id)
        if not course:
            raise ValueError(f"Course with id {course_id} not found")
        
        progress = ProgressRepository.get_user_progress(user_id, course_id)
        
        if not progress:
            progress = ProgressSnapshot(
                user_id=user_id,
                course_id=course_id,
                lesson_id=lesson_id,
                current_lesson_id=lesson_id
            )
        
        completed_attempts = ExerciseAttempt.query.filter_by(
            user_id=user_id,
            is_correct=True
        ).join(ExerciseAttempt.exercise).filter(
            db.text('exercises.lesson_id IN (SELECT id FROM lessons WHERE course_id = :course_id)')
        ).params(course_id=course_id).all()
        
        progress.exercises_completed = len(completed_attempts)
        progress.total_points = sum(attempt.points_earned for attempt in completed_attempts)
        
        completed_lesson_ids = set()
        for attempt in completed_attempts:
            if attempt.exercise and attempt.exercise.lesson_id:
                completed_lesson_ids.add(attempt.exercise.lesson_id)
        
        progress.lessons_completed = len(completed_lesson_ids)
        
        total_lessons = course.lessons.filter_by(deleted_at=None, is_published=True).count()
        if total_lessons > 0:
            progress.completion_percentage = (progress.lessons_completed / total_lessons) * 100
        else:
            progress.completion_percentage = 0.0
        
        progress.last_activity_at = datetime.utcnow()
        
        if lesson_id:
            progress.current_lesson_id = lesson_id
        
        return ProgressRepository.create_or_update(progress)
    
    @staticmethod
    def advance_to_next_lesson(user_id: int, course_id: int, current_lesson_id: int) -> Optional[Lesson]:
        current_lesson = db.session.get(Lesson, current_lesson_id)
        if not current_lesson or current_lesson.course_id != course_id:
            return None
        
        next_lesson = Lesson.query.filter(
            Lesson.course_id == course_id,
            Lesson.order_index > current_lesson.order_index,
            Lesson.deleted_at.is_(None),
            Lesson.is_published == True
        ).order_by(Lesson.order_index).first()
        
        if next_lesson:
            ProgressService.save_progress(user_id, course_id, next_lesson.id)
        
        return next_lesson
