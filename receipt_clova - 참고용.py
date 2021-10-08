# pylint: disable-msg=E0611

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import matplotlib.pyplot as plt

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPixmap
import sys

import requests, uuid, time, json, os, datetime, argparse, io

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Clova Test")

        self.setMouseTracking(True)

        self.init_values()
        self.init_UI()

    # Init values
    def init_values(self):
        print("init_values")
        self.selected_index = 0

    # Init edit values
    def init_edit_values(self):
        print("Edit values")
        #self.edit_doc_type.setText("")

    # Set Global variables (image path)
    def set_global_variables(self):
        split_path = self.image_path.split('/')
        num = len(split_path)

        if num >= 1:
            filename = split_path[num - 1].split('.')

        print("filename:", filename)

        cnt = 0

        if len(filename) > 1:
            print(filename[0])

            dir = ""
            while cnt < (num - 1):
                # dir = dir + split_path[cnt]
                print(cnt, split_path[cnt])

                if cnt > 0:
                    dir += "\\"

                dir += split_path[cnt]
                cnt += 1

            json_path = dir
            json_path += "\\"
            json_path += filename[0]
            json_path += ".json"

            self.json_path = json_path

            save_path = dir
            save_path += "\\result_"
            save_path += filename[0]
            save_path += ".png"

            self.save_path = save_path

            print(save_path)

    # Init UI
    def init_UI(self):
        layout = QBoxLayout(QBoxLayout.TopToBottom)

        h_layout01 = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addLayout(h_layout01)

        h_layout02 = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addLayout(h_layout02)

        # Grid Layout
        grid_result_layout = QGridLayout()

        # h_layout01 (Init Buttons)
        label = QLabel("File Name")
        h_layout01.addWidget(label,0)

        btn_select_file = QPushButton("Select File")
        btn_select_file.clicked.connect(self.on_btn_select_file)
        h_layout01.addWidget(btn_select_file,0)

        self.combo_option = QComboBox(self)
        self.combo_option. addItem("Json File")
        self.combo_option. addItem("Naver Clova")
        self.combo_option.currentTextChanged.connect(self.on_combo_select)
        h_layout01.addWidget(self.combo_option)

        btn_show_result = QPushButton("Load Result")
        btn_show_result.clicked.connect(self.on_btn_show_result)
        h_layout01.addWidget(btn_show_result,0)

        scrollarea = QScrollArea()
        layout.addWidget(scrollarea)

        # h_layout02
        btn_find_keyword = QPushButton("Find Keyword")
        btn_find_keyword.clicked.connect(self.on_btn_find_keyword)

        h_layout02.addWidget(btn_find_keyword,0)
        h_layout02.addLayout(grid_result_layout)



        self.imgLbl = QLabel(self)
        self.imgLbl.resize(1200,800)
        scrollarea.resize(1200,800)
        scrollarea.setWidget(self.imgLbl)


        # Set Main layout
        self.setLayout(layout)

        self.resize(1200,900)
        self.show()

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        img_size = pixmap.size()

        # resize Control
        self.resize(img_size.width(), 1200)

        # resize Image
        pixmap = pixmap.scaledToWidth(img_size.width())

        self.imgLbl.resize(img_size.width(),img_size.height())
        self.imgLbl.setPixmap(QPixmap(pixmap))

    # Draw Rectangle to file
    def draw_clova_json_data_rect_to_image(self, image_path, json_data, save_path):
        font_size = 16

        img = Image.open(image_path)

        draw = ImageDraw.Draw(img)

        if len(image_path) < 1 :
            print("No Image path")
            return -1

        #version = json_data["version"]
        #requestId = json_data["requestId"]
        #timestamp = json_data["timestamp"]
        image_result = json_data["images"]

        for result_info in image_result:

            inferResult = result_info["inferResult"]
            message = result_info["message"]

            if inferResult == "SUCCESS":
                self.text_list = result_info["fields"]
                print("Json file Loaded")
            else:
                print("Json file Loaded fail! ",message)
                return -1

        cnt = 0

        for word_info in self.text_list:
            poly = word_info["boundingPoly"]
            #confidence = word_info["inferConfidence"]
            #lineBreak = word_info["lineBreak"]

            vertices = poly["vertices"]
            x1 = vertices[0]["x"]
            y1 = vertices[0]["y"]
            x2 = vertices[2]["x"]
            y2 = vertices[2]["y"]

            texts = word_info["inferText"]

            draw.rectangle(((x1, y1), (x2, y2)), outline=(0, 0, 255), width=4)
            draw.text((x1, y1 - font_size), texts, font=ImageFont.truetype(".\\font\\gulim.ttc", font_size), fill=(255, 0, 0))

            print(cnt, ":", texts)
            cnt += 1

        print(save_path)
        img.save(save_path)
        return 0


    def draw_clova_json_file_rect_to_image(self, image_path, json_path, save_path):
        font_size = 16

        img = Image.open(image_path)

        draw = ImageDraw.Draw(img)

        with open(self.json_path, encoding='UTF-8') as json_file:
            json_data = json.load(json_file)

            #version = json_data["version"]
            #requestId = json_data["requestId"]
            #timestamp = json_data["timestamp"]
            image_result = json_data["images"]

            for result_info in image_result:

                inferResult = result_info["inferResult"]
                message = result_info["message"]

                if inferResult == "SUCCESS":
                    self.text_list = result_info["fields"]
                    print("Json file Loaded")
                else:
                    print("Json file Loaded fail! ",message)
                    return

            cnt = 0

            for word_info in self.text_list:
                poly = word_info["boundingPoly"]
                #confidence = word_info["inferConfidence"]
                #lineBreak = word_info["lineBreak"]

                vertices = poly["vertices"]
                x1 = vertices[0]["x"]
                y1 = vertices[0]["y"]
                x2 = vertices[2]["x"]
                y2 = vertices[2]["y"]

                texts = word_info["inferText"]

                draw.rectangle(((x1, y1), (x2, y2)), outline=(0, 0, 255), width=4)
                draw.text((x1, y1 - font_size), texts, font=ImageFont.truetype(".\\font\\gulim.ttc", font_size), fill=(255, 0, 0))

                print(cnt, ":", texts)
                cnt += 1

            print(save_path)
            img.save(save_path)
            return 0

        return -1


    # 리턴값이 음수이면 상하 겹치는 영역이 없음
    def get_overlap_height(self, ay1, ay2, by1, by2 ):

        top = max(ay1,by1)
        bottom = min(ay2, by2)

        return bottom - top


    # 기준 영역의 오른쪽 영역을 모두 구함
    def find_right_item(self, bbox):

        find_word = ""
        bx1, by1, bx2, by2 = bbox
        bbox_msg = "\tKeyword bbox\t( bx1:{0}, by1:{1}, bx2:{2},by2:{3} )".format(bx1, by1, bx2, by2)
        print(bbox_msg)

        for text_info in self.text_list:
            x1, y1, x2, y2 = text_info["bbox"]
            text = text_info["texts"]

            if x1 == bx1 and x2 == bx2 and y1 == by1 and y2 == by2 :
                continue

            if by1 > y2 or by2 < y1 :
                continue
            else:
                if bx1 < x1 and bx2 < x1 :
                    bbox_msg = "\tKeyword bbox\t( bx1:{0}, by1:{1}, bx2:{2},by2:{3} )".format(bx1, by1, bx2, by2)
                    find_msg = "\tText bbox\t\t( x1:{0}, y1:{1}, x2:{2},y2:{3} {4})".format(x1, y1, x2, y2, text)
                    print(bbox_msg)
                    print(find_msg)

                    if len(find_word) > 0 :
                        find_word += " "
                    find_word += text

        print("*** Find Word:", find_word)
        return find_word

    # 기준 영역의 아래쪽 영역을 모두 구함
    def find_bottom_item(self, bbox):

        find_word = ""

        bx1, by1, bx2, by2 = bbox
        bbox_msg = "\tKeyword bbox\t( bx1:{0}, by1:{1}, bx2:{2},by2:{3} )".format(bx1, by1, bx2, by2)
        print(bbox_msg)

        for text_info in self.text_list:
            x1, y1, x2, y2 = text_info["bbox"]
            text = text_info["texts"]

            if x1 == bx1 and x2 == bx2 and y1 == by1 and y2 == by2 :
                continue # 자지자신은 비교할 필요없음

            overlap_height = self.get_overlap_height(by1,by2,y1,y2)

            if y1 > by2 :
                continue    # 비교영역보다 위쪽에 있으면 Skip

    def load_json(self):

        with open(self.json_path, encoding='UTF-8') as json_file:
            json_data = json.load(json_file)
            self.parse_naver_clova_json(json_data)


    def parse_naver_clova_json(self, json_data):

        version = json_data["version"]
        requestId = json_data["requestId"]
        timestamp = json_data["timestamp"]
        image_result = json_data["images"]

        for result_info in image_result:

            inferResult = result_info["inferResult"]
            message = result_info["message"]

            if inferResult == "SUCCESS":
                self.text_list = result_info["fields"]
                print("Json file Loaded")
            else:
                print("Json file Loaded fail!")



    def naver_clova_recog_image(self, image_path):
        api_url = "URL"
        secret_key = "KEY"

        request_json = {
            'images': [
                {
                    'format': 'jpg',
                    'name': 'demo'
                }
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }

        payload = {'message': json.dumps(request_json).encode('UTF-8')}

        files = [ ('file', open(image_path, 'rb')) ]
        headers = { 'X-OCR-SECRET': secret_key }

        print('{')

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        print('"요청 시각":"' + now + '",')

        response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        print('"응답 시각":"' + now + '",')

        print('"Result":')

        print('{')

        line1text = ""
        lineno = 1
        textsxlen = len(response.json()['images'][0]['fields'])
        # print(response.text.encode('utf8'))
        # print(response.text)

        for text in response.json()['images'][0]['fields']:
            line1text = line1text + text['inferText']
            print('"Line' + str(lineno + 1) + '":"' + ''.join(text['inferText']) + '",')
            # print('\n"{}"'.format(text['inferText']))
            lineno = lineno + 1

        print('"Line1":"' + ''.join(line1text) + '"')

        print('}')
        print('}')

        return response.json()



    ####################################################################################################################
    # Button Events
    ####################################################################################################################

    # On Select File
    def on_btn_select_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Select File','','png(*.png);;tif(*.tif);;All File(*)')
        file_path, filter = fname
        print("Select file:",file_path)

        if len(file_path) < 1:
            print("No input file!!!")
            return



        self.image_path = file_path
        self.set_global_variables()
        self.display_image(self.image_path)

        #self.init_edit_values()
        #self.load_json()

    # On Select Result
    def on_btn_show_result(self):

        if self.selected_index == 0 :
            # 이미 저장된 JSON파일 사용
            self.load_json()
            ret = self.draw_clova_json_file_rect_to_image(self.image_path, self.json_path, self.save_path)
            self.display_image(self.save_path)
        elif self.selected_index == 1 :
            # Naver Clova이용 
            recog_result = self.naver_clova_recog_image(self.image_path)
            ret = self.draw_clova_json_data_rect_to_image(self.image_path, recog_result, self.save_path)
            self.display_image(self.save_path)
        else:
            print("combo error")



    # On Load Json
    def on_btn_load_json(self):
        self.load_json()

    def on_btn_find_keyword(self):
        print("on_btn_find_keyword")

    # Add Lables for test
    def add_labels(self):
        layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(layout)

        label = QLabel("Label 1")
        layout.addWidget(label,0)
        label = QLabel("Label 2")
        layout.addWidget(label, 0)

        layout2 = QBoxLayout(QBoxLayout.TopToBottom)
        layout.addLayout(layout2)

        label = QLabel("Label 3")
        layout2.addWidget(label,0)
        label = QLabel("Label 4")
        layout2.addWidget(label,0)


    def on_combo_select(self):
        self.selected_index = self.combo_option.currentIndex()
        

    ################################################################################################################
    # Mouse event
    ################################################################################################################
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        print("pos", self.imgLbl.mapToParent(QtCore.QPoint(0, 0)))
        text = "Mouse Pressed x:{0}, y:{1}".format(event.x(), event.y())
        print(text)

# Application start  ----------------------------------------------------------------------#
app = QApplication(sys.argv)

screen = Window()
screen.show()
sys.exit(app.exec_())


