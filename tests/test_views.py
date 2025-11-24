import pytest
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

class TestLearningViews:
    """Test the learning blueprint HTML views"""
    
    def test_learning_index(self, client):
        """Test GET /learning/ endpoint"""
        response = client.get('/learning/')
        assert response.status_code == 200
        assert b'Available Courses' in response.data
        assert b'Test Lesson' in response.data
    
    def test_view_lesson(self, client):
        """Test GET /learning/lesson/<lesson_id> endpoint"""
        response = client.get('/learning/lesson/test-lesson')
        assert response.status_code == 200
        assert b'Test Lesson' in response.data
        assert b'Vocabulary' in response.data
        assert b'Grammar' in response.data
        assert b'Exercises' in response.data
    
    def test_view_lesson_not_found(self, client):
        """Test GET /learning/lesson/<lesson_id> with non-existent lesson"""
        response = client.get('/learning/lesson/non-existent')
        assert response.status_code == 404
        assert b'Lesson not found' in response.data
    
    def test_view_exercise(self, client):
        """Test GET /learning/exercise/<lesson_id>/<exercise_id> endpoint"""
        response = client.get('/learning/exercise/test-lesson/test-ex-1')
        assert response.status_code == 200
        assert b'Exercise' in response.data
        assert b'What does' in response.data  # Part of the question
        assert b'Submit Answer' in response.data
    
    def test_view_exercise_not_found_lesson(self, client):
        """Test GET /learning/exercise/<lesson_id>/<exercise_id> with non-existent lesson"""
        response = client.get('/learning/exercise/non-existent/test-ex-1')
        assert response.status_code == 404
        assert b'Lesson not found' in response.data
    
    def test_view_exercise_not_found_exercise(self, client):
        """Test GET /learning/exercise/<lesson_id>/<exercise_id> with non-existent exercise"""
        response = client.get('/learning/exercise/test-lesson/non-existent')
        assert response.status_code == 404
        assert b'Exercise not found' in response.data
    
    def test_view_progress(self, client):
        """Test GET /learning/progress endpoint"""
        response = client.get('/learning/progress')
        assert response.status_code == 200
        assert b'Your Learning Progress' in response.data
        assert b'Lessons Completed' in response.data
    
    def test_index_page(self, client):
        """Test GET / endpoint (main index page)"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to Chinese Learning' in response.data
        assert b'Start Learning' in response.data