from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit

from loginUser import Ui_Form
from userUPage import userPage
from utils import utils


class Login_user_window(QtWidgets.QWidget):
    def __init__(self, previous_window, server):
        super(Login_user_window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.server = server
        self.__previousWindow = previous_window
        self.ui.loginBtn.clicked.connect(self.loginBtn)
        self.ui.backBtn.clicked.connect(self.back)
        self.ui.leLogin.setPlaceholderText("login")
        self.ui.lePass.setPlaceholderText("password")
        self.ui.lePass.setEchoMode(QLineEdit.Password)

    def back(self):
        self.__previousWindow.show()
        self.hide()

    def loginBtn(self):
        input_login = self.ui.leLogin.text()
        input_password = self.ui.lePass.text()
        authentication = f"SELECT id_passenger, firstname, surname, patronymic, passport_code from Passengers WHERE login='{input_login}' AND password = '{input_password}';"
        user = self.server.execute_sql_one(authentication)
        if not user:
            utils.show_message("Oops!", "Login failed, Please try again!", "Error")
        else:
            self.ui.leLogin.clear()
            self.ui.lePass.clear()
            self.go_to_user_page(user)

    def go_to_user_page(self, user):
        self.user_page = userPage(self, user, self.server)
        self.user_page.show()
        self.hide()
