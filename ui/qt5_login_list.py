import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QPushButton, QWidget, QLabel, QLineEdit, QMessageBox, QDialog
from PyQt5.QtCore import Qt

_id_pw_list = {'id' : '', 'pw' : ''}
_id_pw_list['id'] = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff' ,'ggg', 'hhh', 'iii', 'jjj']
_id_pw_list['pw'] = ['111', '222', '333', '444', '555', '666' ,'777', '888', '999', '000']

class LoginList(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label_id = QLabel('ID :', self)
        label_id.move(40, 20)
        label_pw = QLabel('Password :', self)
        label_pw.move(20, 60)

        self.edit_id = QLineEdit(self)
        self.edit_id.move(95, 15)
        self.edit_pw = QLineEdit(self)
        self.edit_pw.move(95, 55)

        btn_login = QPushButton('Login', self)
        btn_login.move(40, 110)
        btn_login.clicked.connect(self.login)

        btn_reset = QPushButton('Reset', self)
        btn_reset.move(150, 110)
        btn_reset.clicked.connect(self.reset)

        btn_list = QPushButton('List', self)
        btn_list.move(150, 160)
        btn_list.clicked.connect(self.show_list)
        
        self.list = QDialog()
        

        self.setWindowTitle('Login')
        self.setGeometry(200, 200, 300, 250)
        self.show()
        
    def login(self):
        if self.edit_id.text() in _id_pw_list['id']:

            if self.edit_pw.text() in _id_pw_list['pw']:

                if _id_pw_list['id'].index(self.edit_id.text()) == _id_pw_list['pw'].index(self.edit_pw.text()):
                    QMessageBox.information(self, '로그인 완료', '로그인 되었습니다.')
                else:
                    QMessageBox.critical(self, '로그인 실패', '잘못된 Password입니다.')
            else:
                QMessageBox.critical(self, '로그인 실패', '잘못된 Password입니다.')
        else:
            QMessageBox.critical(self, '로그인 실패', '등록되지 않은 ID입니다.')
    
    def reset(self):
        self.edit_id.clear()
        self.edit_pw.clear()
    
    def show_list(self):
        label_lst_id = QLabel('ID', self.list)
        label_lst_id.move(65, 10)
        label_lst_pw = QLabel('Password', self.list)
        label_lst_pw.move(170, 10)

        self.list_id = QListWidget(self.list)
        self.list_id.resize(100, 150)
        self.list_id.move(20,30)
        self.list_id.clicked.connect(self.match)

        self.list_pw = QListWidget(self.list)
        self.list_pw.resize(100, 150)
        self.list_pw.move(150,30)

        for i in range(len(_id_pw_list['id'])):
            self.list_id.insertItem(i, _id_pw_list['id'][i])
        for j in range(len(_id_pw_list['pw'])):
            self.list_pw.insertItem(j, _id_pw_list['pw'][j])

        self.list.setWindowTitle('ID-PW list')
        self.list.setWindowModality(Qt.NonModal)
        self.list.setGeometry(650, 200, 300, 200)
        self.list.show()

    def match(self):
        
        print(self.list_id.currentRow())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoginList()
    sys.exit(app.exec_())