import FreeCAD
import FreeCADGui as Gui

# ############################################################################
# This part of code has been created by Werner Mayer (wmayer) at forum:
# https://forum.freecadweb.org/viewtopic.php?p=187448#p187448
# ############################################################################

from PySide import QtCore
from PySide import QtGui

class AboutInfo(QtCore.QObject):
	def eventFilter(self, obj, ev):
		if obj.metaObject().className() == "Gui::Dialog::AboutDialog":
			if ev.type() == ev.ChildPolished:
				mo = obj.metaObject()
				index = mo.indexOfMethod("on_copyButton_clicked()")
				if index > 0:
					mo.invokeMethod(obj, "on_copyButton_clicked")
					QtGui.qApp.postEvent(obj, QtGui.QCloseEvent())
    
		return False

ai=AboutInfo()
QtGui.qApp.installEventFilter(ai)
Gui.runCommand("Std_About")
QtGui.qApp.removeEventFilter(ai)

# ############################################################################
# by dprojects below:
# ############################################################################

def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):

			# main window
			self.result = userCancelled
			self.setGeometry(450, 100, 410, 500)
			self.setWindowTitle("Platform details for bug report")
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# output
			Info = ""
			Info += "Has been copied to clipboard: \n"
			
			self.oInfo1 = QtGui.QLabel(Info, self)
			self.oInfo1.move(5, 10)
			
			self.o = QtGui.QTextEdit(self)
			self.o.setMinimumSize(400, 350)
			self.o.setMaximumSize(400, 350)
			self.o.move(5, 40)
			
			self.o.setPlainText("")
			self.o.paste()

			Info = ""
			Info += "Note: \n\n"
			Info += "CTRL-V - to paste it at your forum topic \n\n"
			Info += "CTRL-A, CTRL-C - to copy again"
			
			self.oInfo2 = QtGui.QLabel(Info, self)
			self.oInfo2.move(5, 400)

			# show
			self.show()
			
	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################

showQtGUI()
