# routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from app.models import User, Order, FoodItem
from enum import Enum
from flask_cors import cross_origin
from bson import ObjectId
import json
import os

auth_routes = Blueprint('auth_routes', __name__)
food_routes = Blueprint('food_routes', __name__)
order_routes = Blueprint('order_routes', __name__)

jwt = JWTManager()

class Role(Enum):
    ADMIN = "admin"
    DELIVERY_BOY = "delivery_boy"
    USER = "user"

# REGISTER USER
@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    role = data.get('role', Role.USER.value)  # Default to 'user' if role is not provided

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if role not in [r.value for r in Role]:
        return jsonify({"message": f"Invalid role. Valid roles are {[r.value for r in Role]}"}), 400

    existing_user = User.find_by_username(username)
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    user = User(username, password, role)
    user.save()

    return jsonify({"message": f"{role.capitalize()} registered successfully"}), 201

# USER LOGIN LOGIC
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Extract username and password from the request
    username = data.get('username')
    password = data.get('password')
   # Check if username or password is empty or consists only of whitespace
    print(username)
    if not username or username.strip() == "":
        return jsonify({"message": "Username cannot be empty"}), 400

    if not password or password.strip() == "":
        return jsonify({"message": "Password cannot be empty"}), 400
    # Find user by username
    user = User.find_by_username(username)
    
    # Verify credentials
    if user and user['password'] == password:
        # Create JWT token
        access_token = create_access_token(identity=username)
        return jsonify({
            "access_token": access_token,
            "user": {
                "username": user["username"],
                "role": user["role"],
                "_id": str(user["_id"])
            }
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401

@auth_routes.route('/get_trains', methods=['GET'])
def get_trains():
    try:
        # Load JSON file
        file_path = os.path.join(os.path.dirname(__file__), 'train_info.json')
        print(file_path)
        with open(file_path, 'r') as file:
            data = json.load(file)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# FETCH MENU FROM DB
@food_routes.route('/menu', methods=['GET'])
# @jwt_required()
def get_menu():
    items = FoodItem.get_all()
    return jsonify({"menu": items}), 200

@food_routes.route('/addmenu', methods=['POST'])
def add_food_item():
    data = request.json
    # Validate and add food item
    response, status = FoodItem.add_food_item(data)
    return jsonify(response), status
# PLACE ORDER 
@order_routes.route('/order', methods=['POST'])
@jwt_required()
def order_food():
    data = request.get_json()
    
    # Extract user id and food items from the request
    user_id = data.get('user_id')
    food_items = data.get('food_items')
    delivery_address = data.get('delivery_address')
    train_number = data.get('train_number')  # New field for train number
    coach_number = data.get('coach_number')  # New field for coach number
    seat_number = data.get('seat_number')  # New field for seat number
    if not food_items:
        return jsonify({"message": "Food items cannot be empty."}), 400
    if not delivery_address:
        return jsonify({"message": "Delivery address is required."}), 400
    if not train_number:
        return jsonify({"message": "Train number is required."}), 400  # Validate train number
    if not coach_number:
        return jsonify({"message": "Coach number is required."}), 400  # Validate coach number
    if not seat_number:
        return jsonify({"message": "Seat number is required."}), 400  # Validate seat number

    order = Order(
        user_id, 
        food_items, 
        delivery_address, 
        train_number, 
        coach_number, 
        seat_number
    )
    order.save()

    return jsonify({"message": "Order placed successfully"}), 201

#GetAll Orders
@order_routes.route('/orders', methods=['GET'])
# @jwt_required
def get_orders():
    status = request.args.get('status')
    user_id = request.args.get('user_id')
    delivery_boy = request.args.get('delivery_boy')

    if status and user_id:  # If both status and user_id are provided
        orders = Order.find_with_filters(status=status, user_id=user_id)
    elif status and delivery_boy:
        orders = Order.find_with_filters(status=status, delivery_boy=delivery_boy)
    elif delivery_boy:
        orders = order = Order.find_with_filters(delivery_boy=delivery_boy)
    elif status:  # If only status is provided
        orders = Order.find_with_filters(status=status)
    elif user_id:  # If only user_id is provided
        orders = Order.find_with_filters(user_id=user_id)
    else:  # If no filters are provided
        orders = Order.find_with_filters()

    if not orders:
        return jsonify({"message": "No orders found for the given status."}), 404
    return jsonify(orders), 200
    
# CHECK STATUS OF ORERED ITEMS
@order_routes.route('/status/<order_id>', methods=['GET'])
@jwt_required()
def check_order_status(order_id):
    order = Order.find_by_user_id(order_id)
    if order:
        return jsonify({"order_status": order[0]["status"]}), 200
    return jsonify({"message": "Order not found"}), 404

@order_routes.route('/delivery-boys', methods=['GET'])
def get_delivery_boys():
    # Query for users with role deliveryBoy
    delivery_boys = User.get_delivery_boys()
    # Return response
    return jsonify(delivery_boys), 200

# UPDATE STATUS OF ORDER
@order_routes.route('/updateOrderStatus', methods=['POST'])
@jwt_required()
@cross_origin(origins="http://127.0.0.1:3000", supports_credentials=True)
def update_order_status():
    data = request.get_json()
    order_id = data.get('order_id')
    status = data.get('status')
    delivery_person_id = data.get('delivery_boy')
    print(data)
    if not status:
        return jsonify({"message": "Status cannot be empty."}), 400
    if not order_id:
        return jsonify({"message": "Order ID cannot be empty."}), 400
    if not delivery_person_id:
        return jsonify({"message": "Delivery Boy cannot be empty."}), 400
    status_obj = Order.find_and_update(order_id, status,delivery_person_id)

    if status_obj.matched_count == 0:
        return jsonify({"message": "Order not found."}), 404
    
    return jsonify({"message": "Order status updated successfully."}), 200

