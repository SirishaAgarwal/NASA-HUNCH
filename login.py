import hashlib
import json
import os

print("LOGIN SYSTEM IS RUNNING")

USER_DB = "users.json"

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, role="user"):
    users = load_users()
    if username in users:
        return False, "User already exists."

    users[username] = {
        "password": hash_password(password),
        "role": role
    }

    save_users(users)
    return True, "User created successfully."

def login(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found."

    if users[username]["password"] == hash_password(password):
        return True, users[username]["role"]
    return False, "Incorrect password."

if __name__ == "__main__":
    while True:
        print("\n1. Create Account\n2. Login\n3. Exit")
        choice = input("Choose: ")

        if choice == "1":
            u = input("Username: ")
            p = input("Password: ")
            role = input("Role (admin/user): ")
            print(create_user(u, p, role)[1])

        elif choice == "2":
            u = input("Username: ")
            p = input("Password: ")
            success, result = login(u, p)
            if success:
                print(f"Login successful. Role: {result}")
            else:
                print(result)

        elif choice == "3":
            break
        else:
            print("Invalid choice")
