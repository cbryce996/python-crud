# auth_routes.py
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from database.session import SessionLocal
from models.repository import UserRepository
from forms import LoginForm

auth_routes = Blueprint('auth_routes', __name__)

# Instantiate the UserRepository with the database session
user_repository = UserRepository(SessionLocal)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = {'form': None, 'inputs': {'username': None, 'password': None}}

    if request.method == 'POST':
        # Input-level validation
        username = request.form.get('username')
        password = request.form.get('password')

        if len(username) < 4:
            errors['inputs']['username'] = "Username must be at least 4 characters"

        if len(password) < 6:
            errors['inputs']['password'] = "Password must be at least 6 characters"

        if not errors['inputs']['username'] and not errors['inputs']['password']:
            # Assuming you have a function like authenticate_user in your UserRepository
            #authenticated_user = user_repository.authenticate_user(username, password)
            authenticated_user = True

            if authenticated_user:
                # Store user information in the session for future requests
                #session['user_id'] = authenticated_user.id
                session['user_id'] = 1
                return redirect(url_for('user_routes.profile'))
            else:
                errors['form'] = "Incorrect Login"

    # For GET request or failed authentication, render the login form
    return render_template('login.html', errors=errors, form=form)

@auth_routes.route('/logout')
def logout():
    # Clear the user session data
    session.clear()
    return redirect(url_for('auth_routes.login'))
