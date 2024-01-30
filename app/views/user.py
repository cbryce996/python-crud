from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.forms.edit import EditForm
import requests

# Create a Blueprint for user views
user_views = Blueprint('user_views', __name__)

@user_views.route('/profile', methods=['GET'])
def profile():
    """
    Renders the user profile page.

    Displays user data retrieved from the GitHub session and provides an edit link.
    """
    github_user_data = session.get('github_user')
    github_access_token = session.get('github_token')

    if not github_user_data or not github_access_token:
        flash('You must log in to access this page.', 'error')
        return redirect(url_for('auth_views.login'))

    form = EditForm(request.form, **github_user_data)

    return render_template('profile.html', user_data=github_user_data, form=form)

@user_views.route('/edit', methods=['GET', 'POST'])
def edit():
    """
    Renders the user edit page and handles user data updates.

    Retrieves user data from the GitHub session, validates the form,
    and updates the user data on form submission.
    """
    github_user_data = session.get('github_user')
    github_access_token = session.get('github_token')

    if not github_user_data or not github_access_token:
        flash('You must log in to access this page!', 'error')
        return redirect(url_for('auth_views.login'))

    form = EditForm(**github_user_data)

    if form.validate_on_submit():
        if request.method == 'POST':
            new_data = {
                'name': form.name.data,
                'location': form.location.data,
                'bio': form.bio.data
            }

            update_response = update_github_user(github_access_token[0], new_data)

            if update_response:
                updated_user_data = requests.get('https://api.github.com/user', headers={'Authorization': f'Bearer {github_access_token[0]}'})
                updated_user_data = updated_user_data.json()

                session['github_user'] = {
                    'avatar_url': updated_user_data.get('avatar_url'),
                    'login': updated_user_data.get('login'),
                    'name': updated_user_data.get('name'),
                    'location': updated_user_data.get('location'),
                    'bio': updated_user_data.get('bio'),
                    'repositories': github_user_data.get('repositories', []),
                }

                flash('User information updated successfully!', 'success')
                return redirect(url_for('user_views.profile'))
            else:
                flash('Error updating user information. Please try again!', 'error')

    return render_template('edit.html', form=form)

def update_github_user(access_token, new_data):
    """
    Updates the user data on GitHub.

    Sends a PATCH request to the GitHub API with the provided access token and new data.

    Returns True on successful update, False otherwise.
    """
    url = 'https://api.github.com/user'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    response = requests.patch(url, headers=headers, json=new_data)

    if response.status_code == 200:
        return True
    else:
        flash(f'Error updating user information: {response.status_code} - {response.text}', 'error')
        return False
