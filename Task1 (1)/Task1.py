from abc import ABC, abstractmethod
import re
import json
from datetime import datetime

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_student_id(student_id):
    pattern = r'^s\d{8}$'
    return re.match(pattern, student_id) is not None

def format_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

class Person:
    def __init__(self, name, id_num, email):
        if not name.strip():
            raise ValueError("Name cannot be empty!")
        if not validate_student_id(id_num):
            raise ValueError("Invalid student ID format (must start with 's' followed by 8 digits, e.g., s12345678)!")
        if not validate_email(email):
            raise ValueError("Invalid email format!")
        
        self._name = name.strip()
        self._id = id_num
        self._email = email

    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, new_email):
        if validate_email(new_email):
            self._email = new_email
            print(f"✅ Email updated to: {self._email}")
        else:
            raise ValueError("❌ Invalid email format, update failed!")

class Student(Person):
    def __init__(self, name, id_num, email, enrollment_date, courses=None, gpa=0.0):
        super().__init__(name, id_num, email)
        
        self._enrollment_date = format_date(enrollment_date)
        if not self._enrollment_date:
            raise ValueError("❌ Invalid enrollment date format (must be YYYY-MM-DD)!")
        
        self._courses = courses if isinstance(courses, list) else []
        self._course_grades = {}
        self._gpa = self._validate_gpa(gpa)
        self._is_graduated = False

    def _validate_gpa(self, gpa):
        gpa = float(gpa)
        if 0.0 <= gpa <= 4.0:
            return gpa
        raise ValueError("❌ GPA must be between 0.0 and 4.0!")

    def get_role(self):
        return "Undergraduate Student"

    def add_course(self, course_name):
        course_name = course_name.strip()
        if not course_name:
            print("❌ Course name cannot be empty!")
            return False
        if course_name not in self._courses:
            self._courses.append(course_name)
            print(f"✅ Successfully added course: {course_name}")
            return True
        print(f"⚠️ Course {course_name} already exists, no need to add again")
        return False

    def drop_course(self, course_name):
        course_name = course_name.strip()
        if course_name in self._courses:
            self._courses.remove(course_name)
            if course_name in self._course_grades:
                del self._course_grades[course_name]
            print(f"✅ Successfully dropped course: {course_name}")
            return True
        print(f"❌ Course {course_name} not found, deletion failed")
        return False

    def get_courses(self):
        if self._courses:
            return f"📚 Enrolled courses for {self.name}: {', '.join(self._courses)}"
        return f"📚 {self.name} has no enrolled courses"

    def update_gpa(self, new_gpa):
        self._gpa = self._validate_gpa(new_gpa)
        print(f"✅ GPA for {self.name} updated to: {self._gpa}")

    def get_gpa_grade(self):
        if self._gpa >= 3.8:
            return "A+"
        elif self._gpa >= 3.5:
            return "A"
        elif self._gpa >= 3.2:
            return "B+"
        elif self._gpa >= 2.8:
            return "B"
        elif self._gpa >= 2.5:
            return "C"
        elif self._gpa >= 2.0:
            return "D"
        else:
            return "F"

    def set_course_grade(self, course_name, grade):
        course_name = course_name.strip()
        grade = float(grade)
        if course_name not in self._courses:
            print(f"❌ Course {course_name} not enrolled, cannot set grade")
            return False
        if 0 <= grade <= 100:
            self._course_grades[course_name] = grade
            print(f"✅ Grade for course {course_name} set to: {grade}")
            return True
        print(f"❌ Grade must be between 0 and 100!")
        return False

    def get_course_average_grade(self):
        if not self._course_grades:
            return f"📊 {self.name} has no course grade records"
        avg_grade = sum(self._course_grades.values()) / len(self._course_grades)
        return f"📊 Average course grade for {self.name}: {avg_grade:.2f}"

    def set_graduation_status(self, is_graduated):
        self._is_graduated = bool(is_graduated)
        status = "Graduated" if self._is_graduated else "Not Graduated"
        print(f"✅ Graduation status for {self.name} updated to: {status}")

    def check_graduation_eligibility(self, min_gpa=2.0, min_courses=3):
        if self._gpa >= min_gpa and len(self._courses) >= min_courses:
            return f"✅ {self.name} meets graduation requirements (GPA: {self._gpa}, Number of enrolled courses: {len(self._courses)})"
        return f"❌ {self.name} does not meet graduation requirements (requires GPA≥{min_gpa} and at least {min_courses} enrolled courses)"

    def get_student_info(self):
        info = f"""
========== Student Information ==========
Name: {self.name}
ID: {self.id}
Email: {self.email}
Enrollment Date: {self._enrollment_date.strftime('%Y-%m-%d')}
Role: {self.get_role()}
GPA: {self._gpa} (Grade: {self.get_gpa_grade()})
Enrolled Courses: {', '.join(self._courses) if self._courses else 'None'}
Course Grades: {self._course_grades if self._course_grades else 'None'}
Graduation Status: {'Graduated' if self._is_graduated else 'Not Graduated'}
=========================================
        """
        return info

