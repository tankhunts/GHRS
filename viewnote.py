

import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from datetime import date
from bson.objectid import ObjectId
import pymongo

class ViewNote(QWidget):
    note = QTextEdit()
    ret = pyqtSignal(str)
    subject = QLineEdit()
    prof_id = ''
    date = ''
    oldDict={}

    subject.setPlaceholderText("Name of Note")
    note.setPlaceholderText("Type Notes Here")

    addNote = QGroupBox("Note:")


    def back(self):
        self.ret.emit(self.prof_id)
        self.clear()

    def save(self):
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        if(self.date == ''):
            mycol.update({'_id': ObjectId(self.prof_id)}, {"$push": {"Notes": {"Date": str(date.today()), "Note": self.note.toPlainText(), "Subject": self.subject.text()}}})
        else:
            id = ObjectId(self.prof_id)

            mycol.update({'_id': id}, {"$pull": {"Notes": {"Date": self.oldDict["Date"], "Note": self.oldDict["Note"],
                                                           "Subject": self.oldDict["Subject"]}}})
            mycol.update({'_id': id}, {"$push": {
                "Notes": {"Date": self.date, "Note": self.note.toPlainText(), "Subject": self.subject.text()}}})
        self.ret.emit(self.prof_id)
        self.clear()

    def clear(self):
        self.note.clear()
        self.date = ''
        self.prof_id = ''
        self.subject.clear()
        self.oldDict={}
    def __init__(self):
        super(ViewNote, self).__init__()
        back = QPushButton("Back")
        save = QPushButton("Save Changes")
        
        bottom = QHBoxLayout()
        bottom.addWidget(back)
        bottom.addWidget(save)

        overallLayout = QVBoxLayout()
        overallLayout.addWidget(self.subject)
        overallLayout.addWidget(self.note)

        back.clicked.connect(self.back)
        save.clicked.connect(self.save)

        mainLayout = QVBoxLayout()
        self.addNote.setLayout(overallLayout)
        mainLayout.addWidget(self.addNote)

        mainLayout.addLayout(bottom)

        self.setLayout(mainLayout)

