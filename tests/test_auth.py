import tempfile
import unittest
from pathlib import Path

from models.user import Admin, User
from utils.auth import AuthManager


class AuthTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.users_file = Path(self.temp_dir.name) / "users.json"
        self.auth = AuthManager(self.users_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_password_is_hashed(self):
        hashed = User.hash_password("secret123")
        self.assertNotEqual(hashed, "secret123")
        self.assertEqual(len(hashed), 64)

    def test_register_creates_user(self):
        user = self.auth.register("Jane", "jane@example.com", "secret123", "user")
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "jane@example.com")
        self.assertEqual(user.role, "user")

    def test_register_creates_admin(self):
        user = self.auth.register("Admin", "admin@example.com", "secret123", "admin")
        self.assertIsInstance(user, Admin)
        self.assertEqual(user.role, "admin")

    def test_duplicate_email_is_rejected(self):
        self.auth.register("Jane", "jane@example.com", "secret123", "user")
        with self.assertRaises(ValueError):
            self.auth.register("Other", "jane@example.com", "password", "user")

    def test_invalid_email_is_rejected(self):
        with self.assertRaises(ValueError):
            self.auth.register("Jane", "not-an-email", "secret123", "user")

    def test_login_with_correct_password(self):
        self.auth.register("Jane", "jane@example.com", "secret123", "user")
        user = self.auth.login("jane@example.com", "secret123")
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Jane")

    def test_login_with_wrong_password_returns_none(self):
        self.auth.register("Jane", "jane@example.com", "secret123", "user")
        user = self.auth.login("jane@example.com", "wrong")
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()
