 ## import functions
from utils.storage import load_json, save_json

## fixed path strings written in caps to show this should not change
TEACHERS_FILE = "data/teacher(admin).json"
STUDENTS_FILE = "data/students.json"
COURSES_FILE = "data/courses.json"


## create blueprint (encapsulation)
class SchoolAdmin:
    def __init__(self, name, email):
        self.name = name
        self.email = email
   ## create methods
    def add_teacher(self, teacher_data): ## takes whole dictionary
        teachers = load_json(TEACHERS_FILE) ## calls imported function
        teachers.append(teacher_data) ## adds teacher
        save_json(TEACHERS_FILE, teachers) ## writes updated list into the file
        return teacher_data ## returns what was added

    def delete_teacher(self, teacher_id): ## takes only id
        teachers = load_json(TEACHERS_FILE)
        for t in teachers:  ## loops thru every teacher one at a time
            if t.get('id') == teacher_id:
                teachers.remove(t) ## removes it
                save_json(TEACHERS_FILE, teachers)
                return True
        return False ## if not found

    def add_student(self, student_data):
        students = load_json(STUDENTS_FILE)
        students.append(student_data)
        save_json(STUDENTS_FILE, students)
        return student_data

    def delete_student(self, student_id):
        students = load_json(STUDENTS_FILE)
        for s in students:
            if s.get('id') == student_id:
                students.remove(s)
                save_json(STUDENTS_FILE, students)
                return True
        return False


    def add_course(self, course_data):
        courses = load_json(COURSES_FILE)
        courses.append(course_data)
        save_json(COURSES_FILE, courses)
        return course_data

    def delete_course(self, course_id):
        courses = load_json(COURSES_FILE)
        for c in courses:
            if c.get('id') == course_id:
                courses.remove(c)
                save_json(COURSES_FILE, courses)
                return True
        return False