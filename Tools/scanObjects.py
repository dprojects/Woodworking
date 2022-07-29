# ###################################################################################################################
'''

Inspection tool for FreeCAD macro development
Author: Darek L (github.com/dprojects)
Latest version: https://github.com/dprojects/scanObjects

Certified platform:

OS: Ubuntu 22.04 LTS (XFCE/xubuntu)
Word size of FreeCAD: 64-bit
Version: 0.20.29177 (Git) AppImage
Build type: Release
Branch: (HEAD detached at 0.20)
Hash: 68e337670e227889217652ddac593c93b5e8dc94
Python 3.9.13, Qt 5.12.9, Coin 4.0.0, Vtk 9.1.0, OCC 7.5.3
Locale: English/United States (en_US)
Installed mods: 
  * Woodworking 0.20.29177

https://github.com/dprojects/Woodworking

'''
# ###################################################################################################################


import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore


# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		

		# ############################################################################
		# database
		# ############################################################################


		# database for selection
		dbSO = [] # objects
		dbSL = [] # labels
		dbSI = -1 # index
		dbSP = [] # path
		dbSLI = [] # last index

		def clearDB(self):

			self.dbSO = [] # objects
			self.dbSL = [] # labels
			self.dbSI = -1 # index
			self.dbSP = [] # path
			self.dbSLI = [] # last index


		# ############################################################################
		# globals
		# ############################################################################


		gDefaultRoot = ""
		gModeType = "normal"

		# set display grid
		try:
			gW = FreeCADGui.getMainWindow().width()
			gH = FreeCADGui.getMainWindow().height()
	
			# avoid double click and FreeCAD close
			gW = gW - 20

		except:
			gW = 1300
			gH = 700

		gGridCol = int(gW / 5)
		gGridRow = int(gH / 5)


		# ############################################################################
		# errors & info
		# ############################################################################


		def showMsg(self, iMsg, iType = "error"):
		
			try:
				if iType == "info":	
					msg = ""
					msg += "INFO: "
					msg += " | "
					msg += str(iMsg)	
				else:	
					msg = ""
					msg += "ERROR: "
					msg += " | "
					msg += str(iMsg)

				self.o5.setPlainText(msg)
			except:
				self.o5.setPlainText("kernel panic or even FreeCAD panic :-)")


		# ############################################################################
		# init
		# ############################################################################


		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):


			# ############################################################################
			# defaults
			# ############################################################################


			try:
				test = FreeCAD.activeDocument().Objects
				self.gDefaultRoot = "project"
			except:
				self.gDefaultRoot = "FreeCAD"


			# ############################################################################
			# main window
			# ############################################################################
			

			self.result = userCancelled
			self.setGeometry(0, 0, self.gW, self.gH)
			self.setWindowTitle("scanObjects - inspection tool for macro development")
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


			# ############################################################################
			# options
			# ############################################################################


			# scan root
			# ############################################################################
			
			# label
			self.rootL = QtGui.QLabel("Select scan root path:", self)
			
			# options
			self.rootList = (
				"my project root",
				"Module: FreeCAD",
				"Module: QtGui", 
				"Module: QtCore",
				"Module: coin",
				"Module: Path", 
				"Module: Draft", 
				"Module: TechDraw", 
				"Module: Spreadsheet",
				"custom module",
				"custom command result"
			)

			self.rootO = QtGui.QComboBox(self)
			self.rootO.addItems(self.rootList)
			if self.gDefaultRoot == "project":
				self.rootO.setCurrentIndex(self.rootList.index("my project root"))
			else:
				self.rootO.setCurrentIndex(self.rootList.index("Module: FreeCAD"))
			self.rootO.activated[str].connect(self.setRootPath)
			self.rootO.setFixedWidth((1*self.gGridCol)-20)
			
			# custom module
			# ############################################################################

			# label
			self.rootCL = QtGui.QLabel("Custom module name:", self)
			
			# text input
			self.rootCO = QtGui.QLineEdit(self)
			self.rootCO.setText("")
			self.rootCO.setFixedWidth((1*self.gGridCol)-20)
			
			# button
			self.rootCLoad = QtGui.QPushButton("load custom module", self)
			self.rootCLoad.clicked.connect(self.loadCustomModule)
			self.rootCLoad.setFixedWidth((1*self.gGridCol)-20)
			
			# select windows layout
			# ############################################################################

			# label
			self.layL = QtGui.QLabel("Select windows layout:", self)
			
			# options
			self.layList = (
				"all windows",
				"modules",
				"content", 
				"docs", 
				"object",
				"command"
			)

			self.layO = QtGui.QComboBox(self)
			self.layO.addItems(self.layList)
			self.layO.setCurrentIndex(self.layList.index("all windows"))
			self.layO.activated[str].connect(self.setWindowsLayout)
			self.layO.setFixedWidth((1*self.gGridCol)-20)

			# select windows colors
			# ############################################################################

			# label
			self.colorsL = QtGui.QLabel("Select colors:", self)
			
			# options
			self.colorsList = (
				"matrix blue pill",
				"beautiful pinky world",
				"the sky is blue",
				"my world is gray",
				"grass is green everywhere",
				"I like winter more",
				"matrix red pill"
			)

			self.colorsO = QtGui.QComboBox(self)
			self.colorsO.addItems(self.colorsList)
			self.colorsO.setCurrentIndex(self.colorsList.index("matrix blue pill"))
			self.colorsO.activated[str].connect(self.setWindowsColors)
			self.colorsO.setFixedWidth((1*self.gGridCol)-20)
			
			# custom command execute
			# ############################################################################

			# label
			self.oCommandL = QtGui.QLabel("Custom command execute:", self)
			
			# text input
			self.oCommandI = QtGui.QLineEdit(self)
			self.oCommandI.setText("FreeCADGui.getMainWindow().children()")
			self.oCommandI.setFixedWidth((1*self.gGridCol)-20)
			
			# button
			self.oCommandB = QtGui.QPushButton("load command result", self)
			self.oCommandB.clicked.connect(self.executeCustomCommand)
			self.oCommandB.setFixedWidth((1*self.gGridCol)-20)
			
			# options sub-window
			# ############################################################################

			# label
			self.OPTLabel = QtGui.QLabel("Select options type to show:", self)
			
			# options
			self.OPTList = (
				"scan root",
				"layout & colors"
			)

			self.OPTListQ = QtGui.QComboBox(self)
			self.OPTListQ.addItems(self.OPTList)
			self.OPTListQ.setCurrentIndex(self.OPTList.index("scan root"))
			self.OPTListQ.activated[str].connect(self.setOptionsVisibility)
			self.OPTListQ.setFixedWidth((1*self.gGridCol)-20)
			
			self.OPTlayout = QtGui.QVBoxLayout()
			self.OPTlayout.setAlignment(QtGui.Qt.AlignTop)
			
			self.OPTlayout.addWidget(self.OPTLabel)
			self.OPTlayout.addWidget(self.OPTListQ)
			self.OPTseparator = QtGui.QLabel("", self)
			self.OPTlayout.addWidget(self.OPTseparator)

			self.OPTlayout.addWidget(self.rootL)
			self.OPTlayout.addWidget(self.rootO)
			self.OPTlayout.addWidget(self.rootCL)
			self.OPTlayout.addWidget(self.rootCO)
			self.OPTlayout.addWidget(self.rootCLoad)
			self.OPTlayout.addWidget(self.layL)
			self.OPTlayout.addWidget(self.layO)
			self.OPTlayout.addWidget(self.colorsL)
			self.OPTlayout.addWidget(self.colorsO)
			self.OPTlayout.addWidget(self.oCommandL)
			self.OPTlayout.addWidget(self.oCommandI)
			self.OPTlayout.addWidget(self.oCommandB)

			self.rootL.show()
			self.rootO.show()
			self.rootCL.hide()
			self.rootCO.hide()
			self.rootCLoad.hide()
			self.oCommandL.hide()
			self.oCommandI.hide()
			self.oCommandB.hide()
			self.layL.hide()
			self.layO.hide()
			self.colorsL.hide()
			self.colorsO.hide()
			
			self.OPTwidget = QtGui.QWidget()
			self.OPTwidget.setLayout(self.OPTlayout)

			self.OPTsw = QtGui.QMdiSubWindow(self)
			self.OPTsw.setWindowTitle("Options :")
			self.OPTsw.setWidget(self.OPTwidget)


			# ############################################################################
			# selection view
			# ############################################################################


			self.list = QtGui.QListView()
			self.listsw = QtGui.QMdiSubWindow(self)
			self.listsw.setWindowTitle("Select object :")
			self.listsw.setWidget(self.list)


			# ############################################################################
			# outputs
			# ############################################################################


			# output 1
			# ############################################################################

			self.o1 = QtGui.QTextEdit()
			self.o1sw = QtGui.QMdiSubWindow(self)
			self.o1sw.setWindowTitle("Help Window & dir() :")
			self.o1sw.setWidget(self.o1)

			# output 2
			# ############################################################################
			
			self.o2 = QtGui.QTextEdit()
			self.o2sw = QtGui.QMdiSubWindow(self)
			self.o2sw.setWindowTitle("__dict__ :")
			self.o2sw.setWidget(self.o2)
			
			# output 3
			# ############################################################################

			self.o3 = QtGui.QTextEdit()
			self.o3sw = QtGui.QMdiSubWindow(self)
			self.o3sw.setWindowTitle("__doc__ :")
			self.o3sw.setWidget(self.o3)

			# output 4
			# ############################################################################

			self.o4 = QtGui.QTextEdit()
			self.o4sw = QtGui.QMdiSubWindow(self)
			self.o4sw.setWindowTitle("getAllDerivedFrom() :")
			self.o4sw.setWidget(self.o4)

			# output 5
			# ############################################################################

			self.o5 = QtGui.QTextEdit()
			self.o5sw = QtGui.QMdiSubWindow(self)
			self.o5sw.setWindowTitle("Content & Error Console :")
			self.o5sw.setWidget(self.o5)

			# output 6
			# ############################################################################

			self.o6 = QtGui.QTextEdit()
			self.o6sw = QtGui.QMdiSubWindow(self)
			self.o6sw.setWindowTitle("Object parse view :")
			self.o6sw.setWidget(self.o6)


			# ############################################################################
			# keyboard keys
			# ############################################################################


			QtGui.QShortcut(QtGui.QKeySequence("left"), self, self.keyLeft)
			QtGui.QShortcut(QtGui.QKeySequence("right"), self, self.keyRight)


			# ############################################################################
			# show & init defaults
			# ############################################################################


			# init default selection db
			if self.gDefaultRoot == "project":
				self.setRootPath("my project root")
			else:
				self.setRootPath("Module: FreeCAD")

			# show window
			self.show()

			# set default layout
			self.setWindowsLayout("all windows")

			# set default colors
			#self.setWindowsColors("matrix blue pill")
			self.setWindowsColors("beautiful pinky world") # my favorite colors ;-)

		# ############################################################################
		# actions - function for actions
		# ############################################################################


		# ############################################################################
		def setOutput(self, iObj):

			# reset outputs before set new values
			self.resetOutputs()

			# get selected item index
			index = iObj.indexes()[0].row()

			# output 1
			# ########################################

			skip = 0

			try:
				result = dir(self.dbSO[self.dbSI][index])
			except:
				skip = 1

			try:
				if skip == 0:

					o1 = ""
					for row in result:
						o1 += row + "\n"
					
					self.o1.setPlainText(o1)
				else:
					self.o1.setPlainText("")
			except:
				skip = 1

			# output 2
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index].__dict__
			except:
				skip = 1

			try:
				if skip == 0:

					o2 = ""
					for row in result:
						o2 += row + "\n"
					
					self.o2.setPlainText(o2)
				else:
					self.o2.setPlainText("")
			except:
				skip = 1

			# output 3
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index].__doc__
			except:
				skip = 1

			try:
				if skip == 0:
					self.o3.setPlainText(result)
				else:
					self.o3.setPlainText("")
			except:
				skip = 1

			# output 4
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index].getAllDerivedFrom()
			except:
				skip = 1

			try:
				if skip == 0:

					o4 = ""
					for row in result:
						o4 += row + "\n"
					
					self.o4.setPlainText(o4)
				else:
					self.o4.setPlainText("")
			except:
				skip = 1

			# output 5
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index].Content
			except:
				skip = 1

			try:
				if skip == 0:
					self.o5.setPlainText(result)
				else:
					self.o5.setPlainText("")
			except:
				skip = 1

			# output 6 - object window
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index]
			except:
				skip = 1

			try:

				# <class 'str'>
				if skip == 0 and isinstance(result, str):
					self.o6.setPlainText(str(result))

				# <class 'float'>
				elif skip == 0 and isinstance(result, float):
					self.o6.setPlainText(str(result))

				# <class 'list'>
				elif skip == 0 and isinstance(result, list):

					o6 = ""
					for row in result:
						o6 += str(row) + "\n"
					
					self.o6.setPlainText(o6)

				# getChildren()
				elif skip == 0:

					try:
						r = result.getChildren()
						o6 = ""
						for row in r:
							o6 += str(row) + "\n"
													
						self.o6.setPlainText(o6)
					except:
						self.o6.setPlainText(str(result))
						skip = 1

				# show raw object
				else:
					self.o6.setPlainText(str(result))

				# set window title to object type
				self.o6sw.setWindowTitle(str(type(result)) + " :")

			except:
				skip = 1


		# ############################################################################	
		def getSelectionPath(self):

			path = ""
			for item in self.dbSP:
				path += "." + item + "\n"

			return str(path)[1:]


		# ############################################################################
		def resetOutputs(self):

			path = self.getSelectionPath()

			if self.gModeType == "matrix":
				info = ""
				info += "Current rabbit hole is:"
				info += "\n\n"
				info += path
				info += "\n\n\n"
				info += "Usage:"
				info += "\n"
				info += "→ \t | go deeper"
				info += "\n"
				info += "← \t | go back"
				info += "\n"
				info += "↑ ↓ \t | select rabbit hole"
				info += "\n\n"
				info += "Use ↑ ↓ arrow keys to select rabbit hole and enter the matrix."
			else:
				info = ""
				info += "Your current selection path is:"
				info += "\n\n"
				info += path
				info += "\n\n\n"
				info += "Usage:"
				info += "\n"
				info += "→ \t | go deeper"
				info += "\n"
				info += "← \t | go back"
				info += "\n"
				info += "↑ ↓ \t | select object"
				info += "\n\n"
				info += "Use ↑ ↓ arrow keys to select object and start inspection at this path."

			self.o1.setPlainText(info)
			self.o2.setPlainText("")
			self.o3.setPlainText("")
			self.o4.setPlainText("")
			self.o5.setPlainText("")
			self.o6.setPlainText("")


		# ############################################################################
		def updateSelection(self):

			model = QtGui.QStandardItemModel(self.list)
			
			for o in self.dbSL[self.dbSI]:
				item = QtGui.QStandardItem(str(o))
				model.appendRow(item)
				self.list.setModel(model)

			self.list.selectionModel().selectionChanged.connect(self.setOutput)
			
			# reset outputs and show info screen
			self.resetOutputs()


		# ############################################################################
		def removeSelection(self):

			# stop remove if there is only init objects list
			if self.dbSI > 0:

				self.dbSO.pop()
				self.dbSL.pop()
				self.dbSP.pop()
				self.dbSI = self.dbSI - 1

				self.updateSelection()

			# set last selected
			try:

				# select item
				item = self.dbSLI[self.dbSI]
				flag = QtCore.QItemSelectionModel.Select
				self.list.selectionModel().setCurrentIndex(item, flag)

				# scroll to item
				flag = QtGui.QAbstractItemView.EnsureVisible.PositionAtCenter
				self.list.scrollTo(item, flag)

			except:
				skip = 1

			# remove last selected
			if self.dbSI > 0:
				self.dbSLI.pop()

			# reset outputs
			self.resetOutputs()


		# ############################################################################
		def addSelection(self, iObj, iList, iPath, iSelected):

			tmpO = []
			tmpL = []

			# init selection view (compare strings only)
			if str(iObj) == "":
				tmpO = iList
				tmpL = [ o.Label for o in tmpO ]

			# if object is list (eg. faces, edges)
			elif isinstance(iObj, list):
				tmpO = iObj
				tmpL = iObj

			# all objects types
			else:
				for o in iList:
					
					# fix FreeCAD bug https://forum.freecadweb.org/viewtopic.php?f=22&t=70365
					if str(o) == "DraggingPlacement":
						continue
					
					try:
						if hasattr(iObj, o):
							tmpO.append(getattr(iObj, o))
							tmpL.append(str(o))
					except:
						skip = 1

			# not add empty lists (this stuck)
			if len(tmpO) > 0 and len(tmpL) > 0:

				# update db
				self.dbSO.append(tmpO)
				self.dbSL.append(tmpL)
				self.dbSP.append(iPath)

				# not select at init
				if iSelected != -1:
					self.dbSLI.insert(self.dbSI, iSelected)

				self.dbSI = self.dbSI + 1

				# update selection list
				self.updateSelection()

			else:
				if self.gModeType == "matrix":
					self.showMsg("This is the end of the rabbit hole. Go back quickly before you get lost ;-)", "info")
				else:
					self.showMsg("Can't parse this object structure deeper. Check deeper at the python console.", "info")


		# ############################################################################
		# actions - options menu
		# ############################################################################


		# ############################################################################
		def setOptionsVisibility(self, selectedText):

			if selectedText == "scan root":
				self.rootL.show()
				self.rootO.show()
				
				self.rootCL.hide()
				self.rootCO.hide()
				self.rootCLoad.hide()
				self.oCommandL.hide()
				self.oCommandI.hide()
				self.oCommandB.hide()
				self.layL.hide()
				self.layO.hide()
				self.colorsL.hide()
				self.colorsO.hide()
			
			if selectedText == "layout & colors":
				self.rootL.hide()
				self.rootO.hide()
				self.rootCL.hide()
				self.rootCO.hide()
				self.rootCLoad.hide()
				self.oCommandL.hide()
				self.oCommandI.hide()
				self.oCommandB.hide()
				
				self.layL.show()
				self.layO.show()
				self.colorsL.show()
				self.colorsO.show()


		# ############################################################################
		def setRootPath(self, selectedText):

			# clear db before root set
			self.clearDB()

			if selectedText == "my project root":
					
				try:
					root = FreeCAD.activeDocument().Objects
					rootS = "FreeCAD.activeDocument().Objects"
					self.addSelection("", root, rootS, -1)
				except:
					if self.gModeType == "matrix":
						self.showMsg("You need to release project first to enter the matrix ;-)")
					else:
						self.showMsg("You have to set active document (project) to use this root path.")

			if selectedText == "Module: FreeCAD":

				root = dir(FreeCAD)
				rootS = "FreeCAD"
				self.addSelection(FreeCAD, root, rootS, -1)

			if selectedText == "Module: QtGui":

				from PySide import QtGui

				root = dir(QtGui)
				rootS = "QtGui"
				self.addSelection(QtGui, root, rootS, -1)

			if selectedText == "Module: QtCore":

				from PySide import QtCore

				root = dir(QtCore)
				rootS = "QtCore"
				self.addSelection(QtCore, root, rootS, -1)

			if selectedText == "Module: Path":

				import Path

				root = dir(Path)
				rootS = "Path"
				self.addSelection(Path, root, rootS, -1)

			if selectedText == "Module: Draft":

				import Draft

				root = dir(Draft)
				rootS = "Draft"
				self.addSelection(Draft, root, rootS, -1)

			if selectedText == "Module: TechDraw":

				import TechDraw

				root = dir(TechDraw)
				rootS = "TechDraw"
				self.addSelection(TechDraw, root, rootS, -1)

			if selectedText == "Module: Spreadsheet":

				import Spreadsheet

				root = dir(Spreadsheet)
				rootS = "Spreadsheet"
				self.addSelection(Spreadsheet, root, rootS, -1)

			if selectedText == "Module: coin":

				from pivy import coin

				root = dir(coin)
				rootS = "coin"
				self.addSelection(coin, root, rootS, -1)

			if selectedText == "custom module":
				self.rootL.show()
				self.rootO.show()
				self.rootCL.show()
				self.rootCO.show()
				self.rootCLoad.show()
				
				self.oCommandL.hide()
				self.oCommandI.hide()
				self.oCommandB.hide()
				self.layL.hide()
				self.layO.hide()
				self.colorsL.hide()
				self.colorsO.hide()
			
			if selectedText == "custom command result":
				self.rootL.show()
				self.rootO.show()
				self.oCommandL.show()
				self.oCommandI.show()
				self.oCommandB.show()
				
				self.rootCL.hide()
				self.rootCO.hide()
				self.rootCLoad.hide()
				self.layL.hide()
				self.layO.hide()
				self.colorsL.hide()
				self.colorsO.hide()


		# ############################################################################
		def setWindowsLayout(self, selectedText):

			if selectedText == "all windows":

				# options
				self.OPTsw.setGeometry(0, (3*self.gGridRow), (1*self.gGridCol), (2*self.gGridRow))
				self.OPTsw.show()

				# select
				self.listsw.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.listsw.show()
				self.list.show()

				# dir
				self.o1sw.setGeometry((1*self.gGridCol), 0, (1*self.gGridCol), (3*self.gGridRow))
				self.o1sw.show()
				self.o1.show()

				# __dict__
				self.o2sw.setGeometry((2*self.gGridCol), 0, (1*self.gGridCol), (3*self.gGridRow))
				self.o2sw.show()
				self.o2.show()

				# __doc__
				self.o3sw.setGeometry((3*self.gGridCol), 0, (2*self.gGridCol), (1*self.gGridRow))
				self.o3sw.show()
				self.o3.show()

				# getAllDerivedFrom
				self.o4sw.setGeometry((3*self.gGridCol), (1*self.gGridRow), (2*self.gGridCol), (1*self.gGridRow))
				self.o4sw.show()
				self.o4.show()

				# content
				self.o5sw.setGeometry((1*self.gGridCol), (3*self.gGridRow), (4*self.gGridCol), (2*self.gGridRow))
				self.o5sw.show()
				self.o5.show()

				# object
				self.o6sw.setGeometry((3*self.gGridCol), (2*self.gGridRow), (2*self.gGridCol), (1*self.gGridRow))
				self.o6sw.show()
				self.o6.show()

			if selectedText == "modules":
				self.OPTsw.setGeometry(0, (3*self.gGridRow), (1*self.gGridCol), (2*self.gGridRow))
				self.OPTsw.show()
				self.listsw.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.listsw.show()
				self.list.show()
				self.o1sw.setGeometry((1*self.gGridCol), 0, (1*self.gGridCol), (3*self.gGridRow))
				self.o1sw.show()
				self.o1.show()
				self.o2sw.setGeometry((2*self.gGridCol), 0, (1*self.gGridCol), (3*self.gGridRow))
				self.o2sw.show()
				self.o2.show()
				self.o3sw.setGeometry((3*self.gGridCol), 0, (2*self.gGridCol), (2*self.gGridRow))
				self.o3sw.show()
				self.o3.show()

				self.o4sw.hide()
				self.o4.hide()

				self.o5sw.setGeometry((1*self.gGridCol), (3*self.gGridRow), (4*self.gGridCol), (2*self.gGridRow))
				self.o5sw.show()
				self.o5.show()

				self.o6sw.setGeometry((3*self.gGridCol), (2*self.gGridRow), (2*self.gGridCol), (1*self.gGridRow))
				self.o6sw.show()
				self.o6.show()

			if selectedText == "content":
				self.OPTsw.setGeometry(0, (3*self.gGridRow), (1*self.gGridCol), (2*self.gGridRow))
				self.OPTsw.show()
				self.listsw.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.listsw.show()
				self.list.show()

				self.o1sw.hide()
				self.o1.hide()
				self.o2sw.hide()
				self.o2.hide()
				self.o3sw.hide()
				self.o3.hide()
				self.o4sw.hide()
				self.o4.hide()

				self.o5sw.setGeometry((1*self.gGridCol), 0, (4*self.gGridCol), (5*self.gGridRow))
				self.o5sw.show()
				self.o5.show()

				self.o6sw.hide()
				self.o6.hide()

			if selectedText == "docs":
				self.OPTsw.setGeometry(0, (3*self.gGridRow), (1*self.gGridCol), (2*self.gGridRow))
				self.OPTsw.show()
				self.listsw.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.listsw.show()
				self.list.show()

				self.o1sw.hide()
				self.o1.hide()
				self.o2sw.hide()
				self.o2.hide()

				self.o3sw.setGeometry((1*self.gGridCol), 0, (4*self.gGridCol), (5*self.gGridRow))
				self.o3sw.show()
				self.o3.show()

				self.o4sw.hide()
				self.o4.hide()
				self.o5sw.hide()
				self.o5.hide()
				self.o6sw.hide()
				self.o6.hide()

			if selectedText == "object":
				self.OPTsw.setGeometry(0, (3*self.gGridRow), (1*self.gGridCol), (2*self.gGridRow))
				self.OPTsw.show()
				self.listsw.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.listsw.show()
				self.list.show()

				self.o1sw.hide()
				self.o1.hide()
				self.o2sw.hide()
				self.o2.hide()
				self.o3sw.hide()
				self.o3.hide()
				self.o4sw.hide()
				self.o4.hide()
				self.o5sw.hide()
				self.o5.hide()
				self.o6sw.setGeometry((1*self.gGridCol), 0, (4*self.gGridCol), (5*self.gGridRow))
				self.o6sw.show()
				self.o6.show()

			if selectedText == "command":
				self.OPTsw.setGeometry(0, (3*self.gGridRow), (1*self.gGridCol), (2*self.gGridRow))
				self.OPTsw.show()
				self.listsw.setGeometry(0, 0, (2*self.gGridCol), (3*self.gGridRow))
				self.listsw.show()
				self.list.show()
				self.o1sw.setGeometry((2*self.gGridCol), 0, (1*self.gGridCol), (3*self.gGridRow))
				self.o1sw.show()
				self.o1.show()
				self.o2sw.setGeometry((3*self.gGridCol), 0, (1*self.gGridCol), (3*self.gGridRow))
				self.o2sw.show()
				self.o2.show()
				self.o3sw.setGeometry((4*self.gGridCol), 0, (1*self.gGridCol), (2*self.gGridRow))
				self.o3sw.show()
				self.o3.show()

				self.o4sw.hide()
				self.o4.hide()

				self.o5sw.setGeometry((1*self.gGridCol), (3*self.gGridRow), (4*self.gGridCol), (2*self.gGridRow))
				self.o5sw.show()
				self.o5.show()

				self.o6sw.setGeometry((4*self.gGridCol), (2*self.gGridRow), (1*self.gGridCol), (1*self.gGridRow))
				self.o6sw.show()
				self.o6.show()


		# ############################################################################
		def setWindowsColors(self, selectedText):

			if selectedText == "matrix blue pill":

				self.setStyleSheet("")
				self.gModeType = "normal"
			
			if (
				selectedText == "my world is gray" or
				selectedText == "beautiful pinky world" or
				selectedText == "the sky is blue" or
				selectedText == "grass is green everywhere" or
				selectedText == "I like winter more"
				):

				if selectedText == "beautiful pinky world":
					color1 = "#FF00EE"
					color2 = "#FFFFFF"
					color3 = "#FF00EE"

				if selectedText == "the sky is blue":
					color1 = "#AAAAFF"
					color2 = "#FFFFFF"
					color3 = "#AAAAFF"
					
				if selectedText == "my world is gray":
					color1 = "#A1A1A1"
					color2 = "#D1D1D1"
					color3 = "#A1A1A1"

				if selectedText == "grass is green everywhere":
					color1 = "#AAFFAA"
					color2 = "#FFFFFF"
					color3 = "#AAFFAA"
				
				if selectedText == "I like winter more":
					color1 = "#E1E1E1"
					color2 = "#FFFFFF"
					color3 = "#E1E1E1"

				QtCSS =  '''
					QDialog, QScrollBar {
						background-color: '''+color1+''';
					}

					QMdiSubWindow {
						color: #000000;
						background-color: '''+color1+''';
						border: 1px solid transparent;
						selection-color: '''+color1+''';
						selection-background-color: '''+color1+''';
					}

					QTextEdit, QListView, QComboBox {
						color: #000000;
						background-color: qlineargradient( 
							x1: 0, y1: 0, 
							x2: 2, y2: 2,
							stop: 0 '''+color2+''', stop: 1 '''+color1+'''
						);
						border: 0px;
						border-right: 1px dotted '''+color1+''';
						border-bottom: 1px dotted '''+color1+''';
						selection-color: #000000;
						selection-background-color: '''+color3+''';
					}

					QLabel { 
						color: #000000;
						background-color: '''+color1+''';
					}
										
					QLineEdit, QPushButton {
						color: #000000;
						background-color: qlineargradient( 
							x1: 0, y1: 0, 
							x2: 2, y2: 2,
							stop: 0 '''+color2+''', stop: 1 '''+color1+'''
						);
						border: 1px dotted '''+color1+''';
					}
				'''

				self.setStyleSheet(QtCSS)
				self.gModeType = "normal"

			if selectedText == "matrix red pill":

				QtCSS =  '''
					QDialog, QScrollBar {
						background-color: black;
					}

					QMdiSubWindow {
						color: green;
						background-color: black;
						border: 1px solid transparent;
						selection-color: white;
						selection-background-color: black;
					}

					QTextEdit, QListView, QComboBox {
						color: green;
						background-color: qlineargradient( 
							x1: 0, y1: 0, 
							x2: 15, y2: 15,
							stop: 0 #000000, stop: 1 #00FF00
						);
						border: 0px;
						border-right: 1px dotted green;
						border-bottom: 1px dotted green;
						selection-color: white;
						selection-background-color: black;
					}

					QLabel { 
						color: white;
						background-color: black;
					}
										
					QLineEdit, QPushButton {
						color: green;
						background-color: qlineargradient( 
							x1: 0, y1: 0, 
							x2: 10, y2: 10,
							stop: 0 #000000, stop: 1 #00FF00
						);
						border: 1px dotted green;
					}

					QScrollBar {
						border: 0px;
					}
					
					QScrollBar::handle {
						border: 1px dotted #FFFFFF;
					}
				'''
				
				self.setStyleSheet(QtCSS)
				self.gModeType = "matrix"


		# ############################################################################
		# actions - other
		# ############################################################################


		# ############################################################################
		def loadCustomModule(self):

			try:
				rootS = str(self.rootCO.text())				

				module = __import__(rootS, globals(), locals(), [], 0)
				root = dir(module)

				self.clearDB()
				self.addSelection(module, root, rootS, -1)

			except:

				if self.gModeType == "matrix":
					self.showMsg("This module is outside the matrix: "+rootS)
				else:
					self.showMsg("Can't load module: "+rootS)
		
		
		# ############################################################################
		def executeCustomCommand(self):
			try:
				command = self.oCommandI.text()
				result = eval(str(command))
	
				if isinstance(result, list):
					self.clearDB()
					self.addSelection(result, result, command, -1)

				else:
	
					if self.gModeType == "matrix":
						self.showMsg("You calling wrong number to the matrix: "+command)
					else:
						self.showMsg("To scan command the result of command should be list type: "+command)

			except:

				if self.gModeType == "matrix":
					self.showMsg("This command is outside the matrix: "+command)
				else:
					self.showMsg("Can't evaluate command: "+command)


		# ############################################################################
		# actions - for keyboard keys
		# ############################################################################

		def keyLeft(self):
			self.removeSelection()

		def keyRight(self):

			try:
				selected = self.list.currentIndex()
				index = selected.row()
				Obj = self.dbSO[self.dbSI][index]
				path = str(self.dbSL[self.dbSI][index])

				if isinstance(Obj, str):
					skip = 1
				elif isinstance(Obj, float):
					skip = 1
				elif isinstance(Obj, list):
					newList = Obj
					self.addSelection(Obj, newList, path, selected)
				else:
					try:
						newList = []
						for n in Obj.getChildren():
							newList.append(n)
	
						self.addSelection(newList, newList, path, selected)
					except:
						newList = dir(Obj)
						self.addSelection(Obj, newList, path, selected)
			except:
				skip = 1


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


showQtGUI()


# ###################################################################################################################
