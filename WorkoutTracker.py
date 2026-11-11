import json
import os
import hashlib
import getpass
from datetime import datetime

# Setup data file for user data
FILE = "workout_data.json"


def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {"users": {}}


def save_data():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


data = load_data()


# =============================================================
# Create new user
def create_new_user():
    print("\n==========Create New User==========")
    print("\nWarning, once submitted, your user name, name,\n and recovery word cannot be changed.")

    name = input("Full Name: ")
    username = input("Username: ")

    if not name or not username:
        print("Name and/or Username cannot be empty")

    if username in data["users"]:
        print("Username already exists, choose another")
        return

    password = getpass.getpass("Password: ")

    if len(password) < 8:
        print("Password must contain at least 8 characters")

    confirm_password = getpass.getpass("Confirm Password: ")

    if password != confirm_password:
        print("Passwords do not match")
        return

    recovery_word = getpass.getpass("Create Recovery Word: ")

    if len(recovery_word) < 3:
        print("Recovery word must contain at least 3 characters")
        return

    data["users"][username] = {
        "name": name,
        "password": password_hash(password),
        "recovery_word": password_hash(recovery_word),
        "age": "",
        "height": "",
        "weight": "",
        "run goal": "",
        "strength goal": "",
        "history": []
    }

    save_data()

    print("\nAccount created successfully")
    print("Welcome, {name}")


# ==========================================================
# Login to application
def login():
    print("\n==========Login==========")

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    user = data["users"].get(username)

    if user and user["password"] == password_hash(password):
        print("\n Login Successful")
        home_page(username)
    else:
        print("Invalid username or password")


# ===========================================================
# Recover Password
def recover_password():
    print("\n==========Recover Password==========")

    username = input("Username: ")

    if username not in data["users"]:
        print("Account not found")
        return

    recovery_word = getpass.getpass("Enter your recovery word: ")

    if recovery_word != data["users"][username]["recovery_word"]:
        print("Incorrect recovery word, try again")
        return

    new_password = getpass.getpass("Enter new password: ")

    if len(new_password) < 8:
        print("Password must contain at least 8 characters")

    confirm_password = getpass.getpass("Confirm Password: ")

    if new_password != confirm_password:
        print("Passwords do not match")
        return

    data["users"][username]["password"] = new_password

    save_data()

    print("\nPassword reset successfully")


# ============================================
# User Profile

def user_profile(username):
    while True:
        user = data["users"][username]
        print("\n==========User Profile==================")
        print(f"\nYour Info, {username}")

        print(f"\nAge: {user['age']}")
        print(f"Height: {user['height']}")
        print(f"Weight: {user['weight']}")
        print(f"Run Goal: {user['run goal']}")
        print(f"Strength Goal: {user['strength goal']}")

        print("\n\n[1] Update Info")
        print("[2] Historical Info")
        print("[3] Go to FAQ Page")
        print("[0] Back to Homepage")

        selection = input("Choose an option: ")

        if selection == "1":
            update_info(username)
        elif selection == "2":
            historical_info(username)
        elif selection == "3":
            faq()
        elif selection == "0":
            print("\nReturning to Homepage")
            break
        else:
            print("Invalid option, try again.")


def update_info(username):
    user = data["users"][username]
    print("\n========Update Your Information========")

    age = input("Update Age (enter to skip): ")
    height = input("Update Height (enter to skip): ")
    weight = input("Update Weight (enter to skip): ")
    run_goal = input("Update Run Goal (enter to skip): ")
    strength_goal = input("Update Strength Goal (enter to skip): ")

    changes = {}

    if age:
        changes["age"] = age
    if height:
        changes["height"] = height
    if weight:
        changes["weight"] = weight
    if run_goal:
        changes["run goal"] = run_goal
    if strength_goal:
        changes["strength goal"] = strength_goal

    if not changes:
        print("\nNo changes were made")
        return

    print("\n==========Review Your Changes==========")

    for field, new_value in changes.items():
        old_value = user[field] or "Not set"
        print(f"{field}: {old_value} -> {new_value}")

    print("\n\n[1] Save Changes")
    print("[2] Discard Changes")
    print("[0] Cancel and Exit")

    selection = input("Choose an option: ")

    if selection == "1":
        old_values = {
            "age": user["age"],
            "height": user["height"],
            "weight": user["weight"],
            "run goal": user["run goal"],
            "strength goal": user["strength goal"],
        }
        user["history"].append({
            "entries": old_values,
            "date": datetime.now().strftime("%Y-%m-%d")})
        user.update(changes)
        save_data()
        print("\nChanges Saved")

    elif selection == "2":
        print("\nChanges Discarded")

    elif selection == "0":
        print("\nReturning to Homepage")

    else:
        print("Invalid option, try again.")


