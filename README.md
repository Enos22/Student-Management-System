**DATA FILE**
data/
├── courses.json
├── School(super_Admin).json
├── Student.json
├── teacher(admin).json
└── users.json


data/
    This folder contains the JSON files used by the system to store and manage data. Each file is responsible for a different part of the student management system:
    - courses.json – Stores information about the courses available in the system.
    - School(super_Admin).json – Stores school-related information managed by the Super Admin.
    - Student.json – Stores student information and their details.
    - teacher(admin).json – Stores information managed by the Teacher/Admin, including student and academic records.
    - users.json – Stores user information used by the system.

**MODELS**
# models/school_admin.py
    
    The SchoolAdmin class handles the main administrative tasks in the system. It allows a school administrator to manage teachers, students, courses, and user registration.
    Main responsibilities:
        - Teacher management
            - Adds new teachers.
            - Saves teacher information to teacher(admin).json.
            - Creates a teacher login account when a password is provided.
            - Deletes teachers.
        - Student management
            - Registers students and creates their login information.
            - Checks that a student is registered before adding them to the student records.
            - Adds or updates student details.
                - Deletes students.
        - Course management
            - Adds courses to courses.json.
            - Deletes courses using their ID.
        - User registration
            - Stores registered users in users.json.
            - Handles student and teacher/admin roles.
            - Passwords are hashed before being stored when a plain-text password is supplied.
        - Data handling
            - Uses the project's load_json() and save_json() functions to read and update the JSON data files.
            - Automatically generates the next available ID when an ID isn't supplied.
            - Performs basic matching and validation when working with registered students.
# models/student.py
  This file contains two classes: Student and StudentDetails.
Student
  The Student class represents an individual student and keeps their main academic and personal information, including:
    - Student ID
    - Name
    - Email
    - Course
    - Overall grade
    - Units and their grades/details
It also includes:
- from_dict() – Creates a Student object from data loaded from JSON.
- view_details() – Returns the student's information in a dictionary format.
StudentDetails
  The StudentDetails class is used to load and find student information.
It can:
    - Load students from data/students.json.
    - Fall back to registered students in data/users.json if the student file has no data.
    - Find a student using their ID, name, or email.
    - Find classmates who are taking the same course.
    - Return student information as Student objects.
# models/teacher_admin.py
 The TeacherAdmin class handles the day-to-day academic management tasks for teachers. It works with the student records stored in JSON and provides functions for managing students, units, and grades.
What it does
- Loads and saves student data
  - Reads student information from a JSON file when the class starts.
  - Saves changes back to the same file.
  - Creates the required folder if it doesn't already exist.
- Finds students
  - A student can be searched using their ID, name, or email.
  - It can also find students who have registered through the main user registry.
- Manages students
  - Adds registered students to the teacher's student records.
  - Prevents duplicate students.
  - Requires a student to be registered by the School Admin before they can be added.
  - Deletes students when needed.
- Manages units
  - Adds units and their scores to a student's record.
  - Updates an existing unit by adding it again with a new score.
  - Removes units when they are no longer needed.
- Manages grades
  - Adds a grade with both a score and letter grade.
  - Updates an existing grade.
  - Deletes a grade.
- Displays student information
  - Shows the student's ID, name, course, overall grade, and available units.
  - If the student has no units, it displays a message indicating that no units are available.
- Keeps an action log
  - The class maintains a log_actions list and records when students are added.
Example
A teacher can use the class to perform a workflow like:
Find student
     ↓
Add student
     ↓
Add units and scores
     ↓
Add or update grades
     ↓
Display student details
     ↓
Delete student if necessary
# models/user.py
 This file defines the Admin class.
   The Admin class extends the User class from models.users_login. This means an admin inherits the basic user information and login-related functionality instead of implementing everything again.
The class:
- Stores the admin's name
- Stores the admin's email
- Uses a password hash for authentication
- Assigns the user an admin role
- Reuses the functionality provided by the parent User class
In simple terms:
   Admin is a specialised user account for administrators, built on top of the existing User class.

# models/users_login.py
    This file provides the base user and role-specific user classes used for login and authentication.
.User
  User is the main class that stores the common information shared by users:
        - Name
        - Email
        - Password hash
        - User role
