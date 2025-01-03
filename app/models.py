# models.py
from flask_pymongo import PyMongo
from flask_jwt_extended import jwt_required
from bson import ObjectId
from datetime import datetime

mongo = PyMongo()
def convert_objectid_to_str(data):
    """Recursively converts all ObjectId fields to string in a dictionary or list."""
    if isinstance(data, dict):
        # Convert each value in the dictionary
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Recursively convert each item in the list
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        # Convert ObjectId to string
        return str(data)
    else:
        return data
class User:
    def __init__(self, username, password , role):
        self.username = username
        self.password = password
        self.role = role

    def save(self):
        # Save user to MongoDB
        mongo.db.users.insert_one({
            "username": self.username,
            "password": self.password,
            "role": self.role
        })

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def get_delivery_boys():
        delivery_boys = list(mongo.db.users.find({"role": "delivery_boy"}))
        return convert_objectid_to_str(delivery_boys)

class Order:
    def __init__(self, user_id, food_items, delivery_address, train_number, coach_number, seat_number, status='Pending', delivery_person_id=None, delivery_time=None):
        self.user_id = ObjectId(user_id)
        self.food_items = food_items  # List of food items (e.g. [{ "item": "Pasta", "quantity": 1 }])
        self.delivery_address = delivery_address
        self.train_number = train_number
        self.coach_number = coach_number
        self.seat_number = seat_number
        self.status = status
        self.delivery_person_id = delivery_person_id  # References delivery person
        self.delivery_time = delivery_time
        self.created_at = datetime.utcnow()

    def save(self):
        # Save order to MongoDB
        mongo.db.orders.insert_one({
            "user_id": self.user_id,
            "food_items": self.food_items,
            "delivery_address": self.delivery_address,
            "train_number": self.train_number,
            "coach_number": self.coach_number,
            "seat_number": self.seat_number,
            "status": self.status,
            "delivery_person_id": self.delivery_person_id,
            "delivery_time": self.delivery_time,
            "created_at": self.created_at
        })

    @staticmethod
    def find_by_user_id(user_id):
        return list(mongo.db.orders.find({"user_id": user_id}))
    @staticmethod
    def find_by_id(order_id):
        # Fetch order by its ID
        return mongo.db.orders.find_one({"_id": ObjectId(order_id)})

    @staticmethod
    def find_and_update(order_id,status, deliveryBoy):
        update_data = {
            "$set": {
                "status": status,
                "delivery_person_id": ObjectId(deliveryBoy)
            }
        }

        # If status is 'Delivered', add the delivery_time to the update
        if status.lower() == "delivered":
            update_data["$set"]["delivery_time"] = datetime.utcnow()  # Adding delivery time as the current UTC time

        return mongo.db.orders.update_one(
            {"_id": ObjectId(order_id)},  # Filter by order ID
            update_data  # Apply the update data
        )
    @staticmethod
    def find_with_filters(status=None, user_id=None ,delivery_boy=None):
        pipeline=[]
        if delivery_boy:
            pipeline.append({
                "$match": {
                    "delivery_person_id": ObjectId(delivery_boy)  # Filter orders by user_id
                }
            })
        if user_id:
            pipeline.append({
                "$match": {
                    "user_id": ObjectId(user_id)  # Filter orders by user_id
                }
            })
        # Fetch documents from MongoDB without filters
        if status == "notPending":
            pipeline.append({
                "$match": {
                    "status": {"$ne": "Pending"}  # Exclude orders with status 'Pending'
                }
            })
        elif status:
            # If status is provided, filter orders by the exact status
            pipeline.append({
                "$match": {
                    "status": status  # Filter orders by the status provided
                }
            })
        pipeline.append({
        "$lookup": {
            "from": "users",  # The collection to join
            "localField": "user_id",  # Field from the orders collection
            "foreignField": "_id",  # Field from the users collection
            "as": "user_data"  # Output field that will hold the joined user data
            }
        })

        # Flatten the user data (optional) and remove _id if necessary
        pipeline.append({
            "$unwind": {
                "path": "$user_data",
                "preserveNullAndEmptyArrays": True  # Keep orders without matching user data
            }
        })
        pipeline.append({
        "$lookup": {
            "from": "users",
            "localField": "delivery_person_id",
            "foreignField": "_id",
            "as": "delivery_person_data"
            }
        })

        # Unwind delivery_person_data array
        pipeline.append({
            "$unwind": {
                "path": "$delivery_person_data",
                "preserveNullAndEmptyArrays": True
            }
        })
        # Execute the aggregation pipeline
        results = list(mongo.db.orders.aggregate(pipeline))

        # Optionally, you can clean up the user data to remove unnecessary fields or format them
        for order in results:
            order["user_data"] = {
                  # Convert ObjectId to string
                "username": order["user_data"].get("username"),
                "role": order["user_data"].get("role"),
            }
            order["delivery_person_data"] = {
                "username": order["delivery_person_data"].get("username") if order.get("delivery_person_data") else None,
                "role": order["delivery_person_data"].get("role") if order.get("delivery_person_data") else None,
            }
        results = convert_objectid_to_str(results)
        return results



class FoodItem:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        # Save food item to MongoDB
        mongo.db.food_items.insert_one({
            "name": self.name,
            "description": self.description,
            "price": self.price
        })

    @staticmethod
    def get_all():
        food_items = list(mongo.db.food_items.find())
        # Convert each food item document into a dictionary for JSON serialization
        return [FoodItem.to_dict(item) for item in food_items]

    @staticmethod
    def to_dict(food_item):
        # Convert the MongoDB document to a dictionary (e.g., handle ObjectId conversion)
        return {
            "id": str(food_item["_id"]),  # Convert ObjectId to string
            "name": food_item["name"],
            "description": food_item["description"],
            "price": food_item["price"]
        }
    @staticmethod
    def find_by_name(name):
        # Find a food item by name
        return mongo.db.food_items.find_one({"name": name})
    
    @staticmethod
    def add_food_item(data):
        """Validate and add a new food item to the database."""
        required_fields = ["name", "description", "price"]

        # Check for missing fields
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400

        # Validate price (ensure it's a number and non-negative)
        try:
            price = float(data["price"])
            if price < 0:
                return {"error": "Price must be a non-negative number."}, 400
        except ValueError:
            return {"error": "Price must be a valid number."}, 400

        # Check if food item already exists
        if FoodItem.find_by_name(data["name"]):
            return {"error": "A food item with this name already exists."}, 400

        # Save the food item
        new_food_item = FoodItem(data["name"], data["description"], price)
        new_food_item.save()

        return {"message": "Food item added successfully."}, 201