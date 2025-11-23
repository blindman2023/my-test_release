"""Authentication blueprint."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        # TODO: Implement login logic
        flash('Login functionality coming soon', 'info')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        # TODO: Implement registration logic
        flash('Registration functionality coming soon', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
