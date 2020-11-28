import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit, QDoubleSpinBox)
from PyQt5.QtCore import *
from drug_query import DrugQuery
import json
import pymongo
from bson.objectid import ObjectId

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
        if all(x == "" for x in query_res):
            self.results.append("ERROR: invalid query, please try again.")
            self.results.append("Serarch by name, color, shape, or id.")
        else:
            for idx, i in enumerate(query_res):
                if i == "":
                    continue
                json_dict = json.loads(i)
                self.results.append(str(idx + 1) + ". " + "    Id:      "   + json_dict["id"]
                                                        + "    Name:    "   + json_dict["spl_strength"] 
                                                        + "    Color:   "   + json_dict["splcolor_text"]
                                                        + "    Shape:   "   + json_dict["splshape_text"]
                                                        + "    Imprint: "   + json_dict["splimprint"]) 
                self.results.append("\n")
            self.query_res = query_res

    def setID(self, identifier):
        self.currID = identifier
        
    def back(self):
        self.go_back.emit(self.currID)
    
    def add(self):
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        i = int(self.res_num.value() - 1)
        if i < 0 or i > len(self.query_res) - 1:
            return
        json_dict = json.loads(self.query_res[i])
        mycol.update({'_id': ObjectId(self.currID)}, {"$push": { "Perscriptions": { "id"        : json_dict["id"], 
                                                                                    "strength"  : json_dict["spl_strength"],
                                                                                    "color"     : json_dict["splcolor_text"],
                                                                                    "shape"     : json_dict["splshape_text"],
                                                                                    "imprint"   : json_dict["splimprint"],
                                                                                    "status"    : "ACTIVE"}}})

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
        self.limit.setMaximum(20)
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
        add_button.clicked.connect(self.add)

        self.setLayout(overallLayout)

