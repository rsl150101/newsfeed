from flask import Flask, render_template, request, jsonify, current_app
from sqlalchemy import create_engine, text
app = Flask(__name__)


@app.route('/')
def home():
    page_title = "HOME"
    return render_template('index.html', pageTitle=page_title)


@app.route('/login')
def login():
    page_title = "LOGIN"
    return render_template('login.html', pageTitle=page_title)


@app.route('/join')
def join():
    page_title = "JOIN"
    return render_template('join.html', pageTitle=page_title)


@app.route('/users/<user_id>/edit')
def edit_profile(user_id):
    page_title = "Edit Profile"
    return render_template('edit-profile.html', pageTitle=page_title)


if __name__ == '__main__':
    # app.config.from_pyfile("config.py")
    # database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    # app.database = database

    app.run('0.0.0.0', port=5000, debug=True)
