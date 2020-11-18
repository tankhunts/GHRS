# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 20:57:53 2020

@author: matth
"""
import pymongo
import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea)
from PyQt5.QtCore import pyqtSignal


class Export(QWidget):
    
    height = 1000
    width = 1000
    criteria = QComboBox()
    search = QLineEdit()
    scrollData = QVBoxLayout()
    ex = pyqtSignal()
    export = pyqtSignal(str)
    comboData = ["First Name", "Last Name", "Full Name", "DOB"]
    dbList = []

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
        
    def add_profile(self, db_entry):
        self.dbList.append(db_entry)
        self.begin_search()    
    
    def remove_profile(self, db_entry):
        self.dbList.remove(db_entry)
        self.begin_search()     
        
    def create_result_add(self, name, age, db_entry):
        layout = QHBoxLayout()
        text = QLineEdit(name)
        age = QLineEdit(str(age))
        ope = QPushButton("Add") 
        
        text.setReadOnly(True)
        age.setReadOnly(True)
        ope.clicked.connect(lambda: self.add_profile(db_entry))
        
        layout.addWidget(text)
        layout.addWidget(age)
        layout.addWidget(ope)
        return layout
    def create_result_remove(self, name, age, db_entry):
        layout = QHBoxLayout()
        text = QLineEdit(name)
        age = QLineEdit(str(age))
        ope = QPushButton("Remove")
        
        text.setReadOnly(True)
        age.setReadOnly(True)
        ope.clicked.connect(lambda: self.remove_profile(db_entry))
        
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
        addRem = QHBoxLayout()
        remove = QPushButton("Remove all searched profiles")
        add = QPushButton("Add all searched profiles")
        remove.clicked.connect(lambda: self.removeSearched(data))
        add.clicked.connect(lambda: self.addSearched(data))
        addRem.addWidget(add)
        addRem.addWidget(remove)
        self.scrollData.addLayout(addRem)
        for item in data:
            if item in self.dbList:
                self.scrollData.addLayout(self.create_result_remove(item["First Name"] + ' ' + item["Last Name"], item["DOB"], item))
            else:
                self.scrollData.addLayout(self.create_result_add(item["First Name"] + ' ' + item["Last Name"], item["DOB"], item))
        
    def back(self):
        self.criteria.clear()
        self.criteria.addItems(self.comboData)
        self.clear_layout(self.scrollData)
        self.search.clear()
        self.dbList.clear()
        self.ex.emit()

    def addAll(self):
        self.clear_layout(self.scrollData)
        data = self.return_search_results('First Name', '')
        for item in data:
            if item not in self.dbList:
                self.dbList.append(item)

    def removeAll(self):
        self.clear_layout(self.scrollData)
        self.dbList.clear()

    def addSearched(self, results):
        for result in results:
            if result not in self.dbList:
                self.dbList.append(result)
        self.begin_search()                 
    
    def removeSearched(self, results):
        for result in results:
            if result in self.dbList:
                self.dbList.remove(result)   
        self.begin_search() 

    def __init__(self):
        super(Export, self).__init__()
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

        addAll = QPushButton("Add all profiles from export")
        removeAll = QPushButton("Remove all profiles from export")
        export = QPushButton("Export")
        options = QHBoxLayout()
        options.addWidget(addAll)
        options.addWidget(removeAll)
        options.addWidget(export)

        addAll.clicked.connect(self.addAll)
        removeAll.clicked.connect(self.removeAll)
#        export.clicked.connect(self.export)

        resultLayout.addLayout(barLayout)
        resultLayout.addWidget(scroll)
        resultLayout.addLayout(options)

        self.setLayout(resultLayout)