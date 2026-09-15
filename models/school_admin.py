from models.users_login import User
from utils.storage import load_json, save_json

TEACHERS_FILE = "data/teacher(admin).json"
STUDENTS_FILE = "data/students.json"
COURSES_FILE = "data/courses.json"
REGISTER_FILE = "data/users.json"


class SchoolAdmin:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @staticmethod
    def _next_id(items):
        highest = 0
        for item in items:
            try:
                current_id = int(item.get("id", 0))
                if current_id > highest:
                    highest = current_id
            except (TypeError, ValueError):
                continue
        return highest + 1

    @staticmethod
    def _normalize_student_role(role):
        normalized = str(role).strip()
        if normalized.lower() in {"student", "students"}:
            return "Student"
        return "Student"

    @staticmethod
    def _registered_students():
        users = load_json(REGISTER_FILE)
        return [
            user for user in users
            if str(user.get("role", "")).strip().lower() == "student"
        ]

    @classmethod
    def _matches_registered_student(cls, student_data):
        if not isinstance(student_data, dict):
            return False

        target_id = str(student_data.get("id", "")).strip()
        target_name = str(student_data.get("name", "")).strip().lower()
        target_email = str(student_data.get("email", "")).strip().lower()

        for user in cls._registered_students():
            user_id = str(user.get("id", "")).strip()
            user_name = str(user.get("name", "")).strip().lower()
            user_email = str(user.get("email", "")).strip().lower()

            if (target_id and user_id and target_id == user_id) or (target_name and user_name and target_name == user_name) or (target_email and user_email and target_email == user_email):
                return True
        return False

    def add_teacher(self, teacher_data):
        teacher_data = dict(teacher_data)
        teacher_email = str(teacher_data.get("email", "")).strip().lower()
        teacher_name = str(teacher_data.get("name", "")).strip()
        password = teacher_data.get("password")

        teachers = load_json(TEACHERS_FILE)
        teachers.append({
            "id": teacher_data.get("id"),
            "name": teacher_name,
            "email": teacher_email,
            "subject": teacher_data.get("subject", ""),
        })
        save_json(TEACHERS_FILE, teachers)

        users = load_json(REGISTER_FILE)
        if not any(str(user.get("email", "")).strip().lower() == teacher_email for user in users):
            if not password:
                return teacher_data
            users.append({
                "name": teacher_name,
                "email": teacher_email,
                "password_hash": User.hash_password(str(password)),
                "role": "Teacher_Admin",
            })
            save_json(REGISTER_FILE, users)

        return teacher_data

    def delete_teacher(self, teacher_id):
        teachers = load_json(TEACHERS_FILE)
        for teacher in teachers:
            if teacher.get("id") == teacher_id:
                teachers.remove(teacher)
                save_json(TEACHERS_FILE, teachers)
                return True
        return False

    @staticmethod
    def _registered_student_matches(student_data):
        users = load_json(REGISTER_FILE)
        target_id = str(student_data.get("id", "")).strip()
        target_name = str(student_data.get("name", "")).strip().lower()
        target_email = str(student_data.get("email", "")).strip().lower()

        for user in users:
            if str(user.get("role", "")).strip().lower() != "student":
                continue
            user_id = str(user.get("id", "")).strip()
            user_name = str(user.get("name", "")).strip().lower()
            user_email = str(user.get("email", "")).strip().lower()
            if (target_id and user_id and target_id == user_id) or (target_name and user_name and target_name == user_name) or (target_email and user_email and target_email == user_email):
                return True
        return False

    def add_student(self, student_data):
        if not self._registered_student_matches(student_data):
            return None

        students = load_json(STUDENTS_FILE)
        student_id = student_data.get("id")
        if student_id is None:
            student_data["id"] = self._next_id(students)

        if not any(str(item.get("id")) == str(student_data["id"]) for item in students):
            students.append(student_data)
        else:
            for index, item in enumerate(students):
                if str(item.get("id")) == str(student_data["id"]):
                    students[index] = student_data
                    break

        save_json(STUDENTS_FILE, students)
        return student_data

    def delete_student(self, student_id):
        students = load_json(STUDENTS_FILE)
        for student in students:
            if student.get("id") == student_id:
                students.remove(student)
                save_json(STUDENTS_FILE, students)
                return True
        return False

    def register_student(self, name, email, password_hash, role="student", student_id=None):
        name = str(name).strip()
        email = str(email).strip().lower()
        raw_password = str(password_hash).strip()
        password_hash = raw_password
        if raw_password and len(raw_password) != 64:
            password_hash = User.hash_password(raw_password)
        role_name = self._normalize_student_role(role)

        users = load_json(REGISTER_FILE)
        if student_id is None:
            student_id = self._next_id(users)

        student = {
            "id": student_id,
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "role": role_name,
        }

        users.append(student)
        save_json(REGISTER_FILE, users)

        default_student_details = {
            "id": student_id,
            "name": name,
            "email": email,
            "course": "Software Engineering",
            "grade": "N/A",
            "units": {},
        }
        self.add_student(default_student_details)
        return student

    def add_course(self, course_data):
        courses = load_json(COURSES_FILE)
        courses.append(course_data)
        save_json(COURSES_FILE, courses)
        return course_data

    def delete_course(self, course_id):
        courses = load_json(COURSES_FILE)
        for course in courses:
            if course.get("id") == course_id:
                courses.remove(course)
                save_json(COURSES_FILE, courses)
                return True
        return False