It also handles password-related operations:
- hash_password() – Uses SHA-256 to turn a password into a hash before it is stored.
- check_password() – Checks whether a provided password matches the stored password/hash.
- password_hash – Provides access to the stored password hash.
- to_dict() – Converts the user information into a dictionary so it can be stored in JSON.
Teacher_Admin
Teacher_Admin inherits from User and automatically assigns the role:
Teacher_Admin
This is used for teacher/admin accounts.
School_Admin
School_Admin also inherits from User, but assigns:
School_Admin
 This represents the school administrator account.
Simple overview
    User
    ├── Teacher_Admin
    └── School_Admin
    So the idea is that User provides the common login functionality, while Teacher_Admin and School_Admin create specific types of accounts with their own roles.

**TESTS**
# tests/test_auth.py
   This test file checks the project's authentication and user account functionality using Python's built-in unittest framework.
It tests:
- Password hashing – confirms that passwords are hashed and produce a 64-character SHA-256 hash.
- User registration – checks that a normal user can be registered correctly.
- Admin registration – checks that an admin account creates the correct Admin object and role.
- Duplicate emails – makes sure the system rejects an email that is already registered.
- Invalid emails – checks that badly formatted email addresses are rejected.
- Successful login – confirms that a user can log in with the correct password.
- Failed login – confirms that an incorrect password doesn't authenticate the user.
 Testing information for the README
 This gives us an important detail: the project uses Python's built-in unittest framework for this test file.

Since the file contains:
    if __name__ == "__main__":
        unittest.main()

it can also be run directly with:
    "python3 -m unittest tests/test_auth.py
"

# tests/test_cli.py
    This file tests the project's command-line interface (CLI). Instead of manually typing choices into the terminal, it uses mocked input to simulate what a real user would enter.
It currently checks two CLI behaviours:
- Viewing student details
  - Simulates a user entering Enos Arenga.
  - Selects option 1.
  - Exits using option 6.
  - Confirms the student's welcome message and details appear.
  - Confirms that an "INVALID CHOICE" message isn't displayed.
- Viewing classmates
  - Simulates the same student selecting option 5.
  - Checks that the appropriate classmates message is displayed.
  - Confirms there isn't an invalid-choice error.
Testing approach
    The test uses Python's built-in tools:

    unittest


and:

    unittest.mock


    patch() is used to simulate keyboard input, while redirect_stdout() captures what the CLI prints so the test can check the output.
It can also be run directly with:
        "python3 -m unittest tests/test_cli.py
"

# tests/test_decorator.py
This file tests the access-control decorators used in the project:
- login_required
- admin_required
 It creates a small FakeApp to simulate an application with a currently logged-in user.
The tests check:
- Guest access is blocked – a user who isn't logged in cannot access a protected action.
- Logged-in users are allowed – a normal User can access actions protected by login_required.
- Normal users can't access admin actions – admin_required blocks regular users.
- Teacher Admin access – Teacher_Admin is allowed to perform admin actions.
- School Admin access – School_Admin is also allowed to perform admin actions.
What this tells us about the project
 The application has a basic role-based access control system. Different parts of the application can be protected depending on whether someone is logged in and what role they have.

The test can also be run directly with:
     "python3 -m unittest tests/test_decorators.py
"

# tests/test_school_admin.py
This is one of the larger test files. It tests the main functionality of the School Admin side of the system.
 It uses Python's unittest framework together with temporary files, so the tests don't need to modify your real JSON data.
What it tests
Teacher management
- Adding a teacher saves the teacher correctly.
- Adding a teacher with a password creates a Teacher_Admin login account.
- A saved teacher can log in and access the teacher portal.
- Deleting an existing teacher works correctly.
- Trying to delete a teacher that doesn't exist returns False.
Student management
- Registering a student creates a user record with an ID and Student role.
- Registered students receive a hashed password.
- A registered student can log in using their email and password.
- Students can be added to the student records.
- An unregistered student cannot be added.
- Existing students can be deleted.
- Trying to delete a student that doesn't exist returns False.
Course management
- Adding a course saves it correctly.
- Deleting an existing course works.
- Trying to delete a course that doesn't exist returns False.
Important testing detail
The tests create a temporary directory using:
tempfile.TemporaryDirectory()
and create temporary versions of:
    teacher(admin).json
    students.json
    courses.json
    users.json
