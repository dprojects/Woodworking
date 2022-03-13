# -*- coding: utf-8 -*-

# FreeCAD macro for spreadsheet export
# Author: Darek L (aka dprojects)
# Version: 2022.03.07
# Latest version: https://github.com/dprojects/sheet2export

import FreeCAD, Draft, Spreadsheet
from PySide import QtGui, QtCore

# ###################################################################################################################
# Main Settings ( CHANGE HERE IF NEEDED )
# ###################################################################################################################


# File type:
# "csv" - Comma-separated values (.csv file)
# "html" - HyperText Markup Language (.html file)
# "json" - JavaScript Object Notation (.json file), see e.g. json2table.com
# "md" - MarkDown (.md file), see e.g. dillinger.io
sFileType = "html"

# Export type:
# "a" - all spreadsheet objects
# "s" - selected spreadsheet only
sExportType = "a"

# File path:
# "~" - user home folder
# "./" - current macro folder
# or set Your custom path with write permissions
sFilePath = "./"


# ###################################################################################################################
# Additional Settings ( CHANGE HERE IF NEEDED )
# ###################################################################################################################


# Empty cell content:
if sFileType == "html":
	sEmptyCell = "&nbsp;"
else:
	sEmptyCell = ""

# Separator for CSV:
sSepCSV = ","

# custom CSS rules
sCustomCSS ="border-bottom:1px dotted #000000;"

# show Qt boxes
# "yes" - to show
# "no" - to hide
sQT = "yes"


# ###################################################################################################################
# Autoconfig - define globals ( NOT CHANGE HERE )
# ###################################################################################################################


# set reference point to Active Document
gAD = FreeCAD.activeDocument()

# get all objects from 3D model
gOBs = gAD.Objects

# init output file name
gFile = "result" # will be overwritten later

# init spreadsheet object
gSheet = gAD # will be overwritten later

# init output result
gOUT = ""

# exported files names
gExpFilesN = ""

# console print separator
gSepC = "\n ================================================================ \n"

# for cancel buttons assign "no"
gExecute = "yes"


# ###################################################################################################################
# Databases
# ###################################################################################################################


# cell properties
dbCPC = dict() # content
dbCPA = dict() # alignment
dbCPS = dict() # style
dbCPB = dict() # background
dbCPRS = dict() # row span
dbCPCS = dict() # column span

# max
dbMaxR = 0 # row
dbMaxC = 0 # column

# spreadsheet key
dbSKV = dict() # value for letters
dbSKL = dict() # letters for value


# ###################################################################################################################
# Support for Qt GUI
# ###################################################################################################################


