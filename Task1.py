from abc import ABC, abstractmethod

class Person:
    def __init__(self, Name, ID, Email):
        self._Name = Name
        self._ID = ID
        self._Email = Email

class Student(Person):
    def __init__(self, Name, ID, Email, Enrollment_date, Course = None, GPA= 0.0):
        super().__init__(Name, ID, Email)
        self._Enrollment_date = Enrollment_date
        self._Course = Course if Course is not None else []
        self._GPA = GPA

    def get_role(self):
        return "Student"

    def get_id(self):
        return self._ID
    
    def get_email(self):
        return self._Email
    
    def change_email(self, new_email):
        self._Email = new_email
        print(f'The Email has been successfully changed to: {self._Email}.')
        return True
    
    def add_course(self, new_course):
        if new_course not in self._Course:
            print(f'You have successfully added, {new_course}.')
            self._Course.append(new_course)
        else:
            print(f'The course, {new_course} has been chosen.')
    
    def drop_course(self, drop_course):
        if drop_course not in self._Course:
            print('You have not yet chosen this course.')
        else:
            self._Course.remove(drop_course)
            print(f'The course, {drop_course} has been dropped.')
        
    def get_course(self):
        if self._Course:
            return f'{self._Name} selected course: {', '.join(self._Course)}'
        else:
            return 'You haven\'t selected any course'
        
class GraduateStudent(Student):
    def __init__(self, Name, ID, Email, Enrollment_date, Supervisor, Course = None, GPA= 0.0):
        super().__init__(Name, ID, Email, Enrollment_date, Course, GPA)
        self._Supervisor = Supervisor

    def get_role(self):
        return "Graduate Student"

student1 = Student(
    Name='Peter',
    ID='s12345678',
    Email='peter@student.com',
    Enrollment_date='2023-09-01',
    Course=['Math', 'English'],  
    GPA=3.8
)

student2 = Student(
    Name='John',
    ID='s12345679',
    Email='John@student.com',
    Enrollment_date='2024-09-01',
    Course=['Music', 'Sports'],  
    GPA=3.6
)

student3 = GraduateStudent(
    Name="Lisa",
    ID="s87654321",
    Email="lisa@student.com",
    Enrollment_date="2018-09-01",
    Supervisor="Prof. Wang",
    Course=["AI", "ML"],
    GPA=4.0
)

#Student1 testing
print(f"Student ID: {student1.get_id()}")

print(f"Student Email: {student1.get_email()}")

student1.change_email("peter_new@student.com") 
print(f"Updated Email: {student1.get_email()}")

student1.add_course("English")
student1.add_course("Math") 
print(f"Current Courses: {student1.get_course()}")

student1.drop_course('English')
student1.drop_course('Math')
print(f'Current Courses:{student1.get_course()}')

#Student2 testing

print(f"Student ID: {student2.get_id()}")

print(f"Student Email: {student2.get_email()}")

student2.change_email("John_new@student.com") 
print(f"Updated Email: {student2.get_email()}")

#测试如果没join course 的情况下 drop course
student2.drop_course('English')
student2.drop_course('Math')
print(f'Current Courses:{student2.get_course()}')

 
print(f"Lisa's role: {student3.get_role()}")
print(f"Peter's role: {student1.get_role()}")