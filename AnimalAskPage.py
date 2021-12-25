from PyQt5 import QtWidgets


from AnimalYesPage import AnimalYesPage
from animalsAsk import Ui_Dialog
from ticketsUPage import ticketsPage


class AnimalsAskPage(QtWidgets.QDialog):
    def __init__(self, previous_window, user, server):
        super(AnimalsAskPage, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.__previous_window = previous_window
        self.user = user
        self.server = server
        self.ui.yes.clicked.connect(self.go_yes)
        self.ui.no.clicked.connect(self.go_no)
        self.go_back_btn = QtWidgets.QPushButton(self)
        self.go_back_btn.setText("Go back")
        self.go_back_btn.setGeometry(20, 110, 111, 41)
        self.go_back_btn.clicked.connect(self.go_back)

    @property
    def previous_window(self):
        return self.__previous_window

    def go_back(self):
        self.__previous_window.show()
        self.hide()

    def go_yes(self):
        self.yes_page = AnimalYesPage(self, self.user, self.server)
        self.yes_page.show()
        self.hide()

    def go_no(self):
        self.ticket_page = ticketsPage(self, self.user, self.server)
        self.ticket_page.show()
        self.hide()