# ###################################################################################################################
def showQtMain():

	global gExecute

	# ############################################################################
	# Qt Main Class
	# ############################################################################
	
	class QtMainClass(QtGui.QDialog):

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):
			
			# window
			self.result = userCancelled
			self.setGeometry(250, 250, 500, 350)
			self.setWindowTitle("sheet2export - default settings")
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# export type
			# ############################################################################

			# label
			self.eTypeL = QtGui.QLabel("Export type:", self)
			self.eTypeL.move(10, 13)
			
			# options
			self.eTypeList = ("a", "s")
			self.eTypeO = QtGui.QComboBox(self)
			self.eTypeO.addItems(self.eTypeList)
			self.eTypeO.setCurrentIndex(self.eTypeList.index("a"))
			self.eTypeO.activated[str].connect(self.setEType)
			self.eTypeO.move(100, 10)
			
			# info screen
			self.eTypeIS = QtGui.QLabel("all spreadsheets                  ", self)
			self.eTypeIS.move(145, 13)

			# ############################################################################
			# file path
			# ############################################################################

			# label
			self.fPathL = QtGui.QLabel("File path:", self)
			self.fPathL.move(10, 43)

			# text input
			self.fPathTi = QtGui.QLineEdit(self)
			self.fPathTi.setText(str(sFilePath))
			self.fPathTi.setFixedWidth(300)
			self.fPathTi.move(100, 40)

			# button
			self.fPathB = QtGui.QPushButton("...", self)
			self.fPathB.clicked.connect(self.loadCustomDir)
			self.fPathB.move(410, 40)

			# ############################################################################
			# file type
			# ############################################################################
			
			# label
			self.fileTypeL = QtGui.QLabel("File type:", self)
			self.fileTypeL.move(10, 73)
			
			# options
			self.fileTypeOlist = ("csv","html","json","md")
			self.fileTypeO = QtGui.QComboBox(self)
			self.fileTypeO.addItems(self.fileTypeOlist)
			self.fileTypeO.setCurrentIndex(self.fileTypeOlist.index("html"))
			self.fileTypeO.activated[str].connect(self.setFileType)
			self.fileTypeO.move(100, 70)

			# info screen
			self.fileTypeOIS = QtGui.QLabel("HyperText Markup Language (.html file)          ", self)
			self.fileTypeOIS.move(165, 73)

			# ############################################################################
			# empty cell
			# ############################################################################

			# label
			self.emptyCellL = QtGui.QLabel("Empty cell content:", self)
			self.emptyCellL.move(10, 143)

			# text input
			self.emptyCellTi = QtGui.QLineEdit(self)
			self.emptyCellTi.setText(str(sEmptyCell))
			self.emptyCellTi.setFixedWidth(100)
			self.emptyCellTi.move(140, 140)

			# ############################################################################
			# CSV separator
			# ############################################################################
			
			# label
			self.csvSL = QtGui.QLabel("Set CSV separator:", self)
			self.csvSL.move(10, 183)
			self.csvSL.hide()

			# text input
			self.csvSTi = QtGui.QLineEdit(self)
			self.csvSTi.setText(str(sSepCSV))
			self.csvSTi.setFixedWidth(100)
			self.csvSTi.move(140, 180)
			self.csvSTi.hide()

			# ############################################################################
			# custom CSS rules
			# ############################################################################

			# border label
			self.customCSSbl = QtGui.QLabel("Step 1. Border decoration:", self)
			self.customCSSbl.move(10, 193)

			# border options
			self.customCSSbol = ("no border","horizontal dotted","vertical solid",
						"normal solid", "strong solid", "3d effect")
			self.customCSSbo = QtGui.QComboBox(self)
			self.customCSSbo.addItems(self.customCSSbol)
			self.customCSSbo.setCurrentIndex(self.customCSSbol.index("horizontal dotted"))
			self.customCSSbo.activated[str].connect(self.setCustomCSSbo)
			self.customCSSbo.move(180, 190)

			# text input label
			self.customCSStil = QtGui.QLabel("Step 2. Custom CSS rules for each cell (edit or add):", self)
			self.customCSStil.move(10, 230)

			# text input
			self.customCSSti = QtGui.QLineEdit(self)
			self.customCSSti.setText(str(sCustomCSS))
			self.customCSSti.setFixedWidth(460)
			self.customCSSti.move(10, 250)

			# ############################################################################
			# buttons
			# ############################################################################

			# button - cancel
			cancelButton = QtGui.QPushButton('Cancel', self)
			cancelButton.clicked.connect(self.onCancel)
			cancelButton.setAutoDefault(True)
			cancelButton.move(120, 300)
			
			# button - ok
			okButton = QtGui.QPushButton('OK', self)
			okButton.clicked.connect(self.onOk)
			okButton.move(300, 300)

			# ############################################################################
			# show
			# ############################################################################

			self.show()


		# ############################################################################
		# actions
		# ############################################################################

		def loadCustomDir(self):
			sFilePath = str(QtGui.QFileDialog.getExistingDirectory())
			self.fPathTi.setText(sFilePath)
		
		def setFileType(self, selectedText):
			global sFileType

			sFileType = str(selectedText)

			if selectedText == "csv":
				self.fileTypeOIS.setText("Comma-separated values ( .csv file )")
				self.customCSSbl.hide()
				self.customCSSbo.hide()
				self.customCSStil.hide()
				self.customCSSti.hide()
				self.csvSL.show()
				self.csvSTi.show()
				self.emptyCellTi.setText("")

			if selectedText == "html":
				self.fileTypeOIS.setText("HyperText Markup Language ( .html file )")
				self.csvSL.hide()
				self.csvSTi.hide()
				self.customCSSbl.show()
				self.customCSSbo.show()
				self.customCSStil.show()
				self.customCSSti.show()
				self.emptyCellTi.setText(str(sEmptyCell))

			if selectedText == "json":
				self.fileTypeOIS.setText("JavaScript Object Notation ( .json file )")
				self.csvSL.hide()
				self.csvSTi.hide()
				self.customCSSbl.hide()
				self.customCSSbo.hide()
				self.customCSStil.hide()
				self.customCSSti.hide()
				self.emptyCellTi.setText("")

			if selectedText == "md":
				self.fileTypeOIS.setText("MarkDown ( .md file )")
				self.csvSL.hide()
				self.csvSTi.hide()
				self.customCSSbl.hide()
				self.customCSSbo.hide()
				self.customCSStil.hide()
				self.customCSSti.hide()
				self.emptyCellTi.setText("")

		def setEType(self, selectedText):
			global sExportType

			if selectedText == "a":
				sExportType = "a"
				self.eTypeIS.setText("all spreadsheets")
			if selectedText == "s":
				sExportType = "s"
				self.eTypeIS.setText("selected spreadsheet only")

		def setCustomCSSbo(self, selectedText):
			global sCustomCSS

			if selectedText == "no border":
				sCustomCSS = "border:0px dotted #000000;"
				self.customCSSti.setText(str(sCustomCSS))
			if selectedText == "horizontal dotted":
				sCustomCSS = "border-bottom:1px dotted #000000;"
				self.customCSSti.setText(str(sCustomCSS))
			if selectedText == "vertical solid":
				sCustomCSS = "border-left:1px solid #000000;"
				self.customCSSti.setText(str(sCustomCSS))
			if selectedText == "normal solid":
				sCustomCSS = "border:1px solid #000000;"
				self.customCSSti.setText(str(sCustomCSS))
			if selectedText == "strong solid":
				sCustomCSS = "border:3px solid #D1D1D1;"
				self.customCSSti.setText(str(sCustomCSS))
			if selectedText == "3d effect":
				sCustomCSS = "border-bottom:5px solid #D1D1D1;"
				sCustomCSS += "border-right:1px solid #D1D1D1;"
				sCustomCSS += "padding:5px 10px;"
				self.customCSSti.setText(str(sCustomCSS))

		def onCancel(self):
			self.result = userCancelled
			self.close()
		def onOk(self):
			self.result = userOK
			self.close()
	
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		gExecute = "no"
		pass
	
	if form.result == userOK:
		global sCustomCSS
		global sSepCSV
		global sEmptyCell
		global sFilePath

		sCustomCSS = form.customCSSti.text()
		sSepCSV = form.csvSTi.text()
		sEmptyCell = form.emptyCellTi.text()
		sFilePath = form.fPathTi.text()


