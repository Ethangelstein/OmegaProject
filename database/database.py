import mysql.connector


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            database = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )

            return database
        except BaseException as error:
            print("Couldn't connect to MySQL DB")
            exit(1)


database = Database("localhost", "root", "mysql", "omega")
