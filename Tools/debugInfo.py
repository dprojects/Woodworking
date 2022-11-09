import FreeCAD, FreeCADGui
import os, sys
from PySide import QtGui, QtCore
from PySide2 import QtWidgets

translate = FreeCAD.Qt.translate

# ###################################################################################################################
# globals
# ###################################################################################################################

gTests = dict()
gTestsStatus = ""

gWBData = dict()

gCertified = ""
gLatest = ""

# ###################################################################################################################
# workbench verification
# ###################################################################################################################

def wbVersionVerify():

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

def getLastVersion():
	
	global gLatest
	
	import urllib.request
	import tempfile
	import os
	
	# get latest package.xml
	url = "https://raw.githubusercontent.com/dprojects/Woodworking/master/package.xml"
	package = urllib.request.urlopen(url)

	# create temp directory
	tmpDir = tempfile.gettempdir()
	tmpDir = os.path.join(tmpDir, "FreeCAD_debug")
	if not os.path.exists(tmpDir):
		os.makedirs(tmpDir)

	# set tmp filename
	tmpFile = os.path.join(tmpDir, "package.xml.latest")
	out = open(str(tmpFile), "wb")
	out.write(package.read())
	out.close()

	# create Metadata and get Version
	md = FreeCAD.Metadata(tmpFile)
	date = str(md.Date)

	if gWBData["Date"] == date:
		gLatest = True
	else:
		gLatest = False

	return str(date)

# ###################################################################################################################
# tests
# ###################################################################################################################

def testCases():
	
	global gTestsStatus, gCertified
	
	# ######################################
	# test: qApp
	# ######################################
	try:
		test = QtGui.qApp
		gTests["qApp"] = True
	except:
		gTests["qApp"] = False
		gTestsStatus += "qApp, "

	# ######################################
	# test: urllib.request
	# ######################################
	try:
		import urllib.request
		gTests["urllib.request"] = True
	except:
		gTests["urllib.request"] = False
		gTestsStatus += "urllib.request, "
	
	# ######################################
	# test: tempfile
	# ######################################
	try:
		import tempfile
		gTests["tempfile"] = True
	except:
		gTests["tempfile"] = False
		gTestsStatus += "tempfile, "

	# ######################################
	# test: package.xml
	# ######################################
	try:
		wb = FreeCADGui.activeWorkbench()
		package = os.path.join(wb.path, "package.xml")
		md = FreeCAD.Metadata(package)
		gTests["package.xml"] = True
	except:
		gTests["package.xml"] = False
		gTestsStatus += "package.xml parse, "
	
	try:
		gWBData["Version"] = str(md.Version)
		gTests["Version"] = True
	except:
		gTests["Version"] = False
		gTestsStatus += "parse Version in package.xml, "

	try:
		gWBData["Date"] = str(md.Date)
		gTests["Date"] = True
	except:
		gTests["Date"] = False
		gTestsStatus += "parse Date in package.xml, "
	
	try:
		gWBData["Name"] = str(md.Name) + " workbench"
		gWBData["Description"] = str(md.Description)
		gWBData["Author"] = str(md.Author)
		gWBData["Maintainer"] = str(md.Maintainer)
		gWBData["Urls"] = str(md.Urls)
		gTests["data"] = True
	except:
		gTests["data"] = False
		gTestsStatus += "parse data in package.xml, "

	# ######################################
	# test: certified version
	# ######################################
	if gTests["Version"] == True:
		status = wbVersionVerify()
		if status == "yes":
			gCertified = True
		else:
			gCertified = False

	# end cut
	if gTestsStatus != "":
		gTestsStatus = gTestsStatus[:-2]

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
			toolSW = 450
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
			iconSize = 40
			iconAlign = "left"
			info = ""
			
			# set last version
			lastVersion = ""
			if gTests["package.xml"] == True and gTests["Version"] == True and gTests["Date"] == True:
				if gTests["urllib.request"] == True and gTests["tempfile"] == True:
					lastVersion = getLastVersion()

			# worm status
			if gLatest == True and gTestsStatus == "" and gCertified == True:
				info += getIcon("worm_unhappy", 200, "right")
			elif gLatest != True and gTestsStatus != "" and gCertified != True:
				info += getIcon("worm_happy", 200, "right")
			else:
				info += getIcon("worm_undecided", 200, "right")

			# actual version
			if lastVersion != "":

				if gLatest == True:
					info += getIcon("yes", iconSize, iconAlign)
					info += translate('debugInfo', 'Your Woodworking workbench version')
					info += " " + lastVersion + " "
					info += translate('debugInfo', 'is ')
					info += "<br>"
					info += translate('debugInfo', 'up-to-date.')
				else:
					master = "https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip"
					info += getIcon("no", iconSize, iconAlign)
					info += translate('debugInfo', 'There is new update for your Woodworking workbench')
					info += ": " + '<a href="' + master + '">' + lastVersion + '</a>'
			
				info += "<br><br>"
			
			# tests
			if gTestsStatus == "":
				info += getIcon("yes", iconSize, iconAlign)
				info += translate('debugInfo', 'All tests passed. This FreeCAD version is safe to use.')
			else:
				info += getIcon("no", iconSize, iconAlign)
				info += translate('debugInfo', 'This FreeCAD version might not work correctly.')
				info += translate('debugInfo', 'Tests failed: ')
				info += gTestsStatus + ". "
			
			info += "<br><br><br>"
			
			# workbench certification
			if gCertified == True:
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
			self.ov.setOpenExternalLinks(True)
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


testCases()
getDebugInfo()
showQtGUI()


# ###################################################################################################################
