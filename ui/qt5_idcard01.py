import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QMessageBox, QTextBrowser
from PyQt5.QtGui import QImage, QPixmap
import cv2
import base64
import requests
import json
import re

_clova_URL = 'https://c56ee27ada0e4510bd40083285fd9382.apigw.ntruss.com/custom/v1/11509/d447f9082390144fb40087fa8850a5635871c863250e01dcf55789f4090fcb55/general'
_clova_secret_key = 'VUVnY0tlcExkWVFHUHlxSkpPVkloVkx3SkVtcFpTbE4='

class Clova(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()
    
    # Init UI
    def init_UI(self):
        btn_open = QPushButton('Open File', self)
        btn_open.clicked.connect(self.file_open_and_save_json)
        btn_open.setGeometry(10, 10, 80, 40)

        btn_result = QPushButton('->', self)
        btn_result.clicked.connect(self.show_result)
        btn_result.setGeometry(350, 200, 60, 40)

        btn_reset = QPushButton('Reset', self)
        btn_reset.clicked.connect(self.reset)
        btn_reset.setGeometry(150, 10, 80, 40)

        btn_item = QPushButton('Item', self)
        btn_item.clicked.connect(self.find_idcard_item)
        btn_item.setGeometry(10, 400, 80, 40)

        self.lbl_img = QLabel(self)
        self.lbl_img.move(30, 80)
        self.lbl_img.resize(300, 300)
        self.lbl_img.setStyleSheet("border  :2px black; border-style : solid;")

        self.lbl_result = QLabel(self)
        self.lbl_result.move(430, 80)
        self.lbl_result.resize(600,600)
        self.lbl_result.setStyleSheet("border  :2px black; border-style : solid;")
        
        self.text = QTextBrowser(self)
        self.text.setGeometry(30, 460, 300, 200)
        self.text.setStyleSheet("border  :2px black; border-style : solid;")

        self.setWindowTitle('File')
        self.setGeometry(200, 200, 1050, 700)

    # json 파일에서 'fields'값 찾기
    def json_file_fields(self):
        with open(self.json_file, 'r') as f:
            json_data = json.load(f)
        
        list_images = json_data.get('images')
        for list in list_images:
            list_fields = list.get('fields')
        
        return list_fields

    ####################################################################################################################
    # Button Events
    ####################################################################################################################

    # FileDialog 에서 선택한 파일 clova로 보내서 결과 json파일로 저장
    def file_open_and_save_json(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open File', 'D:/', 'Image File(*.jpg *.png)')
        
        self.image_file = self.fname[0]

        pixmap = QPixmap(self.image_file)
        pixmap = pixmap.scaledToWidth(300)
        self.lbl_img.setPixmap(pixmap)

        file_slice = slice(self.image_file.rfind(".")+1, self.image_file.rfind(".")+5)
        image_format = self.image_file[file_slice]

        # image 파일 clova로 보내기
        with open(self.image_file, "rb") as f:
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
        self.json_file = self.image_file[slice(0, self.image_file.rfind(".") )] + '.json'
            
        with open(self.json_file, 'w') as f:
            json.dump(result, f)

    # 이미지 안의 모든 text data
    def show_result(self):

        list_fields = self.json_file_fields()

        img = cv2.imread(self.image_file, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for m in range(len(list_fields)):
            bounding = list_fields[m].get('boundingPoly').get('vertices')
            cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[1].get('x')), int(bounding[1].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[1].get('x')), int(bounding[1].get('y'))), (int(bounding[2].get('x')), int(bounding[2].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[2].get('x')), int(bounding[2].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)

        qimage = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)

        pixmap_res = QPixmap(qimage)
        pixmap_res = pixmap_res.scaledToWidth(600)

        self.lbl_result.setPixmap(pixmap_res)
        
        cv2.destroyAllWindows()
    
    # 신분증 type / item
    def find_idcard_item(self):

        list_fields = self.json_file_fields()

        for list in list_fields:
            text = list.get('inferText')

            if '자동차운전면허증' in text:
                bar_index = []
                dot_index = []

                for m in range(len(list_fields)):
                    if '-' in list_fields[m].get('inferText'):
                        bar_index.append(m)
                    elif '.' in list_fields[m].get('inferText'):
                        dot_index.append(m)

                id_num_list = re.findall("\d+", list_fields[bar_index[1]].get('inferText'))
                id_num = id_num_list[0] + '-' + id_num_list[1]

                license_num = list_fields[bar_index[0]].get('inferText')

                self.text.append(self.image_file + ' : 운전면허증')
                self.text.append('면허번호 : ' + license_num)
                self.text.append('주민등록번호 : ' + id_num)
                self.text.append('')


            elif '주민등록증' in text:
                bar_index = []
                dot_index = []
                jumin_index = []
            
                for m in range(len(list_fields)):
                    if '-' in list_fields[m].get('inferText'):
                        bar_index.append(m)
                    elif '.' in list_fields[m].get('inferText'):
                        dot_index.append(m)
                    elif '주민등록증' in list_fields[m].get('inferText'):
                        jumin_index.append(m)
                
                id_num = list_fields[bar_index[0]].get('inferText')

                name = []
                for n in range(jumin_index[0]+1, bar_index[0]):
                    name.append(list_fields[n].get('inferText').split('(')[0])
                name = ''.join(name)
                
                issue_date = list_fields[dot_index[0]].get('inferText') + list_fields[dot_index[1]].get('inferText') + list_fields[dot_index[1]+1].get('inferText')

                self.text.append(self.image_file + ' : 주민등록증')
                self.text.append('주민등록번호 : ' + id_num)
                self.text.append('이름 : ' + name)
                self.text.append('발행일 : ' + issue_date)
                self.text.append('')
        
    def reset(self):
        self.lbl_img.clear()
        self.lbl_result.clear()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Clova()
    win.show()
    sys.exit(app.exec_())