# ###################################################################################################################
# Support for errors and info
# ###################################################################################################################


# ###################################################################################################################
def showInfo(iText):

	if sQT == "yes":

		QtGui.QMessageBox.information(None,"sheet2export",str(iText))

	else:
		FreeCAD.Console.PrintMessage(gSepC)
		FreeCAD.Console.PrintMessage(str(iText))
		FreeCAD.Console.PrintMessage(gSepC)
	
	return 0


# ###################################################################################################################
def showError(iObj, iPlace, iError):

	FreeCAD.Console.PrintMessage(gSepC)
	
	try:
		FreeCAD.Console.PrintMessage("ERROR: ")
		FreeCAD.Console.PrintMessage(" | ")
		FreeCAD.Console.PrintMessage(str(iObj.Label))
		FreeCAD.Console.PrintMessage(" | ")
		FreeCAD.Console.PrintMessage(str(iPlace))
		FreeCAD.Console.PrintMessage(" | ")
		FreeCAD.Console.PrintMessage(str(iError))
		
	except:
		FreeCAD.Console.PrintMessage("FATAL ERROR, or even worse :-)")
		
	FreeCAD.Console.PrintMessage(gSepC)
	
	return 0


# ###################################################################################################################
# CSV file format ( COPY AND CHANGE TO ADD NEW FILE FORMAT )
# ###################################################################################################################


# ###################################################################################################################
def CSVbegin():
	global gOUT

	gOUT += ''


# ###################################################################################################################
def CSVend():
	global gOUT

	gOUT += ''


# ###################################################################################################################
def CSVrowOpen():
	global gOUT

	gOUT += ''


# ###################################################################################################################
def CSVrowClose():
	global gOUT

	gOUT += '\n'


