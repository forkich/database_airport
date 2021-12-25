from PyQt5 import QtWidgets
from askBuy import Ui_Form

class askBuyPage(QtWidgets.QWidget):
    def __init__(self, previous_window, user, server):
        super(askBuyPage, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.user = user
        self.server = server
        self.__previous_window = previous_window