from colorama import Fore, Style, init

from models.school_admin import SchoolAdmin
from models.student import StudentDetails
from models.teacher_admin import TeacherAdmin
from models.users_login import User
from utils.storage import load_json

init(autoreset=True)


def normalize_student_ids(student_store):
    raw_students = load_json(student_store.file_path)
    for index, student in enumerate(student_store.students):
        raw_student = raw_students[index] if index < len(raw_students) else {}
        student.id = raw_student.get("id", getattr(student, "id", str(index + 1)))
    return student_store


class SchoolCLI:
    def __init__(self, users_file="data/users.json", students_file="data/students.json"):
        from utils.auth import AuthManager

        self.auth = AuthManager(users_file)
        self.student_store = normalize_student_ids(StudentDetails(students_file))
        self.current_user = None
        self.teacher_admin = TeacherAdmin()
        self.school_admin = SchoolAdmin("Kaitlyn", "kaitlyn@school.com")

    def run(self):
        print("\nSCHOOL STUDENT MANAGEMENT SYSTEM")
        while True:
            if self.current_user is None:
                self.guest_menu()
            else:
                self.user_menu()

    def guest_menu(self):
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        option = input("Choose an option: ").strip()
        if option == "1":
            self.register()
        elif option == "2":
            self.login()
        elif option == "3":
            print("Exiting.....")
            raise SystemExit
        else:
            print("Enter Valid Option: (1,2 or 3.)")

    def register(self):
        print("\nEnter Your Registration details Below:")
        name = input("Full name: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        role = input("Role (teacher_admin/school_admin): ").strip().lower()

        if role not in {"teacher_admin", "school_admin"}:
            print("Only teacher_admin and school_admin can register accounts. Students are added by the school admin.")
            return

        try:
            self.current_user = self.auth.register(name, email, password, role)
            print(f"Registered {self.current_user.name} as {self.current_user.role}.")
        except ValueError as exc:
            print(exc)

    def login(self):
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        user = self.auth.login(email, password)
        if user is None:
            print("Invalid email or password.")
            return

        self.current_user = user
        print(f"Welcome, {self.current_user.name}!")

        if self.current_user.role == "Teacher_Admin":
            self.teacher_admin_portal()
        elif self.current_user.role == "School_Admin":
            self.school_admin_portal()
        else:
            self.student_portal()

    def user_menu(self):
        if self.current_user is None:
            return

        print(f"\nWelcome, {self.current_user.name} ({self.current_user.role})")

        if self.current_user.role == "Student":
            self.student_portal()
        elif self.current_user.role == "Teacher_Admin":
            self.teacher_admin_portal()
        elif self.current_user.role == "School_Admin":
            self.school_admin_portal()
        else:
            print("Invalid role detected.")
            self.current_user = None

    def student_portal(self):
        current_student = self.student_store.view_student(self.current_user.email) or self.student_store.view_student(self.current_user.name)
        if current_student is None:
            print(f"Dear '{self.current_user.name}' Your Details Could not be Found! Contact your Teacher.")
            self.current_user = None
            return

        while True:
            self.student_menu()
            choice = input("Choose option (1-6): ").strip()
            if choice == "1":
                print(
                    f"\nID : {current_student.id}\nName: {current_student.name}\nCourse: {current_student.course}\nGrade: {current_student.grade}\nUnits: {current_student.units}"
                )
            elif choice == "2":
                print(f"\nCourse: {current_student.course}")
            elif choice == "3":
                print(f"\nGrade: {current_student.grade}")
            elif choice == "4":
                print("\n----Units and Marks ---")
                for unit, mark in current_student.units.items():
                    print(f"{unit}: {mark}")
            elif choice == "5":
                classmates = self.student_store.view_classmates(current_student)
                if classmates:
                    print(f"Your classmates in {current_student.course}: {', '.join(classmates)}")
                else:
                    print(f"\nYour are The Only one Doing {current_student.course} currently!. Others will join you!")
            elif choice == "6":
                print("Exiting...")
                self.current_user = None
                break
            else:
                print("You entered INVALID CHOICE, Use 1-6.")

    @staticmethod
    def student_menu():
        print("\n ========= STUDENT PORTAL ============")
        print("1. View my Full Details")
        print("2. View my Course")
        print("3. View my Grade")
        print("4. View my Units")
        print("5. View my Classmates")
        print("6. Exit")

    def teacher_admin_portal(self):
        while True:
            print(Fore.YELLOW + "\n--- Teacher Admin Menu ---")
            print(Fore.BLUE + "1. View student")
            print(Fore.GREEN + "2. Add student")
            print(Fore.LIGHTRED_EX + "3. Add unit")
            print(Fore.CYAN + "4. Add grade")
            print(Fore.LIGHTMAGENTA_EX + "5. Update grade")
            print(Fore.MAGENTA + "6. Delete grade")
            print(Fore.RED + "7. Delete unit")
            print(Fore.RED + "8. Delete student")
            print(Fore.RED + "9. Exit")

            choice = input(Style.RESET_ALL + "Choose an option: ").strip()

            if choice == "1":
                student_id = input("Enter student ID, name or email: ").strip()
                print(self.teacher_admin.display_student(student_id))
            elif choice == "2":
                student_id = input("Student ID: ").strip()
                name = input("Name: ").strip()
                course = input("Course: ").strip()
                grade = input("Grade: ").strip()
                print(self.teacher_admin.add_student(student_id, name, course, grade))
            elif choice == "3":
                student_id = input("Student ID: ").strip()
                unit_name = input("Unit name: ").strip()
                try:
                    score = int(input("Score: ").strip())
                except ValueError:
                    print(Fore.RED + "Score must be a number.")
                    continue
                print(self.teacher_admin.add_unit(student_id, unit_name, score))
            elif choice == "4":
                student_id = input("Student ID: ").strip()
                code = input("Unit code: ").strip()
                try:
                    score = int(input("Score: ").strip())
                except ValueError:
                    print(Fore.RED + "Score must be a number.")
                    continue
                letter = input("Letter grade: ").strip().upper()
                print(self.teacher_admin.add_grade(student_id, code, score, letter))
            elif choice == "5":
                student_id = input("Student ID: ").strip()
                code = input("Unit code: ").strip()
                try:
                    score = int(input("New score: ").strip())
                except ValueError:
                    print(Fore.RED + "Score must be a number.")
                    continue
                letter = input("New letter grade: ").strip().upper()
                print(self.teacher_admin.update_grade(student_id, code, score, letter))
            elif choice == "6":
                student_id = input("Student ID: ").strip()
                code = input("Unit code: ").strip()
                print(self.teacher_admin.delete_grade(student_id, code))
            elif choice == "7":
                code = input("Unit code: ").strip()
                print(self.teacher_admin.delete_unit(code))
            elif choice == "8":
                student_id = input("Student ID to delete: ").strip()
                print(self.teacher_admin.delete_student(student_id))
            elif choice == "9":
                print(Fore.YELLOW + "Goodbye!")
                self.current_user = None
                break
            else:
                print(Fore.RED + "Invalid option.")

    def school_admin_portal(self):
        while True:
            print("\n--- School Admin Menu ---")
            print("1. Add Teacher")
            print("2. Delete Teacher")
            print("3. Add Student")
            print("4. Delete Student")
            print("5. Add Course")
            print("6. Delete Course")
            print("7. Register student")
            print("8. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                teacher_id = self.read_id("Teacher ID: ")
                name = input("Teacher name: ")
                email = input("Teacher email: ")
                subject = input("Subject: ")
                password = input("Teacher password: ")
                if not self.is_non_empty(name):
                    print("Name cannot be empty.")
                elif not self.is_valid_email(email):
                    print("This email is not valid.")
                elif not self.is_non_empty(subject):
                    print("Subject cannot be empty.")
                elif len(password) < 4:
                    print("Teacher password must have at least 4 characters.")
                else:
                    self.school_admin.add_teacher({"id": teacher_id, "name": name, "email": email, "subject": subject, "password": password})
                    print("Teacher added and login access created.")
            elif choice == "2":
                teacher_id = self.read_id("Teacher ID to delete: ")
                deleted = self.school_admin.delete_teacher(teacher_id)
                print("Deleted." if deleted else "No teacher found with that ID.")
            elif choice == "3":
                student_id = self.read_id("Student ID: ")
                name = input("Student name: ")
                course = input("Course: ")
                grade = input("Overall grade: ")
                if not self.is_non_empty(name):
                    print("Name cannot be empty.")
                elif not self.is_non_empty(course):
                    print("Course cannot be empty.")
                elif not self.is_non_empty(grade):
                    print("Grade cannot be empty.")
                else:
                    units = self.read_units()
                    self.school_admin.add_student({
                        "id": student_id,
                        "name": name,
                        "course": course,
                        "grade": grade,
                        "units": units,
                    })
                    print("Student added.")
            elif choice == "4":
                student_id = self.read_id("Student ID to delete: ")
                deleted = self.school_admin.delete_student(student_id)
                print("Deleted." if deleted else "No student found with that ID.")
            elif choice == "5":
                course_id = self.read_id("Course ID: ")
                title = input("Course title: ")
                if not self.is_non_empty(title):
                    print("Course title cannot be empty.")
                else:
                    self.school_admin.add_course({"id": course_id, "title": title})
                    print("Course added.")
            elif choice == "6":
                course_id = self.read_id("Course ID to delete: ")
                deleted = self.school_admin.delete_course(course_id)
                print("Deleted." if deleted else "No course found with that ID.")
            elif choice == "7":
                print("\n--- Register New Student ---")
                student_id = self.read_id("Enter student ID: ")
                name = input("Enter student name: ").strip()
                email = input("Enter student email: ").strip()
                password = input("Enter student password: ").strip()
                if not name or not email or not password:
                    print("Student name, email and password are required.")
                    continue
                password_hash = User.hash_password(password)
                student = self.school_admin.register_student(name, email, password_hash, "student", student_id=student_id)
                print(f"Student {student['name']} registered successfully!")
            elif choice == "8":
                print("Goodbye!")
                self.current_user = None
                break
            else:
                print("Invalid option, try again.")

    @staticmethod
    def is_valid_email(email):
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def is_non_empty(text):
        return text.strip() != ""

    @staticmethod
    def read_id(prompt):
        while True:
            value = input(prompt)
            if value.isdigit():
                return int(value)
            print("That ID must be a whole number. Try again.")

    @staticmethod
    def read_units():
        units = {}
        print("Now enter units. Leave the unit name blank when done.")
        while True:
            unit_name = input("Unit name: ")
            if unit_name == "":
                break
            mark = SchoolCLI.read_id(f"Mark for {unit_name}: ")
            units[unit_name] = mark
        return units


def main():
    sd = normalize_student_ids(StudentDetails())
    if not sd.students:
        print("Your Details could not be found! Contact your Teacher")
        return

    student_name = input("Enter your names: ").strip()
    current_student = sd.view_student(student_name)
    if not current_student:
        print(f"Dear'{student_name}' Your Details Could not be Found! Contact your Teacher.")
        return

    print(f"Welcome, {current_student.name}!")
    while True:
        SchoolCLI.student_menu()
        choice = str(input("Choose option (1-6): ")).strip()
        if choice == "1":
            print(f"\nID : {current_student.id}\nName: {current_student.name}\nCourse: {current_student.course}\nGrade: {current_student.grade}\nUnits: {current_student.units}")
        elif choice == "2":
            print(f"\nCourse: {current_student.course}")
        elif choice == "3":
            print(f"\nGrade: {current_student.grade}")
        elif choice == "4":
            print("\n----Units and Marks ---")
            for unit, mark in current_student.units.items():
                print(f"{unit}: {mark}")
        elif choice == "5":
            classmates = sd.view_classmates(current_student)
            if classmates:
                print(f"Your classmates in {current_student.course}: {', '.join(classmates)}")
            else:
                print(f"\nYour are The Only one Doing {current_student.course} currently!. Others will join you!")
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("You entered INVALID CHOICE, Use 1-6.")


if __name__ == "__main__":
    SchoolCLI().run()
