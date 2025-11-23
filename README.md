# Educational Platform Database Models

A comprehensive Flask/SQLAlchemy application with database models for an educational learning platform.

## Features

- **SQLAlchemy Models**: User, Course, Lesson, Exercise, ExerciseAttempt, ProgressSnapshot, ChatMessage
- **Enumerations**: Difficulty levels, exercise types, and exercise status
- **Relationships**: Properly configured with foreign keys and cascade rules
- **Timestamps**: Created/updated timestamps on all models
- **Soft Deletes**: Implemented on User, Course, and Lesson models
- **Migrations**: Alembic/Flask-Migrate integration for database schema management
- **Seed Data**: Sample beginner course data with lessons and exercises
- **Repository Pattern**: Clean data access layer
- **Service Layer**: Business logic for progress tracking
- **Comprehensive Tests**: 41 unit tests covering models, repositories, and services

## Project Structure

```
.
├── app/
│   ├── __init__.py              # Flask app factory and db initialization
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── enums.py             # Enum definitions
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── lesson.py
│   │   ├── exercise.py
│   │   ├── exercise_attempt.py
│   │   ├── progress_snapshot.py
│   │   └── chat_message.py
│   ├── repositories/            # Data access layer
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── progress_repository.py
│   └── services/                # Business logic layer
│       ├── __init__.py
│       └── progress_service.py
├── migrations/                  # Alembic migrations
├── seeds/
│   └── seed_data.py             # Database seeding script
├── tests/                       # Unit tests
│   ├── conftest.py              # Pytest fixtures
│   ├── factories.py             # Factory Boy factories
│   ├── test_models.py
│   ├── test_repositories.py
│   └── test_services.py
├── config.py                    # Application configuration
├── manage.py                    # Flask CLI management
├── requirements.txt             # Python dependencies
└── pytest.ini                   # Pytest configuration
```

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
flask --app manage db upgrade
```

4. Seed the database with sample data:
```bash
PYTHONPATH=. python seeds/seed_data.py
```

## Database Models

### User
- Email (unique, required)
- Username (unique, required)
- Full name
- Password hash
- Active status
- Soft delete support

### Course
- Title
- Description
- Difficulty level (beginner, intermediate, advanced)
- Published status
- Soft delete support

### Lesson
- Course relationship
- Title, description, content
- Order index for sequencing
- Duration in minutes
- Soft delete support

### Exercise
- Lesson relationship
- Title, question, description
- Exercise type (multiple choice, code completion, free form, true/false)
- Difficulty level
- Points
- Options (JSON)
- Correct answer
- Hint and explanation

### ExerciseAttempt
- User and Exercise relationships
- Answer submitted
- Correctness flag
- Points earned
- Time spent
- Attempt number
- Feedback

### ProgressSnapshot
- User and Course relationships
- Current lesson tracking
- Lessons completed count
- Exercises completed count
- Total points
- Completion percentage
- Last activity timestamp
- Unique constraint on user + course

### ChatMessage
- User relationship
- Message and response
- Context (JSON)
- Helpful rating

## Running Tests

Run all tests:
```bash
PYTHONPATH=. pytest tests/ -v
```

Run specific test file:
```bash
PYTHONPATH=. pytest tests/test_models.py -v
```

Run with coverage:
```bash
PYTHONPATH=. pytest tests/ --cov=app --cov-report=html
```

## Database Migrations

Create a new migration:
```bash
flask --app manage db migrate -m "Description of changes"
```

Apply migrations:
```bash
flask --app manage db upgrade
```

Rollback migration:
```bash
flask --app manage db downgrade
```

## Service Layer

### ProgressService

The `ProgressService` provides business logic for tracking user progress:

- `get_current_lesson(user_id, course_id)`: Get the current lesson for a user in a course
- `save_progress(user_id, course_id, lesson_id)`: Save or update progress, calculating completion stats
- `advance_to_next_lesson(user_id, course_id, current_lesson_id)`: Move user to next lesson in sequence

## Repository Layer

### UserRepository
- CRUD operations for users
- Email and username lookups
- Soft delete support

### ProgressRepository
- Get user progress for courses
- Create or update progress snapshots
- Get current lesson based on progress

## Constraints and Validation

- **Unique Constraints**: Email, username, user+course progress
- **Foreign Keys**: Proper relationships with cascade rules
- **NOT NULL**: Required fields enforced at database level
- **Indexes**: Optimized queries on foreign keys and lookup fields
- **JSON Fields**: Support for flexible data like exercise options and chat context

## Sample Data

The seed script creates:
- 2 sample users (John Doe, Jane Smith)
- 2 courses (Python for beginners, JavaScript fundamentals)
- 4 lessons across courses
- 7 exercises with various types (multiple choice, code completion, true/false)

## Configuration

Set environment variables in `.env` file:
```
DATABASE_URL=sqlite:///app.db
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

## License

MIT
