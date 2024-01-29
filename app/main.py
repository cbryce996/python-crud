import sys
from pathlib import Path
from flask import Flask, redirect, url_for

# Add the root directory of your project to the Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


from routes.auth_routes import auth_routes
from routes.user_routes import user_routes

def create_app():
    app = Flask(__name__)

    # Set a secret key for CSRF protection
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with an actual secret key

    # Register the auth_routes and user_routes Blueprints
    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(user_routes, url_prefix='/user')

    @app.route('/')
    def login_page():
        # Redirect to the /login endpoint
        return redirect(url_for('auth_routes.login'))

    return app

if __name__ == '__main__':
    create_app().run(debug=True)