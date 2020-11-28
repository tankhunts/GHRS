from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

app = QApplication([])


import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit)
from PyQt5.QtCore import *
from PyQt5 import QtGui


class NotesPopup(QWidget):
    name = QLineEdit()
    addProfile = QGroupBox("Notes:")
    notes = QTextEdit()
    name.setPlaceholderText("Name of Note")
    notes.setPlaceholderText("Type Notes Here")

    exPop = pyqtSignal()
    note = pyqtSignal(list)

    def cancel(self):
        self.close()

    def savingNote(self):
        self.note.emit(self.getNotes())
        self.close()

    def getNotes(self):
        record = [
            self.name.text(),
            self.notes.toPlainText()
        ]
        return record

    def updateFields(self, initNote):
        self.notes.setText(initNote[0])
        self.name.setText(initNote[1])

    def __init__(self):
        QWidget.__init__(self)

        saveNote = QPushButton("Save Note")
        back = QPushButton("Cancel")

        saveNote.clicked.connect(self.savingNote)
        back.clicked.connect(self.cancel)

        mainLayout = QGridLayout()
        overallLayout = QVBoxLayout()

        overallLayout.addWidget(self.name)
        overallLayout.addWidget(self.notes)
        self.addProfile.setLayout(overallLayout)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(back)
        buttonLayout.addWidget(saveNote)

        mainLayout.addWidget(self.addProfile)

        mainLayout.addWidget(saveNote)
        mainLayout.addWidget(back)

        self.setLayout(mainLayout)


class maker(QWidget):
    height = 1000
    width = 1000
    ex = pyqtSignal()
    sav = pyqtSignal(list)
    currRecord = ''
    race = QLineEdit()
    DOB = QLineEdit()
    #DOB = QDateEdit()
    #DOB.setDisplayFormat("MM/dd/yyyy")
    #DOB.setBaseSize(race.size())
    #DOB.setSizePolicy(race.sizePolicy())


    gender = QLineEdit()
    blood = QLineEdit()
    company = QLineEdit()
    ID = QLineEdit()
    conditions = QTextEdit()
    #Prescriptions = QTextEdit()
    name = QLineEdit()
    notes = ["", ""]

    noteMaker = NotesPopup()



    addProfile = QGroupBox("Add Profile")

    def back(self):
        self.ex.emit()
    def addNotes(self):
        self.noteMaker.updateFields(self.notes)
        self.noteMaker.setGeometry(self.geometry())
        self.noteMaker.show()

    def updateNote(self, newNote):
        self.notes = newNote
    def save(self):
        self.sav.emit(self.getRecord())
        self.ex.emit()

    def getRecord(self):
        record = [
            self.name.text(),
            self.DOB.text(),
            #str((self.DOB.date().toString())),
            self.race.text(),
            self.gender.text(),
            self.blood.text(),
            self.company.text(),
            self.ID.text(),
            self.conditions.toPlainText(),
            self.notes[0],
            self.notes[1]
            ]
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
        nnote.clicked.connect(self.addNotes)
        save.clicked.connect(self.save)
        self.noteMaker.note.connect(self.updateNote)

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
