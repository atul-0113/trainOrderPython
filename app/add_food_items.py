from app.models import FoodItem
from app import mongo

def add_food_items():
    # Sample list of food items
    indian_foods = [
        { "name": "Pani Puri", "description": "Crispy puris filled with spiced water", "price": 5.99},
        { "name": "Samosa", "description": "Fried pastry filled with spiced potatoes", "price": 2.99},
        { "name": "Chole Bhature", "description": "Spicy chickpeas served with fried bread", "price": 7.99},
        { "name": "Dosa", "description": "Crispy rice pancake served with chutney", "price": 4.99},
        { "name": "Pav Bhaji", "description": "Spicy mashed vegetables served with bread", "price": 6.49},
        { "name": "Biryani", "description": "Aromatic rice and meat dish", "price": 10.99},
        { "name": "Momos", "description": "Steamed dumplings filled with vegetables or meat", "price": 4.49},
        { "name": "Gulab Jamun", "description": "Sweet fried dough balls soaked in syrup", "price": 3.99}
    ]
    
    for food in indian_foods:
        # Check if food item already exists
        existing_food = FoodItem.find_by_name(food['name'])
        if not existing_food:
            food_item = FoodItem(name=food['name'], description=food['description'], price=food['price'])
            food_item.save()
            print(f"Food item {food['name']} added.")
        else:
            print(f"Food item {food['name']} already exists.")

if __name__ == "__main__":
    add_food_items()
