from flask import Blueprint, render_template, redirect, url_for, session, request
from database.session import SessionLocal
from models.repository import UserRepository

auth_routes = Blueprint('auth_routes', __name__)

# Instantiate the UserRepository with the database session
user_repository = UserRepository(SessionLocal)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Assuming you have a function like authenticate_user in your UserRepository
        username = request.form.get('username')
        password = request.form.get('password')

        authenticated_user = user_repository.authenticate_user(username, password)

        if authenticated_user:
            # Store user information in the session for future requests
            session['user_id'] = authenticated_user.id
            return redirect(url_for('user_routes.profile_page'))
        else:
            return render_template('login.html', error_message="Invalid credentials")

    # For GET request, render the login form
    return render_template('login.html')

@auth_routes.route('/logout')
def logout():
    # Clear the user session data
    session.clear()
    return redirect(url_for('auth_routes.login'))
