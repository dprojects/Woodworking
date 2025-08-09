# ###################################################################################################################
'''

FreeCAD macro for spreadsheet export
Author: Darek L (github.com/dprojects)
Latest version: https://github.com/dprojects/sheet2export

Certified platform:
https://github.com/dprojects/Woodworking

'''
# ###################################################################################################################


import FreeCAD, FreeCADGui, Draft, Spreadsheet
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate


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
			
			# ############################################################################
			# set screen
			# ############################################################################
			
			# tool screen size
			toolSW = 400
			toolSH = 400
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('sheet2export', 'sheet2export'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			
			self.setMinimumWidth(toolSW)
			self.setMinimumHeight(toolSH)

			# ############################################################################
			# export type
			# ############################################################################

			self.eTypeL = QtGui.QLabel(translate('sheet2export', 'Export type:'), self)
			
			self.eTypeList = ("a", "s")
			self.eTypeO = QtGui.QComboBox(self)
			self.eTypeO.addItems(self.eTypeList)
			self.eTypeO.setCurrentIndex(self.eTypeList.index("a"))
			self.eTypeO.textActivated[str].connect(self.setEType)
			self.eTypeO.setFixedSize(80, 20)
			
			self.eTypeIS = QtGui.QLabel(translate('sheet2export', 'all spreadsheets'), self)
			
			# ############################################################################
			# file path
			# ############################################################################

			self.fPathL = QtGui.QLabel(translate('sheet2export', 'Export file path:'), self)
			
			self.fPathTi = QtGui.QLineEdit(self)
			self.fPathTi.setText(str(sFilePath))
			self.fPathTi.setFixedWidth(250)
			
			self.fPathB = QtGui.QPushButton("...", self)
			self.fPathB.clicked.connect(self.loadCustomDir)
			
			# ############################################################################
			# file type
			# ############################################################################
			
			self.fileTypeL = QtGui.QLabel(translate('sheet2export', 'Export file type:'), self)
			
			self.fileTypeOlist = ("csv","html","json","md")
			self.fileTypeO = QtGui.QComboBox(self)
			self.fileTypeO.addItems(self.fileTypeOlist)
			self.fileTypeO.setCurrentIndex(self.fileTypeOlist.index("html"))
			self.fileTypeO.textActivated[str].connect(self.setFileType)
			self.fileTypeO.setFixedSize(80, 20)
			
			self.fileTypeOIS = QtGui.QLabel(translate('sheet2export', 'HyperText Markup Language (.html file)'), self)
			
			# ############################################################################
			# empty cell
			# ############################################################################

			self.emptyCellL = QtGui.QLabel(translate('sheet2export', 'Empty cell content:'), self)
			
			self.emptyCellTi = QtGui.QLineEdit(self)
			self.emptyCellTi.setText(str(sEmptyCell))
			
			# ############################################################################
			# CSV separator
			# ############################################################################
			
			self.csvSL = QtGui.QLabel(translate('sheet2export', 'Set CSV separator:'), self)
			
			self.csvSTi = QtGui.QLineEdit(self)
			self.csvSTi.setText(str(sSepCSV))
			
			# ############################################################################
			# custom CSS rules
			# ############################################################################

			# border label
			self.customCSSbl = QtGui.QLabel(translate('sheet2export', 'Step 1. Border decoration:'), self)

			# border options
			self.customCSSbol = ("no border","horizontal dotted","vertical solid",
						"normal solid", "strong solid", "3d effect")
			self.customCSSbo = QtGui.QComboBox(self)
			self.customCSSbo.addItems(self.customCSSbol)
			self.customCSSbo.setCurrentIndex(self.customCSSbol.index("horizontal dotted"))
			self.customCSSbo.textActivated[str].connect(self.setCustomCSSbo)

			# text input label
			self.customCSStil = QtGui.QLabel(translate('sheet2export', 'Step 2. Custom CSS rules for each cell (edit or add):'), self)

			# text input
			self.customCSSti = QtGui.QLineEdit(self)
			self.customCSSti.setText(str(sCustomCSS))
			self.customCSSti.setFixedWidth(460)

			# ############################################################################
			# buttons
			# ############################################################################
			
			# button - ok
			self.okButton = QtGui.QPushButton(translate('sheet2export', 'create'), self)
			self.okButton.clicked.connect(self.onOk)
			self.okButton.setFixedHeight(40)

			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.body1 = QtGui.QHBoxLayout()
			self.body1.setAlignment(QtGui.Qt.AlignLeft)
			self.body1.addWidget(self.eTypeL)
			self.body1.addWidget(self.eTypeO)
			self.body1.addWidget(self.eTypeIS)
			self.body2 = QtGui.QHBoxLayout()
			self.body2.setAlignment(QtGui.Qt.AlignLeft)
			self.body2.addWidget(self.fPathL)
			self.body2.addWidget(self.fPathTi)
			self.body2.addWidget(self.fPathB)
			self.body3 = QtGui.QHBoxLayout()
			self.body3.setAlignment(QtGui.Qt.AlignLeft)
			self.body3.addWidget(self.fileTypeL)
			self.body3.addWidget(self.fileTypeO)
			self.body3.addWidget(self.fileTypeOIS)
			self.lay1 = QtGui.QVBoxLayout()
			self.lay1.addLayout(self.body1)
			self.lay1.addLayout(self.body2)
			self.lay1.addLayout(self.body3)
			self.groupBody1 = QtGui.QGroupBox(None, self)
			self.groupBody1.setLayout(self.lay1)
			
			self.body4 = QtGui.QHBoxLayout()
			self.body4.addWidget(self.emptyCellL)
			self.body4.addWidget(self.emptyCellTi)
			self.body5 = QtGui.QHBoxLayout()
			self.body5.addWidget(self.csvSL)
			self.body5.addWidget(self.csvSTi)
			self.body6 = QtGui.QHBoxLayout()
			self.body6.addWidget(self.customCSSbl)
			self.body6.addWidget(self.customCSSbo)
			self.body7 = QtGui.QVBoxLayout()
			self.body7.addWidget(self.customCSStil)
			self.body7.addWidget(self.customCSSti)
			self.lay2 = QtGui.QVBoxLayout()
			self.lay2.addLayout(self.body4)
			self.lay2.addLayout(self.body5)
			self.lay2.addSpacing(20)
			self.lay2.addLayout(self.body6)
			self.lay2.addLayout(self.body7)
			self.groupBody2 = QtGui.QGroupBox(None, self)
			self.groupBody2.setLayout(self.lay2)
			
			self.body8 = QtGui.QHBoxLayout()
			self.body8.addWidget(self.okButton)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			self.layout.addWidget(self.groupBody1)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody2)
			self.layout.addStretch()
			self.layout.addLayout(self.body8)
			self.setLayout(self.layout)

			# hide
			self.csvSL.hide()
			self.csvSTi.hide()

			# ############################################################################
			# show
			# ############################################################################

			self.show()

			# set window position
			sw = self.width()
			sh = self.height()
			pw = int( (FreeCADGui.getMainWindow().width() / 2) - ( sw / 2 ) )
			ph = int( (FreeCADGui.getMainWindow().height() / 2) - ( sh / 2 ) )
			self.setGeometry(pw, ph, sw, sh)
			
			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)
				
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
				self.fileTypeOIS.setText(translate('sheet2export', 'Comma-separated values ( .csv file )'))
				self.customCSSbl.hide()
				self.customCSSbo.hide()
				self.customCSStil.hide()
				self.customCSSti.hide()
				self.csvSL.show()
				self.csvSTi.show()
				self.emptyCellTi.setText("")

			if selectedText == "html":
				self.fileTypeOIS.setText(translate('sheet2export', 'HyperText Markup Language ( .html file )'))
				self.csvSL.hide()
				self.csvSTi.hide()
				self.customCSSbl.show()
				self.customCSSbo.show()
				self.customCSStil.show()
				self.customCSSti.show()
				self.emptyCellTi.setText(str(sEmptyCell))

			if selectedText == "json":
				self.fileTypeOIS.setText(translate('sheet2export', 'JavaScript Object Notation ( .json file )'))
				self.csvSL.hide()
				self.csvSTi.hide()
				self.customCSSbl.hide()
				self.customCSSbo.hide()
				self.customCSStil.hide()
				self.customCSSti.hide()
				self.emptyCellTi.setText("")

			if selectedText == "md":
				self.fileTypeOIS.setText(translate('sheet2export', 'MarkDown ( .md file )'))
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
				self.eTypeIS.setText(translate('sheet2export', 'all spreadsheets'))
			if selectedText == "s":
				sExportType = "s"
				self.eTypeIS.setText(translate('sheet2export', 'selected spreadsheet only'))

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

		QtGui.QMessageBox.information(None, translate('sheet2export', 'sheet2export'), str(iText))

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
		if int(dbMaxR * dbMaxC) > 10000:

			info = ""
			info += translate('sheet2export', 'The spreadsheet') + ' ' + str(gSheet.Label)
			info += ' ' + translate('sheet2export', 'has') + ':' + ' ' + '\n\n'
			info += str(dbMaxC) + ' ' + translate('sheet2export', 'columns') + '\n'
			info += str(dbMaxR) + ' ' + translate('sheet2export', 'rows') + '\n'
			info += "\n"
			info += translate('sheet2export', 'This may take several minutes to export file.')
			info += "\n"
			info += translate('sheet2export', 'Would you like to wait (ok) or skip (cancel) the spreadsheet?') + '\t\t'
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
					if colSpan == 0 or rowSpan == 0:
						selectEmpty(vKey, c, r)

				# colspan is not supported by the file type
				else:
					selectEmpty(vKey, c, r)

			# fix if there is empty row separator
			if sFileType == "html":
				cls = ""
				try:
					cls = int(dbCPCS[vKey])
				except:
					skip = 1
				
				if cls == int(dbMaxC):
					c = int(dbMaxC)
					
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
				info = ""
				info += translate('sheet2export', 'Exported files')
				info += ": \n\n" + str(gExpFilesN) + "\n\n"
				showInfo(info)
			else:
				showInfo(translate('sheet2export', 'Please select spreadsheet to export.'))
		except:
			showInfo(translate('sheet2export', 'Please select spreadsheet to export.'))
	
		
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
		info = ""
		info += translate('sheet2export', 'Exported files')
		info += ": \n\n" + str(gExpFilesN) + "\n\n"
		showInfo(info)
	else:
		showError(gAD, "main", "Please set sExportType correctly.")


# ###################################################################################################################
