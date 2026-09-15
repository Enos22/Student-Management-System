import json
import os

from utils.storage import load_json


class TeacherAdmin:
    admin_name = "Teacher Admin"
    log_actions = []

    def __init__(self, filename="data/students.json"):
        self.filename = filename
        self.students = []
        self.units = {}
        self.grades = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                self.students = data
            else:
                self.students = data.get("students", [])
                self.units = data.get("units", {})
                self.grades = data.get("grades", {})
        else:
            self.students = []
            self.save_data()

    def save_data(self):
        folder = os.path.dirname(self.filename)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.students, file, indent=4)

    def _registered_students(self):
        users = load_json("data/users.json")
        return [
            user for user in users
            if str(user.get("role", "")).strip().lower() == "student"
        ]

    def find_student(self, student_id):
        target = str(student_id).strip()
        if not target:
            return None

        for student in self.students:
            if str(student.get("id")) == target or str(student.get("name", "")).lower() == target.lower() or str(student.get("email", "")).lower() == target.lower():
                return student

        for user in self._registered_students():
            name = str(user.get("name", "")).strip()
            email = str(user.get("email", "")).strip().lower()
            if str(user.get("id")) == target or name.lower() == target.lower() or email == target.lower():
                return {
                    "id": user.get("id"),
                    "name": name,
                    "email": email,
                    "course": "General Studies",
                    "grade": "N/A",
                    "units": {},
                }

        return None

    def add_student(self, student_id, name, course, grade, units=None):
        # Teacher should not create user accounts — they can only add/update details
        target_id = str(student_id).strip()
        target_name = str(name).strip()

        if not target_id and not target_name:
            return "Provide student ID or name"

        # Try to find existing stored student to update
        for s in self.students:
            s_id = str(s.get("id", "")).strip()
            s_name = str(s.get("name", "")).strip().lower()
            s_email = str(s.get("email", "")).strip().lower()
            if (target_id and s_id == target_id) or (target_name and s_name == target_name.lower()) or (target_name and s_email == target_name.lower()):
                # update available fields
                if name:
                    s["name"] = name
                if course:
                    s["course"] = course
                if grade:
                    s["grade"] = grade
                if units is not None:
                    s["units"] = units
                TeacherAdmin.log_actions.append(f"Updated student {s.get('id')}")
                self.save_data()
                return "Student details updated successfully"

        # Not found in stored students; ensure the user is registered by school admin
        registered_user = None
        for user in self._registered_students():
            user_id = str(user.get("id", "")).strip()
            user_name = str(user.get("name", "")).strip().lower()
            user_email = str(user.get("email", "")).strip().lower()
            if (target_id and user_id == target_id) or (target_name and (user_name == target_name.lower() or user_email == target_name.lower())):
                registered_user = user
                break

        if not registered_user:
            return "Student must be registered by the school admin first."

        # create student details record using registered user's canonical data
        final_id = registered_user.get("id") if registered_user.get("id") is not None else (int(target_id) if target_id.isdigit() else target_id)
        student = {
            "id": int(final_id) if str(final_id).isdigit() else final_id,
            "name": registered_user.get("name") or target_name,
            "email": registered_user.get("email", ""),
            "course": course,
            "grade": grade,
            "units": units or {},
        }
        self.students.append(student)
        TeacherAdmin.log_actions.append(f"Added student {student.get('id')}")
        self.save_data()
        return "Student added successfully"

    def delete_student(self, student_id):
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        self.students = [item for item in self.students if str(item.get("id")) != str(student_id)]
        self.save_data()
        return "Student deleted successfully"

    def add_unit(self, student_id, unit_name, score):
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        student.setdefault("units", {})
        student["units"][unit_name] = score
        self.save_data()
        return "Unit added successfully"

    def delete_unit(self, unit_code):
        for student in self.students:
            student.setdefault("units", {})
            if unit_code in student["units"]:
                del student["units"][unit_code]
        self.save_data()
        return "Unit deleted successfully"

    def add_grade(self, student_id, unit_code, score, letter_grade):
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        student.setdefault("grades", {})
        student["grades"][unit_code] = {"score": score, "letter": letter_grade}
        self.save_data()
        return "Grade added successfully"

    def update_grade(self, student_id, unit_code, score=None, letter_grade=None):
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        if unit_code not in student.get("grades", {}):
            return "Grade not found"
        if score is not None:
            student["grades"][unit_code]["score"] = score
        if letter_grade is not None:
            student["grades"][unit_code]["letter"] = letter_grade
        self.save_data()
        return "Grade updated successfully"

    def delete_grade(self, student_id, unit_code):
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        if unit_code not in student.get("grades", {}):
            return "Grade not found"
        del student["grades"][unit_code]
        self.save_data()
        return "Grade deleted successfully"

    def display_student(self, student_id):
        student = self.find_student(student_id)
        if not student:
            return "Student not found"
        details = (
            f"Student ID: {student.get('id')}\n"
            f"Name: {student.get('name')}\n"
            f"Course: {student.get('course', 'General Studies')}\n"
            f"Grade: {student.get('grade', 'N/A')}\n"
            "\nUnits:\n"
        )
        units = student.get("units", {})
        if units:
            for unit_code, score in units.items():
                details += f"  - {unit_code}: {score}\n"
        else:
            details += "  No units available\n"
        return details
