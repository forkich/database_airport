from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from animalsYes import Ui_Form
from ticketsUPage import ticketsPage


class AnimalYesPage(QtWidgets.QWidget):
    def __init__(self, previous_window, user, server):
        super(AnimalYesPage, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.__previous_window = previous_window
        self.__animals_ids = []
        self.user = user
        self.server = server
        self.ui.add.clicked.connect(self.add)
        self.ui.nextBt.clicked.connect(self.next)
        self.ui.backBt.clicked.connect(self.back)
        self.animalsPrice = 0
        self.fill()

    @property
    def previous_window(self):
        return self.__previous_window

    @property
    def animals_ids(self):
        return self.__animals_ids

    def fill(self):
        exec_animals = "exec AnimalsByPassengerFull " + str(self.user[0])
        animals = self.server.execute_sql_full(exec_animals)
        if animals:
            for i in range(len(animals)):
                self.ui.comboBox.addItem(
                    "ID: " + str(animals[i][0]) + " Name: " + animals[i][1] + " Type: " + animals[i][
                        2] + " price: " + str(animals[i][3]))

    def add(self):
        text = self.ui.comboBox.currentText()
        self.__animals_ids.append(text[text.find("ID: ") + len("ID: "): text.find(" Name: ")])
        self.ui.listWidget.addItem(text.strip())
        index = self.ui.comboBox.findText(text)
        self.ui.comboBox.removeItem(index)

    def next(self):
        if self.__animals_ids:
            self.ticket_page = ticketsPage(self, self.user, self.server)
            self.ticket_page.show()
            self.hide()
        else:
            # error_dialog = QtWidgets.QErrorMessage()
            # error_dialog.showMessage('You haven not insert any animal!')
            msg = QMessageBox()
            #msg.setIcon(QMessageBox.Critical)
            msg.setText("Wow!")
            msg.setInformativeText("You haven't inserted any animal!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def back(self):
        self.__previous_window.show()
        self.close()

    def get_added_animals(self):
        self.added_animals = []
        for i in range(self.ui.listWidget.count()):
            self.added_animals.append(self.ui.listWidget.item(i).text())

        return self.added_animals
