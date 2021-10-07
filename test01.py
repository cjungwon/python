import json
import base64
import requests

with open("D:/test/movie.png", "rb") as f:
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
            "format" : "png",
            "data" : img.decode('utf-8')
        }
    ]
}

data = json.dumps(data)
response = requests.post(URL, data=data, headers=headers)
result = json.loads(response.text)

# print(result['images'])

resArray = result.get('images')
for list in resArray:
    list_set = list.get('fields')

    for list_s in list_set:
      print(list_s.get('inferText'))

