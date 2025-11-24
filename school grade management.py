import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# File to store grades data
DATA_FILE = "grades.txt"

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Main application class
class GradesManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Cozy Grades Manager")
        self.root.geometry("500x400")
        self.root.configure(bg="#E0F7FA")  # Light blue background for coziness

        # Load existing data
        self.data = load_data()

        # UI Elements
        self.title_label = tk.Label(root, text="Welcome to Cozy Grades Manager!", font=("Arial", 16, "bold"), bg="#E0F7FA", fg="#00796B")
        self.title_label.pack(pady=10)

        # Frame for adding students
        self.add_student_frame = tk.Frame(root, bg="#E0F7FA")
        self.add_student_frame.pack(pady=5)
        tk.Label(self.add_student_frame, text="Add Student:", bg="#E0F7FA").grid(row=0, column=0)
        self.student_entry = tk.Entry(self.add_student_frame)
        self.student_entry.grid(row=0, column=1)
        tk.Button(self.add_student_frame, text="Add", command=self.add_student, bg="#4CAF50", fg="white").grid(row=0, column=2)

        # Frame for adding grades
        self.add_grade_frame = tk.Frame(root, bg="#E0F7FA")
        self.add_grade_frame.pack(pady=5)
        tk.Label(self.add_grade_frame, text="Student:", bg="#E0F7FA").grid(row=0, column=0)
        self.student_var = tk.StringVar()
        self.student_combo = ttk.Combobox(self.add_grade_frame, textvariable=self.student_var, values=list(self.data.keys()))
        self.student_combo.grid(row=0, column=1)
        tk.Label(self.add_grade_frame, text="Subject:", bg="#E0F7FA").grid(row=1, column=0)
        self.subject_entry = tk.Entry(self.add_grade_frame)
        self.subject_entry.grid(row=1, column=1)
        tk.Label(self.add_grade_frame, text="Grade (0-100):", bg="#E0F7FA").grid(row=2, column=0)
        self.grade_entry = tk.Entry(self.add_grade_frame)
        self.grade_entry.grid(row=2, column=1)
        tk.Button(self.add_grade_frame, text="Add Grade", command=self.add_grade, bg="#4CAF50", fg="white").grid(row=3, column=1)

        # Frame for viewing grades
        self.view_frame = tk.Frame(root, bg="#E0F7FA")
        self.view_frame.pack(pady=5)
        tk.Label(self.view_frame, text="View Grades for:", bg="#E0F7FA").grid(row=0, column=0)
        self.view_student_var = tk.StringVar()
        self.view_student_combo = ttk.Combobox(self.view_frame, textvariable=self.view_student_var, values=list(self.data.keys()))
        self.view_student_combo.grid(row=0, column=1)
        tk.Button(self.view_frame, text="View", command=self.view_grades, bg="#2196F3", fg="white").grid(row=0, column=2)

        # Text area for displaying results
        self.result_text = tk.Text(root, height=10, width=50, bg="#F5F5F5", fg="#333")
        self.result_text.pack(pady=10)

    def add_student(self):
        name = self.student_entry.get().strip()
        if name and name not in self.data:
            self.data[name] = {}
            save_data(self.data)
            self.student_combo['values'] = list(self.data.keys())
            self.view_student_combo['values'] = list(self.data.keys())
            messagebox.showinfo("Success", f"Student {name} added!")
            self.student_entry.delete(0, tk.END)
        elif name in self.data:
            messagebox.showerror("Error", "Student already exists!")
        else:
            messagebox.showerror("Error", "Please enter a student name.")

    def add_grade(self):
        student = self.student_var.get()
        subject = self.subject_entry.get().strip()
        try:
            grade = float(self.grade_entry.get())
            if 0 <= grade <= 100 and student in self.data:
                self.data[student][subject] = grade
                save_data(self.data)
                messagebox.showinfo("Success", f"Grade added for {student} in {subject}!")
                self.subject_entry.delete(0, tk.END)
                self.grade_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Invalid grade or student not selected.")
        except ValueError:
            messagebox.showerror("Error", "Grade must be a number between 0 and 100.")

    def view_grades(self):
        student = self.view_student_var.get()
        if student in self.data:
            grades = self.data[student]
            if grades:
                avg = sum(grades.values()) / len(grades)
                result = f"Grades for {student}:\n"
                for subj, grd in grades.items():
                    result += f"{subj}: {grd}\n"
                result += f"Average: {avg:.2f}"
            else:
                result = f"No grades for {student} yet."
        else:
            result = "Please select a student."
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GradesManager(root)
    root.mainloop()
