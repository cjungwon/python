import json

'''
Name       : find_text()
Desc       : json 파일 호출하여 신분증 종류 판별 후, text data 추출
Parameter  : json_file
Return     : text data(면허증 - 면허증번호, 이름, 주민등록번호, 발행일 / 주민등록증- 이름, 주민등록번호, 발행일)
----------------------------------------
2021.10.07    최정원
'''

def find_text(json_file):
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    res_array = json_data.get('images')
    for list in res_array:
        list_set = list.get('fields')

        for list_s in list_set:
            text = list_s.get('inferText')

            # 면허증
            if '자동차운전면허증' in text:

                bar_index = []
                dot_index = []
                res_array = json_data.get('images')
            
                for list in res_array:
                    list_set = list.get('fields')
                    # print(list_set)

                for n in range(len(list_set)):
                    if '-' in list_set[n].get('inferText'):
                        bar_index.append(n)
                    if '.' in list_set[n].get('inferText'):
                        dot_index.append(n)

                license_num = list_set[bar_index[0]].get('inferText')
                name = list_set[bar_index[0] + 1].get('inferText')
                id_num = list_set[bar_index[1]].get('inferText') + list_set[bar_index[1] + 1].get('inferText')
                date = list_set[dot_index[len(dot_index) - 2]].get('inferText') + list_set[dot_index[len(dot_index) - 1]].get('inferText')
            
                print(" 면허증번호 : ", license_num, "\n", "이름 :", name, "\n", "주민등록번호 : ", id_num, "\n", "발행일 : ", date)

            # 주민등록증
            if '주민등록증' in text:

                date_index = []
                res_array = json_data.get('images')

                for list in res_array:
                    list_set = list.get('fields')
                for n in range(len(list_set)):
                    if '주민등록증' in list_set[n].get('inferText'):
                        name_index = n + 1
                        # print(name_index)
                    if '-' in list_set[n].get('inferText'):
                        id_num_index = n
                        # print(id_num_index)
                    if '.' in list_set[n].get('inferText'):
                        date_index.append(n)

                name = list_set[name_index].get('inferText').replace("(", "").replace(")", "") + list_set[name_index + 1].get('inferText')
                id_num = list_set[id_num_index].get('inferText')
                date = list_set[date_index[0]].get('inferText') + list_set[date_index[1]].get('inferText') + list_set[date_index[2]].get('inferText')
                
                print(" 이름 :", name, "\n", "주민등록번호 : ", id_num, "\n", "발행일 : ", date)


json_file = input("json file : ")
    # D:/test/Mobile_D.json
    # D:/test/Mobile_R.json
find_text(json_file)
