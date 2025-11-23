"""Learning blueprint for educational content."""
from flask import Blueprint, render_template, request
from flask_login import login_required

learning_bp = Blueprint('learning', __name__, url_prefix='/learning', url_defaults={'lang': 'zh'})


@learning_bp.route('/')
def index():
    """Render learning dashboard."""
    return render_template('learning/index.html')


@learning_bp.route('/courses')
def courses():
    """List all courses."""
    return render_template('learning/courses.html')


@learning_bp.route('/course/<int:course_id>')
def course_detail(course_id):
    """Display course details."""
    return render_template('learning/course_detail.html', course_id=course_id)


@learning_bp.route('/progress')
@login_required
def progress():
    """Display user learning progress."""
    return render_template('learning/progress.html')
