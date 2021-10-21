import os
import json
import base64
import requests
import cv2
import csv
import re

class ClovaRecog:

    def __init__(self, directory):
        self.directory = directory
        self.clova_URL = 'https://c56ee27ada0e4510bd40083285fd9382.apigw.ntruss.com/custom/v1/11509/d447f9082390144fb40087fa8850a5635871c863250e01dcf55789f4090fcb55/general'
        self.clova_secret_key = 'VUVnY0tlcExkWVFHUHlxSkpPVkloVkx3SkVtcFpTbE4='

        # self.json_file_list = self.send_request_and_save()
        

    '''
    Name       : make_file_list()
    Desc       : 폴더 내 원하는 종류의 파일들의 list 생성
    Parameter  : self, file_type
    Return     : file_list
    ----------------------------------------
    2021.10.08    최정원
    '''

    def make_file_list(self, file_type):
        files = os.listdir(self.directory)
        file_list = []

        for n in range(len(files)):
            if file_type in files[n]:
                file_list.append(files[n])
        
        return file_list

    '''
    Name       : save_csv_file()
    Desc       : result_list 를 csv 파일로 저장
    Parameter  : self, json_file_list, result_list, n
    Return     : 파일 저장
    ----------------------------------------
    2021.10.12    최정원
    '''

    def save_csv_file(self, json_file_list, result_list, n):
        file_path = self.directory + '/' + json_file_list[n][slice(0, json_file_list[n].rfind("."))] + '.csv'

        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(result_list)

    '''
    Name       : save_json_file()
    Desc       : result_data 를 json 파일로 저장
    Parameter  : self, image_file_list, result_data, n
    Return     : 파일 저장
    ----------------------------------------
    2021.10.12    최정원
    '''

    def save_json_file(self, image_file_list, result_data,n):
        file_path = self.directory + '/' + image_file_list[n][slice(0, image_file_list[n].rfind("."))] + '.json'
            
        with open(file_path, 'w') as f:
            json.dump(result_data, f)


    '''
    Name       : send_request_and_save()
    Desc       : 폴더 내 이미지 파일의 데이터를 clova ocr로 추출하여 json 파일로 저장
    Parameter  : self
    Return     : 파일 저장
    ----------------------------------------
    2021.10.08    최정원
    '''

    def send_request_and_save(self):

        # 폴더 내 이미지 파일 찾기
        image_file_list = self.make_file_list('jpg')

        # 이미지 파일 clova로 보내서 데이터 받기
        for n in range(len(image_file_list)):
            file_slice = slice(image_file_list[n].rfind(".")+1, image_file_list[n].rfind(".")+5)
            image_format = image_file_list[n][file_slice]

            image_file = self.directory + '/' + image_file_list[n]
            with open(image_file, "rb") as f:
                img = base64.b64encode(f.read())
            
            headers = {
                "Content-Type" : "application/json",
                "X-OCR-SECRET" : self.clova_secret_key
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
            response = requests.post(self.clova_URL, data=data, headers=headers)
            result = json.loads(response.text)
            
            # json 파일 저장
            self.save_json_file(image_file_list, result, n)


    '''
    Name       : open_file_and_save_bound()
    Desc       : json 파일 호출하여 text data의 좌표 찾기
    Parameter  : self
    Return     : text data와 그 좌표
    ----------------------------------------
    2021.10.14    최정원
    '''

    def open_file_and_save_bound(self):

        json_file_list = self.make_file_list('json')

        # json 파일 호출하여 신분증 종류 판별
        for n in range(len(json_file_list)):

            json_file = self.directory + '/' + json_file_list[n]
            with open(json_file, 'r') as f:
                json_data = json.load(f)

            list_images = json_data.get('images')
            for list_i in list_images:
                list_fields = list_i.get('fields')

            for list_f in list_fields:
                text = list_f.get('inferText')
            

                # 면허증
                if '자동차운전면허증' in text:
                    bounding_D = []
                    y_range_D = []
                    
                    for m in range(len(list_fields)):
                        bounding_D.append(list_fields[m].get('boundingPoly').get('vertices'))

                        y_list = [bounding_D[m][0].get('y'), bounding_D[m][1].get('y'), bounding_D[m][2].get('y'), bounding_D[m][3].get('y')]
                        y_range_D.append([min(y_list), max(y_list)])

                        text_bound_D = [list_fields[m].get('inferText'), y_range_D[m]]
                        # print(text_bound_D)
                    

                # 주민등록증
                elif '주민등록증' in text:
                    bounding_R = []
                    y_range_R = []
                    text_bound_R = {'text' : '', 'y_range' : ''}
                    
                    text_bound_R_text = []
                    text_bound_R_y = []
                    text_bound_R['text'] = text_bound_R_text
                    text_bound_R['y_range'] = text_bound_R_y
                    
                    for m in range(len(list_fields)):
                        bounding_R.append(list_fields[m].get('boundingPoly').get('vertices'))

                        y_list = [bounding_R[m][0].get('y'), bounding_R[m][1].get('y'), bounding_R[m][2].get('y'), bounding_R[m][3].get('y')]
                        y_range_R.append([min(y_list), max(y_list)])
                        
                        text_bound_R_text.append(list_fields[m].get('inferText'))
                        text_bound_R_y.append(y_range_R[m])
                        
                    # print(text_bound_R) 
                    # print(text_bound_R['text'][0])

                    for i in range(len(text_bound_R['text'])):
                        if '.' in text_bound_R['text'][i]:
                            print(text_bound_R['y_range'][i])
                    
                    
                    


recog = ClovaRecog('d:/id_card')

# recog.send_request_and_save()
recog.open_file_and_save_bound()