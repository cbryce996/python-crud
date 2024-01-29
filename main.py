import sys
from pathlib import Path
from flask import Flask, redirect, url_for, session
from app.routes.auth_routes import auth_routes
from app.routes.user_routes import user_routes

def create_app():
    app = Flask(__name__)

    # Set a secret key for CSRF protection
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with an actual secret key

    app.template_folder = 'app/templates'
    app.static_folder = 'app/static'

    return app

def register_routes(app):
    # Register the auth_routes and user_routes Blueprints
    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(user_routes, url_prefix='/user')

    @app.route('/')
    def login_page():
        # Check if user data and token are present
        github_user_data = session.get('github_user')
        github_access_token = session.get('github_token')

        if github_user_data and github_access_token:
            # Redirect to the profile page if data and token are present
            return redirect(url_for('user_routes.profile'))

        # Redirect to the /login endpoint if no user data or token
        return redirect(url_for('auth_routes.login'))

if __name__ == '__main__':
    app = create_app()
    register_routes(app)
    app.run(debug=True, host='0.0.0.0')