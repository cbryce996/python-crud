# user_routes.py
from flask import Blueprint, render_template, session, redirect, url_for, request
from database.session import SessionLocal
from models.repository import UserRepository

user_routes = Blueprint('user_routes', __name__)

# Instantiate the UserRepository with the database session
user_repository = UserRepository(SessionLocal)


@user_routes.route('/profile', methods=['GET', 'POST'])
def profile():
    github_user_data = session.get('github_user')

    # Rest of your code...
    return render_template('profile.html', user_data=github_user_data)

@user_routes.route('/edit')
def edit():
    user_data = request.args.get('user_data')  # Access the user_data parameter
    # Rest of your code...
    return render_template('edit.html', user_data=user_data)