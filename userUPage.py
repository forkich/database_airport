from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton

from animalAddPage import animalAddPage
from animalDeletePage import animalDeletePage
from flightsUPage import flightsPage
from userPage import Ui_MainWindow
from utils import utils



class userPage(QtWidgets.QMainWindow):
    def __init__(self, previous_window, user, server):
        super(userPage, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user = user
        self.server = server
        self.__previous_window = previous_window
        self.animal_id = -1
        self.animal_id_and_btn = {}
        self.ui.firstname.setText(user[1])
        self.ui.surname.setText(user[2])
        self.ui.patronymic.setText(user[3])
        self.ui.passportCode.setText(user[4])
        self.grid_animals = QGridLayout()
        self.set_animal_scroll()
        self.set_scroll_tickets_names()
        self.update_layout()
        self.scroll_tikcet_u.hide()
        self.ui.buyTicketBt.clicked.connect(self.go_to_flights_page)
        self.ui.logOutBt.clicked.connect(self.log_out)
        self.ui.showTicketsBt.clicked.connect(self.show_tickets)
        self.ui.addAnimalsBt.clicked.connect(self.add_animal)
        #self.ui.deleteAnimalsBt.clicked.connect(self.confirm_animal)


    @property
    def previous_window(self):
        return self.__previous_window

    def add_animal(self):
        self.add_animal_page = animalAddPage(self,self.user, self.server)
        self.add_animal_page.show()

    # def delete_animal(self):
    #     sql = f"DELETE FROM Animals WHERE id_animal='{self.animal_id}'"
    #     self.server.execute_sql_one(sql)
    #
    # def confirm_animal(self):
    #     self.delete_animal_page = animalDeletePage(self, self.user, self.server)
    #     self.delete_animal_page.show()

    def log_out(self):
        self.__previous_window.show()
        self.hide()

    def go_to_flights_page(self):
        self.flights_page = flightsPage(self, self.user, self.server)
        self.flights_page.show()
        if self.scroll_tikcet_u.isVisible():
            self.show_tickets()
        self.hide()

    def choose_button(self, id_btn):
        if self.animal_id != -1:
            prev = self.animal_id
            for i in self.animal_id_and_btn.keys():
                if self.animal_id_and_btn[i] == prev:
                    self.grid_animals.itemAtPosition(i, 0).widget().setStyleSheet("background-color : light gray")

        self.animal_id = self.animal_id_and_btn[id_btn]
        self.grid_animals.itemAtPosition(id_btn, 0).widget().setStyleSheet("background-color : cyan")

    def set_animal_scroll(self):
        exec_animals = "exec AnimalsByPassengerFull " + str(self.user[0])
        animals = self.server.execute_sql_full(exec_animals)
        if animals:
            for i in range(len(animals)):
                for j in range(3):
                    if j == 0:
                        temp = QPushButton("Choose")
                        self.animal_id_and_btn[i] = int(animals[i][j])
                        temp.clicked.connect(lambda ch, id_btn=i: self.choose_button(id_btn))
                    elif j == 1:
                        temp = QtWidgets.QLabel(" Name: \n" + animals[i][j])
                    else:
                        temp = QtWidgets.QLabel(" Type: \n" + animals[i][j])
                    self.grid_animals.addWidget(temp, i, j)

            w = QWidget()
            w.setLayout(self.grid_animals)
            scroll = self.ui.scrollAnimals
            scroll.setWidget(w)
            scroll.show()

    def show_tickets(self):
        if self.scroll_tikcet_u.isVisible():
            self.scroll_tikcet_u.hide()
            self.ui.showTicketsBt.setText("Show bought tickets")
        else:
            self.update_tickets_scroll()
            self.scroll_tikcet_u.show()
            self.ui.showTicketsBt.setText("Hide tickets")

    def set_scroll_tickets_names(self):
        self.scroll_grid = QGridLayout()

        self.names = []
        self.names.append(QtWidgets.QLabel("Department time: "))
        self.names.append(QtWidgets.QLabel("Arrival time: "))
        self.names.append(QtWidgets.QLabel("Price: "))
        self.names.append(QtWidgets.QLabel("Tariff: "))
        self.names.append(QtWidgets.QLabel("Department airport: "))
        self.names.append(QtWidgets.QLabel("Arrival airport: "))
        self.names.append(QtWidgets.QLabel("ID:"))
        for i in range(len(self.names)):
            self.scroll_grid.addWidget(self.names[i], 0, i)

    def update_layout(self):
        w = QWidget()
        w.setLayout(self.scroll_grid)
        self.scroll_tikcet_u = self.ui.scrollTickets
        self.scroll_tikcet_u.setWidget(w)


    def update_tickets_scroll(self):
        exec_tickets = "exec TicketsByPassenger " + str(self.user[0])
        tickets = self.server.execute_sql_full(exec_tickets)
        if tickets:
            if self.scroll_grid.rowCount() == 1:
                i = 0
            elif self.scroll_grid.rowCount() - 1 < len(tickets):
                i = self.scroll_grid.rowCount() - 1
            else:
                i = len(tickets)
            while i < len(tickets):
                for j in range(len(self.names)):
                    if j == 0 or j == 1:
                        temp = QtWidgets.QLabel(tickets[i][j].strftime("%Y-%d-%m %H:%M"))
                    elif j == 4 or j == 5:
                        temp = QtWidgets.QLabel(utils.get_city_by_airport(self.server, str(tickets[i][j])))
                    else:
                        temp = QtWidgets.QLabel(str(tickets[i][j]))
                    self.scroll_grid.addWidget(temp, i + 1, j)
                i += 1
            self.update_layout()


    def set_animals_scroll(self):
        w = QWidget()
        w.setLayout(self.scrollLayout)
        scroll = self.ui.scrollAnimals
        scroll.setWidget(w)
        scroll.show()
