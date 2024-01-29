from flask import Blueprint, redirect, url_for, session, flash, request, render_template, session
from flask_oauthlib.client import OAuth
from forms import LoginForm

auth_routes = Blueprint('auth_routes', __name__)

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
    authorize_url='https://github.com/login/oauth/authorize?scope=user:email'
)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = {'form': None, 'inputs': {'username': None, 'password': None}}

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        authenticated_user = False

        # Placeholder alternative authentication
        if authenticated_user:
            session['user_id'] = 1
            return redirect(url_for('user_routes.profile'))
        else:
            errors['form'] = "Login Disabled: Log in with Github"

    # For GET request or failed authentication, render the login form
    return render_template('login.html', errors=errors, form=form)

@auth_routes.route('/oauth/login')
def initiate_github_oauth():
    return github.authorize(callback=url_for('auth_routes.github_authorized', _external=True))

@auth_routes.route('/oauth/callback')
def github_authorized():
    resp = github.authorized_response()

    if resp is None or resp.get('access_token') is None:
        flash('Access denied: reason={} error={}'.format(
            request.args.get('error_reason'),
            request.args.get('error_description')
        ), 'error')
        return redirect(url_for('auth_routes.login'))

    session['github_token'] = (resp['access_token'], '')

    github_user_data = github.get('user').data

    # Fetch repositories
    repositories = github.get('user/repos').data

    # Extract relevant repository information
    formatted_repositories = [
        {
            'name': repo['name'],
            'full_name': repo['full_name'],
            'url': repo['url'],
            'description': repo['description'],
            # Add other fields as needed
        }
        for repo in repositories
    ]

    print("GitHub User Data:", github_user_data)
    print("GitHub Repositories:", formatted_repositories)

    session['github_user'] = {
        'avatar_url': github_user_data.get('avatar_url'),
        'login': github_user_data.get('login'),
        'name': github_user_data.get('name'),
        'location': github_user_data.get('location'),
        'bio': github_user_data.get('bio'),
        'email': github_user_data.get('email'),
        'repositories': formatted_repositories,  # Add formatted repositories to the session
        # Add other relevant fields as needed
    }

    flash('Login successful!')
    return redirect(url_for('user_routes.profile'))

@auth_routes.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('github_user', None)
    session.pop('github_token', None)
    return redirect(url_for('auth_routes.login'))

# Callback to load user information from the GitHub OAuth
@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')