# ============================================
# Historical Info

def historical_info(username):
    user = data["users"][username]
    history = user["history"]

    print("\n========Your Historical Information========")

    if not history:
        print("\nNo historical information saved")
        return

    index = 0

    while True:
        entry = history[index]

        print(f"\n==========Entry {index + 1}==========")
        print(f"Date: {entry['date']}")

        values = entry["entries"]

        print(f"\nAge: {values['age'] or 'Not set'}")
        print(f"\nHeight: {values['height'] or 'Not set'}")
        print(f"\nWeight: {values['weight'] or 'Not set'}")
        print(f"\nRun Goal: {values['run goal'] or 'Not set'}")
        print(f"\nStrength Goal: {values['strength goal'] or 'Not set'}")

        print("\n\n[1] Previous Entry")
        print("[2] Next Entry")
        print("[3] All Entries")
        print("[0] Return to User Profile")

        selection = input("Choose an option: ")

        if selection == "1":
            if index > 0:
                index -= 1
            else:
                print("\nNo previous entries")

        elif selection == "2":
            if index < len(history) - 1:
                index += 1
            else:
                print("\nNo further entries")

        elif selection == "3":
            for i, entry in enumerate(history):
                print(f"\n==========Entry {i + 1}==========")
                print(f"Date: {entry['date']}")

                all_values = entry["entries"]
                print(f"\nAge: {all_values['age'] or 'Not set'}")
                print(f"\nHeight: {all_values['height'] or 'Not set'}")
                print(f"\nWeight: {all_values['weight'] or 'Not set'}")
                print(f"\nRun Goal: {all_values['run goal'] or 'Not set'}")
                print(f"\nStrength Goal: {all_values['strength goal'] or 'Not set'}")

        elif selection == "0":
            print("\nReturning to User Profile")
            break

        else:
            print("\nInvalid option, try again")


# ============================================
# FAQ Page

def faq():
    while True:
        print("\n=====Fitness Tracker 1.0 FAQs======")

        print("\n1. This program lets you track your health a fitness goals.")
        print("2. This user profiles page displays your current metrics and fitness goals.")
        print("3. The update info page lets you update your metrics and fitness goals.")
        print("4. The historical info page lets you see all your previous entries.")

        print("\n[0] Return to the Previous Screen")
        selection = input("Choose an option: ")
        if selection == "0":
            break
        else:
            print("Invalid option, try again")


# ============================================
# Homepage

def home_page(username):
    while True:
        user = data["users"][username]

        print("\n==========Homepage======================")
        print(f"Welcome, {username}")

        print(f"\nAge: {user['age']}")
        print(f"Height: {user['height']}")
        print(f"Weight: {user['weight']}")
        print(f"Run Goal: {user['run goal']}")
        print(f"Strength Goal: {user['strength goal']}")

        print("\n\n[1] User Profile")
        print("[2] FAQ")
        print("[0] Logout")

        selection = input("Choose an option: ")

        if selection == "1":
            user_profile(username)
        elif selection == "2":
            faq()
        elif selection == "0":
            print("\nLogging Out")
            break
        else:
            print("Invalid option, try again")


# ======================================================
# Login Menu

def main_menu():
    while True:
        print("\n==========Fitness Tracker 1.0===========")
        print("\n[1] Login")
        print("[2] Create New User")
        print("[3] Forgot Password")
        print("[0] Exit")

        selection = input("Choose an option: ")

        if selection == "1":
            login()
        elif selection == "2":
            create_new_user()
        elif selection == "3":
            recover_password()
        elif selection == "0":
            print("\nThank you for using, goodbye")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main_menu()
