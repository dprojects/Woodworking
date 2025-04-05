# ###################################################################################################################
# globals
# ###################################################################################################################

gMaster = "https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip"

gTests = dict()
gWBCurrent = dict()
gWBLatest = dict()

gJokeDates = [ "22-03", "01-04", "19-12", "24-12", "25-12", "26-12", "31-12", "01-01" ]
gCurrentDate = ""

# ###################################################################################################################
# tests
# ###################################################################################################################

def setTests():
	
	gTests["status"] = ""
	
	# ######################################
	# test: FreeCAD
	# ######################################
	try:
		import FreeCAD
		gTests["FreeCAD"] = True
	except:
		gTests["FreeCAD"] = False
		gTests["status"] += "FreeCAD, "

	# ######################################
	# test: FreeCADGui
	# ######################################
	try:
		import FreeCADGui
		gTests["FreeCADGui"] = True
	except:
		gTests["FreeCADGui"] = False
		gTests["status"] += "FreeCADGui, "

	# ######################################
	# test: PySide
	# ######################################
	try:
		import PySide
		gTests["PySide"] = True
	except:
		gTests["PySide"] = False
		gTests["status"] += "PySide, "

	# ######################################
	# test: QtGui
	# ######################################
	try:
		from PySide import QtGui
		gTests["QtGui"] = True
	except:
		gTests["QtGui"] = False
		gTests["status"] += "QtGui, "

	# ######################################
	# test: QtCore
	# ######################################
	try:
		from PySide import QtCore
		gTests["QtCore"] = True
	except:
		gTests["QtCore"] = False
		gTests["status"] += "QtCore, "

	# ######################################
	# test: QtWidgets
	# ######################################
	try:
		from PySide import QtWidgets
		gTests["QtWidgets"] = True
	except:
		gTests["QtWidgets"] = False
		gTests["status"] += "QtWidgets, "

	# ######################################
	# test: translate
	# ######################################
	try:
		translate = FreeCAD.Qt.translate
		gTests["translate"] = True
	except:
		gTests["translate"] = False
		gTests["status"] += "translate, "

	# ######################################
	# test: os, sys
	# ######################################
	try:
		import os, sys
		gTests["os, sys"] = True
	except:
		gTests["os, sys"] = False
		gTests["status"] += "os, sys, "

	# ######################################
	# test: urllib.request
	# ######################################
	try:
		import urllib.request
		gTests["urllib.request"] = True
	except:
		gTests["urllib.request"] = False
		gTests["status"] += "urllib.request, "

	# ######################################
	# test: datetime
	# ######################################
	try:
		from datetime import datetime
		gCurrentDate = datetime.today().strftime("%d-%m")

		gTests["datetime"] = True
	except:
		gTests["datetime"] = False
		gTests["status"] += "datetime, "

	# ######################################
	# test: tempfile
	# ######################################
	try:
		import tempfile
		gTests["tempfile"] = True
	except:
		gTests["tempfile"] = False
		gTests["status"] += "tempfile, "

	# ######################################
	# test: zipfile
	# ######################################
	try:
		from zipfile import ZipFile
		gTests["zipfile"] = True
	except:
		gTests["zipfile"] = False
		gTests["status"] += "zipfile, "

	# ######################################
	# test: RegularPolygon
	# ######################################
	try:
		import ProfileLib.RegularPolygon
		gTests["RegularPolygon"] = True
	except:
		gTests["RegularPolygon"] = False
		gTests["status"] += "ProfileLib.RegularPolygon, "

	# ######################################
	# test: getCornerCrossSize
	# ######################################
	try:
		test1 = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
		gTests["getCornerCrossSize"] = True
	except:
		gTests["getCornerCrossSize"] = False
		gTests["status"] += "getCornerCrossSize, "

	# ######################################
	# test: hasAxisCross
	# ######################################
	try:
		test1 = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()
		gTests["hasAxisCross"] = True
	except:
		gTests["hasAxisCross"] = False
		gTests["status"] += "hasAxisCross, "

	# ######################################
	# test: qApp
	# ######################################
	try:
		test = QtGui.qApp
		gTests["qApp"] = True
	except:
		gTests["qApp"] = False
	#	gTests["status"] += "qApp, "

	# ######################################
	# end cut
	# ######################################
	
	if gTests["status"] != "":
		gTests["status"] = gTests["status"][:-2]

