import os
import json
import base64
import requests
import cv2


'''
Name       : send_request_and_save()
Desc       : 폴더 내 이미지 파일의 데이터를 clova ocr로 추출하여 json 파일로 저장
Parameter  : directory
Return     : 파일 저장
----------------------------------------
2021.10.08    최정원
'''

def send_request_and_save(directory):

    # 폴더 내 이미지 파일 찾기
    file_list = os.listdir(directory)

    image_file_list = []
    for n in range(len(file_list)):
        if 'jpg' in file_list[n]:
            image_file_list.append(file_list[n])

    clova_URL = 'https://c56ee27ada0e4510bd40083285fd9382.apigw.ntruss.com/custom/v1/11509/d447f9082390144fb40087fa8850a5635871c863250e01dcf55789f4090fcb55/general'
    clova_secret_key = 'VUVnY0tlcExkWVFHUHlxSkpPVkloVkx3SkVtcFpTbE4='

    # 이미지 파일 clova로 보내서 데이터 받기
    for n in range(len(image_file_list)):
        file_slice = slice(image_file_list[n].find(".")+1, image_file_list[n].find(".")+5)
        image_format = image_file_list[n][file_slice]
        
        with open(image_file_list[n], "rb") as f:
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
        
        # json 파일 저장
        file_path = 'D:/test/' + image_file_list[n][0:8] + '.json'
        
        with open(file_path, 'w') as f:
            json.dump(result, f)




'''
Name       : open_file_and_sort_idcard()
Desc       : 폴더 내 json 파일 호출하여 신분증 종류 판별 후, 필요한 데이터 추출
Parameter  : directory
Return     : 신분증 종류(면허증, 주민등록증), 필요한 데이터(면허번호, 이름, 주민번호, 발행일)
----------------------------------------
2021.10.08    최정원
'''

def open_file_and_sort_idcard(directory):

    # 폴더 내 json파일 찾기
    file_list = os.listdir(directory)
    json_file_list = []

    for n in range(len(file_list)):
        if 'json' in file_list[n]:
            json_file_list.append(file_list[n])

    # json 파일 호출하여 신분증 종류 판별
    for n in range(len(json_file_list)):
        with open(json_file_list[n], 'r') as f:
            json_data = json.load(f)
            # print(json.dumps(json_data))

        res_array = json_data.get('images')
        for list in res_array:
            list_set = list.get('fields')
        
            for list_s in list_set:
                text = list_s.get('inferText')

                # 면허증
                if '자동차운전면허증' in text:
                    print('\n' + json_file_list[n][slice(0, json_file_list[n].find("."))] + ' : 면허증')

                    bar_index = []
                    dot_index = []
                    res_array = json_data.get('images')
            
                    for list in res_array:
                        list_set = list.get('fields')

                    for n in range(len(list_set)):
                        if '-' in list_set[n].get('inferText'):
                            bar_index.append(n)
                        elif '.' in list_set[n].get('inferText'):
                            dot_index.append(n)

                    license_num = list_set[bar_index[0]].get('inferText')
                    name = list_set[bar_index[0] + 1].get('inferText')
                    id_num = list_set[bar_index[1]].get('inferText') + list_set[bar_index[1] + 1].get('inferText')
                    date = list_set[dot_index[len(dot_index) - 2]].get('inferText') + list_set[dot_index[len(dot_index) - 1]].get('inferText')
            
                    print(" 면허증번호 :", license_num, "\n", "이름 :", name, "\n", "주민등록번호 :", id_num, "\n", "발행일 :", date)


                # 주민등록증
                elif '주민등록증' in text:
                    print('\n' + json_file_list[n][slice(0, json_file_list[n].find("."))] + ' : 주민등록증')

                    date_index = []
                    res_array = json_data.get('images')

                    for list in res_array:
                        list_set = list.get('fields')
                    for n in range(len(list_set)):
                        if '주민등록증' in list_set[n].get('inferText'):
                            name_index = n + 1
                        
                        elif '-' in list_set[n].get('inferText'):
                            id_num_index = n
                        
                        elif '.' in list_set[n].get('inferText'):
                            date_index.append(n)

                    name = list_set[name_index].get('inferText').replace("(", "").replace(")", "") + list_set[name_index + 1].get('inferText')
                    id_num = list_set[id_num_index].get('inferText')
                    date = list_set[date_index[0]].get('inferText') + list_set[date_index[1]].get('inferText') + list_set[date_index[2]].get('inferText')
                
                    print(" 이름 :", name, "\n", "주민등록번호 :", id_num, "\n", "발행일 :", date)



'''
Name       : show_idcard_image()
Desc       : 폴더 내 json 파일 호출하여 신분증 종류 판별 후, 필요한 데이터의 위치 시각화
Parameter  : directory
Return     : 이미지 파일
----------------------------------------
2021.10.08    최정원
'''

