class StudentA:
    def __init__(self, name, korean, math, english, science):
        self.name = name
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science
    
    def get_sum(self):
        return self.korean + self.math +\
            self.english + self.science
    
    def get_average(self):
        return self.get_sum() / 4

    def to_string(self):
        return "{}\t{}\t{}".format(self.name, self.get_sum(), self.get_average())

    def __str__(self):
        return "{}\t{}\t{}".format(self.name, self.get_sum(), self.get_average())

    def __eq__(self, value):
        return self.get_sum() == value.get_sum()
    def __ne__(self, value):
        return self.get_sum() != value.get_sum()
    def __gt__(self, value):
        return self.get_sum() > value.get_sum()
    def __ge__(self, value):
        return self.get_sum() >= value.get_sum()
    def __lt__(self, value):
        return self.get_sum() < value.get_sum()
    def __le__(self, value):
        return self.get_sum() <= value.get_sum()
        

students = [
    StudentA("윤인성", 87, 98, 99, 95),
    StudentA("연하진", 92, 98, 96, 98),
    StudentA("구지연", 76, 96, 94, 90),
    StudentA("나선주", 80, 88, 94, 91),
    StudentA("윤아린", 85, 67, 72, 80),
    StudentA("윤명월", 94, 79, 88, 83)
]

student_a = StudentA("윤인성", 87, 98, 99, 95),
student_b = StudentA("연하진", 92, 98, 96, 98),

# print(students[3].name)
# print(students[2].english)

print(student_a != student_b)
print(student_a >= student_b)


for student in students:
    # print(student.to_string())
    print(str(student))


class Test:
    def __init__(self, name):
        self.name = name
        print('{} - 생성'.format(self.name))
    def __del__(self):
        print('{} - 파괴'.format(self.name))

test = Test("A")

print(isinstance(student, StudentA))
print(type(student) == StudentA)



class StudentA:
    def study(self):
        print('공부를 합니다.')

class Teacher:
    def teach(self):
        print('가르칩니다.')

classroom = [StudentA(), StudentA(), Teacher(), StudentA()]

for person in classroom:
    if isinstance(person, StudentA):
        person.study()
    elif isinstance(person, Teacher):
        person.teach()