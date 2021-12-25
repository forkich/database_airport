from PyQt5 import QtWidgets
from animalDelete import Ui_Form

class animalDeletePage(QtWidgets.QWidget):
    def __init__(self, previous_window, user, server):
        super(animalDeletePage, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.user = user
        self.server = server
        self.__previous_window = previous_window
        self.ui.confirm.clicked.connect(self.delete)
        self.ui.decline.clicked.connect(self.back)


    def delete(self):
        self.__previous_window.delete_animal()
        self.__previous_window.show()
        self.close()

    def back(self):
        self.__previous_window.show()
        self.hide()