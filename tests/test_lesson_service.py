import pytest
import json
import os
import sys

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.lesson_service import LessonService

class TestLessonService:
    """Test the lesson service functionality"""
    
    def test_get_curriculum(self, setup_content_dir):
        """Test loading curriculum data"""
        service = LessonService(setup_content_dir)
        curriculum = service.get_curriculum()
        
        assert "lessons" in curriculum
        assert len(curriculum["lessons"]) == 1
        assert curriculum["lessons"][0]["id"] == "test-lesson"
    
    def test_get_lessons_list(self, setup_content_dir):
        """Test getting list of lessons"""
        service = LessonService(setup_content_dir)
        lessons = service.get_lessons_list()
        
        assert len(lessons) == 1
        assert lessons[0]["id"] == "test-lesson"
        assert lessons[0]["title"] == "Test Lesson"
    
    def test_get_lesson_by_id(self, setup_content_dir):
        """Test loading a specific lesson"""
        service = LessonService(setup_content_dir)
        lesson = service.get_lesson_by_id("test-lesson")
        
        assert lesson is not None
        assert lesson["id"] == "test-lesson"
        assert lesson["title"] == "Test Lesson"
        assert "vocabulary" in lesson
        assert "grammar" in lesson
        assert "exercises" in lesson
    
    def test_get_lesson_by_id_not_found(self, setup_content_dir):
        """Test loading a non-existent lesson"""
        service = LessonService(setup_content_dir)
        lesson = service.get_lesson_by_id("non-existent")
        
        assert lesson is None
    
    def test_get_exercise_by_id(self, setup_content_dir):
        """Test getting a specific exercise"""
        service = LessonService(setup_content_dir)
        exercise = service.get_exercise_by_id("test-lesson", "test-ex-1")
        
        assert exercise is not None
        assert exercise["id"] == "test-ex-1"
        assert exercise["type"] == "multiple_choice"
        assert exercise["question"] == "What does 测试 mean?"
    
    def test_get_exercise_by_id_not_found(self, setup_content_dir):
        """Test getting a non-existent exercise"""
        service = LessonService(setup_content_dir)
        exercise = service.get_exercise_by_id("test-lesson", "non-existent")
        
        assert exercise is None
    
    def test_validate_exercise_answer_multiple_choice_correct(self, setup_content_dir):
        """Test validating a correct multiple choice answer"""
        service = LessonService(setup_content_dir)
        result = service.validate_exercise_answer("test-lesson", "test-ex-1", "0")
        
        assert result["valid"] is True
        assert result["correct"] is True
        assert "explanation" in result
    
    def test_validate_exercise_answer_multiple_choice_incorrect(self, setup_content_dir):
        """Test validating an incorrect multiple choice answer"""
        service = LessonService(setup_content_dir)
        result = service.validate_exercise_answer("test-lesson", "test-ex-1", "1")
        
        assert result["valid"] is True
        assert result["correct"] is False
        assert "explanation" in result
    
    def test_validate_exercise_answer_translation_correct(self, setup_content_dir):
        """Test validating a correct translation answer"""
        service = LessonService(setup_content_dir)
        result = service.validate_exercise_answer("test-lesson", "test-ex-2", "测试")
        
        assert result["valid"] is True
        assert result["correct"] is True
        assert "explanation" in result
    
    def test_validate_exercise_answer_translation_case_insensitive(self, setup_content_dir):
        """Test case insensitive validation for translation"""
        service = LessonService(setup_content_dir)
        result = service.validate_exercise_answer("test-lesson", "test-ex-2", "测试")
        
        assert result["valid"] is True
        assert result["correct"] is True
    
    def test_validate_exercise_answer_not_found(self, setup_content_dir):
        """Test validating answer for non-existent exercise"""
        service = LessonService(setup_content_dir)
        result = service.validate_exercise_answer("test-lesson", "non-existent", "answer")
        
        assert result["valid"] is False
        assert "error" in result