# app.py
from flask import Flask, redirect, url_for
from routes.auth_routes import auth_routes
from routes.user_routes import user_routes
from database.session import init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set a secret key for CSRF protection
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with an actual secret key

# Initialize the database
init_db(app)

# Register the auth_routes and user_routes Blueprints
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(user_routes, url_prefix='/user')

@app.route('/')
def login_page():
    # Redirect to the /login endpoint
    return redirect(url_for('auth_routes.login'))

if __name__ == '__main__':
    app.run(debug=True)