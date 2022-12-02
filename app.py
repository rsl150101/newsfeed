from flask import Flask, render_template, request, jsonify, current_app
from sqlalchemy import create_engine, text
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    # app.config.from_pyfile("config.py")
    # database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    # app.database = database

    app.run('0.0.0.0', port=5000, debug=True)