from colorama import Fore, Style, init
from models.teacher_admin import TeacherAdmin


init(autoreset=True)


class AdminCLI:
    def __init__(self):
        self.admin = TeacherAdmin()

    def user_menu(self):
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
            student_id = input("Enter student ID: ").strip()
            print(self.admin.display_student(student_id))

        elif choice == "2":
            student_id = input("Student ID: ").strip()
            name = input("Name: ").strip()
            course = input("Course: ").strip()
            grade = input("Grade: ").strip()

            print(
                self.admin.add_student(
                    student_id,
                    name,
                    course,
                    grade
                )
            )

        elif choice == "3":
            student_id = input("Student ID: ").strip()
            unit_name = input("Unit name: ").strip()
            try:
                score = int(input("Score: ").strip())
            except ValueError:
                print(Fore.RED + "Score must be a number.")
                return True
            print(self.admin.add_unit(student_id, unit_name, score))

        elif choice == "4":
            student_id = input("Student ID: ").strip()
            code = input("Unit code: ").strip()

            try:
                score = int(input("Score: ").strip())
            except ValueError:
                print(Fore.RED + "Score must be a number.")
                return True

            letter = input("Letter grade: ").strip().upper()
            print(self.admin.add_grade(student_id, code, score, letter))

        elif choice == "5":
            student_id = input("Student ID: ").strip()
            code = input("Unit code: ").strip()

            try:
                score = int(input("New score: ").strip())
            except ValueError:
                print(Fore.RED + "Score must be a number.")
                return True

            letter = input("New letter grade: ").strip().upper()
            print(self.admin.update_grade(student_id, code, score, letter))

        elif choice == "6":
            student_id = input("Student ID: ").strip()
            code = input("Unit code: ").strip()
            print(self.admin.delete_grade(student_id, code))

        elif choice == "7":
            code = input("Unit code: ").strip()
            print(self.admin.delete_unit(code))

        elif choice == "8":
            student_id = input("Student ID to delete: ").strip()
            print(self.admin.delete_student(student_id))

        elif choice == "9":
            print(Fore.YELLOW + "Goodbye!")
            return False

        else:
            print(Fore.RED + "Invalid option.")

        return True

    def run(self):
        while self.user_menu():
            pass


if __name__ == "__main__":
    app = AdminCLI()
    app.run()
    print(Fore.YELLOW + "\nApplication closed.")