from PyQt5 import QtWidgets
from forAnotherBuy import Ui_Form

class anotherBuyPage(QtWidgets.QWidget):
    def __init__(self, previous_window, user, server):
        super(anotherBuyPage, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.user = user
        self.server = server
        self.__previous_window = previous_window