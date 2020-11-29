import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import importing
import pathlib

class MainMenu(QWidget):

    title = "Main Menu"
    name = "G.H.R.S"
    width = 1000
    height = 1000
    #main options layout
    mainWidget = QWidget()
    optionsLayout = QHBoxLayout()
    nameLabel = QLabel()
    mainLayout = QVBoxLayout(mainWidget)

    #main menu buttons
    addPatientButton = QPushButton('Add patient')
    searchButton = QPushButton('Search for a profile')
    exportButton = QPushButton("Export Data")
    importButton = QPushButton("Import Data")
    search = pyqtSignal()
    add = pyqtSignal()
    export = pyqtSignal()
    impor = pyqtSignal()

    new = QGroupBox("For new customers")
    returning = QGroupBox("For returning customers")
    exporting = QGroupBox("Shipping data off")
    importing = QGroupBox("Import data")

    def goAdd(self):
        self.add.emit()
    def goSearch(self):
        self.search.emit()
    def goExport(self):
        self.export.emit()
    def goImport(self):
        self.impor.emit()

    def getFile(self):
        print(pathlib.Path().absolute())
        fname = QFileDialog.getOpenFileName(self, 'Open file', str(pathlib.Path().absolute()), 'csv(*.csv)')
        importing.readFile(fname)
    def __init__(self, parent=None):
        super().__init__() 
        #creating window



        self.nameLabel.setText(self.name)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.setWindowTitle(self.title)
        #creating layout

        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QVBoxLayout()

        layout1.addWidget(self.addPatientButton)
        layout2.addWidget(self.searchButton)
        layout3.addWidget(self.exportButton)
        layout4.addWidget(self.importButton)




        self.new.setLayout(layout1)
        self.returning.setLayout(layout2)
        self.exporting.setLayout(layout3)
        self.importing.setLayout(layout4)
        self.mainLayout.addWidget(self.nameLabel)
        #self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.new)
        self.mainLayout.addWidget(self.returning)
        self.mainLayout.addWidget(self.exporting)
        self.mainLayout.addWidget(self.importing)
        #self.mainLayout.addStretch()
        self.setLayout(self.mainLayout)

        self.exportButton.clicked.connect(self.goExport)
        self.addPatientButton.clicked.connect(self.goAdd)
        self.searchButton.clicked.connect(self.goSearch) 
        self.importButton.clicked.connect(self.getFile)