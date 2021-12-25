import pyodbc

class Server:
    SERVER = 'DESKTOP-VRPPT8H\\SQLEXPRESS'
    DATABASE = 'Airport'
    USERNAME = 'DESKTOP-VRPPT8H\\meshc'
    PASSWORD = ''

    def __init__(self):
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.SERVER + ';DATABASE=' + self.DATABASE + ';Trusted_Connection=yes;')
        self.cursor = self.cnxn.cursor()

    def execute_insert(self, sql, values):
        try:
            self.cursor.execute(sql, values)
            self.cnxn.commit()
        except pyodbc.Error as error:
            print("Error while input into database: ", error)

    def execute_is_exist(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if not result:
            return False
        else:
            return True

    def execute_sql_full(self, sql):
        self.cursor.execute(sql)
        items = self.cursor.fetchall()
        result = []
        for i in range(len(items)):
            result.append(items[i])
        return result

    def execute_sql_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def execute_with_id(self, sql, id):
        self.cursor.execute(sql, id)
        return str(self.cursor.fetchone()[0])