def show_idcard_image(directory):
    # 폴더 내 json파일 찾기
    file_list = os.listdir(directory)

    json_file_list = []
    for n in range(len(file_list)):
        if 'json' in file_list[n]:
            json_file_list.append(file_list[n])

    # json 파일 호출하여 신분증 종류 판별
    for n in range(len(json_file_list)):
        with open(json_file_list[n], 'r') as f:
            json_data = json.load(f)
    
        res_array = json_data.get('images')
        for list in res_array:
            list_set = list.get('fields')
        
        for list_s in list_set:
            text = list_s.get('inferText')
            
            # 면허증
            if '자동차운전면허증' in text:
                
                image_file = directory + '/' + json_file_list[n][slice(0, json_file_list[n].find("s")-2)] + '__sample.jpg'

                bar_index = []
                dot_index = []

                for n in range(len(list_set)):
                    if '-' in list_set[n].get('inferText'):
                        bar_index.append(n)
                    elif '.' in list_set[n].get('inferText'):
                        dot_index.append(n)

                lecense_num_bounding1 = list_set[bar_index[0]].get('boundingPoly').get('vertices')[0]
                lecense_num_bounding2 = list_set[bar_index[0]].get('boundingPoly').get('vertices')[2]

                name_bounding1 = list_set[bar_index[0] + 1].get('boundingPoly').get('vertices')[0]
                name_bounding2 = list_set[bar_index[0] + 1].get('boundingPoly').get('vertices')[2]

                id_num_bounding1 = list_set[bar_index[1]].get('boundingPoly').get('vertices')[0]
                id_num_bounding2 = list_set[bar_index[1] + 1].get('boundingPoly').get('vertices')[2]

                date_bounding1 = list_set[dot_index[len(dot_index) - 2]].get('boundingPoly').get('vertices')[0]
                date_bounding2 = list_set[dot_index[len(dot_index) - 1]].get('boundingPoly').get('vertices')[2]

                img = cv2.imread(image_file, cv2.IMREAD_COLOR)

                # license_num
                cv2.rectangle(img, (int(lecense_num_bounding1.get('x')), int(lecense_num_bounding1.get('y'))),
                    (int(lecense_num_bounding2.get('x')), int(lecense_num_bounding2.get('y'))), (0, 0, 255), 2)
                # name
                cv2.rectangle(img, (int(name_bounding1.get('x')), int(name_bounding1.get('y'))),
                   (int(name_bounding2.get('x')), int(name_bounding2.get('y'))), (0, 0, 255), 2)
                # id_num
                cv2.rectangle(img, (int(id_num_bounding1.get('x')), int(id_num_bounding1.get('y'))),
                   (int(id_num_bounding2.get('x')), int(id_num_bounding2.get('y'))), (0, 0, 255), 2)
                # date
                cv2.rectangle(img, (int(date_bounding1.get('x')), int(date_bounding1.get('y'))),
                   (int(date_bounding2.get('x')), int(date_bounding2.get('y'))), (0, 0, 255), 2)

                cv2.namedWindow('Mobile_D', cv2.WINDOW_NORMAL)
                cv2.imshow('Mobile_D', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                cv2.imwrite('D:/test/Mobile_D_result.jpg', img)
            

            # 주민등록증
            elif '주민등록증' in text:

                image_file = directory + '/' + json_file_list[n][slice(0, json_file_list[n].find("s")-2)] + '__sample.jpg'

                date_index = []

                for n in range(len(list_set)):
                    if '주민등록증' in list_set[n].get('inferText'):
                        name_index = n + 1
                    elif '-' in list_set[n].get('inferText'):
                        id_num_index = n
                    elif '.' in list_set[n].get('inferText'):
                        date_index.append(n)

                name_bounding1 = list_set[name_index].get('boundingPoly').get('vertices')[0]
                name_bounding2 = list_set[name_index + 1].get('boundingPoly').get('vertices')[2]

                id_num_bounding1 = list_set[id_num_index].get('boundingPoly').get('vertices')[0]
                id_num_bounding2 = list_set[id_num_index].get('boundingPoly').get('vertices')[2]

                date_bounding1 = list_set[date_index[0]].get('boundingPoly').get('vertices')[0]
                date_bounding2 = list_set[date_index[2]].get('boundingPoly').get('vertices')[2]

                img = cv2.imread(image_file, cv2.IMREAD_COLOR)

                # name
                cv2.rectangle(img, (int(name_bounding1.get('x')), int(name_bounding1.get('y'))),
                    (int(name_bounding2.get('x')), int(name_bounding2.get('y'))), (0, 0, 255), 2)
                # id_num
                cv2.rectangle(img, (int(id_num_bounding1.get('x')), int(id_num_bounding1.get('y'))),
                    (int(id_num_bounding2.get('x')), int(id_num_bounding2.get('y'))), (0, 0, 255), 2)
                # date
                cv2.rectangle(img, (int(date_bounding1.get('x')), int(date_bounding1.get('y'))),
                   (int(date_bounding2.get('x')), int(date_bounding2.get('y'))), (0, 0, 255), 2)

                cv2.namedWindow('Mobile_R', cv2.WINDOW_NORMAL)
                cv2.imshow('Mobile_R', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                cv2.imwrite('D:/test/Mobile_R_result.jpg', img)



directory = input("folder : ")
    # D:/test

send_request_and_save(directory)
open_file_and_sort_idcard(directory)
show_idcard_image(directory)

