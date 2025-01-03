# config.py
import os

class Config:
    # MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/train_food_ordering")
    # MONGO_URI = 'mongodb+srv://graphQLDemo:password12345@mycluster.qbijw.mongodb.net/train_food_ordering?retryWrites=true&w=majority&appName=MyCluster'
    MONGO_URI = "mongodb+srv://graphQLDemo:password12345@mycluster.qbijw.mongodb.net/train_food_ordering?retryWrites=true&w=majority&ssl=true&tlsAllowInvalidCertificates=true"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")  # Change this to a secure key