# ###################################################################################################################
def CSVempty(iKey, iC, iR):
	global gOUT

	gOUT += str(sEmptyCell)
	gOUT += sSepCSV


# ###################################################################################################################
def CSVcell(iKey, iCell, iC, iR):
	global gOUT

	gOUT += str(iCell)
	gOUT += sSepCSV


# ###################################################################################################################
# HTML file format
# ###################################################################################################################


# ###################################################################################################################
def HTMLbegin():
	global gOUT

	# there is no need to add html document header here because if the file is html table 
	# only the file is correctly parsed by browser, moreover this is easier to copy the 
	# file content and place it to the post or other web page
	gOUT += '<TABLE>\n'


# ###################################################################################################################
def HTMLend():
	global gOUT

	gOUT += "</TABLE>"


# ###################################################################################################################
def HTMLrowOpen():
	global gOUT

	gOUT += " <TR>\n"


# ###################################################################################################################
def HTMLrowClose():
	global gOUT

	gOUT += " </TR>\n"


# ###################################################################################################################
def HTMLempty(iKey, iC, iR):
	global gOUT

	gOUT += '  <TD '

	try:
		gOUT += 'colspan="'+str(dbCPCS[iKey]) + '" '
	except:
		gOUT += ''

	try:
		gOUT += 'rowspan="'+str(dbCPRS[iKey]) + '" '
	except:
		gOUT += ''

	gOUT += 'style=' 
	gOUT += '"'
	gOUT += str(sCustomCSS)
	
	try:
		gOUT += 'text-align:'+str(dbCPA[iKey]).split("|")[0] + ';'
	except:
		gOUT += ''
	
	try:
		gOUT += 'background-color:'+str(dbCPB[iKey]) + ';'
	except:
		gOUT += ''
	
	try:
		gOUT += 'font-weight:'+str(dbCPS[iKey]) + ';'
	except:
		gOUT += ''
	

	gOUT += '"'
	gOUT += '>'
	gOUT += str(sEmptyCell)
	gOUT += "</TD>\n"


# ###################################################################################################################
def HTMLcell(iKey, iCell, iC, iR):
	global gOUT

	gOUT += '  <TD '

	try:
		gOUT += 'colspan="'+str(dbCPCS[iKey]) + '" '
	except:
		gOUT += ''

	try:
		gOUT += 'rowspan="'+str(dbCPRS[iKey]) + '" '
	except:
		gOUT += ''

	gOUT += 'style=' 
	gOUT += '"'
	gOUT += str(sCustomCSS)
	
	try:
		gOUT += 'text-align:'+str(dbCPA[iKey]).split("|")[0] + ';'
	except:
		gOUT += ''
	
	try:
		gOUT += 'background-color:'+str(dbCPB[iKey]) + ';'
	except:
		gOUT += ''
	
	try:
		gOUT += 'font-weight:'+str(dbCPS[iKey]) + ';'
	except:
		gOUT += ''
	

	gOUT += '"'
	gOUT += '>'
	gOUT += str(iCell)
	gOUT += "</TD>\n"


# ###################################################################################################################
# JSON file format
# ###################################################################################################################


# ###################################################################################################################
def JSONbegin():
	global gOUT

	gOUT += '['


# ###################################################################################################################
def JSONend():
	global gOUT

	gOUT = gOUT[:-1]
	gOUT += ']'


# ###################################################################################################################
def JSONrowOpen():
	global gOUT

	gOUT += '{'


# ###################################################################################################################
def JSONrowClose():
	global gOUT

	gOUT = gOUT[:-1]
	gOUT += '},'


# ###################################################################################################################
def JSONempty(iKey, iC, iR):
	global gOUT

	key = str(dbSKL[str(iC)])
	gOUT += '"' + str(key) + '":'
	gOUT += '"' + str(sEmptyCell) + '"'
	gOUT += ','


# ###################################################################################################################
def JSONcell(iKey, iCell, iC, iR):
	global gOUT

	key = str(dbSKL[str(iC)])
	gOUT += '"' + str(key) + '":'
	gOUT += '"' + str(iCell) + '"'
	gOUT += ','


# ###################################################################################################################
# MarkDown file format
# ###################################################################################################################


