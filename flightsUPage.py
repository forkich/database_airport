from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout
from flightsPage import Ui_MainWindow as flightsPageMain
from AnimalAskPage import AnimalsAskPage
from utils import utils


class flightsPage(QtWidgets.QMainWindow):
    def __init__(self, previous_window, user, server):
        super(flightsPage, self).__init__()
        self.ui = flightsPageMain()
        self.ui.setupUi(self)
        self.user = user
        self.server = server
        self.__previous_window = previous_window
        self.ui.departureCb.addItems(self.get_cities_list())
        self.ui.arrivalCb.addItems(self.get_cities_list())
        self.ui.showFlightsBt.clicked.connect(self.show_flights)
        self.ui.nextBt.clicked.connect(self.go_next)
        self.ui.backBt.clicked.connect(self.back)
        self.scrollLayout = QGridLayout()
        self.flight_id_and_btn = {}
        self.__flight_id = -1

    @property
    def previous_window(self):
        return self.__previous_window

    @property
    def flight_id(self):
        return self.__flight_id

    def is_already_bought(self):
        sql = f"SELECT id_ticket from Tickets WHERE id_passenger='{self.user[0]}' AND id_flight = '{self.__flight_id}';"
        if not self.server.execute_sql_one(sql):
            return False
        else:
            return True

    def get_cities_list(self):
        sql_cities = "SELECT name FROM Cities"
        cities = self.server.execute_sql_full((sql_cities))
        result = []
        for i in range(len(cities)):
            result.append(cities[i][0])
        return result

    def back(self):
        self.__previous_window.show()
        self.hide()

    def go_next(self):
        if self.__flight_id != -1:
            if not self.is_already_bought():
                self.animalAsk = AnimalsAskPage(self, self.user, self.server)
                self.animalAsk.show()
                self.hide()
            else:
                utils.show_message("Wow!", "It's seems what you already have bought a ticket on this flight!", "Message")
        else:
            utils.show_message("Wow!", "Please choose a flight before you go next!", "Message")

    def get_name_of_airport_by_id(self, id):
        return self.server.execute_with_id("""SELECT name FROM Airports WHERE id_airport = ?""", id)

    def get_code_plane(self, id):
        return self.server.execute_with_id("""SELECT individual_code FROM Planes WHERE id_plane= ?""", id)

    def choose_button(self, id_btn):
        if self.__flight_id != -1:
            prev = self.flight_id
            for i in self.flight_id_and_btn.keys():
                if self.flight_id_and_btn[i] == prev:
                    self.scrollLayout.itemAtPosition(i, 6).widget().setStyleSheet("background-color : light gray")

        self.__flight_id = self.flight_id_and_btn[id_btn]
        self.scrollLayout.itemAtPosition(id_btn, 6).widget().setStyleSheet("background-color : cyan")

    def compare_dates(self, chosen_date):
        now = datetime.now().strftime("%Y-%d-%m")
        if int(now[0:4]) < int(chosen_date[0:4]):
            return True
        elif int(now[0:4]) == int(chosen_date[0:4]):
            if int(now[8:10]) < int(chosen_date[8:10]):
                return True
            elif int(now[8:10]) == int(chosen_date[8:10]):
                if int(now[5:7]) < int(chosen_date[5:7]):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def compare_date_time(self, chosen_date):
        now = datetime.now().strftime("%Y-%d-%m %H:%M:%S")

        if int(now[8:10]) == int(chosen_date[8:10]) and (int(chosen_date[11:13]) - int(now[11:13]) <= 1):
            return False
        else:
            return True

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
    def show_flights(self):
        depart = self.ui.departureCb.currentText().strip()
        arrival = self.ui.arrivalCb.currentText().strip()
        date = self.ui.calendarWidget.selectedDate().toString("yyyy-dd-MM")
        if self.compare_dates(date):
            exec_directions = "exec flightsByDate '" + depart + "', '" + arrival + "', '" + date + "'"
            flights = self.server.execute_sql_full(exec_directions)
            self.clear_layout(self.scrollLayout)
            self.__flight_id = -1
            if flights:
                for i in range(len(flights)):
                    if self.compare_date_time(flights[i][0].strftime("%Y-%d-%m %H:%M")):
                        for j in range(7):
                            # ToDo clean names of airports
                            if j == 0:
                                temp = QtWidgets.QLabel("Department time:" + '\n' + flights[i][j].strftime("%Y-%d-%m %H:%M"))
                            elif j == 1:
                                temp = QtWidgets.QLabel("Arrival time:" + '\n' + flights[i][j].strftime("%Y-%d-%m %H:%M"))
                            elif j == 2:
                                temp = QtWidgets.QLabel(
                                    "Department airport:" + '\n' + self.get_name_of_airport_by_id((int(flights[i][j]))))
                            elif j == 3:
                                temp = QtWidgets.QLabel(
                                    "Arrival airport:" + '\n' + self.get_name_of_airport_by_id((int(flights[i][j]))))
                            elif j == 4:
                                temp = QtWidgets.QLabel("Code of plane:" + '\n' + self.get_code_plane((int(flights[i][j]))))
                            elif j == 5:
                                free_seats = utils.free_seats(self.server, flights[i][j])
                                temp = QtWidgets.QLabel("Free seats:" + '\n' + str(free_seats))
                                if free_seats == 0:
                                    self.scrollLayout.addWidget(temp, i, j)
                                    break
                            else:
                                temp = QPushButton("Choose")
                                self.flight_id_and_btn[i] = int(flights[i][j - 1])
                                temp.clicked.connect(lambda ch, id_btn=i: self.choose_button(id_btn))

                            self.scrollLayout.addWidget(temp, i, j)

                w = QWidget()
                w.setLayout(self.scrollLayout)

                scroll = self.ui.flightsScroll
                scroll.setWidget(w)
                scroll.show()
            else:
                utils.show_message("Oops!", "Not any available flights on this date!", "Message")

        else:
            utils.show_message("Wow!", "Please choose date since today!", "Message")
