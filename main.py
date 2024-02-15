from flask import Flask, redirect, session, url_for

from app.views.auth import auth_views
from app.views.user import user_views


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "your_secret_key"
    app.template_folder = "app/templates"
    app.static_folder = "app/static"

    return app


def register_routes(app):
    app.register_blueprint(auth_views, url_prefix="/auth")
    app.register_blueprint(user_views, url_prefix="/user")

    @app.route("/")
    def login_page():
        github_user_data = session.get("github_user")
        github_access_token = session.get("github_token")

        if github_user_data and github_access_token:
            return redirect(url_for("user_views.profile"))

        return redirect(url_for("auth_views.login"))


if __name__ == "__main__":
    app = create_app()
    register_routes(app)
    app.run(debug=True, host="0.0.0.0")
