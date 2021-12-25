import inspect


import PyQt5
from datetime import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QScrollArea, QButtonGroup, \
    QVBoxLayout
import sys
# ui
# app = QtWidgets.QApplication([])
# win = uic.loadUi("test.ui")  # расположение вашего файла .ui
#
# win.show()
# sys.exit(app.exec())
from Server import Server
from airlines import Ui_MainWindow as airlinesMain
from flightsUPage import flightsPage
from initialPage import Initial_window

from loginUser import Ui_Form as loginUserForm  # импорт нашего сгенерированного файла
import sys

class Utils:
    def __init__(self):
        pass


def application(server):
    app = QtWidgets.QApplication(sys.argv)
    window = Initial_window(server)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
   # server = 'DESKTOP-VRPPT8H\\SQLEXPRESS'
   #  database = 'Airport'
   #  username = 'DESKTOP-VRPPT8H\\meshc'
   #  password = ''
   #  # +';UID='+username+';PWD='+ password
   #  cnxn = pyodbc.connect(
   #      'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
   #  cursor = cnxn.cursor()
   # now = datetime.now()
   # print(now.strftime("%Y-%d-%m %H:%M:%S"))
   server = Server()
   #print()
   application(server)


   # cursor = server.cursor
   # sql_cities = "SELECT name FROM Cities"
   # cursor.execute(sql_cities)
   # temp = cursor.fetchall()
   # for i in range(len(temp)):
   #     print(temp[i][0])
   # print(temp)




# #ToDo add check for id
# sql_insert_flight = ("INSERT INTO Flights (id_plane,id_pilot, id_departure, id_arrival, time_departure, time_arrival) "
#                     "VALUES (?,?,?,?,?,?);")
# values = ['1', '2', '1', '4', '2021-12-11 00:00:00.000', '2021-12-11 10:00:00.000']
# exec_tickets = 'exec TicketsByPassenger 1'
# exec_directions = "exec FlightsByDirection 'KALININGRAD', 'MOSCOW', '2021-12-04 00:00:00.000'"
# exec_animals = "exec AnimalsByPassenger "+str(user[0])
# try:
#     cursor.execute(sql_insert_flight, values)
#     cnxn.commit()
# except pyodbc.Error as error:
#     print("some error while unput ", error)
# #results = cursor.fetchone()
# results = cursor.fetchall()
# for i in results:
#      print(i)
# print(results)
# rest_of_rows = cursor.fetchall()
