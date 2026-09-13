from pathlib import Path

from models.user import Admin
from models.users_login import School_Admin, Teacher_Admin, User
from utils.storage import load_json, save_json
from utils.validators import not_empty, valid_email


class AuthManager:
    def __init__(self, users_file="data/users.json"):
        self.users_file = Path(users_file)

    def register(self, name, email, password, role="user"):
        name = str(name).strip()
        email = str(email).strip().lower()
        role = str(role).strip().lower().replace(" ", "_")

        if not not_empty(name):
            raise ValueError("Name cannot be empty.")
        if not valid_email(email):
            raise ValueError("Please enter a valid email.")
        if len(password) < 4:
            raise ValueError("Password must have at least 4 characters.")
        if role not in {"student", "teacher_admin", "school_admin", "user", "admin"}:
            raise ValueError("Role must be student, teacher_admin, school_admin, user, or admin.")

        users = load_json(self.users_file)
        for saved_user in users:
            if str(saved_user.get("email", "")).lower() == email:
                raise ValueError("An account with that email already exists.")

        password_hash = User.hash_password(password)

        if role == "admin":
            user = Admin(name, email, password_hash, role="admin")
        elif role == "teacher_admin":
            user = Teacher_Admin(name, email, password_hash)
        elif role == "school_admin":
            user = School_Admin(name, email, password_hash)
        elif role == "student":
            user = User(name, email, password_hash, role="Student")
        else:
            user = User(name, email, password_hash, role="user")

        users.append(user.to_dict())
        save_json(self.users_file, users)
        return user

    def login(self, email, password):
        email = str(email).strip().lower()
        users = load_json(self.users_file)

        for saved_user in users:
            if str(saved_user.get("email", "")).lower() != email:
                continue

            role_name = str(saved_user.get("role", "user"))
            if role_name == "admin":
                user = Admin(saved_user["name"], saved_user["email"], saved_user["password_hash"], role="admin")
            elif role_name == "Teacher_Admin":
                user = Teacher_Admin(saved_user["name"], saved_user["email"], saved_user["password_hash"])
            elif role_name == "School_Admin":
                user = School_Admin(saved_user["name"], saved_user["email"], saved_user["password_hash"])
            elif role_name == "Student":
                user = User(saved_user["name"], saved_user["email"], saved_user["password_hash"], role="Student")
            else:
                user = User(saved_user["name"], saved_user["email"], saved_user["password_hash"], role=role_name or "user")

            if user.check_password(password):
                return user
            return None

        return None

