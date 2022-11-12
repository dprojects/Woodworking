import FreeCAD, FreeCADGui
import os, sys
from PySide import QtGui, QtCore

translate = FreeCAD.Qt.translate

# ###################################################################################################################
# globals
# ###################################################################################################################

gTests = dict()
gTestsStatus = ""

gWBData = dict()

gCertified = ""
gLatest = ""
gLastVersion = ""

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
	version = str(md.Version)

	# skip update from master branch for stable versions
	if gWBData["Version"] == version:
		if gWBData["Date"] == date:
			gLatest = True
		else:
			gLatest = False
	else:
		gLatest = True

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
	# test: QtWidgets
	# ######################################
	try:
		from PySide2 import QtWidgets
		gTests["QtWidgets"] = True
	except:
		gTests["QtWidgets"] = False
		gTestsStatus += "QtWidgets, "

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
	# test: zipfile
	# ######################################
	try:
		from zipfile import ZipFile
		gTests["zipfile"] = True
	except:
		gTests["zipfile"] = False
		gTestsStatus += "zipfile, "

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

	error = 1

	if error == 1 and gTests["qApp"] == True:
		try:
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
	
			error = 0
		except:
			error = 1

	if error == 1 and gTests["QtWidgets"] == True:
		try:
			from PySide2 import QtWidgets
			
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

			error = 0
		except:
			error = 1

	if error == 1:
		try:
			info = translate('debugInfo', 'This FreeCAD version is too buggy to get debug information.')
			QtGui.QApplication.clipboard().setText(info)

			error = 0
		except:
			error = 1

# ############################################################################
# main Qt screen
# ############################################################################

def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):
			
			global gLastVersion
			
			# ############################################################################
			# set screen
			# ############################################################################
			
			# tool screen size
			toolSW = 470
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
			gLastVersion = ""
			if gTests["package.xml"] == True and gTests["Version"] == True and gTests["Date"] == True:
				if gTests["urllib.request"] == True and gTests["tempfile"] == True:
					gLastVersion = getLastVersion()

			# worm status
			if gLatest == True and gTestsStatus == "" and gCertified == True:
				info += getIcon("worm_unhappy", 200, "right")
			elif gLatest != True and gTestsStatus != "" and gCertified != True:
				info += getIcon("worm_happy", 200, "right")
			else:
				info += getIcon("worm_undecided", 200, "right")

			# actual version
			if gLastVersion != "":

				if gLatest == True:
					info += getIcon("yes", iconSize, iconAlign)
					info += translate('debugInfo', 'Your Woodworking workbench version')
					info += " " + gLastVersion + " "
					info += translate('debugInfo', 'is ')
					info += "<br>"
					info += translate('debugInfo', 'up-to-date.')
				else:
					master = "https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip"
					info += getIcon("no", iconSize, iconAlign)
					info += translate('debugInfo', 'Update is available for this workbench')
					info += ": " + '<a href="' + master + '">' + gLastVersion + '</a>'
			
				info += "<br><br><br><br>"
			
			# tests
			if gTestsStatus == "":
				info += getIcon("yes", iconSize, iconAlign)
				info += translate('debugInfo', 'All tests passed. This FreeCAD version is safe to use.')
			else:
				info += getIcon("no", iconSize, iconAlign)
				info += translate('debugInfo', 'This FreeCAD version might not work correctly.')
				info += translate('debugInfo', 'Tests failed: ')
				info += gTestsStatus + ". "
			
			info += "<br><br><br><br><br>"
			
			# workbench certification
			if gCertified == True:
				info += getIcon("yes", iconSize, iconAlign)
				info += translate('debugInfo', 'You are using certified version. Thanks.')
			else:
				info += getIcon("no", iconSize, iconAlign)
				info += translate('debugInfo', 'Your FreeCAD version not match the Woodworking workbench version. ')
			
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

			# update button - after info, to not hide by text
			self.ub1 = QtGui.QPushButton(translate('debugInfo', 'update workbench \n and restart FreeCAD'), self)
			self.ub1.clicked.connect(self.wbUpdate)
			bW = 160
			bH = 40
			self.ub1.setFixedWidth(bW)
			self.ub1.setFixedHeight(bH)
			self.ub1.move(toolSW-10-bW, toolSH-10-bH)
			if gLastVersion != "" and gLatest == True:
				self.ub1.hide()
			else:
				self.ub1.show()

			# ############################################################################
			# show
			# ############################################################################

			self.show()

		# ############################################################################
		# actions - internal functions
		# ############################################################################

		def wbUpdateTask(self):
			
			# #########################
			# download zip file
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Downloading latest update...')
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			from zipfile import ZipFile
			import urllib.request
			import tempfile, os

			pathRoot = str(FreeCAD.ConfigDump()["UserAppData"])
			pathMod = str(os.path.join(pathRoot, "Mod"))
			pathWB = FreeCADGui.activeWorkbench().path
			
			url = "https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip"
			master = urllib.request.urlopen(url)

			zipPattern = "Woodworking" + " " + str(gLastVersion)
			zipFileName = zipPattern + ".zip"
			zipFilePath = os.path.join(pathMod, zipFileName)

			out = open(str(zipFilePath), "wb")
			out.write(master.read())
			out.close()
			
			# #########################
			# extract zip file
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Extracting latest update...')
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			with ZipFile(zipFilePath, 'r') as ex:
				ex.extractall(path=pathMod)
				ex.close()

			# #########################
			# rename extracted folder
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Renaming extracted folder...')
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			oldDir = os.path.join(pathMod, "Woodworking-master")
			newDir = os.path.join(pathMod, zipPattern)
			os.rename(oldDir, newDir)
			
			# #########################
			# prevent loading old workbench
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Disable old workbech...')
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			disableFile = os.path.join(pathWB, "ADDON_DISABLED")
			disable = open(str(disableFile), "w")
			disable.write("disabled")
			disable.close()
			
			# #########################
			# remove zip file
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Clean...')
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			os.remove(zipFilePath)
			
			# #########################
			# restart FreeCAD
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Restarting FreeCAD...')
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			import PySide2 
			from PySide2 import QtWidgets, QtCore, QtGui
			
			args = QtWidgets.QApplication.arguments()[1:]
			if FreeCADGui.getMainWindow().close():
				QtCore.QProcess.startDetached(
					QtWidgets.QApplication.applicationFilePath(), args
				)

		def wbUpdate(self):
			
			self.ub1.setDisabled(True)
			
			info = ""
			info += translate('debugInfo', 'Latest update for Woodworking workbench will be downloaded. ')
			info += translate('debugInfo', 'FreeCAD will restart with new Woodworking workbench version ')
			info += translate('debugInfo', 'but old version will be stored and disabled. ')
			info += "\n\n"
			
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			self.wbUpdateTask()

	# ############################################################################
	# final settings
	# ############################################################################

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
