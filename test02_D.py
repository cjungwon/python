import json
import base64
import requests

with open("./Mobile_D__sample.jpg", "rb") as f:
    img = base64.b64encode(f.read())

URL = "https://c56ee27ada0e4510bd40083285fd9382.apigw.ntruss.com/custom/v1/11509/d447f9082390144fb40087fa8850a5635871c863250e01dcf55789f4090fcb55/general"

KEY = "VUVnY0tlcExkWVFHUHlxSkpPVkloVkx3SkVtcFpTbE4="

headers = {
    "Content-Type" : "application/json",
    "X-OCR-SECRET" : KEY
}

data = {
    "version" : "V2",
    "requestId" : "sample_id",
    "timestamp" : 0,
    "images" : [
        {
            "name" : "sample_image",
            "format" : "jpg",
            "data" : img.decode('utf-8')
        }
    ]
}

data = json.dumps(data)
response = requests.post(URL, data=data, headers=headers)
result = json.loads(response.text)

# print(result)

# print(result['images'])

file_path = 'id_D.json'

with open(file_path, 'w') as f:
  json.dump(result, f)


with open('./id_D.json', 'r') as f:
  json_data = json.load(f)
# print(json.dumps(json_data))


resArray = json_data.get('images')
for list in resArray:
    list_set = list.get('fields')

    for list_s in list_set:
      text = list_s.get('inferText')
      # print(text)

      if '자동차운전면허증' in text:
        print('면허증')
      if '주민등록증' in text:
        print('주민등록증')
