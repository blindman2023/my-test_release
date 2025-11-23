from typing import Optional, List
from app import db
from app.models import ProgressSnapshot, Lesson, Course


class ProgressRepository:
    @staticmethod
    def get_user_progress(user_id: int, course_id: int) -> Optional[ProgressSnapshot]:
        return ProgressSnapshot.query.filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()
    
    @staticmethod
    def get_all_user_progress(user_id: int) -> List[ProgressSnapshot]:
        return ProgressSnapshot.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def create_or_update(progress: ProgressSnapshot) -> ProgressSnapshot:
        from datetime import datetime
        
        existing = ProgressRepository.get_user_progress(
            progress.user_id,
            progress.course_id
        )
        
        if existing:
            existing.current_lesson_id = progress.current_lesson_id
            existing.lessons_completed = progress.lessons_completed
            existing.exercises_completed = progress.exercises_completed
            existing.total_points = progress.total_points
            existing.completion_percentage = progress.completion_percentage
            if progress.last_activity_at:
                existing.last_activity_at = progress.last_activity_at
            else:
                existing.last_activity_at = datetime.utcnow()
            db.session.commit()
            return existing
        else:
            db.session.add(progress)
            db.session.commit()
            return progress
    
    @staticmethod
    def get_current_lesson(user_id: int, course_id: int) -> Optional[Lesson]:
        progress = ProgressRepository.get_user_progress(user_id, course_id)
        if progress and progress.current_lesson_id:
            return db.session.get(Lesson, progress.current_lesson_id)
        
        course = db.session.get(Course, course_id)
        if course:
            return course.lessons.filter_by(deleted_at=None, is_published=True).order_by(Lesson.order_index).first()
        
        return None