class StudentManagementSystem:
    def __init__(self):
        self.students = {} 

    def add_student(self, student):
        if not isinstance(student, Student):
            print("❌ Only Student type objects can be added!")
            return False
        if student.id in self.students:
            print(f"❌ Student ID {student.id} already exists, addition failed")
            return False
        self.students[student.id] = student
        print(f"✅ Successfully added student: {student.name} (ID: {student.id})")
        return True

    def delete_student(self, student_id):#del student by id
        if student_id in self.students:
            deleted_student = self.students.pop(student_id)
            print(f"✅ Successfully deleted student: {deleted_student.name} (ID: {student_id})")
            return True
        print(f"❌ Student ID {student_id} not found, deletion failed")
        return False

    def list_all_students(self):
        if not self.students:
            return "📋 No student records"
        result = "📋 All Students List:\n"
        for idx, (stu_id, student) in enumerate(self.students.items(), 1):
            result += f"{idx}. Name: {student.name} | ID: {stu_id} | Role: {student.get_role()} | GPA: {student._gpa}\n"
        return result

    def calculate_overall_gpa_average(self):
        if not self.students:
            return "📊 No student records, cannot calculate average GPA"
        total_gpa = sum(student._gpa for student in self.students.values())
        avg_gpa = total_gpa / len(self.students)
        return f"📊 Average GPA of all students: {avg_gpa:.2f}"

    def save_to_file(self, file_path="students_data.json"):
        data = {}
        for stu_id, student in self.students.items():
            student_data = {
                "name": student.name,
                "id": student.id,
                "email": student.email,
                "enrollment_date": student._enrollment_date.strftime('%Y-%m-%d'),
                "courses": student._courses,
                "gpa": student._gpa,
                "course_grades": student._course_grades,
                "is_graduated": student._is_graduated,
                "role": student.get_role()
            }
            data[stu_id] = student_data
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Student data saved to: {file_path}")

    def load_from_file(self, file_path="students_data.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"❌ File {file_path} does not exist, loading failed")
            return False
        
        self.students.clear()
        for stu_id, student_data in data.items():
            student = Student(
                name=student_data["name"],
                id_num=student_data["id"],
                email=student_data["email"],
                enrollment_date=student_data["enrollment_date"],
                courses=student_data["courses"],
                gpa=student_data["gpa"]
            )

            student._course_grades = student_data["course_grades"]
            student._is_graduated = student_data["is_graduated"]
            self.students[stu_id] = student
        
        print(f"✅ Successfully loaded {len(self.students)} student records from {file_path}")
        return True

if __name__ == "__main__":
    sms = StudentManagementSystem()

    try:
        student1 = Student(
            name="Peter",
            id_num="s12345678",
            email="peter@student.com",
            enrollment_date="2023-09-01",
            courses=["Math", "English"],
            gpa=3.8
        )
        student2 = Student(
            name="John",
            id_num="s12345679",
            email="john@student.com",
            enrollment_date="2024-09-01",
            courses=["Music", "Sports"],
            gpa=3.6
        )
    except ValueError as e:
        print(e)

