

import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit)
from PyQt5.QtCore import pyqtSignal
from datetime import date
from bson.objectid import ObjectId
import pymongo

class ViewNote(QWidget):
    note = QTextEdit()
    ret = pyqtSignal()
    subject = QLineEdit()
    prof_id = ''
    date = ''
    oldDict={}


    def back(self):
        self.clear()
        self.ret.emit()
    def save(self):
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        if(self.date == ''):
            mycol.update({'_id': ObjectId(self.prof_id)}, {"$push": {"Notes": {"Date": str(date.today()), "Note": self.note.toPlainText(), "Subject": self.subject.text()}}})
        else:
            mycol.update({'_id': ObjectId(self.prof_id)}, {"$push": {"Notes": {"Date": self.date, "Note": self.note.toPlainText(), "Subject": self.subject.text()}}})
            mycol.update({'_id': ObjectId(self.prof_id)}, {"$pull": {"Notes": {"Date": self.oldDict["Date"], "Note": self.oldDict["Note"], "Subject": self.oldDict["Subject"]}}})
        self.clear()
        self.ret.emit()
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
        overallLayout.addLayout(bottom)

        back.clicked.connect(self.back)
        save.clicked.connect(self.save)

        self.setLayout(overallLayout)