# ###################################################################################################################
# set latest workbench database
# ###################################################################################################################

def setWBLatest():
	
	try:
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
		gWBLatest["Date"] = str(md.Date)
		gWBLatest["Version"] = str(md.Version)

	except:
		skip = 1

# ###################################################################################################################
# set current workbench database
# ###################################################################################################################

def setWBCurrent():

	try:
		wb = FreeCADGui.activeWorkbench()
		package = os.path.join(wb.path, "package.xml")
		md = FreeCAD.Metadata(package)
	except:
		return
	
	try:
		gWBCurrent["Name"] = str(md.Name)
	except:
		skip = 1

	try:
		gWBCurrent["Description"] = str(md.Description)
	except:
		skip = 1

	try:
		gWBCurrent["Author"] = str(md.Author)
	except:
		skip = 1

	try:
		gWBCurrent["Maintainer"] = str(md.Maintainer)
	except:
		skip = 1

	try:
		gWBCurrent["Urls"] = str(md.Urls)
	except:
		skip = 1

	try:
		gWBCurrent["Version"] = str(md.Version)
	except:
		skip = 1

	try:
		gWBCurrent["DedicatedFreeCAD"] = ".".join(str(md.Version).split(".")[:-3])
	except:
		skip = 1

	try:
		gWBCurrent["Release"] = ".".join(str(md.Version).split(".")[-3:-1])
	except:
		skip = 1

	try:
		gWBCurrent["ReleaseState"] = ".".join(str(md.Version).split(".")[-1:])
	except:
		skip = 1

	try:
		gWBCurrent["Date"] = str(md.Date)
	except:
		skip = 1

# ###################################################################################################################
def setFreeCADVersion():

	try:
		v = str(FreeCAD.ConfigDump()["ExeVersion"]) + "."
		v += str(FreeCAD.ConfigDump()["BuildRevision"]).split(" ")[0]
		gWBCurrent["FreeCADVersion"] = v
	except:
		skip = 1

# ###################################################################################################################
def setCertified():

	try:
		if gWBCurrent["DedicatedFreeCAD"] == gWBCurrent["FreeCADVersion"]:
			gWBCurrent["Certified"] = "yes"
		else:
			gWBCurrent["Certified"] = "no"
	except:
		skip = 1

# ###################################################################################################################
def setUpToDate():
	
	try:
		gWBCurrent["up-to-date"] = ""
		gWBCurrent["update"] = ""

		# update the same version branch
		if gWBCurrent["Version"] == gWBLatest["Version"]:
			
			if gWBCurrent["Date"] == gWBLatest["Date"]:
				gWBCurrent["up-to-date"] = "yes"
				gWBCurrent["update"] = "no-update"
				gWBCurrent["info"] = "1"
			else:
				gWBCurrent["up-to-date"] = "no"
				gWBCurrent["update"] = "update"
				gWBCurrent["info"] = "2"

		# change version branch, upgrade to the latest master branch
		else:
			
			if gWBCurrent["Certified"] == "yes":
				gWBCurrent["up-to-date"] = "yes"
				gWBCurrent["update"] = "upgrade"
				gWBCurrent["info"] = "3"
			else:
				gWBCurrent["up-to-date"] = "no"
				gWBCurrent["update"] = "upgrade"
				gWBCurrent["info"] = "4"
	except:
		skip = 1

# ###################################################################################################################
# debug info
#
# This part of code has been created using forum code samples:
# https://forum.freecadweb.org/viewtopic.php?p=187448#p187448
# ###################################################################################################################

