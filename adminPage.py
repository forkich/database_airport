from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from adminWindow import Ui_MainWindow
from utils import utils


class adminPage(QtWidgets.QMainWindow):
    def __init__(self, previousWindow, server):
        super(adminPage, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.server = server
        self.__previous_window = previousWindow
        self.ui.foodBtn.clicked.connect(lambda ch, table="Food": self.add_food_or_insurance(table))
        self.ui.insuranceBtn.clicked.connect(lambda ch, table="Insurance": self.add_food_or_insurance(table))
        self.ui.foodCb.addItems(self.get_food_or_insurance("Food"))
        self.ui.insuranceCb.addItems(self.get_food_or_insurance("Insurance"))
        self.ui.foodCb.activated.connect(self.update_tariff_price)
        self.ui.insuranceCb.activated.connect(self.update_tariff_price)
        self.ui.tariffBtn.clicked.connect(self.add_tariff)
        self.ui.showBtn.clicked.connect(self.show_list)
        self.ui.backBtn.clicked.connect(self.back)
        self.w = QWidget()
        self.update_tariff_price()

    def update_tariff_price(self):
        text_food = self.ui.foodCb.currentText()
        self.food_id = int(text_food[text_food.find("ID: ") + len("ID: "): text_food.find(" Name")])
        food_price = int(text_food[text_food.find("Price: ") + len("Price: "):])
        text_insurance = self.ui.insuranceCb.currentText()
        self.insurance_id = int(text_insurance[text_insurance.find("ID: ") + len("ID: "): text_insurance.find(" Name")])
        insurance_price = int(text_insurance[text_insurance.find("Price: ") + len("Price: "):])
        self.ui.tariffPrice.setText(str(1500 + food_price + insurance_price))

    def add_food_or_insurance(self, table):
        if table == "Food":
            name = self.ui.foodName.text()
            text_price = self.ui.foodPrice.text().strip()
        else:
            name = self.ui.insuranceName.text()
            text_price = self.ui.insurancePrice.text().strip()
        try:

            if text_price[0] == '0':
                utils.show_message("Oops!", "Price can't starts with zero!", "Error")
            price = int(text_price)
            if not name.replace(' ', '').isalpha():
                utils.show_message("Oops!", "Insert in name line only strings", "Error")
            else:
                values = [name.upper(), price]
                sql = ("INSERT INTO " + table + "(name, price) "
                                                "VALUES (?,?);")
                self.server.execute_insert(sql, values)
                if table == "Food":
                    self.ui.foodCb.clear()
                    self.ui.foodCb.addItems(self.get_food_or_insurance(table))
                    self.ui.foodName.clear()
                    self.ui.foodPrice.clear()
                    utils.show_message("Successfully!", "You added new food!", "Message")
                else:
                    self.ui.insuranceCb.clear()
                    self.ui.insuranceCb.addItems(self.get_food_or_insurance(table))
                    self.ui.insuranceName.clear()
                    self.ui.insurancePrice.clear()
                    utils.show_message("Successfully!", "You added new insurance!", "Message")
        except:
            utils.show_message("Oops!", "Insert in price line only numbers", "Error")

    def get_food_or_insurance(self, table):
        sql = "SELECT * FROM " + table
        items = self.server.execute_sql_full((sql))
        result = []
        for i in range(len(items)):
            result.append("ID: " + str(items[i][0]) + " Name: " + items[i][1] + " Price: " + str(items[i][2]))
        return result

    def add_tariff(self):
        sql = f"SELECT id_tariff from Tariff WHERE id_food='{self.food_id}' AND id_insurance = '{self.insurance_id}';"
        tariff = self.server.execute_sql_one(sql)
        if not tariff:
            try:
                price = int(self.ui.tariffPrice.text())
                values = [self.insurance_id, self.food_id, price]
                sql_insert = ("INSERT INTO Tariff (id_insurance, id_food, price) "
                              "VALUES (?,?, ?);")
                self.server.execute_insert(sql_insert, values)
                utils.show_message("Successfully!", "You added new tariff!", "Message")
            except:
                utils.show_message("Oops!", "Insert in price line only numbers", "Error")
        else:
            utils.show_message("Oops!", "You already have tariff like this!", "Error")

    def back(self):
        self.__previous_window.show()
        self.w.close()
        self.hide()

    def show_list(self):
        tariffs = self.server.execute_sql_full("exec allTariffs")
        self.scroll = QVBoxLayout()
        for i in range(len(tariffs)):
            temp = QtWidgets.QLabel(
                "ID: " + str(tariffs[i][0]) + "  Insurance: " + tariffs[i][1] + "  Food: " + tariffs[i][2] +
                "  Price: " + str(tariffs[i][3]))
            self.scroll.addWidget(temp)
        self.w.setWindowTitle("Tariffs")
        self.w.setLayout(self.scroll)
        self.w.show()
