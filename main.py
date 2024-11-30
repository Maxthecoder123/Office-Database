from colorama import Fore

login_details = {
    "Max": "admin123"
}

rank_details = {
    "Max": "Admin"
}

menu_loop = True

class Person:
    def __init__(self, name, age, rank):
        self.name = name
        self.age = age
        self.rank = rank

    def info(self):
        print("Information in database: ")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Rank: {self.rank}")

class Employee(Person):
    employee_registry = {}

    def __init__(self, name, age, rank, unique_id):
        super().__init__(name, age, rank)
        self.pending_jobs = []
        self.unique_id = unique_id  # Store the unique ID
        Employee.employee_registry[unique_id] = self  # Register the employee instance by their unique ID

    def jobs_check(self):
        print()
        if not self.pending_jobs:
            print("You have no pending jobs")  # No jobs
        elif len(self.pending_jobs) == 1:
            print(f"You have 1 uncompleted job")
            for job in self.pending_jobs:
                print(f"1. {job}")
        else:
            print(f"You have {len(self.pending_jobs)} uncompleted jobs")
            for i, job in enumerate(self.pending_jobs, 1):
                print(f"{i}. {job}")
        Employee.employee_menu(self)

    def job_completed(self, job_text):
        print()
        if job_text in self.pending_jobs:
            self.pending_jobs.remove(job_text)
            print(f"'{job_text}' was removed from pending jobs")
        else:
            print(f"'{job_text}' is not in pending jobs.")

    def employee_menu(self):
        print("-- MENU --")
        print("1. Check for pending jobs")
        print("2. Mark job as complete")
        print("3. Logout")
        print("4. Quit")
        while True:
            menu_choice = int(input("   > "))
            if menu_choice == 1: self.jobs_check(); break
            elif menu_choice == 2: self.remove_jobs(); break # todo
            elif menu_choice == 3: log_in(); break
            elif menu_choice == 4: quit()
            else: print("Please enter [1,2,3 or 4 only]")


class Admin(Person):
    admin_registry = {}

    def __init__(self, name, age, rank, unique_id):
        super().__init__(name, age, rank)
        self.unique_id = unique_id
        Admin.admin_registry[unique_id] = self

    @staticmethod
    def add_job(employee_id, job_text):
        employee = Employee.employee_registry.get(employee_id)
        if employee:
            employee.pending_jobs.append(job_text)
            print(f"Added job '{job_text}' to {employee.name}.")
        else:
            print(f"Employee with ID '{employee_id}' not found.")

    @staticmethod
    def list_employees():
        i = 0
        for user in login_details:
            if rank_details[user] == "Employee":
                i += 1
                print(f"{i}. {user}")
        else:
            print("No employee's in database")


    def admin_menu(self):
        while True:
            print("-- MENU --")
            print("1. Create a job")
            print("2. List Employee's and their jobs")
            print("3. Logout")
            print("4. Quit")
            menu_choice = int(input("   > "))
            if menu_choice == 1: employee = input("Enter employee ID: "); text = input(f"Job text for '{employee}': "); self.add_job(employee, text)
            elif menu_choice == 2: self.list_employees()
            elif menu_choice == 3: log_in(); break
            elif menu_choice == 4: quit()
            else: print("Please enter [1,2,3 or 4 only]")


def menu():
    # Menu
    print("**-- Office Database --**")
    print("1. Log in")
    print("2. Sign up")
    print("3. Quit")
    while menu_loop:
        try:
            menu_choice = int(input("   > "))
            if menu_choice == 1:
                log_in()
            elif menu_choice == 2:
                sign_up()
            elif menu_choice == 3:
                quit()
        except ValueError:
            print("Enter [1, 2, or 3] only")

def id_generation(username, age):
    return username[:3] + str(age)  # Create a unique ID based on username and age

def log_in():
    global menu_loop
    print("-- LOGIN --")
    username_input = input("Enter your username: ")
    password_input = input("Enter your password: ")
    if username_input in login_details and password_input == login_details[username_input]:
        print(f"Welcome {username_input}")
        for employee in Employee.employee_registry.values():
            if employee.name == username_input and employee.rank == "Employee":
                print("Logged in as Employee.")
                employee.employee_menu()
                break
        else:
            for admin in Admin.admin_registry.values():
                print(f"{admin.name} == {username_input}")
                if admin.name == username_input and admin.rank == "Admin":
                    print("Logged in as Admin.")
                    admin.admin_menu()
                    break
            else:
                print("No matching user found.")


            #if rank_details[username_input] == "Admin":
                #print("Logged in as Admin.")
                #Admin.admin_menu()

        menu_loop = False
    else:
        print("Username or Password is incorrect")
        menu()

def sign_up():
    print("-- SIGNUP --")
    username_input = input("Username: ")
    password_input = input("Password: ")
    if username_input in login_details:
        print("This username is already in use")
        menu()
    password_repeat = input("Password (again): ")
    if password_input != password_repeat:
        print("Passwords are not the same")
        sign_up()
    else:
        age = int(input("Enter your age: "))
        login_details[username_input] = password_input
        rank_details[username_input] = "Employee"

        unique_id = id_generation(username_input, age)
        new_employee = Employee(username_input, age, "Employee", unique_id)

        print(f"Employee created with ID: {unique_id}")
        log_in()


# Test Data
p1 = Employee("Bob", 34, "Employee", "Bob34")
a1 = Admin("Max", 15, "Admin", "admin1")

if __name__ == "__main__":
    print(Admin.admin_registry)
    print(Employee.employee_registry)
    menu()

