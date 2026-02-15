# ###################################################################################################################
# globals
# ###################################################################################################################

gMaster = "https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip"

gTests = dict()
gUserVersion = dict()
gLatestVersion = dict()

gTestedKernels = [ 
	"0.21.2.33771",      # https://github.com/FreeCAD/FreeCAD/releases/tag/0.21.2
	"0.21.4.33929",       # https://codeberg.org/xCAD/FreeCAD21/releases/tag/0.21.4
	"1.0.1.39285",       # https://github.com/FreeCAD/FreeCAD/releases/tag/1.0.1
	"1.0.2.39319",       # https://github.com/FreeCAD/FreeCAD/releases/tag/1.0.2
	"1.1.0.20251104"     # https://github.com/FreeCAD/FreeCAD/releases/tag/weekly-2025.11.05 or magicCAD_2.0
]

gJokeDates = [ "22-03", "01-04", "19-12", "24-12", "25-12", "26-12", "31-12", "01-01" ]
gCurrentDate = ""

import MagicPanels

# ###################################################################################################################
# tests
# ###################################################################################################################

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
	# test: shutil
	# ######################################
	try:
		import shutil
		gTests["shutil"] = True
	except:
		gTests["shutil"] = False
		gTests["status"] += "shutil, "

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

# ###################################################################################################################
def setLatestVersion():
	
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
		xmlDate = str(md.Date)
		
		# testing purposes
		#xmlVersion = "2.0.20251120"
		#xmlDate = "2025-11-20"
		
		[ release, path, commit ] = xmlVersion.split(".")
		
		gLatestVersion["Version"] = xmlVersion
		gLatestVersion["Release"] = release
		gLatestVersion["Path"] = path
		gLatestVersion["Commit"] = commit
		gLatestVersion["Date"] = xmlDate
		
	except:
		skip = 1

# ###################################################################################################################
# set user workbench database
# ###################################################################################################################

# ###################################################################################################################
def setUserVersion():

	try:
		wb = FreeCADGui.activeWorkbench()
		package = os.path.join(wb.path, "package.xml")
		md = FreeCAD.Metadata(package)
		xmlVersion = str(md.Version)
		xmlDate = str(md.Date)
		[ release, path, commit ] = xmlVersion.split(".")
	except:
		return
	
	try:
		gUserVersion["Description"] = str(md.Description)
	except:
		skip = 1

	try:
		gUserVersion["Author"] = str(md.Author[0]["name"])
	except:
		skip = 1

	try:
		gUserVersion["AuthorURL"] = str(md.Urls[0]["location"])[8:]
	except:
		skip = 1
		
	try:
		gUserVersion["Version"] = xmlVersion
	except:
		skip = 1

	try:
		gUserVersion["Release"] = release
	except:
		skip = 1

	try:
		gUserVersion["Path"] = path
	except:
		skip = 1

	try:
		gUserVersion["Commit"] = commit
	except:
		skip = 1

	try:
		gUserVersion["Date"] = xmlDate
	except:
		skip = 1

# ###################################################################################################################
def setKernelVersion():

	try:
		v = str(FreeCAD.ConfigDump()["ExeVersion"]) + "."
		v += str(FreeCAD.ConfigDump()["BuildRevision"]).split(" ")[0]
		gUserVersion["kernelVersion"] = v
	except:
		skip = 1

# ###################################################################################################################
def setCertified():

	# certify supported kernels for backward compatibility
	try:
		if gUserVersion["kernelVersion"] in gTestedKernels:
			gUserVersion["Certified"] = "yes"
		else:
			gUserVersion["Certified"] = "no"
	except:
		skip = 1
	
# ###################################################################################################################
def setUpToDate():
	
	try:
		gUserVersion["up-to-date"] = ""

		if gUserVersion["Date"] == gLatestVersion["Date"]:
			gUserVersion["up-to-date"] = "yes"
		else:
			gUserVersion["up-to-date"] = "no"

	except:
		skip = 1

# ###################################################################################################################
# debug info
#
# This part of code has been created using forum code samples:
# https://forum.freecadweb.org/viewtopic.php?p=187448#p187448
# ###################################################################################################################

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