def getDebugInfo():

	getDebug = True

	if getDebug == True and gTests["qApp"] == True:
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
	
			getDebug = False
		except:
			getDebug = True

	if getDebug == True and gTests["QtWidgets"] == True:
		try:
			from PySide import QtWidgets

			class AboutInfo(QtCore.QObject):
				def eventFilter(self, obj, ev):
					if obj.metaObject().className() == 'Gui::Dialog::AboutDialog':
						
						if ev.type() == ev.Type.ChildPolished:
							copyBut = obj.findChild(QtWidgets.QPushButton, 'copyButton')
							if copyBut:
								QtWidgets.QApplication.instance().removeEventFilter(self)
								copyBut.click()
								QtCore.QMetaObject.invokeMethod(obj, 'reject', QtCore.Qt.QueuedConnection)

					return False
          
			ai = AboutInfo()
			QtWidgets.QApplication.instance().installEventFilter(ai)
			FreeCADGui.runCommand('Std_About')
			del ai

			getDebug = False
		except:
			getDebug = True

	if getDebug == True:
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
			
			# ############################################################################
			# set screen
			# ############################################################################
			
			# tool screen size
			toolSW = 470
			toolSH = 630
			
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
			# release info
			# ############################################################################
			
			row = 10
			iconSize = 10
			iconAlign = "left"
			info = ""
			
			# set info
			
			info += "<div style='margin-bottom:10px;'>"
			
			info += "<span style='font-size:20px;font-weight:bold;'>"
			info += translate('debugInfo', 'Woodworking') + ": "
			info += gWBCurrent["Release"] + " "
			info += "</span>"
			
			info += "<span style='font-size:20px;'>"
			if gWBCurrent["ReleaseState"] == "0":
				info += "(release)"
			else:
				info += "(development)"
			info += "</span>"
			
			info += "</div>"
			
			info += "<div>"
			info += translate('debugInfo', 'Woodworking workbench version ')
			info += gWBCurrent["Release"] + " "
			if gWBCurrent["ReleaseState"] == "0":
				info += "(release)"
			else:
				info += "(development)"
			info += "</div>"
			info += "<div>"
			info += translate('debugInfo', 'dedicated for FreeCAD version ')
			info += gWBCurrent["DedicatedFreeCAD"]
			info += "</div>"
			
			# show info
			self.ori = QtGui.QLabel(info, self)
			self.ori.setFixedWidth(toolSW - 20)
			self.ori.setWordWrap(False)
			self.ori.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.ori.setOpenExternalLinks(True)
			self.ori.move(10, row)
			
			# ############################################################################
			# validation status
			# ############################################################################
			
			row = 100
			iconSize = 40
			iconAlign = "left"
			info = ""
			
			# overall icon
			try:
				if gWBCurrent["up-to-date"] == "yes" and gTests["status"] == "" and gWBCurrent["Certified"] == "yes":
					if gCurrentDate in gJokeDates:
						info += self.getIcon("worm_unhappy", 200, "right")
					else:
						info += self.getIcon("yes", 200, "right")
				
				elif gWBCurrent["up-to-date"] == "no" and gTests["status"] != "" and gWBCurrent["Certified"] == "no":
					if gCurrentDate in gJokeDates:
						info += self.getIcon("worm_happy", 200, "right")
					else:
						info += self.getIcon("no", 200, "right")
				
				else:
					if gCurrentDate in gJokeDates:
						info += self.getIcon("worm_undecided", 200, "right")
					else:
						info += self.getIcon("unknown", 200, "right")
			except:
				
				if gCurrentDate in gJokeDates:
					info += self.getIcon("worm_happy", 200, "right")
				else:
					info += self.getIcon("no", 200, "right")
					
			# up-to-date status
			try:
				if gWBCurrent["info"] == "1":
					
					info += self.getIcon("yes", iconSize, iconAlign)
					info += translate('debugInfo', 'Your workbench is up-to-date. ')
					info += "<br><br><br><br>"
					
				if gWBCurrent["info"] == "2":
					
					info += self.getIcon("no", iconSize, iconAlign)
					
					info += translate('debugInfo', 'New update for your workbench')
					info += ": " + '<a href="' + gMaster + '">' + gWBLatest["Date"] + '.</a>'
					info += "<br><br><br><br>"
					
				if gWBCurrent["info"] == "3":
					
					info += self.getIcon("yes", iconSize, iconAlign)
					
					info += translate('debugInfo', 'Consider upgrade workbench to the new version branch')
					info += ": " + gWBLatest["Version"]
					info += ", " + '<a href="' + gMaster + '">' + gWBLatest["Date"] + '.</a>'
					info += "<br><br><br>"
					
				if gWBCurrent["info"] == "4":
					
					info += self.getIcon("no", iconSize, iconAlign)
					
					info += translate('debugInfo', 'Consider upgrade workbench to the new version branch')
					info += ": " + gWBLatest["Version"]
					info += ", " + '<a href="' + gMaster + '">' + gWBLatest["Date"] + '.</a>'
					info += "<br><br><br>"

			except:
				skip = 1
			
			# tests status
			try:
				if gTests["status"] == "":
					info += self.getIcon("yes", iconSize, iconAlign)
					info += translate('debugInfo', 'All tests passed. This FreeCAD version is safe to use.')
				else:
					info += self.getIcon("no", iconSize, iconAlign)
					info += translate('debugInfo', 'This FreeCAD version might not work correctly.')
					info += translate('debugInfo', 'Tests failed: ')
					info += gTests["status"] + ". "
			
				info += "<br><br><br><br><br>"
			except:
				skip = 1
			
			# workbench certification
			try:
				if gWBCurrent["Certified"] == "yes":
					info += self.getIcon("yes", iconSize, iconAlign)
					info += translate('debugInfo', 'You are using certified version. Thanks.')
				else:
					info += self.getIcon("no", iconSize, iconAlign)
					info += translate('debugInfo', 'Your FreeCAD version not match the Woodworking workbench version. ')
			except:
				skip = 1
				
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
			try:
				if gWBCurrent["update"] == "update":
					self.ub1 = QtGui.QPushButton(translate('debugInfo', 'update workbench \n and restart FreeCAD'), self)
				if gWBCurrent["update"] == "upgrade":
					self.ub1 = QtGui.QPushButton(translate('debugInfo', 'upgrade workbench \n and restart FreeCAD'), self)
				
				self.ub1.clicked.connect(self.wbUpdate)
				bW = 160
				bH = 40
				self.ub1.setFixedWidth(bW)
				self.ub1.setFixedHeight(bH)
				self.ub1.move(toolSW-10-bW, toolSH-10-bH)
			except:
				skip = 1

			# ############################################################################
			# show
			# ############################################################################

			self.show()

		# ############################################################################
		# actions - internal functions
		# ############################################################################

		def getIcon(self, iType, iSize, iAlign):
			
			path = FreeCADGui.activeWorkbench().path
			iconPath = str(os.path.join(path, "Icons"))
			
			filename = ""
			icon = ""
			
			f = os.path.join(iconPath, iType+".png")
			if os.path.exists(f):
				filename = f
				icon += '<img src="'+ filename + '" width="'+str(iSize)+'" height="'+str(iSize)+'" align="'+iAlign+'">'
			
			return icon

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
			
			url = gMaster
			master = urllib.request.urlopen(url)

			zipPattern = "Woodworking" + " " + gWBLatest["Date"]
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
			
			try:
				info = self.odie.toPlainText() + "\n"
				info += translate('debugInfo', 'Renaming extracted folder...')
				self.odie.setPlainText(info)
				self.odie.repaint()
				
				oldDir = os.path.join(pathMod, "Woodworking-master")
				newDir = os.path.join(pathMod, zipPattern)
				os.rename(oldDir, newDir)
			except:
				skip = 1

			# #########################
			# prevent loading old workbench
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Disable old workbench...')
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


setTests()

if (
	gTests["FreeCAD"] == True and
	gTests["FreeCADGui"] == True and
	gTests["PySide"] == True and
	gTests["QtGui"] == True and 
	gTests["os, sys"] == True
	):

	import FreeCAD, FreeCADGui, PySide
	from PySide import QtGui, QtCore, QtWidgets
	import os, sys
	
	if gTests["translate"] == True:
		translate = FreeCAD.Qt.translate

	setWBLatest()
	setWBCurrent()

	setFreeCADVersion()
	setCertified()
	setUpToDate()

	getDebugInfo()

	showQtGUI()
	
else:
	import FreeCAD
	
	if gTests["translate"] == True:
		translate = FreeCAD.Qt.translate
		info = translate('debugInfo', 'This FreeCAD version is too buggy to get debug information.') + "\n"
		info += translate('debugInfo', 'Errors:') + "\n"
		info += gTests["status"]
	else:
		info = "This FreeCAD version is too buggy to get debug information." + "\n"
		info += "Errors:" + "\n"
		info += gTests["status"]
		
	FreeCAD.Console.PrintMessage(info)
	

# ###################################################################################################################
