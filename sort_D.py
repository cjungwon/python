import json
import base64
import requests

'''
Name       : send_request_and_save()
Desc       : 이미지 파일의 데이터를 clova ocr로 추출하여 json 파일로 저장
Parameter  : image_file, clova_URL, clova_secret_key
Return     : 파일 저장
----------------------------------------
2021.10.07    최정원
'''

def send_request_and_save(image_file, clova_URL, clova_secret_key):
  
  file_slice = slice(image_file.find(".")+1, image_file.find(".")+5)
  image_format = image_file[file_slice]

  with open(image_file, "rb") as f:
    img = base64.b64encode(f.read())
  
  headers = {
    "Content-Type" : "application/json",
    "X-OCR-SECRET" : clova_secret_key
    }

  data = {
    "version" : "V2",
    "requestId" : "sample_id",
    "timestamp" : 0,
    "images" : [
      {
        "name" : "sample_image",
        "format" : image_format,
        "data" : img.decode('utf-8')
        }
        ]
        }

  data = json.dumps(data)
  response = requests.post(clova_URL, data=data, headers=headers)
  result = json.loads(response.text)
  # print(result)

  # json 파일 저장
  file_path = 'D:/test/id_R.json'
  
  with open(file_path, 'w') as f:
    json.dump(result, f)

'''
Name       : open_file_and_sort()
Desc       : json 파일 호출하여 신분증 종류 판별
Parameter  : json_file
Return     : 신분증 종류(면허증 or 주민등록증)
----------------------------------------
2021.10.07    최정원
'''

def open_file_and_sort(json_file):
  # json 파일 호출
  with open(json_file, 'r') as f:
    json_data = json.load(f)
  # print(json.dumps(json_data))

  res_array = json_data.get('images')
  for list in res_array:
    list_set = list.get('fields')

    for list_s in list_set:
      text = list_s.get('inferText')
      # print(text)

      if '자동차운전면허증' in text:
        print('면허증')
      if '주민등록증' in text:
        print('주민등록증')



image_file = input("image file : ")
  # D:/test/Mobile_D__sample.jpg
clova_URL = input("clova URL : ")
  # https://c56ee27ada0e4510bd40083285fd9382.apigw.ntruss.com/custom/v1/11509/d447f9082390144fb40087fa8850a5635871c863250e01dcf55789f4090fcb55/general
clova_secret_key = input("clova Secret Key : ")
  # VUVnY0tlcExkWVFHUHlxSkpPVkloVkx3SkVtcFpTbE4=
send_request_and_save(image_file, clova_URL, clova_secret_key)


json_file = input("json file : ")
  # D:/test/id_D.json
open_file_and_sort(json_file)
