
from models.teacher_admin import TeacherAdmin


def run_tests():
    admin = TeacherAdmin("data/test_students.json")

    admin.add_student( "S002","Brian","Software Engineering","B",{})
    admin.add_unit("S002", "Mathematics", 90)
    admin.add_unit("S002", "English", 85)
    admin.display_student("S002")
      # Update Mathematics by adding it again with a new score.
    admin.add_unit("S002", "Mathematics", 95)
    admin.display_student("S002")
    admin.delete_student("S002")
      # This should now display: Student not found
    admin.display_student("S002")
    
if __name__=="__main__":
   try:
       run_tests()
       print("All tests passed")
   except Exception as e:
       print("Test failed:", e)