from PyQt5 import QtCore, QtWidgets

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

import sqlite3
import sys
import regis_info
import generate_file.gener_info
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from generation_window import GeneratWindow
from registrat_window import RegisterWindow
from ui_files.mainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.reg_flag = False
        self.reg_id = 0
        self.action_stat = 0
        self.MainLoginButton.clicked.connect(self.open_main_reg)
        self.PasswGener.clicked.connect(self.open_generat)
        self.AppendButton.clicked.connect(self.add_data_button)
        self.DeleteButton.clicked.connect(self.dell_data_button)
        self.CopyButton.clicked.connect(self.copy_gen_button)
        self.ResumeButton.clicked.connect(self.show_data)
        self.TableButton.clicked.connect(self.save_data)
        self.db_data = sqlite3.connect("database.db")

    # вызов окна регистрации
    def open_main_reg(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    # вызов окна генерации
    def open_generat(self):
        self.gener_window = GeneratWindow()
        self.gener_window.method_generate()
        self.gener_window.show()

    # метод добавление данных в таблицу
    def add_data_button(self):
        self.action_stat = 0
        self.work_with_data()

    # вставка данных из генератора
    def copy_gen_button(self):
        self.PasswEdit.setText(generate_file.gener_info.generat_password)

    # метод удаление записи из таблицы по логину и сервису
    def dell_data_button(self):
        self.action_stat = 1
        self.work_with_data()

    # Метод отображение и обновления данных в таблице
    def show_data(self):
        self.action_stat = 2
        self.work_with_data()

    # Метод сохранения данных файлом
    def save_data(self):
        self.action_stat = 3
        self.work_with_data()

    # метод для работы с базой данных пользователей, выводом данных в таблицу, и сохранения в файл
    def work_with_data(self):
        service = self.ServerEdit.text()
        login = self.LoginEdit.text()
        password = self.PasswEdit.text()
        cursor = self.db_data.cursor()
        reg_id = regis_info.reg_ind
        reg_log = regis_info.login_id
        if regis_info.reg_flag is False and reg_id == 0:
            self.status_lab.setText("CHECK authorization")
        else:
            if self.action_stat == 0:
                # Добавление новой записи или обновление
                if service == "" or password == "":
                    self.status_lab.setText("Password and Service are REQUIRED")
                else:
                    cursor.execute(
                        "SELECT id_user, service, login FROM data WHERE id_user = ? AND service = ? AND login = ?",
                        [reg_id, service, login])
                    if cursor.fetchone() is None:
                        cursor.execute("INSERT INTO data (id_user, service, login, password) VALUES(?, ?, ?, ?)",
                                       [reg_id, service, login, password])
                        self.db_data.commit()
                        self.status_lab.setText("Data ADDED")
                    else:
                        cursor.execute("UPDATE data SET password = ? WHERE id_user = ? AND service = ? AND login = ?",
                                       (password, reg_id, service, login))
                        self.db_data.commit()
                        self.status_lab.setText("Data UPDATED")
            elif self.action_stat == 1:
                # Удаление существующих записей
                if service == "" or login == "":
                    self.status_lab.setText("Service and Login are REQUIRED")
                else:
                    cursor.execute(
                        "SELECT id_user, service, login FROM data WHERE id_user = ? AND service = ? AND login = ?",
                        [reg_id, service, login])
                    if cursor.fetchone() is None:
                        self.status_lab.setText("NO Data found")
                    else:
                        cursor.execute("DELETE FROM data WHERE id_user = ? AND service = ? AND login = ?",
                                       [reg_id, service, login])
                        self.status_lab.setText("Data DELETED")
                        self.db_data.commit()
            elif self.action_stat == 2 or self.action_stat == 3:
                promt_ser = self.SearchLine.text()
                req = f"SELECT service, login, password FROM data WHERE id_user = {reg_id} AND service LIKE '" \
                      f"{promt_ser}%'"
                res = cursor.execute(req).fetchall()
                if res is None:
                    self.status_lab.setText("NO data for table")
                else:
                    # Отображение данных конкретного пользователся с возможностью поска
                    if self.action_stat == 2:
                        self.tableWidget.setColumnCount(3)
                        self.tableWidget.setHorizontalHeaderLabels(["Service", "Login", "Password"])
                        self.tableWidget.setRowCount(len(res))
                        tab = 0
                        for row in res:
                            self.tableWidget.setItem(tab, 0, QTableWidgetItem(row[0]))
                            self.tableWidget.setItem(tab, 1, QTableWidgetItem(row[1]))
                            self.tableWidget.setItem(tab, 2, QTableWidgetItem(row[2]))
                            tab += 1
                        self.tableWidget.resizeColumnsToContents()
                        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                    # сохранение txt файла с данными отображаемой таблицы
                    elif self.action_stat == 3:
                        fname = \
                        QFileDialog.getSaveFileName(self, 'Select the path and enter the name of the file to save',
                                                    f'info_{reg_log}', '*.txt')[0]
                        file = open(fname, "w")
                        file.write("service, login, password" + "\n")
                        for row in res:
                            file.write("; ".join(row))
                            file.write("\n")
                        file.close()

    # после закрытия закрывается и соединение с бд
    def closeEvent(self, event):
        self.db_data.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
