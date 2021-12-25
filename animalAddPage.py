from PyQt5 import QtWidgets
from animalAdd import Ui_Form
from utils import utils


class animalAddPage(QtWidgets.QWidget):
    def __init__(self, previous_window, user, server):
        super(animalAddPage, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.user = user
        self.server = server
        self.__previous_window = previous_window
        self.ui.decline.clicked.connect(self.decline)
        self.ui.add.clicked.connect(self.add)
        self.ui.comboBox.addItems(utils.get_list_items_id_name(self.server, "AnimalType"))

    def is_animal_already_exist(self, name, type):
        sql = f"SELECT id_animal from Animals WHERE name='{name}' AND id_passenger='{self.user[0]}' AND id_type='{type}';"
        if self.server.execute_is_exist(sql):
            utils.show_message("Wow!","That animal already exist!", "Error")
            return True
        else:
            return False

    def add(self):
        name = self.ui.lineEdit.text()
        type = self.ui.comboBox.currentText().strip()
        id_type = int(type[type.find("ID: ") + len("ID: "):type.find(" Name:")])
        if not name.replace(' ', '').replace('-', '').isalpha():
            utils.show_message("Oops!", "Insert in name line only strings", "Error")
        elif not self.is_animal_already_exist(name, id_type):
            values = [name, id_type, self.user[0]]
            sql_insert = ("INSERT INTO Animals (name, id_type, id_passenger) "
                          "VALUES (?, ?, ?);")
            self.server.execute_insert(sql_insert, values)
            self.ui.lineEdit.clear()
            utils.show_message("Successfully!", "You added new animal!", "Message")

    def decline(self):
        self.__previous_window.show()
        self.hide()