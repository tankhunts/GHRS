import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea)
from PyQt5.QtCore import pyqtSignal

class searchNotes(QWidget):
    
    height = 1000
    width = 1000
    currId = ''
    criteria = QComboBox()
    search = QLineEdit()
    scrollData = QVBoxLayout()
    ex = pyqtSignal()
    op = pyqtSignal(str)
    comboData = ["Date", "Keyword"]

    def return_search_results(self, criteria, text):
        results = []
        
        return results
        
    def open_profile(self, name):
        self.op.emit(name)
        
    def create_result(self, name, date):
        layout = QHBoxLayout()
        text = QLineEdit(name)
        age = QLineEdit(str(date))
        ope = QPushButton("Open")
        
        text.setReadOnly(True)
        age.setReadOnly(True)
        ope.clicked.connect(lambda: self.open_profile(name))
        
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
        data = self.return_search_results(self.criteria.currentData(), self.search.text())
        for item in data:
            self.scrollData.addLayout(self.create_result(item["name"], item["age"]))
        
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