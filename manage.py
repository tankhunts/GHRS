import sys
from PyQt5.QtWidgets import (QComboBox, QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea, QTextEdit, QDoubleSpinBox)
from PyQt5.QtCore import *
import pymongo
from bson.objectid import ObjectId


class Manage(QWidget):

    search_drug = QPushButton("Search for a drug")
    curr_label = QLabel("Current Perscriptions")
    curr_prescriptions = QTextEdit()

    select_box = QDoubleSpinBox()
    prescriptions = ''
    drug_search = pyqtSignal()
    go_back = pyqtSignal(str)

    currID = ''

    def search(self):
        self.drug_search.emit()

    def back(self):
        self.go_back.emit(self.currID)

    def setID(self, identifier):
        self.currID = identifier

    def toggleActive(self):
        idx = int(self.select_box.value() - 1)
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        idx_string = "Perscriptions.%d" % idx
        currRecord = mycol.find_one({'_id': ObjectId(self.currID)})
        status_update = ""
        if idx < 0 or idx > len(currRecord["Perscriptions"]) - 1:
            return
        currPrescrip = currRecord["Perscriptions"][idx]
        if currPrescrip["status"] == "ACTIVE":
            status_update = "INACTIVE" 
        elif currPrescrip["status"] == "INACTIVE":
            status_update = "ACTIVE" 

        
        mycol.update({'_id': ObjectId(self.currID)}, {'$set': { idx_string : {      "id"        : currPrescrip["id"], 
                                                                                    "strength"  : currPrescrip["strength"],
                                                                                    "color"     : currPrescrip["color"],
                                                                                    "shape"     : currPrescrip["shape"],
                                                                                    "imprint"   : currPrescrip["imprint"],
                                                                                    "status"    : status_update}}})

        self.showPrescriptions()

    def showPrescriptions(self):
        self.curr_prescriptions.clear()
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        currRecord = mycol.find_one({'_id': ObjectId(self.currID)})
        
        if "Perscriptions" in currRecord:
            for idx, p in enumerate(currRecord["Perscriptions"]):
                self.curr_prescriptions.append(str(idx + 1) + ". " + "    Id:      "   + p["id"]
                                        + "    Name:    "   + p["strength"] 
                                        + "    Color:   "   + p["color"]
                                        + "    Shape:   "   + p["shape"]
                                        + "    Imprint: "   + p["imprint"]
                                        + "    Status:  "   + p["status"]) 
                self.curr_prescriptions.append("\n")
    
        
    def __init__(self):
        super(Manage, self).__init__()

        search_drug = QPushButton("Search for a drug")
        curr_label = QLabel("Current Perscriptions")
        select_label = QLabel("Selected Drug: ")
        remove_button = QPushButton("Remove")
        back_button = QPushButton("Back")
        active_button = QPushButton("Toggle Active")
        search_drug.clicked.connect(self.search)
        back_button.clicked.connect(self.back)
        active_button.clicked.connect(self.toggleActive)

        self.select_box.setValue(1)
        self.select_box.setDecimals(0)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(select_label)
        bottomLayout.addWidget(self.select_box)
        bottomLayout.addWidget(active_button)
        bottomLayout.addWidget(remove_button)

        overallLayout = QVBoxLayout()
        overallLayout.addWidget(search_drug)
        overallLayout.addWidget(curr_label)
        overallLayout.addWidget(self.curr_prescriptions)
        overallLayout.addLayout(bottomLayout)
        overallLayout.addWidget(back_button)
        self.setLayout(overallLayout)


        
        