# ###################################################################################################################
def MDbegin():
	global gOUT

	c = 1
	while c < dbMaxC + 1:
		gOUT += '|   '
		c = c + 1

	gOUT += '|\n'

	c = 1
	while c < dbMaxC + 1:

		# set alignment
		try:	

			# check 2nd row with data
			# first row can be header with colspans
			key = str(dbSKL[str(c)]) + str(2)
			a = str(dbCPA[key]).split("|")[0]

			if a == "left":
				gOUT += '|:--'
			if a == "right":
				gOUT += '|--:'
			if a == "center":
				gOUT += '|:-:'
		except:
			gOUT += '|---'

		c = c + 1

	gOUT += '|\n'


# ###################################################################################################################
def MDend():
	global gOUT

	gOUT += ''


# ###################################################################################################################
def MDrowOpen():
	global gOUT

	gOUT += ''


# ###################################################################################################################
def MDrowClose():
	global gOUT

	gOUT += '|'
	gOUT += '\n'


# ###################################################################################################################
def MDempty(iKey, iC, iR):
	global gOUT

	gOUT += '|   '
	gOUT += str(sEmptyCell)


# ###################################################################################################################
def MDcell(iKey, iCell, iC, iR):
	global gOUT

	gOUT += '|   '
	gOUT += str(iCell)
	gOUT += '   '


# ###################################################################################################################
# Database write controller
# ###################################################################################################################


# ###################################################################################################################
def getKey(iC, iR):

	letters = "ZABCDEFGHIJKLMNOPQRSTUVWXYZ" # max 26

	mod = int((iC % 26))
	div = int((iC - 1) / 26) 

	keyC = ""

	if iC < 27:
		keyC = letters[iC]
	else:
		keyC = letters[div] + letters[mod]

	keyR = str(iR)

	key = keyC + keyR

	# for given column and row it returns
	# spreadsheet key for cell like e.g. A5, AG125 etc
	return str(key)


# ###################################################################################################################
def setSK():

	# set spreadsheet keys databases
	c = 1
	while c < 703:

		# get key for first row and remove number
		key = getKey(c, 1)[:-1]
		
		# set spreadsheet key value
		dbSKV[key] = c

		# set spreadsheet key letter
		dbSKL[str(c)] = key

		# go to next column
		c = c + 1


# ###################################################################################################################
def setDB():

	# import regular expressions
	import re

	# refer to globals
	global dbMaxR
	global dbMaxC
	
	# XML parse part from python doc
	import xml.etree.ElementTree as ET
	result = str(gSheet.cells.Content)
	root = ET.fromstring(result)

	# set only available data
	for child in root:
		root2 = dict(child.attrib)
		
		# skip data not related to cells
		try:
			key = root2["address"]
		except:
			continue

		try:
			# the XML parse may not be consistent with the FreeCAD spreadsheet objects,
			# the XML may contains extra characters like "=" or '' so you have to write 
			# the FreeCAD content not the XML content with the extra characters
			dbCPC[key] = gSheet.get(key)
		except:
			skip = 1

		try:
			dbCPA[key] = root2["alignment"]
		except:
			skip = 1

		try:
			dbCPS[key] = root2["style"]
		except:
			skip = 1

		try:
			dbCPB[key] = root2["backgroundColor"]
		except:
			skip = 1

		try:
			dbCPRS[key] = root2["rowSpan"]
		except:
			skip = 1

		try:
			dbCPCS[key] = root2["colSpan"]
		except:
			skip = 1

		# width is not set because web pages and other formats has its own 
		# page size, for advance science data the spreadsheet can be even 
		# for ZZ column, so its not make any sense to recalculate it, 
		# width of column should be in auto mode, as small as possible 
		# but keep the text readable and possible to print, 
		# columns can be adjusted manually if needed

	# set max row and max column
	# search keys in content db
	for k in dbCPC.keys():
		
		# split spreadsheet key to word and number
		res = [re.findall(r'(\w+?)(\d+)', str(k))[0] ]

		w = str(res[0][0]) # word column
		n = int(res[0][1]) # number rows
		
		if int(dbSKV[w]) > int(dbMaxC):
			dbMaxC = int(dbSKV[w])
		
		if int(n) > int(dbMaxR):
			dbMaxR = int(n)

	# search keys also in background db
	# this can be page separator line using background color
	for k in dbCPB.keys():
		
		# split spreadsheet key to word and number
		res = [re.findall(r'(\w+?)(\d+)', str(k))[0] ]

		w = str(res[0][0]) # word column
		n = int(res[0][1]) # number rows
		
		if int(dbSKV[w]) > int(dbMaxC):
			dbMaxC = int(dbSKV[w])
		
		if int(n) > int(dbMaxR):
			dbMaxR = int(n)
	

