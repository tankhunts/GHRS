import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea)
from PyQt5.QtCore import pyqtSignal
import pymongo
from bson.objectid import ObjectId

class searchNotes(QWidget):
    
    height = 1000
    width = 1000
    currId = ''
    criteria = QComboBox()
    search = QLineEdit()
    scrollData = QVBoxLayout()
    ex = pyqtSignal()
    op = pyqtSignal(dict)
    comboData = ["Date", "Keyword", "Subject"]

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
        self.op.emit(noteDict)
        
    def create_result(self, noteDict):
        layout = QHBoxLayout()
        text = QLineEdit(noteDict["Subject"])
        age = QLineEdit(noteDict["Date"])
        ope = QPushButton("Open")
        
        text.setReadOnly(True)
        age.setReadOnly(True)
        ope.clicked.connect(lambda: self.open_note(noteDict))
        
        layout.addWidget(text)
        layout.addWidget(age)
        layout.addWidget(ope)
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
        enter = QPushButton("Search")    
        back = QPushButton("Back")
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
        self.setLayout(resultLayout)