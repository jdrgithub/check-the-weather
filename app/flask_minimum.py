"""
A microservice that consumes data from external AP, transforms the data, and provides via new API endpoint.

This is the core flask template to build on.
"""

from flask import Flask
from routes import main
from flask_sqlalchemy import SQLAlchemy

# FLASK INSTANCE
app = Flask(__name__)
# CREATE LOCAL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Disable track modifications to suppress warnings
# SQLALCHEMY INSTANCE
db = SQLAlchemy(app)
# REGISTER ROUTES
app.register_blueprint(main)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}'


# Define a route for root URL -> tells Flask what URL triggers `home` function.
@app.route('/')
def home():
    # `home` executed when upon access to root URL ('/')
    # Returns response message displayed in the browser
    return "TEMP TEXT"


# Server starts only if script is executed directly, not as module.
if __name__ == '__main__':
    # app.run() starts the Flask development server on http://127.0.0.1:5000
    # enables debug mode -> error messages and auto-reloads server on code change.
    app.run(debug=True)
