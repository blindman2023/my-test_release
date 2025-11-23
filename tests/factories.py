import factory
from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory
from app import db
from app.models import (
    User, Course, Lesson, Exercise, ExerciseAttempt,
    ProgressSnapshot, ChatMessage,
    DifficultyLevel, ExerciseType
)


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'


class UserFactory(BaseFactory):
    class Meta:
        model = User
    
    email = Faker('email')
    username = Faker('user_name')
    full_name = Faker('name')
    password_hash = 'hashed_password'
    is_active = True


class CourseFactory(BaseFactory):
    class Meta:
        model = Course
    
    title = Faker('sentence', nb_words=4)
    description = Faker('paragraph')
    difficulty = DifficultyLevel.BEGINNER
    is_published = True
    order_index = factory.Sequence(lambda n: n)


class LessonFactory(BaseFactory):
    class Meta:
        model = Lesson
    
    course = factory.SubFactory(CourseFactory)
    title = Faker('sentence', nb_words=5)
    description = Faker('paragraph')
    content = Faker('text')
    order_index = factory.Sequence(lambda n: n)
    duration_minutes = 30
    is_published = True


class ExerciseFactory(BaseFactory):
    class Meta:
        model = Exercise
    
    lesson = factory.SubFactory(LessonFactory)
    title = Faker('sentence', nb_words=4)
    description = Faker('paragraph')
    question = Faker('sentence', nb_words=10)
    exercise_type = ExerciseType.MULTIPLE_CHOICE
    difficulty = DifficultyLevel.BEGINNER
    order_index = factory.Sequence(lambda n: n)
    points = 10
    options = ['Option A', 'Option B', 'Option C', 'Option D']
    correct_answer = 'Option A'


class ExerciseAttemptFactory(BaseFactory):
    class Meta:
        model = ExerciseAttempt
    
    user = factory.SubFactory(UserFactory)
    exercise = factory.SubFactory(ExerciseFactory)
    answer = 'Option A'
    is_correct = True
    points_earned = 10
    time_spent_seconds = 60
    attempt_number = 1


class ProgressSnapshotFactory(BaseFactory):
    class Meta:
        model = ProgressSnapshot
    
    user = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    lesson = factory.SubFactory(LessonFactory)
    lessons_completed = 0
    exercises_completed = 0
    total_points = 0
    completion_percentage = 0.0


class ChatMessageFactory(BaseFactory):
    class Meta:
        model = ChatMessage
    
    user = factory.SubFactory(UserFactory)
    message = Faker('sentence', nb_words=10)
    response = Faker('paragraph')
    context = {'topic': 'python'}
