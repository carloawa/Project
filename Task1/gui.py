import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import sys
from Task1 import StudentManagementSystem, Student
from management_center import StudentManagementCenter

class StudentSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System - Simple Launcher")
        self.root.geometry("600x500")
    
        
        self.sms = StudentManagementSystem()
        self.management_center = StudentManagementCenter(self.root, self.sms)
        
        btn_frame = tk.Frame(root, pady=10)
        btn_frame.pack()

        tk.Button(btn_frame, text="1. Run Preset Test Cases", command=self.run_demo, width=25, bg="#e1f5fe").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="2. Load Last Saved Data", command=self.load_data, width=25, bg="#e8f5e9").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="3. Save Current Data", command=self.save_data, width=25, bg="#fff3e0").grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="4. View All Students", command=self.show_all, width=25, bg="#f3e5f5").grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="5. Add Custom Student", command=self.add_custom_student, width=25, bg="#fce4ec").grid(row=2, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="6. Sort Students", command=self.open_sort_window, width=25, bg="#e0f7fa").grid(row=2, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="7. Student Comprehensive Management Center", command=self.open_management_center, width=52, bg="#d1c4e9").grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        tk.Label(root, text="System Output Log:", anchor="w").pack(fill="x", padx=10)
        self.output_text = scrolledtext.ScrolledText(root, height=20, wrap=tk.WORD)
        self.output_text.pack(fill="both", expand=True, padx=10, pady=5)
        sys.stdout = TextRedirector(self.output_text)

    def run_demo(self):
        self.output_text.delete(1.0, tk.END)
        print("===== Running preset test cases... =====\n")
        
        try:
            student1 = Student(
                name="Peter", id_num="s12345678", email="peter@student.com",
                enrollment_date="2023-09-01", courses=["Math", "English"], gpa=3.8
            )
            student2 = Student(
                name="John", id_num="s12345679", email="john@student.com",
                enrollment_date="2024-09-01", courses=["Music", "Sports"], gpa=3.6
            )
            
            self.sms.add_student(student1)
            self.sms.add_student(student2)
            
            print("\n===== Test cases completed =====")
            print(self.sms.list_all_students())
            
        except ValueError as e:
            print(f"Error: {e}")

    def load_data(self):
        self.output_text.delete(1.0, tk.END)
        self.sms.load_from_file()

    def save_data(self):
        #save data to json
        self.sms.save_to_file()
        messagebox.showinfo("Prompt", "Data saved successfully!")

    def show_all(self):
        #show all student
        self.output_text.delete(1.0, tk.END)
        print(self.sms.list_all_students())

    def add_custom_student(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Undergraduate Student")
        add_window.geometry("400x420")

        tk.Label(add_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        name_entry = tk.Entry(add_window, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Student ID (s+8 digits):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        id_entry = tk.Entry(add_window, width=30)
        id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        email_entry = tk.Entry(add_window, width=30)
        email_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Enrollment Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        date_entry = tk.Entry(add_window, width=30)
        date_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(add_window, text="GPA (0.0-4.0):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        gpa_entry = tk.Entry(add_window, width=30)
        gpa_entry.grid(row=4, column=1, padx=10, pady=5)

        def confirm_add():
            try:
                #Basic info
                name = name_entry.get()
                id_num = id_entry.get()
                email = email_entry.get()
                enroll_date = date_entry.get()
                gpa = float(gpa_entry.get())

                student = Student(
                    name=name,
                    id_num=id_num,
                    email=email,
                    enrollment_date=enroll_date,
                    gpa=gpa
                )

                if self.sms.add_student(student):
                    messagebox.showinfo("Success", "Undergraduate student added successfully!")
                    add_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Addition failed: {e}")

        #comfirm button
        tk.Button(add_window, text="Confirm Add", command=confirm_add, bg="#c8e6c9", width=20).grid(row=5, column=0, columnspan=2, pady=15)

    def open_sort_window(self):
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Students")
        sort_window.geometry("400x320")
        tk.Label(sort_window, text="Please select sorting method:", font=("Arial", 12, "bold")).pack(pady=15)
        #Sorting button
        btn_style = {"width": 38, "pady": 8, "bg": "#f5f5f5"}
        
        tk.Button(sort_window, text="1. Sort by Student ID", command=lambda: self.execute_sort("id"), **btn_style).pack(pady=5)
        tk.Button(sort_window, text="2. Sort by GPA (Descending)", command=lambda: self.execute_sort("gpa"), **btn_style).pack(pady=5)
        tk.Button(sort_window, text="3. Sort by Student Name (Alphabetical)", command=lambda: self.execute_sort("name"), **btn_style).pack(pady=5)
        tk.Button(sort_window, text="4. Sort by Graduation Status", command=lambda: self.execute_sort("graduation"), **btn_style).pack(pady=5)

    def execute_sort(self, sort_type):
        self.output_text.delete(1.0, tk.END)
        
        if not self.sms.students:
            print("📋 No student records, cannot sort")
            return
        student_list = list(self.sms.students.items())
        #sorting
        if sort_type == "id":
            #Sort by id (ascending)
            sorted_list = sorted(student_list, key=lambda x: x[0])
            title = "===== Sorted by Student ID (Ascending) ====="
        elif sort_type == "gpa":
            #Sort by gpa (high to low)
            sorted_list = sorted(student_list, key=lambda x: x[1]._gpa, reverse=True)
            title = "===== Sorted by GPA (Descending) ====="
        elif sort_type == "name":
            #Sort by name
            sorted_list = sorted(student_list, key=lambda x: x[1].name)
            title = "===== Sorted by Student Name (Alphabetical Ascending) ====="
        elif sort_type == "graduation":
            #Sorted by Graduation Status
            sorted_list = sorted(student_list, key=lambda x: x[1]._is_graduated)
            title = "===== Sorted by Graduation Status (Not Graduated First) ====="
        else:
            return
        
        print(title)
        for idx, (stu_id, student) in enumerate(sorted_list, 1):
            grad_status = "Graduated" if student._is_graduated else "Not Graduated"
            print(f"{idx}. Name: {student.name} | ID: {stu_id} | GPA: {student._gpa} | Status: {grad_status} | Role: {student.get_role()}")

    def open_management_center(self):
        self.management_center.open()

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
    def write(self, s):
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)
    def flush(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentSystemGUI(root)
    root.mainloop()