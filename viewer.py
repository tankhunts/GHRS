

import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout,QDateEdit, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit, QGridLayout, QGroupBox)
from PyQt5.QtCore import *
from PyQt5 import (QtGui)
from bson.objectid import ObjectId
import pymongo

class WarningPopup(QWidget):

    name = QLineEdit()
    addProfile = QGroupBox("Delete Profile:")
    warn = QTextEdit("Are you sure you want to delete this profile?")

    warn.isReadOnly()

    exPop = pyqtSignal()
    confirmed = pyqtSignal()
    def delete(self):
        self.confirmed.emit()
        self.close()
    def cancel(self):
        self.close()

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("WARNING: Deleting Profile")

        confirm = QPushButton("Delete")
        back = QPushButton("Cancel")

        confirm.clicked.connect(self.delete)
        back.clicked.connect(self.cancel)
        descPal = QtGui.QPalette()
        descPal.setColor(QtGui.QPalette.Text, Qt.red)
        self.warn.setPalette(descPal)

        mainLayout = QVBoxLayout()
        overallLayout = QVBoxLayout()

        overallLayout.addWidget(self.warn)
        self.addProfile.setLayout(overallLayout)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(confirm)
        buttonLayout.addWidget(back)

        mainLayout.addWidget(self.addProfile)

        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)


class ViewProfile(QWidget):
    height = 1000
    width = 1000
    dele = pyqtSignal(str)
    ex = pyqtSignal()
    note = pyqtSignal(str)
    sav = pyqtSignal(str, list)
    noteSearch = pyqtSignal(str)
    manage = pyqtSignal(str)
    currRecord = ''

    delete_warning = WarningPopup()

    gender = QLineEdit()


    #race = QLineEdit()
    race = QComboBox()
    race.setBaseSize(gender.size())
    race.setSizePolicy(gender.sizePolicy())

    DOB = QDateEdit()
    DOB.setDisplayFormat("yyyy-MM-dd")
    DOB.setBaseSize(gender.size())
    DOB.setSizePolicy(gender.sizePolicy())

    #blood = QLineEdit()
    blood = QComboBox()
    blood.setBaseSize(gender.size())
    blood.setSizePolicy(gender.sizePolicy())

    company = QLineEdit()
    ID = QLineEdit()
    conditions = QTextEdit()
    Perscriptions = QTextEdit() 
    name = QLineEdit()

    bloodT = ["", "A+", "AB+", "B+", "O+", "A-", "AB-", "B-", "O-"]
    raceT = ["", "American Indian", "Asian", "Black", "Hispanic", "Native Hawaiian", "White"]

    currID = ""

    editProfile = QGroupBox("View/Edit Profile:")

    def warn(self):
        self.delete_warning.show()
    def delete(self):
        self.dele.emit(self.currID)
        self.ex.emit()
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
        QDate_ofBirth = self.DOB.date()
        record = [
            self.name.text(),
            QDate_ofBirth.toString("yyyy-MM-dd"),
            str(self.race.currentText()),
            self.gender.text(),
            str(self.blood.currentText()),
            self.company.text(),
            self.ID.text(),
            self.conditions.toPlainText()]
            #TODO add notes sections
        return record
    
    def __init__(self):
        super(ViewProfile, self).__init__()
        back = QPushButton("Back")
        notes = QPushButton("Notes")
        #nnote = QPushButton("Add note")
        perscription = QPushButton("Manage Perscriptions")
        save = QPushButton("Save Changes")
        delete_but = QPushButton("Delete Profile")
        toppest = QHBoxLayout()
        toppest.addWidget(back)
        toppest.addWidget(save)
        top = QHBoxLayout()
        top.addWidget(perscription)
        top.addWidget(notes)
        #top.addWidget(nnote)
        top.addWidget(delete_but)

        back.clicked.connect(self.back)
        notes.clicked.connect(self.notesSearch)
        #nnote.clicked.connect(self.notes)
        delete_but.clicked.connect(self.warn)

        save.clicked.connect(self.save)
        perscription.clicked.connect(self.managePerscriptions)

        self.race.addItems(self.raceT)
        self.blood.addItems(self.bloodT)

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

        descPal = QtGui.QPalette()
        descPal.setColor(QtGui.QPalette.Base, Qt.lightGray)

        nameDesc = QLineEdit("Name")
        nameDesc.setPalette(descPal)
        nameDesc.setFrame(False)
        nameDesc.setAlignment(Qt.AlignCenter)
        nameDesc.setReadOnly(True)

        dateDesc = QLineEdit("Date of Birth (YYYY-MM-DD)")
        dateDesc.setPalette(descPal)
        dateDesc.setFrame(False)
        dateDesc.setAlignment(Qt.AlignCenter)
        dateDesc.setReadOnly(True)

        raceDesc = QLineEdit("Race")
        raceDesc.setPalette(descPal)
        raceDesc.setFrame(False)
        raceDesc.setAlignment(Qt.AlignCenter)
        raceDesc.setReadOnly(True)

        genderDesc = QLineEdit("Gender")
        genderDesc.setPalette(descPal)
        genderDesc.setFrame(False)
        genderDesc.setAlignment(Qt.AlignCenter)
        genderDesc.setReadOnly(True)

        bloodDesc = QLineEdit("Blood Type")
        bloodDesc.setPalette(descPal)
        bloodDesc.setFrame(False)
        bloodDesc.setAlignment(Qt.AlignCenter)
        bloodDesc.setReadOnly(True)

        compDesc = QLineEdit("Insurance Provider")
        compDesc.setPalette(descPal)
        compDesc.setFrame(False)
        compDesc.setAlignment(Qt.AlignCenter)
        compDesc.setReadOnly(True)

        IDDesc = QLineEdit("Insurance Identification")
        IDDesc.setPalette(descPal)
        IDDesc.setFrame(False)
        IDDesc.setAlignment(Qt.AlignCenter)
        IDDesc.setReadOnly(True)

        condDesc = QLineEdit("Allergies")
        condDesc.setPalette(descPal)
        condDesc.setFrame(False)
        condDesc.setAlignment(Qt.AlignCenter)
        condDesc.setReadOnly(True)

        perscDesc = QLineEdit("Perscriptions")
        perscDesc.setPalette(descPal)
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

        mainLayout = QVBoxLayout()

        self.editProfile.setLayout(overallLayout)
        mainLayout.addWidget(self.editProfile)
        mainLayout.addLayout(top)
        mainLayout.addLayout((toppest))

        self.delete_warning.confirmed.connect(self.delete)

        self.setLayout(mainLayout)

