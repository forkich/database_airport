from PyQt5 import QtWidgets

from confirmPage import confirmPage
from ticketsPage import Ui_MainWindow


class ticketsPage(QtWidgets.QMainWindow):
    def __init__(self, previous_window, user, server):
        super(ticketsPage, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user = user
        self.server = server
        self.__previous_window = previous_window
        self.__price_without_baggage = 0
        self.__list_of_baggage_types = []
        self.ui.addBgBt.clicked.connect(self.addBaggage)
        self.ui.lanchLb.hide()
        self.ui.yesCb.hide()
        self.ui.noCb.hide()
        self.ui.tariffLb.hide()
        self.ui.tariffTypeCb.hide()
        self.ui.totalPrice.hide()
        self.ui.price.hide()
        self.ui.buyBt.hide()
        self.lunchFlag = bool
        self.ui.buyBt.clicked.connect(self.buy)
        self.ui.backBt.clicked.connect(self.back)
        self.ui.withNoBagBt.clicked.connect(self.without)
        self.ui.tariffTypeCb.activated.connect(self.lunch_recount)
        self.ui.yesCb.clicked.connect(lambda ch, flag=True: self.lunch(flag))
        self.ui.noCb.clicked.connect(lambda ch, flag=False: self.lunch(flag))
        self.collectTariff()
        self.set_cb()

    #ToDo:WTF?????
    @property
    def previous_window(self):
        try:
            return self.__previous_window
        except:
            pass

    @property
    def price_without_baggage(self):
        return self.__price_without_baggage

    @property
    def list_of_baggage_types(self):
        return self.__list_of_baggage_types

    def set_cb(self):
        types = self.server.execute_sql_full("SELECT id_baggage_type, volume, price FROM BaggageType")
        for i in range(len(types)):
            self.ui.bagTypeCb.addItem("Type: " + str(types[i][0]) + " Volume KG: " + types[i][1] + " price: " + str(types[i][2]))

    def back(self):
        self.__previous_window.show()
        self.hide()

    def buy(self):
        ticket = []
        animals_price = 0
        if self.__previous_window.windowTitle() == 'animalsYes':
            animals = self.__previous_window.get_added_animals()
            if len(animals) > 0:
                ticket.append("Animals:")
                for i in range(len(animals)):
                    ticket.append(animals[i])
                    animals_price += int(animals[i][animals[i].find("price: ") + len("price: "):])

        if self.ui.listWidget.count() != 0:
            ticket.append("Baggage:")
            for i in range(self.ui.listWidget.count()):
                temp_text = self.ui.listWidget.item(i).text()
                ticket.append(temp_text)
                self.__list_of_baggage_types.append(int(temp_text[temp_text.find("Type: ") + len("Type: ")]))
        ticket.append(self.ui.tariffTypeCb.currentText().strip())
        ticket.append("Total price:")
        ticket.append(str(int(self.ui.price.text()) + animals_price))
        self.__price_without_baggage = int(self.price_tariff) + animals_price

        self.confirmPage = confirmPage(self, ticket, self.server, self.user)
        self.confirmPage.show()
        self.hide()

    def lunch(self, flag):
        self.lunchFlag = flag
        if flag:
            self.ui.noCb.setChecked(False)
        else:
            self.ui.yesCb.setChecked(False)
        self.ui.tariffLb.show()
        self.change_visible_tariffs()
        self.ui.tariffTypeCb.show()
        self.recount_baggage_price()
        self.recount_tariff_price()
        self.set_total_price()
        self.ui.buyBt.show()

    def recount_baggage_price(self):
        baggage = []
        for i in range(self.ui.listWidget.count()):
            baggage.append(self.ui.listWidget.item(i).text())
        self.price_baggage = 0
        for i in range(len(baggage)):
            self.price_baggage += int(baggage[i][baggage[i].find('price: ') + len('price: '):])

    def recount_tariff_price(self):
        tariff_str = self.ui.tariffTypeCb.currentText().strip()
        if self.lunchFlag:
            self.price_tariff = int(tariff_str[tariff_str.find("Price: ") + len("Price: "):tariff_str.find(" Food:")])
        else:
            self.price_tariff = int(tariff_str[tariff_str.find("Price: ") + len("Price: "):tariff_str.find(" Insurance:")])

    def lunch_recount(self):
        self.recount_tariff_price()
        self.set_total_price()

    def set_total_price(self):
        self.ui.totalPrice.show()
        self.ui.price.setText(str(self.price_tariff + self.price_baggage))
        self.ui.price.show()

    def collectTariff(self):
        exec_tariff = "tarifs"
        self.list_tariffs = self.server.execute_sql_full(exec_tariff)

    def change_visible_tariffs(self):
        self.ui.tariffTypeCb.clear()
        for i in range(len(self.list_tariffs)):
            if self.lunchFlag and self.list_tariffs[i][2] != 'NONE':
                self.ui.tariffTypeCb.addItem(
                    "Tariff: " + str(self.list_tariffs[i][0]) + " Price: " + str(self.list_tariffs[i][1]) + " Food: " +
                    self.list_tariffs[i][2] + " Insurance: " + self.list_tariffs[i][3])
            elif not self.lunchFlag and self.list_tariffs[i][2] == 'NONE':
                self.ui.tariffTypeCb.addItem(
                    "Tariff: " + str(self.list_tariffs[i][0]) + " Price: " + str(self.list_tariffs[i][1]) +
                    " Insurance: " + self.list_tariffs[i][3])

    def addBaggage(self):
        self.ui.listWidget.addItem(self.ui.bagTypeCb.currentText().strip())
        self.show_combobox()
        self.recount_baggage_price()
        if self.ui.tariffTypeCb.isVisible():
            self.set_total_price()

    def without(self):
        self.ui.listWidget.clear()
        self.show_combobox()
        self.price_baggage = 0
        if self.ui.tariffTypeCb.isVisible():
            self.set_total_price()

    def show_combobox(self):
        self.ui.lanchLb.show()
        self.ui.yesCb.show()
        self.ui.noCb.show()
