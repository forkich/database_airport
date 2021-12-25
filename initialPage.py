from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget

from adminPage import adminPage
from loginUPage import Login_user_window
from airlines import  Ui_MainWindow
from managerPage import managerPage


class Initial_window(QtWidgets.QMainWindow):
    def __init__(self, server):
        super(Initial_window, self).__init__()
        self.ui = Ui_MainWindow()
        self.server = server
        self.ui.setupUi(self)
        self.ui.userBtn.clicked.connect(self.go_to_user_window)
        self.ui.adminBtn.clicked.connect(self.go_to_admin_window)
        self.ui.managerBtn.clicked.connect(self.go_to_manager_window)
        self.center()

    def go_to_admin_window(self):
        self.admin_page = adminPage(self, self.server)
        self.admin_page.show()
        self.hide()

    def go_to_manager_window(self):
        self.manager_page = managerPage(self, self.server)
        self.manager_page.show()
        self.hide()

    def go_to_user_window(self):
        self.login_window = Login_user_window(self, self.server)
        self.login_window.show()
        self.hide()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())