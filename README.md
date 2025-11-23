# Chinese Learning Platform

A Flask-based web application for learning Chinese language with interactive lessons, vocabulary, grammar explanations, and exercises.

## Features

- **Interactive Lessons**: Structured lessons with vocabulary, grammar explanations, and Chinese translations
- **Exercise System**: Multiple choice, translation, and fill-in-the-blank exercises with immediate feedback
- **REST API**: JSON API endpoints for integration with frontend applications
- **Progress Tracking**: Monitor learning progress and completion status
- **Responsive Design**: Bootstrap-based UI that works on desktop and mobile devices

## Project Structure

```
├── app.py                 # Flask application factory
├── run.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── content/               # Lesson content directory
│   ├── curriculum.json    # Course metadata
│   └── lessons/           # Individual lesson files
├── services/              # Business logic layer
│   └── lesson_service.py  # Lesson content management
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── learning/         # Learning module templates
│   └── error.html        # Error page
├── api.py                # API blueprint
├── learning.py           # Learning blueprint
└── tests/                # Test suite
    ├── conftest.py       # Test fixtures
    ├── test_lesson_service.py
    ├── test_api.py
    └── test_views.py
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Development mode:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

### Lessons
- `GET /api/lessons` - List all available lessons
- `GET /api/lessons/<lesson_id>` - Get detailed lesson information

### Exercises
- `POST /api/exercises/<exercise_id>/attempt` - Submit exercise answer

Request body:
```json
{
    "lesson_id": "lesson-1",
    "answer": "user_answer_here"
}
```

Response:
```json
{
    "success": true,
    "data": {
        "correct": true,
        "explanation": "Explanation of the answer",
        "correct_answer": "The correct answer"
    }
}
```

## Web Views

### Learning Module
- `/learning/` - List of available courses
- `/learning/lesson/<lesson_id>` - View lesson content
- `/learning/exercise/<lesson_id>/<exercise_id>` - Attempt exercises
- `/learning/progress` - View learning progress

## Content Structure

Lessons are stored as JSON files in the `content/lessons/` directory:

```json
{
    "id": "lesson-1",
    "title": "Lesson Title",
    "description": "Lesson description",
    "level": "beginner",
    "category": "conversation",
    "vocabulary": [
        {
            "chinese": "你好",
            "pinyin": "nǐ hǎo",
            "english": "Hello",
            "audio": "audio/ni-hao.mp3"
        }
    ],
    "grammar": [
        {
            "title": "Grammar Point",
            "explanation": "Explanation",
            "examples": [
                {
                    "chinese": "Example",
                    "pinyin": "pīnyīn",
                    "english": "Translation"
                }
            ]
        }
    ],
    "exercises": [
        {
            "id": "ex-1-1",
            "type": "multiple_choice",
            "question": "Question text",
            "options": ["Option 1", "Option 2"],
            "correct_answer": 0,
            "explanation": "Explanation"
        }
    ]
}
```

## Running Tests

```bash
pytest
```

The test suite includes:
- Unit tests for the lesson service
- API endpoint integration tests
- Web view tests

## Technologies Used

- **Backend**: Flask 3.0.0
- **Frontend**: Bootstrap 5.3.0, jQuery 3.6.0
- **Testing**: pytest 7.4.3, pytest-flask 1.3.0
- **CORS**: Flask-CORS 4.0.0

## Contributing

1. Add new lessons by creating JSON files in `content/lessons/`
2. Update `content/curriculum.json` with new lesson metadata
3. Write tests for new features
4. Follow existing code style and patterns

## License

This project is open source and available under the MIT License.