This is good because your actual project data isn't changed when the tests run.
The test also temporarily redirects the SchoolAdmin class to those test files.
README testing command
 
    "python3 -m unittest tests/test_school_admin.py"


# tests/test_student.py
 This file tests the student information and classmate functionality provided by Student and StudentDetails.
 It creates a temporary JSON file containing sample student records, so the tests are isolated from the project's real student data.
What it tests
 Loading students
- Confirms that student records are loaded correctly from the JSON file.
- Checks that all three test students are available.
Finding students
- Finds a student by their name.
- Checks that searching is case-insensitive.
- Confirms that searching for a student who doesn't exist returns no result.
Classmates
- Finds students taking the same course.
- Confirms that students from a different course aren't included.
- Makes sure the current student isn't included in their own classmates list.
- Checks that a student with no classmates gets an empty list.
Student units
- Confirms that a student's units are loaded correctly.
- Checks that the expected unit and its value are available.
Testing detail
The test uses:
     tempfile.NamedTemporaryFile()
 to create a temporary JSON file containing the test data.
   Once the test finishes, the temporary file is deleted. This keeps the test environment clean and prevents the real students.json from being changed.
Direct command
   This file can be run directly with:
   "python3 -m unittest tests/test_student.py"

# test_teacher_admin.py
    This file checks the main functionality of the Teacher Admin class.
It creates a TeacherAdmin instance using: 

TeacherAdmin("data/test_students.json") 
Then it tests the following workflow:
1. Add a student
   - Adds Brian as student S002.
2. Add units
   - Adds Mathematics with a score of 90.
   - Adds English with a score of 85.
3. Display student details
   - Displays Brian's information and academic records.
4. Update a unit
   - Adds Mathematics again with a new score of 95.
   - This checks that the existing unit can be updated.
5. Delete the student
   - Removes student S002.
6. Check deletion
   - Attempts to display the deleted student.
   - The expected result is Student not found.
How to run it 

Because this is a standalone Python script, it can be run with:

"python3 -m tests.test_teacher_admin"

If everything works without an exception, it prints:

All tests passed

If something goes wrong, it catches the error and prints: 

Test failed: ...

**UTILS**

# utils/auth.py
This file handles the project's registration and login system through the AuthManager class.
User registration
The register() method:
- Cleans up the user's name and email.
- Checks that the name isn't empty.
- Validates the email address.
- Requires a password of at least 4 characters.
- Allows the supported roles:
  - user
  - admin
  - teacher_admin
  - school_admin
- Prevents two accounts from using the same email.
- Hashes the password before saving it.
- Creates the appropriate user object based on the selected role.
- Saves the new account to users.json.
User login
The login() method:
- Looks for the user's email in users.json.
- Recreates the appropriate user type based on their stored role.
- Checks the entered password against the stored password hash.
- Returns the logged-in user when the credentials are correct.
- Returns None when the credentials don't match.
It also checks teacher(admin).json for teacher accounts that may not yet have a record in the main users registry.
How it connects to the rest of the project
AuthManager brings several parts of the project together:
AuthManager
   │
   ├── User / Admin / Teacher_Admin / School_Admin
   │
   ├── validators.py
   │
   └── storage.py
So authentication isn't handled in isolation. It uses the user models, validation utilities, and JSON storage utilities.
Security note
Passwords aren't stored as plain text when users register through AuthManager. The password is converted into a SHA-256 hash before being written to the JSON data.

# utils/decorator.py
This file controls access to certain parts of the system using Python decorators.
It contains two decorators:
login_required
Makes sure a user is logged in before allowing a function to run.
- Checks self.current_user.
- If nobody is logged in, it prints "Please login first."
- Otherwise, the original function continues normally.
Example:
  @login_required
 def view_profile(self):
    ...
admin_required
Makes sure the logged-in user has an admin-level role.
It allows these roles:
- admin
- Teacher_Admin
- School_Admin
If there is no logged-in user, it asks them to log in first.
If the user is logged in but doesn't have an admin role, it prints:
Admin access required.
How it fits into the project
decorator.py
    │
    ├── login_required
    │       └── Checks if a user is logged in
    │
    └── admin_required
            └── Checks if the user has admin privileges

