from utils.storage import load_json, save_json

TEACHERS_FILE= "data/teacher(admin).json"
STUDENTS_FILE = "data/students.json"

class SchoolAdmin:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def add_teacher(self, teacher_data):
        teacher= load_json(TEACHERS_FILE)
        teacher.append(teacher_data)
        save_json(TEACHERS_FILE, teacher)
        return teacher_data

    def delete_teacher(self, teacher_id):
        teachers = load_json(TEACHERS_FILE)
        for t in teachers:
            if t.get('id') == teacher_id:
                 teachers.remove(t)
                 save_json(TEACHERS_FILE, teachers)
                 return True
        return False

    def add_student(self, student_data):
        students = load_json(STUDENTS_FILE)
        students.append(student_data)
        save_json(STUDENTS_FILE, students)
        return student_data