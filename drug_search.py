import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit, QDoubleSpinBox)
from PyQt5.QtCore import *
from drug_query import DrugQuery
import json

class DrugSearch(QWidget):

    
    results = QTextEdit()
    query = QLineEdit()
    limit = QDoubleSpinBox()
    res_num = QDoubleSpinBox()
    dq = DrugQuery()

    currID = ''

    go_back = pyqtSignal(str)
    def start(self):
        self.results.clear()
        query_res = self.dq.query(self.query.text(), int(self.limit.value()))
    
        for idx, i in enumerate(query_res):
            json_dict = json.loads(i)
            self.results.append(str(idx + 1) + ". " + "    Id:      "   + json_dict["id"]
                                                    + "    Name:    "   + json_dict["spl_strength"] 
                                                    + "    Color:   "   + json_dict["splcolor_text"]
                                                    + "    Shape:   "   + json_dict["splshape_text"]
                                                    + "    Imprint: "   + json_dict["splimprint"]) 
            self.results.append("\n")

    def setID(self, identifier):
        self.currID = identifier
        
    def back(self):
        self.go_back.emit(self.currID)

    def __init__(self):
        super(DrugSearch, self).__init__()
        
        enter_label = QLabel("Enter Query:")
        res_label = QLabel("Results:")
        limit_label = QLabel("Limit:")
        choose_label = QLabel("Choose a result to add to patient profile:")

        overallLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        bottomLayout = QHBoxLayout()
        go_button = QPushButton("Go")
        add_button = QPushButton("Add")
        back_button = QPushButton("Back")
        self.limit.setValue(1)
        self.limit.setDecimals(0)
        self.res_num.setValue(1)
        self.res_num.setDecimals(0)

        
        topLayout.addWidget(enter_label)
        topLayout.addWidget(self.query)
        topLayout.addWidget(limit_label)
        topLayout.addWidget(self.limit)
        topLayout.addWidget(go_button)
        bottomLayout.addWidget(choose_label)
        bottomLayout.addWidget(self.res_num)
        bottomLayout.addWidget(add_button)
        overallLayout.addLayout(topLayout)
        overallLayout.addWidget(res_label)
        overallLayout.addWidget(self.results)
        overallLayout.addLayout(bottomLayout)
        overallLayout.addWidget(back_button)

        go_button.clicked.connect(self.start)
        back_button.clicked.connect(self.back)

        self.setLayout(overallLayout)

