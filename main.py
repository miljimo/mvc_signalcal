from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication , QMainWindow
import PyQt5.uic as UI

for proper in dir(UI):
    print(proper )

if __name__ =="__main__":
    app  = QApplication([])
    mainwindow  =  QMainWindow();
    mainwindow.setWindowFlags(Qt.Window | Qt.FramelessWindowHint);
    mainwindow.setAttribute(Qt.WA_TranslucentBackground, True);
    UI.loadUi("test.ui", mainwindow);
   
    mainwindow.show()
    app.exec_()