# ###################################################################################################################
def resetDB():

	# reset db
	global dbCPC
	global dbCPA
	global dbCPS
	global dbCPB
	global dbCPRS
	global dbCPCS

	dbCPC.clear() # content
	dbCPA.clear() # alignment
	dbCPS.clear() # style
	dbCPB.clear() # background
	dbCPRS.clear() # row span
	dbCPCS.clear() # column span

	# reset output
	global gOUT

	gOUT = ""

	# max
	global dbMaxR
	global dbMaxC

	dbMaxR = 0 # row
	dbMaxC = 0 # column


# ###################################################################################################################
# File format selector
# ###################################################################################################################


# ###################################################################################################################
def selectBegin():

	if sFileType == "csv":
		CSVbegin()

	if sFileType == "html":
		HTMLbegin()

	if sFileType == "json":
		JSONbegin()

	if sFileType == "md":
		MDbegin()


# ###################################################################################################################
def selectEnd():

	if sFileType == "csv":
		CSVend()

	if sFileType == "html":
		HTMLend()

	if sFileType == "json":
		JSONend()

	if sFileType == "md":
		MDend()


# ###################################################################################################################
def selectRowOpen():

	if sFileType == "csv":
		CSVrowOpen()

	if sFileType == "html":
		HTMLrowOpen()

	if sFileType == "json":
		JSONrowOpen()

	if sFileType == "md":
		MDrowOpen()


# ###################################################################################################################
def selectRowClose():

	if sFileType == "csv":
		CSVrowClose()

	if sFileType == "html":
		HTMLrowClose()

	if sFileType == "json":
		JSONrowClose()

	if sFileType == "md":
		MDrowClose()


# ###################################################################################################################
def selectEmpty(iKey, iC, iR):

	if sFileType == "csv":
		CSVempty(iKey, iC, iR)

	if sFileType == "html":
		HTMLempty(iKey, iC, iR)

	if sFileType == "json":
		JSONempty(iKey, iC, iR)

	if sFileType == "md":
		MDempty(iKey, iC, iR)


# ###################################################################################################################
def selectCell(iKey, iCell, iC, iR):

	if sFileType == "csv":
		CSVcell(iKey, iCell, iC, iR)

	if sFileType == "html":
		HTMLcell(iKey, iCell, iC, iR)

	if sFileType == "json":
		JSONcell(iKey, iCell, iC, iR)

	if sFileType == "md":
		MDcell(iKey, iCell, iC, iR)


# ###################################################################################################################
# Set output
# ###################################################################################################################


