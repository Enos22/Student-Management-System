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

        # These dictionaries/lists will hold our student information
        self.students = []
        self.units = {}
        self.grades = {}

        # Load any existing information when the program starts
        self.load_data()

    def load_data(self):
        """Load student data from the JSON file."""

        # Check whether the data file already exists
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)

            # Support both the older list format and the newer format
            if isinstance(data, list):
                self.students = data
            else:
                self.students = data.get("students", [])
                self.units = data.get("units", {})
                self.grades = data.get("grades", {})

        else:
            # If there is no file yet, start with empty records
            self.students = []
            self.save_data()

    def save_data(self):
        # Save the current records to the JSON file.

        # Get the folder where the JSON file will be stored
        folder = os.path.dirname(self.filename)

        # Create the folder if it doesn't already exist
        if folder:
            os.makedirs(folder, exist_ok=True)

        # Write the student records to the JSON file
        with open(self.filename, "w") as file:
            json.dump(self.students, file, indent=4)

    def find_student(self, student_id):
        # Find a student using their ID.

        for student in self.students:
            if str(student["id"]) == str(student_id):
                return student

        # Return None when the student cannot be found
        return None

    def add_student(self, student_id, name, course, grade, units=None):
        # Add a new student to the system.

        # Don't allow two students to have the same ID
        if self.find_student(student_id):
            return "A student with that ID already exists"

        # Give the student an empty units dictionary if none was provided
        if units is None:
            units = {}

        student = {
            "id": student_id,
            "name": name,
            "course": course,
            "grade": grade,
            "units": units
        }

        # Add the new student to our list
        self.students.append(student)

        # Record the action
        TeacherAdmin.log_actions.append(
            f"Added student {student_id}"
        )

        # Save the updated information
        self.save_data()

        return "Student added successfully"

    def delete_student(self, student_id):
        # Delete a student and their related grades.

        student = self.find_student(student_id)

        if not student:
            return "Student not found"

        # Remove the student from the student list
        self.students.remove(student)

        # Find grades belonging to this student
        grade_ids = [
            grade_id
            for grade_id, grade in self.grades.items()
            if str(grade["student_id"]) == str(student_id)
        ]

        # Remove the student's grades
        for grade_id in grade_ids:
            del self.grades[grade_id]

        TeacherAdmin.log_actions.append(
            f"Deleted student {student_id}"
        )

        self.save_data()

        return "Student deleted successfully"

    def add_unit(self, student_id, unit_name, score):
        # Add a unit and score to a student's record.

        student = self.find_student(student_id)

        if not student:
            return "Student not found"

        # Make sure the student has a units dictionary
        student.setdefault("units", {})

        # Add the unit and its score
        student["units"][unit_name] = score

        self.save_data()

        return "Unit added successfully"

    def delete_unit(self, unit_code):
        #  a unit and remove its scores from students.

        if unit_code not in self.units:
            return "Unit not found"

        # Remove the unit from the main units dictionary
        del self.units[unit_code]

        # Remove the unit from each student's records
        for student in self.students:
            student.setdefault("units", {})
            student.setdefault("grades", {})

            if unit_code in student["units"]:
                del student["units"][unit_code]

            if unit_code in student["grades"]:
                del student["grades"][unit_code]

        # Find grades connected to this unit
        grade_ids = []

        for grade_id, grade in self.grades.items():
            if grade["unit_code"] == unit_code:
                grade_ids.append(grade_id)

        # Delete those grades
        for grade_id in grade_ids:
            del self.grades[grade_id]

        TeacherAdmin.log_actions.append(
            f"Deleted unit {unit_code}"
        )

        self.save_data()

        return "Unit deleted successfully"

    def update_unit(
        self,
        unit_code,
        unit_name=None,
        description=None
    ):
        """Update information about an existing unit."""

        if unit_code not in self.units:
            return "Unit not found"

        unit = self.units[unit_code]

        # Only update the values that were provided
        if unit_name is not None:
            unit["unit_name"] = unit_name

        if description is not None:
            unit["description"] = description

        TeacherAdmin.log_actions.append(
            f"Updated unit {unit_code}"
        )

        self.save_data()

        return "Unit updated successfully"

    def add_grade(self, student_id, unit_code, score, letter_grade):
        """Add a student's score and letter grade for a unit."""

        student = self.find_student(student_id)

        if not student:
            return "Student not found"

        if unit_code not in self.units:
            return "Unit not found"

        # Make sure the student has places to store units and grades
        student.setdefault("units", {})
        student.setdefault("grades", {})

        # Store the score and letter grade
        student["units"][unit_code] = score

        student["grades"][unit_code] = {
            "score": score,
            "letter": letter_grade
        }

        # Create a unique ID for this student's grade
        grade_id = f"{student_id}-{unit_code}"

        self.grades[grade_id] = {
            "student_id": student_id,
            "unit_code": unit_code,
            "score": score,
            "letter_grade": letter_grade
        }

        TeacherAdmin.log_actions.append(
            f"Added grade for {student_id} in {unit_code}"
        )

        self.save_data()
        return "Grade added successfully"

    def update_grade(self,student_id,unit_code,score=None,letter_grade=None):
        #Update an existing grade for a student.
        student = self.find_student(student_id)

        if not student:
            return "Student not found"

        if unit_code not in student.get("grades", {}):
            return "Grade not found"
        student_grade = student["grades"][unit_code]
        # Update the score if a new score was provided
        if score is not None:
            student_grade["score"] = score
            student["units"][unit_code] = score
        # Update the letter grade if a new one was provided
        if letter_grade is not None:
            student_grade["letter"] = letter_grade
        grade_id = f"{student_id}-{unit_code}"
        # Update the main grades dictionary as well
        if grade_id in self.grades:
            if score is not None:
                self.grades[grade_id]["score"] = score
            if letter_grade is not None:
                self.grades[grade_id]["letter_grade"] = letter_grade
        TeacherAdmin.log_actions.append(
            f"Updated grade for {student_id} in {unit_code}"
        )
        self.save_data()
        return "Grade updated successfully"

    def delete_grade(self, student_id, unit_code):
        """Remove a student's grade for a particular unit."""
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        if unit_code not in student.get("grades", {}):
            return "Grade not found"
        # Remove the grade from the student's record
        del student["grades"][unit_code]
        # Remove the score from the student's units
        if unit_code in student["units"]:
            del student["units"][unit_code]
        # Remove the grade from the main grades dictionary
        grade_id = f"{student_id}-{unit_code}"
        if grade_id in self.grades:
            del self.grades[grade_id]

        TeacherAdmin.log_actions.append(
            f"Deleted grade for {student_id} in {unit_code}"
        )
        self.save_data()
        return "Grade deleted successfully"

    def display_student(self, student_id):
        """Return a readable summary of a student's information."""
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        # Build the student's basic information
        details = (
            f"Student ID: {student['id']}\n"
            f"Name: {student['name']}\n"
            f"Course: {student['course']}\n"
            f"Grade: {student['grade']}\n"
            "\nUnits:\n"
        )

        # Display the student's units and scores
        if student["units"]:
            for unit_code, score in student["units"].items():
                details += f"  - {unit_code}: {score}\n"
        else:
            details += "  No units available\n"

        return details