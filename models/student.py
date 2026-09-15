from pathlib import Path

from utils.storage import load_json


class Student:
    def __init__(self, name, course="General Studies", grade="N/A", units=None, student_id=None, email=""):
        self.id = student_id
        self.name = str(name).strip() or "Unknown Student"
        self.email = str(email).strip().lower()
        self.course = course or "General Studies"
        self.grade = grade or "N/A"
        self.units = units or {}

    @classmethod
    def from_dict(cls, data):
        name = str(data.get("name", "Unknown Student")).strip()
        if name:
            name = " ".join(part.capitalize() for part in name.split())
        return cls(
            name=name or "Unknown Student",
            course=data.get("course", "General Studies"),
            grade=data.get("grade", "N/A"),
            units=data.get("units", {}),
            student_id=data.get("id"),
            email=data.get("email", ""),
        )

    def view_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "course": self.course,
            "grade": self.grade,
            "units": self.units,
        }


class StudentDetails:
    def __init__(self, file_path="data/students.json"):
        self.file_path = Path(file_path)
        self._loaded_from_registry = False
        self.students = self._load_students()

    def _load_students(self):
        data = load_json(self.file_path)
        if data:
            return [Student.from_dict(item) for item in data]

        self._loaded_from_registry = True
        users = load_json("data/users.json")
        registered_students = []
        for user in users:
            if str(user.get("role", "")).lower() == "student":
                registered_students.append(
                    Student.from_dict({
                        "id": user.get("id", 0),
                        "name": user.get("name", "Unknown Student"),
                        "email": user.get("email", ""),
                        "course": "General Studies",
                        "grade": "N/A",
                        "units": {},
                    })
                )
        return registered_students

    def view_student(self, search_value):
        if search_value is None:
            return None
        key = str(search_value).strip().lower()
        for student in self.students:
            if key in {student.name.lower(), student.email.lower(), str(student.id).lower()}:
                return student

        for user in load_json("data/users.json"):
            if str(user.get("role", "")).strip().lower() != "student":
                continue
            user_name = str(user.get("name", "")).strip()
            user_email = str(user.get("email", "")).strip().lower()
            if key in {user_name.lower(), user_email, str(user.get("id", "")).lower()}:
                return Student.from_dict({
                    "id": user.get("id", 0),
                    "name": user_name,
                    "email": user_email,
                    "course": "General Studies",
                    "grade": "N/A",
                    "units": {},
                })
        return None

    def view_classmates(self, current_student):
        if self._loaded_from_registry:
            return []
        return [
            student.name for student in self.students
            if student.course.lower() == current_student.course.lower() and student.name.lower() != current_student.name.lower()
        ]
