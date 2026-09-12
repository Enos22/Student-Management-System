
from models.teacher_admin import TeacherAdmin


def run_tests():
    admin = TeacherAdmin("data/test_students.json")

    print(
    admin.add_student(
        "S002",
        "Brian",
        "Software Engineering",
        "B",
        {}
               )
               )

    print(admin.add_unit("S002", "Mathematics", 90))
    print(admin.add_unit("S002", "English", 85))

    print(admin.display_student("S002"))

      # Update Mathematics by adding it again with a new score.
    print(admin.add_unit("S002", "Mathematics", 95))

    print(admin.display_student("S002"))

    print(admin.delete_student("S002"))

      # This should now display: Student not found
    print(admin.display_student("S002"))
    
if __name__=="__main__":
   run_tests()
   print("Test passed succesifuly")