from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from forms import EditProfileForm
import requests

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/profile', methods=['GET', 'POST'])
def profile():
    github_user_data = session.get('github_user')
    form = EditProfileForm(request.form, **github_user_data)  # Initialize form with existing user data

    if request.method == 'POST' and form.validate():
        # Handle the form submission for updating user information
        new_data = {
            'name': form.name.data,
            'location': form.location.data,
            'bio': form.bio.data,
            'email': form.email.data,
            # Add other fields as needed
        }

        access_token = session.get('github_token')[0]
        update_github_user(access_token, new_data)

        # Optionally, you can fetch the updated user information and update the session
        updated_user_data = requests.get('https://api.github.com/user', headers={'Authorization': f'Bearer {access_token}'}).json()
        session['github_user'] = updated_user_data

        flash('User information updated successfully!', 'success')

    return render_template('profile.html', user_data=github_user_data, form=form)

@user_routes.route('/edit', methods=['GET', 'POST'])
def edit():
    form = EditProfileForm()
    user_data = session.get('github_user')

    if request.method == 'POST' and form.validate_on_submit():
        new_data = {
            'name': form.name.data,
            'location': form.location.data,
            'bio': form.bio.data,
            'email': form.email.data,
            # Add other fields as needed
        }

        access_token = session.get('github_token')[0]
        update_response = update_github_user(access_token, new_data)

        if update_response:
            flash('User information updated successfully!', 'success')
        else:
            flash('Error updating user information. Please try again.', 'error')
    else:
        flash('Please correct the form errors and try again.', 'error')

    return render_template('edit.html', form=form, user_data=user_data)

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