# ###################################################################################################################
def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):
			
			# ############################################################################
			# settings
			# ############################################################################
			
			toolSW = 1200                   # tool GUI width
			toolSH = 600                    # tool GUI height
			
			area = toolSW - 20              # GUI text area
			
			areaTW = 200                    # width of area for tests
			areaTH = 200                    # height of area for tests
			
			imageSize = 200                 # overall image width and height
			iconSize = 40                   # test status icon size
			iconAlign = "left"              # test status icon align
			
			oldWorkbenches = []             # disabled old workbenches to remove
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('debugInfo', 'debugInfo'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			
			self.setMinimumSize(toolSW, toolSH)
				
			# ############################################################################
			# header
			# ############################################################################
			
			icon = self.getIcon("Woodworking", imageSize, "left")
			self.oHeaderIcon = QtGui.QLabel(icon, self)
			self.oHeaderIcon.resize(imageSize, imageSize)
			self.oHeaderIcon.setWordWrap(False)
			self.oHeaderIcon.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.oHeaderIcon.setOpenExternalLinks(True)
			self.oHeaderIcon.setFixedWidth(imageSize)
			self.oHeaderIcon.setFixedHeight(imageSize)
			
			
			info = ""
			info += "<div style='font-size:30px;font-weight:bold;'>"
			info += translate('debugInfo', 'Woodworking') + " "
			info += gUserVersion["Release"] + "." + gUserVersion["Path"]
			info += "</div>"
			self.oHeaderName = QtGui.QLabel(info, self)
			self.oHeaderName.setWordWrap(False)
			self.oHeaderName.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.oHeaderName.setOpenExternalLinks(True)
		
			# ############################################################################
			# release info description
			# ############################################################################

			info = ""
			info += "<div style='margin:10px;font-size:12px;font-weight:normal;'>"
			info += gUserVersion["Description"]
			info += "</div>"
			self.oHeaderDescription = QtGui.QLabel(info, self)
			self.oHeaderDescription.setWordWrap(True)
			self.oHeaderDescription.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.oHeaderDescription.setOpenExternalLinks(True)
			
			info = ""
			info += "<div style='margin:10px;font-size:12px;font-weight:bold;text-align:right;'>"
			info += gUserVersion["Author"] + ", "
			info += '<a href=https://www.' + gUserVersion["AuthorURL"] + '>'
			info += gUserVersion["AuthorURL"] 
			info += '</a>'
			info += "</div>"
			self.oHeaderAuthor = QtGui.QLabel(info, self)
			self.oHeaderAuthor.setWordWrap(True)
			self.oHeaderAuthor.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.oHeaderAuthor.setOpenExternalLinks(True)
			
			# ############################################################################
			# overall validation status icon
			# ############################################################################
			
			info = ""
			
			# validation status icon
			try:
				if gUserVersion["up-to-date"] == "yes" and gTests["status"] == "" and gUserVersion["Certified"] == "yes":
					if gCurrentDate in gJokeDates:
						info += self.getIcon("worm_unhappy", imageSize, "right")
					else:
						info += self.getIcon("yes", imageSize, "right")
				
				elif gUserVersion["up-to-date"] == "no" and gTests["status"] != "" and gUserVersion["Certified"] == "no":
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
				if gUserVersion["up-to-date"] == "yes":
					
					infoI += self.getIcon("yes", iconSize, iconAlign)
					infoD += translate('debugInfo', 'Your workbench is up-to-date. ')
					
				if gUserVersion["up-to-date"] == "no":
					
					infoI += self.getIcon("no", iconSize, iconAlign)
					infoD += translate('debugInfo', 'New update for your workbench')
					infoD += ": " + '<a href="' + gMaster + '">' + gLatestVersion["Date"] + '.</a>'

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
					infoD += translate('debugInfo', 'This kernel passed all tests.')
				else:
					infoI += self.getIcon("no", iconSize, iconAlign)
					infoD += translate('debugInfo', 'This kernel version might not work correctly.')
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
				if gUserVersion["Certified"] == "yes":
					infoI += self.getIcon("yes", iconSize, iconAlign)
					infoD += translate('debugInfo', 'You are using tested kernel version. Thanks.')
				else:
					infoI += self.getIcon("no", iconSize, iconAlign)
					infoD += translate('debugInfo', 'Your kernel version is not tested.')
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
			self.odie.setFixedHeight(250)
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
			
			self.ub1 = QtGui.QPushButton(translate('debugInfo', 'update Woodworking workbench and restart'), self)
			self.ub1.setFixedHeight(40)
			self.ub1.clicked.connect(self.wbUpdate)
			self.ub1.hide()
			
			self.ub2 = QtGui.QPushButton(translate('debugInfo', 'show disabled workbenches'), self)
			self.ub2.setFixedHeight(40)
			self.ub2.clicked.connect(self.listOldWorkbenches)
			self.ub2.hide()
			
			self.ub3 = QtGui.QPushButton(translate('debugInfo', 'remove disabled workbenches'), self)
			self.ub3.setFixedHeight(40)
			self.ub3.clicked.connect(self.removeOldWorkbenches)
			self.ub3.hide()

			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.headerIcon = QtGui.QVBoxLayout()
			self.headerIcon.addWidget(self.oHeaderIcon)
			
			self.headerInfo1 = QtGui.QVBoxLayout()
			self.headerInfo1.addWidget(self.oHeaderName)
			
			self.headerInfo2 = QtGui.QVBoxLayout()
			self.headerInfo2.addWidget(self.oHeaderDescription)
			self.headerInfo2.addWidget(self.oHeaderAuthor)
			
			self.headerInfo = QtGui.QVBoxLayout()
			self.headerInfo.addLayout(self.headerInfo1)
			self.headerInfo.addLayout(self.headerInfo2)
			
			self.header = QtGui.QHBoxLayout()
			self.header.addLayout(self.headerIcon)
			self.header.addLayout(self.headerInfo)
			
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
			self.layFoot.addWidget(self.ub1)
			self.layFoot.addWidget(self.ub2)
			self.layFoot.addWidget(self.ub3)
			
			# set layout to main window
			self.layoutHeader = QtGui.QHBoxLayout()
			self.layoutHeader.addWidget(self.groupHeader)
			self.layoutHeader.addWidget(self.groupTests)
			
			self.layout = QtGui.QVBoxLayout()
			self.layout.addLayout(self.layoutHeader)
			self.layout.addStretch()
			self.layout.addLayout(self.layDebug)
			self.layout.addStretch()
			self.layout.addLayout(self.layFoot)
			self.setLayout(self.layout)

			if gUserVersion["up-to-date"] == "no":
				self.ub1.show()
			elif len(oldWorkbenches) == 0:
				self.ub2.show()
			else:
				self.ub3.show()
				
			# ############################################################################
			# show
			# ############################################################################

			# set theme
			MagicPanels.setTheme(self)
			
			self.ub2.setStyleSheet("background-color: green; color: black; font-weight: bold;")
			self.ub3.setStyleSheet("background-color: red; color: black; font-weight: bold;")
			
			self.show()

			MagicPanels.adjustGUI(self, "center")
	
		# ############################################################################
		# actions - internal functions
		# ############################################################################

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

		# ############################################################################
		def searchPathName(self, iPath):
		
			newPath = iPath
			
			i = 1
			while os.path.exists(newPath):
				newPath = iPath + " " + str(i)
				i += 1

			return newPath

		# ############################################################################
		def wbUpdateTask(self):
			
			from zipfile import ZipFile
			import urllib.request
			import tempfile, os
			
			pathRoot = str(FreeCAD.ConfigDump()["UserAppData"])
			pathMod = str(os.path.join(pathRoot, "Mod"))
			pathWB = FreeCADGui.activeWorkbench().path
			unzipPath = pathMod
			
			unzipDirName = "Woodworking-master"
			tmpFlag = False
			if os.path.exists(os.path.join(unzipPath, unzipDirName)):
				unzipPath = tempfile.mkdtemp(dir=pathMod)
				tmpFlag = True
			
			# #########################
			# download zip file
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Downloading latest update for Woodworking workbench from')
			info += ": " + str(gMaster) + " ..."
			self.odie.setPlainText(info)
			self.odie.repaint()

			try:
				zipFilePath = os.path.join(unzipPath, unzipDirName + ".zip")
				req = urllib.request.Request( gMaster, headers={'User-Agent': 'Mozilla/5.0'} )
				master = urllib.request.urlopen(req)
				out = open(str(zipFilePath), "wb")
				out.write(master.read())
				out.close()
				master.close()

			except Exception as e:
				info = self.odie.toPlainText() + "\n"
				info += translate('debugInfo', 'Download failed!')
				info += "\n"
				info += translate('debugInfo', 'Error: ')
				info += str(e)
				self.odie.setPlainText(info)
				return

			# #########################
			# extract zip file
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Unpacking Woodworking workbench to')
			info += ": " + str(unzipPath) + " ..."
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			with ZipFile(zipFilePath, 'r') as ex:
				ex.extractall(path=unzipPath)
				ex.close()

			# #########################
			# setting new folder
			# #########################
			
			oldPath = os.path.join(unzipPath, "Woodworking-master")
			
			newDirName = "Woodworking" + " " + gLatestVersion["Date"]
			if tmpFlag == False:
				newPath = os.path.join(unzipPath, newDirName)
				newPath = self.searchPathName(newPath)
			else:
				newPath = os.path.join(pathMod, newDirName)
				newPath = self.searchPathName(newPath)
				
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Setting new folder as:')
			info += ": " + str(newPath) + " ..."
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			if tmpFlag == False:
				os.rename(oldPath, newPath)
			else:
				import shutil
				shutil.move(oldPath, newPath)
			
			# #########################
			# disable old workbench
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Disable old Woodworking workbench')
			info += ": " + str(pathWB) + " ..."
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			try:
				disableFile = os.path.join(pathWB, "ADDON_DISABLED")
				disable = open(str(disableFile), "w")
				disable.write("disabled")
				disable.close()
			except:
				skip = 1
			
			# #########################
			# remove temporary files
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Cleaning temporary files')
			info += " ..."
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			if tmpFlag == False:
				os.remove(zipFilePath)
			else:
				if unzipPath != pathMod:
					shutil.rmtree(unzipPath)
			
			# #########################
			# restart FreeCAD
			# #########################
			
			info = self.odie.toPlainText() + "\n"
			info += translate('debugInfo', 'Restarting FreeCAD')
			info += " ..."
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			if FreeCAD.ActiveDocument != None:
				info = self.odie.toPlainText() + "\n"
				info += translate('debugInfo', 'Please save current ActiveDocument to continue')
				info += " ..."
				self.odie.setPlainText(info)
				self.odie.repaint()
			
			args = QtWidgets.QApplication.arguments()[1:]
			if FreeCADGui.getMainWindow().close():
				QtCore.QProcess.startDetached(
					QtWidgets.QApplication.applicationFilePath(), args
				)

		# ############################################################################
		def wbUpdate(self):
			
			self.ub1.setDisabled(True)
			
			info = ""
			info += translate('debugInfo', 'Latest update for Woodworking workbench will be downloaded. ')
			info += translate('debugInfo', 'FreeCAD will restart with new Woodworking workbench version ')
			info += "\n"
			info += translate('debugInfo', 'but old version will be stored and disabled. ')
			info += "\n\n"
			
			self.odie.setPlainText(info)
			self.odie.repaint()
			
			self.wbUpdateTask()

		# ############################################################################
		def listOldWorkbenches(self):
			
			import os
			
			pathRoot = str(FreeCAD.ConfigDump()["UserAppData"])
			pathMod = os.path.join(pathRoot, "Mod")
			self.oldWorkbenches = []
			
			info = "\n"
			info += translate('debugInfo', 'Woodworking workbench folders to remove')
			info += ": \n" 
			self.odie.setPlainText(info)
			
			for folder in os.listdir(pathMod):
				fullPath = os.path.join(pathMod, folder)
				
				if os.path.isdir(fullPath):
					package = os.path.join(fullPath, "package.xml")
					disabled = os.path.join(fullPath, "ADDON_DISABLED")
					
					if os.path.exists(package) and os.path.exists(disabled):
						try:
							md = FreeCAD.Metadata(package)
							name = str(md.Name)
							if name == "Woodworking":
								self.oldWorkbenches.append(fullPath)
								info += "\n" + str(fullPath)
						except:
							continue
							
			if not self.oldWorkbenches:
				info += "\n" + translate('debugInfo', 'No old Woodworking workbench versions found.')
			else:
				self.ub2.hide()
				self.ub3.show()
		
			self.odie.setPlainText(info)
			self.odie.repaint()
			
		# ############################################################################
		def removeOldWorkbenches(self):
    
			import shutil
			
			info = "\n"
			
			if not self.oldWorkbenches:
				info += translate('debugInfo', 'Nothing to remove.')
				self.odie.setPlainText(info)
				self.ub2.show()
				self.ub3.hide()
				return

			for path in self.oldWorkbenches:
				try:
					shutil.rmtree(path)
					info += "\n" + translate('debugInfo', 'Removed')
					info += ": " + str(path)
				except Exception as e:
					info += "\n" + translate('debugInfo', 'Error removing')
					info += ": " + str(path)
					
			self.oldWorkbenches = []
			self.odie.setPlainText(info)
			self.odie.repaint()

			self.ub2.show()
			self.ub3.hide()

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

	setLatestVersion()
	setUserVersion()

	setKernelVersion()
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
