from flask import Blueprint, render_template, redirect, url_for, flash
from forms import LoginForm
from database.session import SessionLocal
from models.repository import UserRepository

user_routes = Blueprint('user_routes', __name__)
user_repository = UserRepository(SessionLocal)

@user_routes.route('/profile', methods=['GET', 'POST'])
def profile_page():
    form = LoginForm()

    if form.validate_on_submit():
        # Handle form submission
        username = form.username.data
        password = form.password.data

        # Your authentication logic goes here
        # Example: Check credentials using the user repository
        if user_repository.authenticate_user(username, password):
            flash('Login successful!', 'success')
            return redirect(url_for('user_routes.profile_page'))

        flash('Invalid username or password', 'error')

    return render_template('profile.html', form=form)