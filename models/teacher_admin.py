import json
import os

class TeacherAdmin:
    # Basic information about the administrator
    admin_name = "Teacher Admin"

    # Keep a simple record of actions performed during the session
    log_actions = []

    def __init__(self, filename="data/students.json"):
        # Store the location of our JSON data file
        self.filename = filename

        # These will hold student, unit, and grade information
        self.students = []
        self.units = {}
        self.grades = {}

        # Load any existing information when the program starts
        self.load_data()

    def load_data(self):
        """Load student data from the JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)

            # Handle both list-only format and dict format
            if isinstance(data, list):
                self.students = data
            else:
                self.students = data.get("students", [])
                self.units = data.get("units", {})
                self.grades = data.get("grades", {})
        else:
            # If no file exists, start fresh
            self.students = []
            self.units = {}
            self.grades = {}
            self.save_data()

    def save_data(self):
        """Save the current records to the JSON file."""
        folder = os.path.dirname(self.filename)
        if folder:
            os.makedirs(folder, exist_ok=True)

        # Save all data consistently (students, units, grades)
        data = {
            "students": self.students,
            "units": self.units,
            "grades": self.grades
        }

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def find_student(self, student_id):
        """Find a student using their ID."""
        for student in self.students:
            if str(student["id"]) == str(student_id):
                return student
        return None

    def add_student(self, student_id, name, course, grade, units=None):
        """Add a new student to the system."""
        if self.find_student(student_id):
            return "A student with that ID already exists"

        if units is None:
            units = {}

        student = {
            "id": student_id,
            "name": name,
            "course": course,
            "grade": grade,
            "units": units,
            "grades": {}  # keep grades separate
        }

        self.students.append(student)
        TeacherAdmin.log_actions.append(f"Added student {student_id} - {name}")
        self.save_data()
        return "Student added successfully"

    def delete_student(self, student_id):
        """Delete a student and their related grades."""
        student = self.find_student(student_id)
        if not student:
            return "Student not found"

        self.students.remove(student)

        # Remove grades linked to this student
        grade_ids = [
            grade_id for grade_id, grade in self.grades.items()
            if str(grade["student_id"]) == str(student_id)
        ]
        for grade_id in grade_ids:
            del self.grades[grade_id]

        TeacherAdmin.log_actions.append(f"Deleted student {student_id}")
        self.save_data()
        return "Student deleted successfully"

    def add_unit(self, student_id, unit_name, score):
        """Add a unit and score to a student's record."""
        student = self.find_student(student_id)
        if not student:
            return "Student not found"

        student.setdefault("units", {})
        student["units"][unit_name] = score

        # Also track globally
        self.units[unit_name] = {"unit_name": unit_name}

        self.save_data()
        return "Unit added successfully"

    def delete_unit(self, unit_code):
        """Delete a unit and remove its scores from students."""
        if unit_code not in self.units:
            return "Unit not found"

        del self.units[unit_code]

        for student in self.students:
            student.setdefault("units", {})
            student.setdefault("grades", {})
            student["units"].pop(unit_code, None)
            student["grades"].pop(unit_code, None)

        # Remove grades tied to this unit
        grade_ids = [gid for gid, grade in self.grades.items() if grade["unit_code"] == unit_code]
        for gid in grade_ids:
            del self.grades[gid]

        TeacherAdmin.log_actions.append(f"Deleted unit {unit_code}")
        self.save_data()
        return "Unit deleted successfully"

    def update_unit(self, unit_code, unit_name=None, description=None):
        """Update information about an existing unit."""
        if unit_code not in self.units:
            return "Unit not found"

        unit = self.units[unit_code]
        if unit_name is not None:
            unit["unit_name"] = unit_name
        if description is not None:
            unit["description"] = description

        TeacherAdmin.log_actions.append(f"Updated unit {unit_code}")
        self.save_data()
        return "Unit updated successfully"

    def add_grade(self, student_id, unit_code, score, letter_grade):
        """Add a student's score and letter grade for a unit."""
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        if unit_code not in self.units:
            return "Unit not found"

        student.setdefault("units", {})
        student.setdefault("grades", {})

        student["units"][unit_code] = score
        student["grades"][unit_code] = {"score": score, "letter": letter_grade}

        grade_id = f"{student_id}-{unit_code}"
        self.grades[grade_id] = {
            "student_id": student_id,
            "unit_code": unit_code,
            "score": score,
            "letter_grade": letter_grade
        }

        TeacherAdmin.log_actions.append(f"Added grade for {student_id} in {unit_code}")
        self.save_data()
        return "Grade added successfully"

    def update_grade(self, student_id, unit_code, score=None, letter_grade=None):
        """Update an existing grade for a student."""
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        if unit_code not in student.get("grades", {}):
            return "Grade not found"

        student_grade = student["grades"][unit_code]
        if score is not None:
            student_grade["score"] = score
            student["units"][unit_code] = score
        if letter_grade is not None:
            student_grade["letter"] = letter_grade

        grade_id = f"{student_id}-{unit_code}"
        if grade_id in self.grades:
            if score is not None:
                self.grades[grade_id]["score"] = score
            if letter_grade is not None:
                self.grades[grade_id]["letter_grade"] = letter_grade

        TeacherAdmin.log_actions.append(f"Updated grade for {student_id} in {unit_code}")
        self.save_data()
        return "Grade updated successfully"

    def delete_grade(self, student_id, unit_code):
        """Remove a student's grade for a particular unit."""
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        if unit_code not in student.get("grades", {}):
            return "Grade not found"

        student["grades"].pop(unit_code, None)
        student["units"].pop(unit_code, None)

        grade_id = f"{student_id}-{unit_code}"
        self.grades.pop(grade_id, None)

        TeacherAdmin.log_actions.append(f"Deleted grade for {student_id} in {unit_code}")
        self.save_data()
        return "Grade deleted successfully"

    def display_student(self, student_id):
        """Return a readable summary of a student's information."""
        student = self.find_student(student_id)
        if not student:
            return "Student not found"

        details = (
            f"Student ID: {student['id']}\n"
            f"Name: {student['name']}\n"
            f"Course: {student['course']}\n"
            f"Grade: {student['grade']}\n"
            "\nUnits:\n"
        )

        if student["units"]:
            for unit_code, score in student["units"].items():
                details += f"  - {unit_code}: {score}\n"
        else:
            details += "  No units available\n"

        return details
