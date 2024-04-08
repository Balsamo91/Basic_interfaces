# Basic on how to use a class

class Student:
    def __init__(self, firstname, lastname, year=1, group="A"):
        self.firstname = firstname
        self.lastname = lastname
        self.year = year
        self.group = group

    def __str__(self):
        return f"Student: {self.firstname} {self.lastname}" # this is like print(f"Student: {student_1.firstname} {student_1.lastname}")
    
    def __int__(self):
        return self.year
    
    def __bool__(self):
        return self.year > 1
    

student_1 = Student("Adam", "Something")
student_2 = Student("John", "Doe", 3)

print(student_1)
print(student_2)


print(int(student_1))


if student_2:
    print("Student no longer in first year")

else:
    print("First year of studies")