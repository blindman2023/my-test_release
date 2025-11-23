from flask import Blueprint, jsonify, request
from services.lesson_service import lesson_service

api_bp = Blueprint('api', __name__)

@api_bp.route('/lessons', methods=['GET'])
def get_lessons():
    """Get list of all available lessons"""
    try:
        lessons = lesson_service.get_lessons_list()
        return jsonify({
            "success": True,
            "data": lessons
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/lessons/<lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    """Get detailed information about a specific lesson"""
    try:
        lesson = lesson_service.get_lesson_by_id(lesson_id)
        if not lesson:
            return jsonify({
                "success": False,
                "error": "Lesson not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": lesson
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/exercises/<exercise_id>/attempt', methods=['POST'])
def submit_exercise_attempt(exercise_id):
    """Submit an answer for an exercise and get feedback"""
    try:
        # Check if request has JSON data
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        lesson_id = data.get('lesson_id')
        user_answer = data.get('answer')
        
        if not lesson_id or user_answer is None:
            return jsonify({
                "success": False,
                "error": "lesson_id and answer are required"
            }), 400
        
        result = lesson_service.validate_exercise_answer(lesson_id, exercise_id, user_answer)
        
        if not result.get("valid"):
            return jsonify({
                "success": False,
                "error": result.get("error", "Invalid exercise")
            }), 400
        
        return jsonify({
            "success": True,
            "data": {
                "correct": result["correct"],
                "explanation": result["explanation"],
                "correct_answer": result["correct_answer"]
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500