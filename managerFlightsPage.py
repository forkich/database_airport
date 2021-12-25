from datetime import datetime, timedelta

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout

from utils import utils
from managerFlights import Ui_MainWindow

class managerFlightsPage(QtWidgets.QMainWindow):
    def __init__(self, previous_window, server):
        super(managerFlightsPage, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.server = server
        self.__previous_window = previous_window
        self.ui.planeCb.addItems(self.get_planes())
        self.ui.departureCb.addItems(self.get_airports())
        self.ui.arrivalCb.addItems(self.get_airports())
        self.ui.addBtn.clicked.connect(self.add_flight)
        self.ui.backBtn.clicked.connect(self.back)
        self.ui.showBtn.clicked.connect(self.show_flights)
        self.w = QWidget()
        self.set_time()

    def get_planes(self):
        sql = "exec getPlaneInfo"
        items = self.server.execute_sql_full((sql))
        result = []
        for i in range(len(items)):
            result.append("ID: " + str(items[i][0]) + " Company: " + items[i][1] + " Code: " + items[i][2])
        return result

    def get_airports(self):
        sql = "exec getAirportInfo"
        items = self.server.execute_sql_full((sql))
        result = []
        for i in range(len(items)):
            result.append("ID: " + str(items[i][0]) + " City: " + items[i][1] + " Name: " + str(items[i][2]))
        return result

    def back(self):
        self.__previous_window.show()
        self.w.close()
        self.hide()

    def show_flights(self):
        sql = "exec flightsListInPeriod '" + self.ui.fromTime.dateTime().toString("yyyy-dd-MM hh:mm") + "', '" + self.ui.toTime.dateTime().toString("yyyy-dd-MM hh:mm") + "'"
        flights = self.server.execute_sql_full(sql)

        self.scroll = QGridLayout()
        self.scroll.setSpacing(20)
        names = []
        names.append(QtWidgets.QLabel("Department time: "))
        names.append(QtWidgets.QLabel("Arrival time: "))
        names.append(QtWidgets.QLabel("Department airport: "))
        names.append(QtWidgets.QLabel("Arrival airport: "))
        names.append(QtWidgets.QLabel("Code of plane: "))
        names.append(QtWidgets.QLabel("ID:"))
        for i in range(len(names)):
            self.scroll.addWidget(names[i], 0, i)

        for i in range(len(flights)):
            for j in range(len(names)):
                if j == 0 or j == 1:
                    temp = QtWidgets.QLabel(flights[i][j].strftime("%Y-%d-%m %H:%M"))
                elif j == 2 or j == 3:
                    temp = QtWidgets.QLabel(utils.get_city_by_airport(self.server, str(flights[i][j])))
                else:
                    temp = QtWidgets.QLabel(str(flights[i][j]))
                self.scroll.addWidget(temp, i + 1, j)
        self.w.setWindowTitle("Timetable")
        self.w.setLayout(self.scroll)
        self.w.show()

    def set_time(self):
        min_date_departure = datetime.now() + timedelta(days=7)
        min_date_arrival = QDateTime(min_date_departure + timedelta(hours=1, minutes=30))
        min_date_departure = QDateTime(min_date_departure)
        self.ui.departureTime.setMinimumDateTime(min_date_departure)
        self.ui.arrivalTime.setMinimumDateTime(min_date_arrival)

        date_from = datetime.now()
        date_to = QDateTime(date_from + timedelta(days=30))
        date_from = QDateTime(date_from)
        self.ui.fromTime.setDateTime(date_from)
        self.ui.toTime.setDateTime(date_to)

    def add_flight(self):
        plane = self.ui.planeCb.currentText().strip()
        id_plane = int(plane[plane.find("ID: ") + len("ID: "): plane.find(" Company: ")])
        d_time = self.ui.departureTime.dateTime()
        a_time = self.ui.arrivalTime.dateTime()
        departure = self.ui.departureCb.currentText().strip()
        id_departure = int(departure[departure.find("ID: ") + len("ID: "): departure.find(" City: ")])
        arrival = self.ui.arrivalCb.currentText().strip()
        id_arrival = int(arrival[arrival.find("ID: ") + len("ID: "): arrival.find(" City: ")])
        if not self.server.execute_sql_one("exec sameCity " + str(id_departure) + ", " + str(id_arrival)):
            if d_time.addSecs(5400) < a_time:
                sql_insert_flight = ("INSERT INTO Flights (id_plane, id_departure, id_arrival, time_departure, time_arrival) "
                                    "VALUES (?,?,?,?,?);")
                values = [id_plane, id_departure, id_arrival, d_time.toString("yyyy-dd-MM hh:mm"), a_time.toString("yyyy-dd-MM hh:mm")]
                self.server.execute_insert(sql_insert_flight, values)
                utils.show_message("Successfully!", "You added new flight!", "Message")
            else:
                utils.show_message("Wow!", "Arrival datetime should be more than departure time on 1 hour and 30 min!", "Error")
        else:
            utils.show_message("Wow!", "Please choose airports from different cities!", "Error")
