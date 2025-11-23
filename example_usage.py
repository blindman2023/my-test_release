"""
Example usage of the educational platform database models and services.
This script demonstrates how to interact with the database through
the repository and service layers.
"""
from app import create_app, db
from app.models import User, Course, Lesson, Exercise, ExerciseAttempt
from app.repositories import UserRepository, ProgressRepository
from app.services import ProgressService


def main():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Educational Platform - Example Usage")
        print("=" * 60)
        
        user = UserRepository.get_by_email('john.doe@example.com')
        if not user:
            print("Error: Sample data not found. Please run seed script first.")
            return
        
        print(f"\n👤 User: {user.full_name} ({user.email})")
        
        courses = Course.query.filter_by(is_published=True, deleted_at=None).all()
        print(f"\n📚 Available Courses: {len(courses)}")
        
        for course in courses:
            print(f"\n  • {course.title}")
            print(f"    Difficulty: {course.difficulty.value}")
            print(f"    Lessons: {course.lessons.filter_by(deleted_at=None).count()}")
            
            current_lesson = ProgressService.get_current_lesson(user.id, course.id)
            if current_lesson:
                print(f"    📖 Current Lesson: {current_lesson.title}")
            else:
                print("    📖 Not started yet")
        
        python_course = Course.query.filter_by(title="Introduction to Python Programming").first()
        
        if python_course:
            print(f"\n" + "=" * 60)
            print(f"Starting Course: {python_course.title}")
            print("=" * 60)
            
            first_lesson = python_course.lessons.filter_by(
                deleted_at=None,
                is_published=True
            ).order_by(Lesson.order_index).first()
            
            if first_lesson:
                print(f"\n📖 Lesson 1: {first_lesson.title}")
                print(f"   Duration: {first_lesson.duration_minutes} minutes")
                
                exercises = first_lesson.exercises.filter_by(deleted_at=None).all()
                print(f"\n   Exercises: {len(exercises)}")
                
                for idx, exercise in enumerate(exercises, 1):
                    print(f"\n   {idx}. {exercise.title}")
                    print(f"      Type: {exercise.exercise_type.value}")
                    print(f"      Points: {exercise.points}")
                    print(f"      Question: {exercise.question}")
                    
                    if exercise.exercise_type.value == 'multiple_choice' and exercise.options:
                        print(f"      Options:")
                        for option in exercise.options:
                            print(f"        - {option}")
                
                print(f"\n" + "-" * 60)
                print("Simulating Exercise Attempts...")
                print("-" * 60)
                
                first_exercise = exercises[0] if exercises else None
                if first_exercise:
                    attempt = ExerciseAttempt(
                        user_id=user.id,
                        exercise_id=first_exercise.id,
                        answer=first_exercise.correct_answer,
                        is_correct=True,
                        points_earned=first_exercise.points,
                        time_spent_seconds=45,
                        attempt_number=1,
                        feedback="Great job!"
                    )
                    db.session.add(attempt)
                    db.session.commit()
                    
                    print(f"\n✅ Exercise completed: {first_exercise.title}")
                    print(f"   Points earned: {first_exercise.points}")
                
                progress = ProgressService.save_progress(
                    user.id,
                    python_course.id,
                    first_lesson.id
                )
                
                print(f"\n📊 Progress Updated:")
                print(f"   Exercises completed: {progress.exercises_completed}")
                print(f"   Total points: {progress.total_points}")
                print(f"   Completion: {progress.completion_percentage:.1f}%")
                
                next_lesson = ProgressService.advance_to_next_lesson(
                    user.id,
                    python_course.id,
                    first_lesson.id
                )
                
                if next_lesson:
                    print(f"\n➡️  Advanced to next lesson: {next_lesson.title}")
                else:
                    print(f"\n🎉 Course completed!")
        
        print("\n" + "=" * 60)
        print("Example completed successfully!")
        print("=" * 60)


if __name__ == '__main__':
    main()
