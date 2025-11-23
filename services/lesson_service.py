import os
import json
from typing import Dict, List, Optional, Any

class LessonService:
    def __init__(self, content_dir: str = "content"):
        self.content_dir = content_dir
        self.lessons_dir = os.path.join(content_dir, "lessons")
        self.curriculum_file = os.path.join(content_dir, "curriculum.json")
    
    def get_curriculum(self) -> Dict[str, Any]:
        """Load the curriculum metadata"""
        try:
            with open(self.curriculum_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"lessons": []}
    
    def get_lessons_list(self) -> List[Dict[str, Any]]:
        """Get list of all available lessons"""
        curriculum = self.get_curriculum()
        return curriculum.get("lessons", [])
    
    def get_lesson_by_id(self, lesson_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific lesson by ID"""
        lesson_file = os.path.join(self.lessons_dir, f"{lesson_id}.json")
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def get_exercise_by_id(self, lesson_id: str, exercise_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific exercise from a lesson"""
        lesson = self.get_lesson_by_id(lesson_id)
        if not lesson:
            return None
        
        for exercise in lesson.get("exercises", []):
            if exercise.get("id") == exercise_id:
                return exercise
        return None
    
    def validate_exercise_answer(self, lesson_id: str, exercise_id: str, user_answer: str) -> Dict[str, Any]:
        """Validate user's answer to an exercise"""
        exercise = self.get_exercise_by_id(lesson_id, exercise_id)
        if not exercise:
            return {
                "valid": False,
                "error": "Exercise not found"
            }
        
        exercise_type = exercise.get("type")
        correct_answer = exercise.get("correct_answer")
        
        if exercise_type == "multiple_choice":
            try:
                user_answer_int = int(user_answer)
                is_correct = user_answer_int == correct_answer
            except (ValueError, TypeError):
                is_correct = False
        else:
            # For translation, fill_blank, etc.
            is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
        
        return {
            "valid": True,
            "correct": is_correct,
            "explanation": exercise.get("explanation", ""),
            "correct_answer": correct_answer
        }

# Global instance
lesson_service = LessonService()