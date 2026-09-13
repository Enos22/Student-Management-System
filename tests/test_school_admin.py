import tempfile
import unittest
from pathlib import Path

from models.school_admin import SchoolAdmin
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

        school_admin_module.TEACHERS_FILE = str(self.teachers_file)
        school_admin_module.STUDENTS_FILE = str(self.students_file)
        school_admin_module.COURSES_FILE = str(self.courses_file)

        self.admin = SchoolAdmin("Kaitlyn", "kaitlyn@school.com")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_teacher_saves_teacher(self):
        teacher = {"id": 1, "name": "Mr. Otieno", "email": "otieno@school.com"}
        self.admin.add_teacher(teacher)
        teachers = school_admin_module.load_json(school_admin_module.TEACHERS_FILE)
        self.assertEqual(len(teachers), 1)
        self.assertEqual(teachers[0]["name"], "Mr. Otieno")

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