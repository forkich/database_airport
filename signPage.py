from PyQt5 import QtWidgets
from signIn import Ui_Form

class signPage(QtWidgets.QWidget):
    def __init__(self, previous_window, user, server):
        super(signPage, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.user = user
        self.server = server
        self.__previous_window = previous_window