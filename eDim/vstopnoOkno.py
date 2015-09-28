from PyQt4 import QtCore, QtGui, uic
import os
app = QtGui.QApplication([])
vstopno = uic.loadUi("design/main.ui")
main = uic.loadUi("design/uporabnik.ui")
vnos_kn = uic.loadUi("design/vnos_kn.ui")

os.startfile("D:/eDim/eDim/files/Program.pdf")

#vstopno.show()
app.exec_()
