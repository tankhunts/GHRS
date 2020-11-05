import sys
import pymongo
from PyQt5.QtWidgets import (QWidget, QMainWindow, QStackedWidget, QApplication, QVBoxLayout)
app = QApplication(sys.argv)
from bson.objectid import ObjectId
from Searching import Searching
from viewer import ViewProfile
from menu import MainMenu
from searchNotes import searchNotes
from profileEditor import ProfileEditor

app.setStyle('Fusion')
class GHRS(QWidget):
    stacked = QStackedWidget()
    view = ViewProfile()
    edit = ProfileEditor()

    def goAdd(self):
        return
    def goSearch(self):
        self.stacked.setCurrentIndex(1)
    def goMenu(self):
        self.stacked.setCurrentIndex(0)
        self.resize(self.width(), 1000)
    def goView(self, identifier):
        self.view.currRecord = identifier
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        record = mycol.find_one({'_id': ObjectId(identifier)})
        self.view.name.setText(record['First Name'] + ' ' + record['Last Name'])
        self.view.DOB.setText(record["DOB"])
        self.view.race.setText(record["Race"])
        self.view.gender.setText(record["Gender"])
        self.view.blood.setText(record["Blood Type"])
        self.view.company.setText(record["Insurance"])
        self.view.ID.setText(record["ID"])
        self.view.conditions.setText(record["Conditions"])
        self.view.Perscriptions.setText(record["Perscriptions"])
        self.stacked.setCurrentIndex(2)
    def goNoteSearch(self):
        self.stacked.setCurrentIndex(3)
    def __init__(self):
        super(GHRS, self).__init__()
        search = Searching()
        menu = MainMenu()
        searchNote = searchNotes()
        self.stacked.addWidget(menu)
        self.stacked.addWidget(search)
        self.stacked.addWidget(self.view)
        self.stacked.addWidget(searchNote)
        menu.add.connect(self.goAdd)
        menu.search.connect(self.goSearch)
        search.ex.connect(self.goMenu) 
        search.op.connect(self.goView)
        self.view.ex.connect(self.goSearch)
        self.view.note.connect(self.goNoteSearch)
        searchNote.ex.connect(self.goView)
        
        self.view.sav.connect(self.edit.saveProfile)
        search.op.connect(self.view.setID)
    
        layout = QVBoxLayout()
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        self.stacked.setCurrentIndex(0)

        self.resize(1000,1000)
    
ghrs = GHRS()
ghrs.show()
app.exec_()