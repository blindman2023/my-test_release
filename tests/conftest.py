import pytest
import json
import os
import sys

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_lesson_data():
    return {
        "id": "test-lesson",
        "title": "Test Lesson",
        "description": "A test lesson for testing",
        "level": "beginner",
        "category": "test",
        "vocabulary": [
            {
                "chinese": "测试",
                "pinyin": "cèshì",
                "english": "Test",
                "audio": "audio/test.mp3"
            }
        ],
        "grammar": [
            {
                "title": "Test Grammar",
                "explanation": "This is a test grammar point",
                "examples": [
                    {
                        "chinese": "这是测试",
                        "pinyin": "zhè shì cèshì",
                        "english": "This is a test"
                    }
                ]
            }
        ],
        "exercises": [
            {
                "id": "test-ex-1",
                "type": "multiple_choice",
                "question": "What does 测试 mean?",
                "options": ["Test", "Hello", "Goodbye", "Thank you"],
                "correct_answer": 0,
                "explanation": "测试 (cèshì) means test in Chinese."
            },
            {
                "id": "test-ex-2",
                "type": "translation",
                "question": "Translate 'Test' to Chinese",
                "correct_answer": "测试",
                "explanation": "Test in Chinese is 测试 (cèshì)."
            }
        ]
    }

@pytest.fixture
def setup_content_dir(tmp_path, sample_lesson_data):
    """Create a temporary content directory with test lesson data"""
    content_dir = tmp_path / "content"
    lessons_dir = content_dir / "lessons"
    lessons_dir.mkdir(parents=True)
    
    # Create test lesson file
    with open(lessons_dir / "test-lesson.json", "w", encoding="utf-8") as f:
        json.dump(sample_lesson_data, f, ensure_ascii=False, indent=2)
    
    # Create curriculum file
    curriculum_data = {
        "lessons": [
            {
                "id": "test-lesson",
                "title": "Test Lesson",
                "description": "A test lesson for testing",
                "level": "beginner",
                "category": "test",
                "estimated_duration": "10 minutes"
            }
        ]
    }
    
    with open(content_dir / "curriculum.json", "w", encoding="utf-8") as f:
        json.dump(curriculum_data, f, ensure_ascii=False, indent=2)
    
    return str(content_dir)