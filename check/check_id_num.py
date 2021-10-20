import re
from datetime import datetime
import string

class IDcardUtil:
    def __init__(self) -> None:
        pass

    '''
    Name       : extract_digit()
    Desc       : input_num에서 기호를 제외하고 13자리 숫자만 추출
    Parameter  : self, input_num
    Return     : id_num(13자리 숫자), 조건에 맞지 않으면 0 13개
    ----------------------------------------
    2021.10.15    최정원
    '''

    def extract_digit(self, input_num):

        if len(input_num) == 13 and input_num.isdigit():

            id_num = input_num
            return id_num

        elif len(input_num) > 13 and len(re.findall("\d", input_num)) == 13:

            input_num_digit = re.findall("\d", input_num)
            id_num = ''.join(input_num_digit)
            return id_num

        else:
            return '0000000000000'
            
    #split , 6, 8 ...
    # 2021.10.15 
    # 2021-10-15
    #  2021.1. 2 
    # 2021 12 05

    # 1. 앞뒤 기호문자 제거
    # 2. 문자열 중간 스페이스 제거
    # 3. .- 있는지

    '''
    Name       : check_date_format()
    Desc       : input_num이 날짜 형태에 부합하는지 확인
    Parameter  : self, input_num
    Return     : 조건에 맞으면 True
    ----------------------------------------
    2021.10.18    최정원
    '''

    def check_date_format(self, input_num):
 
        # no_blank = input_num.replace(" ", "") # 공백 제거
        no_blank = ''.join(input_num.split()) # 공백, 탭, cr, lf 제거
        split_num = no_blank.replace('-', '.').split('.') # -, . 으로 split
        num_list = list(filter(None, split_num))

        year = int(num_list[0])
        month = int(num_list[1])
        day = int(num_list[2])
            
        if len(str(year)) == 4 and year <= datetime.today().year:

            if month == 2:
                if year % 4 == 0 and 1 <= day <= 29: # 윤년일 때
                    return True
                elif year % 4 != 0 and 1 <= day <= 28: # 윤년 아닐 때
                    return True
            
            elif month in [4,6,9,11]:
                if 1 <= day <= 30:
                    return True

            elif month in [1,3,5,7,8,10,12]:
                if 1 <= day <= 31:
                    return True

        elif len(str(year)) == 2:

            if month == 2:
                if year % 4 == 0 and 1 <= day <= 29: # 윤년일 때
                    return True
                elif year % 4 != 0 and 1 <= day <= 28: # 윤년 아닐 때
                    return True
            
            elif month in [4,6,9,11]:
                if 1 <= day <= 30:
                    return True

            elif month in [1,3,5,7,8,10,12]:
                if 1 <= day <= 31:
                    return True


    '''
    Name       : check_year_month_day()
    Desc       : 생년월일을 나타내는 id_num의 1~6번째 숫자가 날짜 형태에 부합하는지 확인
    Parameter  : self, input_num
    Return     : 조건에 맞으면 True
    ----------------------------------------
    2021.10.15    최정원
    '''

    def check_year_month_day(self, input_num):
        id_num = self.extract_digit(input_num)

        year = int(id_num[0:2])
        month = int(id_num[2:4])
        day = int(id_num[4:6]) 

        if 1 <= month <= 12 and 1 <= day <= 31:
            
            if month == 2:

                if year % 4 == 0 and day <= 29: # 윤년일 때
                    return True
                elif year % 4 != 0 and day <= 28: # 윤년 아닐 때
                    return True
            
            elif month in [4,6,9,11]:
                if day <= 30:
                    return True

            else:
                return True


    '''
    Name       : check_birthplace_num()
    Desc       : 출생지역을 나타내는 id_num의 7,8번쨰 숫자가 범위 안에 포함되는지 확인
    Parameter  : self, input_num
    Return     : 조건에 맞으면 True
    ----------------------------------------
    2021.10.15    최정원
    '''

    def check_birthplace_num(self, input_num):
        id_num = self.extract_digit(input_num)

        birthplace = int(id_num[7:9])
        if 0 <= birthplace <= 95:
            return True


    '''
    Name       : check_year_and_gender_num()
    Desc       : 성별을 나타내는 id_num의 6번째 숫자에 맞는 연도인지 확인
    Parameter  : self, input_num
    Return     : 조건에 맞으면 True
    ----------------------------------------
    2021.10.15    최정원
    '''

    def check_year_and_gender_num(self, input_num):
        id_num = self.extract_digit(input_num)

        year = int(id_num[0:2])
        gender = int(id_num[6])
        
        if gender in [3,4,7,8]:  # 2000년대

            if 0 <= year <= int( datetime.today().strftime('%y') ):
                return True
        
        else:
            return True
        

    '''
    Name       : check_last_num()
    Desc       : id_num의 마지막 숫자가 앞의 12자리 숫자들의 식으로 만들어진 것인지 확인
    Parameter  : self, input_num
    Return     : 조건에 맞으면 True
    ----------------------------------------
    2021.10.15    최정원
    '''

    def check_last_num(self, input_num):
        id_num = self.extract_digit(input_num)

        weight = '234567892345'
        res = 0
        for n in range(len(weight)):
                res = res + ( int(id_num[n]) * int(weight[n]) )
                
        if int(id_num[12]) == (11 - (res % 11)) % 10:
            return True


    '''
    Name       : result()
    Desc       : id_num 이 모든 조건을 만족하는지 확인
    Parameter  : self
    Return     : 조건을 만족하면 '주민번호 O', 만족하지 않으면 '주민번호 X'
    ----------------------------------------
    2021.10.15    최정원
    '''

    def result(self, input_num):
        
        if self.check_year_month_day(input_num) == True and\
            self.check_birthplace_num(input_num) == True and\
            self.check_year_and_gender_num(input_num) == True and\
            self.check_last_num(input_num) == True:
            print('주민번호 O')
        else:
            print('주민번호 X')
        



input_num = input("번호 입력: ")

check = IDcardUtil()

check.result(input_num)

# print(check.check_date_format(input_num))

# print(re.findall("\d", input_num))