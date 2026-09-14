import tempfile  # creates a temporary throwaway folder for safe testing
import unittest  # Python's built-in testing framework (TestCase, assert methods)
from pathlib import Path  # clean way to build file paths, e.g. folder / "file.json"

from models.school_admin import SchoolAdmin  # imports the class itself, to create SchoolAdmin objects
import models.school_admin as school_admin_module  # imports the whole file as an object, so I can override its constants during tests


class SchoolAdminTests(unittest.TestCase):
    # inherits from TestCase so I get assertEqual/assertTrue etc for free

    def setUp(self):
        # runs before every test, sets up a clean fake environment

        self.temp_dir = tempfile.TemporaryDirectory()
        # creates a temporary folder that deletes itself later

        temp_path = Path(self.temp_dir.name)
        # wraps that folder's location so I can build file paths in it

        self.teachers_file = temp_path / "teacher(admin).json"
        self.students_file = temp_path / "students.json"
        self.courses_file = temp_path / "courses.json"
        # fake versions of my real data files, just for testing

        self.teachers_file.write_text("[]")
        self.students_file.write_text("[]")
        self.courses_file.write_text("[]")
        # start each file empty so every test begins the same way

        school_admin_module.TEACHERS_FILE = str(self.teachers_file)
        school_admin_module.STUDENTS_FILE = str(self.students_file)
        school_admin_module.COURSES_FILE = str(self.courses_file)
        # redirect school_admin.py's file paths to my fake ones
        # so tests never touch my real project data

        self.admin = SchoolAdmin("Kaitlyn", "kaitlyn@school.com")
        # a real SchoolAdmin, but now pointing at the fake files above

    def tearDown(self):
        # runs after every test, no matter pass or fail

        self.temp_dir.cleanup()
        # deletes the whole temp folder, nothing left behind

    def test_add_teacher_saves_teacher(self):
        # checks that adding a teacher actually saves it to the file

        teacher = {"id": 1, "name": "Mr. Otieno", "email": "otieno@school.com"}
        self.admin.add_teacher(teacher)

        teachers = school_admin_module.load_json(school_admin_module.TEACHERS_FILE)
        # read the file back myself, to prove it really got saved

        self.assertEqual(len(teachers), 1)  # exactly one teacher saved
        self.assertEqual(teachers[0]["name"], "Mr. Otieno")  # it's the right one

    def test_delete_teacher_removes_teacher(self):
        # checks that deleting a teacher actually removes it from the file

        teacher = {"id": 1, "name": "Mr. Otieno", "email": "otieno@school.com"}
        self.admin.add_teacher(teacher)  # add one first so there's something to delete

        deleted = self.admin.delete_teacher(1)
        self.assertTrue(deleted)  # confirms delete said "yes, I found and removed it"

        teachers = school_admin_module.load_json(school_admin_module.TEACHERS_FILE)
        self.assertEqual(teachers, [])  # file should be empty again

    def test_delete_missing_teacher_returns_false(self):
        # checks deleting an ID that was never added just returns False, no crash

        result = self.admin.delete_teacher(999)
        self.assertFalse(result)

    def test_add_student_saves_student(self):
        # same idea as add_teacher, just for students

        student = {"id": 1, "name": "Jane Wanjiru", "course": "Software Engineering", "grade": "B", "units": {"Mathematics": 90}}
        self.admin.add_student(student)

        students = school_admin_module.load_json(school_admin_module.STUDENTS_FILE)
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]["name"], "Jane Wanjiru")

    def test_delete_student_removes_student(self):
        # same idea as delete_teacher, just for students

        student = {"id": 1, "name": "Jane Wanjiru", "course": "Software Engineering", "grade": "B", "units": {}}
        self.admin.add_student(student)

        deleted = self.admin.delete_student(1)
        self.assertTrue(deleted)

        students = school_admin_module.load_json(school_admin_module.STUDENTS_FILE)
        self.assertEqual(students, [])

    def test_delete_missing_student_returns_false(self):
        # deleting a student ID that doesn't exist should just return False

        result = self.admin.delete_student(999)
        self.assertFalse(result)

    def test_add_course_saves_course(self):
        # same idea again, just for courses

        course = {"id": 1, "title": "Data Structures"}
        self.admin.add_course(course)

        courses = school_admin_module.load_json(school_admin_module.COURSES_FILE)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0]["title"], "Data Structures")

    def test_delete_course_removes_course(self):
        # same idea as delete_teacher/delete_student, just for courses

        course = {"id": 1, "title": "Data Structures"}
        self.admin.add_course(course)

        deleted = self.admin.delete_course(1)
        self.assertTrue(deleted)

        courses = school_admin_module.load_json(school_admin_module.COURSES_FILE)
        self.assertEqual(courses, [])

    def test_delete_missing_course_returns_false(self):
        # deleting a course ID that doesn't exist should just return False

        result = self.admin.delete_course(999)
        self.assertFalse(result)