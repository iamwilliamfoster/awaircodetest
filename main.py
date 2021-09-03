import sqlite3
from sqlite3 import Error
from flask import Flask


class AppHandler:
    def __init__(self):
        self.conn = None
        self.cur = None

    def db_init(self, db_loc=":memory:"):
        try:
            conn = sqlite3.connect(db_loc)
            self.conn = conn
            self.cur = conn.cursor()
        except Error as e:
            print(e)

    #Function for running SQL queries
    def sql_query(self, sql_str):
        result = 0
        try:
            self.cur.execute(sql_str)
            result = self.cur.fetchall()
        except Error as e:
            print(e)
        return result

    #Function for executing SQL commands
    def sql_cmd(self, sql_str):
        try:
            self.cur.execute(sql_str)
        except Error as e:
            print(e)


if __name__ == '__main__':
    handler = AppHandler()
    handler.db_init()
    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            email text NOT NULL UNIQUE,
                                            password NOT NULL
                                        ); """
    handler.sql_cmd(sql_create_user_table)
    handler.sql_cmd("""insert into user values (1234,"joe", "me@test.com", "cats");""")
    print(handler.sql_query("select * from user;"))