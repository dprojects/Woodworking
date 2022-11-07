import FreeCAD, FreeCADGui
import os, sys
from PySide import QtGui, QtCore
from PySide2 import QtWidgets

translate = FreeCAD.Qt.translate

# ###################################################################################################################
# globals
# ###################################################################################################################

gTests = dict()
gWBData = dict()

# ###################################################################################################################
# tests
# ###################################################################################################################

def runTests():
	
	try:
		test = QtGui.qApp
		gTests["qApp"] = True
	except:
		gTests["qApp"] = False

	status = WorkbenchVersionVerify()
	if status == "yes":
		gTests["certified"] = True
	else:
		gTests["certified"] = False

# ###################################################################################################################
# workbench verification
# ###################################################################################################################

def setWBData():
	
	wb = FreeCADGui.activeWorkbench()
	package = os.path.join(wb.path, "package.xml")
	md = FreeCAD.Metadata(package)
	
	try:
		gWBData["Name"] = str(md.Name) + " workbench"
		gWBData["Description"] = str(md.Description)
		gWBData["Author"] = str(md.Author)
		gWBData["Maintainer"] = str(md.Maintainer)
		gWBData["Date"] = str(md.Date)
		gWBData["InfoStatus"] = True
	except:
		gWBData["InfoStatus"] = False
		
	gWBData["Version"] = str(md.Version)
	
def WorkbenchVersionVerify():

	fVersion = ""
	fVersion += str(FreeCAD.ConfigDump()["ExeVersion"]) + "."
	fVersion += str(FreeCAD.ConfigDump()["BuildRevision"]).split(" ")[0]
	
	if gWBData["Version"] == fVersion:
		return "yes"
	else:
		return "no"

def getIcon(iType, iSize, iAlign):
	
	path = FreeCADGui.activeWorkbench().path
	iconPath = str(os.path.join(path, "Icons"))
	
	filename = ""
	icon = ""
	
	f = os.path.join(iconPath, iType+".png")
	if os.path.exists(f):
		filename = f
		icon += '<img src="'+ filename + '" width="'+str(iSize)+'" height="'+str(iSize)+'" align="'+iAlign+'">'
	
	return icon

# ###################################################################################################################
# debug info
#
# This part of code has been created using forum code samples:
# https://forum.freecadweb.org/viewtopic.php?p=187448#p187448
# ###################################################################################################################

def getDebugInfo():

	if gTests["qApp"] == True:
		
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

		ai = AboutInfo()
		QtGui.qApp.installEventFilter(ai)
		FreeCADGui.runCommand("Std_About")
		QtGui.qApp.removeEventFilter(ai)
	
	else:
		
		class AboutInfo(QtCore.QObject):
			def eventFilter(self, obj, ev):
				if obj.metaObject().className() == 'Gui::Dialog::AboutDialog':
					if ev.type() == ev.ChildPolished:
						if hasattr(obj, 'on_copyButton_clicked'):
							QtWidgets.QApplication.instance().removeEventFilter(self)
							obj.on_copyButton_clicked()
							QtCore.QMetaObject.invokeMethod(obj, 'reject', QtCore.Qt.QueuedConnection)
				return False
                
		ai = AboutInfo()
		QtWidgets.QApplication.instance().installEventFilter(ai)
		FreeCADGui.runCommand('Std_About')
		del ai

# ############################################################################
# main Qt screen
# ############################################################################

def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):
			
			# ############################################################################
			# set screen
			# ############################################################################
			
			# tool screen size
			toolSW = 410
			toolSH = 540
			
			# active screen size - FreeCAD main window
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = int( ( gSW - toolSW ) / 2 )
			gPH = int( ( gSH - toolSH ) / 2 )

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('debugInfo', 'debugInfo'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# validation
			# ############################################################################

			row = 10

			info = ""
			
			if not False in gTests.values():
				info += getIcon("yes", 200, "right")
			elif not True in gTests.values():
				info += getIcon("no", 200, "right")
			else:
				info += getIcon("unknown", 200, "right")
			
			
			# workbench package informations
			
			if gWBData["InfoStatus"] == True:
				info += "<b>" + gWBData["Name"] + "</b>" + "<br>"
				info += "<b>" + gWBData["Date"] + "</b>" + "<br>"
				info += "<br><br>"
			
			# tests
			
			iconSize = 30
			iconAlign = "left"
			
			# qApp
			
			if gTests["qApp"] == True:
				info += getIcon("yes", iconSize, iconAlign)
				info += translate('debugInfo', 'Test for qApp passed. This FreeCAD version is safe to use.')
			else:
				info += getIcon("no", iconSize, iconAlign)
				info += translate('debugInfo', 'Test for qApp failed. This FreeCAD version might be broken.')
			
			info += "<br><br>"
			
			# workbench certification
			
			if gTests["certified"] == True:
				info += getIcon("yes", iconSize, iconAlign)
				info += translate('debugInfo', 'You are using certified version. Thanks.')
			else:
				info += getIcon("no", iconSize, iconAlign)
				info += translate('debugInfo', 'Your FreeCAD version not match the Woodworking workbench version. ')
				info += translate('debugInfo', 'You are using this configuration on your own risk.')
			
			# show info
			
			self.ov = QtGui.QLabel(info, self)
			self.ov.setFixedWidth(toolSW - 20)
			self.ov.setFixedHeight(200)
			self.ov.setWordWrap(True)
			self.ov.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.ov.move(10, row)

			# ############################################################################
			# debug info
			# ############################################################################

			row = row + 230
			
			editSizeX = toolSW - 20
			editSizeY = 220
			self.odie = QtGui.QTextEdit(self)
			self.odie.setMinimumSize(editSizeX, editSizeY)
			self.odie.setMaximumSize(editSizeX, editSizeY)
			self.odie.move(10, row)
			
			#self.o.setPlainText(out)
			self.odie.paste()

			# ############################################################################
			# debug info - note
			# ############################################################################

			row = row + 180
			
			info = ""
			info += "<b>"
			info += translate('debugInfo', 'Note:')
			info += "</b>"
			info += "<br>"
			info += translate('debugInfo', 'CTRL-V - to paste it at your forum topic')
			info += "<br>"
			info += translate('debugInfo', 'CTRL-A, CTRL-C - to copy again')
			info += "<br><br><br>"

			self.odin = QtGui.QLabel(info, self)
			self.odin.setFixedWidth(toolSW - 20)
			self.odin.setFixedHeight(200)
			self.odin.setWordWrap(True)
			self.odin.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.odin.move(10, row)

			# ############################################################################
			# show
			# ############################################################################

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


setWBData()
runTests()
getDebugInfo()
showQtGUI()


# ###################################################################################################################
