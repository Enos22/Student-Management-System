import tempfile
import json
import unittest
from pathlib import Path
from models.student import StudentDetails, Student

TEST_DATA = [
    {
        "name": "Enos Arenga",
        "course": "Software Engineering",
        "grade": "B",
        "units": {"Math": "300", "English": "250", "Kiswahili": "400"}
    },
    {
        "name": "James Orina",
        "course": "Software Engineering",
        "grade": "A",
        "units": {"Math": "350", "English": "300", "Kiswahili": "380"}
    },
    {
        "name": "Benson Kamau",
        "course": "Data Science",
        "grade": "C",
        "units": {"Python": "280", "Stats": "310"}
    }
]

def create_temp_json(data=TEST_DATA):
    tmp = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    json.dump(data, tmp)
    tmp.close()
    return tmp.name

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.file_path = create_temp_json()
        self.sd = StudentDetails(self.file_path)

    def tearDown(self):
        try:
            Path(self.file_path).unlink()
        except:
            pass

    def test_load_students(self):
        self.assertEqual(len(self.sd.students), 3)

    def test_view_student_found(self):
        student = self.sd.view_student("Enos Arenga")
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Enos Arenga")
        self.assertEqual(student.course, "Software Engineering")

    def test_view_student_case_insensitive(self):
        student = self.sd.view_student("enos arenga")
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Enos Arenga")

    def test_view_student_not_found(self):
        student = self.sd.view_student("Unknown Student")
        self.assertIsNone(student)

    def test_view_classmates(self):
        enos = self.sd.view_student("Enos Arenga")
        classmates = self.sd.view_classmates(enos)
        self.assertIn("James Orina", classmates)
        self.assertNotIn("Benson Kamau", classmates)
        self.assertNotIn("Enos Arenga", classmates)

    def test_view_classmates_no_classmates(self):
        benson = self.sd.view_student("Benson Kamau")
        classmates = self.sd.view_classmates(benson)
        self.assertEqual(len(classmates), 0)

    def test_units(self):
        student = self.sd.view_student("Enos Arenga")
        self.assertIn("Math", student.units)
        self.assertEqual(student.units["Math"], "300")

if __name__ == "__main__":
    unittest.main()