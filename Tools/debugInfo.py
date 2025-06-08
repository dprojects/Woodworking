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
	# test: MagicPanels
	# ######################################
	try:
		import MagicPanels
		gTests["MagicPanels"] = True
	except:
		gTests["MagicPanels"] = False
		gTests["status"] += "MagicPanels, "
	
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
		xmlVersion = str(md.Version)
		
		versionWB = xmlVersion.split(".")[-6:]
		versionFC = xmlVersion.split(".")[:-6]
		
		gWBLatest["Version"] = xmlVersion
		gWBLatest["Release"] = str(versionWB[0]) + "." + str(versionWB[1])
		gWBLatest["Date"] = ".".join( versionWB[-3:] )
		
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
		versionWB = str(md.Version).split(".")[-6:]
		versionFC = str(md.Version).split(".")[:-6]
	except:
		skip = 1

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
		gWBCurrent["DedicatedFreeCAD"] = ".".join(versionFC)
	except:
		skip = 1

	try:
		gWBCurrent["Release"] = str(versionWB[0]) + "." + str(versionWB[1])
	except:
		skip = 1

	try:
		gWBCurrent["ReleaseState"] = str(versionWB[2])
	except:
		skip = 1

	try:
		gWBCurrent["Date"] = ".".join(versionWB[-3:])
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

		# version string is the same
		if gWBCurrent["Version"] == gWBLatest["Version"]:
			gWBCurrent["up-to-date"] = "yes"
			gWBCurrent["update"] = "no-update"
			gWBCurrent["info"] = "1"
		
		# version string is different
		else:
		
			# check date first
			if gWBCurrent["Date"] != gWBLatest["Date"]:
				gWBCurrent["up-to-date"] = "no"
				gWBCurrent["update"] = "update"
				gWBCurrent["info"] = "2"
			
			# same date
			else:
			
				# release not the same
				if gWBCurrent["Release"] != gWBLatest["Release"]:
					
					# stable version, consider upgrade to the latest master branch
					if gWBCurrent["ReleaseState"] == "0":
						gWBCurrent["up-to-date"] = "yes"
						gWBCurrent["update"] = "upgrade"
						gWBCurrent["info"] = "3"
						
					# development version, change version branch, upgrade to the latest master branch
					else:
						gWBCurrent["up-to-date"] = "no"
						gWBCurrent["update"] = "upgrade"
						gWBCurrent["info"] = "4"
					
				# change version branch, upgrade to the latest master branch
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
			# settings
			# ############################################################################
			
			toolSW = 550                    # tool GUI width
			toolSH = 690                    # tool GUI height
			
			area = toolSW - 20              # GUI text area
			
			areaTW = 200                    # width of area for tests
			areaTH = 200                    # height of area for tests
			
			imageSize = 200                 # overall image width and height
			iconSize = 40                   # test status icon size
			iconAlign = "left"              # test status icon align
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('debugInfo', 'debugInfo'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			self.setMinimumWidth(toolSW)
			self.setMinimumHeight(toolSH)
				
			# ############################################################################
			# release info header
			# ############################################################################
			
			info = ""
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

			self.orih = QtGui.QLabel(info, self)
			self.orih.setWordWrap(False)
			self.orih.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.orih.setOpenExternalLinks(True)

			# ############################################################################
			# release info description
			# ############################################################################

			info = ""
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
			
			self.orid = QtGui.QLabel(info, self)
			self.orid.setWordWrap(False)
			self.orid.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.orid.setOpenExternalLinks(True)
			
			# ############################################################################
			# overall validation status icon
			# ############################################################################
			
			info = ""
			
			# validation status icon
			try:
				if gWBCurrent["up-to-date"] == "yes" and gTests["status"] == "" and gWBCurrent["Certified"] == "yes":
					if gCurrentDate in gJokeDates:
						info += self.getIcon("worm_unhappy", imageSize, "right")
					else:
						info += self.getIcon("yes", imageSize, "right")
				
				elif gWBCurrent["up-to-date"] == "no" and gTests["status"] != "" and gWBCurrent["Certified"] == "no":
					if gCurrentDate in gJokeDates:
						info += self.getIcon("worm_happy", imageSize, "right")
					else:
						info += self.getIcon("no", imageSize, "right")
				
				else:
					if gCurrentDate in gJokeDates:
						info += self.getIcon("worm_undecided", imageSize, "right")
					else:
						info += self.getIcon("unknown", imageSize, "right")
			except:
				
				if gCurrentDate in gJokeDates:
					info += self.getIcon("worm_happy", imageSize, "right")
				else:
					info += self.getIcon("no", imageSize, "right")

			self.oovsi = QtGui.QLabel(info, self)
			self.oovsi.resize(imageSize, imageSize)
			self.oovsi.setWordWrap(False)
			self.oovsi.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.oovsi.setOpenExternalLinks(True)
			
			# ############################################################################
			# up-to-date status
			# ############################################################################

			infoI = ""
			infoD = ""

			try:
				if gWBCurrent["info"] == "1":
					
					infoI += self.getIcon("yes", iconSize, iconAlign)
					infoD += translate('debugInfo', 'Your workbench is up-to-date. ')
					
				if gWBCurrent["info"] == "2":
					
					infoI += self.getIcon("no", iconSize, iconAlign)
					infoD += translate('debugInfo', 'New update for your workbench')
					infoD += ": " + '<a href="' + gMaster + '">' + gWBLatest["Date"] + '.</a>'
					
				if gWBCurrent["info"] == "3":
					
					infoI += self.getIcon("yes", iconSize, iconAlign)
					infoD += translate('debugInfo', 'Consider upgrade workbench to the new version branch')
					infoD += ": " + gWBLatest["Version"]
					infoD += ", " + '<a href="' + gMaster + '">' + gWBLatest["Date"] + '.</a>'
					
				if gWBCurrent["info"] == "4":
					
					infoI += self.getIcon("no", iconSize, iconAlign)
					infoD += translate('debugInfo', 'Consider upgrade workbench to the new version branch')
					infoD += ": " + gWBLatest["Version"]
					infoD += ", " + '<a href="' + gMaster + '">' + gWBLatest["Date"] + '.</a>'

			except:
				skip = 1
			
			# icon
			self.outdsi = QtGui.QLabel(infoI, self)
			self.outdsi.setFixedWidth(iconSize)
			self.outdsi.setWordWrap(False)
			self.outdsi.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.outdsi.setOpenExternalLinks(True)
			
			# description
			self.outdsd = QtGui.QLabel(infoD, self)
			self.outdsd.resize(areaTW, areaTH)
			self.outdsd.setWordWrap(True)
			self.outdsd.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.outdsd.setOpenExternalLinks(True)

			# ############################################################################
			# tests status
			# ############################################################################

			infoI = ""
			infoD = ""

			try:
				if gTests["status"] == "":
					infoI += self.getIcon("yes", iconSize, iconAlign)
					infoD += translate('debugInfo', 'All tests passed. This FreeCAD version is safe to use.')
				else:
					infoI += self.getIcon("no", iconSize, iconAlign)
					infoD += translate('debugInfo', 'This FreeCAD version might not work correctly.')
					infoD += translate('debugInfo', 'Tests failed: ')
					infoD += gTests["status"] + ". "
			except:
				skip = 1
			
			# icon
			self.otsi = QtGui.QLabel(infoI, self)
			self.otsi.setFixedWidth(iconSize)
			self.otsi.setWordWrap(False)
			self.otsi.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.otsi.setOpenExternalLinks(True)
			
			# description
			self.otsd = QtGui.QLabel(infoD, self)
			self.otsd.resize(areaTW, areaTH)
			self.otsd.setWordWrap(True)
			self.otsd.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.otsd.setOpenExternalLinks(True)

			# ############################################################################
			# workbench certification
			# ############################################################################

			infoI = ""
			infoD = ""

			try:
				if gWBCurrent["Certified"] == "yes":
					infoI += self.getIcon("yes", iconSize, iconAlign)
					infoD += translate('debugInfo', 'You are using certified version. Thanks.')
				else:
					infoI += self.getIcon("no", iconSize, iconAlign)
					infoD += translate('debugInfo', 'Your FreeCAD version not match the Woodworking workbench version. ')
			except:
				skip = 1
				
			# icon
			self.owci = QtGui.QLabel(infoI, self)
			self.owci.setFixedWidth(iconSize)
			self.owci.setWordWrap(False)
			self.owci.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.owci.setOpenExternalLinks(True)
			
			# description
			self.owcd = QtGui.QLabel(infoD, self)
			self.owcd.resize(areaTW, areaTH)
			self.owcd.setWordWrap(True)
			self.owcd.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.owcd.setOpenExternalLinks(True)

			# ############################################################################
			# debug info
			# ############################################################################

			self.odie = QtGui.QTextEdit(self)
			self.odie.setFixedHeight(230)
			self.odie.paste()

			# ############################################################################
			# debug info - note
			# ############################################################################

			info = ""
			info += "<b>" + translate('debugInfo', 'Note:') + "</b>" + "<br>"
			info += translate('debugInfo', 'CTRL-V - to paste it at your forum topic') + "<br>"
			info += translate('debugInfo', 'CTRL-A, CTRL-C - to copy again')

			self.odin = QtGui.QLabel(info, self)
			self.odin.setWordWrap(False)
			self.odin.setTextFormat(QtCore.Qt.TextFormat.RichText)

			# ############################################################################
			# update button
			# ############################################################################
			
			try:
				if gWBCurrent["update"] == "update":
					self.ub1 = QtGui.QPushButton(translate('debugInfo', 'update workbench \n and restart FreeCAD'), self)
				if gWBCurrent["update"] == "upgrade":
					self.ub1 = QtGui.QPushButton(translate('debugInfo', 'upgrade workbench \n and restart FreeCAD'), self)
				
				self.ub1.clicked.connect(self.wbUpdate)
				
			except:
				self.ub1 = False

			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.header = QtGui.QVBoxLayout()
			self.header.addWidget(self.orih)
			self.header.addWidget(self.orid)
			self.groupHeader = QtGui.QGroupBox(None, self)
			self.groupHeader.setLayout(self.header)
			
			self.layState = QtGui.QGridLayout()
			self.layState.addWidget(self.outdsi, 0, 0)
			self.layState.addWidget(self.outdsd, 0, 1)
			self.layState.addWidget(self.otsi, 1, 0)
			self.layState.addWidget(self.otsd, 1, 1)
			self.layState.addWidget(self.owci, 2, 0)
			self.layState.addWidget(self.owcd, 2, 1)
			
			self.layImage = QtGui.QVBoxLayout()
			self.layImage.addWidget(self.oovsi)
			
			self.layTests = QtGui.QHBoxLayout()
			self.layTests.addLayout(self.layState)
			self.layTests.addLayout(self.layImage)
			self.groupTests = QtGui.QGroupBox(None, self)
			self.groupTests.setLayout(self.layTests)
			
			self.layDebug = QtGui.QVBoxLayout()
			self.layDebug.addWidget(self.odie)
			
			self.layFoot = QtGui.QHBoxLayout()
			self.layFoot.addWidget(self.odin)
			if self.ub1 != False:
				self.layFoot.addWidget(self.ub1)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			self.layout.addWidget(self.groupHeader)
			self.layout.addStretch()
			self.layout.addWidget(self.groupTests)
			self.layout.addStretch()
			self.layout.addLayout(self.layDebug)
			self.layout.addStretch()
			self.layout.addLayout(self.layFoot)
			self.setLayout(self.layout)

			# ############################################################################
			# show
			# ############################################################################

			self.show()

			# set window position
			sw = self.width()
			sh = self.height()
			pw = int( (FreeCADGui.getMainWindow().width() / 2) - ( sw / 2 ) )
			ph = int( FreeCADGui.getMainWindow().height() - sh )
			self.setGeometry(pw, ph, sw, sh)
			
			# set theme
			try:
				import MagicPanels
				QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
				self.setStyleSheet(QtCSS)
			except:
				skip = 1
			
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
