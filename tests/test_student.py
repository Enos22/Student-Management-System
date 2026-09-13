import tempfile
import json
import sys
import os
from pathlib import Path
from models.student import StudentDetails, Student

# Sample data for testing - teacher adds students here
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

def create_temp_json(data):
    """Helper to create temp students.json for tests"""
    tmp = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    json.dump(data, tmp)
    tmp.close()
    return tmp.name

def test_load_students():
    file_path = create_temp_json(TEST_DATA)
    sd = StudentDetails(file_path)
    assert len(sd.students) == 3
    print("PASS: test_load_students")
    Path(file_path).unlink()

def test_view_student_found():
    file_path = create_temp_json(TEST_DATA)
    sd = StudentDetails(file_path)
    student = sd.view_student("Enos Arenga")
    assert student is not None
    assert student.name == "Enos Arenga"
    assert student.course == "Software Engineering"
    assert student.grade == "B"
    print("PASS: test_view_student_found")
    Path(file_path).unlink()

def test_view_student_case_insensitive():
    file_path = create_temp_json(TEST_DATA)
    sd = StudentDetails(file_path)
    student = sd.view_student("enos arenga") 
    assert student is not None
    assert student.name == "Enos Arenga"
    print("PASS: test_view_student_case_insensitive")
    Path(file_path).unlink()

def test_view_student_not_found():
    file_path = create_temp_json(TEST_DATA)
    sd = StudentDetails(file_path)
    student = sd.view_student("Unknown Student")
    assert student is None
    print("PASS: test_view_student_not_found")
    Path(file_path).unlink()

def test_view_classmates():
    file_path = create_temp_json(TEST_DATA)
    sd = StudentDetails(file_path)
    enos = sd.view_student("Enos Arenga")
    classmates = sd.view_classmates(enos)

    assert "James Orina" in classmates
    assert "Benson Kamau" not in classmates
    assert "Enos Arenga" not in classmates  
    print(f"PASS: test_view_classmates -> Found: {classmates}")
    Path(file_path).unlink()

def test_view_classmates_no_classmates():
    file_path = create_temp_json(TEST_DATA)
    sd = StudentDetails(file_path)
    john = sd.view_student("Benson Kamau")
    classmates = sd.view_classmates(john)
    assert len(classmates) == 0
    print("PASS: test_view_classmates_no_classmates")
    Path(file_path).unlink()

def test_units():
    file_path = create_temp_json(TEST_DATA)
    sd = StudentDetails(file_path)
    student = sd.view_student("Enos Arenga")
    assert "Math" in student.units
    assert student.units["Math"] == "300"
    print("PASS: test_units")
    Path(file_path).unlink()

if __name__ == "__main__":
    print("Running Student Tests...\n")
    test_load_students()
    test_view_student_found()
    test_view_student_case_insensitive()
    test_view_student_not_found()
    test_view_classmates()
    test_view_classmates_no_classmates()
    test_units()
    print("\nAll tests passed! Your main.py CLI is ready.")