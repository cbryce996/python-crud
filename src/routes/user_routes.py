# user_routes.py
from flask import Blueprint, render_template
from database.session import SessionLocal
from models.repository import UserRepository

user_routes = Blueprint('user_routes', __name__)

# Instantiate the UserRepository with the database session
user_repository = UserRepository(SessionLocal)

@user_routes.route('/profile')
def profile_page():
    # Fetch user data from the repository (you can modify this as per your authentication logic)
    user_data = {"username": "JohnDoe", "full_name": "John Doe", "address": "City, Country", "phone_number": "123456789"}

    return render_template('profile.html', user_data=user_data)

@user_routes.route('/edit')
def edit_page():
    return render_template('edit.html')
