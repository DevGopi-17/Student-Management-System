import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "students.txt"


class Student:
    def __init__(self, name, roll, cgpa):
        self.name = name
        self.roll = roll
        self.cgpa = cgpa


class StudentManager:
    def __init__(self):
        self.students = []
        self.load_from_file()

    def load_from_file(self):
        try:
            with open(FILE_NAME, "r") as f:
                for line in f:
                    roll, name, cgpa = line.strip().split("|")
                    self.students.append(Student(name, int(roll), float(cgpa)))
        except FileNotFoundError:
            pass

    def save_to_file(self):
        with open(FILE_NAME, "w") as f:
            for s in self.students:
                f.write(f"{s.roll}|{s.name}|{s.cgpa}\n")

    def add_student(self, name, roll, cgpa):
        if roll <= 0:
            return "Invalid roll number"
        if not (0 <= cgpa <= 10):
            return "CGPA must be between 0 and 10"
        if any(s.roll == roll for s in self.students):
            return "Roll already exists"
        self.students.append(Student(name, roll, cgpa))
        self.save_to_file()
        return "Student added successfully"

    def remove_student(self, roll):
        for s in self.students:
            if s.roll == roll:
                self.students.remove(s)
                self.save_to_file()
                return "Student removed"
        return "Roll not found"


#GUI LAYER 
class StudentGUI:
    def __init__(self, root):
        self.manager = StudentManager()
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x500")

        # Themed widgets
        style = ttk.Style()
        style.theme_use("clam")

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(expand=True, fill="both")

        main.columnconfigure(1, weight=1)
        main.rowconfigure(7, weight=1)

        ttk.Label(
            main,
            text="Student Management System",
            font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=0, columnspan=4, pady=10)

        #INPUTS 
        ttk.Label(main, text="Name").grid(row=1, column=0, sticky="w")
        ttk.Label(main, text="Roll No").grid(row=2, column=0, sticky="w")
        ttk.Label(main, text="CGPA").grid(row=3, column=0, sticky="w")

        self.name_var = tk.StringVar()
        self.roll_var = tk.IntVar()
        self.cgpa_var = tk.DoubleVar()

        ttk.Entry(main, textvariable=self.name_var).grid(
            row=1, column=1, sticky="ew", padx=5
        )
        ttk.Entry(main, textvariable=self.roll_var).grid(
            row=2, column=1, sticky="ew", padx=5
        )
        ttk.Entry(main, textvariable=self.cgpa_var).grid(
            row=3, column=1, sticky="ew", padx=5
        )

        #BUTTONS
        ttk.Button(main, text="Add Student", command=self.add_student).grid(row=4, column=0, pady=5)
        ttk.Button(main, text="Remove Student", command=self.remove_student).grid(row=4, column=1, pady=5)
        ttk.Button(main, text="Sort By Name", command=self.sort_students).grid(row=4, column=2, pady=5)
        ttk.Button(main, text="Show Statistics", command=self.show_statistics).grid(row=4, column=3, padx=5)

        #LIVE SEARCH  
        ttk.Label(main, text="Live Search").grid(row=5, column=0, sticky="w")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(main, textvariable=self.search_var)
        search_entry.grid(row=5, column=1, sticky="ew", padx=5)
        search_entry.bind("<KeyRelease>", self.live_search)

        #TABLE (Treeview)
        columns = ("Roll", "Name", "CGPA")
        self.tree = ttk.Treeview(main, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(main, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=7, column=0, columnspan=4, sticky="nsew", pady=10)
        scrollbar.grid(row=7, column=4, sticky="ns")

        #EVENT BINDING 
        self.root.bind("<Return>", lambda e: self.add_student())
        self.tree.bind("<Double-1>", self.show_details)

    #FUNCTIONS 
    def refresh_table(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        students = data if data is not None else self.manager.students
        for s in students:
            self.tree.insert("", "end", values=(s.roll, s.name, f"{s.cgpa:.2f}"))

    def add_student(self):
        try:
            msg = self.manager.add_student(
                self.name_var.get(),
                self.roll_var.get(),
                self.cgpa_var.get()
            )
            messagebox.showinfo("Info", msg)
            self.refresh_table()
        except tk.TclError:
            messagebox.showerror("Error", "Invalid input")

    def remove_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student first")
            return

        if messagebox.askyesno("Confirm", "Delete selected student?"):
            roll = int(self.tree.item(selected[0])["values"][0])
            messagebox.showinfo("Info", self.manager.remove_student(roll))
            self.refresh_table()

    def sort_students(self):
        self.manager.students.sort(key=lambda s: s.name.lower())
        self.manager.save_to_file()
        self.refresh_table()

    #LIVE SEARCH  
    def live_search(self, event):
        query = self.search_var.get().lower()
        filtered = [s for s in self.manager.students if query in s.name.lower()]
        self.refresh_table(filtered)

    #STATISTICS PANEL 
    def show_statistics(self):
        if not self.manager.students:
            messagebox.showinfo("Statistics", "No student data available")
            return

        total = len(self.manager.students)
        avg = sum(s.cgpa for s in self.manager.students) / total
        topper = max(self.manager.students, key=lambda s: s.cgpa)

        messagebox.showinfo(
            "Statistics",
            f"Total Students: {total}\n"
            f"Average CGPA: {avg:.2f}\n"
            f"Topper: {topper.name} ({topper.cgpa})"
        )

    #DOUBLE CLICK SHOW DETAILS
    def show_details(self, event):
        item = self.tree.selection()[0]
        roll, name, cgpa = self.tree.item(item)["values"]
        messagebox.showinfo(
            "Student Details",
            f"Roll No: {roll}\nName: {name}\nCGPA: {cgpa}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    StudentGUI(root)
    root.mainloop()
