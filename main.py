from models.school_admin import SchoolAdmin


def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1]


def is_non_empty(text):
    return text.strip() != ""


def read_id(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        print("That ID must be a whole number. Try again.")


def read_units():
    units = {}
    print("Now enter units. Leave the unit name blank when done.")
    while True:
        unit_name = input("Unit name: ")
        if unit_name == "":
            break
        mark = read_id(f"Mark for {unit_name}: ")
        units[unit_name] = mark
    return units


admin = SchoolAdmin("Kaitlyn", "kaitlyn@school.com")

while True:
    print("\n--- School Admin Menu ---")
    print("1. Add Teacher")
    print("2. Delete Teacher")
    print("3. Add Student")
    print("4. Delete Student")
    print("5. Add Course")
    print("6. Delete Course")
    print("7. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        teacher_id = read_id("Teacher ID: ")
        name = input("Teacher name: ")
        email = input("Teacher email: ")
        subject = input("Subject: ")

        if not is_non_empty(name):
            print("Name cannot be empty.")
        elif not is_valid_email(email):
            print("This email is not valid.")
        elif not is_non_empty(subject):
            print("Subject cannot be empty.")
        else:
            admin.add_teacher({"id": teacher_id, "name": name, "email": email, "subject": subject})
            print("Teacher added.")

    elif choice == "2":
        teacher_id = read_id("Teacher ID to delete: ")
        deleted = admin.delete_teacher(teacher_id)
        print("Deleted." if deleted else "No teacher found with that ID.")

    elif choice == "3":
        student_id = read_id("Student ID: ")
        name = input("Student name: ")
        course = input("Course: ")
        grade = input("Overall grade: ")

        if not is_non_empty(name):
            print("Name cannot be empty.")
        elif not is_non_empty(course):
            print("Course cannot be empty.")
        elif not is_non_empty(grade):
            print("Grade cannot be empty.")
        else:
            units = read_units()
            admin.add_student({
                "id": student_id,
                "name": name,
                "course": course,
                "grade": grade,
                "units": units
            })
            print("Student added.")

    elif choice == "4":
        student_id = read_id("Student ID to delete: ")
        deleted = admin.delete_student(student_id)
        print("Deleted." if deleted else "No student found with that ID.")

    elif choice == "5":
        course_id = read_id("Course ID: ")
        title = input("Course title: ")

        if not is_non_empty(title):
            print("Course title cannot be empty.")
        else:
            admin.add_course({"id": course_id, "title": title})
            print("Course added.")

    elif choice == "6":
        course_id = read_id("Course ID to delete: ")
        deleted = admin.delete_course(course_id)
        print("Deleted." if deleted else "No course found with that ID.")

    elif choice == "7":
        print("Goodbye!")
        break

    else:
        print("Invalid option, try again.")