import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QTextEdit, QGroupBox, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea)
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtCore import *
import pymongo
from bson.objectid import ObjectId

class WarningPopup(QWidget):

    name = QLineEdit()
    addProfile = QGroupBox("Delete Profile:")
    warn = QTextEdit("Are you sure you want to delete this note?")

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


class searchNotes(QWidget):
    
    height = 1000
    width = 1000
    currId = ''
    criteria = QComboBox()
    search = QLineEdit()
    scrollData = QVBoxLayout()
    ex = pyqtSignal()
    op = pyqtSignal(dict, str, bool)
    comboData = ["Date", "Keyword", "Subject"]
    adding_note = pyqtSignal(str, bool)

    delete_entry = {}

    warn = WarningPopup()

    def add(self):
        self.adding_note.emit(self.currId, False)

    def warning(self, noteDict):
        self.delete_entry = noteDict
        print(self.delete_entry)
        self.warn.show()

    def delete(self):
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        mycol.update({'_id': ObjectId(self.currId)}, {"$pull": {"Notes": {"Date": self.delete_entry["Date"], "Note": self.delete_entry["Note"],
                                                       "Subject": self.delete_entry["Subject"]}}})
        delete_entry = {}



    def return_search_results(self, criteria, text):
        results = []
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        notes = mycol.find_one({'_id': ObjectId(self.currId)})["Notes"]
        if(criteria == 'Keyword'):
            criteria = "Note"
        if(text != ''):
            for note in notes:
                if text.lower() in note[criteria].lower():
                    results.append(note)
        else:
            results = notes
        results = sorted(results, key = lambda i: i[criteria])
        return results
        
    def open_note(self, noteDict):
        self.op.emit(noteDict, self.currId, True)
        
    def create_result(self, noteDict):
        layout = QHBoxLayout()
        text = QLineEdit(noteDict["Subject"])
        age = QLineEdit(noteDict["Date"])
        ope = QPushButton("Open")
        dele = QPushButton("Delete")

        
        text.setReadOnly(True)
        age.setReadOnly(True)
        ope.clicked.connect(lambda: self.open_note(noteDict))
        dele.clicked.connect(lambda: self.warning(noteDict))

        layout.addWidget(text)
        layout.addWidget(age)
        layout.addWidget(ope)
        layout.addWidget(dele)
        return layout
    
    def clear(self):
        self.clear_layout(self.scrollData)
        self.search.clear()
        self.criteria.clear()
        self.criteria.addItems(self.comboData)

    #code taken from https://stackoverflow.com/questions/9374063/remove-all-items-from-a-layout
    def clear_layout(self, layout):
        if(layout is not None):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
    
    def begin_search(self):
        self.clear_layout(self.scrollData)
        data = self.return_search_results(self.criteria.currentText(), self.search.text())
        for item in data:
            self.scrollData.addLayout(self.create_result(item))
        
    def back(self):
        self.criteria.clear()
        self.criteria.addItems(self.comboData)
        self.clear_layout(self.scrollData)
        self.search.clear()
        self.ex.emit()

    def __init__(self):
        super(searchNotes, self).__init__()
        self.resize(self.width, self.height)      
        barLayout = QHBoxLayout()
        addNote = QPushButton("Add Note")
        enter = QPushButton("Search")    
        back = QPushButton("Back")
        addNote.clicked.connect(self.add)
        self.criteria.addItems(self.comboData)
        enter.clicked.connect(self.begin_search)
        back.clicked.connect(self.back) 
        barLayout.addWidget(back)
        barLayout.addWidget(self.criteria)
        barLayout.addWidget(self.search)
        barLayout.addWidget(enter)
        scrollContents = QWidget()
        scroll = QScrollArea()
        scrollContents.setLayout(self.scrollData)
        resultLayout = QVBoxLayout()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scrollContents)
        resultLayout.addLayout(barLayout)
        resultLayout.addWidget(scroll)
        resultLayout.addWidget(addNote)

        self.warn.confirmed.connect(self.delete)
        self.warn.confirmed.connect(self.begin_search)

        self.setLayout(resultLayout)