import json

'''
Name       : find_text_R()
Desc       : json 파일 호출하여 text data 추출
Parameter  : json_file
Return     : text data(이름, 주민등록번호, 발행일)
----------------------------------------
2021.10.07    최정원
'''

def find_text_R(json_file):

  with open(json_file, 'r') as f:
    json_data_R = json.load(f)
    # print(json.dumps(json_data))

  # text index 찾기
  date_index = []
  res_array = json_data_R.get('images')

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
  # D:/test/Mobile_R.json
find_text_R(json_file)