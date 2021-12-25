from PyQt5.QtWidgets import QMessageBox


class utils:

    @staticmethod
    def show_message(text, informative_text, title):
        msg = QMessageBox()
        msg.setText(text)
        msg.setInformativeText(informative_text)
        msg.setWindowTitle(title)
        msg.exec_()

    @staticmethod
    def get_city_by_airport(server, name):
        sql = "exec getCityByAirportName " + name
        return name + " (" + str(server.execute_sql_one(sql)[0]).strip() + ")"

    @staticmethod
    def free_seats(server, id):
        sql = "exec countOfFreeSeatsByFlight " + str(id)
        return server.execute_sql_one(sql)[0]

    @staticmethod
    def get_list_items_id_name(server, table):
        sql = "SELECT * FROM " + table
        items = server.execute_sql_full((sql))
        result = []
        for i in range(len(items)):
            result.append("ID: " + str(items[i][0]) + " Name: " + items[i][1])
        return result
