from app.models import User
from app import mongo

def create_users():
    # Check and create Admin user
    if not User.find_by_username("admin"):
        admin_user = User(username="admin", password="admin123", role="admin")
        admin_user.save()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

    # Check and create Delivery Boy users
    delivery_boys = [
        {"username": "DeliveryBoy1", "password": "123456", "role": "delivery_boy"},
        {"username": "DeliveryBoy2", "password": "123456", "role": "delivery_boy"},
        {"username": "DeliveryBoy3", "password": "123456", "role": "delivery_boy"}
    ]

    for boy in delivery_boys:
        if not User.find_by_username(boy["username"]):
            delivery_boy = User(username=boy["username"], password=boy["password"], role=boy["role"])
            delivery_boy.save()
            print(f"{boy['username']} created.")
        else:
            print(f"{boy['username']} already exists.")

    # Check and create regular users
    regular_users = [
        {"username": "User1", "password": "123456", "role": "user"},
        {"username": "User2", "password": "123456", "role": "user"}
    ]

    for user in regular_users:
        if not User.find_by_username(user["username"]):
            regular_user = User(username=user["username"], password=user["password"], role=user["role"])
            regular_user.save()
            print(f"{user['username']} created.")
        else:
            print(f"{user['username']} already exists.")

if __name__ == "__main__":
    create_users()
