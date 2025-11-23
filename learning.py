from flask import Blueprint, render_template, request, jsonify
from services.lesson_service import lesson_service

learning_bp = Blueprint('learning', __name__)

@learning_bp.route('/')
def index():
    """Learning module home page - list all courses"""
    try:
        lessons = lesson_service.get_lessons_list()
        return render_template('learning/index.html', lessons=lessons)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@learning_bp.route('/lesson/<lesson_id>')
def view_lesson(lesson_id):
    """View a specific lesson with its content"""
    try:
        lesson = lesson_service.get_lesson_by_id(lesson_id)
        if not lesson:
            return render_template('error.html', error="Lesson not found"), 404
        
        return render_template('learning/lesson.html', lesson=lesson)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@learning_bp.route('/exercise/<lesson_id>/<exercise_id>')
def view_exercise(lesson_id, exercise_id):
    """View and attempt a specific exercise"""
    try:
        lesson = lesson_service.get_lesson_by_id(lesson_id)
        if not lesson:
            return render_template('error.html', error="Lesson not found"), 404
        
        exercise = lesson_service.get_exercise_by_id(lesson_id, exercise_id)
        if not exercise:
            return render_template('error.html', error="Exercise not found"), 404
        
        return render_template('learning/exercise.html', 
                             lesson=lesson, 
                             exercise=exercise,
                             lesson_id=lesson_id,
                             exercise_id=exercise_id)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@learning_bp.route('/progress')
def view_progress():
    """View learning progress"""
    return render_template('learning/progress.html')