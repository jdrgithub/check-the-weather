"""
A microservice that consumes data from external AP, transforms the data, and provides via new API endpoint.

This is the core flask template to build on.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# SQLITE INSTANCE
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # CREATE LOCAL DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    # SUPPRESSES WARNINGS
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # PUSH CONTEXT MANUALLY TO APP
    with app.app_context():
        db.create_all()

    # IMPORT AND REGISTER BLUEPRINT FOR ROUTES
    from routes import main
    app.register_blueprint(main)

    return app


# Server starts only if script is executed directly, not as module.
if __name__ == '__main__':
    app = create_app()
    # STARTS FLASK AND ENABLES DEBUG MODE
    app.run(debug=True)
