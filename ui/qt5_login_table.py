import sys
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QDialog
from PyQt5.QtCore import Qt

_id_pw_list = {'id' : '', 'pw' : ''}
_id_pw_list['id'] = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff' ,'ggg', 'hhh', 'iii', 'jjj']
_id_pw_list['pw'] = ['111', '222', '333', '444', '555', '666' ,'777', '888', '999', '000']

class LoginTable(QWidget):
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
        table_id_pw = QTableWidget()
        table_id_pw.setRowCount(len(_id_pw_list['id']))
        table_id_pw.setColumnCount(len(_id_pw_list))
        table_id_pw.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_id_pw.setHorizontalHeaderLabels(['id', 'pw'])

        for i in range(len(_id_pw_list['id'])):
            table_id_pw.setItem(i, 0, QTableWidgetItem(_id_pw_list['id'][i]))
            table_id_pw.setItem(i, 1, QTableWidgetItem(_id_pw_list['pw'][i]))

        layout = QVBoxLayout()
        layout.addWidget(table_id_pw)
        self.list.setLayout(layout)
        
        self.list.setWindowTitle('ID-PW list')
        self.list.setWindowModality(Qt.NonModal)
        self.list.setGeometry(650, 200, 300, 400)
        self.list.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoginTable()
    sys.exit(app.exec_())