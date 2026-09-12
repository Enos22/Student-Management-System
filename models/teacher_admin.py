import json
import os


class TeacherAdmin:

    # These are shared by all TeacherAdmin objects
    admin_name = "Teacher Admin"
    log_actions = []

    def __init__(self, filename="data/students.json"):
        # Where our data will be stored
        self.filename = filename

        # Dictionaries for storing students, units and grades
        self.students = {}
        self.units = {}
        self.grades = {}

        #load saved records from the JSON file
        self.load_data()

    # JSON PERSISTENCE

    def load_data(self):
        # Load students, units and grades from the JSON file.

        if os.path.exists(self.filename):

            with open(self.filename, "r") as file:
                data = json.load(file)

            self.students = data.get("students",{})
            self.units = data.get("units",{})
            self.grades = data.get("grades",{})

        else:
            # If the file does not exist,
            # create it with empty data.
            self.students = {}
            self.units = {}
            self.grades = {}
            self.save_data()

    def save_data(self):  
        # Save all our data into the JSON file.
        data = {
            "students": self.students,
            "units": self.units,
            "grades": self.grades
        }

        # Make sure the data folder exists
        folder = os.path.dirname(self.filename)

        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    # STUDENT OPERATIONS

    def add_student(self, student_id, name, course, grade, units):
        
        #Add a student :
       
        self.students[student_id] = {
            "name": name,
            "course": course,
            "grade": grade,
            "units": units
        }
        self.save_data()

    # UNIT OPERATIONS

    def add_unit(
        self,
        unit_code,
        unit_name,
        description,
        credit_hours=3
    ):
       
        # Add a new unit to the system.
       

        self.units[unit_code] = {
            "unit_name": unit_name,
            "description": description,
            "credit_hours": credit_hours
        }

        TeacherAdmin.log_actions.append(
            f"Added unit {unit_code}"
        )

        self.save_data()

    def delete_unit(self, unit_code):
        """
        Delete a unit from the system.
        We also remove the unit from students
        and remove any grades belonging to that unit.
        """

        # First check whether the unit exists
        if unit_code not in self.units:
            return "Unit not found"

        # Delete the unit
        del self.units[unit_code]

        # Remove the unit from every student
        for student in self.students.values():

            if unit_code in student["units"]:
                del student["units"][unit_code] 

            # Remove the grade for this unit
            if unit_code in student["grades"]:
             del student["grades"][unit_code]

        # Remove the unit from the main grades dictionary
        grades_to_delete = []
        for grade_id, grade in self.grades.items():
            if grade["unit_code"] == unit_code:
                grades_to_delete.append(grade_id)

        for grade_id in grades_to_delete:
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
        description=None,
        credit_hours=None
    ):
        """
        Update information about an existing unit.
        """

        if unit_code not in self.units:
            return "Unit not found"

        unit = self.units[unit_code]

        # Only change values that were provided
        if unit_name is not None:
            unit["unit_name"] = unit_name

        if description is not None:
            unit["description"] = description

        if credit_hours is not None:
            unit["credit_hours"] = credit_hours

        TeacherAdmin.log_actions.append(
            f"Updated unit {unit_code}"
        )

        self.save_data()

        return "Unit updated successfully"

    # GRADE OPERATIONS

    def add_grade(self, student_id, unit_code, score, letter):
      if student_id not in self.students:
        return "Student not found"
      if unit_code not in self.units:
        return "Unit not found"

    # record score in units dict
      self.students[student_id]["units"][unit_code] = score

    # record grade details
      self.students[student_id].setdefault("grades", {})
      self.students[student_id]["grades"][unit_code] = {"score": score, "letter": letter}

    # also save in main grades dict
      self.grades[f"{student_id}-{unit_code}"] = {
        "student_id": student_id,
        "unit_code": unit_code,
        "score": score,
        "letter_grade": letter
    }

      self.save_data()
      return "Grade added successfully"

    def update_grade(
        self,
        student_id,
        unit_code,
        score=None,
        letter_grade=None
    ):
        """
        Update an existing student grade.
        """

        # Check student
        if student_id not in self.students:
            return "Student not found"

        # Check grade
        if unit_code not in self.students[student_id]["grades"]:
            return "Grade not found"

        student_grade = self.students[student_id]["grades"][unit_code]

        # Update score if a new score was provided
        if score is not None:
            student_grade["score"] = score

        # Update letter grade if provided
        if letter_grade is not None:
            student_grade["letter"] = letter_grade

        # Update the main grades dictionary too
        grade_id = f"{student_id}-{unit_code}"

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
        """
        Delete a student's grade for a particular unit.
        """

        # Check student
        if student_id not in self.students:
            return "Student not found"

        # Check grade
        if unit_code not in self.students[student_id]["grades"]:
            return "Grade not found"

        # Delete grade from student's records
        del self.students[student_id]["grades"][unit_code]

        # Delete grade from main grades dictionary
        grade_id = f"{student_id}-{unit_code}"

        if grade_id in self.grades:
            del self.grades[grade_id]

        TeacherAdmin.log_actions.append(
            f"Deleted grade for {student_id} in {unit_code}"
        )

        self.save_data()

        return "Grade deleted successfully"

    # DISPLAY STUDENT
    def display_student(self, student_id):
        student = self.students.get(student_id)

        if not student:
          return "Student not found"

        details = ""
        details += f"Student ID: {student_id}\n"
        details += f"Name: {student['name']}\n"
        details += f"Course: {student['course']}\n"
        details += f"Grade: {student['grade']}\n"

        details += "\nUnits:\n"
        if student["units"]:
           for unit, score in student["units"].items():
            details += f"  - {unit}: {score}\n"
        else:
             details += "  No units available\n"

        return details
 