# utils/storage.py
This file handles reading and saving JSON data for the project. Instead of repeating file-handling code throughout the system, other parts of the project can use these two functions.
load_json(file_path)
Loads data from a JSON file.
- Converts the file path into a Path object.
- If the file doesn't exist, it returns an empty list.
- Opens and reads the JSON file.
- If the JSON is invalid or there is a file-related error, it returns an empty list instead of crashing.
Example:
students = load_json("data/students.json")
save_json(file_path, data)
Saves Python data into a JSON file.
- Creates the parent directory if it doesn't already exist.
- Opens the file for writing.
- Saves the data using json.dump().
- Uses indentation of 4 spaces so the JSON files remain easy to read.
Example:
save_json("data/students.json", students)
How it fits into the project
  storage.py
    │
    ├── load_json()
    │      └── Reads data from JSON files
    │
    └── save_json()
           └── Writes data to JSON files

# utils/validator.py
This file contains small validation functions used to check user input before it is accepted by the system.
not_empty(value)
Checks whether a value contains something meaningful.
- Returns False if the value is None.
- Removes spaces around the value.
- Returns True if something remains.
- Returns False for an empty string or spaces only.
Example:
not_empty("Benson")   # True
not_empty("   ")      # False
not_empty(None)       # False
valid_email(email)
Performs a basic email format check.
It checks that:
- The email isn't None.
- It contains an @.
- There is something before the @.
- The domain contains a .
- The domain doesn't end with .
Example:
valid_email("benson@gmail.com")  # True
valid_email("bensongmail.com")   # False
How it fits into the project
validator.py
    │
    ├── not_empty()
    │      └── Checks required input
    │
    └── valid_email()
           └── Checks basic email format
AuthManager uses these validators when registering users, so invalid names and email addresses can be rejected before the account is saved.
**main.py**
main.py is where the different parts of the Student Management System come together. It provides the command-line menus that students, teachers, and school administrators use.
It connects:
- SchoolAdmin — school-level administration
- StudentDetails — student information
- TeacherAdmin — academic management
- User — user/password handling
- AuthManager — registration and login
- storage.py — loading JSON data
- colorama — adds colours to the terminal interface
Main parts
SchoolCLI
This is the main command-line interface.
When the program starts, it creates the required managers and keeps track of the currently logged-in user.
The system has different menus depending on the user's role:
Guest
  │
  ├── Register
  ├── Login
  └── Exit
       │
       ▼
    Logged in
       │
       ├── Student
       │      └── Student Portal
       │
       ├── Teacher_Admin
       │      └── Teacher Admin Portal
       │
       └── School_Admin
              └── School Admin Portal
Student portal
Students can:
1. View their full details
2. View their course
3. View their grade
4. View their units and marks
5. View classmates
6. Exit
Students can search their information using their name or email.
Teacher Admin portal
Teacher administrators can:
1. View a student
2. Add a student
3. Add a unit
4. Add a grade
5. Update a grade
6. Delete a grade
7. Delete a unit
8. Delete a student
9. Exit
The program also checks that scores entered for units and grades are numbers.
School Admin portal
School administrators have wider control over the system. They can:
1. Add teachers
2. Delete teachers
3. Add students
4. Delete students
5. Add courses
6. Delete courses
7. Register students
8. Exit
When registering a student, the password is hashed before being stored.
Input helpers
main.py also has a few helper methods:
- is_valid_email() — basic email validation
- is_non_empty() — checks that required text isn't blank
- read_id() — makes sure IDs are whole numbers
- read_units() — allows the admin to enter multiple units and marks
normalize_student_ids()
    This helper loads the student JSON data and makes sure the student objects use the IDs stored in the data file.
main()
    There is also a standalone main() function that provides a simpler student-only interface. It asks for a student's name and then lets them view their details, course, grade, units, or classmates.
However, the file ends with:
if __name__ == "__main__":
    SchoolCLI().run()
So when you run:

python main.py

the SchoolCLI application is what starts.
README note
    For the final README, I'll explain main.py as the entry point/command-line interface, rather than going through every function. Something along the lines of:
main.py brings the project together and provides the terminal menus for students, teacher admins, and school admins. After login, each user is taken to the portal that matches their role. The CLI also handles input validation and connects the menus to the models and JSON storage.