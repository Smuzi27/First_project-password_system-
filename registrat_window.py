import sqlite3
from PyQt5.QtWidgets import QWidget
import regis_info
from ui_files.register import Ui_RegisterWidget


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

    #метод авторизации
    #Чтобы выйти в акаунт нужно зарегистрироваться и после войти в аккаунт
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
            else:
                self.statuslabel.setText("LOGIN NOT found")
        # При status == 1 регистрация
        elif status == 1:
            cursor.execute("SELECT login FROM registr WHERE login = ?", [login])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO registr(login, password) VALUES(?, ?)", (login, password))
                self.db.commit()
                self.statuslabel.setText("Registration is COMPLETED")
            else:
                self.statuslabel.setText("Login is USED")

    # при закрытии закрывается и соединение с бд
    def closeEvent(self, event):
        self.db.close()
