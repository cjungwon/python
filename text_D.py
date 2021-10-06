import json

with open('./id_D.json', 'r') as f:
  json_data = json.load(f)
# print(json.dumps(json_data))


resArray = json_data.get('images')
for list in resArray:
    list_set = list.get('fields')
    # print(list_set)


d_num = list_set[4].get('inferText')

name = list_set[5].get('inferText')

id_num = list_set[6].get('inferText') + list_set[7].get('inferText')

date = list_set[31].get('inferText') + list_set[32].get('inferText')

print(" 면허증번호 : ", d_num, "\n", "이름 :", name, "\n", "주민등록번호 : ", id_num, "\n", "발행일 : ", date)     
