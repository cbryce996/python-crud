from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from forms import EditProfileForm
import requests

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/profile', methods=['GET'])
def profile():
    # Get required information
    github_user_data = session.get('github_user')
    github_access_token = session.get('github_token')
    
    # Check if required information is present
    if not github_user_data or not github_access_token:
        flash('You must log in to access this page.', 'error')
        return redirect(url_for('auth_routes.login'))
    
    # Populate form with session data
    form = EditProfileForm(request.form, **github_user_data)

    # Render the profile page
    return render_template('profile.html', user_data=github_user_data, form=form)

@user_routes.route('/edit', methods=['GET', 'POST'])
def edit():
    # Get required information
    github_user_data = session.get('github_user')
    github_access_token = session.get('github_token')

    # Check if required information is present
    if not github_user_data or not github_access_token:
        flash('You must log in to access this page!', 'error')
        return redirect(url_for('auth_routes.login'))

    # Populate form with session data
    form = EditProfileForm(**github_user_data)

    print(github_access_token)

    # Validate the form
    if form.validate_on_submit():

        # Handle POST method
        if request.method == 'POST':
            new_data = {
                'name': form.name.data,
                'location': form.location.data,
                'bio': form.bio.data
            }

            update_response = update_github_user(github_access_token[0], new_data)

            if update_response:
                # Update session with the latest user data
                updated_user_data = requests.get('https://api.github.com/user', headers={'Authorization': f'Bearer {github_access_token[0]}'})
                updated_user_data = updated_user_data.json()

                # Update the session with the same format as auth data
                session['github_user'] = {
                    'avatar_url': updated_user_data.get('avatar_url'),
                    'login': updated_user_data.get('login'),
                    'name': updated_user_data.get('name'),
                    'location': updated_user_data.get('location'),
                    'bio': updated_user_data.get('bio'),
                    'repositories': github_user_data.get('repositories', []),
                }

                flash('User information updated successfully!', 'success')
                return redirect(url_for('user_routes.profile'))
            else:
                flash('Error updating user information. Please try again!', 'error')

    return render_template('edit.html', form=form)

def update_github_user(access_token, new_data):
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