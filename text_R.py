import json

with open('./id_R.json', 'r') as f:
  json_data = json.load(f)
# print(json.dumps(json_data))


resArray = json_data.get('images')
for list in resArray:
    list_set = list.get('fields')
    # print(list_set)



name = list_set[1].get('inferText').replace("(", "").replace(")", "") + list_set[2].get('inferText')

id_num = list_set[3].get('inferText')

date = list_set[11].get('inferText') + list_set[12].get('inferText') + list_set[13].get('inferText')

print(" 이름 :", name, "\n", "주민등록번호 : ", id_num, "\n", "발행일 : ", date)     