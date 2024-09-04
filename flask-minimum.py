# Import Flask class from flask module
from flask import Flask

# Create instance of Flask class
# The __name__ variable helps Flask to understand where the app is located (used for setting up paths).
app = Flask(__name__)

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
