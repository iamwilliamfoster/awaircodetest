# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request

app = Flask(__name__)

HANDLER = None


class AppHandler:
    def __init__(self, db_loc=":memory:"):
        self.db_loc = db_loc

    def db_init(self):
        try:
            conn = sqlite3.connect(self.db_loc)
        except Error as e:
            print(e)

    #Function for running SQL queries
    def sql_query(self, sql_str):
        result = 0
        try:
            with sqlite3.connect(self.db_loc) as con:
                cur = con.cursor()
                cur.execute(sql_str)
                result = cur.fetchall()
        except Error as e:
            print(e)
        return result

    #Function for executing SQL commands
    def sql_cmd(self, sql_str):
        try:
            with sqlite3.connect(self.db_loc) as con:
                cur = con.cursor()
                cur.execute(sql_str)
                con.commit
        except Error as e:
            print(e)

    def sql_user_exists(self, in_str):
        result = self.sql_query("select count(*) from users where user_name ='{}';".format(in_str))
        if result[0][0]:
            return True
        return False

@app.route('/')
def main(inp = "Welcome!"):
    print(HANDLER.sql_query("select * from user;"))
    return render_template('main.html', x = inp)


@app.route('/print_user')
def print_user():
    result = HANDLER.sql_query("select * from user;")
    return render_template('print.html', users = result)


if __name__ == '__main__':
    HANDLER = AppHandler("C:/!Coding/sqltest.db")
    HANDLER.db_init()
    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            email text NOT NULL UNIQUE,
                                            password NOT NULL
                                        ); """
    HANDLER.sql_cmd(sql_create_user_table)
    HANDLER.sql_cmd("""insert into user values ("1234","joe", "me@test.com", "cats");""")
    HANDLER.sql_cmd("""insert into user values ("4321","bob", "you@test.com", "dogs");""")
    print(HANDLER.sql_query("select * from user;"))
    app.run()