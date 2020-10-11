import sys
from PyQt5.QtWidgets import (QWidget, QMainWindow, QStackedWidget, QApplication, QVBoxLayout)
app = QApplication(sys.argv)
from Searching import Searching
from viewer import ViewProfile
from menu import MainMenu

class GHRS(QWidget):
    stacked = QStackedWidget()

    def goAdd(self):
        return
    def goSearch(self):
        self.stacked.setCurrentIndex(1)
    def goMenu(self):
        self.stacked.setCurrentIndex(0)
    def goView(self):
        self.stacked.setCurrentIndex(2)
    def __init__(self):
        super(GHRS, self).__init__()
        search = Searching()
        menu = MainMenu()
        view = ViewProfile()
        self.stacked.addWidget(menu)
        self.stacked.addWidget(search)
        self.stacked.addWidget(view)
        menu.add.connect(self.goAdd)
        menu.search.connect(self.goSearch)
        search.ex.connect(self.goMenu) 
        search.op.connect(self.goView)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        self.stacked.setCurrentIndex(0)
    
ghrs = GHRS()
ghrs.show()
app.exec_()