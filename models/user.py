from models.users_login import School_Admin, Teacher_Admin, User


class Admin(User):
    def __init__(self, name, email, password_hash, role="admin"):
        super().__init__(name, email, password_hash, role=role)
