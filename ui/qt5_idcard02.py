import sys
import os
import cv2
import base64
import requests
import json
import re
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTableWidget, QAbstractItemView, QTableWidgetItem, QLabel, QTextBrowser
from PyQt5.QtGui import QImage, QPixmap
from check.check_id_num import IDcardUtil

_clova_URL = 'https://c56ee27ada0e4510bd40083285fd9382.apigw.ntruss.com/custom/v1/11509/d447f9082390144fb40087fa8850a5635871c863250e01dcf55789f4090fcb55/general'
_clova_secret_key = 'VUVnY0tlcExkWVFHUHlxSkpPVkloVkx3SkVtcFpTbE4='

class IDCard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()
    
    def init_UI(self):
        btn_folder = QPushButton('폴더', self)
        btn_folder.clicked.connect(self.open_folder)
        btn_folder.setGeometry(20, 10, 80, 40)

        btn_recog = QPushButton('인식', self)
        btn_recog.clicked.connect(self.recog_image_and_show_items)
        btn_recog.setGeometry(110, 10, 80, 40)

        btn_result = QPushButton('결과', self)
        btn_result.clicked.connect(self.find_idcard_item)
        btn_result.setGeometry(200, 10, 80, 40)

        self.lbl_img = QLabel(self)
        self.lbl_img.move(20, 70)
        self.lbl_img.resize(600, 600)
        self.lbl_img.setStyleSheet("border : 2px black; border-style : solid;")

        self.result_item = QTextBrowser(self)
        self.result_item.move(650, 350)
        self.result_item.resize(250, 318)
        self.result_item.setStyleSheet("border : 2px black; border-style : solid;")

        self.table_file = QTableWidget(10, 1, self)
        self.table_file.resize(250, 250)
        self.table_file.move(650, 70)
        self.table_file.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_file.setHorizontalHeaderLabels(['File Name'])
        self.table_file.setColumnWidth(0, 200)
        self.table_file.cellClicked.connect(self.show_image)

        self.setWindowTitle('File')
        self.setGeometry(200, 200, 950, 700)