# ###################################################################################################################
def setOUTPUT():

	if sQT == "yes":
		if int(dbMaxR * dbMaxC) > 100000:

			info = "The spreadsheet "+str(gSheet.Label)+" has: \n\n"
			info += str(dbMaxC) + " columns \n"
			info += str(dbMaxR) + " rows. \n"
			info += "\n"
			info += "This may take several minutes to export file. "
			info += "\n"
			info += "Would you like to wait (ok) or skip (cancel) the spreadsheet?\t\t"
			info += "\n\n"
			reply = QtGui.QMessageBox.question(None, "", str(info), 
				QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			
			if reply == QtGui.QMessageBox.Yes:
				skip = 0

			if reply == QtGui.QMessageBox.No:
				skip = 1
				return -1
	
	# set begin of the spreadsheet table
	selectBegin()
	
	# set variables for loop
	colSpan = 0
	rowSpan = 0
	vCell = ""
	c = 1
	r = 1
	
	# just simple walk thru the matrix and setting each cell
	while r <= dbMaxR:

		FreeCAD.Console.PrintMessage(".")
		FreeCAD.Console.PrintMessage("")

		# set row extra properties
		selectRowOpen()
		
		# go thru columns for given row
		while c <= dbMaxC:

			# get access point
			vKey = str(dbSKL[str(c)]) + str(r)

			try:

				# get content
				vCell = str(dbCPC[vKey])

				# set colspan before you set the cell
				try:
					colSpan = int(dbCPCS[vKey])
					rowSpan = int(dbCPRS[vKey])
				except:
					skip = 1

				# set the cell content
				if vCell != "":
					selectCell(vKey, vCell, c, r)					
				else:
					selectEmpty(vKey, c, r)

			except:

				# if there was no such cell access point it will be empty cell
				# if there is open colspan this should be skipped
				if sFileType == "html":
					if colSpan == 0 or  rowSpan == 0:
						selectEmpty(vKey, c, r)

				# colspan is not supported by the file type
				else:
					selectEmpty(vKey, c, r)

			# if the cell was written and there is colspan open
			if colSpan > 0:
				colSpan = colSpan - 1 
		
			# just go to next column
			c = c + 1

		# add extra close row properties
		selectRowClose()
		
		if rowSpan > 0:
			rowSpan = rowSpan - 1 		

		# set variables for next row
		c = 1
		r = r + 1

	# set end of the spreadsheet table
	selectEnd()

	# set info
	FreeCAD.Console.PrintMessage("done.")


# ###################################################################################################################
# Save spreadsheet data to file
# ###################################################################################################################


# ###################################################################################################################
def saveToDisk():

	global gExpFilesN

	import os, sys
	from os.path import expanduser
	
	vRoot = expanduser(sFilePath)
	vFileName = str(gFile) + "." + str(sFileType)
	vFile = os.path.join(vRoot, vFileName)
	
	with open(vFile, 'w') as vFH:
		vFH.write("%s" % gOUT)

	gExpFilesN += vFile + "\t\n"


# ###################################################################################################################
# MAIN TASKS
# ###################################################################################################################

# ###################################################################################################################
def runTasks():

	try:
		setDB()
	except:
		showError(gSheet, "setDB" , "Databese is not set correctly.")
		
	try:
		if setOUTPUT() == -1:
			return 0
	except:
		showError(gSheet, "setOUTPUT" , "Output is not set correctly.")
		
	try:	
		saveToDisk()
	except:
		showError(gSheet, "saveToDisk" , "File is not exported correctly.")


# ###################################################################################################################
# MAIN
# ###################################################################################################################


# show Qt box
if sQT == "yes":
	showQtMain()

# skip if cancel button
if gExecute == "yes":

	# set spreadsheet key databases
	try:
		setSK()
	except:
		showError(gAD, "setSK" , "Spreadsheet key databases is not set correctly.")
	
	# for selected
	if sExportType == "s":
		try:
			# try set selected spreadsheet
			gSheet = FreeCADGui.Selection.getSelection()[0]

			# check if this is correct spreadsheet object
			if gSheet.isDerivedFrom("Spreadsheet::Sheet"):
		
				# set output filename
				gFile = gAD.Label + " - " + gSheet.Label
		
				# set info
				FreeCAD.Console.PrintMessage("\n")
				FreeCAD.Console.PrintMessage("Exporting: ")
				FreeCAD.Console.PrintMessage(gSheet.Label + " ")
		
				# create output file
				runTasks()
	
				# info
				showInfo("Exported files: \n\n"+str(gExpFilesN)+"\n\n")	
			else:
				showInfo("Please select spreadsheet to export.")
		except:
			showInfo("Please select spreadsheet to export.")
	
		
	# for all spreadsheets
	elif sExportType == "a":
	
		# search all objects and export spreadsheets
		for obj in gOBs:
	
			# try set spreadsheet
			gSheet = obj
	
			# check if this is correct spreadsheet object
			if gSheet.isDerivedFrom("Spreadsheet::Sheet"):
	
					# set output filename
				gFile = gAD.Label + " - " + gSheet.Label
			else:
				continue
	
			# set info
			FreeCAD.Console.PrintMessage("\n")
			FreeCAD.Console.PrintMessage("Exporting: ")
			FreeCAD.Console.PrintMessage(gSheet.Label + " ")
			
			# create output file
			resetDB()
			runTasks()

		# info
		showInfo("Exported files: \n\n"+str(gExpFilesN)+"\n\n")
	else:
		showError(gAD, "main", "Please set sExportType correctly.")


# ###################################################################################################################