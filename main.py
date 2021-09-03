# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request
import re

app = Flask(__name__)

HANDLER = None


#Simple function just to verify all characters are English characters
def is_english(txt):
    try:
        txt.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def valid_email(email):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(email_regex, email)):
        return True
    else:
        return False

class AppHandler:
    def __init__(self, db_loc=":memory:"):
        self.db_loc = db_loc

    def db_init(self):
        try:
            conn = sqlite3.connect(self.db_loc)
        except Error as e:
            print(e)

    def table_init(self):
        #Normally this would be stored in a separate file, but for the sake of time it is just here.
        sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                email text NOT NULL UNIQUE,
                                                password NOT NULL
                                            ); """
        self.sql_cmd(sql_create_user_table)

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
                con.commit()
        except Error as e:
            print(e)

    def sql_user_exists(self, in_str):
        result = self.sql_query("select count(*) from user where email ='{}';".format(in_str))
        if result[0][0]:
            return True
        return False

    def sql_create_user(self, name, pw, email):
        self.sql_cmd("insert into user(name, password, email) values ('{}', '{}', '{}');".format(name, pw, email))


@app.route('/')
def main(inp = "Welcome!"):
    print(HANDLER.sql_query("select * from user;"))
    return render_template('main.html', x = inp)


@app.route('/print_user')
def print_user():
    result = HANDLER.sql_query("select * from user;")
    return render_template('print.html', users = result)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    send = request.form['send']
    email = email.lower()
    if not is_english(email) or not is_english(name) or not is_english(password):
        return main("English only please")
    if not valid_email(email):
        return main("Please enter a valid e-mail")
    if send == 'create user':
        if not email or not name or not password:
            return main("Please fill out all fields!")
        else:
            if HANDLER.sql_user_exists(email):
                return main("Account already exists for email: {}".format(email))
            else:
                HANDLER.sql_create_user(name, password, email)
                return main("User {} for email {} added!".format(name, email))
    elif send == 'delete user':
        if not HANDLER.sql_user_exists(email):
            return main("Account does not exist for email: {}".format(email))
        else:
            HANDLER.sql_cmd("delete from user where email = '{}';".format(email))
            return main("Deleted account with email: {}!".format(email))

if __name__ == '__main__':
    HANDLER = AppHandler("C:/!Coding/sqltest.db")
    HANDLER.db_init()
    HANDLER.table_init()
    #Test data
    HANDLER.sql_create_user("joe", "cats", "me@test.com")
    HANDLER.sql_create_user("bob", "dogs", "you@test.com")
    app.run()