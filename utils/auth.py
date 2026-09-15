from pathlib import Path
# Path helps build/manage file locations cleanly

from models.user import Admin
# brings in the Admin class 

from models.users_login import School_Admin, Teacher_Admin, User
# brings in the other role classes: School_Admin, Teacher_Admin, and the base User

from utils.storage import load_json, save_json
# functions for reading/writing JSON files

from utils.validators import not_empty, valid_email
#functions from validators.py, checking for blank text and valid email format


class AuthManager:
    # this class handles registering new users and logging existing ones in

    def __init__(self, users_file="data/users.json"):
        self.users_file = Path(users_file)
        # stores the file path where all registered users are saved

    def register(self, name, email, password, role="user", student_id=None):
        # creates a brand new user account

        name = str(name).strip()
        # str() makes sure it's text, .strip() removes extra spaces

        email = str(email).strip().lower()
        # same as above, plus .lower() so emails aren't case-sensitive
        # (Jane@x.com and jane@x.com should count as the same email)

        role = str(role).strip().lower().replace(" ", "_")
        # cleans role text too, and turns spaces into underscores
        # so "school admin" becomes "school_admin"

        if not not_empty(name):
            raise ValueError("Name cannot be empty.")
        # not_empty checks the name has real content
        # "not not_empty(name)" means "if the name IS empty"
        # raise stops the function immediately and sends this error upward

        if not valid_email(email):
            raise ValueError("Please enter a valid email.")
        # same idea, using my valid_email check (needs @ and a . in the domain)

        if len(password) < 4:
            raise ValueError("Password must have at least 4 characters.")
        # len() counts how many characters are in the password
        # rejects anything shorter than 4 characters

        if role not in {"student", "teacher_admin", "school_admin", "user", "admin"}:
            raise ValueError("Role must be student, teacher_admin, school_admin, user, or admin.")
        # {...} here is a set of allowed roles
        # if the role isn't one of these 5, reject it

        if role == "student" and (student_id is None or str(student_id).strip() == ""):
            raise ValueError("Student ID is required for student registration.")
        # NEW: students must provide a student_id (given to them by their teacher)
        # so we can later link their account to their actual student record

        users = load_json(self.users_file)
        # loads the list of everyone already registered

        for saved_user in users:
            if str(saved_user.get("email", "")).lower() == email:
                raise ValueError("An account with that email already exists.")
        # .get("email", "") safely grabs the email, or "" if missing (no crash)
        # loops through every saved user checking if this email is already taken

        password_hash = User.hash_password(password)
        # scrambles the password into a hash before it ever touches the file
        # so real passwords are never stored in plain text

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
        # builds the correct type of user object depending on their chosen role
        
        users.append(user.to_dict())
        # to_dict() turns the user object into a plain dictionary, ready for JSON
        # adds it onto the end of the existing users list

        save_json(self.users_file, users)
        # writes the whole updated list back into data/users.json

        return user
        # hands back the newly created user object

    def login(self, email, password):
        # checks if an email + password combo matches a real saved account

        email = str(email).strip().lower()
        # clean the typed email the same way as during registration

        users = load_json(self.users_file)
        # load everyone who's registered

        for saved_user in users:
            if str(saved_user.get("email", "")).lower() != email:
                continue
            # if this saved user's email doesn't match, skip to the next one

            role_name = str(saved_user.get("role", "user"))
            # safely grab this saved user's role, defaulting to "user" if missing

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
            # rebuilds the matching type of user object from the saved data

            if user.check_password(password):
                return user
            # check_password re-hashes the typed password and compares it
            # to the stored hash - never compares plain text directly
            # if it matches, return the real logged-in user

            return None
            # email matched, but the password was wrong

        return None
        # no saved user had this email at all