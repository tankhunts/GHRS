# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 20:57:53 2020

@author: matth
"""
import pymongo
import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QGroupBox)
from PyQt5.QtCore import pyqtSignal


class Searching(QWidget):
    
    height = 1000
    width = 1000
    criteria = QComboBox()
    search = QLineEdit()
    scrollData = QVBoxLayout()
    title = QGroupBox("Searching Profiles")
    ex = pyqtSignal()
    op = pyqtSignal(str)
    comboData = ["First Name", "Last Name", "Full Name", "DOB", "Keyword"]

    def return_search_results(self, criteria, text):
        results = []
        mongodbIter = 0
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        if(text == ''):
            mongodbIter = mycol.find()
        else:
            if(criteria != 'Full Name'):
                myquery = {criteria: {"$regex": "^"+text, "$options": "-i"}}
            else:
                myquery = {"$or": [{"First Name": {"$regex": "^"+text, "$options": "-i"}}, {"Last Name": {"$regex": "^"+text, "$options": "-i"}}]}
            mongodbIter = mycol.find(myquery)
        for item in mongodbIter:
            results.append(item)
        if(criteria != 'Full Name'):
            results = sorted(results, key = lambda i: i[criteria])
        else:
            results = sorted(results, key = lambda i: i["First Name"])
        return results
        
    def open_profile(self, name):
        self.op.emit(name)
        
    def create_result(self, name, age, id):
        layout = QHBoxLayout()
        text = QLineEdit(name)
        age = QLineEdit(str(age))
        ope = QPushButton("Open")
        
        text.setReadOnly(True)
        age.setReadOnly(True)
        ope.clicked.connect(lambda: self.open_profile(id))
        
        layout.addWidget(text)
        layout.addWidget(age)
        layout.addWidget(ope)
        return layout
    
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
            self.scrollData.addLayout(self.create_result(item["First Name"] + ' ' + item["Last Name"], item["DOB"], str(item["_id"])))
        
    def back(self):
        self.criteria.clear()
        self.criteria.addItems(self.comboData)
        self.clear_layout(self.scrollData)
        self.search.clear()
        self.ex.emit()

    def __init__(self):
        super(Searching, self).__init__()
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

        mainLayout = QVBoxLayout()
        self.title.setLayout(resultLayout)
        mainLayout.addWidget(self.title)

        self.setLayout(mainLayout)
