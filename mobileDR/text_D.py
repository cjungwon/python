import json

'''
Name       : find_text_D()
Desc       : json 파일 호출하여 text data 추출
Parameter  : json_file
Return     : text data(면허증번호, 이름, 주민등록번호, 발행일)
----------------------------------------
2021.10.07    최정원
'''

def find_text_D(json_file):
  
  with open(json_file, 'r') as f:
    json_data_D = json.load(f)
    # print(json.dumps(json_data))

  # text index 찾기
  bar_index = []
  dot_index = []
  res_array = json_data_D.get('images')

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




json_file = input("json file : ")
  # D:/test/Mobile_D.json
find_text_D(json_file)
