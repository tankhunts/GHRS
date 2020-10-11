

import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit)
from PyQt5.QtCore import pyqtSignal

class ViewProfile(QWidget):
    height = 1000
    width = 1000
    criteria = QComboBox()
    search = QLineEdit()
    scrollData = QVBoxLayout()
    ex = pyqtSignal()
    note = pyqtSignal()

    def back(self):
        self.ex.emit()
    def notes(self):
        self.note.emit()
    def __init__(self):
        super(ViewProfile, self).__init__()
        back = QPushButton("Back")
        name = QLineEdit()
        notes = QPushButton("View or add note")
        top = QHBoxLayout()
        top.addWidget(back)
        top.addWidget(name)
        top.addWidget(notes)

        back.clicked.connect(self.back)
        notes.clicked.connect(self.notes)

        DOB = QLineEdit()
        race = QLineEdit()
        gender = QLineEdit()
        mid = QHBoxLayout()
        mid.addWidget(DOB)
        mid.addWidget(race)
        mid.addWidget(gender)

        blood = QLineEdit()
        company = QLineEdit()
        ID = QLineEdit()
        bot = QHBoxLayout()
        bot.addWidget(blood)
        bot.addWidget(company)
        bot.addWidget(ID)

        conditions = QTextEdit()
        Perscriptions = QTextEdit()
        bottomest = QHBoxLayout()
        bottomest.addWidget(conditions)
        bottomest.addWidget(Perscriptions)

        overallLayout = QVBoxLayout()
        overallLayout.addLayout(top)
        overallLayout.addLayout(mid)
        overallLayout.addLayout(bot)
        overallLayout.addLayout(bottomest)

        self.setLayout(overallLayout)

