import sys
import pymongo
from PyQt5.QtWidgets import (QWidget , QMainWindow, QStackedWidget, QApplication, QVBoxLayout, QGroupBox)
from PyQt5 import QtCore
from PyQt5.QtCore import (QDate)

app = QApplication(sys.argv)
from bson.objectid import ObjectId
from Searching import Searching
from viewer import ViewProfile
from menu import MainMenu
from searchNotes import searchNotes
from profileEditor import ProfileEditor
from viewnote import ViewNote
from Export import Export
from manage import Manage
from drug_search import DrugSearch
from Create_Profile import maker

app.setStyle('Fusion')
class GHRS(QWidget):
    stacked = QStackedWidget()
    view = ViewProfile()
    edit = ProfileEditor()
    searchNote = searchNotes()
    viewNote = ViewNote()
    export = Export()
    man = Manage()
    drugSearch = DrugSearch()
    addProf = maker()



    def goAdd(self):
        self.setWindowTitle("GHRS - RLA - Add Profile")
        self.stacked.setCurrentIndex(8)
    def goSearch(self):
        self.setWindowTitle("GHRS - RLA - Search Profile")
        self.stacked.setCurrentIndex(1)
    def goMenu(self):
        self.setWindowTitle("GHRS - RLA - Main Menu")
        self.stacked.setCurrentIndex(0)
        self.resize(self.width(), 1000)
    def goView(self, identifier):
        self.view.currRecord = identifier
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        record = mycol.find_one({'_id': ObjectId(identifier)})
        self.view.name.setText(record['First Name'] + ' ' + record['Last Name'])
        self.setWindowTitle("GHRS - RLA - Profile: " + record['First Name'] + ' ' + record['Last Name'])
        self.view.DOB.setDate(QDate.fromString(record["DOB"], "yyyy-MM-dd"))
        self.view.race.setCurrentIndex(self.view.race.findText(record["Race"]))
        self.view.gender.setText(record["Gender"])
        self.view.blood.setCurrentIndex(self.view.blood.findText(record["Blood Type"]))
        self.view.company.setText(record["Insurance"])
        self.view.ID.setText(record["ID"])
        self.view.conditions.setText(record["Conditions"])
        self.view.showPrescriptions()
        self.stacked.setCurrentIndex(2)
    def goNoteSearch(self, id):
        self.setWindowTitle("GHRS - RLA - Note Search: " + self.view.name.text())
        self.searchNote.currId = id
        self.stacked.setCurrentIndex(3)
    def returnView(self):
        self.setWindowTitle("GHRS - RLA - Profile: " + self.view.name.text())
        self.stacked.setCurrentIndex(2)
    def newNote(self, id):
        self.setWindowTitle("GHRS - RLA - New Note: " + self.view.name.text())
        self.viewNote.prof_id = id
        self.stacked.setCurrentIndex(4)
    def editNote(self, noteDict, id):
        self.viewNote.prof_id = id
        self.setWindowTitle("GHRS - RLA - Edit Note: " + self.view.name.text())
        self.searchNote.clear()
        self.viewNote.oldDict = noteDict
        self.viewNote.date = noteDict["Date"]
        self.viewNote.note.setText(noteDict["Note"])
        self.viewNote.subject.setText(noteDict["Subject"])
        self.stacked.setCurrentIndex(4)
    def goExport(self):
        self.setWindowTitle("GHRS - RLA - Export Data")
        self.stacked.setCurrentIndex(5)

    def goManage(self, identifier):
        self.setWindowTitle("GHRS - RLA - Manage Meds: " + self.view.name.text())
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["GHRS"]
        mycol = mydb["PatientData"]
        record = mycol.find_one({'_id': ObjectId(identifier)})
        #self.man.prescriptions = record["Perscriptions"]
        self.man.showPrescriptions()
        self.stacked.setCurrentIndex(6)
    def goDrugSearch(self):
        self.setWindowTitle("GHRS - RLA - Drug Search: " + self.view.name.text())
        self.stacked.setCurrentIndex(7)


    def __init__(self):
        super(GHRS, self).__init__()
        self.setWindowTitle("GHRS - RLA")
        search = Searching()
        menu = MainMenu()
        self.stacked.addWidget(menu)
        self.stacked.addWidget(search)
        self.stacked.addWidget(self.view)
        self.stacked.addWidget(self.searchNote)
        self.stacked.addWidget(self.viewNote)
        self.stacked.addWidget(self.export)
        self.stacked.addWidget(self.man)
        self.stacked.addWidget(self.drugSearch)
        self.stacked.addWidget(self.addProf)

        menu.add.connect(self.goAdd)
        menu.search.connect(self.goSearch)
        menu.export.connect(self.goExport)

        menu.search.connect(search.begin_search)

        search.ex.connect(self.goMenu) 
        search.op.connect(self.goView)
        self.view.ex.connect(self.goSearch)
        self.view.ex.connect(search.begin_search)

        self.addProf.ex.connect(self.goMenu)
        self.addProf.sav.connect(self.edit.addPatient)
        
        self.view.noteSearch.connect(self.goNoteSearch)
        self.view.noteSearch.connect(self.searchNote.begin_search)
        self.view.dele.connect(self.edit.deleteProfile)
        self.view.dele.connect(search.begin_search)
        self.searchNote.adding_note.connect(self.newNote)
        self.viewNote.ret.connect(self.goNoteSearch)
        self.viewNote.ret.connect(self.searchNote.begin_search)

        self.searchNote.ex.connect(self.returnView)
        #self.viewNote.ret.connect(self.returnView)
        self.searchNote.op.connect(self.editNote)
        self.view.sav.connect(self.edit.saveProfile)
        search.op.connect(self.view.setID)
        self.view.manage.connect(self.goManage)
        self.man.drug_search.connect(self.goDrugSearch)
        search.op.connect(self.man.setID)
        search.op.connect(self.drugSearch.setID)
        self.man.go_back.connect(self.goView)
        self.export.ex.connect(self.goMenu)
        self.drugSearch.go_back.connect(self.goManage)
        
        
        layout = QVBoxLayout()
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        self.stacked.setCurrentIndex(0)

        self.resize(1000,1000)
    
ghrs = GHRS()
ghrs.show()
app.exec_()