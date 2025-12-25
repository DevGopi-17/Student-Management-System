FILE_NAME = "students.txt"

class Student:
    def __init__(self, name="", roll=0, cpi=0.0):
        self.name = name
        self.roll = roll
        self.cpi = cpi


class StudentManager:
    def __init__(self):
        self.students = []
        self.load_from_file()


    def data_validation(self, roll, cpi, name):
        if roll <= 0:
            print("Invalid roll number.")
            return False

        if cpi < 0.0 or cpi > 10.0:
            print("Invalid CPI.")
            return False

        for ch in name:
            if not (ch.isalpha() or ch == ' '):
                print("Invalid name.")
                return False

        return True


    def load_from_file(self):
        try:
            with open(FILE_NAME, "r") as file:
                for line in file:
                    roll, name, cpi = line.strip().split("|")
                    self.students.append(Student(name, int(roll), float(cpi)))
        except FileNotFoundError:
            pass

    def save_to_file(self):
        with open(FILE_NAME, "w") as file:
            for s in self.students:
                file.write(f"{s.roll}|{s.name}|{s.cpi}\n")


    def add_student(self):
        name = input("Enter name: ")
        roll = int(input("Enter roll no: "))
        cpi = float(input("Enter CGPA: "))

        if not self.data_validation(roll, cpi, name):
            return

        for s in self.students:
            if s.roll == roll:
                print("Roll no. already exists.")
                return

        self.students.append(Student(name, roll, cpi))
        self.save_to_file()
        print("Student added successfully")

    def remove_student(self):
        roll = int(input("Enter roll no to remove: "))

        for s in self.students:
            if s.roll == roll:
                self.students.remove(s)
                self.save_to_file()
                print("Student removed successfully")
                return

        print("Roll number doesn't exist.")

    def search_student(self):
        name = input("Enter the name: ").lower()
        found = False

        for s in self.students:
            if s.name.lower() == name:
                print(f"\nName : {s.name}")
                print(f"Roll : {s.roll}")
                print(f"CPI  : {s.cpi:.2f}")
                found = True

        if not found:
            print("Student not found.")

    def sort_students(self):
        self.students.sort(key=lambda s: s.name.lower())
        self.save_to_file()
        print("Students sorted successfully")

    def display_all(self):
        print("\n--- ALL STUDENTS ---")
        for s in self.students:
            print(f"{s.roll:<5} {s.name:<20} {s.cpi:.2f}")


    def menu(self):
        while True:     
            print("\n--- STUDENT DATABASE MANAGEMENT SYSTEM ---")
            print("1. Add student")
            print("2. Remove student")
            print("3. Search by name")
            print("4. Sort by name")
            print("5. Display all")
            print("0 / exit. Exit")

            choice = input("Enter choice: ").strip().lower()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.remove_student()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.sort_students()
            elif choice == "5":
                self.display_all()
            elif choice == "0" or choice == "exit":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number or 'exit'.")


if __name__ == "__main__":
    manager = StudentManager()
    manager.menu()
