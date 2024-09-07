"""
A microservice that consumes data from external AP, transforms the data, and provides via new API endpoint.

THIS IS A STANDALONE FILE FOR NOW
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import os
import requests
from dash_weather import init_dashboard

app_blueprint = Blueprint('app_blueprint', __name__)
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}'


@app_blueprint.route('/')
def home():
    return 'Welcome to the Home Page!'


@app_blueprint.route('/about')
def about():
    return 'This is the ABOUT page.'


# ROUTE TO TEST
@app_blueprint.route('/test')
def users():
    return "This is working!"


# PUT USER_ID IN TO QUERY
@app_blueprint.route("/get-user/<user_id>")
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {
        "user_id": user.id,
        "name": user.username,
        "email": user.email
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200


@app_blueprint.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()

    return jsonify(data), 201


@app_blueprint.route('/list_users')
def list_users():
    all_users = User.query.all()
    if not users:
        return "No users found."
    return render_template('users.html', users=all_users)


# ROUTE TO ADD A NEW USER VIA FORM SUBMISSION
@app_blueprint.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        if username and email:
            # CREATE NEW USER
            new_user = User(username=username, email=email)

            # ADD TO SESSION
            try:
                with db.session.begin():
                    db.session.add(new_user)
                return redirect(url_for('app_blueprint.list_users'))
            except Exception as e:
                # Prevents BadRequestKeyError if no keys.
                return render_template('add_user.html', error=str(e))  # Display errors
        else:
            return render_template('add_user.html', error="Please provide username and email both.\n")
    return render_template('add_user.html')


@app_blueprint.route('/weather/<city>')
def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key not found.  Please set OPENWEATER_API_KEY environmental variable.")
    city = 'London'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        weather_data = response.json()
        print(weather_data)
    else:
        print(f"Failed to retrieve data: {response.status_code}")

    data = response.json()
    return jsonify(data), 200

@app_blueprint.route('/weather-transformed/<city>')
def get_weather_transformed(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key not found.  Please set OPENWEATER_API_KEY environmental variable.")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Unable to fetch weather data"}), 500

    data = response.json()

    # Transform the data
    transformed_data = {
        "city": data["name"],
        "temperature_celsius": data["main"]["temp"],
        "temperature_fahrenheit": data["main"]["temp"] * 9/5 + 32,  # Convert to Fahrenheit
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"]
    }

    # return jsonify(transformed_data), 200
    return jsonify(transformed_data), 200



def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    # Import blueprints or routes
    flask_app.register_blueprint(app_blueprint)

    # Initialize the Dash app and pass flask app's server
    init_dashboard(flask_app)

    return flask_app


# Create/name the blueprint/Create blueprint object
# Server starts only if script is executed directly, not as module.
if __name__ == '__main__':
    app = create_app()
    # STARTS FLASK AND ENABLES DEBUG MODE
    app.run(debug=True)
