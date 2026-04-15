import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

class StudentManagementCenter:
    def __init__(self, parent, sms):
        self.parent = parent
        self.sms = sms
        self.center_window = None
        self.student_listbox = None
        self.info_text = None
        self.grad_status_var = None

    def open(self):# open management_center
        if self.center_window and self.center_window.winfo_exists():
            self.center_window.focus()
            return
        
        self.center_window = tk.Toplevel(self.parent)
        self.center_window.title("Student Comprehensive Management Center")
        self.center_window.geometry("900x700")
        
        left_frame = tk.Frame(self.center_window, padx=10, pady=10, bg="#f5f5f5")
        left_frame.pack(side="left", fill="y")
        
        tk.Label(left_frame, text="Student List", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(pady=(0, 10))
        
        self.student_listbox = tk.Listbox(left_frame, width=30, height=20)
        self.student_listbox.pack(pady=(0, 10))
        
        self.refresh_student_list()
        
        right_frame = tk.Frame(self.center_window, padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)
        
        info_frame = tk.LabelFrame(right_frame, text="Complete Student Information", padx=10, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=10, wrap=tk.WORD)
        self.info_text.pack(fill="x")
        
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill="both", expand=True)
        
        self._create_course_tab(notebook)# course Management page
        self._create_grade_tab(notebook)# grade Management page
        self._create_gpa_grad_tab(notebook)# gpa and grad Management page
        self._create_system_tab(notebook)# System operation page
        
        self.student_listbox.bind("<<ListboxSelect>>", self.refresh_student_info)

    def refresh_student_list(self):#refresh student list
        self.student_listbox.delete(0, tk.END)
        for stu_id, student in self.sms.students.items():
            self.student_listbox.insert(tk.END, f"{student.name} ({stu_id})")

    def refresh_student_info(self, event=None):
        """刷新选中学生的信息展示"""
        selection = self.student_listbox.curselection()
        if not selection:
            return
        stu_id = list(self.sms.students.keys())[selection[0]]
        student = self.sms.students[stu_id]
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, student.get_student_info())
        
        if self.grad_status_var:#update graduated state
            self.grad_status_var.set(student._is_graduated)

    def _create_course_tab(self, notebook):#create course tab
        course_frame = tk.Frame(notebook, padx=10, pady=10)
        notebook.add(course_frame, text="Course Management")
        
        tk.Label(course_frame, text="Add Course:").grid(row=0, column=0, sticky="w", pady=5)
        course_add_entry = tk.Entry(course_frame, width=30)
        course_add_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def add_course():
            selection = self.student_listbox.curselection()
            if not selection:
                messagebox.showwarning("Prompt", "Please select a student first!")
                return
            stu_id = list(self.sms.students.keys())[selection[0]]
            student = self.sms.students[stu_id]
            if student.add_course(course_add_entry.get()):
                self.refresh_student_info()
                course_add_entry.delete(0, tk.END)
        
        tk.Button(course_frame, text="Add", command=add_course, bg="#c8e6c9").grid(row=0, column=2, pady=5)
        
        tk.Label(course_frame, text="Drop Course:").grid(row=1, column=0, sticky="w", pady=5)
        course_drop_entry = tk.Entry(course_frame, width=30)
        course_drop_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def drop_course():
            selection = self.student_listbox.curselection()
            if not selection:
                messagebox.showwarning("Prompt", "Please select a student first!")
                return
            stu_id = list(self.sms.students.keys())[selection[0]]
            student = self.sms.students[stu_id]
            if student.drop_course(course_drop_entry.get()):
                self.refresh_student_info()
                course_drop_entry.delete(0, tk.END)
        
        tk.Button(course_frame, text="Drop", command=drop_course, bg="#ffcdd2").grid(row=1, column=2, pady=5)

    def _create_grade_tab(self, notebook):
        """创建成绩管理标签页"""
        grade_frame = tk.Frame(notebook, padx=10, pady=10)
        notebook.add(grade_frame, text="Grade Management")
        
        tk.Label(grade_frame, text="Course Name:").grid(row=0, column=0, sticky="w", pady=5)
        grade_course_entry = tk.Entry(grade_frame, width=20)
        grade_course_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(grade_frame, text="Grade (0-100):").grid(row=0, column=2, sticky="w", pady=5)
        grade_score_entry = tk.Entry(grade_frame, width=10)
        grade_score_entry.grid(row=0, column=3, padx=5, pady=5)
        
        def set_grade():
            selection = self.student_listbox.curselection()
            if not selection:
                messagebox.showwarning("Prompt", "Please select a student first!")
                return
            stu_id = list(self.sms.students.keys())[selection[0]]
            student = self.sms.students[stu_id]
            if student.set_course_grade(grade_course_entry.get(), grade_score_entry.get()):
                self.refresh_student_info()
                grade_course_entry.delete(0, tk.END)
                grade_score_entry.delete(0, tk.END)
        
        tk.Button(grade_frame, text="Set Grade", command=set_grade, bg="#c8e6c9").grid(row=0, column=4, padx=5, pady=5)
        
        def show_avg_grade():
            selection = self.student_listbox.curselection()
            if not selection:
                messagebox.showwarning("Prompt", "Please select a student first!")
                return
            stu_id = list(self.sms.students.keys())[selection[0]]
            student = self.sms.students[stu_id]
            messagebox.showinfo("Average Course Grade", student.get_course_average_grade())
        
        tk.Button(grade_frame, text="View Average Course Grade", command=show_avg_grade, bg="#bbdefb").grid(row=1, column=0, columnspan=5, pady=10)

    def _create_gpa_grad_tab(self, notebook):
        gpa_grad_frame = tk.Frame(notebook, padx=10, pady=10)
        notebook.add(gpa_grad_frame, text="GPA & Graduation Management")
        
        tk.Label(gpa_grad_frame, text="Update GPA (0.0-4.0):").grid(row=0, column=0, sticky="w", pady=5)
        gpa_entry = tk.Entry(gpa_grad_frame, width=20)
        gpa_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def update_gpa():
            selection = self.student_listbox.curselection()
            if not selection:
                messagebox.showwarning("Prompt", "Please select a student first!")
                return
            stu_id = list(self.sms.students.keys())[selection[0]]
            student = self.sms.students[stu_id]
            try:
                student.update_gpa(float(gpa_entry.get()))
                self.refresh_student_info()
                gpa_entry.delete(0, tk.END)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(gpa_grad_frame, text="Update GPA", command=update_gpa, bg="#c8e6c9").grid(row=0, column=2, padx=5, pady=5)
        
        def check_grad_eligibility():
            selection = self.student_listbox.curselection()
            if not selection:
                messagebox.showwarning("Prompt", "Please select a student first!")
                return
            stu_id = list(self.sms.students.keys())[selection[0]]
            student = self.sms.students[stu_id]
            messagebox.showinfo("Graduation Eligibility Check", student.check_graduation_eligibility())
        
        tk.Button(gpa_grad_frame, text="Check Graduation Eligibility", command=check_grad_eligibility, bg="#fff9c4").grid(row=1, column=0, columnspan=3, pady=10)
        
        tk.Label(gpa_grad_frame, text="Graduation Status:").grid(row=2, column=0, sticky="w", pady=5)
        self.grad_status_var = tk.BooleanVar()
        tk.Checkbutton(gpa_grad_frame, text="Graduated", variable=self.grad_status_var).grid(row=2, column=1, sticky="w", pady=5)
        
        def set_grad_status():
            selection = self.student_listbox.curselection()
            if not selection:
                messagebox.showwarning("Prompt", "Please select a student first!")
                return
            stu_id = list(self.sms.students.keys())[selection[0]]
            student = self.sms.students[stu_id]
            student.set_graduation_status(self.grad_status_var.get())
            self.refresh_student_info()
        
        tk.Button(gpa_grad_frame, text="Set Graduation Status", command=set_grad_status, bg="#e1bee7").grid(row=2, column=2, padx=5, pady=5)

    def _create_system_tab(self, notebook):
        """创建系统操作标签页"""
        system_frame = tk.Frame(notebook, padx=10, pady=10)
        notebook.add(system_frame, text="System Operations")
        
        def delete_student():
            selection = self.student_listbox.curselection()
            if not selection:
                messagebox.showwarning("Prompt", "Please select a student first!")
                return
            stu_id = list(self.sms.students.keys())[selection[0]]
            student = self.sms.students[stu_id]
            if messagebox.askyesno("Confirmation", f"Are you sure to delete student {student.name}?"):
                self.sms.delete_student(stu_id)
                self.refresh_student_list()
                self.info_text.delete(1.0, tk.END)
        
        tk.Button(system_frame, text="Delete Selected Student", command=delete_student, bg="#ffcdd2", width=30).pack(pady=10)
        
        def calculate_overall_gpa():
            messagebox.showinfo("Overall GPA Statistics", self.sms.calculate_overall_gpa_average())
        
        tk.Button(system_frame, text="Calculate Average GPA of All Students", command=calculate_overall_gpa, bg="#fff3e0", width=35).pack(pady=10)