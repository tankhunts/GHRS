

import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit)
from PyQt5.QtCore import *
from bson.objectid import ObjectId
import pymongo

class ViewProfile(QWidget):
    height = 1000
    width = 1000
    ex = pyqtSignal()
    note = pyqtSignal(str)
    sav = pyqtSignal(str, list)
    noteSearch = pyqtSignal(str)
    manage = pyqtSignal(str)
    currRecord = ''
    DOB = QLineEdit()
    race = QLineEdit()
    gender = QLineEdit()
    blood = QLineEdit()
    company = QLineEdit()
    ID = QLineEdit()
    conditions = QTextEdit()
    Perscriptions = QTextEdit() 
    name = QLineEdit()

    currID = ""

    def back(self):
        self.ex.emit()
    def notes(self):
        self.note.emit(self.currID)
    def notesSearch(self):
        self.noteSearch.emit(self.currID)
    def save(self):
        self.sav.emit(self.currID, self.getRecord())
    def setID(self, identifier):
        self.currID = identifier
    
    def managePerscriptions(self):
        self.manage.emit(self.currID)

    def showPrescriptions(self):
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        record = mycol.find_one({'_id': ObjectId(self.currRecord)})
        self.Perscriptions.clear()
        if "Perscriptions" not in record:
            return
        for p in record["Perscriptions"]:
            self.Perscriptions.append(p["strength"] + "  " + p["status"])
            self.Perscriptions.append("\n")
        
    def getRecord(self):
        record = [
            self.name.text(),
            self.DOB.text(),
            self.race.text(),
            self.gender.text(), 
            self.blood.text(),
            self.company.text(),
            self.ID.text()]
            #TODO add notes sections
        return record
    
    def __init__(self):
        super(ViewProfile, self).__init__()
        back = QPushButton("Back")
        notes = QPushButton("Search Notes") 
        nnote = QPushButton("Add note")
        perscription = QPushButton("Manage Perscriptions")
        save = QPushButton("Save Changes")
        top = QHBoxLayout()
        top.addWidget(back)
        top.addWidget(perscription)
        top.addWidget(notes)
        top.addWidget(nnote)
        top.addWidget(save)

        back.clicked.connect(self.back)
        notes.clicked.connect(self.notesSearch)
        nnote.clicked.connect(self.notes)
        save.clicked.connect(self.save)
        perscription.clicked.connect(self.managePerscriptions)


        mid = QHBoxLayout()
        mid.addWidget(self.DOB)
        mid.addWidget(self.race)
        mid.addWidget(self.gender)


        bot = QHBoxLayout()
        bot.addWidget(self.blood)
        bot.addWidget(self.company)
        bot.addWidget(self.ID)


        bottomest = QHBoxLayout()
        bottomest.addWidget(self.conditions)
        bottomest.addWidget(self.Perscriptions)

        nameDesc = QLineEdit("Name")
        nameDesc.setFrame(False)
        nameDesc.setAlignment(Qt.AlignCenter)
        nameDesc.setReadOnly(True)

        dateDesc = QLineEdit("Date of Birth")
        dateDesc.setFrame(False)
        dateDesc.setAlignment(Qt.AlignCenter)
        dateDesc.setReadOnly(True)

        raceDesc = QLineEdit("Race")
        raceDesc.setFrame(False)
        raceDesc.setAlignment(Qt.AlignCenter)
        raceDesc.setReadOnly(True)

        genderDesc = QLineEdit("Gender")
        genderDesc.setFrame(False)
        genderDesc.setAlignment(Qt.AlignCenter)
        genderDesc.setReadOnly(True)

        bloodDesc = QLineEdit("Blood Type")
        bloodDesc.setFrame(False)
        bloodDesc.setAlignment(Qt.AlignCenter)
        bloodDesc.setReadOnly(True)

        compDesc = QLineEdit("Insurance Provider")
        compDesc.setFrame(False)
        compDesc.setAlignment(Qt.AlignCenter)
        compDesc.setReadOnly(True)

        IDDesc = QLineEdit("Insurance Identification")
        IDDesc.setFrame(False)
        IDDesc.setAlignment(Qt.AlignCenter)
        IDDesc.setReadOnly(True)

        condDesc = QLineEdit("Allergies")
        condDesc.setFrame(False)
        condDesc.setAlignment(Qt.AlignCenter)
        condDesc.setReadOnly(True)

        perscDesc = QLineEdit("Perscriptions")
        perscDesc.setFrame(False)
        perscDesc.setAlignment(Qt.AlignCenter)
        perscDesc.setReadOnly(True)

        descOne = QHBoxLayout()
        descTwo = QHBoxLayout()
        descThree = QHBoxLayout()

        descOne.addWidget(dateDesc)
        descOne.addWidget(raceDesc)
        descOne.addWidget(genderDesc)

        descTwo.addWidget(bloodDesc)
        descTwo.addWidget(compDesc)
        descTwo.addWidget(IDDesc)

        descThree.addWidget(condDesc)
        descThree.addWidget(perscDesc)

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

        self.setLayout(overallLayout)

