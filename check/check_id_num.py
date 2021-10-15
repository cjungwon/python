import re

class CheckIdNum:
    def __init__(self) -> None:
        pass

    '''
    Name       : extract_digit()
    Desc       : input_num에서 기호를 제외하고 13자리 숫자만 추출
    Parameter  : self
    Return     : id_num(13자리 숫자), 조건에 맞지 않으면 0 13개
    ----------------------------------------
    2021.10.15    최정원
    '''

    def extract_digit(self, input_num):

        if len(input_num) == 13 and input_num.isdigit():

            id_num = input_num
            return id_num

        elif len(input_num) == 14 and input_num[6].isdigit() == 0 and len(re.findall("\d", input_num)) == 13:

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

    def check_date_format(input_num):
        
        pass



    '''
    Name       : check_year_month_day()
    Desc       : 
    Parameter  : self
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

                if year % 4 ==0 and day <= 29: # 윤년일 때
                    return True
                elif year % 4 != 0 and day <= 28: # 윤년 아닐 때
                    return True
            
            elif month == 4 or 6 or 9 or 11:
                if day <= 30:
                    return True

            else:
                return True


    '''
    Name       : check_birthplace_num()
    Desc       : id_num의 8~9번째 숫자가 출생지역 번호에 맞게 주어졌는지 확인
    Parameter  : self
    Return     : 조건에 맞으면 id_num
    ----------------------------------------
    2021.10.15    최정원
    '''

    def check_birthplace_num(self, input_num):
        id_num = self.extract_digit(input_num)

        birthplace = int(id_num[7:9])
        if 0 <= birthplace <= 95:
            return True

            

    '''
    Name       : check_last_num()
    Desc       : id_num의 마지막 숫자가 앞의 12자리 숫자들의 식으로 만들어진 것인지 확인
    Parameter  : self
    Return     : 조건에 맞으면 id_num
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
            self.check_last_num(input_num) == True:
            print('주민번호 O')
        else:
            print('주민번호 X')
        



input_num = input("번호 입력: ")

check = CheckIdNum()

# check.result(input_num)


def test(input_num):

    no_blank = input_num.replace(" ", "")
    print(no_blank)

test(input_num)
    