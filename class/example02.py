class Student:
    count = 0

    def __init__(self, name, korean, math, english, science):
        self.name = name
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science

        Student.count += 1
        print("{}번째 학생 생성".format(Student.count))
    
students = [
    Student("윤인성", 87, 98, 99, 95),
    Student("연하진", 92, 98, 96, 98),
    Student("구지연", 76, 96, 94, 90),
    Student("나선주", 80, 88, 94, 91),
    Student("윤아린", 85, 67, 72, 80),
    Student("윤명월", 94, 79, 88, 83)
]

print("현재 생성된 학생은 {}명".format(Student.count))



class Studentt:
    count = 0
    students = []

    @classmethod
    def print(cls):
        print("--학생 목록--")
        print("이름\t총점\t평균")
        for student in cls.students:
            print(str(student))
    
    def __init__(self, name, korean, math, english, science):
        self.name = name
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science

        Studentt.count += 1
        Studentt.students.append(self)

    def get_sum(self):
        return self.korean + self.math + self.english + self.science

    def get_average(self):
        return self.get_sum() / 4
    
    def __str__(self):
        return "{}\t{}\t{}".format(self.name, self.get_sum(), self.get_average())
    
Studentt("윤인성", 87, 98, 99, 95)
Studentt("연하진", 92, 98, 96, 98)
Studentt("구지연", 76, 96, 94, 90)
Studentt("나선주", 80, 88, 94, 91)
Studentt("윤아린", 85, 67, 72, 80)
Studentt("윤명월", 94, 79, 88, 83)

Studentt.print()



import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
    def get_circumference(self):
        return 2 * math.pi * self.radius
    def get_area(self):
        return math.pi * (self.radius ** 2)
    
    @property
    def radius(self):
        return self.__radius
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise TypeError("길이는 양수여야 함")
        self.__radius = value

circle = Circle(10)
# print("원의 둘레:", circle.get_circumference())
# print("원의 넓이:", circle.get_area())

print("원래 원의 반지름:", circle.radius)
circle.radius = 2
print("변경된 원의 반지름:", circle.radius)
# 예외 발생
circle.radius = -10 
