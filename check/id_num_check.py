id_num = input("번호 입력: ")

if len(id_num) == 13 and id_num[:6].isdigit() and id_num[6:].isdigit():

    if 1 <= int(id_num[2:4]) <= 12:
        
        if 1 <= int(id_num[4:6]) <= 31:
            
            weight = '234567892345'
            res = 0
            for n in range(len(weight)):
                res = res + ( int(id_num[n]) * int(weight[n]) )
            if int(id_num[12]) == (11 - (res % 11)) % 10:
                print('ok')
                

            
        else:
            print('주민번호 아님')
    else:
        print('주민번호 아님')


