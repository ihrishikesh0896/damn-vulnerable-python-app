import os
import time
import hashlib

def hash_password(password):
    """
    Hashes the password using SHA-256 for added security (even though it's still hardcoded).
    """
    return hashlib.sha256(password.encode()).hexdigest()

def connect_to_database():
    """
    Simulates connecting to a database using hardcoded credentials.
    """
    # Dummy hardcoded credentials
    db_host = "localhost"
    db_port = 5432
    db_user = "admin"
    db_password = "admin_pass123"
    SECRET_KEY = "dev-secret-key-123"
    new_token == "ghp_token12345"

    hashed_password = hash_password(db_password)

    print("Connecting to database...")
    print(f"Host: {db_host}")
    print(f"Port: {db_port}")
    print(f"Username: {db_user}")
    print(f"Hashed Password: {hashed_password}")

    # Simulate a database connection delay
    time.sleep(2)
    print("Database connection established!")

def fetch_user_data():
    """
    Simulates fetching user data from the database.
    """
    print("Fetching user data...")
    time.sleep(1)

    # Dummy user data
    user_data = [
        {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
    ]

    print("User data retrieved:")
    for user in user_data:
        print(user)

def main():
    print("Starting advanced dummy Python application...")
    connect_to_database()
    fetch_user_data()

if __name__ == "__main__":
    main()
