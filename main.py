from models.student import StudentDetails
from utils.auth import AuthManager


class SchoolCLI:
    def __init__(self, users_file="data/users.json", students_file="data/students.json"):
        self.auth = AuthManager(users_file)
        self.student_store = StudentDetails(students_file)
        self.current_user = None

    def run(self):
        print("\nSCHOOL STUDENT MANAGEMENT SYSTEM")

        while True:
            if self.current_user is None:
                self.guest_menu()
            else:
                self.user_menu()

    def guest_menu(self):
        print("\n1. Register (ADMIN ONLY)")
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
        role = input("Role (teacher_admin/school_admin): ").strip()

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

        if self.current_user.role == "Teacher_Admin" or self.current_user.role == "School_Admin":
            print("Admin portal is still under progress.")
            self.current_user = None
            return

        self.student_portal()

    def user_menu(self):
        if self.current_user is None:
            return

        print(f"\nWelcome, {self.current_user.name} ({self.current_user.role})")
        if self.current_user.role == "Student":
            self.student_portal()
        else:
            print("Admin portal is still under progress.")
            self.current_user = None

    def student_portal(self):
        if not self.student_store.students:
            print("Your Details could not be found! Contact your Teacher")
            self.current_user = None
            return

        current_student = self.student_store.view_student(self.current_user.name)
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


def main():
    sd = StudentDetails()
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
