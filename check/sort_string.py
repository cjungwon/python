import re

input_str = input('입력: ')

class ClassifyString:
    def __init__(self, input_str):
        self.input_str = input_str
        self.str_list = self.split_string()

    def split_string(self):
        str_list = list(self.input_str)
        return str_list

    def is_num(self):
        num = 0
        for n in range(len(self.str_list)):
            if self.str_list[n].isdigit():
                num = num + 1
        return num
    
    def is_eng(self):
        eng =0
        reg = re.compile(r'[a-z]')
        for n in range(len(self.str_list)):
            if reg.match(self.str_list[n]):
                eng = eng + 1
        return eng

    # 안됨
    def is_kor(self):
        kor = 0
        for n in range(len(self.str_list)):
            if self.str_list[n].encode().isalpha():
                kor = kor + 1
        return kor
    

str = ClassifyString(input_str)
print(str.is_kor())
