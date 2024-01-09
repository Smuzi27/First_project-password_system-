# import sqlite3
#
# name = input()
# password = input()
#
#
# def registration(login, password):
#     try:
#         db = sqlite3.connect("database.db")
#         cursor = db.cursor()
#
#         cursor.execute("SELECT login FROM registr WHERE login = ?", [login])
#         if cursor.fetchone() is None:
#             cursor.execute("INSERT INTO registr(login, password) VALUES(?, ?)", [name, password])
#             db.commit()
#         else:
#             print("такой логин существе")
#     except sqlite3.Error as e:
#         print("Error", e)
#     finally:
#         cursor.close()
#         db.close()


# система регистрации

# self.InButton.clicked.connect(self.login)
# # self.UpButton.clicked.connect(self.reg)
# self.authorization_status = False

# def check_input(self):
#     login = self.LoginEdit.setText()
#     passw = self.PasswEdit.setText()
#     db = sqlite3.connect("database.db")
#     cursor = db.cursor()
#     s

#     if login and passw:
#         cursor.execute("SELECT login FROM registr WHERE login = ?", [login])
#         if cursor.fetchone() is None:
#             return "not_found"
#         else:
#             return "exist"
#     else:
#         return "no_data"
#     cursor.close()
#     db.c
#
# def login(self):
#     login = self.LoginEdit.setText()
#     passw = self.PasswEdit.setText()
#     db = sqlite3.connect("database.db")
#     cursor = db.cursor()


import sqlite3
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QDialog
import regis_info
from register import Ui_RegisterWidget


class RegisterWindow(QWidget, Ui_RegisterWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = sqlite3.connect("database.db")
        self.reg = 0
        self.UpButton.clicked.connect(self.sign_up)
        self.InButton.clicked.connect(self.sign_in)

    def sign_in(self):
        self.reg = 0
        self.regist_or_login()

    def sign_up(self):
        self.reg = 1
        self.regist_or_login()

    def regist_or_login(self):
        status = self.reg
        cursor = self.db.cursor()
        login = self.LoginEdit.text()
        password = self.PasswEdit.text()
        if login == "":
            self.statuslabel.setText("Password and Login are REQUIRED")
            return
        elif password == "":
            self.statuslabel.setText("Password and Login are REQUIRED")
            return
        # При status == 0 вход
        if status == 0:
            self.statuslabel.setText("")
            res = cursor.execute("SELECT * FROM registr WHERE login = ?", (login,)).fetchone()

            if res:
                if password == res[2]:
                    self.statuslabel.setText("Login is COMPLETED")
                    regis_info.regis_chek(True, res[0], res[1])
                else:
                    self.statuslabel.setText("Wrong PASSWORD")
        # При status == 1 регистрация
        elif status == 1:
            cursor.execute("SELECT login FROM registr WHERE login = ?", [login])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO registr(login, password) VALUES(?, ?)", (login, password))
                self.db.commit()
                self.db.close()
                self.statuslabel.setText("Registration is COMPLETED")
            else:
                self.statuslabel.setText("Login is USED")