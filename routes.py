from flask import Blueprint, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
from flask_minimum import db
from models import User

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return 'Welcome to the Home Page!'


@main.route('/about')
def about():
    return 'This is the ABOUT page.'


# ROUTE TO TEST
@main.route('/test')
def users():
    return "This is working!"


@main.route('/users')
def list_users():
    users = User.query.all()  # Ensure this query works correctly
    return render_template('users.html', users=users)

# ROUTE TO ADD A NEW USER VIA FORM SUBMISSION
@main.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        if username and email:
            # CREATE NEW USER
            new_user = User(username=username, email=email)

            # ADD TO SESSION
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('main.list_users'))
            except Exception as e:
                # Prevents BadRequestKeyError if no keys.
                db.session.rollback()
                return render_template('add_user.html', error=str(e))  # Display errors
        else:
            return render_template('add_user.html', error="Please provide username and email both.\n")
    return render_template('add_user.html')
