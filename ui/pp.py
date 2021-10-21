import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTableWidget, QAbstractItemView, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()
    
    def init_UI(self):
        btn_open = QPushButton('Open', self)
        btn_open.clicked.connect(self.file_open)
        btn_open.setGeometry(10, 10, 80, 40)

        self.table = QTableWidget()
        self.table.setRowCount(2)
        self.table.setColumnCount(2)


        self.table.setItem(0, 1, QTableWidgetItem('Banana'))
        self.table.setItem(1, 0, QTableWidgetItem('Orange'))
        self.table.setItem(1, 1, QTableWidgetItem('Grape'))
        self.table.setItem(0, 0, QTableWidgetItem('Apple'))
        # for i in range(len(self.file_name_list)):
        #     self.table.setItem(i, 0, QTableWidgetItem(self.file_name_list[i]))

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.setWindowTitle('File')
        self.setGeometry(200, 200, 1050, 700)

    def file_open(self):
        self.folder = QFileDialog.getExistingDirectory(self, 'Select Directory', 'D:/')
        
        self.file_name_list = os.listdir(self.folder)
        # print(self.file_name_list)

        # table_id_pw = QTableWidget()
        # table_id_pw.setRowCount(len(self.file_name_list))
        # table_id_pw.setColumnCount(1)
        # table_id_pw.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # table_id_pw.setHorizontalHeaderLabels(['file'])

        # for i in range(len(self.file_name_list)):
        #     table_id_pw.setItem(i, 0, QTableWidgetItem(self.file_name_list[i]))
            

        # layout = QVBoxLayout()
        # layout.addWidget(table_id_pw)
        
        
        




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    win.show()
    sys.exit(app.exec_())