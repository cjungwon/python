import re

input_str = input('입력: ')

class ClassifyString:
    def __init__(self, input_str):
        self.input_str = input_str
        self.str_list = self.split_string()

    def split_string(self):
        str_list = list(self.input_str)
        return str_list

    def is_num(self): # 숫자
        num = 0
        for n in range(len(self.str_list)):
            if self.str_list[n].isdigit():
                num = num + 1
        return num
    
    def is_eng(self): # 영어
        eng = 0
        for n in range(len(self.str_list)):
            if ord('a') <= ord(self.str_list[n].lower()) <= ord('z'):
                eng = eng +1
        return eng

    def is_kor(self): # 한글
        kor = 0
        for n in range(len(self.str_list)):
            if ord('가') <= ord(self.str_list[n]) <= ord('힣'):
                kor = kor + 1
        return kor
    
    def is_mark(self): # 기호
        mark = 0
        for n in range(len(self.str_list)):
            if self.str_list[n].isalnum() == 0 and self.str_list[n] != ' ':
                mark = mark + 1
        return mark

    

    

str = ClassifyString(input_str)
print(str.is_mark())
