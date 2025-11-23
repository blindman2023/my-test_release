from app import create_app, db
from app.models import (
    User, Course, Lesson, Exercise,
    ExerciseAttempt, ProgressSnapshot, ChatMessage
)

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Course': Course,
        'Lesson': Lesson,
        'Exercise': Exercise,
        'ExerciseAttempt': ExerciseAttempt,
        'ProgressSnapshot': ProgressSnapshot,
        'ChatMessage': ChatMessage,
    }


if __name__ == '__main__':
    app.run(debug=True)
