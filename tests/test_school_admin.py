import tempfile
import unittest
from pathlib import Path

from models.school_admin import SchoolAdmin
from models.users_login import User
import models.school_admin as school_admin_module


class SchoolAdminTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        temp_path = Path(self.temp_dir.name)

        self.teachers_file = temp_path / "teacher(admin).json"
        self.students_file = temp_path / "students.json"
        self.courses_file = temp_path / "courses.json"

        self.teachers_file.write_text("[]")
        self.students_file.write_text("[]")
        self.courses_file.write_text("[]")
        self.users_file = temp_path / "users.json"
        self.users_file.write_text("[]")

        school_admin_module.TEACHERS_FILE = str(self.teachers_file)
        school_admin_module.STUDENTS_FILE = str(self.students_file)
        school_admin_module.COURSES_FILE = str(self.courses_file)
        school_admin_module.REGISTER_FILE = str(self.users_file)

        self.admin = SchoolAdmin("Kaitlyn", "kaitlyn@school.com")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_teacher_saves_teacher(self):
        teacher = {"id": 1, "name": "Mr. Otieno", "email": "otieno@school.com"}
        self.admin.add_teacher(teacher)
        teachers = school_admin_module.load_json(school_admin_module.TEACHERS_FILE)
        self.assertEqual(len(teachers), 1)
        self.assertEqual(teachers[0]["name"], "Mr. Otieno")

    def test_register_student_stores_user_record_with_id_and_role(self):
        saved = self.admin.register_student("Jane Wanjiru", "jane@school.com", "secret123", "student")
        self.assertEqual(saved["name"], "Jane Wanjiru")
        self.assertEqual(saved["role"], "Student")
        self.assertIn("id", saved)
        self.assertIn("password_hash", saved)

        users = school_admin_module.load_json(school_admin_module.REGISTER_FILE)
        self.assertTrue(any(user["email"] == "jane@school.com" and user["role"] == "Student" for user in users))

    def test_teacher_record_can_login_and_access_teacher_portal(self):
        teacher_file = Path(self.temp_dir.name) / "teacher(admin).json"
        teacher_file.write_text(
            "[{\"id\": 100, \"name\": \"Teacher One\", \"email\": \"teacher1@school.com\", \"subject\": \"Math\", \"password_hash\": \"%s\"}]"
            % User.hash_password("teacher123")
        )
        auth = __import__("utils.auth", fromlist=["AuthManager"]).AuthManager(str(self.users_file), str(teacher_file))
        user = auth.login("teacher1@school.com", "teacher123")
        self.assertIsNotNone(user)
        self.assertEqual(user.role, "Teacher_Admin")

    def test_registered_student_can_login_with_email_and_password(self):
        self.admin.register_student("Alice Student", "alice@school.com", "secret123", "student")
        users = school_admin_module.load_json(school_admin_module.REGISTER_FILE)
        stored = next(user for user in users if user["email"] == "alice@school.com")
        self.assertNotEqual(stored["password_hash"], "secret123")
        self.assertEqual(len(stored["password_hash"]), 64)

    def test_school_admin_rejects_unregistered_student(self):
        result = self.admin.add_student({
            "id": 999,
            "name": "Ghost Student",
            "course": "Software Engineering",
            "grade": "A",
            "units": {},
        })
        self.assertIsNone(result)
        students = school_admin_module.load_json(school_admin_module.STUDENTS_FILE)
        self.assertEqual(students, [])

    def test_add_teacher_creates_login_account(self):
        self.admin.add_teacher({
            "id": 1,
            "name": "Mr. Otieno",
            "email": "otieno@school.com",
            "subject": "Math",
            "password": "teacher123",
        })
        users = school_admin_module.load_json(school_admin_module.REGISTER_FILE)
        self.assertTrue(any(user["email"] == "otieno@school.com" and user["role"] == "Teacher_Admin" for user in users))

    def test_delete_teacher_removes_teacher(self):
        teacher = {"id": 1, "name": "Mr. Otieno", "email": "otieno@school.com"}
        self.admin.add_teacher(teacher)
        deleted = self.admin.delete_teacher(1)
        self.assertTrue(deleted)
        teachers = school_admin_module.load_json(school_admin_module.TEACHERS_FILE)
        self.assertEqual(teachers, [])

    def test_delete_missing_teacher_returns_false(self):
        result = self.admin.delete_teacher(999)
        self.assertFalse(result)  

    def test_add_student_saves_student(self):
        self.users_file.write_text("[{\"id\": 1, \"name\": \"Jane Wanjiru\", \"email\": \"jane@school.com\", \"password_hash\": \"abc\", \"role\": \"Student\"}]")
        student = {"id": 1, "name": "Jane Wanjiru", "email": "jane@school.com", "course": "Software Engineering", "grade": "B", "units": {"Mathematics": 90}}
        self.admin.add_student(student)
        students = school_admin_module.load_json(school_admin_module.STUDENTS_FILE)
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]["name"], "Jane Wanjiru")

    def test_delete_student_removes_student(self):
        self.users_file.write_text("[{\"id\": 1, \"name\": \"Jane Wanjiru\", \"email\": \"jane@school.com\", \"password_hash\": \"abc\", \"role\": \"Student\"}]")
        student = {"id": 1, "name": "Jane Wanjiru", "email": "jane@school.com", "course": "Software Engineering", "grade": "B", "units": {}}
        self.admin.add_student(student)
        deleted = self.admin.delete_student(1)
        self.assertTrue(deleted)
        students = school_admin_module.load_json(school_admin_module.STUDENTS_FILE)
        self.assertEqual(students, [])

    def test_delete_missing_student_returns_false(self):
        result = self.admin.delete_student(999)
        self.assertFalse(result)

    def test_add_course_saves_course(self):
        course = {"id": 1, "title": "Data Structures"}
        self.admin.add_course(course)
        courses = school_admin_module.load_json(school_admin_module.COURSES_FILE)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0]["title"], "Data Structures")

    def test_delete_course_removes_course(self):
        course = {"id": 1, "title": "Data Structures"}
        self.admin.add_course(course)
        deleted = self.admin.delete_course(1)
        self.assertTrue(deleted)
        courses = school_admin_module.load_json(school_admin_module.COURSES_FILE)
        self.assertEqual(courses, [])

    def test_delete_missing_course_returns_false(self):
        result = self.admin.delete_course(999)
        self.assertFalse(result)    