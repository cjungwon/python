import sys, os
sys.path.insert(1, 'D:/test/sort')
sys.path.insert(1, 'D:/test/check')
import cv2
import base64
import requests
import json
import re
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTableWidget, QAbstractItemView, QTableWidgetItem, QLabel, QTextBrowser
from PyQt5.QtGui import QImage, QPixmap
from sorting import SortNum
from check_id_num import IDcardUtil
import math

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

        btn_sort = QPushButton('정렬', self)
        btn_sort.clicked.connect(self.sort_ybound)
        btn_sort.setGeometry(290, 10, 80, 40)

        btn_line = QPushButton('합치기', self)
        btn_line.clicked.connect(self.show_merge_result)
        btn_line.setGeometry(380, 10, 80, 40)

        btn_angle = QPushButton('각도', self)
        btn_angle.clicked.connect(self.check_angle)
        btn_angle.setGeometry(470, 10, 80, 40)

        btn_reset = QPushButton('Reset', self)
        btn_reset.clicked.connect(self.reset)
        btn_reset.setGeometry(910, 10, 80, 40)

        self.lbl_img = QLabel(self)
        self.lbl_img.move(20, 70)
        self.lbl_img.resize(700, 700)
        self.lbl_img.setStyleSheet("border : 2px black; border-style : solid;")

        self.merge_result = QTextBrowser(self)
        self.merge_result.move(750, 310)
        self.merge_result.resize(250, 220)
        self.merge_result.setStyleSheet("border : 2px black; border-style : solid;")

        self.result_item = QTextBrowser(self)
        self.result_item.move(750, 545)
        self.result_item.resize(250, 220)
        self.result_item.setStyleSheet("border : 2px black; border-style : solid;")

        self.table_file = QTableWidget(10, 1, self)
        self.table_file.resize(250, 230)
        self.table_file.move(750, 70)
        self.table_file.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_file.setHorizontalHeaderLabels(['File Name'])
        self.table_file.setColumnWidth(0, 200)
        self.table_file.cellClicked.connect(self.show_image)

        self.check_idnum = IDcardUtil()

        self.setWindowTitle('File')
        self.setGeometry(300, 150, 1050, 800)

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
        pixmap = pixmap.scaledToWidth(700)
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
            
    def show_merge_result(self):
        merged_text, merged_bound = self.merge_row()

        img = cv2.imread(self.picked_image, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for i in range(len(merged_text)):

            cv2.line(img, (int(merged_bound[i][0][0].get('x')), int(merged_bound[i][0][0].get('y'))), (int(merged_bound[i][len(merged_text[i]) -1][1].get('x')), int(merged_bound[i][len(merged_text[i]) -1][1].get('y'))), (0,0,255), 7)
            cv2.line(img, (int(merged_bound[i][len(merged_text[i]) -1][1].get('x')), int(merged_bound[i][len(merged_text[i]) -1][1].get('y'))), (int(merged_bound[i][len(merged_text[i]) -1][2].get('x')), int(merged_bound[i][len(merged_text[i]) -1][2].get('y'))), (0,0,255), 7)
            cv2.line(img, (int(merged_bound[i][len(merged_text[i]) -1][2].get('x')), int(merged_bound[i][len(merged_text[i]) -1][2].get('y'))), (int(merged_bound[i][0][3].get('x')), int(merged_bound[i][0][3].get('y'))), (0,0,255), 7)
            cv2.line(img, (int(merged_bound[i][0][0].get('x')), int(merged_bound[i][0][0].get('y'))), (int(merged_bound[i][0][3].get('x')), int(merged_bound[i][0][3].get('y'))), (0,0,255), 7)

        for m in range(len(self.list_fields)):
            text = str(m+1)
            bounding = self.list_fields[m].get('boundingPoly').get('vertices')
            cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[1].get('x')), int(bounding[1].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[1].get('x')), int(bounding[1].get('y'))), (int(bounding[2].get('x')), int(bounding[2].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[2].get('x')), int(bounding[2].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)

            cv2.putText(img, text, (int(bounding[0].get('x')), int(bounding[0].get('y'))), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 5 )

        qimage = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)

        pixmap_res = QPixmap(qimage)
        pixmap_res = pixmap_res.scaledToWidth(700)

        self.lbl_img.setPixmap(pixmap_res)
        
        cv2.destroyAllWindows()

        for n in range(len(merged_text)):
            merged_text[n] = ' '.join(merged_text[n])
            self.merge_result.append(merged_text[n])
        self.merge_result.append('')

    def check_angle(self):
        self.bound_text, self.bound_y, self.bound_xy = self.find_text_and_bound()

        standard_rad = math.atan2(int(self.bound_xy[0][1].get('y')) - int(self.bound_xy[0][0].get('y')), \
                int(self.bound_xy[0][1].get('x')) - int(self.bound_xy[0][0].get('x')) )
        standard_ang = (standard_rad * 180) / math.pi

        fine_angle= []
        for n in range(len(self.bound_xy)):
            rad = math.atan2(int(self.bound_xy[n][1].get('y')) - int(self.bound_xy[n][0].get('y')), \
                int(self.bound_xy[n][1].get('x')) - int(self.bound_xy[n][0].get('x')) )
            ang = (rad * 180) / math.pi

            if abs(standard_ang - ang) < 3:
                fine_angle.append(self.bound_xy[n])

        img = cv2.imread(self.picked_image, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for m in range(len(fine_angle)):

            cv2.line(img, (int(fine_angle[m][0].get('x')), int(fine_angle[m][0].get('y'))), (int(fine_angle[m][1].get('x')), int(fine_angle[m][1].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(fine_angle[m][1].get('x')), int(fine_angle[m][1].get('y'))), (int(fine_angle[m][2].get('x')), int(fine_angle[m][2].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(fine_angle[m][2].get('x')), int(fine_angle[m][2].get('y'))), (int(fine_angle[m][3].get('x')), int(fine_angle[m][3].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(fine_angle[m][0].get('x')), int(fine_angle[m][0].get('y'))), (int(fine_angle[m][3].get('x')), int(fine_angle[m][3].get('y'))), (255,0,0), 3)

        qimage = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)

        pixmap_res = QPixmap(qimage)
        pixmap_res = pixmap_res.scaledToWidth(700)

        self.lbl_img.setPixmap(pixmap_res)
            
        cv2.destroyAllWindows()

    def reset(self):
        self.merge_result.clear()
        self.result_item.clear()


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

    def find_text_and_bound(self):
        
        bound_text = []
        bound_y = []
        bound_xy = []

        for m in range(len(self.list_fields)):
            bounding = self.list_fields[m].get('boundingPoly').get('vertices')
            y_list = [bounding[0].get('y'), bounding[1].get('y'), bounding[2].get('y'), bounding[3].get('y')]

            bound_text.append(self.list_fields[m].get('inferText'))
            bound_y.append([min(y_list), max(y_list)])
            bound_xy.append(bounding)
        
        return bound_text, bound_y, bound_xy

    def show_all_item(self):
        json_file = self.picked_image[slice(0, self.picked_image.rfind(".") )] + '.json'
        self.list_fields = self.find_json_file_fields(json_file)

        img = cv2.imread(self.picked_image, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for m in range(len(self.list_fields)):
            text = str(m+1)
            bounding = self.list_fields[m].get('boundingPoly').get('vertices')
            cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[1].get('x')), int(bounding[1].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[1].get('x')), int(bounding[1].get('y'))), (int(bounding[2].get('x')), int(bounding[2].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[2].get('x')), int(bounding[2].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)
            cv2.line(img, (int(bounding[0].get('x')), int(bounding[0].get('y'))), (int(bounding[3].get('x')), int(bounding[3].get('y'))), (255,0,0), 3)

            cv2.putText(img, text, (int(bounding[0].get('x')), int(bounding[0].get('y'))), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 5 )

        qimage = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)

        pixmap_res = QPixmap(qimage)
        pixmap_res = pixmap_res.scaledToWidth(700)

        self.lbl_img.setPixmap(pixmap_res)
        
        cv2.destroyAllWindows()
    
    # 운전면허증 items
    def find_driver_license_item(self):

        self.result_item.append(self.picked_image  + ' : 운전면허증')
        self.result_item.append('면허번호 : ' + self.find_driver_license_num())
        self.result_item.append('이름 : ' + self.find_driver_license_name())

        if self.check_idnum.result(self.find_driver_license_idnum()) == True:
            self.result_item.append('주민등록번호 : ' + self.find_driver_license_idnum())
        else:
            self.result_item.append('주민등록번호 : 잘못된 번호')

        self.result_item.append('발행일 : ' + self.find_driver_license_date())
        self.result_item.append('')
    
    # 운전면허증 - 면허번호
    def find_driver_license_num(self):
    
        self.bound_text, self.bound_y, self.bound_xy = self.find_text_and_bound()

        self.bar_y_range = []
        for i in range(len(self.bound_text)):
            if '-' in self.bound_text[i]:
                self.bar_y_range.append(self.bound_y[i])
        
        lcnum_line = []
        for n in range(len(self.bound_text)):
            if self.bound_y[n][0] >= self.bar_y_range[0][0] - 10 and\
                self.bound_y[n][1] <= self.bar_y_range[0][1] + 10:
                lcnum_line.append(self.bound_text[n])
        lcnum = ' '.join(lcnum_line)

        return lcnum

    # 운전면허증 - 이름
    def find_driver_license_name(self):

        name_line = []
        for n in range(len(self.bound_text)):
            if self.bound_y[n][0] >= self.bar_y_range[0][1] - 10 and self.bound_y[n][1] <= self.bar_y_range[1][0] + 40:
                name_line.append(self.bound_text[n])
        name_line = ''.join(name_line)
        name_line_split = name_line.split(":")

        if len(name_line_split) == 1:
            name = re.compile('[가-힣]+').findall(name_line_split[0])
        elif len(name_line_split) > 1:
            name = re.compile('[가-힣]+').findall(name_line_split[1])
        
        return name[0]

    # 운전면허증 - 주민번호
    def find_driver_license_idnum(self):
        
        idnum_line = []
        for n in range(len(self.bound_text)):
            if self.bound_y[n][0] >= self.bar_y_range[1][0] - 10 and\
                self.bound_y[n][1] <= self.bar_y_range[1][1] + 10:
                idnum_line.append(self.bound_text[n])
        idnum = ''.join(idnum_line)
        idnum = re.findall(r'\d+', idnum)
        idnum = '-'.join(idnum)

        return idnum

    # 운전면허증 - 발행일
    def find_driver_license_date(self):

        dot_y_range = []
        for i in range(len(self.bound_text)):
            if '.' in self.bound_text[i]:
                dot_y_range.append(self.bound_y[i])

        date_line = []
        for n in range(len(self.bound_text)):
            if self.bound_y[n][0] >= dot_y_range[len(dot_y_range) - 1][0] - 30 and\
                self.bound_y[n][1] <= dot_y_range[len(dot_y_range) - 1][1] + 30:
                date_line.append(self.bound_text[n])

        date_line = ''.join(date_line)
        date_line = re.findall(r'\d+', date_line)
        date_line = ''.join(date_line)
        date = date_line[:4] + '.' + date_line[4:6] + '.' + date_line[6:] + '.'

        return date

    # 주민등록증 items
    def find_registration_card_item(self):

        self.result_item.append(self.picked_image + ' : 주민등록증')
        self.result_item.append('이름 : ' + self.find_registration_card_name())

        if self.check_idnum.result(self.find_registration_card_idnum()) == True:
            self.result_item.append('주민등록번호 : ' + self.find_registration_card_idnum())
        else:
            self.result_item.append('주민등록번호 : 잘못된 번호')

        self.result_item.append('발행일 : ' + self.find_registration_card_date())
        self.result_item.append('')

    # 주민등록증 - 이름
    def find_registration_card_name(self):
        self.bound_text, self.bound_y, self.bound_xy = self.find_text_and_bound()

        jumin_y_range = []
        self.bar_y_range = []
        for i in range(len(self.bound_text)):
            if '주민등록증' in self.bound_text[i]:
                jumin_y_range.append(self.bound_y[i])
            elif '-' in self.bound_text[i]:
                self.bar_y_range.append(self.bound_y[i])

        name_line = []
        for n in range(len(self.bound_text)):
            if self.bound_y[n][0] >= jumin_y_range[0][1] - 10 and self.bound_y[n][1] <= self.bar_y_range[0][0] + 40:
                name_line.append(self.bound_text[n])
        name_line = ''.join(name_line)
        name = name_line.split("(")[0] + name_line.split(")")[1]
        
        return name

    # 주민등록증 - 주민번호
    def find_registration_card_idnum(self):
        
        idnum_line = []
        for n in range(len(self.bound_text)):
            if self.bound_y[n][0] >= self.bar_y_range[0][0] - 10 and\
                self.bound_y[n][1] <= self.bar_y_range[0][1] + 10:
                idnum_line.append(self.bound_text[n])
        idnum = ''.join(idnum_line)
        idnum = re.findall(r'\d+', idnum)
        idnum = '-'.join(idnum)

        return idnum

    # 주민등록증 - 발행일
    def find_registration_card_date(self):

        dot_y_range = []
        for i in range(len(self.bound_text)):
            if '.' in self.bound_text[i]:
                dot_y_range.append(self.bound_y[i])
        
        date_line = []
        for n in range(len(self.bound_text)):
            if self.bound_y[n][0] >= dot_y_range[len(dot_y_range) - 1][0] - 30 and\
                self.bound_y[n][1] <= dot_y_range[len(dot_y_range) - 1][1] + 30:
                date_line.append(self.bound_text[n])
        
        date_line = ''.join(date_line).split(".")
        date_line = list(filter(None, date_line))
        date = '.'.join(date_line) + '.'

        return date

    def sort_ybound(self):
        self.bound_text, self.bound_y, self.bound_xy = self.find_text_and_bound()
        
        sort_num = SortNum()
        print(sort_num.selection_sort(self.bound_y))

    def merge_row(self):
        self.bound_text, self.bound_y, self.bound_xy = self.find_text_and_bound()

        merged_text = []
        merged_bound = []
        n=0
        while n < len(self.bound_text):
            line_text = []
            line_bound = []

            line_text.append(self.bound_text[n])
            line_bound.append(self.bound_xy[n])

            m = n + 1
            while m < len(self.bound_text):
                if abs(self.bound_y[n][0] - self.bound_y[m][0]) <= 50 and\
                    abs(self.bound_y[n][1] - self.bound_y[m][1]) <= 50:
                    line_text.append(self.bound_text[m])
                    line_bound.append(self.bound_xy[m])
                    m = m + 1
                else:
                    break
            n = m

            merged_text.append(line_text)
            merged_bound.append(line_bound)
        
        return merged_text, merged_bound


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = IDCard()
    win.show()
    sys.exit(app.exec_())

