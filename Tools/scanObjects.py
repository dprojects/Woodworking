# ###################################################################################################################
'''

Inspection tool for FreeCAD macro development
Author: Darek L (github.com/dprojects)
Latest version: https://github.com/dprojects/scanObjects

Certified platform:
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

		dbObjects = dict()     # dbObjects[dbPage] = array of objects
		dbLabels = dict()      # dbLabels[dbPage] = array of labels
		dbPath = dict()        # dbPath[dbPage] = string label path for this page
		dbLastIndex = dict()   # dbLastIndex[dbPage] = string selection index for this page
		dbPage = "0"           # string page index used as key

		# ############################################################################
		# controllers for database
		# ############################################################################

		def clearDB(self):

			self.dbObjects = dict()
			self.dbLabels = dict()
			self.dbPath = dict()
			self.dbLastIndex = dict()
			self.dbPage = "0"

		def getSelectionIndex(self):
			
			# convert from proxy filter index to data real index
			# this will be quicker and better I guess than 
			# updating the data with the filter in real-time
			# big data not change, change only index, that's the trick ;-)
			try:
				selected = self.slist.currentIndex()
				label = selected.data()
				index = self.dbLabels[self.dbPage].index(label)
			except:
				index = ""

			return index

		def getSelectionObject(self):

			try:
				index = self.getSelectionIndex()
				obj = self.dbObjects[self.dbPage][index]
				
			except:
				obj = ""

			return obj
		
		def getSelectionLabel(self):

			try:
				index = self.getSelectionIndex()
				label = str(self.dbLabels[self.dbPage][index])
				
			except:
				label = ""

			return label

		def getSelectionPath(self):

			path = ""
			for item in self.dbPath.values():
				path += "." + item + "\n"

			return str(path)[1:]

		def setNewPage(self, iType):

			if iType == "init":
				self.dbLastIndex[self.dbPage] = ""
			else:
				index = self.getSelectionIndex()
				self.dbLastIndex[self.dbPage] = str(index)
				self.dbPage = str(int(self.dbPage) + 1)

		def removeCurrentPage(self):
			
			if int(self.dbPage) > 0:
				
				del self.dbObjects[self.dbPage]
				del self.dbLabels[self.dbPage]
				del self.dbPath[self.dbPage]
				if self.dbPage in self.dbLastIndex.keys():
					del self.dbLastIndex[self.dbPage]
			
				self.dbPage = str(int(self.dbPage) - 1)

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
		# init - it should be first but not in my code ;-)
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
			# options - scan root
			# ############################################################################
			
			# label
			self.orootlabel = QtGui.QLabel("Select scan root path:", self)
			
			# options
			self.orootlist = (
				"my project root",
				"Module: FreeCAD",
				"Module: Part",
				"Module: QtGui", 
				"Module: QtCore",
				"Module: coin",
				"Module: Path",
				"Module: Draft", 
				"Module: TechDraw", 
				"Module: Spreadsheet",
				"Module: MagicPanels",
				"custom module",
				"custom command result"
			)

			self.orootcb = QtGui.QComboBox(self)
			self.orootcb.addItems(self.orootlist)
			if self.gDefaultRoot == "project":
				self.orootcb.setCurrentIndex(self.orootlist.index("my project root"))
			else:
				self.orootcb.setCurrentIndex(self.orootlist.index("Module: FreeCAD"))
			self.orootcb.activated[str].connect(self.setRootPath)
			self.orootcb.setFixedWidth((1*self.gGridCol)-20)
			
			# ############################################################################
			# options - custom module
			# ############################################################################

			# label
			self.ocmlabel = QtGui.QLabel("Custom module name:", self)
			
			# input
			self.ocminput = QtGui.QLineEdit(self)
			self.ocminput.setText("")
			self.ocminput.setFixedWidth((1*self.gGridCol)-20)
			
			# button
			self.ocmbutton = QtGui.QPushButton("load custom module", self)
			self.ocmbutton.clicked.connect(self.loadCustomModule)
			self.ocmbutton.setFixedWidth((1*self.gGridCol)-20)
			self.ocmbutton.setFixedHeight(40)
			
			# ############################################################################
			# options - windows layout
			# ############################################################################

			# label
			self.owllabel = QtGui.QLabel("Select windows layout:", self)
			
			# list
			self.owllist = (
				"all windows",
				"coding",
				"docs",
				"modules",
				"content",
				"object",
				"command"
			)

			self.owlcb = QtGui.QComboBox(self)
			self.owlcb.addItems(self.owllist)
			self.owlcb.setCurrentIndex(self.owllist.index("all windows"))
			self.owlcb.activated[str].connect(self.setWindowsLayout)
			self.owlcb.setFixedWidth((1*self.gGridCol)-20)
			
			# ############################################################################
			# options - windows colors
			# ############################################################################

			# label
			self.owclabel = QtGui.QLabel("Select colors:", self)
			
			# options
			self.owclist = (
				"matrix blue pill",
				"beautiful pinky world",
				"the Sun is free?",
				"the sky is blue",
				"my world is gray",
				"grass is green everywhere",
				"I like winter more",
				"matrix red pill"
			)

			gDefaultColors = "matrix blue pill"

			self.owcqb = QtGui.QComboBox(self)
			self.owcqb.addItems(self.owclist)
			self.owcqb.setCurrentIndex(self.owclist.index(gDefaultColors))
			self.owcqb.activated[str].connect(self.setWindowsColors)
			self.owcqb.setFixedWidth((1*self.gGridCol)-20)
			
			# ############################################################################
			# options - command result
			# ############################################################################

			# label
			self.ocrlabel = QtGui.QLabel("Custom command execute:", self)
			
			# input
			self.ocrinput = QtGui.QLineEdit(self)
			self.ocrinput.setText("FreeCADGui.getMainWindow().children()")
			self.ocrinput.setFixedWidth((1*self.gGridCol)-20)
			
			# button
			self.ocrbutton = QtGui.QPushButton("load command result", self)
			self.ocrbutton.clicked.connect(self.executeCustomCommand)
			self.ocrbutton.setFixedWidth((1*self.gGridCol)-20)
			self.ocrbutton.setFixedHeight(40)
			
			# ############################################################################
			# options - container
			# ############################################################################

			self.oseparator = QtGui.QLabel("", self)

			self.oclayout = QtGui.QVBoxLayout()
			self.oclayout.setAlignment(QtGui.Qt.AlignTop)
			
			self.oclayout.addWidget(self.orootlabel)
			self.oclayout.addWidget(self.orootcb)
			self.oclayout.addWidget(self.ocmlabel)
			self.oclayout.addWidget(self.ocminput)
			self.oclayout.addWidget(self.ocmbutton)
			self.oclayout.addWidget(self.ocrlabel)
			self.oclayout.addWidget(self.ocrinput)
			self.oclayout.addWidget(self.ocrbutton)
			self.oclayout.addWidget(self.oseparator)
			self.oclayout.addWidget(self.owllabel)
			self.oclayout.addWidget(self.owlcb)
			self.oclayout.addWidget(self.owclabel)
			self.oclayout.addWidget(self.owcqb)
			
			self.ocmlabel.hide()
			self.ocminput.hide()
			self.ocmbutton.hide()
			self.ocrlabel.hide()
			self.ocrinput.hide()
			self.ocrbutton.hide()
			
			self.ocwidget = QtGui.QWidget()
			self.ocwidget.setLayout(self.oclayout)

			self.OPTsw = QtGui.QMdiSubWindow(self)
			self.OPTsw.setWindowTitle("Options :")
			self.OPTsw.setWidget(self.ocwidget)

			# ############################################################################
			# window - selection
			# ############################################################################
			
			self.slist = QtGui.QListView()
			
			placeholder = "... search filter ..."
			
			self.sfilter = QtGui.QLineEdit()
			self.sfilter.setPlaceholderText(placeholder)
			self.sfilter.textChanged.connect(self.setFilter)

			self.slayout = QtGui.QVBoxLayout()
			self.slayout.setAlignment(QtGui.Qt.AlignTop)
			self.slayout.addWidget(self.sfilter)
			self.slayout.addWidget(self.slist)
			
			self.swidget = QtGui.QWidget()
			self.swidget.setLayout(self.slayout)

			self.swindow = QtGui.QMdiSubWindow(self)
			self.swindow.setWindowTitle("Select object :")
			self.swindow.setWidget(self.swidget)

			self.smodel = QtGui.QStandardItemModel(self.slist)
			
			self.sproxy = QtCore.QSortFilterProxyModel()
			self.sproxy.setSourceModel(self.smodel)
			self.sproxy.setDynamicSortFilter(False)

			self.slist.setModel(self.sproxy)
			self.slist.selectionModel().selectionChanged.connect(self.selectionChanged)
			
			# ############################################################################
			# window - output 1
			# ############################################################################

			self.o1 = QtGui.QTextEdit()
			self.o1sw = QtGui.QMdiSubWindow(self)
			self.o1sw.setWindowTitle("Help Window & dir() :")
			self.o1sw.setWidget(self.o1)

			# ############################################################################
			# window - output 2
			# ############################################################################
			
			self.o2 = QtGui.QTextEdit()
			self.o2sw = QtGui.QMdiSubWindow(self)
			self.o2sw.setWindowTitle("__dict__ :")
			self.o2sw.setWidget(self.o2)

			# ############################################################################
			# window - output 3
			# ############################################################################

			self.o3 = QtGui.QTextEdit()
			self.o3sw = QtGui.QMdiSubWindow(self)
			self.o3sw.setWindowTitle("__doc__ :")
			self.o3sw.setWidget(self.o3)

			# ############################################################################
			# window - output 4
			# ############################################################################

			self.o4 = QtGui.QTextEdit()
			self.o4sw = QtGui.QMdiSubWindow(self)
			self.o4sw.setWindowTitle("getAllDerivedFrom() :")
			self.o4sw.setWidget(self.o4)

			# ############################################################################
			# window - output 5
			# ############################################################################

			self.o5 = QtGui.QTextEdit()
			self.o5sw = QtGui.QMdiSubWindow(self)
			self.o5sw.setWindowTitle("Content & Error Console :")
			self.o5sw.setWidget(self.o5)

			# ############################################################################
			# window - output 6
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
			self.setWindowsColors(gDefaultColors)

		# ############################################################################
		# actions - update screens
		# ############################################################################

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

			self.smodel.clear()
			
			for o in self.dbLabels[self.dbPage]:
				item = QtGui.QStandardItem(str(o))
				self.smodel.appendRow(item)
			
			self.resetOutputs()

		# ############################################################################
		def selectionChanged(self, iSelection):

			self.resetOutputs()
			
			index = self.getSelectionIndex()

			# after right key pressed there is no selection
			if index == "":
				return
			
			# ########################################
			# output 1
			# ########################################

			skip = 0

			try:
				result = dir(self.dbObjects[self.dbPage][index])
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

			# ########################################
			# output 2
			# ########################################

			skip = 0

			try:
				result = self.dbObjects[self.dbPage][index].__dict__
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

			# ########################################
			# output 3
			# ########################################

			skip = 0

			try:
				result = self.dbObjects[self.dbPage][index].__doc__
			except:
				skip = 1

			try:
				if skip == 0:
					self.o3.setPlainText(result)
				else:
					self.o3.setPlainText("")
			except:
				skip = 1

			# ########################################
			# output 4
			# ########################################

			skip = 0

			try:
				result = self.dbObjects[self.dbPage][index].getAllDerivedFrom()
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

			# ########################################
			# output 5
			# ########################################

			skip = 0

			try:
				result = self.dbObjects[self.dbPage][index].Content
			except:
				skip = 1

			try:
				if skip == 0:
					self.o5.setPlainText(result)
				else:
					self.o5.setPlainText("")
			except:
				skip = 1

			# ########################################
			# output 6 - object window
			# ########################################

			skip = 0

			try:
				result = self.dbObjects[self.dbPage][index]
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
		# actions - options menu
		# ############################################################################

		def setRootPath(self, selectedText):

			# clear db before root set
			self.clearDB()
			
			self.ocmlabel.hide()
			self.ocminput.hide()
			self.ocmbutton.hide()
			self.ocrlabel.hide()
			self.ocrinput.hide()
			self.ocrbutton.hide()

			if selectedText == "my project root":
					
				try:
					root = FreeCAD.activeDocument().Objects
					rootS = "FreeCAD.activeDocument().Objects"
					self.goDeeper("", rootS, root, "init")
				except:
					if self.gModeType == "matrix":
						self.showMsg("You need to release project first to enter the matrix ;-)")
					else:
						self.showMsg("You have to set active document (project) to use this root path.")

			if selectedText == "Module: FreeCAD":

				root = dir(FreeCAD)
				rootS = "FreeCAD"
				self.goDeeper(FreeCAD, rootS, root, "init")

			if selectedText == "Module: QtGui":

				from PySide import QtGui

				root = dir(QtGui)
				rootS = "QtGui"
				self.goDeeper(QtGui, rootS, root, "init")

			if selectedText == "Module: QtCore":

				from PySide import QtCore

				root = dir(QtCore)
				rootS = "QtCore"
				self.goDeeper(QtCore, rootS, root, "init")

			if selectedText == "Module: Part":

				import Part

				root = dir(Part)
				rootS = "Part"
				self.goDeeper(Part, rootS, root, "init")

			if selectedText == "Module: Path":

				import Path

				root = dir(Path)
				rootS = "Path"
				self.goDeeper(Path, rootS, root, "init")

			if selectedText == "Module: Draft":

				import Draft

				root = dir(Draft)
				rootS = "Draft"
				self.goDeeper(Draft, rootS, root, "init")

			if selectedText == "Module: TechDraw":

				import TechDraw

				root = dir(TechDraw)
				rootS = "TechDraw"
				self.goDeeper(TechDraw, rootS, root, "init")

			if selectedText == "Module: Spreadsheet":

				import Spreadsheet

				root = dir(Spreadsheet)
				rootS = "Spreadsheet"
				self.goDeeper(Spreadsheet, rootS, root, "init")

			if selectedText == "Module: coin":

				from pivy import coin

				root = dir(coin)
				rootS = "coin"
				self.goDeeper(coin, rootS, root, "init")

			if selectedText == "Module: MagicPanels":

				try:
					import MagicPanels

					root = dir(MagicPanels)
					rootS = "MagicPanels"
					self.goDeeper(MagicPanels, rootS, root, "init")
				
					self.setWindowsLayout("coding")
				
				except:
					self.showMsg("You need to install Woodworking workbench to see the MagicPanels API.")
				
			if selectedText == "custom module":
				self.orootlabel.show()
				self.orootcb.show()
				self.ocmlabel.show()
				self.ocminput.show()
				self.ocmbutton.show()
				
				self.ocrlabel.hide()
				self.ocrinput.hide()
				self.ocrbutton.hide()
				
			if selectedText == "custom command result":
				self.orootlabel.show()
				self.orootcb.show()
				self.ocrlabel.show()
				self.ocrinput.show()
				self.ocrbutton.show()
				
				self.ocmlabel.hide()
				self.ocminput.hide()
				self.ocmbutton.hide()

		# ############################################################################
		def setWindowsLayout(self, selectedText):

			if selectedText == "all windows":

				# options
				self.OPTsw.setGeometry(0, (3*self.gGridRow), (1*self.gGridCol), (2*self.gGridRow))
				self.OPTsw.show()

				# select
				self.swindow.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.swindow.show()
				self.slist.show()

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
			
			if selectedText == "coding":

				# options
				self.OPTsw.setGeometry(0, (3*self.gGridRow), (1*self.gGridCol), (2*self.gGridRow))
				self.OPTsw.show()

				# select
				self.swindow.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.swindow.show()
				self.slist.show()

				# dir
				self.o1sw.hide()
				self.o1.hide()

				# __dict__
				self.o2sw.hide()
				self.o2.hide()

				# __doc__
				self.o3sw.setGeometry((1*self.gGridCol), 0, (4*self.gGridCol), (4*self.gGridRow))
				self.o3sw.show()
				self.o3.show()

				# getAllDerivedFrom
				self.o4sw.hide()
				self.o4.hide()

				# content
				self.o5sw.hide()
				self.o5.hide()

				# object
				self.o6sw.setGeometry((1*self.gGridCol), (4*self.gGridRow), (4*self.gGridCol), (1*self.gGridRow))
				self.o6sw.show()
				self.o6.show()
				
			if selectedText == "modules":
				self.OPTsw.setGeometry(0, (3*self.gGridRow), (1*self.gGridCol), (2*self.gGridRow))
				self.OPTsw.show()
				self.swindow.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.swindow.show()
				self.slist.show()
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
				self.swindow.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.swindow.show()
				self.slist.show()

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
				self.swindow.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.swindow.show()
				self.slist.show()

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
				self.swindow.setGeometry(0, 0, (1*self.gGridCol), (3*self.gGridRow))
				self.swindow.show()
				self.slist.show()

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
				self.swindow.setGeometry(0, 0, (2*self.gGridCol), (3*self.gGridRow))
				self.swindow.show()
				self.slist.show()
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
				selectedText == "the Sun is free?" or
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
				
				if selectedText == "the Sun is free?":
					color1 = "#FFAA00"
					color2 = "#FFFFFF"
					color3 = "#FFAA00"
					
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
		def loadCustomModule(self):

			try:
				rootS = str(self.ocminput.text())

				module = __import__(rootS, globals(), locals(), [], 0)
				root = dir(module)

				self.clearDB()
				self.goDeeper(module, rootS, root, "init")

			except:

				if self.gModeType == "matrix":
					self.showMsg("This module is outside the matrix: "+rootS)
				else:
					self.showMsg("Can't load module: "+rootS)
		
		# ############################################################################
		def executeCustomCommand(self):
			try:
				command = self.ocrinput.text()
				result = eval(str(command))
	
				if isinstance(result, list):
					self.clearDB()
					self.goDeeper(result, command, result, "init")

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
		# actions - selection search filter
		# ############################################################################

		# ############################################################################
		def setFilter(self):
			
			try:
				self.slist.selectionModel().selectionChanged.disconnect()
				
				if self.slist.selectionModel().hasSelection():
					self.slist.selectionModel().clearSelection()
				
				search = str(self.sfilter.text())
				regExp = QtCore.QRegExp(search, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.Wildcard)
				self.sproxy.setFilterRegExp(regExp)
				
				self.slist.selectionModel().selectionChanged.connect(self.selectionChanged)

			except:
				if self.gModeType == "matrix":
					self.showMsg("This search is outside the matrix: "+str(self.sfilter.text()))
				else:
					self.showMsg("Search not possible: "+str(self.sfilter.text()))
		
		def cleanFilter(self):
			self.sfilter.setText("")
			
		# ############################################################################
		# actions - for keyboard keys
		# ############################################################################

		# ############################################################################
		def goDeeper(self, iObj, iLabel, iList, iType):

			tmpO = []
			tmpL = []

			# init selection view (compare strings only)
			if str(iObj) == "":
				tmpO = iList
				tmpL = [ o.Label for o in tmpO ]

			# if object is list (eg. faces, edges)
			elif isinstance(iObj, list):
				
				convert = 0
				
				i = 0
				for o in iObj:
					
					i = i + 1
					
					if str(o).find("Face") != -1:
						convert = 1
						tmpO.append(o)
						tmpL.append("Face"+str(i))
					
					if str(o).find("Edge") != -1:
						convert = 1
						tmpO.append(o)
						tmpL.append("Edge"+str(i))
				
					if str(o).find("Vertex") != -1:
						convert = 1
						tmpO.append(o)
						tmpL.append("Vertex"+str(i))
				
				if convert == 0:
					tmpO = iObj
					tmpL = iObj
				
				
			# other types
			else:
				for o in iList:
					
					try:
						if hasattr(iObj, o):
							tmpO.append(getattr(iObj, o))
							tmpL.append(str(o))
					except:
						skip = 1

			# not add empty lists (this stuck)
			if len(tmpO) > 0 and len(tmpL) > 0:

				self.setNewPage(iType)
				
				# update db
				self.dbObjects[self.dbPage] = tmpO
				self.dbLabels[self.dbPage] = tmpL
				self.dbPath[self.dbPage] = iLabel
				
				self.cleanFilter()
				self.updateSelection()

			else:
				if self.gModeType == "matrix":
					self.showMsg("This is the end of the rabbit hole. Go back quickly before you get lost ;-)", "info")
				else:
					self.showMsg("Can't parse this object structure deeper. Check deeper at the python console.", "info")

		# ############################################################################
		def goBack(self):

			# stop remove if there is only init
			if int(self.dbPage) > 0:

				# back page
				self.removeCurrentPage()
				self.updateSelection()
				
				# select row
				index = int(self.dbLastIndex[self.dbPage])
				index = self.smodel.index(index, 0)
				flag = QtCore.QItemSelectionModel.Select
				self.slist.selectionModel().setCurrentIndex(index, flag)
				
				# scroll to item
				flag = QtGui.QAbstractItemView.EnsureVisible.PositionAtCenter
				self.slist.scrollTo(index, flag)

				# reset outputs
				self.cleanFilter()
				self.resetOutputs()

		# ############################################################################
		def keyLeft(self):
			
			self.goBack()

		# ############################################################################
		def keyRight(self):

			try:
				if self.slist.selectionModel().hasSelection() == False:
					raise

				obj = self.getSelectionObject()
				label = self.getSelectionLabel()
				
				if isinstance(obj, str):
					raise
				elif isinstance(obj, float):
					raise
				elif isinstance(obj, list):
					newList = obj
					self.goDeeper(obj, label, newList, "next")
				else:
					try:
						newList = []
						for n in obj.getChildren():
							newList.append(n)
	
						self.goDeeper(newList, label, newList, "next")
					except:
						newList = dir(obj)
						self.goDeeper(obj, label, newList, "next")

			except:

				if self.gModeType == "matrix":
					self.showMsg("This is the end of the rabbit hole. Go back quickly before you get lost ;-)", "info")
				else:
					self.showMsg("Can't parse this object structure deeper. Check deeper at the python console.", "info")

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
