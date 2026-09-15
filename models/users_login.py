import hashlib


class User:
    def __init__(self, name, email, password_hash, role="user"):
        self.name = name
        self.email = email
        self._password_hash = password_hash
        self.role = role

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        stored_value = str(self._password_hash or "").strip()
        candidate = str(password or "").strip()
        return stored_value == candidate or stored_value == self.hash_password(candidate)

    @property
    def password_hash(self):
        return self._password_hash

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password_hash": self._password_hash,
            "role": self.role,
        }


class Teacher_Admin(User):
    def __init__(self, name, email, password_hash):
        super().__init__(name, email, password_hash, role="Teacher_Admin")


class School_Admin(User):
    def __init__(self, name, email, password_hash):
        super().__init__(name, email, password_hash, role="School_Admin")
