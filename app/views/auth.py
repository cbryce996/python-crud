from flask import Blueprint, redirect, url_for, session, flash, request, render_template
from flask_oauthlib.client import OAuth
from app.forms.login import LoginForm

# Create a Blueprint for authentication views
auth_views = Blueprint('auth_views', __name__)

# Initialize OAuth extension
oauth = OAuth()

# GitHub OAuth configuration
github = oauth.remote_app(
    'github',
    consumer_key='4adb213cf55ab88d80a7',
    consumer_secret='186a1648ac0505825550da87e8fb54009b33dee4',
    request_token_params=None,
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize?scope=user'
)

@auth_views.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles traditional form-based login.

    GET: Renders the login form.
    POST: Displays a message for unavailable login.

    If form submission is valid and alternative authentication succeeds,
    sets user_id in the session and redirects to the profile.
    """
    form = LoginForm()

    if request.method == 'POST':
        flash('Login unavailable, you can authenticate using GitHub instead!', 'error')

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        authenticated_user = False

        if authenticated_user:
            session['user_id'] = 1
            return redirect(url_for('user_views.profile'))

    return render_template('login.html', form=form)

@auth_views.route('/oauth/login')
def initiate_github_oauth():
    """
    Initiates GitHub OAuth login.
    """
    return github.authorize(callback=url_for('auth_views.github_authorized', _external=True))

@auth_views.route('/oauth/callback')
def github_authorized():
    """
    Handles the callback after successful GitHub authorization.

    Retrieves GitHub user data, extracts relevant repository information,
    and stores user information in the session.
    """
    resp = github.authorized_response()

    if resp is None or resp.get('access_token') is None:
        flash('Access denied', 'error')
        return redirect(url_for('auth_views.login'))

    session['github_token'] = (resp['access_token'], '')

    github_user_data = github.get('user').data
    repositories = github.get('user/repos').data

    formatted_repositories = [
        {
            'name': repo['name'],
            'full_name': repo['full_name'],
            'url': repo['url'],
            'description': repo['description'],
        }
        for repo in repositories
    ]

    session['github_user'] = {
        'avatar_url': github_user_data.get('avatar_url'),
        'html_url': github_user_data.get('html_url'),
        'login': github_user_data.get('login'),
        'name': github_user_data.get('name'),
        'location': github_user_data.get('location'),
        'bio': github_user_data.get('bio'),
        'repositories': formatted_repositories
    }

    flash('Successfully authenticated using GitHub!')
    return redirect(url_for('user_views.profile'))

@auth_views.route('/logout')
def logout():
    """
    Logs out the user by removing GitHub-related information from the session.
    """
    session.pop('github_user', None)
    session.pop('github_token', None)
    return redirect(url_for('auth_views.login'))

@github.tokengetter
def get_github_oauth_token():
    """
    Callback to load user information from the GitHub OAuth.
    """
    return session.get('github_token')