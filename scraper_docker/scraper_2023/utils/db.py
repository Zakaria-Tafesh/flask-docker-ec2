import os
import sqlite3


basedir = os.path.abspath(os.path.dirname(__file__))
shared_docker = os.path.join('/', 'opt', 'shared_docker')
DB_NAME = 'database.db'
DB_PATH = os.path.join(shared_docker, DB_NAME)


class MySQLite:
    def __init__(self):
        self.db_path = DB_PATH
        self.con = None
        self.cur = None
        self.table = None

    def get_zones(self):
        self.open_con()

        self.table = 'zone'
        query = f"SELECT client_name, payload FROM {self.table}"
        res = self.cur.execute(query)
        clients_list = []
        for c_name, payload in res.fetchall():
            print(c_name, payload)
            clients_list.append({'client_name': c_name,
                                 'payload_fresh_map': payload})

        self.close_con()
        return clients_list

    def close_con(self):
        if self.con:
            self.cur.close()
            self.con.close()
            print("sqlite connection is closed")

    def open_con(self):
        try:
            self.con = sqlite3.connect(DB_PATH)
            self.cur = self.con.cursor()
            print("Successfully Connected to SQLite")
            return self.con, self.cur
        except sqlite3.Error as error:
            print("Error while Opening sqlite connection", error)

    def add_column(self, table_name, column_name, data_type):
        self.open_con()

        base_command = ("ALTER TABLE '{table_name}' ADD column '{column_name}' '{data_type}'")
        sql_command = base_command.format(table_name=table_name, column_name=column_name,
                                          data_type=data_type)

        self.cur.execute(sql_command)
        self.con.commit()

        self.close_con()
        print('column add_column successfully')

    def rename_column(self, table_name, column_name, new_column_name):
        self.open_con()

        base_command = f"ALTER TABLE {table_name} RENAME COLUMN {column_name} TO {new_column_name}"
        # sql_command = base_command.format(table_name=table_name, column_name=column_name,
        #                                   new_column_name=new_column_name)
        print(base_command)
        self.cur.execute(base_command)
        self.con.commit()

        self.close_con()
        print('column rename_column successfully')

    def get_columns_types(self):
        self.open_con()

        base_command = "SELECT name, type FROM pragma_table_info('zone')"
        # sql_command = base_command.format(table_name=table_name, column_name=column_name,
        #                                   new_column_name=new_column_name)
        res = self.cur.execute(base_command)
        for row in res.fetchall():
            print(row)

        self.close_con()


if __name__ == "__main__":
    my_sql = MySQLite()
    # my_sql.get_zones()
    my_sql.get_columns_types()

    my_sql.add_column(table_name='zone', column_name='last_run_at', data_type='DATETIME')
    # my_sql.rename_column(table_name='zone', column_name='date', new_column_name='created_at')
    my_sql.get_columns_types()
