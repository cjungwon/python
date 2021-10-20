import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QTextEdit, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
import os

qt_path= os.path.dirname(PyQt5.__file__)
os.environ['QT_PLUGIN_PATH'] = os.path.join(qt_path, "Qt/plugins")

class File(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.button = QPushButton('Open File', self)
        self.button.clicked.connect(self.file_open)
        self.button.setGeometry(10, 10, 100, 50)

        self.label = QLabel(self)
        
        self.setWindowTitle('File')
        self.setGeometry(200, 200, 200, 200)

    def file_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '', 'Image File(*.jpg *.png)')
        
        #pixmap = QPixmap(fname[0])

        pixmap = QPixmap()
        pixmap = pixmap.scaledToWidth(500)
        if pixmap.load(fname[0]):        
            print("loaded successfully!")
        
       
        self.label.setPixmap(pixmap)
        self.label.setContentsMargins(10, 50, 500, 500)

        # self.label.resize(pixmap.width(), pixmap.height())

        # self.resize(pixmap.width(), pixmap.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = File()
    win.show()
    sys.exit(app.exec_())