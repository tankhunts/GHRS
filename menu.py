import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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
    search = pyqtSignal()
    add = pyqtSignal()
    export = pyqtSignal()

    def goAdd(self):
        self.add.emit()
    def goSearch(self):
        self.search.emit()
    def goExport(self):
        self.export.emit()

    def __init__(self, parent=None):
        super().__init__() 
        #creating window

        self.nameLabel.setText(self.name)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.setWindowTitle(self.title)
        #creating layout
        self.optionsLayout.addWidget(self.addPatientButton)
        self.optionsLayout.addWidget(self.searchButton)
        self.mainLayout.addWidget(self.nameLabel)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.optionsLayout)
        self.mainLayout.addWidget(self.exportButton)
        self.mainLayout.addStretch()
        self.setLayout(self.mainLayout)

        self.exportButton.clicked.connect(self.goExport)
        self.addPatientButton.clicked.connect(self.goAdd)
        self.searchButton.clicked.connect(self.goSearch) 