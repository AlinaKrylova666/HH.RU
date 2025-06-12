


class DBManage:
    def __init__(self, user, password, database, host, port = 5432):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database