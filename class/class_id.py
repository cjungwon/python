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


    '''
    Name       : make_file_list()
    Desc       : 폴더 내 원하는 종류의 파일들의 list 생성
    Parameter  : directory, file_type
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
    Parameter  : file_path, result_list
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
    Parameter  : directory, image_file_list, result_data, n
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
    Parameter  : directory
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
    Name       : open_file_and_sort_idcard()
    Desc       : 폴더 내 json 파일 호출하여 신분증  종류 판별 후, 필요한 데이터 추출
    Parameter  : directory
    Return     : 신분증 종류(면허증, 주민등록증), 필요한 데이터(면허번호, 이름, 주민번호, 발행일)
    ----------------------------------------
    2021.10.08    최정원
    '''

    def open_file_and_sort_idcard(self):

        # 폴더 내 json파일 찾기
        json_file_list = self.make_file_list('json')

        # json 파일 호출하여 신분증 종류 판별
        for n in range(len(json_file_list)):

            json_file = self.directory + '/' + json_file_list[n]
            with open(json_file, 'r') as f:
                json_data = json.load(f)

            list_images = json_data.get('images')
            for list in list_images:
                list_fields = list.get('fields')
            
            for list_s in list_fields:
                text = list_s.get('inferText')


                # 면허증
                if '자동차운전면허증' in text:
                    # print('\n' + json_file_list[n][slice(0, json_file_list[n].rfind("."))] + ' : 면허증')

                    bar_index = []
                    dot_index = []

                    for m in range(len(list_fields)):
                        if '-' in list_fields[m].get('inferText'):
                            bar_index.append(m)
                        elif '.' in list_fields[m].get('inferText'):
                            dot_index.append(m)

                    # name = list_fields[bar_index[0] + 1].get('inferText')

                    id_num_list = re.findall("\d+", list_fields[bar_index[1]].get('inferText'))
                    id_num = id_num_list[0] + '-' + id_num_list[1]
                
                    # issue_date = list_fields[dot_index[len(dot_index) - 2]].get('inferText') + list_fields[dot_index[len(dot_index) - 1]].get('inferText')

                    license_num = list_fields[bar_index[0]].get('inferText')

                    print(id_num, license_num)
        


                    # # CSV 파일로 저장
                    # Mobile_D_data = [name, id_num, issue_date, license_num]
                    # print(Mobile_D_data)

                    # save_csv_file(directory, json_file_list, Mobile_D_data, n)

                # 주민등록증
                elif '주민등록증' in text:
                    # print('\n' + json_file_list[n][slice(0, json_file_list[n].rfind("."))] + ' : 주민등록증')

                    bar_index = []
                    dot_index = []
                
                    for m in range(len(list_fields)):
                            
                        if '-' in list_fields[m].get('inferText'):
                            bar_index.append(m)
                        elif '.' in list_fields[m].get('inferText'):
                            dot_index.append(m)

                    # name = list_fields[bar_index[0] - 2].get('inferText').replace("(", "").replace(")", "") + list_fields[bar_index - 1].get('inferText')
                    id_num = list_fields[bar_index[0]].get('inferText')
                    # issue_date = list_fields[dot_index[0]].get('inferText') + list_fields[dot_index[1]].get('inferText') + list_fields[dot_index[2]].get('inferText')

                    print(id_num)
                    
                    # # CSV 파일로 저장
                    # Mobile_R_data = [name, id_num, issue_date, ]
                    # print(Mobile_R_data)

                    # save_csv_file(directory, json_file_list, Mobile_R_data, n)



    '''
    Name       : show_idcard_every_data()
    Desc       : 폴더 내 json 파일 호출하여 신분증 종류 판별 후, 모든 데이터의 위치 시각화
    Parameter  : directory
    Return     : 이미지 파일
    ----------------------------------------
    2021.10.12    최정원
    '''

    def show_idcard_every_data(self):
        # 폴더 내 json파일 찾기
        json_file_list = self.make_file_list('json')

        # json 파일 호출하여 신분증 종류 판별
        for n in range(len(json_file_list)):

            json_file = self.directory + '/' + json_file_list[n]
            with open(json_file, 'r') as f:
                json_data = json.load(f)
        
            list_images = json_data.get('images')
            for list in list_images:
                list_fields = list.get('fields')
            
            for list_s in list_fields:
                text = list_s.get('inferText')
                
                # 면허증
                if '자동차운전면허증' in text:
                    
                    image_file = self.directory + '/' + json_file_list[n][slice(0, json_file_list[n].rfind("."))] + '.jpg'
                    img = cv2.imread(image_file, cv2.IMREAD_COLOR)

                    for m in range(len(list_fields)):
                        bounding = list_fields[m].get('boundingPoly').get('vertices')
                        cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[1].get('x')), int(bounding[1].get('y'))), (255,0,0), 3)
                        cv2.line(img, (int(bounding[1].get('x')), int(bounding[1].get('y'))), (int(bounding[2].get('x')), int(bounding[2].get('y'))), (255,0,0), 3)
                        cv2.line(img, (int(bounding[2].get('x')), int(bounding[2].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)
                        cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)

                    cv2.namedWindow('Mobile_D', cv2.WINDOW_NORMAL)
                    cv2.imshow('Mobile_D', img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    # cv2.imwrite('D:/test/Mobile_D__sample_every_data.jpg', img)
                
                # 주민등록증
                elif '주민등록증' in text:

                    image_file = self.directory + '/' + json_file_list[n][slice(0, json_file_list[n].find("."))] + '.jpg'
                    img = cv2.imread(image_file, cv2.IMREAD_COLOR)

                    for m in range(len(list_fields)):
                        bounding = list_fields[m].get('boundingPoly').get('vertices')
                        cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[1].get('x')), int(bounding[1].get('y'))), (255,0,0), 3)
                        cv2.line(img, (int(bounding[1].get('x')), int(bounding[1].get('y'))), (int(bounding[2].get('x')), int(bounding[2].get('y'))), (255,0,0), 3)
                        cv2.line(img, (int(bounding[2].get('x')), int(bounding[2].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)
                        cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)
                        
                    cv2.namedWindow('Mobile_R', cv2.WINDOW_NORMAL)
                    cv2.imshow('Mobile_R', img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    # cv2.imwrite('D:/test/Mobile_R__sample_every_data.jpg', img)


    '''
    Name       : show_idcard_main_data()
    Desc       : 폴더 내 json 파일 호출하여 신분증 종류 판별 후, 필요한 데이터의 위치 시각화
    Parameter  : directory
    Return     : 이미지 파일
    ----------------------------------------
    2021.10.08    최정원
    '''

    def show_idcard_main_data(directory):
        # 폴더 내 json파일 찾기
        json_file_list = make_file_list(directory, 'json')

        # json 파일 호출하여 신분증 종류 판별
        for n in range(len(json_file_list)):

            json_file = directory + '/' + json_file_list[n]
            with open(json_file, 'r') as f:
                json_data = json.load(f)
        
            list_images = json_data.get('images')
            for list in list_images:
                list_fields = list.get('fields')
            
            for list_s in list_fields:
                text = list_s.get('inferText')
                
                # 면허증
                if '자동차운전면허증' in text:
                    
                    image_file = directory + '/' + json_file_list[n][slice(0, json_file_list[n].rfind("."))] + '.jpg'

                    bar_index = []
                    dot_index = []
                    
                    for n in range(len(list_fields)):
                        if '-' in list_fields[n].get('inferText'):
                            bar_index.append(n)
                        elif '.' in list_fields[n].get('inferText'):
                            dot_index.append(n)

                    lecense_num_bounding1 = list_fields[bar_index[0]].get('boundingPoly').get('vertices')[0]
                    lecense_num_bounding2 = list_fields[bar_index[0]].get('boundingPoly').get('vertices')[2]

                    name_bounding1 = list_fields[bar_index[0] + 1].get('boundingPoly').get('vertices')[0]
                    name_bounding2 = list_fields[bar_index[0] + 1].get('boundingPoly').get('vertices')[2]

                    id_num_bounding1 = list_fields[bar_index[1]].get('boundingPoly').get('vertices')[0]
                    id_num_bounding2 = list_fields[bar_index[1] + 1].get('boundingPoly').get('vertices')[2]

                    date_bounding1 = list_fields[dot_index[len(dot_index) - 2]].get('boundingPoly').get('vertices')[0]
                    date_bounding2 = list_fields[dot_index[len(dot_index) - 1]].get('boundingPoly').get('vertices')[2]

                    img = cv2.imread(image_file, cv2.IMREAD_COLOR)

                    # license_num
                    cv2.rectangle(img, (int(lecense_num_bounding1.get('x')), int(lecense_num_bounding1.get('y'))),
                        (int(lecense_num_bounding2.get('x')), int(lecense_num_bounding2.get('y'))), (0, 0, 255), 3)
                    # name
                    cv2.rectangle(img, (int(name_bounding1.get('x')), int(name_bounding1.get('y'))),
                    (int(name_bounding2.get('x')), int(name_bounding2.get('y'))), (0, 0, 255), 3)
                    # id_num
                    cv2.rectangle(img, (int(id_num_bounding1.get('x')), int(id_num_bounding1.get('y'))),
                    (int(id_num_bounding2.get('x')), int(id_num_bounding2.get('y'))), (0, 0, 255), 3)
                    # date
                    cv2.rectangle(img, (int(date_bounding1.get('x')), int(date_bounding1.get('y'))),
                    (int(date_bounding2.get('x')), int(date_bounding2.get('y'))), (0, 0, 255), 3)

                    cv2.namedWindow('Mobile_D', cv2.WINDOW_NORMAL)
                    cv2.imshow('Mobile_D', img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    cv2.imwrite('D:/test/Mobile_D__sample_main_data.jpg', img)
                

                # 주민등록증
                elif '주민등록증' in text:

                    image_file = directory + '/' + json_file_list[n][slice(0, json_file_list[n].rfind("."))] + '.jpg'

                    dot_index = []

                    for n in range(len(list_fields)):
                        if '-' in list_fields[n].get('inferText'):
                            bar_index = n
                        elif '.' in list_fields[n].get('inferText'):
                            dot_index.append(n)

                    name_bounding1 = list_fields[bar_index - 2].get('boundingPoly').get('vertices')[0]
                    name_bounding2 = list_fields[bar_index - 1].get('boundingPoly').get('vertices')[2]

                    id_num_bounding1 = list_fields[bar_index].get('boundingPoly').get('vertices')[0]
                    id_num_bounding2 = list_fields[bar_index].get('boundingPoly').get('vertices')[2]

                    date_bounding1 = list_fields[dot_index[0]].get('boundingPoly').get('vertices')[0]
                    date_bounding2 = list_fields[dot_index[2]].get('boundingPoly').get('vertices')[2]

                    img = cv2.imread(image_file, cv2.IMREAD_COLOR)

                    # name
                    cv2.rectangle(img, (int(name_bounding1.get('x')), int(name_bounding1.get('y'))),
                        (int(name_bounding2.get('x')), int(name_bounding2.get('y'))), (0, 0, 255), 3)
                    # id_num
                    cv2.rectangle(img, (int(id_num_bounding1.get('x')), int(id_num_bounding1.get('y'))),
                        (int(id_num_bounding2.get('x')), int(id_num_bounding2.get('y'))), (0, 0, 255), 3)
                    # date
                    cv2.rectangle(img, (int(date_bounding1.get('x')), int(date_bounding1.get('y'))),
                    (int(date_bounding2.get('x')), int(date_bounding2.get('y'))), (0, 0, 255), 3)

                    cv2.namedWindow('Mobile_R', cv2.WINDOW_NORMAL)
                    cv2.imshow('Mobile_R', img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    cv2.imwrite('D:/test/Mobile_R__sample_main_data.jpg', img)




recog = ClovaRecog('d:/id_card')

# print(recog.make_file_list('jpg'))
# recog.open_file_and_sort_idcard()
recog.show_idcard_every_data()