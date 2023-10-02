import os
import sqlite3
import traceback

from input.config import PATH_SHARED_DOCKER
import mysql.connector
from .logger import logger


basedir = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'database.db'
DB_PATH = os.path.join(PATH_SHARED_DOCKER, DB_NAME)

MYSQL_USER = os.getenv('MYSQL_USER')
# DB_USER = 'zak'
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
DB_HOST = '127.0.0.1'


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
            logger.info(c_name, payload)
            clients_list.append({'client_name': c_name,
                                 'payload_fresh_map': payload})

        self.close_con()
        return clients_list

    def close_con(self):
        if self.con:
            self.cur.close()
            self.con.close()
            logger.info("sqlite connection is closed")

    def open_con(self):
        try:
            self.con = sqlite3.connect(DB_PATH)
            self.cur = self.con.cursor()
            logger.info("Successfully Connected to SQLite")
            return self.con, self.cur
        except sqlite3.Error as error:
            logger.info("Error while Opening sqlite connection", error)

    def add_column(self, table_name, column_name, data_type):
        self.open_con()

        base_command = ("ALTER TABLE '{table_name}' ADD column '{column_name}' '{data_type}'")
        sql_command = base_command.format(table_name=table_name, column_name=column_name,
                                          data_type=data_type)

        self.cur.execute(sql_command)
        self.con.commit()

        self.close_con()
        logger.info('column add_column successfully')

    def rename_column(self, table_name, column_name, new_column_name):
        self.open_con()

        base_command = f"ALTER TABLE {table_name} RENAME COLUMN {column_name} TO {new_column_name}"
        # sql_command = base_command.format(table_name=table_name, column_name=column_name,
        #                                   new_column_name=new_column_name)
        logger.info(base_command)
        self.cur.execute(base_command)
        self.con.commit()

        self.close_con()
        logger.info('column rename_column successfully')

    def get_columns_types(self):
        self.open_con()

        base_command = "SELECT name, type FROM pragma_table_info('zone')"
        # sql_command = base_command.format(table_name=table_name, column_name=column_name,
        #                                   new_column_name=new_column_name)
        res = self.cur.execute(base_command)
        for row in res.fetchall():
            print(row)

        self.close_con()


class MySQLDB:

    def __init__(self):
        self.cur = None
        self.con = None
        self.db_config = {
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'host': DB_HOST,  # Use the service name 'mysql'
            'database': MYSQL_DATABASE,
        }

    def get_zones(self):
        self.open_con()

        self.table = 'zone'
        query = f"SELECT client_name, payload FROM {self.table}"
        # query = "SELECT * FROM zone"
        # query = "show tables"
        logger.info(query)

        self.cur.execute(query)

        clients_list = []
        records = self.cur.fetchall()

        # Print the fetched data
        for c_name, payload in records:
            logger.info(c_name, payload)
            clients_list.append({'client_name': c_name,
                                 'payload_fresh_map': payload})

        # for c_name, payload in self.cur.fetchall():
        #     print(c_name, payload)
        #     clients_list.append({'client_name': c_name,
        #                          'payload_fresh_map': payload})

        self.close_con()
        return clients_list

    def open_con(self):
        try:
            # Connect to the MySQL server
            self.con = mysql.connector.connect(**self.db_config)
            # Create a cursor
            self.cur = self.con.cursor()
            logger.info("Successfully Connected to MySQLDB")
            logger.info(str(self.db_config))
        except:
            logger.info("Error while Opening MySQLDB connection")
            traceback.print_exc()

    def close_con(self):
        if self.con:
            # Close the cursor and the connection when done
            self.con.close()
            self.cur.close()
            logger.info("MySQLDB connection closed")
        else:
            logger.info("No MySQLDB connection to Close")


# if __name__ == "__main__":
#     my_sql = MySQLite()
#     # my_sql.get_zones()
#     my_sql.get_columns_types()
#
#     my_sql.add_column(table_name='zone', column_name='last_run_at', data_type='DATETIME')
#     # my_sql.rename_column(table_name='zone', column_name='date', new_column_name='created_at')
#     my_sql.get_columns_types()
