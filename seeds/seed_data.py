from datetime import datetime
from app import create_app, db
from app.models import (
    User, Course, Lesson, Exercise,
    DifficultyLevel, ExerciseType
)


def seed_database():
    app = create_app()
    
    with app.app_context():
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        print("Creating sample users...")
        user1 = User(
            email="john.doe@example.com",
            username="johndoe",
            full_name="John Doe",
            password_hash="hashed_password_123",
            is_active=True
        )
        
        user2 = User(
            email="jane.smith@example.com",
            username="janesmith",
            full_name="Jane Smith",
            password_hash="hashed_password_456",
            is_active=True
        )
        
        db.session.add_all([user1, user2])
        db.session.commit()
        
        print("Creating beginner Python course...")
        python_course = Course(
            title="Introduction to Python Programming",
            description="Learn the fundamentals of Python programming from scratch. Perfect for complete beginners!",
            difficulty=DifficultyLevel.BEGINNER,
            is_published=True,
            order_index=1
        )
        
        db.session.add(python_course)
        db.session.commit()
        
        print("Creating lessons...")
        lesson1 = Lesson(
            course_id=python_course.id,
            title="Python Basics and Setup",
            description="Introduction to Python, installation, and your first program",
            content="Python is a versatile, beginner-friendly programming language. In this lesson, you'll learn how to set up Python and write your first program.",
            order_index=1,
            duration_minutes=30,
            is_published=True
        )
        
        lesson2 = Lesson(
            course_id=python_course.id,
            title="Variables and Data Types",
            description="Understanding variables, strings, numbers, and basic data types",
            content="Variables are containers for storing data. Python has several built-in data types including strings, integers, floats, and booleans.",
            order_index=2,
            duration_minutes=45,
            is_published=True
        )
        
        lesson3 = Lesson(
            course_id=python_course.id,
            title="Control Flow and Conditionals",
            description="Learn about if statements, loops, and program flow control",
            content="Control flow allows your program to make decisions. You'll learn about if/elif/else statements and how to control program execution.",
            order_index=3,
            duration_minutes=50,
            is_published=True
        )
        
        db.session.add_all([lesson1, lesson2, lesson3])
        db.session.commit()
        
        print("Creating exercises...")
        exercise1 = Exercise(
            lesson_id=lesson1.id,
            title="Hello World",
            description="Write your first Python program",
            question="Which function is used to display output in Python?",
            exercise_type=ExerciseType.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.BEGINNER,
            order_index=1,
            points=10,
            options=["echo()", "print()", "console.log()", "display()"],
            correct_answer="print()",
            hint="This function is used in almost every Python tutorial",
            explanation="The print() function is the standard way to display output in Python. Example: print('Hello, World!')"
        )
        
        exercise2 = Exercise(
            lesson_id=lesson1.id,
            title="Python File Extension",
            description="Test your knowledge about Python files",
            question="What is the correct file extension for Python source files?",
            exercise_type=ExerciseType.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.BEGINNER,
            order_index=2,
            points=10,
            options=[".python", ".py", ".pt", ".pyt"],
            correct_answer=".py",
            hint="It's a two-letter extension",
            explanation="Python source files use the .py extension. For example: script.py"
        )
        
        exercise3 = Exercise(
            lesson_id=lesson2.id,
            title="Variable Assignment",
            description="Understanding how to assign values to variables",
            question="Which of the following is the correct way to assign the value 10 to a variable named 'age'?",
            exercise_type=ExerciseType.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.BEGINNER,
            order_index=1,
            points=15,
            options=["age = 10", "var age = 10", "int age = 10", "age := 10"],
            correct_answer="age = 10",
            hint="Python uses simple assignment syntax",
            explanation="In Python, you assign values to variables using the = operator. No type declaration is needed!"
        )
        
        exercise4 = Exercise(
            lesson_id=lesson2.id,
            title="String vs Number",
            description="Identifying data types",
            question="What is the data type of the value '42' (with quotes)?",
            exercise_type=ExerciseType.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.BEGINNER,
            order_index=2,
            points=15,
            options=["Integer", "String", "Float", "Boolean"],
            correct_answer="String",
            hint="Look at the quotes!",
            explanation="Values enclosed in quotes are strings, even if they contain numbers. '42' is a string, while 42 (without quotes) is an integer."
        )
        
        exercise5 = Exercise(
            lesson_id=lesson3.id,
            title="If Statement Syntax",
            description="Understanding conditional statements",
            question="Complete the code: ___ x > 10: print('Greater than 10')",
            exercise_type=ExerciseType.CODE_COMPLETION,
            difficulty=DifficultyLevel.BEGINNER,
            order_index=1,
            points=20,
            correct_answer="if",
            hint="This keyword is used to start a conditional statement",
            explanation="The 'if' keyword is used to create conditional statements in Python."
        )
        
        exercise6 = Exercise(
            lesson_id=lesson3.id,
            title="Python Uses Indentation",
            description="True or False questions about Python syntax",
            question="Python uses indentation to define code blocks.",
            exercise_type=ExerciseType.TRUE_FALSE,
            difficulty=DifficultyLevel.BEGINNER,
            order_index=2,
            points=10,
            correct_answer="True",
            hint="Think about how Python code is formatted",
            explanation="True! Python uses indentation (spaces or tabs) to define code blocks, unlike many languages that use curly braces."
        )
        
        db.session.add_all([exercise1, exercise2, exercise3, exercise4, exercise5, exercise6])
        db.session.commit()
        
        print("Creating intermediate JavaScript course...")
        js_course = Course(
            title="JavaScript Fundamentals",
            description="Master the core concepts of JavaScript programming",
            difficulty=DifficultyLevel.INTERMEDIATE,
            is_published=True,
            order_index=2
        )
        
        db.session.add(js_course)
        db.session.commit()
        
        lesson4 = Lesson(
            course_id=js_course.id,
            title="JavaScript Syntax and Variables",
            description="Learn JavaScript basics, variables with let, const, and var",
            content="JavaScript is the language of the web. Learn about variable declarations and modern ES6+ syntax.",
            order_index=1,
            duration_minutes=40,
            is_published=True
        )
        
        db.session.add(lesson4)
        db.session.commit()
        
        exercise7 = Exercise(
            lesson_id=lesson4.id,
            title="Variable Declaration",
            description="Understanding let vs const",
            question="Which keyword should you use to declare a variable that won't be reassigned?",
            exercise_type=ExerciseType.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.INTERMEDIATE,
            order_index=1,
            points=15,
            options=["var", "let", "const", "static"],
            correct_answer="const",
            hint="The keyword suggests the value is constant",
            explanation="Use 'const' for variables that won't be reassigned. Use 'let' for variables that will change."
        )
        
        db.session.add(exercise7)
        db.session.commit()
        
        print("✅ Database seeded successfully!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Course.query.count()} courses")
        print(f"Created {Lesson.query.count()} lessons")
        print(f"Created {Exercise.query.count()} exercises")


if __name__ == '__main__':
    seed_database()
