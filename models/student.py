#from students.json, read the following:
            # view course
            # view grade
            # view Units
            # view classmates


from pathlib import Path
from utils.storage import load_json, save_json

class Student:  #read student details posted by admins!
    def __init__(self, name, course, grade, units):
        self.name = name
        self.course = course
        self.grade = grade
        self.units = units

          
    @classmethod

    def from_dict(cls, data):
        return cls(
        data["name"],
        data["course"],
        data["grade"],
        data["units"],
        )

    # def view_details(self):
    #     return {
    #     "name": self.name,
    #     "course": self.course,
    #     "grade" : self.grade, 
    #     "units" : self.units
    #     }        

class StudentDetails:
    def __init__(self, file_path = "data/students.json"):
        self.file_path = Path(file_path)
        self.students = self._load_students()

    def _load_students(self):
        try:
            data = load_json(self.file_path)
            return [Student.from_dict(item) for item in data]
        except FileExistsError:
            print(f"[Error] {self.file_path} not found, Check with your Teacher!")
            return []

    def view_student(self, name):
        for student in self.students:
            if student.name.lower() == name.lower():
                return student
            return None
        
    def view_classmates(self, student):

        return [ student.name for student in self.students if student.course.lower() == student.course.lower() and student.name.lower()!= student.name.lower()]
  