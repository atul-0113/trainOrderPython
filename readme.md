
# Train Food Ordering Backend

This is the backend for the Train Food Ordering application. It allows users to place food orders while traveling on trains, with features such as authentication, order management, and food item selection.

## Prerequisites

- Python 3.x
- MongoDB (local or Atlas)
- A virtual environment (recommended)

## Steps to Run the Project

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/yourusername/your-repository-name.git
cd your-repository-name
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

- **On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

- **On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies by running:

```bash
pip3 install -r requirements.txt
```

### 4. Set Up MongoDB

If you're using a **local MongoDB instance**, ensure MongoDB is installed and running. If you're using **MongoDB Atlas**, make sure you have a connection URI.

- Open the `config.py` file and update the `MONGO_URI` variable with your MongoDB connection string:

```python
MONGO_URI = 'your_mongo_connection_string_here'
```

### 5. Create Users (If Necessary)

If your application requires an initial admin user or other setup, ensure the script to create users is run. You can set up your database and users programmatically during the first run. This might be part of your app's start-up process, like in the `create_users.py` script.

### 6. Run the Application

Once everything is set up, run the Flask app using the following command:

```bash
python run.py
```

The backend server will start, and you should be able to access the API at `http://127.0.0.1:5000` by default.

### 7. Testing the Application

You can use tools like **Postman** or **Insomnia** to make API requests or test the functionality via `curl`.

### 8. Environment Variables

Some configurations might require environment variables. For instance:

- **JWT_SECRET_KEY** for JWT-based authentication.
  
Set the environment variable:

```bash
export JWT_SECRET_KEY="your_secret_key"  # On macOS/Linux
set JWT_SECRET_KEY="your_secret_key"     # On Windows
```

Alternatively, you can hardcode them in the `config.py` file.

### 9. Troubleshooting

- If you encounter errors related to missing packages, ensure you’ve installed all dependencies correctly by running `pip install -r requirements.txt` again.
- If MongoDB is not connecting, verify your URI in `config.py` and ensure that the MongoDB instance is running.

---

## Project Structure

- `app/`: Main directory containing the app.
  - `routes.py`: Defines API routes and endpoints.
  - `models.py`: Defines database models.
  - `create_users.py`: A script to create initial users in the app.
  - `add_food_items.py`: A Script to add default menu in the app.
  - `enum.py`: Default file for adding new enums to app.
- `config.py`: Configuration settings for the app (e.g., MongoDB URI, JWT key).
- `requirements.txt`: List of Python packages the app depends on.
- `run.py`: Main file to run the Flask app.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
