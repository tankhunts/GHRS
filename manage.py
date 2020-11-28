import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit)
from PyQt5.QtCore import *



class Manage(QWidget):

    search_drug = QPushButton("Search for a drug")
    curr_label = QLabel("Current Perscriptions")
    curr_prescriptions = QTextEdit()

    drug_search = pyqtSignal()
    go_back = pyqtSignal(str)

    currID = ''

    def search(self):
        self.drug_search.emit()

    def back(self):
        self.go_back.emit(self.currID)

    def setID(self, identifier):
        self.currID = identifier

    def __init__(self):
        super(Manage, self).__init__()
        search_drug = QPushButton("Search for a drug")
        curr_label = QLabel("Current Perscriptions")
        back_button = QPushButton("Back")
        search_drug.clicked.connect(self.search)
        back_button.clicked.connect(self.back)

        overallLayout = QVBoxLayout()
        overallLayout.addWidget(search_drug)
        overallLayout.addWidget(curr_label)
        overallLayout.addWidget(self.curr_prescriptions)
        overallLayout.addWidget(back_button)
        self.setLayout(overallLayout)


        
        


