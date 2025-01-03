# __init__.py
from flask import Flask
from flask_jwt_extended import JWTManager
from .models import mongo
from .routes import auth_routes, food_routes, order_routes
from flask_cors import CORS
# SCRIPTS
from .create_users import create_users
from .add_food_items import add_food_items

app = Flask(__name__)
app.config.from_object('config.Config')

CORS(app, supports_credentials=True)

mongo.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_routes)
app.register_blueprint(food_routes)
app.register_blueprint(order_routes)

def create_app():
    with app.app_context():
        create_users()  # Create users on app startup
        add_food_items()  # Add food items on app startup
    return app
