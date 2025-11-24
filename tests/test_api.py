import pytest
import json
import os
import sys

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

@pytest.fixture
def app(setup_content_dir):
    """Create application for testing with custom content directory"""
    app = create_app()
    app.config['TESTING'] = True
    
    # Override the content directory in the lesson service
    with app.app_context():
        from services.lesson_service import lesson_service
        lesson_service.content_dir = setup_content_dir
        lesson_service.lessons_dir = os.path.join(setup_content_dir, "lessons")
        lesson_service.curriculum_file = os.path.join(setup_content_dir, "curriculum.json")
    
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

class TestAPIEndpoints:
    """Test the API endpoints"""
    
    def test_get_lessons_success(self, client):
        """Test GET /api/lessons endpoint"""
        response = client.get('/api/lessons')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) == 1
        assert data["data"][0]["id"] == "test-lesson"
    
    def test_get_lesson_success(self, client):
        """Test GET /api/lessons/<lesson_id> endpoint"""
        response = client.get('/api/lessons/test-lesson')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["id"] == "test-lesson"
        assert "vocabulary" in data["data"]
        assert "grammar" in data["data"]
        assert "exercises" in data["data"]
    
    def test_get_lesson_not_found(self, client):
        """Test GET /api/lessons/<lesson_id> with non-existent lesson"""
        response = client.get('/api/lessons/non-existent')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data["success"] is False
        assert "error" in data
    
    def test_submit_exercise_attempt_multiple_choice_correct(self, client):
        """Test POST /api/exercises/<exercise_id>/attempt with correct multiple choice"""
        response = client.post('/api/exercises/test-ex-1/attempt',
                             data=json.dumps({
                                 'lesson_id': 'test-lesson',
                                 'answer': '0'
                             }),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["data"]["correct"] is True
        assert "explanation" in data["data"]
    
    def test_submit_exercise_attempt_multiple_choice_incorrect(self, client):
        """Test POST /api/exercises/<exercise_id>/attempt with incorrect multiple choice"""
        response = client.post('/api/exercises/test-ex-1/attempt',
                             data=json.dumps({
                                 'lesson_id': 'test-lesson',
                                 'answer': '1'
                             }),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["data"]["correct"] is False
        assert "explanation" in data["data"]
        assert data["data"]["correct_answer"] == 0
    
    def test_submit_exercise_attempt_translation_correct(self, client):
        """Test POST /api/exercises/<exercise_id>/attempt with correct translation"""
        response = client.post('/api/exercises/test-ex-2/attempt',
                             data=json.dumps({
                                 'lesson_id': 'test-lesson',
                                 'answer': '测试'
                             }),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["data"]["correct"] is True
    
    def test_submit_exercise_attempt_missing_data(self, client):
        """Test POST /api/exercises/<exercise_id>/attempt with missing data"""
        response = client.post('/api/exercises/test-ex-1/attempt',
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data["success"] is False
        assert "error" in data
    
    def test_submit_exercise_attempt_no_json(self, client):
        """Test POST /api/exercises/<exercise_id>/attempt with no JSON data"""
        response = client.post('/api/exercises/test-ex-1/attempt')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data["success"] is False
        assert "error" in data
    
    def test_submit_exercise_attempt_non_existent(self, client):
        """Test POST /api/exercises/<exercise_id>/attempt with non-existent exercise"""
        response = client.post('/api/exercises/non-existent/attempt',
                             data=json.dumps({
                                 'lesson_id': 'test-lesson',
                                 'answer': 'answer'
                             }),
                             content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data["success"] is False
        assert "error" in data