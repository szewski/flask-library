import sqlite3


class SQLiteDb:
    def get_books(self, cursor, one=False):
        pass

    # def get_data(self, query, params=(), one=False):
    #     """
    #     :param query: SQLite query
    #     :param params: key word argument
    #     :return: cursor
    #     """
    #     conn = sqlite3.connect(self.path)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #
    #     c.execute(query, params)
    #     data = c.fetchall()
    #
    #     conn.close()
    #     return (data[0] if data else None) if one else data
    #
    # def write_data(self, query, params=()):
    #     """
    #     :param query: SQL query
    #     :param params: key word argument
    #     """
    #     conn = sqlite3.connect(self.path)
    #     c = conn.cursor()
    #
    #     c.execute(query, params)
    #
    #     conn.commit()
    #     conn.close()