#############################################################################################
# Button Event  

    def open_folder(self):
        self.folder = QFileDialog.getExistingDirectory(self, 'Select Directory', 'D:/')

        self.file_all_type = os.listdir(self.folder)

        # png file list
        self.img_file_list = []
        for n in range(len(self.file_all_type)):
            if 'png' in self.file_all_type[n]:
                self.img_file_list.append(self.file_all_type[n])
        
        for i in range(len(self.img_file_list)):
            self.table_file.setItem(i, 0, QTableWidgetItem(self.img_file_list[i]))
        
    def show_image(self):
        self.picked_image = self.folder + '/' + self.table_file.selectedItems()[0].text()

        pixmap = QPixmap(self.picked_image)
        pixmap = pixmap.scaledToWidth(600)
        self.lbl_img.setPixmap(pixmap)
    
    def recog_image_and_show_items(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        # self.json_file = self.request_clova_and_save_json()
        self.show_all_item()

        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def find_idcard_item(self):
        type = 0
        for list in self.list_fields:
            text = list.get('inferText')

            if '자동차운전면허증' in text:
                type = 1
                break
            elif '주민등록증' in text:
                type = 2
                break

        if type == 1:
            self.find_driver_license_item()
        elif type == 2:
            self.find_registration_card_item()

#############################################################################################



    def request_clova_and_save_json(self):
        file_slice = slice(self.picked_image.rfind(".")+1, self.picked_image.rfind(".")+5)
        image_format = self.picked_image[file_slice]

        # image 파일 clova로 보내기
        with open(self.picked_image, "rb") as f:
            img = base64.b64encode(f.read())
        
        headers = {
            "Content-Type" : "application/json",
            "X-OCR-SECRET" : _clova_secret_key
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
        response = requests.post(_clova_URL, data=data, headers=headers)
        result = json.loads(response.text)
        
        # json 파일 저장
        self.json_file = self.picked_image[slice(0, self.picked_image.rfind(".") )] + '.json'
            
        with open(self.json_file, 'w') as f:
            json.dump(result, f)

        return self.json_file

    # json 파일에서 'fields'값 찾기
    def find_json_file_fields(self, json_file):
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        
        list_images = json_data.get('images')
        for list in list_images:
            list_fields = list.get('fields')
        
        return list_fields

    def show_all_item(self):
        json_file = self.picked_image[slice(0, self.picked_image.rfind(".") )] + '.json'
        self.list_fields = self.find_json_file_fields(json_file)

        img = cv2.imread(self.picked_image, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for m in range(len(self.list_fields)):
            bounding = self.list_fields[m].get('boundingPoly').get('vertices')
            cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[1].get('x')), int(bounding[1].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[1].get('x')), int(bounding[1].get('y'))), (int(bounding[2].get('x')), int(bounding[2].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[2].get('x')), int(bounding[2].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)

        qimage = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)

        pixmap_res = QPixmap(qimage)
        pixmap_res = pixmap_res.scaledToWidth(600)

        self.lbl_img.setPixmap(pixmap_res)
        
        cv2.destroyAllWindows()
    
    # 운전면허증 items
    def find_driver_license_item(self):
        bar_index = []
        dot_index = []

        for m in range(len(self.list_fields)):
            if '-' in self.list_fields[m].get('inferText'):
                bar_index.append(m)
            elif '.' in self.list_fields[m].get('inferText'):
                dot_index.append(m)

        id_num_list = re.findall("\d+", self.list_fields[bar_index[1]].get('inferText'))
        id_num = id_num_list[0] + '-' + id_num_list[1]

        self.result_item.append(self.picked_image  + ' : 운전면허증')
        self.result_item.append('면허번호 : ' + self.find_driver_license_num())
        self.result_item.append('이름 : ' + self.find_driver_license_name())
        self.result_item.append('주민등록번호 : ' + id_num)
        self.result_item.append('발행일 : ' + self.find_driver_license_date())
        self.result_item.append('')
    
    # 운전면허증 - 면허번호
    def find_driver_license_num(self):

        self.bound_D_text = []
        self.bound_D_y = []

        for m in range(len(self.list_fields)):
            bounding_D = self.list_fields[m].get('boundingPoly').get('vertices')
            y_list = [bounding_D[0].get('y'), bounding_D[1].get('y'), bounding_D[2].get('y'), bounding_D[3].get('y')]

            self.bound_D_y.append([min(y_list), max(y_list)])
            self.bound_D_text.append(self.list_fields[m].get('inferText'))
    
        self.bar_y_range = []
        for i in range(len(self.bound_D_text)):
            if '-' in self.bound_D_text[i]:
                self.bar_y_range.append(self.bound_D_y[i])
        
        lcnum_line = []
        for n in range(len(self.bound_D_text)):
            if self.bound_D_y[n][0] >= self.bar_y_range[0][0] - 10 and\
                self.bound_D_y[n][1] <= self.bar_y_range[0][1] + 10:
                lcnum_line.append(self.bound_D_text[n])
        lcnum = ' '.join(lcnum_line)

        return lcnum

    # 운전면허증 - 이름
    def find_driver_license_name(self):

        name_line = []
        for n in range(len(self.bound_D_text)):
            if self.bound_D_y[n][0] >= self.bar_y_range[0][1] - 10 and self.bound_D_y[n][1] <= self.bar_y_range[1][0] + 40:
                name_line.append(self.bound_D_text[n])
        name_line = ''.join(name_line)
        name_line_split = name_line.split(":")

        if len(name_line_split) == 1:
            name = re.compile('[가-힣]+').findall(name_line_split[0])
        elif len(name_line_split) > 1:
            name = re.compile('[가-힣]+').findall(name_line_split[1])
        
        return name[0]

    # 운전면허증 - 발행일
    def find_driver_license_date(self):

        dot_y_range = []
        for i in range(len(self.bound_D_text)):
            if '.' in self.bound_D_text[i]:
                dot_y_range.append(self.bound_D_y[i])

        date_line = []
        for n in range(len(self.bound_D_text)):
            if self.bound_D_y[n][0] >= dot_y_range[len(dot_y_range) - 1][0] - 10 and\
                self.bound_D_y[n][1] <= dot_y_range[len(dot_y_range) - 1][1] + 10:
                date_line.append(self.bound_D_text[n])

        date_line = ''.join(date_line)
        date_line = date_line.replace('.', '')
        date = date_line[:4] + '.' + date_line[4:6] + '.' + date_line[6:] + '.'

        return date

    # 주민등록증 items
    def find_registration_card_item(self):
        bar_index = []
        dot_index = []
        jumin_index = []
    
        for m in range(len(self.list_fields)):
            if '-' in self.list_fields[m].get('inferText'):
                bar_index.append(m)
            elif '.' in self.list_fields[m].get('inferText'):
                dot_index.append(m)
            elif '주민등록증' in self.list_fields[m].get('inferText'):
                jumin_index.append(m)
        
        id_num = self.list_fields[bar_index[0]].get('inferText')

        name = []
        for n in range(jumin_index[0]+1, bar_index[0]):
            name.append(self.list_fields[n].get('inferText').split('(')[0])
        name = ''.join(name)
        
        issue_date = self.list_fields[dot_index[0]].get('inferText') + self.list_fields[dot_index[1]].get('inferText') + self.list_fields[dot_index[1]+1].get('inferText')

        self.result_item.append(self.picked_image + ' : 주민등록증')
        self.result_item.append('이름 : ' + name)
        self.result_item.append('주민등록번호 : ' + id_num)
        self.result_item.append('발행일 : ' + issue_date)
        self.result_item.append('')
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = IDCard()
    win.show()
    sys.exit(app.exec_())