from PyQt5 import QtWidgets

from managerFlightsPage import managerFlightsPage
from managerWindow import Ui_MainWindow
from utils import utils


class managerPage(QtWidgets.QMainWindow):
    def __init__(self, previousWindow, server):
        super(managerPage, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.server = server
        self.__previous_window = previousWindow
        self.ui.countydBtn.clicked.connect(self.add_country)
        self.ui.companyBtn.clicked.connect(self.add_company)
        self.ui.cityBtn.clicked.connect(self.add_city)
        self.ui.airportBtn.clicked.connect(self.add_airport)
        self.ui.planeBtn.clicked.connect(self.add_plane)
        self.ui.backBtn.clicked.connect(self.back)
        self.ui.addFlightBtn.clicked.connect(self.go_to_new_flight_page)
        self.ui.companyCb.addItems(self.get_list_items("Companies"))
        self.ui.countryCb.addItems(self.get_list_items("Countries"))
        self.ui.cityCb.addItems(self.get_list_items("Cities"))

    def is_country_already_exist(self, name):
        sql = f"SELECT id_country from Countries WHERE name='{name}';"
        if self.server.execute_is_exist(sql):
            utils.show_message("Wow!","That country already exist!", "Error")
            return True
        else:
            return False

    def is_city_already_exist(self, name, id_country):
        sql = f"SELECT id_city from Cities WHERE name='{name}' AND id_country='{id_country}';"
        if self.server.execute_is_exist(sql):
            utils.show_message("Wow!", "That city already exist!", "Error")
            return True
        else:
            return False

    def is_company_already_exist(self, name):
        sql = f"SELECT id_company from Companies WHERE name='{name}';"
        if self.server.execute_is_exist(sql):
            utils.show_message("Wow!", "That company already exist!", "Error")
            return True
        else:
            return False
    def is_airport_already_exist(self, name, id_city):
        sql = f"SELECT id_airport from Airports WHERE name='{name}' AND id_city='{id_city}';"
        if self.server.execute_is_exist(sql):
            utils.show_message("Wow!", "That airport already exist!", "Error")
            return True
        else:
            return False

    def is_plane_already_exist(self, individual_code, id_company):
        sql = f"SELECT id_plane from Planes WHERE individual_code='{individual_code}' AND id_company='{id_company}';"
        if self.server.execute_is_exist(sql):
            utils.show_message("Wow!", "That plane already exist!", "Error")
            return True
        else:
            return False

    def get_list_items(self, table):
        sql = "SELECT * FROM " + table
        items = self.server.execute_sql_full((sql))
        result = []
        for i in range(len(items)):
            result.append("ID: " + str(items[i][0]) + " Name: " + items[i][1])
        return result

    def add_city(self):
        name = self.ui.cityName.text()
        country = self.ui.countryCb.currentText().strip()
        id_country = int(country[country.find("ID: ") + len("ID: "):country.find(" Name: ")])
        if not name.replace(' ', '').replace('-', '').isalpha():
            utils.show_message("Oops!", "Insert in name line only strings", "Error")
        elif not self.is_city_already_exist(name, id_country):
            values = [name.upper(), id_country]
            sql_insert = ("INSERT INTO Cities (name, id_country) "
                          "VALUES (?, ?);")
            self.server.execute_insert(sql_insert, values)
            self.ui.cityName.clear()
            self.ui.cityCb.clear()
            self.ui.cityCb.addItems(self.get_list_items("Cities"))
            utils.show_message("Successfully!", "You added new city!", "Message")

    def add_country(self):
        name = self.ui.countyName.text()
        if not name.replace(' ', '').replace('-','').isalpha():
            utils.show_message("Oops!", "Insert in name line only strings", "Error")
        elif not self.is_country_already_exist(name):
            values = [name.upper()]
            sql_insert = ("INSERT INTO Countries (name) "
                          "VALUES (?);")
            self.server.execute_insert(sql_insert, values)
            self.ui.countryCb.clear()
            self.ui.countryCb.addItems(self.get_list_items("Countries"))
            self.ui.countyName.clear()
            utils.show_message("Successfully!", "You added new country!", "Message")

    def add_airport(self):
        name = self.ui.airportName.text()
        city = self.ui.cityCb.currentText().strip()
        id_city = int(city[city.find("ID: ") + len("ID: "):city.find(" Name: ")])
        if not name.replace(' ', '').replace('-', '').isalnum() or name.isnumeric():
            utils.show_message("Oops!", "Insert in name line only strings with numbers or just strings", "Error")
        elif not self.is_airport_already_exist(name, id_city):
            values = [id_city, name]
            sql_insert = ("INSERT INTO Airports (id_city, name) "
                          "VALUES (?, ?);")
            self.server.execute_insert(sql_insert, values)
            self.ui.airportName.clear()
            utils.show_message("Successfully!", "You added new airport!", "Message")

    def add_plane(self):
        try:
            volume = int(self.ui.volume.text())
            company = self.ui.companyCb.currentText().strip()
            id_company = company[company.find("ID: ") + len("ID: "):company.find(" Name: ")]
            individual_code = self.ui.idPlane.text()
            if not individual_code.replace(' ', '').replace('-', '').isalnum() or individual_code.isnumeric():
                utils.show_message("Oops!", "Insert in individual code line only strings with numbers or just strings", "Error")
            elif volume < 500 and volume > 0:
                if not self.is_plane_already_exist(individual_code, id_company):
                    values = [id_company, volume, individual_code.upper()]
                    sql_insert = ("INSERT INTO Planes (id_company, volume_seats, individual_code) "
                                  "VALUES (?, ?, ?);")
                    self.server.execute_insert(sql_insert, values)
                    self.ui.volume.clear()
                    self.ui.idPlane.clear()
                    utils.show_message("Successfully!", "You added new plane!", "Message")
            else:
                utils.show_message("Oops!", "Volume line available only for number less that 500", "Error")
        except:
            utils.show_message("Oops!", "Volume line available only for number less that 500", "Error")


    def add_company(self):
        name = self.ui.companyName.text()
        if not name.replace(' ', '').replace('-', '').isalnum() or name.isnumeric():
            utils.show_message("Oops!", "Insert in name line only strings with numbers or just strings", "Error")
        elif not self.is_company_already_exist(name):
            values = [name.upper()]
            sql_insert = ("INSERT INTO Companies (name) "
                          "VALUES (?);")
            self.server.execute_insert(sql_insert, values)
            self.ui.companyCb.clear()
            self.ui.companyCb.addItems(self.get_list_items("Companies"))
            self.ui.companyName.clear()
            utils.show_message("Successfully!", "You added new company!", "Message")

    def back(self):
        self.__previous_window.show()
        self.hide()

    def go_to_new_flight_page(self):
        self.manager_flights = managerFlightsPage(self, self.server)
        self.manager_flights.show()
        self.hide()