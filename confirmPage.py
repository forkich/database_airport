from PyQt5 import QtWidgets, QtCore

from confirmTicket import Ui_Dialog
from utils import utils


class confirmPage(QtWidgets.QDialog):
    def __init__(self, previous_window, ticket, server, user):
        super(confirmPage, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.__previous_window = previous_window
        self.user = user
        self.ticket = ticket
        self.server = server
        self.ui.back.clicked.connect(self.back)
        self.ui.confirm.clicked.connect(self.confirm)
        self.set_ticket()


    def set_ticket(self):
        for i in range(len(self.ticket)):
            self.ui.listWidget.addItem(self.ticket[i])

    def confirm(self):
        self.add_ticket()

    def add_ticket(self):
        prev_window = self.__previous_window
        price = prev_window.price_without_baggage
        baggage_list = prev_window.list_of_baggage_types
        prev_window = prev_window.previous_window
        animals = []
        if prev_window.windowTitle() == 'animalsYes':
            animals = prev_window.animals_ids

        while prev_window.windowTitle() != 'flightsPage':
            prev_window = prev_window.previous_window
        id_passenger = self.user[0]
        id_flight = prev_window.flight_id
        id_tariff = -1
        for i in range(len(self.ticket)):
            if self.ticket[i].startswith('Tariff'):
                id_tariff = int(self.ticket[i][self.ticket[i].find("Tariff: ") + len("Tariff: ")])
                break
        values = [id_passenger, id_flight, id_tariff, price]
        sql_insert_ticket = ("INSERT INTO Tickets (id_passenger, id_flight, id_tariff, total_price) "
                            "VALUES (?,?,?,?);")
        self.server.execute_insert(sql_insert_ticket, values)
        sql_id_ticket = ("SELECT TOP 1 id_ticket FROM Tickets ORDER BY id_ticket DESC ")
        id_ticket = self.server.execute_sql_one(sql_id_ticket)
        self.add_baggage(baggage_list, id_ticket[0])
        if animals:
            self.add_animal_ticket(animals, id_ticket[0])
        self.cancel_buy(prev_window)


    def add_animal_ticket(self, animals, id_ticket):
        sql_insert_animals = ("INSERT INTO TicketAndAnimal (id_ticket, id_animal) "
                              "VALUES (?,?);")
        for i in range(len(animals)):
            values = [id_ticket, animals[i]]
            self.server.execute_insert(sql_insert_animals, values)

    def add_baggage(self, baggage_list, id_ticket):
        sql_insert_baggage = ("INSERT INTO Baggage (id_baggage_type, id_ticket) "
                             "VALUES (?,?);")
        for i in range(len(baggage_list)):
            values = [baggage_list[i], id_ticket]
            self.server.execute_insert(sql_insert_baggage, values)

    def cancel_buy(self, prev_window):
        utils.show_message("Congratulations!", "You bought a ticket!", "Message")
        while prev_window.windowTitle() != 'userPage':
            prev_window = prev_window.previous_window
        prev_window.show()
        self.hide()

    def back(self):
        self.__previous_window.show()
        self.hide()
