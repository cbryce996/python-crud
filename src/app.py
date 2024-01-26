from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/profile')
def edit_profile():
    return render_template('profile.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Your authentication logic goes here

    return f"Username: {username}, Password: {password}"

if __name__ == '__main__':
    app.run(debug=True)