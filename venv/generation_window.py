import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QDialog

import generate_file.password
from generat import Ui_GenerationPass
import generate_file.button
import generate_file.gener_info


class GeneratWindow(QWidget, Ui_GenerationPass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.line = ""
        for bt in button.Generate_Password:
            getattr(self, bt).clicked.connect(self.set_password)
        self.method_generate()


    def connect_slider_to_spin(self):
        self.SliderLenght.valueChanged.connect(self.SpinboxLenght.setValue)
        self.SpinboxLenght.valueChanged.connect(self.SliderLenght.setValue)
        self.SpinboxLenght.valueChanged.connect(self.set_password)

    def get_characters(self):
        chars = ""
        for bt in button.Characters:
            if getattr(self, bt.name).isChecked():
                chars += bt.value
        return chars

    def set_password(self):
        try:
            self.lineEdit.setText(
                password.create_new(length=self.SpinboxLenght.value(), characters=self.get_characters())
            )
        except IndexError:
            self.lineEdit.clear()

        self.set_strenght()

    def get_character_number(self):
        num = 0
        for bt in button.Characters_Number.items():
            if getattr(self, bt[0]).isChecked():
                num += bt[1]
        return num

    def set_strenght(self):
        length = len(self.lineEdit.text())
        char_num = self.get_character_number()
        for s in password.StrenghtToEntropy:
            if password.get_entropy(length, char_num) >= s.value:
                self.LabelStronk.setText(
                    f"Complexity: {s.name}"
                )

    def do_when_password_edit(self):
        self.lineEdit.textEdited.connect(self.set_strenght())

    def method_generate(self):
        self.connect_slider_to_spin()
        self.set_password()
        self.CopyButton.clicked.connect(self.copy_pass)

    def copy_pass(self):
        QApplication.clipboard().setText(self.lineEdit.text())
        gener_info.save_generate(self.lineEdit.text())



