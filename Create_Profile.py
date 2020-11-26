from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

app = QApplication([])


import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit)
from PyQt5.QtCore import *
from PyQt5 import QtGui

class maker(QWidget):
    height = 1000
    width = 1000
    ex = pyqtSignal()
    sav = pyqtSignal()
    note = pyqtSignal(str)
    sav = pyqtSignal(str, list)
    currRecord = ''
    race = QLineEdit()
    DOB = QDateEdit()
    DOB.setDisplayFormat("MM/dd/yyyy")
    DOB.setBaseSize(race.size())
    DOB.setSizePolicy(race.sizePolicy())

    gender = QLineEdit()
    blood = QLineEdit()
    company = QLineEdit()
    ID = QLineEdit()
    conditions = QTextEdit()
    Prescriptions = QTextEdit()
    name = QLineEdit()

    addProfile = QGroupBox("Add Profile")

    def back(self):
        self.ex.emit()
    def notes(self):
        self.note.emit("")
    def save(self):
        self.sav.emit(self.currID, self.getRecord())
        self.ex.emit()

    def getRecord(self):
        record = [
            self.name.text(),
            str(self.DOB.date()),
            self.race.text(),
            self.gender.text(),
            self.blood.text(),
            self.company.text(),
            self.ID.text()]
            #TODO add notes sections
        return record
    def __init__(self):
        super(maker, self).__init__()
        back = QPushButton("Back")
        nnote = QPushButton("Add note")
        save = QPushButton("Add Patient")
        top = QHBoxLayout()
        top.addWidget(back)
        top.addWidget(nnote)
        top.addWidget(save)

        back.clicked.connect(self.back)
        save.clicked.connect(self.save)

        mid = QHBoxLayout()
        mid.setAlignment(Qt.AlignCenter)
        mid.addWidget(self.DOB)
        mid.addWidget(self.race)
        mid.addWidget(self.gender)

        bot = QHBoxLayout()
        bot.setAlignment(Qt.AlignCenter)
        bot.addWidget(self.blood)
        bot.addWidget(self.company)
        bot.addWidget(self.ID)

        bottomest = QHBoxLayout()
        bottomest.addWidget(self.conditions)

        descPal = QtGui.QPalette()
        descPal.setColor(QPalette.Base, Qt.lightGray)

        nameDesc = QLineEdit("Name")
        nameDesc.setPalette(descPal)
        nameDesc.setAutoFillBackground(True)
        nameDesc.setFrame(False)
        nameDesc.setAlignment(Qt.AlignCenter)
        nameDesc.setReadOnly(True)

        dateDesc = QLineEdit("Date of Birth (MM/DD/YYYY)")
        dateDesc.setFrame(False)
        dateDesc.setPalette(descPal)
        dateDesc.setAutoFillBackground(True)
        dateDesc.setAlignment(Qt.AlignCenter)
        dateDesc.setReadOnly(True)

        raceDesc = QLineEdit("Race/Ethnicity")
        raceDesc.setPalette(descPal)
        raceDesc.setAutoFillBackground(True)
        raceDesc.setFrame(False)
        raceDesc.setAlignment(Qt.AlignCenter)
        raceDesc.setReadOnly(True)

        genderDesc = QLineEdit("Gender")
        genderDesc.setPalette(descPal)
        genderDesc.setAutoFillBackground(True)
        genderDesc.setFrame(False)
        genderDesc.setAlignment(Qt.AlignCenter)
        genderDesc.setReadOnly(True)

        bloodDesc = QLineEdit("Blood Type")
        bloodDesc.setPalette(descPal)
        bloodDesc.setAutoFillBackground(True)
        bloodDesc.setFrame(False)
        bloodDesc.setAlignment(Qt.AlignCenter)
        bloodDesc.setReadOnly(True)

        compDesc = QLineEdit("Insurance Provider")
        compDesc.setPalette(descPal)
        compDesc.setAutoFillBackground(True)
        compDesc.setFrame(False)
        compDesc.setAlignment(Qt.AlignCenter)
        compDesc.setReadOnly(True)

        IDDesc = QLineEdit("Insurance Identification")
        IDDesc.setPalette(descPal)
        IDDesc.setAutoFillBackground(True)
        IDDesc.setFrame(False)
        IDDesc.setAlignment(Qt.AlignCenter)
        IDDesc.setReadOnly(True)

        condDesc = QLineEdit("Allergies")
        condDesc.setPalette(descPal)
        condDesc.setAutoFillBackground(True)
        condDesc.setFrame(False)
        condDesc.setAlignment(Qt.AlignCenter)
        condDesc.setReadOnly(True)

        descOne = QHBoxLayout()
        descOne.setAlignment(Qt.AlignCenter)
        descTwo = QHBoxLayout()
        descTwo.setAlignment(Qt.AlignCenter)
        descThree = QHBoxLayout()
        descThree.setAlignment(Qt.AlignCenter)

        descOne.addWidget(dateDesc)
        descOne.addWidget(raceDesc)
        descOne.addWidget(genderDesc)

        descTwo.addWidget(bloodDesc)
        descTwo.addWidget(compDesc)
        descTwo.addWidget(IDDesc)

        descThree.addWidget(condDesc)

        overallLayout = QVBoxLayout()
        overallLayout.addWidget(nameDesc)
        overallLayout.addWidget(self.name)
        overallLayout.addLayout(descOne)
        overallLayout.addLayout(mid)
        overallLayout.addLayout(descTwo)
        overallLayout.addLayout(bot)
        overallLayout.addLayout(descThree)
        overallLayout.addLayout(bottomest)
        overallLayout.addLayout(top)

        mainLayout = QGridLayout()

        self.addProfile.setLayout(overallLayout)
        mainLayout.addWidget(self.addProfile)

        self.setLayout(mainLayout)
