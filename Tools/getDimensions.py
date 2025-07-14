# ###################################################################################################################
'''

FreeCAD macro to get chipboards dimensions to cut
Author: Darek L (github.com/dprojects)
Latest version: https://github.com/dprojects/getDimensions

Certified platform:
https://github.com/dprojects/Woodworking

'''
# ###################################################################################################################


import FreeCAD, FreeCADGui, Draft, Spreadsheet
from PySide import QtGui, QtCore

translate = FreeCAD.Qt.translate


gKernelVersion = 0
try:
	gKernelVersion = float( str(FreeCAD.Version()[0]) + "." + str(FreeCAD.Version()[1]) + str(FreeCAD.Version()[2]) )
except:
	skip = 1


# ###################################################################################################################
#
# 				Default Settings
#		Qt GUI gets from here to avoid inconsistency
#
# 			CHANGE ONLY HERE IF NEEDED
#
# ###################################################################################################################


# Languages:
sLang = "en"
sLangDsc = { 
	"en" : translate("getDimensions", "English language"), 
	"pl" : translate("getDimensions", "Polish language") # no comma
}

# Report print quality:
sRPQ = "hq"
sRPQDsc = {
	"eco" : translate("getDimensions", "low ink mode (good for printing)"),
	"hq" : translate("getDimensions", "high quality mode (good for pdf or html export)") # no comma
}

# Visibility (Toggle Visibility Feature):
sTVF = "off"
sTVFDsc = {
	"off" : translate("getDimensions", "normal mode, show and calculate all objects and groups"),
	"on" : translate("getDimensions", "simple mode, not show hidden objects for simple structures"),
	"edge" : translate("getDimensions", "simple edge mode, show all but not add hidden to the edge size"),
	"parent" : translate("getDimensions", "simple nesting, inherit visibility from the nearest container"),
	"inherit" : translate("getDimensions", "advanced nesting, inherit visibility from the highest container") # no comma
}

# Part Cut Visibility:
sPartCut = "all"
sPartCutDsc = {
	"all" : translate("getDimensions", "Woodworking workbench approach, show Base and Tool"),
	"base" : translate("getDimensions", "FreeCAD default approach, show Base only"),
	"tool" : translate("getDimensions", "custom approach, show Tool only") # no comma
}

# Parse path mode
sPPM = "default"
sPPMDsc = {
	"default" : translate("getDimensions", "normal mode"),
	"assembly" : translate("getDimensions", "dedicated for Assembly workbench objects") # no comma
}

# Report customization (Label Type Feature):
sLTF = "q"
sLTFDsc = {
	"q" : translate("getDimensions", "quick, quantity first"),
	"n" : translate("getDimensions", "names, objects listing"),
	"g" : translate("getDimensions", "group, grandparent or parent folder name first"),
	"e" : translate("getDimensions", "edgeband, extended edge"),
	"d" : translate("getDimensions", "detailed, edgeband, drill holes, countersinks"),
	"c" : translate("getDimensions", "constraints names, totally custom report"),
	"p" : translate("getDimensions", "pads, show list of all constraints"),
	"a" : translate("getDimensions", "approximation for cutlistoptimizer.com") # no comma
}

# Units for dimensions:
sUnitsMetric = "mm"
sUnitsMetricDsc = {
	"mm" : translate("getDimensions", "millimeter"),
	"m" : translate("getDimensions", "meter"),
	"in" : translate("getDimensions", "inch") # no comma
}

# Units for area:
sUnitsArea = "m"
sUnitsAreaDsc = {
	"m" : translate("getDimensions", "square meter (m2)"),
	"mm" : translate("getDimensions", "square millimeter (mm2)"),
	"in" : translate("getDimensions", "square inch (in2)") # no comma
}

# Units for edge size:
sUnitsEdge = "m"
sUnitsEdgeDsc = {
	"mm" : translate("getDimensions", "millimeter"),
	"m" : translate("getDimensions", "meter"),
	"in" : translate("getDimensions", "inch") # no comma
}

# Precision Defaults - Dimensions (d)
sPrecisionDD = {
	"mm" : 0,
	"m" : 3,
	"in" : 3 # no comma
}
sPDD = sPrecisionDD[sUnitsMetric]

# Precision Defaults - Edge
sPrecisionDE = {
	"mm" : 0,
	"m" : 3,
	"in" : 3 # no comma
}
sPDE = sPrecisionDE[sUnitsEdge]

# Precision Defaults - Area
sPrecisionDA = {
	"mm" : 0,
	"m" : 6,
	"in" : 6 # no comma
}
sPDA = sPrecisionDA[sUnitsArea]

# Edgeband code:
sEColorD = "PL55 PVC"
sEColorDsc = {
	"PL55 PVC" : "PL55 PVC",
	"white" : "white",
	"black" : "black",
	"bronze" : "bronze" # no comma
}
sEColor = sEColorDsc[sEColorD]

# checkboxes - additional reports

sARME = True      # measurements
sARM = True       # mounting
sARP = True       # profiles
sARD = False      # decoration
sARGD = True      # grain direction
sATS = True       # thickness summary
sAEI = True       # edgeband info


# ###################################################################################################################
# Default Settings ( CHANGE HERE IF NEEDED )
# ###################################################################################################################


# Qt GUI empty info width screen size
sEmptyDsc = "                                                                                                     "

# Qt GUI
# "yes" - to show
# "no" - to hide
sQT = "yes"

# DEBUG
# 1 - debug mode
# 0 - keep console clean
gDebugErrors = 0   # for errors
gDebugLoop = 0     # for main loop
gDebugParser = 0   # for parser in main loop


# ###################################################################################################################
# Autoconfig - define globals ( NOT CHANGE HERE )
# ###################################################################################################################


# active document init
gAD = ""

# objects to parse init
gOBs = ""

# currently parsed object called from main loop
gCallerObj = ""

# spreadsheet result init
gSheet = gAD

# spreadsheet row init
gSheetRow = 1

# unit for calculation purposes (not change)
gUnitC = "mm"

# header color
gHeadCS = (0.862745,0.862745,0.862745,1.000000) # strong
gHeadCW = (0.941176,0.941176,0.941176,1.000000) # weak

# language support
gLang1 = ""
gLang2 = ""
gLang3 = ""
gLang4 = ""
gLang5 = ""
gLang6 = ""
gLang7 = ""
gLang8 = ""
gLang9 = ""
gLang10 = ""
gLang11 = ""
gLang12 = ""
gLang13 = ""
gLang14 = ""
gLang15 = ""
gLang16 = ""
gLang17 = ""
gLang18 = ""
gLang19 = ""
gLang20 = ""
gLang21 = ""
gLang22 = ""
gLang23 = ""
gLang24 = ""
gLang25 = ""
gLang26 = ""


# ###################################################################################################################
# Init databases
# ###################################################################################################################


# init database for Fake Cube
dbFCO = [] # objects
dbFCW = dict() # width
dbFCH = dict() # height
dbFCL = dict() # length

# init database for dimensions
dbDQ = dict() # quantity
dbDA = dict() # area

# init database for thickness
dbTQ = dict() # quantity
dbTA = dict() # area

# init database for edge
dbE = dict()
dbE["total"] = 0 # total
dbE["empty"] = 0 # empty
dbE["edgeband"] = 0 # edgeband

# init database for face number
dbEFN = dict() # array names
dbEFD = dict() # array dimensions
dbEFV = dict() # array veneers

# init database for constraints
dbCNO = [] # objects
dbCNQ = dict() # quantity
dbCNN = dict() # names
dbCNV = dict() # values
dbCNL = dict() # length
dbCNH = dict() # header
dbCNOH = dict() # objects for hole

# init database for additional reports
dbARQ = dict() # quantity
dbARN = dict() # names
dbARV = dict() # values

gColorReference = (0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 1.0)

# ###################################################################################################################
# Support for Qt GUI
# ###################################################################################################################

# ###################################################################################################################
def showQtGUI():

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
			toolSW = 820
			toolSH = 680
			
			selWidth = 150 # selection width
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate("getDimensions", "getDimensions"))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			self.setMinimumWidth(toolSW)
			self.setMinimumHeight(toolSH)
			
			# ############################################################################
			# report types
			# ############################################################################
			
			# report customization
			self.ppmList = tuple(sPPMDsc.keys())
			self.ppmO = QtGui.QComboBox(self)
			self.ppmO.addItems(self.ppmList)
			self.ppmO.setCurrentIndex(self.ppmList.index(str(sPPM)))
			self.ppmO.textActivated[str].connect(self.setPPM)
			self.ppmO.setFixedWidth(selWidth)
			
			self.rcList = tuple(sLTFDsc.keys())
			self.rcO = QtGui.QComboBox(self)
			self.rcO.addItems(self.rcList)
			self.rcO.setCurrentIndex(self.rcList.index(str(sLTF)))
			self.rcO.textActivated[str].connect(self.setRC)
			self.rcO.setFixedWidth(selWidth)
			
			self.rcIS = QtGui.QLabel(str(sLTFDsc[sLTF]) + sEmptyDsc, self)
			
			# additional reports
			self.artsCB = QtGui.QCheckBox(translate('getDimensions', '- thickness summary'), self)
			self.artsCB.setCheckState(QtCore.Qt.Checked)
			
			self.areiCB = QtGui.QCheckBox(translate('getDimensions', '- edgeband info'), self)
			self.areiCB.setCheckState(QtCore.Qt.Checked)
			
			self.armeCB = QtGui.QCheckBox(translate('getDimensions', '- custom measurements'), self)
			self.armeCB.setCheckState(QtCore.Qt.Checked)
			
			self.armCB = QtGui.QCheckBox(translate('getDimensions', '- dowels and screws'), self)
			self.armCB.setCheckState(QtCore.Qt.Checked)
			
			self.arpCB = QtGui.QCheckBox(translate('getDimensions', '- construction profiles'), self)
			self.arpCB.setCheckState(QtCore.Qt.Checked)
			
			self.argdCB = QtGui.QCheckBox(translate('getDimensions', '- grain direction'), self)
			self.argdCB.setCheckState(QtCore.Qt.Checked)
			
			self.ardCB = QtGui.QCheckBox(translate('getDimensions', '- decorations'), self)
			self.ardCB.setCheckState(QtCore.Qt.Unchecked)
			
			# ############################################################################
			# units
			# ############################################################################

			# units for dimensions
			self.ufdL = QtGui.QLabel(translate("getDimensions", "Units for dimensions:"), self)
			
			self.ufdList = tuple(sUnitsMetricDsc.keys())
			self.ufdO = QtGui.QComboBox(self)
			self.ufdO.addItems(self.ufdList)
			self.ufdO.setCurrentIndex(self.ufdList.index(str(sUnitsMetric)))
			self.ufdO.textActivated[str].connect(self.setDFO)
			self.ufdO.setFixedWidth(selWidth)
			
			self.ufdIS = QtGui.QLabel(str(sUnitsMetricDsc[sUnitsMetric]) + sEmptyDsc, self)
			
			# precision for dimensions
			self.pufdL = QtGui.QLabel(translate("getDimensions", "Precision for dimensions:"), self)
			
			self.pufde = QtGui.QLineEdit(self)
			self.pufde.setText(str(sPDD))
			self.pufde.setFixedWidth(selWidth)
			
			# units for area
			self.ufaL = QtGui.QLabel(translate("getDimensions", "Units for area:"), self)
			
			self.ufaList = tuple(sUnitsAreaDsc.keys())
			self.ufaO = QtGui.QComboBox(self)
			self.ufaO.addItems(self.ufaList)
			self.ufaO.setCurrentIndex(self.ufaList.index(str(sUnitsArea)))
			self.ufaO.textActivated[str].connect(self.setUFA)
			self.ufaO.setFixedWidth(selWidth)
			
			self.ufaIS = QtGui.QLabel(str(sUnitsAreaDsc[sUnitsArea]) + sEmptyDsc, self)
			
			# precision for area
			self.pufaL = QtGui.QLabel(translate("getDimensions", "Precision for area:"), self)
			
			self.pufae = QtGui.QLineEdit(self)
			self.pufae.setText(str(sPDA))
			self.pufae.setFixedWidth(selWidth)
			
			# units for edge size
			self.ufsL = QtGui.QLabel(translate("getDimensions", "Units for edge size:"), self)
			
			self.ufsList = tuple(sUnitsEdgeDsc.keys())
			self.ufsO = QtGui.QComboBox(self)
			self.ufsO.addItems(self.ufsList)
			self.ufsO.setCurrentIndex(self.ufsList.index(str(sUnitsEdge)))
			self.ufsO.textActivated[str].connect(self.setUFS)
			self.ufsO.setFixedWidth(selWidth)
			
			self.ufsIS = QtGui.QLabel(str(sUnitsEdgeDsc[sUnitsEdge]) + sEmptyDsc, self)
			
			# precision for edge size
			self.pufsL = QtGui.QLabel(translate("getDimensions", "Precision for edge size:"), self)
			
			self.pufse = QtGui.QLineEdit(self)
			self.pufse.setText(str(sPDE))
			self.pufse.setFixedWidth(selWidth)
		
			# ############################################################################
			# visibility
			# ############################################################################
			
			# Toggle Visibility Feature
			self.visibilityL = QtGui.QLabel(translate("getDimensions", "All objects:"), self)
			
			self.visibilityList = tuple(sTVFDsc.keys())
			self.visibilityO = QtGui.QComboBox(self)
			self.visibilityO.addItems(self.visibilityList)
			self.visibilityO.setCurrentIndex(self.visibilityList.index(str(sTVF)))
			self.visibilityO.textActivated[str].connect(self.setVisibility)
			self.visibilityO.setFixedWidth(selWidth)
			
			self.visibilityIS = QtGui.QLabel(str(sTVFDsc[sTVF]) + sEmptyDsc, self)
			
			# part cut visibility
			self.pcvisibilityL = QtGui.QLabel(translate("getDimensions", "Part :: Cut content:"), self)
			
			self.pcvisibilityList = tuple(sPartCutDsc.keys())
			self.pcvisibilityO = QtGui.QComboBox(self)
			self.pcvisibilityO.addItems(self.pcvisibilityList)
			self.pcvisibilityO.setCurrentIndex(self.pcvisibilityList.index(str(sPartCut)))
			self.pcvisibilityO.textActivated[str].connect(self.setPartCutVisibility)
			self.pcvisibilityO.setFixedWidth(selWidth)
			
			self.pcvisibilityIS = QtGui.QLabel(str(sPartCutDsc[sPartCut]) + sEmptyDsc, self)
		
			# ############################################################################
			# additional settings
			# ############################################################################

			# languages
			self.LangL = QtGui.QLabel(translate("getDimensions", "Report language:"), self)
			
			self.LangList = tuple(sLangDsc.keys())
			self.LangO = QtGui.QComboBox(self)
			self.LangO.addItems(self.LangList)
			self.LangO.setCurrentIndex(self.LangList.index(str(sLang)))
			self.LangO.textActivated[str].connect(self.setLang)
			self.LangO.setFixedWidth(selWidth)
			
			self.LangIS = QtGui.QLabel(str(sLangDsc[sLang]) + sEmptyDsc, self)
			
			# report print quality
			self.rpqL = QtGui.QLabel(translate("getDimensions", "Report quality:"), self)
			
			self.rpqList = tuple(sRPQDsc.keys())
			self.rpqO = QtGui.QComboBox(self)
			self.rpqO.addItems(self.rpqList)
			self.rpqO.setCurrentIndex(self.rpqList.index(str(sRPQ)))
			self.rpqO.textActivated[str].connect(self.setQuality)
			self.rpqO.setFixedWidth(selWidth)
			
			self.rpqIS = QtGui.QLabel(str(sRPQDsc[sRPQ]) + sEmptyDsc, self)
			
			# ############################################################################
			# edgeband
			# ############################################################################
			
			# furniture color reference to calculate edgeband
			self.fcrB = QtGui.QPushButton(translate('getDimensions', 'set'), self)
			self.fcrB.clicked.connect(self.getColorReference)
			self.fcrB.setFixedWidth(50)
			self.fcrB.setAutoDefault(False)
			
			self.fcrE = QtGui.QLineEdit(self)
			self.fcrE.setText(translate('getDimensions','Please select face to get furniture color reference.'))
			self.fcrE.setFixedWidth(3*selWidth)
			
			# edgeband code, here is different you set description to variable
			self.ecL = QtGui.QLabel(translate("getDimensions", "Edgeband code:"), self)
			
			self.ecList = tuple(sEColorDsc.keys())
			self.ecO = QtGui.QComboBox(self)
			self.ecO.addItems(self.ecList)
			self.ecO.setCurrentIndex(self.ecList.index(str(sEColorD)))
			self.ecO.textActivated[str].connect(self.setEColor)
			self.ecO.setFixedWidth(selWidth)
			
			self.ectiL = QtGui.QLabel(translate("getDimensions", "Custom:"), self)
			
			self.ecti = QtGui.QLineEdit(self)
			self.ecti.setText(str(sEColor))
			self.ecti.setFixedWidth(selWidth)

			# ############################################################################
			# create
			# ############################################################################

			info = translate("getDimensions", "create spreadsheet toCut with dimensions, cut-list, BOM")
			self.okButton = QtGui.QPushButton(info, self)
			self.okButton.clicked.connect(self.onOk)
			self.okButton.setAutoDefault(True)
			self.okButton.setFixedHeight(40)

			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.layRC = QtGui.QHBoxLayout()
			self.layRC.setAlignment(QtGui.Qt.AlignLeft)
			self.layRC.addWidget(self.ppmO)
			self.layRC.addWidget(self.rcO)
			self.layRC.addWidget(self.rcIS)
			
			self.layAR = QtGui.QGridLayout()
			self.layAR.addWidget(self.artsCB, 0, 0)
			self.layAR.addWidget(self.areiCB, 0, 1)
			self.layAR.addWidget(self.armeCB, 0, 2)
			self.layAR.addWidget(self.armCB, 1, 0)
			self.layAR.addWidget(self.arpCB, 1, 1)
			self.layAR.addWidget(self.argdCB, 1, 2)
			self.layAR.addWidget(self.ardCB, 2, 0)
			
			self.layRT = QtGui.QVBoxLayout()
			self.layRT.addLayout(self.layRC)
			self.layRT.addLayout(self.layAR)
			
			self.groupRT = QtGui.QGroupBox(translate('getDimensions', 'Report type:'), self)
			self.groupRT.setLayout(self.layRT)
			
			self.layU = QtGui.QGridLayout()
			self.layU.addWidget(self.ufdL, 0, 0)
			self.layU.addWidget(self.ufdO, 0, 1)
			self.layU.addWidget(self.ufdIS, 0, 2)
			self.layU.addWidget(self.pufdL, 0, 3)
			self.layU.addWidget(self.pufde, 0, 4)
			self.layU.addWidget(self.ufaL, 1, 0)
			self.layU.addWidget(self.ufaO, 1, 1)
			self.layU.addWidget(self.ufaIS, 1, 2)
			self.layU.addWidget(self.pufaL, 1, 3)
			self.layU.addWidget(self.pufae, 1, 4)
			self.layU.addWidget(self.ufsL, 2, 0)
			self.layU.addWidget(self.ufsO, 2, 1)
			self.layU.addWidget(self.ufsIS, 2, 2)
			self.layU.addWidget(self.pufsL, 2, 3)
			self.layU.addWidget(self.pufse, 2, 4)
			self.groupU = QtGui.QGroupBox(translate('getDimensions', 'Units:'), self)
			self.groupU.setLayout(self.layU)
			
			self.layV1 = QtGui.QHBoxLayout()
			self.layV1.setAlignment(QtGui.Qt.AlignLeft)
			self.layV1.addWidget(self.visibilityL)
			self.layV1.addWidget(self.visibilityO)
			self.layV1.addWidget(self.visibilityIS)
			self.layV2 = QtGui.QHBoxLayout()
			self.layV2.setAlignment(QtGui.Qt.AlignLeft)
			self.layV2.addWidget(self.pcvisibilityL)
			self.layV2.addWidget(self.pcvisibilityO)
			self.layV2.addWidget(self.pcvisibilityIS)
			self.layV = QtGui.QVBoxLayout()
			self.layV.addLayout(self.layV1)
			self.layV.addLayout(self.layV2)
			self.groupV = QtGui.QGroupBox(translate('getDimensions', 'Visibility:'), self)
			self.groupV.setLayout(self.layV)
			
			self.layAS1 = QtGui.QHBoxLayout()
			self.layAS1.setAlignment(QtGui.Qt.AlignLeft)
			self.layAS1.addWidget(self.LangL)
			self.layAS1.addWidget(self.LangO)
			self.layAS1.addWidget(self.LangIS)
			self.layAS2 = QtGui.QHBoxLayout()
			self.layAS2.setAlignment(QtGui.Qt.AlignLeft)
			self.layAS2.addWidget(self.rpqL)
			self.layAS2.addWidget(self.rpqO)
			self.layAS2.addWidget(self.rpqIS)
			self.layAS = QtGui.QVBoxLayout()
			self.layAS.addLayout(self.layAS1)
			self.layAS.addLayout(self.layAS2)
			self.groupAS = QtGui.QGroupBox(translate('getDimensions', 'Additional settings:'), self)
			self.groupAS.setLayout(self.layAS)
			
			self.layED1 = QtGui.QHBoxLayout()
			self.layED1.setAlignment(QtGui.Qt.AlignLeft)
			self.layED1.addWidget(self.fcrB)
			self.layED1.addWidget(self.fcrE)
			self.layED2 = QtGui.QHBoxLayout()
			self.layED2.setAlignment(QtGui.Qt.AlignLeft)
			self.layED2.addWidget(self.ecL)
			self.layED2.addWidget(self.ecO)
			self.layED2.addWidget(self.ectiL)
			self.layED2.addWidget(self.ecti)
			self.layED2.addStretch()
			self.layED = QtGui.QVBoxLayout()
			self.layED.addLayout(self.layED1)
			self.layED.addLayout(self.layED2)
			self.groupED = QtGui.QGroupBox(translate('getDimensions', 'Edgeband:'), self)
			self.groupED.setLayout(self.layED)
			
			self.layCR = QtGui.QVBoxLayout()
			self.layCR.addWidget(self.okButton)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			self.layout.addWidget(self.groupRT)
			self.layout.addStretch()
			self.layout.addWidget(self.groupU)
			self.layout.addStretch()
			self.layout.addWidget(self.groupV)
			self.layout.addStretch()
			self.layout.addWidget(self.groupAS)
			self.layout.addStretch()
			self.layout.addWidget(self.groupED)
			self.layout.addStretch()
			self.layout.addLayout(self.layCR)
			self.setLayout(self.layout)

			# edge color hide by default
			self.ecL.hide()
			self.ecO.hide()
			self.ectiL.hide()
			self.ecti.hide()

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
			try:
				import MagicPanels as MP
				QtCSS = MP.getTheme(MP.gTheme)
				self.setStyleSheet(QtCSS)
			except:
				skip = 1
			
		# ############################################################################
		# actions auto define
		# ############################################################################

		def setLang(self, selectedText):
			global sLang
			sLang = selectedText
			self.LangIS.setText(str(sLangDsc[sLang]) + sEmptyDsc)

		def setQuality(self, selectedText):
			global sRPQ
			sRPQ = selectedText
			self.rpqIS.setText(str(sRPQDsc[sRPQ]) + sEmptyDsc)

		def setVisibility(self, selectedText):
			global sTVF
			sTVF = selectedText
			self.visibilityIS.setText(str(sTVFDsc[sTVF]) + sEmptyDsc)

		def setPartCutVisibility(self, selectedText):
			global sPartCut
			sPartCut = selectedText
			self.pcvisibilityIS.setText(str(sPartCutDsc[sPartCut]) + sEmptyDsc)

		# submenu for report types
		def setSubmenu(self, iAction):

			if iAction == "show":
				# units for area
				self.ufaL.show()
				self.ufaO.show()
				self.ufaIS.show()
				# units for edge size
				self.ufsL.show()
				self.ufsO.show()
				self.ufsIS.show()
				
			if iAction == "hide":
				# units for area
				self.ufaL.hide()
				self.ufaO.hide()
				self.ufaIS.hide()
				# units for edge size
				self.ufsL.hide()
				self.ufsO.hide()
				self.ufsIS.hide()
				
		def setRC(self, selectedText):
			global sLTF
			sLTF = selectedText
			self.rcIS.setText(str(sLTFDsc[sLTF]) + sEmptyDsc)

			# submenu for report type
			if selectedText == "c" or selectedText == "p" or selectedText == "a":
				self.setSubmenu("hide")
			else:
				self.setSubmenu("show")

			# edgeband code
			if selectedText == "e" or selectedText == "d":
				self.ecL.show()
				self.ecO.show()
				self.ectiL.show()
				self.ecti.show()
			else:
				self.ecL.hide()
				self.ecO.hide()
				self.ectiL.hide()
				self.ecti.hide()
				
			if selectedText == "a":
				self.ufdL.hide()
				self.ufdO.hide()
				self.ufdIS.hide()
				
				self.ufaL.hide()
				self.ufaO.hide()
				self.ufaIS.hide()
				
				self.ufsL.hide()
				self.ufsO.hide()
				self.ufsIS.hide()
				
				self.artsCB.hide()
				self.areiCB.hide()
				self.armeCB.hide()
				self.ardCB.hide()
				self.armCB.hide()
				self.arpCB.hide()
				self.argdCB.hide()
				
				self.pufdL.hide()
				self.pufde.hide()
				self.pufaL.hide()
				self.pufae.hide()
				self.pufsL.hide()
				self.pufse.hide()
				
			else:
				self.ufdL.show()
				self.ufdO.show()
				self.ufdIS.show()
				
				self.ufaL.show()
				self.ufaO.show()
				self.ufaIS.show()
				
				self.ufsL.show()
				self.ufsO.show()
				self.ufsIS.show()
				
				self.artsCB.show()
				self.areiCB.show()
				self.armeCB.show()
				self.ardCB.show()
				self.armCB.show()
				self.arpCB.show()
				self.argdCB.show()
				
				self.pufdL.show()
				self.pufde.show()
				self.pufaL.show()
				self.pufae.show()
				self.pufsL.show()
				self.pufse.show()

		def setPPM(self, selectedText):
			global sPPM
			sPPM = selectedText

		def setDFO(self, selectedText):
			global sUnitsMetric, sPDD
			sUnitsMetric = selectedText
			self.ufdIS.setText(str(sUnitsMetricDsc[sUnitsMetric]) + sEmptyDsc)
			# set precision
			sPDD = sPrecisionDD[sUnitsMetric]
			self.pufde.setText(str(sPDD))

		def setUFA(self, selectedText):
			global sUnitsArea, sPDA
			sUnitsArea = selectedText
			self.ufaIS.setText(str(sUnitsAreaDsc[sUnitsArea]) + sEmptyDsc)
			# set precision
			sPDA = sPrecisionDA[sUnitsArea]
			self.pufae.setText(str(sPDA))
			
		def setUFS(self, selectedText):
			global sUnitsEdge, sPDE
			sUnitsEdge = selectedText
			self.ufsIS.setText(str(sUnitsEdgeDsc[sUnitsEdge]) + sEmptyDsc)
			# set precision
			sPDE = sPrecisionDE[sUnitsEdge]
			self.pufse.setText(str(sPDE))

		# here is different you set description to variable
		def setEColor(self, selectedText):
			global sEColor
			tmpColor = sEColorDsc[str(selectedText)]
			self.ecti.setText(str(tmpColor))
		
		# buttons
		def getColorReference(self):
			
			try:
				obj = FreeCADGui.Selection.getSelection()[0]
				face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				i = 1
				for f in obj.Shape.Faces:
					if str(f.BoundBox) == str(face.BoundBox):
						index = i
						break

					i = i + 1
				
				try:
					test = obj.ViewObject.ShapeAppearance
					colorsSchema = 1
				except:
					colorsSchema = 0
				
				color = ""
				if colorsSchema == 1:
					try:
						color = obj.ViewObject.ShapeAppearance[index-1].DiffuseColor
					except:
						color = obj.ViewObject.ShapeAppearance[0].DiffuseColor
				else:
					try:
						color = obj.ViewObject.DiffuseColor[index-1]
					except:
						color = obj.ViewObject.DiffuseColor[0]
				
				global gColorReference
				gColorReference = color
				self.fcrE.setText(str(color))
			
			except:
				self.fcrE.setText(translate('getDimensions','Select face to get furniture color reference.'))
			

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
		global sEColor
		global sARME, sARM, sARP, sARD, sARGD
		global sATS, sAEI
		global sPDD, sPDA, sPDE
		
		# set edgeband code from text form
		sEColor = form.ecti.text()
		
		# set precisions
		sPDD = int(form.pufde.text())
		sPDA = int(form.pufae.text())
		sPDE = int(form.pufse.text())
		
		# measurements
		if form.armeCB.isChecked():
			sARME = True
		else:
			sARME = False
		
		# mounting
		if form.armCB.isChecked():
			sARM = True
		else:
			sARM = False
			
		# profiles
		if form.arpCB.isChecked():
			sARP = True
		else:
			sARP = False
		
		# decoration
		if form.ardCB.isChecked():
			sARD = True
		else:
			sARD = False

		# grain direction
		if form.argdCB.isChecked():
			sARGD = True
		else:
			sARGD = False

		# thickness summary
		if form.artsCB.isChecked():
			sATS = True
		else:
			sATS = False
			
		# edgeband info
		if form.areiCB.isChecked():
			sAEI = True
		else:
			sAEI = False

		gExecute = "yes"


# ###################################################################################################################
# Support for errors
# ###################################################################################################################


# ###################################################################################################################
def showError(iCaller, iObj, iPlace, iError):

	if gDebugErrors == 1:
		
		FreeCAD.Console.PrintMessage("\n ====================================================== \n")
		
		try:
			FreeCAD.Console.PrintMessage("ERROR: ")
			FreeCAD.Console.PrintMessage(" | ")
			FreeCAD.Console.PrintMessage(str(iCaller))
			FreeCAD.Console.PrintMessage(" | ")
			FreeCAD.Console.PrintMessage(str(iObj.Label))
			FreeCAD.Console.PrintMessage(" | ")
			FreeCAD.Console.PrintMessage(str(iPlace))
			FreeCAD.Console.PrintMessage(" | ")
			FreeCAD.Console.PrintMessage(str(iError))
			
		except:
			FreeCAD.Console.PrintMessage("FATAL ERROR, or even worse :-)")
			
		FreeCAD.Console.PrintMessage("\n ====================================================== \n")
	
	return 0


# ###################################################################################################################
# Support for calculations
# ###################################################################################################################


# ###################################################################################################################
def getUnit(iValue, iType, iCaller="getUnit"):

	# for dimensions
	if iType == "d":
	
		gFakeCube.Length = float(iValue)
		v = gFakeCube.Length.getValueAs(gUnitC).Value

		if sUnitsMetric == "mm":
			if sPDD == 0:
				return str( int(round(v, 0)) )
			else:
				return str( float(round(v, sPDD)) )

		if sUnitsMetric == "m":
			return str( round(v * float(0.001), sPDD) )
		
		if sUnitsMetric == "in":
			return str( round(v * float(0.0393700787), sPDD) )
	
	# for edge
	if iType == "edge":
		
		gFakeCube.Length = float(iValue)
		v = gFakeCube.Length.getValueAs(gUnitC).Value

		if sUnitsEdge == "mm":
			if sPDE == 0:
				return str( int(round(v, 0)) )
			else:
				return str( float(round(v, sPDE)) )
		
		if sUnitsEdge == "m":
			return str( round(v * float(0.001), sPDE) )
		
		if sUnitsEdge == "in":
			return str( round(v * float(0.0393700787), sPDE) )
	
	# for area
	if iType == "area":
		
		gFakeCube.Length = float(iValue)
		v = gFakeCube.Length.getValueAs(gUnitC).Value
		
		if sUnitsArea == "mm":
			if sPDA == 0:
				return str( int(round(v, 0)) )
			else:
				return str( float(round(v, sPDA)) )
		
		if sUnitsArea == "m":
			return str( round(v * float(0.000001), sPDA) )
		
		if sUnitsArea == "in":
			return str( round(v * float(0.0015500031), sPDA) )
	
	# for to-angle conversion
	if iType == "to-angle":
		
		gFakeCube.Placement.Rotation.Angle = float(iValue)
		return str( int( gFakeCube.Placement.Rotation.getYawPitchRoll()[0] ) )
	
	return -1


# ###################################################################################################################
def toSheet(iValue, iType, iCaller="toSheet"):

	# prevent FreeCAD to change "18 mm" string into "18.0 mm"
	
	# for dimensions
	if iType == "d":
		return  "=<<" + getUnit(iValue, iType, iCaller) + " " + sUnitsMetric + ">>"

	# for edge
	if iType == "edge":
		return  "=<<" + getUnit(iValue, iType, iCaller) + " " + sUnitsEdge + ">>"

	# for area
	if iType == "area":
		return  "=<<" + getUnit(iValue, iType, iCaller) + ">>"

	# for raw angle
	if iType == "to-angle":
		return  getUnit(iValue, iType, iCaller)
	
	# for raw angle
	if iType == "raw-angle":
		return str( int(round(float(iValue), 0)) )
		
	# for string
	if iType == "string":
		return str(iValue)

	return -1


# ###################################################################################################################
def switchApproximation(iA, iB, iCaller="switchApproximation"):
	
	# solves the problem if an element intersects the coordinate axis

	if iA >= 0 and iB >= 0 and iB > iA:
		return iB - iA
	if iB >= 0 and iA >= 0 and iA > iB:
		return iA - iB
		
	if iA < 0 and iB >= 0 and iB > iA:
		return abs(iA) + iB
	if iB < 0 and iA >= 0 and iA > iB:
		return abs(iB) + iA

	if iA < 0 and iB <= 0 and iB > iA:
		return abs(iA) - abs(iB)
	if iB < 0 and iA <= 0 and iA > iB:
		return abs(iB) - abs(iA)

	return 0
	
	
# ###################################################################################################################
def getApproximation(iObj, iCaller="getApproximation"):

	init = 0
	
	minX = 0
	minY = 0
	minZ = 0

	maxX = 0
	maxY = 0
	maxZ = 0

	vs = getattr(iObj.Shape, "Vertex"+"es")

	for v in vs:
		
		[ x, y, z ] = [ v.X, v.Y, v.Z ]
		
		if init == 0:
			[ minX, minY, minZ ] = [ x, y, z ]
			[ maxX, maxY, maxZ ] = [ x, y, z ]
			init = 1
		
		if x > maxX:
			maxX = x
		
		if y > maxY:
			maxY = y

		if z > maxZ:
			maxZ = z

		if x < minX:
			minX = x

		if y < minY:
			minY = y

		if z < minZ:
			minZ = z
		
	s1 = switchApproximation(minX, maxX, iCaller)
	s2 = switchApproximation(minY, maxY, iCaller)
	s3 = switchApproximation(minZ, maxZ, iCaller)

	mWidth = round(s1, 2)
	mDepth = round(s2, 2)
	mHeight = round(s3, 2)
	
	s = [ mWidth, mDepth, mHeight ]
	s.sort()
	
	
	key = ""
	key += str(round(s[0], 2))
	key += ":"
	key += str(round(s[1], 2))
	key += ":"
	key += str(round(s[2], 2))
	key += ":"
	key += str(getGroup(iObj, iCaller))

	return [ key, s[0], s[1], s[2] ]


# ###################################################################################################################
def getGroup(iObj, iCaller="getGroup"):

	# init variable
	vGroup = ""

	# support for Pad and Pocket
	if (
		iObj.isDerivedFrom("PartDesign::Pad") or 
		iObj.isDerivedFrom("PartDesign::Pocket")
		):
		
		# get parent reference key
		try:
			key = iObj.Profile[0].Parents[0][0]
			parents = iObj.Profile[0].Parents
			for p in parents:
				if p[0].isDerivedFrom("PartDesign::Body"):
					key = p[0]
		except:
			vGroup = ""
			
		# get grandparent
		try:
			vGroup = key.getParentGroup().Label
		except:
			vGroup = ""
		
		# get parent
		if vGroup == "":
			try:
				vGroup = key.Label
			except:
				vGroup = ""

	# support for Cube and other calls
	else:
		
		# get grandparent
		try:
			vGroup = iObj.getParentGroup().getParentGroup().Label
		except:
			vGroup = ""
		
		# get parent
		if vGroup == "":
			try:
				vGroup = iObj.getParentGroup().Label
			except:
				vGroup = ""
	
	# get parent for LinkGroup
	if vGroup == "":
		try:
			vGroup = iObj.InListRecursive[1].Label
		except:
			vGroup = ""
	
	if vGroup == "":
		try:
			vGroup = iObj.InListRecursive[0].Label
		except:
			vGroup = ""
	
	return vGroup


# ###################################################################################################################
def getKey(iObj, iW, iH, iL, iType, iCaller="getKey"):

	# set array with values
	vKeyArr = [ iW, iH, iL ]

	# sort as values to have thickness first
	vKeyArr.sort()

	# create key string with thickness first
	vKey = ""
	vKey += str(vKeyArr[0])
	vKey += ":"
	vKey += str(vKeyArr[1])
	vKey += ":"
	vKey += str(vKeyArr[2])

	# key for name report
	if iType == "d" and (sLTF == "n" or sLTF == "e" or sLTF == "d"):
		vKey = str(vKey) + ":" + str(iObj.Label)

	# key for group report
	if iType == "d" and (sLTF == "g" or sLTF == "d"):
		
		# get grandparent or parent group name
		vGroup = getGroup(iObj, iCaller)
		
		if vGroup != "":
			vKey = str(vKey) + ":" + str(vGroup)
		else:
			vKey = str(vKey) + ":[...]"

	# return thickness (this is value, not string)
	if iType == "thick":
		return vKeyArr[0]

	return str(vKey)


# ###################################################################################################################
def getArea(iObj, iW, iH, iL, iCaller="getArea"):

	# make sure to not calculate thickness
	vT = getKey(iObj, iW, iH, iL, "thick", iCaller)

	if iL == vT:
		vD1 = iW
		vD2 = iH
	
	elif iW == vT:
		vD1 = iL
		vD2 = iH
	
	else:
		vD1 = iL
		vD2 = iW

	# calculate area without thickness
	vArea = vD1 * vD2

	return vArea


# ###################################################################################################################
def getEdge(iObj, iW, iH, iL, iCaller="getEdge"):

	# skip the thickness dimension
	vT = getKey(iObj, iW, iH, iL, "thick", iCaller)

	if iL == vT:
		vD1 = iW
		vD2 = iH

	elif iW == vT:
		vD1 = iL
		vD2 = iH

	else:
		vD1 = iL
		vD2 = iW

	# calculate the edge size
	vEdge = (2 * vD1) + (2 * vD2)

	return vEdge


# ###################################################################################################################
def getEdgeBand(iObj, iW, iH, iL, iCaller="getEdgeBand"):

	try:

		# get faces colors
		vFacesColors = []
		try:
			vFacesColors = iObj.ViewObject.ShapeAppearance
			colorsSchema = 1
		except:
			vFacesColors = iObj.ViewObject.DiffuseColor
			colorsSchema = 0

		# edgeband for given object
		vEdgeSum = 0

		# there can be more faces than 6 (Array Cube)
		vFaceN = []
		vFaceD = []
		vFaceV = []

		# search for edgeband
		i = 0
		for c in vFacesColors:
			
			if colorsSchema == 1:
				c = c.DiffuseColor
		
			# there can be more faces than 6 (Array Cube)
			vFaceN.insert(i, "")
			vFaceD.insert(i, 0)
			vFaceV.insert(i, "")

			# if the edge face color is different than object color, 
			# it means this is edgeband added by the user
			if str(c) != str(gColorReference):
				
				vFaceEdge = iObj.Shape.Faces[i].Length
	
				# get the thickness dimension
				vT = getKey(iObj, iW, iH, iL, "thick", iCaller)
	
				# if you know the thickness you can 
				# calculate the edge for the face
				vEdge = ( vFaceEdge - (2 * vT)) / 2

				# sort thickness
				a = [ iW, iH, iL ]
				a.sort()

				# check if this is correct edge
				if int(vEdge) == int(a[1]) or int(vEdge) == int(a[2]):
					
					vFaceN[i] = gLang12
					vFaceD[i] = vEdge
					vFaceV[i] = str(sEColor)
				
				else:
				
					vFaceN[i] = gLang13
					vFaceD[i] = -1
					vFaceV[i] = str(sEColor)
					vEdge = 0

				# add all faces to edge size
				vEdgeSum = vEdgeSum + vEdge

			# next face index
			i = i + 1

	except:

		# get edgeband error
		showError(iCaller, iObj, "getEdgeBand", "getting edgeband error")
		return -1

	return [ vEdgeSum, vFaceN, vFaceD, vFaceV ]


# ###################################################################################################################
def getConstraintName(iObj, iName, iCaller="getConstraintName"):

	try:

		# workaround for FreeCAD constraints name bug
		# https://forum.freecadweb.org/viewtopic.php?f=10&t=67042
		
		# numbers way of encoding
		iName = iName.replace("00",", ")
		iName = iName.replace("0"," ")
		
		# underscores way of encoding
		iName = iName.replace("__",", ")
		iName = iName.replace("_"," ")

	except:

		showError(iCaller, iObj, "getConstraintName", "getting constraint name error")
		return -1

	return str(iName)


# ###################################################################################################################
# Database controllers - set db only via this controllers
# ###################################################################################################################


# ###################################################################################################################
def setDB(iObj, iW, iH, iL, iCaller="setDB"):

	try:
		
		# set db for Fake Cube Object 
		dbFCO.append(iObj)

		# set db for Fake Cube dimensions
		dbFCW[iObj.Label] = iW
		dbFCH[iObj.Label] = iH
		dbFCL[iObj.Label] = iL

		# get area for object
		vArea = getArea(iObj, iW, iH, iL, iCaller) 
	
		# get key  for object
		vKey = getKey(iObj, iW, iH, iL, "d", iCaller)
	
		# set dimensions db for quantity & area
		if vKey in dbDQ:
	
			dbDQ[vKey] = dbDQ[vKey] + 1
			dbDA[vKey] = dbDA[vKey] + vArea
		else:
	
			dbDQ[vKey] = 1
			dbDA[vKey] = vArea

		# get key  for object (convert value to dimension string)
		vKeyT = str(getKey(iObj, iW, iH, iL, "thick", iCaller))
	
		# set thickness db for quantity & area
		if vKeyT in dbTQ:
	
			dbTQ[vKeyT] = dbTQ[vKeyT] + 1
			dbTA[vKeyT] = dbTA[vKeyT] + vArea
		else:
	
			dbTQ[vKeyT] = 1
			dbTA[vKeyT] = vArea

		# check visibility for edge if visibility feature is "edge"
		# if visibility feature is "on" the whole object is skipped
		# so never run this part for such object
		vSkip = 0
		if sTVF == "edge":
			if FreeCADGui.ActiveDocument.getObject(iObj.Name).Visibility == False:
				vSkip = 1

		# if object is not visible not calculate the edge
		if vSkip == 0:

			# set edge db for total edge size
			vEdge = getEdge(iObj, iW, iH, iL, iCaller)
			dbE["total"] = dbE["total"] + vEdge
			
			colorsNum = 1
			try:
				colorsNum = len(iObj.ViewObject.ShapeAppearance)
			except:
				colorsNum = len(iObj.ViewObject.DiffuseColor)

			# if color faces, not whole object color
			if colorsNum != 1:
				
				# set edge db for edgeband edge size & faces
				vEdge , dbEFN[vKey], dbEFD[vKey], dbEFV[vKey] = getEdgeBand(iObj, iW, iH, iL, iCaller)
				dbE["edgeband"] = dbE["edgeband"] + vEdge

			# set edge db for empty edge size
			dbE["empty"] = dbE["total"] - dbE["edgeband"]

	except:

		# set db error
		showError(iCaller, iObj, "setDB", "set db error")
		return -1

	return 0


# ###################################################################################################################
def setDBApproximation(iObj, iCaller="setDBApproximation"):

	try:
		
		[ vKey, thick, s1, s2 ] = getApproximation(iObj, iCaller)
		
		if thick <= 0 or s1 <= 0 or s2 <= 0:
			raise
		
		# set dimensions db
		if vKey in dbDQ:
			
			dbDQ[vKey] = dbDQ[vKey] + 1
			
		else:
		
			dbDQ[vKey] = 1

	except:

		# set db error
		error = ""
		error += "Object is not supported, because has no exact vertex values to calculate dimensions."
		showError(iCaller, iObj, "setDBApproximation", error)
		return -1

	return 0


# ###################################################################################################################
def setDBConstraints(iObj, iL, iN, iV, iHoleObj, iCaller="setDBConstraints"):

	try:

		# set key
		vKey = iObj.Label
				
		# set quantity
		if vKey in dbCNQ:

			# increase quantity only
			dbCNQ[vKey] = dbCNQ[vKey] + 1

			# show only one object at report
			return 0
			
		# init quantity
		dbCNQ[vKey] = 1

		# add object with no empty constraints names
		dbCNO.append(iObj)

		# set length, names, values
		dbCNL[vKey] = iL
		dbCNN[vKey] = iN
		dbCNV[vKey] = iV
		
		# set holes for detailed report
		if sLTF == "d":
			try:
				dbCNOH[str(iHoleObj)] += str(vKey) + ":"
			except:
				dbCNOH[str(iHoleObj)] = str(vKey) + ":"

		# constraints report header for Length
		if iObj.isDerivedFrom("PartDesign::Pad"):
			dbCNH[vKey] = gLang9

		if iObj.isDerivedFrom("Part::Extrusion"):
			dbCNH[vKey] = gLang9

		if iObj.isDerivedFrom("PartDesign::Hole"):
			dbCNH[vKey] = gLang15

	except:

		# set db error
		showError(iCaller, iObj, "setDBConstraints", "set db error")
		return -1

	return 0


# ###################################################################################################################
def setDBAllConstraints(iObj, iL, iN, iV, iCaller="setDBAllConstraints"):

	try:

		# make values sorted copy
		vValues = iV.copy()
		vValues.sort()
		vVal = str(":".join(map(str, vValues)))

		# get group name for base element
		vGroup = getGroup(iObj, iCaller)

		# set key
		vKey = vGroup
		vKey += ":" + vVal
		vKey += ":" + iL

		# set quantity
		if vKey in dbCNQ:

			# increase quantity only
			dbCNQ[vKey] = dbCNQ[vKey] + 1

			# show only one object at report
			return 0
			
		# init quantity
		dbCNQ[vKey] = 1

		# set names and values
		dbCNN[vKey] = str(":".join(map(str, iN)))
		dbCNV[vKey] = str(":".join(map(str, iV)))

		# set length
		dbCNL[vKey] = iL
		dbCNH[vKey] = gLang9

	except:

		# set db error
		showError(iCaller, iObj, "setDBAllConstraints", "set db error")
		return -1

	return 0


# ###################################################################################################################
def setDBAdditional(iObj, iType, iN, iV, iKey="", iCaller="setDBAdditional"):

	try:

		# set key
		vV = str(":".join(map(str, iV)))
		
		if iKey != "":
			
			vKey = iKey
		
		else:
			if (
				iType == "Fillet" or
				iType == "Chamfer"
				):
			
				vKey = iType + ", "
				vKey += iObj.Base[0].Label + ", " + ', '.join(map(str, iObj.Base[1]))
				vKey += ":" + vV
			
			else:
				vKey = iType
				vKey += ":" + vV
		
		# set quantity
		if vKey in dbARQ:
	
			# increase quantity only
			dbARQ[vKey] = dbARQ[vKey] + 1
	
			# show only one object at report if there is no custom key
			# update existing entry if there is custom key
			if iKey == "":
				return 0
			else:
				# set names and values
				dbARN[vKey] = str(":".join(map(str, iN)))
				dbARV[vKey] = vV
				return 0
		
		dbARQ[vKey] = 1
		
		# set names and values
		dbARN[vKey] = str(":".join(map(str, iN)))
		dbARV[vKey] = vV

	except:

		# set db error
		showError(iCaller, iObj, "setDBAdditional", "set db error")
		return -1

	return 0


# ###################################################################################################################
# Support for base furniture parts
# ###################################################################################################################


# ###################################################################################################################
def setCube(iObj, iCaller="setCube"):

	try:

		if sLTF == "a":
		
			setDBApproximation(iObj, iCaller)
		
		else:
		
			# get correct dimensions as values
			vW = iObj.Width.Value
			vH = iObj.Height.Value
			vL = iObj.Length.Value

			# set db for quantity & area & edge size
			setDB(iObj, vW, vH, vL, iCaller)

	except:

		# if no access to the values
		showError(iCaller, iObj, "setCube", "no access to the values")
		return -1

	return 0


# ###################################################################################################################
def setPad(iObj, iCaller="setPad"):

	try:
		
		if sLTF == "a":
		
			setDBApproximation(iObj, iCaller)
		
		else:
		
			vW = ""
			vH = ""
			vL = ""
			skip = 0
		
			# try get values from named constraints
			try:
				constraints = iObj.Profile[0].Constraints
				for c in constraints:
					if c.Name == "SizeX":
						vW = c.Value
					if c.Name == "SizeY":
						vL = c.Value
				
				vH = iObj.Length.Value
			
			# get first dimensions (this may not work for non-rectangle shapes)
			except:
				skip = 1

			if vW == "" or vL == "" or vH == "":
				vW = iObj.Profile[0].Shape.OrderedEdges[0].Length
				vH = iObj.Profile[0].Shape.OrderedEdges[1].Length
				vL = iObj.Length.Value
		
			# set db for quantity & area & edge size
			setDB(iObj, vW, vH, vL, iCaller)

	except:

		# if no access to the values (wrong design of Sketch and Pad)
		showError(iCaller, iObj, "setPad", "no access to the values")
		return -1

	return 0


# ###################################################################################################################
def setExtrusion(iObj, iCaller="setExtrusion"):

	try:

		if sLTF == "a":
		
			setDBApproximation(iObj, iCaller)
		
		else:
		
			# try get values from named constraints
			try:
				constraints = iObj.Base.Constraints
				for c in constraints:
					if c.Name == "SizeX":
						vW = c.Value
					if c.Name == "SizeY":
						vL = c.Value
				
				vH = abs(iObj.LengthFwd.Value)
			
			# get first dimensions (this may not work for non-rectangle shapes)
			except:
				skip = 1

			if vW == "" or vL == "" or vH == "":
				[ vKey, vW, vH, vL ] = getApproximation(iObj, iCaller)
		
			# set db for quantity & area & edge size
			setDB(iObj, vW, vH, vL, iCaller)

	except:

		# if no access to the values
		showError(iCaller, iObj, "setExtrusion", "no access to the values")
		return -1

	return 0


# ###################################################################################################################
def setCustomObject(iObj, iCaller="setCustomObject"):

	try:

		if sLTF == "a":
		
			setDBApproximation(iObj, iCaller)
		
		else:
		
			# get correct dimensions as values
			vW = iObj.Width.Value
			vH = iObj.Height.Value
			vL = iObj.Length.Value

			# set db for quantity & area & edge size
			setDB(iObj, vW, vH, vL, iCaller)

	except:

		# if no access to the values
		showError(iCaller, iObj, "setCustomObject", "no access to the values")
		return -1

	return 0


# ###################################################################################################################
def setConstraints(iObj, iCaller="setConstraints"):

	try:

		# init variables
		isSet = 0
		vNames = ""
		vValues = ""
		vHoleObj = ""	

		# set reference point
		if iObj.isDerivedFrom("Part::Extrusion"):
			vCons = iObj.Base.Constraints
		else:
			vCons = iObj.Profile[0].Constraints

		for c in vCons:
			if c.Name != "":

				# decode
				c.Name = getConstraintName(iObj, c.Name, iCaller)

				# set Constraint Name
				vNames += str(c.Name) + ":"

				if str(c.Type) == "Angle":
					v = "to-angle;" + str(c.Value)
				else:
					v = "d;" + str(c.Value)
				
				# get values as the correct dimensions
				vValues += v + ":"
	
				# non empty names, so object can be set
				isSet = 1
	
		if isSet == 1:
	
			vLength = ""
	
			# support for Pad furniture part
			if iObj.isDerivedFrom("PartDesign::Pad"):
				vLength = "d;" + str(iObj.Length.Value)

			# support for Part::Extrusion
			if iObj.isDerivedFrom("Part::Extrusion"):
				vLength = "d;" + str(iObj.LengthFwd.Value)

			# support for pilot hole and countersink
			if iObj.isDerivedFrom("PartDesign::Hole"):

				if iObj.DepthType == "Dimension":
					vLength = "d;" + str(iObj.Depth.Value)
				else:
					# no length header
					vLength = ""

				# detailed report for holes
				if sLTF == "d":
				
					try:

						# set reference point until will be something 
						# different than hole
						ref = iObj.BaseFeature

						while ref.isDerivedFrom("PartDesign::Hole"):
							ref = ref.BaseFeature

						vHoleObj = ref.Label

					except:
						skip = 1

			# set db for Constraints
			setDBConstraints(iObj, vLength, vNames, vValues, vHoleObj, iCaller)

	except:
		
		# if there is wrong structure
		showError(iCaller, iObj, "setConstraints", "wrong structure")
		return -1

	return 0


# ###################################################################################################################
def setAllConstraints(iObj, iCaller="setAllConstraints"):

	try:

		# init variables
		vArrNames = []
		vArrValues = []

		if iObj.isDerivedFrom("Part::Extrusion"):
			vCons = iObj.Base.Constraints
		else:
			vCons = iObj.Profile[0].Constraints
		
		for c in vCons:
			
			name = str(c.Name)
			value = float(c.Value)
			
			if value != float(0):

				if str(c.Type) == "Angle":
					v = "to-angle;" + str(value)
				else:
					v = "d;" + str(value)
				
				vArrValues.append(v)

				# set Constraint Name
				if name != "":
	
					# decode
					n = getConstraintName(iObj, name, iCaller)

				else:
					
					# no empty array key
					n = "-"

				vArrNames.append(n)
			
		# convert float to the correct dimension
		if iObj.isDerivedFrom("Part::Extrusion"):
			vLength = "d;" + str(iObj.LengthFwd.Value)
		else:
			vLength = "d;" + str(iObj.Length.Value)

		# set db for Constraints
		if len(vArrNames) > 0 and len(vArrValues) > 0:
			setDBAllConstraints(iObj, vLength, vArrNames, vArrValues, iCaller)

	except:
		
		# if there is wrong structure
		showError(iCaller, iObj, "setAllConstraints", "wrong structure")
		return -1

	return 0


# ###################################################################################################################
def setDecoration(iObj, iCaller="setDecoration"):

	try:

		# init variables
		vArrNames = []
		vArrValues = []
		vType = ""

		if iObj.isDerivedFrom("PartDesign::Fillet"):
			
			vType = "Fillet"

			vArrNames.append("Radius")
			v = "d;" + str(iObj.Radius.Value)
			vArrValues.append(v)

		if iObj.isDerivedFrom("PartDesign::Chamfer"):

			vType = "Chamfer"

			vArrNames.append("ChamferType")
			v = "string;" + str(iObj.ChamferType)
			vArrValues.append(v)

			vArrNames.append("FlipDirection")
			v = "string;" + str(iObj.FlipDirection)
			vArrValues.append(v)
			
			vArrNames.append("Refine")
			v = "string;" + str(iObj.Refine)
			vArrValues.append(v)
			
			vArrNames.append("Size 1")
			v = "d;" + str(iObj.Size.Value)
			vArrValues.append(v)

			vArrNames.append("Size 2")
			v = "d;" + str(iObj.Size2.Value)
			vArrValues.append(v)

		if iObj.isDerivedFrom("Part::Sphere"):

			vType = "Sphere"

			vArrNames.append("Radius")
			v = "d;" + str(iObj.Radius.Value)
			vArrValues.append(v)

		if iObj.isDerivedFrom("Part::Cone"):

			vType = "Cone"

			vArrNames.append("Radius1")
			v = "d;" + str(iObj.Radius1.Value)
			vArrValues.append(v)

			vArrNames.append("Radius2")
			v = "d;" + str(iObj.Radius2.Value)
			vArrValues.append(v)
			
			vArrNames.append("Height")
			v = "d;" + str(iObj.Height.Value)
			vArrValues.append(v)


		if iObj.isDerivedFrom("Part::Torus"):

			vType = "Torus"

			vArrNames.append("Radius1")
			v = "d;" + str(iObj.Radius1.Value)
			vArrValues.append(v)

			vArrNames.append("Radius2")
			v = "d;" + str(iObj.Radius2.Value)
			vArrValues.append(v)
			
			vArrNames.append("Angle1")
			v = "raw-angle;" + str(iObj.Angle1.Value)
			vArrValues.append(v)

			vArrNames.append("Angle2")
			v = "raw-angle;" + str(iObj.Angle2.Value)
			vArrValues.append(v)
			
			vArrNames.append("Angle3")
			v = "raw-angle;" + str(iObj.Angle3.Value)
			vArrValues.append(v)

		# set db for additional report
		if vType != "":
			setDBAdditional(iObj, vType, vArrNames, vArrValues, "", iCaller)

	except:
		
		# if there is wrong structure
		showError(iCaller, iObj, "setDecoration", "wrong structure")
		return -1

	return 0


# ###################################################################################################################
def setMounting(iObj, iCaller="setMounting"):

	try:

		# init variables
		vArrNames = []
		vArrValues = []
		vType = ""

		if iObj.isDerivedFrom("Part::Cylinder"):
		
			vType = gLang19
		
			s = str(iObj.Label)
		
			if s.find(" ") != -1:
				n = s.split(" ")[0]
				
				if n.find(",") != -1:
					m = n.split(",")[0]
					vType += ", " + str(m)
				else:
					vType += ", " + str(n)
					
			s = str(iObj.Label2)

			if s != "":
				vType += ", " + s

			vType += ", " + str(2 * iObj.Radius.Value) + " x " + str(int(iObj.Height.Value))

			vArrNames.append(gLang20)
			v = "d;" + str(2 * iObj.Radius.Value)
			vArrValues.append(v)

			vArrNames.append(gLang21)
			v = "d;" + str(iObj.Height.Value)
			vArrValues.append(v)

		# set db for additional report
		if vType != "":
			setDBAdditional(iObj, vType, vArrNames, vArrValues, "", iCaller)
		
	except:
		
		# if there is wrong structure
		showError(iCaller, iObj, "setMounting", "wrong structure")
		return -1

	return 0


# ###################################################################################################################
def setProfiles(iObj, iCaller="setProfiles"):

	try:

		# init variables
		vArrNames = []
		vArrValues = []
		vType = ""

		if iObj.isDerivedFrom("PartDesign::Thickness"):

			vType = gLang16

			# thickness
			vArrNames.append(gLang17)
			
			v = "d;" + str(iObj.Value.Value)
			vArrValues.append(v)
			
			# sizes
			vArrNames.append(gLang18)
			
			s = [ iObj.Base[0].Profile[0].Constraints[10].Value, 
				iObj.Base[0].Length.Value, 
				iObj.Base[0].Profile[0].Constraints[9].Value ]
			s.sort()
			
			v1 = getUnit(s[0], "d", iCaller)
			v2 = getUnit(s[1], "d", iCaller)
			v3 = getUnit(s[2], "d", iCaller)
			
			v = ""
			v += v1 + " " + sUnitsMetric
			v += " x "
			v += v2 + " " + sUnitsMetric
			v += " x "
			v += v3 + " " + sUnitsMetric
			
			v = "string;" + v
			
			vArrValues.append(v)

		if iObj.isDerivedFrom("Part::FeaturePython") and iObj.Name.startswith("Structure"):

			vType = gLang16

			# thickness
			vArrNames.append(gLang17)

			v1 = getUnit(iObj.Base.t1.Value, "d", iCaller)
			v2 = getUnit(iObj.Base.t2.Value, "d", iCaller)
			
			v = ""
			v += v1 + " " + sUnitsMetric
			v += " x "
			v += v2 + " " + sUnitsMetric
			
			v = "string;" + v
			
			vArrValues.append(v)
			
			# sizes
			vArrNames.append(gLang18)
			
			s = [ iObj.Base.W.Value, 
				iObj.Base.H.Value, 
				iObj.ComputedLength.Value ]
			s.sort()
			
			v1 = getUnit(s[0], "d", iCaller)
			v2 = getUnit(s[1], "d", iCaller)
			v3 = getUnit(s[2], "d", iCaller)
			
			v = ""
			v += v1 + " " + sUnitsMetric
			v += " x "
			v += v2 + " " + sUnitsMetric
			v += " x "
			v += v3 + " " + sUnitsMetric
			
			v = "string;" + v
			
			vArrValues.append(v)

		# set db for additional report
		if vType != "":
			setDBAdditional(iObj, vType, vArrNames, vArrValues, "", iCaller)

	except:
		
		# if there is wrong structure
		showError(iCaller, iObj, "setProfiles", "wrong structure")
		return -1

	return 0


# ###################################################################################################################
def setMeasurementsList(iObj, iCaller="setMeasurementsList"):

	try:

		# init variables
		vArrNames = []
		vArrValues = []
		vType = ""

		if (
			iObj.isDerivedFrom("App::MeasureDistance") or             # support for FreeCAD 0.21
			iObj.isDerivedFrom("Measure::MeasureDistanceDetached")    # support for FreeCAD 1.0
			):

			arr = str(iObj.Label2).split(", ")
			
			n = str(arr[0])
			sub = str(arr[len(arr)-1])
			
			# set key
			vType = gLang23 + ", " + n
			
			# add existing entries
			if vType in dbARN.keys():
				
				vArrNames.append(dbARN[vType])
				vArrValues.append(dbARV[vType])
			
			# add new entry
			
			# set name for entry
			v = str(sub)
			vArrNames.append(v)
			
			# set value for entry
			v = "d;" + str(iObj.Distance.Value)
			vArrValues.append(v)

		# set db for additional report
		if vType != "":
			setDBAdditional(iObj, vType, vArrNames, vArrValues, vType, iCaller)

	except:
		
		# if there is wrong structure
		showError(iCaller, iObj, "setMeasurementsList", "wrong structure")
		return -1

	return 0


# ###################################################################################################################
def setGrainDirection(iObj, iCaller="setGrainDirection"):

	try:

		# init variables
		vArrNames = []
		vArrValues = []
		vType = ""

		if hasattr(iObj, "Grain"):

			faces = iObj.Grain

			i = 1
			for f in faces:
			
				if str(f) != "x":
					v = "Face" + str(i)
					vArrNames.append(v)
					
					if str(f) == "h":
						v = "string;" + gLang25
					if str(f) == "v":
						v = "string;" + gLang26
					
					vArrValues.append(v)
	
				i = i + 1

			# set key
			vType = gLang24 + ", " + str(iObj.Label)

		# set db for additional report
		if vType != "":
			setDBAdditional(iObj, vType, vArrNames, vArrValues, "", iCaller)

	except:
		
		# if there is wrong structure
		showError(iCaller, iObj, "setGrainDirection", "wrong structure")
		return -1

	return 0


# ###################################################################################################################
# Furniture parts selector - add objects to db only via this selector
# ###################################################################################################################


# ###################################################################################################################
def selectFurniturePart(iObj, iCaller="selectFurniturePart"):

	# normal reports
	if sLTF != "c" and sLTF != "p":

		# support for Part::Box
		if iObj.isDerivedFrom("Part::Box"):
			setCube(iObj, iCaller)
    
		# support for PartDesign::Pad
		elif iObj.isDerivedFrom("PartDesign::Pad"):
			setPad(iObj, iCaller)

		# support for Part::Extrusion
		elif iObj.isDerivedFrom("Part::Extrusion"):
			setExtrusion(iObj, iCaller)

		else:
			# support for custom objects
			try:
				test = iObj.Width.Value
				test = iObj.Height.Value
				test = iObj.Length.Value
				setCustomObject(iObj, iCaller)
				
			except:
				skip = 1

	# constraints reports
	else:

		# only named constraints
		if sLTF == "c":
			if (
				iObj.isDerivedFrom("PartDesign::Pad") or
				iObj.isDerivedFrom("PartDesign::Pocket") or 
				iObj.isDerivedFrom("Part::Extrusion")
				):
				setConstraints(iObj, iCaller)

		# pads (all constraints)
		if sLTF == "p":
			if (
				iObj.isDerivedFrom("PartDesign::Pad") or
				iObj.isDerivedFrom("PartDesign::Pocket") or 
				iObj.isDerivedFrom("Part::Extrusion") 
				):
				setAllConstraints(iObj, iCaller)

	# constraints or detailed
	if sLTF == "c" or sLTF == "d":

		# support for pilot holes and countersinks
		if iObj.isDerivedFrom("PartDesign::Hole"):
			setConstraints(iObj, iCaller)

	# additional report - measurements
	if sARME == True:
		setMeasurementsList(iObj, iCaller)

	# additional report - mounting
	if sARM == True:
		setMounting(iObj, iCaller)
		
	# additional report - profiles
	if sARP == True:
		setProfiles(iObj, iCaller)

	# additional report - decoration
	if sARD == True:
		setDecoration(iObj, iCaller)
	
	# additional report - grain direction
	if sARGD == True:
		setGrainDirection(iObj, iCaller)
	
	# skip not supported furniture parts with no error
	# Sheet, Transformations will be handling later
	return 0


# ###################################################################################################################
# Support for transformations of base furniture parts
# ###################################################################################################################


# ###################################################################################################################
def setAppPart(iObj, iCaller="setAppPart"):

	# support for LinkGroup on Part
	if iObj.isDerivedFrom("App::Part"):

		try:

			# set reference point to the objects list
			key = iObj.Group

			# call scan for each object at the list
			scanObjects(key, iCaller)
		
		except:
			
			# if there is wrong structure
			showError(iCaller, iObj, "setAppPart", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setAppLinkGroup(iObj, iCaller="setAppLinkGroup"):

	# support for LinkGroup
	if iObj.isDerivedFrom("App::LinkGroup"):

		try:

			# set reference point to the objects list
			key = iObj.ElementList

			# call scan for each object at the list
			scanObjects(key, iCaller)
		
		except:
			
			# if there is wrong structure
			showError(iCaller, iObj, "setAppLinkGroup", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setAppLink(iObj, iCaller="setAppLink"):

	# support for Link
	if iObj.isDerivedFrom("App::Link"):

		try:
			
			# set reference point to the objects list
			key = iObj.LinkedObject

			# select and add furniture part
			scanObjects([ key ], iCaller)
		
		except:
			
			# if there is wrong structure
			showError(iCaller, iObj, "setAppLink", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setAssembly(iObj, iCaller="setAssembly"):

	# support for Link
	if (
		iObj.isDerivedFrom("Assembly::AssemblyObject") or
		iObj.isDerivedFrom("Assembly::AssemblyLink") 
		):

		try:
			
			# set reference point to the assembly object
			for gm in iObj.Group:
				if gm.isDerivedFrom("App::Link"):
					keys = [ gm.LinkedObject ]
				
				elif gm.isDerivedFrom("Assembly::AssemblyLink"):
					keys = [ gm.Group ]

				else:
					keys = []

				# parse only the base object from assembly
				for key in keys:
					scanObjects([ key ], iCaller)
		except:
			
			# if there is wrong structure
			showError(iCaller, iObj, "setAssembly", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setPartCut(iObj, iCaller="setPartCut"):

	# support for Cut
	if iObj.isDerivedFrom("Part::Cut"):

		try:

			# set reference point to the objects list
			key = iObj.OutList

			# call scan for each object at the list
			scanObjects(key, iCaller)
		
		except:
			
			# if there is wrong structure
			showError(iCaller, iObj, "setPartCut", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setBody(iObj, iCaller="setBody"):

	# support for Body object type only
	if iObj.isDerivedFrom("PartDesign::Body") and iObj.Name.startswith("Body"):

		try:

			# set reference point to the Body objects list
			key = iObj.Group

			# call scan for each object at the list
			scanObjects(key, iCaller)
		
		except:
			
			# if there is wrong structure
			showError(iCaller, iObj, "setBody", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setPartMirroring(iObj, iCaller="setPartMirroring"):

	# support for Part :: Mirroring FreeCAD feature
	if iObj.isDerivedFrom("Part::Mirroring"):

		try:

			# set reference point to the furniture part
			key = iObj.Source

			# select and add furniture part
			scanObjects([ key ], iCaller)

		except:

			# if there is wrong structure
			showError(iCaller, iObj, "setPartMirroring", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setDraftArray(iObj, iCaller="setDraftArray"):

	# support for Array FreeCAD feature
	if iObj.isDerivedFrom("Part::FeaturePython") and iObj.Name.startswith("Array"):

		try:

			# set reference point to the furniture part
			key = iObj.Base

			if iObj.ArrayType == "polar":
				
				# without the base furniture part
				vArray = iObj.NumberPolar - 1
			else:
				
				# without the base furniture part
				vArray = (iObj.NumberX * iObj.NumberY * iObj.NumberZ) - 1

			# array on array
			if iCaller == "self":
				vArray = vArray + 1

			# if array on array add base too
			if key.isDerivedFrom("Part::FeaturePython") and key.Name.startswith("Array"):
				
				k = 0
				while k < vArray:
					setDraftArray(key, "self")
					k = k + 1
			
			# array on Compound
			elif key.isDerivedFrom("Part::Compound"):
				
				for c in key.Links:
					k = 0
					while k < vArray:
						scanObjects([ c ], iCaller)
						k = k + 1
				
			# single array
			else:
			
				k = 0
				while k < vArray:
					scanObjects([ key ], iCaller)
					k = k + 1

		except:
			
			# if there is wrong structure
			showError(iCaller, iObj, "setDraftArray", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setDraftClone(iObj, iCaller="setDraftClone"):

	# support for Clone FreeCAD feature
	if iObj.Name.startswith("Clone"):

		try:

			# set reference point to the Clone objects list
			try:

				# for group Clone
				if iObj.isDerivedFrom("Part::FeaturePython"):
					key = iObj.Objects[0].Group

				# for Clone as PartDesign :: FeatureBase
				if iObj.isDerivedFrom("PartDesign::FeatureBase"):
					key = [ iObj.BaseFeature ]

			except:

				# for single object Clone
				key = iObj.Objects


			# call scanner for each object at the list
			scanObjects(key, iCaller)

		except:
			
			# if there is wrong structure
			showError(iCaller, iObj, "setDraftClone", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setPartDesignMirrored(iObj, iCaller="setPartDesignMirrored"):

	# support for Single Mirror FreeCAD feature
	if iObj.isDerivedFrom("PartDesign::Mirrored"):

		try:

			# skip Mirrored from MultiTransform with no error
			if len(iObj.Originals) == 0:
				return 0

			# set reference point to the base furniture part
			key = iObj.Originals[0]

			# if object is Mirror this create new furniture part
			scanObjects([ key ], iCaller)
		
		except:
			
			# if there is wrong structure
			showError(iCaller, iObj, "setPartDesignMirrored", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setPartDesignLinearPattern(iObj, iCaller="setPartDesignLinearPattern"):
	
	# support for LinearPattern FreeCAD feature
	if iObj.isDerivedFrom("PartDesign::LinearPattern"):

		try:

			# skip LinearPattern from MultiTransform with no error
			if len(iObj.Originals) == 0:
				return 0

			# set number of occurrences
			oc = iObj.Occurrences

			k = 0
			if oc > 0:
				
				# loop for each occurrence without base element
				while k < oc - 1:

					# set reference object (only one is supported for now)
					key = iObj.Originals[0]

					# select furniture part
					scanObjects([ key ], iCaller)
					k = k + 1
		except:

			# if there is wrong structure
			showError(iCaller, iObj, "setPartDesignLinearPattern", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
def setPartDesignMultiTransform(iObj, iCaller="setPartDesignMultiTransform"):
	
	# support for MultiTransform FreeCAD feature
	if iObj.isDerivedFrom("PartDesign::MultiTransform"):

		try:

			# set variables
			mirror = 0
			linear = 0
			
			for t in iObj.Transformations:

				if t.isDerivedFrom("PartDesign::Mirrored"):
					mirror = mirror + 1

				if t.isDerivedFrom("PartDesign::LinearPattern"):
					linear = linear + t.Occurrences

			# mirror makes 2 elements but each mirror in MultiTransform makes 
			# next mirror but using current transformed object, so this will raise 
			# the number of mirrors to the power, also you have to remove the 
			# base furniture part already added
			mirror = (2 ** mirror)

			# stay as it is
			linear = linear

			# if no such transformation type
			if linear == 0:
				linear = 1
			if mirror == 0:
				mirror = 1

			# calculate number of base elements
			lenT = (linear * mirror) - 1

			# for number off transformations
			k = 0
			while k < lenT:

				# select furniture part for all objects
				for key in iObj.Originals:
					scanObjects([ key ], iCaller)

				k = k + 1

		except:

			# if there is wrong structure
			showError(iCaller, iObj, "setPartDesignMultiTransform", "wrong structure")
			return -1
	
	return 0


# ###################################################################################################################
# Scan objects (MAIN CALCULATIONS LOOP)
# ###################################################################################################################

# ###################################################################################################################
def getCutContentPath(iObj, iType, iCaller="getCutContentPath"):

	visibility = True
	assign = ""
	
	try:
		# not check Cut containers
		if not iObj.isDerivedFrom("Part::Cut"):
			
			# if is Base but the Tool is called
			if str(iObj.Name) == str(iObj.InList[0].Base.Name):
				if iType == "Tool":
					visibility = False
	
			# if is Tool but the Base is called
			if str(iObj.Name) == str(iObj.InList[0].Tool.Name):
				if iType == "Base":
					visibility = False

	# if there is no Cut structure
	except:
		skip = 1

	return visibility


# ###################################################################################################################
def getParentVisibility(iObj, iCaller="getParentVisibility"):

	# set starting point if there is no parent
	if gCallerObj.Visibility == True:
		v = True
	else:
		v = False

	# try to get parent
	try:
		if iObj.InList[0].Visibility == True:
			v = True
		else:
			v = False
	
	# if there is no correct parent
	except:
		skip = 1

	return v


# ###################################################################################################################
def getInheritedVisibility(iObj, iCaller="getInheritedVisibility"):

	# set starting point
	v = True
	
	try:

		# if the caller highest object is visible break
		if gCallerObj.Visibility == True:
			return True
		
		# inherit visibility from the highest container only if the object is hidden
		for o in iObj.InListRecursive:
			
			if (
				o.isDerivedFrom("App::LinkGroup") or 
				o.isDerivedFrom("Part::Compound") or 
				o.isDerivedFrom("Part::Cut") or 
				o.isDerivedFrom("App::Part") or 
				o.isDerivedFrom("PartDesign::Body") 
				):
				
				if o.Visibility == False:
					v = False
					
					# first hidden LinkGroup
					if o.isDerivedFrom("App::LinkGroup"):
						return False
				else:
					v = True

	except:
		skip = 1

	return v


# ###################################################################################################################
def getAssemblyObject(iObj, iCaller="getAssemblyObject"):

	try:
		if (
			iObj.isDerivedFrom("Assembly::AssemblyObject") or 
			iObj.isDerivedFrom("Assembly::AssemblyLink") 
			):
			return True
		else:
			return False
	except:
		skip = 1
	
	return False
	

# ###################################################################################################################
def scanObjects(iOBs, iCaller="main"):
	
	global gCallerObj

	# search all objects in document and set database for correct ones
	for obj in iOBs:

		# set currently parsed object called from main loop
		if iCaller == "main":
			gCallerObj = obj

		# ##################################################################
		# debug section
		# ##################################################################
		
		if gDebugLoop == 1:
			
			FreeCAD.Console.PrintMessage("\n\n")
			FreeCAD.Console.PrintMessage("scanObjects")
			FreeCAD.Console.PrintMessage("\n")
			FreeCAD.Console.PrintMessage("Caller function: "+str(iCaller))
			FreeCAD.Console.PrintMessage("\n")
			FreeCAD.Console.PrintMessage("Caller object: "+str(gCallerObj.Label))
			FreeCAD.Console.PrintMessage("\n")
			FreeCAD.Console.PrintMessage("Parsed object: "+str(obj.Label))
			
		# ##################################################################
		# check if parsing is allowed
		# ##################################################################
		
		# check copy listing special property
		if hasattr(obj, "BOM"):
			if obj.BOM == False:
				continue

		# simple object visibility
		if sTVF == "on":
			if obj.Visibility == False:
				continue

		# inherit visibility from nearest parent
		if sTVF == "parent":
			if getParentVisibility(obj, iCaller) == False:
				continue

		# inherit visibility from highest container
		# linking from middle visible container in highest hidden container
		if sTVF == "inherit":
			if getInheritedVisibility(obj, iCaller) == False:
				continue

		# show only Base objects from Part :: Cut
		if sPartCut == "base":
			if getCutContentPath(obj, "Base", iCaller) == False:
				continue
				
		# show only Tool objects from Part :: Cut
		if sPartCut == "tool":
			if getCutContentPath(obj, "Tool", iCaller) == False:
				continue

		# ##################################################################
		# support for Assembly workbench objects
		# ##################################################################

		if sPPM == "assembly":
			
			# start assebly parse way only for assembly objects
			if getAssemblyObject(obj, iCaller) == True:
				setAssembly(obj)
			
			# users have other objects, not used in assembly, 
			# so go tru assembly path only
			# but you have to allow for assembly calls to parse 
			# objects inside assembly
			if iCaller == "main":
				continue

		# ##################################################################
		# debug parser section
		# ##################################################################
		
		if gDebugParser == 1:
			
			FreeCAD.Console.PrintMessage("\n\n")
			FreeCAD.Console.PrintMessage("scanObjects")
			FreeCAD.Console.PrintMessage("\n")
			FreeCAD.Console.PrintMessage("Caller function: "+str(iCaller))
			FreeCAD.Console.PrintMessage("\n")
			FreeCAD.Console.PrintMessage("Caller object: "+str(gCallerObj.Label))
			FreeCAD.Console.PrintMessage("\n")
			FreeCAD.Console.PrintMessage("Parsed object: "+str(obj.Label))
		
		# ##################################################################
		# common parser section
		# ##################################################################

		# select and set furniture part
		selectFurniturePart(obj)

		# set transformations
		setPartMirroring(obj)
		setDraftArray(obj)
		setPartDesignLinearPattern(obj)
		setPartDesignMirrored(obj)
		setPartDesignMultiTransform(obj)
		setDraftClone(obj)
		setAppLink(obj)
		
		if iCaller != "main":
			setAppPart(obj)
			setPartCut(obj)
			setBody(obj)
			setAppLinkGroup(obj)


# ###################################################################################################################
# View types (regiester each view at view selector)
# ###################################################################################################################


# ###################################################################################################################
def initLang():

	global gLang1
	global gLang2
	global gLang3
	global gLang4
	global gLang5
	global gLang6
	global gLang7
	global gLang8
	global gLang9
	global gLang10
	global gLang11
	global gLang12
	global gLang13
	global gLang14
	global gLang15
	global gLang16
	global gLang17
	global gLang18
	global gLang19
	global gLang20
	global gLang21
	global gLang22
	global gLang23
	global gLang24
	global gLang25
	global gLang26

	# Polish language
	if sLang  == "pl":

		gLang1 = "Nazwa"
		gLang2 = "Ilość"
		gLang3 = "Wymiary"
		gLang4 = "Grubość"
		
		if sUnitsArea == "mm":
			gLang5 = "mm2"
		if sUnitsArea == "m":
			gLang5 = "m2"
		if sUnitsArea == "in":
			gLang5 = "in2"

		gLang6 = "Podsumowanie dla grup"
		gLang7 = "Podsumowanie dla grubości"
		gLang8 = "Długość obrzeża"
		gLang9 = "Długość"
		gLang10 = "Obrzeże bez okleiny"
		gLang11 = "Potrzebna okleina"
		gLang12 = "brzeg"
		gLang13 = "wierzch"
		gLang14 = "wymiary"
		gLang15 = "Głębokość"
		gLang16 = "Profil konstrukcyjny"
		gLang17 = "Grubość"
		gLang18 = "Wymiary"
		gLang19 = "Punkty montażowe"
		gLang20 = "Średnica"
		gLang21 = "Długość"
		gLang22 = "Obszar"
		gLang23 = "Własne pomiary"
		gLang24 = "Kierunek słojów"
		gLang25 = "poziomo"
		gLang26 = "pionowo"

	# English language
	else:

		gLang1 = "Name"
		gLang2 = "Quantity"
		gLang3 = "Dimensions"
		gLang4 = "Thickness"

		if sUnitsArea == "mm":
			gLang5 = "mm2"
		if sUnitsArea == "m":
			gLang5 = "m2"
		if sUnitsArea == "in":
			gLang5 = "in2"

		gLang6 = "Summary by groups"
		gLang7 = "Summary by thickness"
		gLang8 = "Edge size"
		gLang9 = "Length"
		gLang10 = "Edge without veneer"
		gLang11 = "Needed veneer for edge"
		gLang12 = "edge"
		gLang13 = "surface"
		gLang14 = "dimensions"
		gLang15 = "Depth"
		gLang16 = "Construction profile"
		gLang17 = "Thickness"
		gLang18 = "Dimensions"
		gLang19 = "Mounting points"
		gLang20 = "Diameter"
		gLang21 = "Length"
		gLang22 = "Area"
		gLang23 = "Custom measurements"
		gLang24 = "Grain Direction"
		gLang25 = "horizontal"
		gLang26 = "vertical"


# ###################################################################################################################
def setViewQ(iCaller="setViewQ"):

	global gSheet
	global gSheetRow

	# set headers
	gSheet.set("A1", gLang2)
	gSheet.set("C1", gLang3)
	gSheet.set("F1", gLang4)
	gSheet.set("G1", gLang5)

	# text header decoration
	gSheet.setStyle("A1:G1", "bold", "add")

	# merge cells
	gSheet.mergeCells("A1:B1")
	gSheet.mergeCells("C1:E1")

	# set background
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.setBackground(vCell, gHeadCS)

	# go to next spreadsheet row
	gSheetRow = gSheetRow + 1

	# add values
	for key in dbDA.keys():

		a = key.split(":")

		gSheet.set("A" + str(gSheetRow), toSheet(dbDQ[key], "string", iCaller) + " x")
		gSheet.set("C" + str(gSheetRow), toSheet(a[1], "d", iCaller))
		gSheet.set("D" + str(gSheetRow), "x")
		gSheet.set("E" + str(gSheetRow), toSheet(a[2], "d", iCaller))
		gSheet.set("F" + str(gSheetRow), toSheet(a[0], "d", iCaller))
		gSheet.set("G" + str(gSheetRow), toSheet(dbDA[key], "area", iCaller))

		# merge cells
		vCell = "A" + str(gSheetRow) + ":B" + str(gSheetRow)	
		gSheet.mergeCells(vCell)

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

	# cell sizes
	gSheet.setColumnWidth("A", 215)
	gSheet.setColumnWidth("B", 80)
	gSheet.setColumnWidth("C", 90)
	gSheet.setColumnWidth("D", 20)
	gSheet.setColumnWidth("E", 90)
	gSheet.setColumnWidth("F", 100)
	gSheet.setColumnWidth("G", 120)

	# alignment
	gSheet.setAlignment("A1:A" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("B1:B" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("C1:C" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("D1:D" + str(gSheetRow), "center", "keep")
	gSheet.setAlignment("E1:E" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("F1:F" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("G1:G" + str(gSheetRow), "right", "keep")

	# fix for center header text in merged cells
	gSheet.setAlignment("C1:C1", "center", "keep")
	gSheet.setAlignment("D1:D1", "center", "keep")
	gSheet.setAlignment("E1:E1", "center", "keep")

	# ########################################################
	# thickness part - depends on view columns order, so better here
	# ########################################################

	if sATS == False:
		return

	# add summary title for thickness
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.mergeCells(vCell)
	gSheet.set(vCell, gLang7)
	gSheet.setStyle(vCell, "bold", "add")
	gSheet.setAlignment(vCell, "left", "keep")
	gSheet.setBackground(vCell, gHeadCS)

	# go to next spreadsheet row
	gSheetRow = gSheetRow + 1
	
	for key in dbTQ.keys():

		gSheet.set("A" + str(gSheetRow), toSheet(dbTQ[key], "string", iCaller) + " x")
		gSheet.set("F" + str(gSheetRow), toSheet(key, "d", iCaller))
		gSheet.set("G" + str(gSheetRow), toSheet(dbTA[key], "area", iCaller))
		gSheet.setAlignment("A" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("B" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("F" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("G" + str(gSheetRow), "right", "keep")

		# merge cells
		vCell = "A" + str(gSheetRow) + ":B" + str(gSheetRow)	
		gSheet.mergeCells(vCell)

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1


# ###################################################################################################################
def setViewA(iCaller="setViewA"):

	global gSheet
	global gSheetRow

	# set headers
	gSheet.set("A1", "Length")
	gSheet.set("B1", "Width")
	gSheet.set("C1", "Qty")
	gSheet.set("D1", "Material")
	gSheet.set("E1", "Label")
	gSheet.set("F1", "Enabled")
	gSheet.set("G1", "Grain direction")
	gSheet.set("H1", "Top band")
	gSheet.set("I1", "Left band")
	gSheet.set("J1", "Bottom band")
	gSheet.set("K1", "Right band")
	
	# text header decoration
	gSheet.setStyle("A1:K1", "bold", "add")

	# set background
	vCell = "A" + str(gSheetRow) + ":K" + str(gSheetRow)
	gSheet.setBackground(vCell, gHeadCS)

	# go to next spreadsheet row
	gSheetRow = gSheetRow + 1

	# add values
	for key in dbDQ.keys():
		
		# split key
		a = key.split(":")
		
		# split group
		group = a[3]
		label = a[3]
		grain = ""
		
		if group.find(", ") != -1:
			
			more = group.split(", ")
			label = more[0]
			g = more[1]
			
			if g == "grain horizontal":
				grain = "h"
			if g == "grain vertical":
				grain = "v"

		gSheet.set("A" + str(gSheetRow), toSheet(a[1], "string", iCaller)) 			# Length
		gSheet.set("B" + str(gSheetRow), toSheet(a[2], "string", iCaller)) 			# Width
		gSheet.set("C" + str(gSheetRow), toSheet(dbDQ[key], "string", iCaller)) 	# Qty
		gSheet.set("D" + str(gSheetRow), toSheet(a[0], "string", iCaller))			# Material
		gSheet.set("E" + str(gSheetRow), toSheet(label, "string", iCaller))			# Label
		gSheet.set("F" + str(gSheetRow), "true")									# Enabled
		gSheet.set("G" + str(gSheetRow), toSheet(grain, "string", iCaller))			# Grain direction
		gSheet.set("H" + str(gSheetRow), "")										# Top band
		gSheet.set("I" + str(gSheetRow), "")										# Left band
		gSheet.set("J" + str(gSheetRow), "")										# Bottom band
		gSheet.set("K" + str(gSheetRow), "")										# Right band
		
		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1
		
	# cell sizes
	gSheet.setColumnWidth("A", 100)
	gSheet.setColumnWidth("B", 100)
	gSheet.setColumnWidth("C", 70)
	gSheet.setColumnWidth("D", 100)
	gSheet.setColumnWidth("E", 100)
	gSheet.setColumnWidth("F", 70)
	gSheet.setColumnWidth("G", 120)
	gSheet.setColumnWidth("H", 100)
	gSheet.setColumnWidth("I", 100)
	gSheet.setColumnWidth("J", 100)
	gSheet.setColumnWidth("K", 100)

	# alignment
	gSheet.setAlignment("A1:A" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("B1:B" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("C1:C" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("D1:D" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("E1:E" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("F1:F" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("G1:G" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("H1:H" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("I1:I" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("J1:J" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("K1:K" + str(gSheetRow), "right", "keep")


# ###################################################################################################################
def setViewN(iCaller="setViewN"):

	global gSheet
	global gSheetRow

	# set headers
	gSheet.set("A1", gLang1)
	gSheet.set("B1", gLang3)
	gSheet.set("E1", gLang4)
	gSheet.set("F1", gLang2)
	gSheet.set("G1", gLang5)

	# text header decoration
	gSheet.setStyle("A1:G1", "bold", "add")

	# merge cells
	gSheet.mergeCells("B1:D1")

	# set background
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.setBackground(vCell, gHeadCS)

	# go to next spreadsheet row
	gSheetRow = gSheetRow + 1

	# add values
	for key in dbDA.keys():

		a = key.split(":")

		gSheet.set("A" + str(gSheetRow), toSheet(a[3], "string", iCaller))
		gSheet.set("B" + str(gSheetRow), toSheet(a[1], "d", iCaller))
		gSheet.set("C" + str(gSheetRow), "x")
		gSheet.set("D" + str(gSheetRow), toSheet(a[2], "d", iCaller))
		gSheet.set("E" + str(gSheetRow), toSheet(a[0], "d", iCaller))
		gSheet.set("F" + str(gSheetRow), toSheet(dbDQ[key], "string", iCaller))
		gSheet.set("G" + str(gSheetRow), toSheet(dbDA[key], "area", iCaller))

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

	# cell sizes
	gSheet.setColumnWidth("A", 215)
	gSheet.setColumnWidth("B", 90)
	gSheet.setColumnWidth("C", 20)
	gSheet.setColumnWidth("D", 90)
	gSheet.setColumnWidth("E", 100)
	gSheet.setColumnWidth("F", 80)
	gSheet.setColumnWidth("G", 120)

	# alignment
	gSheet.setAlignment("A1:A" + str(gSheetRow), "left", "keep")
	gSheet.setAlignment("B1:B" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("C1:C" + str(gSheetRow), "center", "keep")
	gSheet.setAlignment("D1:D" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("E1:E" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("F1:F" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("G1:G" + str(gSheetRow), "right", "keep")

	# fix for center header text in merged cells
	gSheet.setAlignment("B1:B1", "center", "keep")
	gSheet.setAlignment("C1:C1", "center", "keep")
	gSheet.setAlignment("D1:D1", "center", "keep")

	# ########################################################
	# thickness part - depends on view columns order, so better here
	# ########################################################

	if sATS == False:
		return

	# add summary title for thickness
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.mergeCells(vCell)
	gSheet.set(vCell, gLang7)
	gSheet.setStyle(vCell, "bold", "add")
	gSheet.setAlignment(vCell, "left", "keep")
	gSheet.setBackground(vCell, gHeadCS)

	# go to next spreadsheet row
	gSheetRow = gSheetRow + 1
	
	for key in dbTQ.keys():

		gSheet.set("E" + str(gSheetRow), toSheet(key, "d", iCaller))
		gSheet.set("F" + str(gSheetRow), toSheet(dbTQ[key], "string", iCaller))
		gSheet.set("G" + str(gSheetRow), toSheet(dbTA[key], "area", iCaller))
		gSheet.setAlignment("E" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("F" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("G" + str(gSheetRow), "right", "keep")

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1


# ###################################################################################################################
def setViewG(iCaller="setViewG"):

	global gSheet
	global gSheetRow

	# set headers
	gSheet.set("A1", gLang1)
	gSheet.set("B1", gLang4)
	gSheet.set("C1", gLang3)
	gSheet.set("F1", gLang2)
	gSheet.set("G1", gLang5)

	# text header decoration
	gSheet.setStyle("A1:G1", "bold", "add")

	# merge cells
	gSheet.mergeCells("C1:E1")

	# set background
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.setBackground(vCell, gHeadCS)

	# go to next spreadsheet row
	gSheetRow = gSheetRow + 1

	# add values
	for key in dbDA.keys():

		a = key.split(":")

		gSheet.set("A" + str(gSheetRow), toSheet(a[3], "string", iCaller))
		gSheet.set("B" + str(gSheetRow), toSheet(a[0], "d", iCaller))
		gSheet.set("C" + str(gSheetRow), toSheet(a[1], "d", iCaller))
		gSheet.set("D" + str(gSheetRow), "x")
		gSheet.set("E" + str(gSheetRow), toSheet(a[2], "d", iCaller))
		gSheet.set("F" + str(gSheetRow), toSheet(dbDQ[key], "string", iCaller))
		gSheet.set("G" + str(gSheetRow), toSheet(dbDA[key], "area", iCaller))

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

	# cell sizes
	gSheet.setColumnWidth("A", 215)
	gSheet.setColumnWidth("B", 100)
	gSheet.setColumnWidth("C", 90)
	gSheet.setColumnWidth("D", 20)
	gSheet.setColumnWidth("E", 90)
	gSheet.setColumnWidth("F", 80)
	gSheet.setColumnWidth("G", 120)

	# alignment
	gSheet.setAlignment("A1:A" + str(gSheetRow), "left", "keep")
	gSheet.setAlignment("B1:B" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("C1:C" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("D1:D" + str(gSheetRow), "center", "keep")
	gSheet.setAlignment("E1:E" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("F1:F" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("G1:G" + str(gSheetRow), "right", "keep")

	# fix for center header text in merged cells
	gSheet.setAlignment("C1:C1", "center", "keep")
	gSheet.setAlignment("D1:D1", "center", "keep")
	gSheet.setAlignment("E1:E1", "center", "keep")

	# ########################################################
	# thickness part - depends on view columns order, so better here
	# ########################################################

	if sATS == False:
		return

	# add summary title for thickness
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.mergeCells(vCell)
	gSheet.set(vCell, gLang7)
	gSheet.setStyle(vCell, "bold", "add")
	gSheet.setAlignment(vCell, "left", "keep")
	gSheet.setBackground(vCell, gHeadCS)

	# go to next spreadsheet row
	gSheetRow = gSheetRow + 1
	
	for key in dbTQ.keys():

		gSheet.set("B" + str(gSheetRow), toSheet(key, "d", iCaller))
		gSheet.set("F" + str(gSheetRow), toSheet(dbTQ[key], "string", iCaller))
		gSheet.set("G" + str(gSheetRow), toSheet(dbTA[key], "area", iCaller))
		gSheet.setAlignment("B" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("F" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("G" + str(gSheetRow), "right", "keep")

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1


# ###################################################################################################################
def setViewE(iCaller="setViewE"):

	global gSheet
	global gSheetRow


	# add values
	for key in dbDA.keys():

		# set headers
		gSheet.set("A" + str(gSheetRow), gLang1)
		gSheet.set("B" + str(gSheetRow), gLang3)
		gSheet.set("E" + str(gSheetRow), gLang4)
		gSheet.set("F" + str(gSheetRow), gLang2)
		gSheet.set("G" + str(gSheetRow), gLang5)
	
		# text header decoration
		vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCS)
	
		# alignment
		gSheet.setAlignment("A" + str(gSheetRow), "left", "keep")
		gSheet.setAlignment("B" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("C" + str(gSheetRow), "center", "keep")
		gSheet.setAlignment("D" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("E" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("F" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("G" + str(gSheetRow), "right", "keep")
	
		# merge cells
		vCell = "B" + str(gSheetRow) + ":D" + str(gSheetRow)
		gSheet.mergeCells(vCell)
	
		# fix for center header text in merged cells
		gSheet.setAlignment("B" + str(gSheetRow), "center", "keep")
		gSheet.setAlignment("C" + str(gSheetRow), "center", "keep")
		gSheet.setAlignment("D" + str(gSheetRow), "center", "keep")
	
		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

		a = key.split(":")

		gSheet.set("A" + str(gSheetRow), toSheet(a[3], "string", iCaller))
		gSheet.set("B" + str(gSheetRow), toSheet(a[1], "d", iCaller))
		gSheet.set("C" + str(gSheetRow), "x")
		gSheet.set("D" + str(gSheetRow), toSheet(a[2], "d", iCaller))
		gSheet.set("E" + str(gSheetRow), toSheet(a[0], "d", iCaller))
		gSheet.set("F" + str(gSheetRow), toSheet(dbDQ[key], "string", iCaller))
		gSheet.set("G" + str(gSheetRow), toSheet(dbDA[key], "area", iCaller))

		# alignment
		gSheet.setAlignment("A" + str(gSheetRow), "left", "keep")
		vCell = "B" + str(gSheetRow) + ":G" + str(gSheetRow)
		gSheet.setAlignment(vCell, "right", "keep")

		# if there are faces with edgeband
		faces = 0
		try:
			faces = str(dbEFD[key])
		except:
			faces = 0
		
		if faces != 0:
		
			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1
		
			# ####################################################
			# faces numbers
			# ####################################################

			# set header
			vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
			gSheet.setBackground(vCell, gHeadCS)
			gSheet.setStyle(vCell, "bold", "add")

			gSheet.set("A" + str(gSheetRow), "5")
			gSheet.set("B" + str(gSheetRow), "6")
			gSheet.set("D" + str(gSheetRow), "1")
			gSheet.set("E" + str(gSheetRow), "2")
			gSheet.set("F" + str(gSheetRow), "3")
			gSheet.set("G" + str(gSheetRow), "4")

			# alignment
			vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
			gSheet.setAlignment(vCell, "right", "keep")

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

			# ####################################################
			# faces names
			# ####################################################

			try:
				# try get values
				gSheet.set("A" + str(gSheetRow), toSheet(dbEFN[key][4], "string", iCaller))
				gSheet.set("B" + str(gSheetRow), toSheet(dbEFN[key][5], "string", iCaller))
				gSheet.set("D" + str(gSheetRow), toSheet(dbEFN[key][0], "string", iCaller))
				gSheet.set("E" + str(gSheetRow), toSheet(dbEFN[key][1], "string", iCaller))
				gSheet.set("F" + str(gSheetRow), toSheet(dbEFN[key][2], "string", iCaller))
				gSheet.set("G" + str(gSheetRow), toSheet(dbEFN[key][3], "string", iCaller))

			except:
				skip = 1

			# alignment
			vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
			gSheet.setAlignment(vCell, "right", "keep")

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

			# ####################################################
			# faces dimensions
			# ####################################################

			try:
			
				# try get values
				if dbEFD[key][4] > 0:
					gSheet.set("A" + str(gSheetRow), toSheet(dbEFD[key][4], "d", iCaller))
				if dbEFD[key][4] == -1:
					gSheet.set("A" + str(gSheetRow), gLang14)
				
				if dbEFD[key][5] > 0:
					gSheet.set("B" + str(gSheetRow), toSheet(dbEFD[key][5], "d", iCaller))
				if dbEFD[key][5] == -1:
					gSheet.set("B" + str(gSheetRow), gLang14)
					
				if dbEFD[key][0] > 0:
					gSheet.set("D" + str(gSheetRow), toSheet(dbEFD[key][0], "d", iCaller))
				if dbEFD[key][0] == -1:
					gSheet.set("D" + str(gSheetRow), gLang14)
				
				if dbEFD[key][1] > 0:
					gSheet.set("E" + str(gSheetRow), toSheet(dbEFD[key][1], "d", iCaller))
				if dbEFD[key][1] == -1:
					gSheet.set("E" + str(gSheetRow), gLang14)
					
				if dbEFD[key][2] > 0:
					gSheet.set("F" + str(gSheetRow), toSheet(dbEFD[key][2], "d", iCaller))
				if dbEFD[key][2] == -1:
					gSheet.set("F" + str(gSheetRow), gLang14)
					
				if dbEFD[key][3] > 0:
					gSheet.set("G" + str(gSheetRow), toSheet(dbEFD[key][3], "d", iCaller))
				if dbEFD[key][3] == -1:
					gSheet.set("G" + str(gSheetRow), gLang14)

			except:
				skip = 1

			# alignment
			vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
			gSheet.setAlignment(vCell, "right", "keep")

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

			# ####################################################
			# faces veneers
			# ####################################################

			try:
				# try get values
				gSheet.set("A" + str(gSheetRow), toSheet(dbEFV[key][4], "string", iCaller))
				gSheet.set("B" + str(gSheetRow), toSheet(dbEFV[key][5], "string", iCaller))
				gSheet.set("D" + str(gSheetRow), toSheet(dbEFV[key][0], "string", iCaller))
				gSheet.set("E" + str(gSheetRow), toSheet(dbEFV[key][1], "string", iCaller))
				gSheet.set("F" + str(gSheetRow), toSheet(dbEFV[key][2], "string", iCaller))
				gSheet.set("G" + str(gSheetRow), toSheet(dbEFV[key][3], "string", iCaller))

			except:
				skip = 1


		# alignment
		vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
		gSheet.setAlignment(vCell, "right", "keep")

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

		# empty line separator
		vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
		gSheet.mergeCells(vCell)

		# next entry or thickness summary
		gSheetRow = gSheetRow + 1

	# ########################################################
	# width part
	# ########################################################

	# cell sizes
	gSheet.setColumnWidth("A", 215)
	gSheet.setColumnWidth("B", 90)
	gSheet.setColumnWidth("C", 20)
	gSheet.setColumnWidth("D", 90)
	gSheet.setColumnWidth("E", 100)
	gSheet.setColumnWidth("F", 80)
	gSheet.setColumnWidth("G", 120)

	# ########################################################
	# thickness part - depends on view columns order, so better here
	# ########################################################

	if sATS == False:
		return

	# add summary title for thickness
	vCell = "A" + str(gSheetRow) + ":D" + str(gSheetRow)
	gSheet.mergeCells(vCell)
	gSheet.set(vCell, gLang7)

	# header
	gSheet.set("E" + str(gSheetRow), gLang4)
	gSheet.set("F" + str(gSheetRow), gLang2)
	gSheet.set("G" + str(gSheetRow), gLang5)

	# alignment
	gSheet.setAlignment("A" + str(gSheetRow), "left", "keep")
	gSheet.setAlignment("E" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("F" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("G" + str(gSheetRow), "right", "keep")

	# decoration
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.setStyle(vCell, "bold", "add")
	gSheet.setBackground(vCell, gHeadCS)

	# go to next spreadsheet row
	gSheetRow = gSheetRow + 1
	
	for key in dbTQ.keys():

		gSheet.set("E" + str(gSheetRow), toSheet(key, "d", iCaller))
		gSheet.set("F" + str(gSheetRow), toSheet(dbTQ[key], "string", iCaller))
		gSheet.set("G" + str(gSheetRow), toSheet(dbTA[key], "area", iCaller))
		gSheet.setAlignment("E" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("F" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("G" + str(gSheetRow), "right", "keep")

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1


# ###################################################################################################################
def setViewD(iCaller="setViewD"):

	global gSheet
	global gSheetRow

	# add values
	for key in dbDA.keys():

		a = key.split(":")

		# text header decoration
		vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCS)
		gSheet.mergeCells(vCell)

		# set group name
		gSheet.set("A" + str(gSheetRow), toSheet(a[4], "string", iCaller))

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

		# set headers
		gSheet.set("B" + str(gSheetRow), gLang3)
		gSheet.set("E" + str(gSheetRow), gLang4)
		gSheet.set("F" + str(gSheetRow), gLang2)
		gSheet.set("G" + str(gSheetRow), gLang5)
	
		# text header decoration
		vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCW)
	
		# alignment
		gSheet.setAlignment("A" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("B" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("C" + str(gSheetRow), "center", "keep")
		gSheet.setAlignment("D" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("E" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("F" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("G" + str(gSheetRow), "right", "keep")
	
		# merge cells
		vCell = "B" + str(gSheetRow) + ":D" + str(gSheetRow)
		gSheet.mergeCells(vCell)
	
		# fix for center header text in merged cells
		gSheet.setAlignment("B" + str(gSheetRow), "center", "keep")
		gSheet.setAlignment("C" + str(gSheetRow), "center", "keep")
		gSheet.setAlignment("D" + str(gSheetRow), "center", "keep")
	
		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

		gSheet.set("B" + str(gSheetRow), toSheet(a[1], "d", iCaller))
		gSheet.set("C" + str(gSheetRow), "x")
		gSheet.set("D" + str(gSheetRow), toSheet(a[2], "d", iCaller))
		gSheet.set("E" + str(gSheetRow), toSheet(a[0], "d", iCaller))
		gSheet.set("F" + str(gSheetRow), toSheet(dbDQ[key], "string", iCaller))
		gSheet.set("G" + str(gSheetRow), toSheet(dbDA[key], "area", iCaller))

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

		# alignment
		vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
		gSheet.setAlignment(vCell, "right", "keep")

		# if there are faces with edgeband
		faces = 0
		try:
			faces = str(dbEFD[key])
		except:
			faces = 0
		
		if faces != 0:

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1
			
			# ####################################################
			# faces numbers
			# ####################################################

			# set header
			vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
			gSheet.setBackground(vCell, gHeadCW)
			gSheet.setStyle(vCell, "bold", "add")

			gSheet.set("A" + str(gSheetRow), "5")
			gSheet.set("B" + str(gSheetRow), "6")
			gSheet.set("D" + str(gSheetRow), "1")
			gSheet.set("E" + str(gSheetRow), "2")
			gSheet.set("F" + str(gSheetRow), "3")
			gSheet.set("G" + str(gSheetRow), "4")

			# alignment
			vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
			gSheet.setAlignment(vCell, "right", "keep")

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

			# ####################################################
			# faces names
			# ####################################################

			try:
				# try get values
				gSheet.set("A" + str(gSheetRow), toSheet(dbEFN[key][4], "string", iCaller))
				gSheet.set("B" + str(gSheetRow), toSheet(dbEFN[key][5], "string", iCaller))
				gSheet.set("D" + str(gSheetRow), toSheet(dbEFN[key][0], "string", iCaller))
				gSheet.set("E" + str(gSheetRow), toSheet(dbEFN[key][1], "string", iCaller))
				gSheet.set("F" + str(gSheetRow), toSheet(dbEFN[key][2], "string", iCaller))
				gSheet.set("G" + str(gSheetRow), toSheet(dbEFN[key][3], "string", iCaller))

			except:
				skip = 1

			# alignment
			vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
			gSheet.setAlignment(vCell, "right", "keep")

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

			# ####################################################
			# faces dimensions
			# ####################################################

			try:
			
				# try get values
				if dbEFD[key][4] > 0:
					gSheet.set("A" + str(gSheetRow), toSheet(dbEFD[key][4], "d", iCaller))
				if dbEFD[key][4] == -1:
					gSheet.set("A" + str(gSheetRow), gLang14)
				
				if dbEFD[key][5] > 0:
					gSheet.set("B" + str(gSheetRow), toSheet(dbEFD[key][5], "d", iCaller))
				if dbEFD[key][5] == -1:
					gSheet.set("B" + str(gSheetRow), gLang14)
					
				if dbEFD[key][0] > 0:
					gSheet.set("D" + str(gSheetRow), toSheet(dbEFD[key][0], "d", iCaller))
				if dbEFD[key][0] == -1:
					gSheet.set("D" + str(gSheetRow), gLang14)
				
				if dbEFD[key][1] > 0:
					gSheet.set("E" + str(gSheetRow), toSheet(dbEFD[key][1], "d", iCaller))
				if dbEFD[key][1] == -1:
					gSheet.set("E" + str(gSheetRow), gLang14)
					
				if dbEFD[key][2] > 0:
					gSheet.set("F" + str(gSheetRow), toSheet(dbEFD[key][2], "d", iCaller))
				if dbEFD[key][2] == -1:
					gSheet.set("F" + str(gSheetRow), gLang14)
					
				if dbEFD[key][3] > 0:
					gSheet.set("G" + str(gSheetRow), toSheet(dbEFD[key][3], "d", iCaller))
				if dbEFD[key][3] == -1:
					gSheet.set("G" + str(gSheetRow), gLang14)

			except:
				skip = 1

			# alignment
			vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
			gSheet.setAlignment(vCell, "right", "keep")

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

			# ####################################################
			# faces veneers
			# ####################################################

			try:
				# try get values
				gSheet.set("A" + str(gSheetRow), toSheet(dbEFV[key][4], "string", iCaller))
				gSheet.set("B" + str(gSheetRow), toSheet(dbEFV[key][5], "string", iCaller))
				gSheet.set("D" + str(gSheetRow), toSheet(dbEFV[key][0], "string", iCaller))
				gSheet.set("E" + str(gSheetRow), toSheet(dbEFV[key][1], "string", iCaller))
				gSheet.set("F" + str(gSheetRow), toSheet(dbEFV[key][2], "string", iCaller))
				gSheet.set("G" + str(gSheetRow), toSheet(dbEFV[key][3], "string", iCaller))

			except:
				skip = 1

			# alignment
			vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
			gSheet.setAlignment(vCell, "right", "keep")

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

		# ########################################################
		# holes constraints part
		# ########################################################
		
		try:
			# set reference for object holes
			vHoles = dbCNOH[str(a[3])][:-1].split(":")
	
			for vKey in vHoles:
				
				# go to next spreadsheet row
				gSheetRow = gSheetRow + 1
			
				# set object header
				vCell = "A" + str(gSheetRow)
				vStr = str(dbCNQ[vKey]) + " x "
				gSheet.set(vCell, vStr)
				gSheet.setAlignment(vCell, "right", "keep")
				gSheet.setStyle(vCell, "bold", "add")
				gSheet.setBackground(vCell, gHeadCW)
		
				vCell = "B" + str(gSheetRow) + ":G" + str(gSheetRow)
				vStr = str(vKey)
				gSheet.set(vCell, vStr)
				gSheet.mergeCells(vCell)	
				gSheet.setAlignment(vCell, "left", "keep")
				gSheet.setStyle(vCell, "bold", "add")
				gSheet.setBackground(vCell, gHeadCW)
	
				# set Length header only for Pads
				if dbCNL[vKey] != "":
		
					# go to next spreadsheet row
					gSheetRow = gSheetRow + 1
		
					# set object length
					vCell = "A" + str(gSheetRow)
					gSheet.setBackground(vCell, (1,1,1))
		
					vCell = "B" + str(gSheetRow) + ":F" + str(gSheetRow)
					gSheet.set(vCell, toSheet(dbCNH[vKey], "string", iCaller))
					gSheet.mergeCells(vCell)
					gSheet.setAlignment(vCell, "left", "keep")
					gSheet.setStyle(vCell, "bold", "add")
					gSheet.setBackground(vCell, gHeadCW)
			
					vCell = "G" + str(gSheetRow)
					v = dbCNL[vKey].split(";")
					gSheet.set(vCell, toSheet(v[1], v[0], iCaller))
					gSheet.setAlignment(vCell, "right", "keep")
					gSheet.setStyle(vCell, "bold", "add")
					gSheet.setBackground(vCell, gHeadCW)
			
				# create constraints lists
				keyN = dbCNN[vKey].split(":")
				keyV = dbCNV[vKey].split(":")
		
				# go to next spreadsheet row
				gSheetRow = gSheetRow + 1
		
				# set all constraints
				k = 0
				while k < len(keyN)-1: 
			
					# the first A column is empty for better look
					vCell = "A" + str(gSheetRow)
					gSheet.setBackground(vCell, (1,1,1))
		
					# set constraint name
					vCell = "B" + str(gSheetRow) + ":F" + str(gSheetRow)
					gSheet.set(vCell, toSheet(keyN[k], "string", iCaller))
					gSheet.mergeCells(vCell)
					gSheet.setAlignment(vCell, "left", "keep")
		
					# set dimension
					vCell = "G" + str(gSheetRow)
					v = keyV[k].split(";")
					gSheet.set(vCell, toSheet(v[1], v[0], iCaller))
					gSheet.setAlignment(vCell, "right", "keep")
		
					# go to next spreadsheet row
					gSheetRow = gSheetRow + 1
		
					# go to next constraint
					k = k + 1
		except:
			skip = 1

		# empty line separator
		vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
		gSheet.mergeCells(vCell)

		# next entry or thickness summary
		gSheetRow = gSheetRow + 1

	# ########################################################
	# width part
	# ########################################################

	# cell sizes
	gSheet.setColumnWidth("A", 215)
	gSheet.setColumnWidth("B", 90)
	gSheet.setColumnWidth("C", 20)
	gSheet.setColumnWidth("D", 90)
	gSheet.setColumnWidth("E", 100)
	gSheet.setColumnWidth("F", 80)
	gSheet.setColumnWidth("G", 120)

	# ########################################################
	# thickness part - depends on view columns order, so better here
	# ########################################################

	if sATS == False:
		return

	# add summary title for thickness
	vCell = "A" + str(gSheetRow) + ":D" + str(gSheetRow)
	gSheet.mergeCells(vCell)
	gSheet.set(vCell, gLang7)

	# header
	gSheet.set("E" + str(gSheetRow), gLang4)
	gSheet.set("F" + str(gSheetRow), gLang2)
	gSheet.set("G" + str(gSheetRow), gLang5)

	# alignment
	gSheet.setAlignment("A" + str(gSheetRow), "left", "keep")
	gSheet.setAlignment("E" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("F" + str(gSheetRow), "right", "keep")
	gSheet.setAlignment("G" + str(gSheetRow), "right", "keep")

	# decoration
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.setStyle(vCell, "bold", "add")
	gSheet.setBackground(vCell, gHeadCS)

	# go to next spreadsheet row
	gSheetRow = gSheetRow + 1
	
	for key in dbTQ.keys():

		gSheet.set("E" + str(gSheetRow), toSheet(key, "d", iCaller))
		gSheet.set("F" + str(gSheetRow), toSheet(dbTQ[key], "string", iCaller))
		gSheet.set("G" + str(gSheetRow), toSheet(dbTA[key], "area", iCaller))
		gSheet.setAlignment("E" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("F" + str(gSheetRow), "right", "keep")
		gSheet.setAlignment("G" + str(gSheetRow), "right", "keep")

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1


# ###################################################################################################################
def setViewC(iCaller="setViewC"):

	global gSheet
	global gSheetRow

	# search objects for constraints (custom report)
	for o in dbCNO:

		# set key for db
		vKey = o.Label

		# set object header
		vCell = "A" + str(gSheetRow)
		vStr = str(dbCNQ[vKey]) + " x "
		gSheet.set(vCell, vStr)
		gSheet.setAlignment(vCell, "right", "keep")
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCS)

		vCell = "B" + str(gSheetRow) + ":G" + str(gSheetRow)
		vStr = str(vKey)
		gSheet.set(vCell, vStr)
		gSheet.mergeCells(vCell)
		gSheet.setAlignment(vCell, "left", "keep")
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCS)

		# set Length header only for Pads
		if dbCNL[vKey] != "":

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

			# set object length
			vCell = "A" + str(gSheetRow)
			gSheet.setBackground(vCell, (1,1,1))

			vCell = "B" + str(gSheetRow) + ":F" + str(gSheetRow)
			gSheet.set(vCell, toSheet(dbCNH[vKey], "string", iCaller))
			gSheet.mergeCells(vCell)
			gSheet.setAlignment(vCell, "left", "keep")
			gSheet.setStyle(vCell, "bold", "add")
			gSheet.setBackground(vCell, gHeadCW)
	
			vCell = "G" + str(gSheetRow)
			v = dbCNL[vKey].split(";")
			gSheet.set(vCell, toSheet(v[1], v[0], iCaller))
			gSheet.setAlignment(vCell, "right", "keep")
			gSheet.setStyle(vCell, "bold", "add")
			gSheet.setBackground(vCell, gHeadCW)
	
		# create constraints lists
		keyN = dbCNN[vKey].split(":")
		keyV = dbCNV[vKey].split(":")

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

		# set all constraints
		k = 0
		while k < len(keyN)-1: 
	
			# the first A column is empty for better look
			vCell = "A" + str(gSheetRow)
			gSheet.setBackground(vCell, (1,1,1))

			# set constraint name
			vCell = "B" + str(gSheetRow) + ":F" + str(gSheetRow)
			gSheet.set(vCell, toSheet(keyN[k], "string", iCaller))
			gSheet.mergeCells(vCell)
			gSheet.setAlignment(vCell, "left", "keep")

			# set dimension
			vCell = "G" + str(gSheetRow)
			v = keyV[k].split(";")
			gSheet.set(vCell, toSheet(v[1], v[0], iCaller))
			gSheet.setAlignment(vCell, "right", "keep")

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

			# go to next constraint
			k = k + 1
			
	# set cell width
	gSheet.setColumnWidth("A", 60)
	gSheet.setColumnWidth("B", 155)
	gSheet.setColumnWidth("C", 120)
	gSheet.setColumnWidth("D", 80)
	gSheet.setColumnWidth("E", 100)
	gSheet.setColumnWidth("F", 100)
	gSheet.setColumnWidth("G", 100)

	# remove empty line separator
	gSheetRow = gSheetRow - 1


# ###################################################################################################################
def setViewP(iCaller="setViewP"):

	global gSheet
	global gSheetRow

	# search objects for constraints
	for vKey in dbCNQ.keys():

		# split key and get the group name
		vArr = vKey.split(":")
		vGroup = vArr[0]

		# set object header
		vCell = "A" + str(gSheetRow)
		vStr = str(dbCNQ[vKey]) + " x "
		gSheet.set(vCell, vStr)
		gSheet.setAlignment(vCell, "right", "keep")
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCS)

		vCell = "B" + str(gSheetRow) + ":G" + str(gSheetRow)
		vStr = str(vGroup)
		gSheet.set(vCell, vStr)
		gSheet.mergeCells(vCell)	
		gSheet.setAlignment(vCell, "left", "keep")
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCS)

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

		# set object length
		vCell = "A" + str(gSheetRow)
		gSheet.setBackground(vCell, (1,1,1))

		vCell = "B" + str(gSheetRow) + ":F" + str(gSheetRow)
		gSheet.set(vCell, toSheet(dbCNH[vKey], "string", iCaller))
		gSheet.mergeCells(vCell)
		gSheet.setAlignment(vCell, "left", "keep")
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCW)

		vCell = "G" + str(gSheetRow)
		v = dbCNL[vKey].split(";")
		gSheet.set(vCell, toSheet(v[1], v[0], iCaller))
		gSheet.setAlignment(vCell, "right", "keep")
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCW)

		# create constraints lists
		keyN = dbCNN[vKey].split(":")
		keyV = dbCNV[vKey].split(":")

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

		# set all constraints
		k = 0
		while k < len(keyV): 
	
			# the first A column is empty for better look
			vCell = "A" + str(gSheetRow)
			gSheet.setBackground(vCell, (1,1,1))

			# set constraint name
			vCell = "B" + str(gSheetRow) + ":F" + str(gSheetRow)
			
			# fix for FreeCAD crash on empty string
			if str(keyN[k]) == "-":
				gSheet.set(vCell, "")
			else:
				gSheet.set(vCell, toSheet(keyN[k], "string", iCaller))
				
			gSheet.mergeCells(vCell)
			gSheet.setAlignment(vCell, "left", "keep")

			# set dimension
			vCell = "G" + str(gSheetRow)
			v = keyV[k].split(";")
			gSheet.set(vCell, toSheet(v[1], v[0], iCaller))
			gSheet.setAlignment(vCell, "right", "keep")

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

			# go to next constraint
			k = k + 1
	
	# set cell width
	gSheet.setColumnWidth("A", 60)
	gSheet.setColumnWidth("B", 155)
	gSheet.setColumnWidth("C", 120)
	gSheet.setColumnWidth("D", 80)
	gSheet.setColumnWidth("E", 100)
	gSheet.setColumnWidth("F", 100)
	gSheet.setColumnWidth("G", 100)

	# remove row
	gSheetRow = gSheetRow - 1


# ###################################################################################################################
def setViewEdge(iCaller="setViewEdge"):

	global gSheet
	global gSheetRow

	# merge cells for better look line separation
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.mergeCells(vCell)

	# go to next spreadsheet row
	gSheetRow = gSheetRow + 1

	# add summary for total edge size
	vCell = "A" + str(gSheetRow) + ":F" + str(gSheetRow)
	gSheet.mergeCells(vCell)
	gSheet.set(vCell, gLang8)
	gSheet.setStyle(vCell, "bold", "add")
	gSheet.setAlignment(vCell, "left", "keep")

	vCell = "G" + str(gSheetRow)
	gSheet.set(vCell, toSheet(dbE["total"], "edge", iCaller))
	gSheet.setAlignment(vCell, "right", "keep")

	vCell = "A" + str(gSheetRow) + ":F" + str(gSheetRow)
	gSheet.setBackground(vCell, gHeadCS)

	# skip if edgeband is not set correctly
	if dbE["empty"] >= 0 and dbE["edgeband"] > 0:

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1
	
		# add summary for empty edge size
		vCell = "A" + str(gSheetRow) + ":F" + str(gSheetRow)
		gSheet.mergeCells(vCell)
		gSheet.set(vCell, gLang10)
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setAlignment(vCell, "left", "keep")
	
		vCell = "G" + str(gSheetRow)
		gSheet.set(vCell, toSheet(dbE["empty"], "edge", iCaller))
		gSheet.setAlignment(vCell, "right", "keep")
	
		vCell = "A" + str(gSheetRow) + ":F" + str(gSheetRow)
		gSheet.setBackground(vCell, gHeadCS)
	
		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1
	
		# add summary for edgeband edge size
		vCell = "A" + str(gSheetRow) + ":F" + str(gSheetRow)
		gSheet.mergeCells(vCell)
		gSheet.set(vCell, gLang11)
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setAlignment(vCell, "left", "keep")
	
		vCell = "G" + str(gSheetRow)
		gSheet.set(vCell, toSheet(dbE["edgeband"], "edge", iCaller))
		gSheet.setAlignment(vCell, "right", "keep")
	
		vCell = "A" + str(gSheetRow) + ":F" + str(gSheetRow)
		gSheet.setBackground(vCell, gHeadCS)


# ###################################################################################################################
def setViewAdditional(iCaller="setViewAdditional"):

	global gSheet
	global gSheetRow

	startRow = gSheetRow

	# add empty line separator & merge for better look
	gSheetRow = gSheetRow + 1
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.mergeCells(vCell)

	# go to next row
	gSheetRow = gSheetRow + 1

	# search objects for constraints (custom report)
	for vKey in dbARQ.keys():

		# split key and get the group name
		vArr = vKey.split(":")
		vGroup = vArr[0]

		# set object header
		vCell = "A" + str(gSheetRow)
		vStr = str(dbARQ[vKey]) + " x "
		gSheet.set(vCell, vStr)
		gSheet.setAlignment(vCell, "right", "keep")
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCS)

		vCell = "B" + str(gSheetRow) + ":G" + str(gSheetRow)
		vStr = str(vGroup)
		gSheet.set(vCell, vStr)
		gSheet.mergeCells(vCell)	
		gSheet.setAlignment(vCell, "left", "keep")
		gSheet.setStyle(vCell, "bold", "add")
		gSheet.setBackground(vCell, gHeadCS)

		# create constraints lists
		keyN = dbARN[vKey].split(":")
		keyV = dbARV[vKey].split(":")

		# go to next spreadsheet row
		gSheetRow = gSheetRow + 1

		# set all constraints
		k = 0
		while k < len(keyV): 
	
			# the first A column is empty for better look
			vCell = "A" + str(gSheetRow)
			gSheet.setBackground(vCell, (1,1,1))

			# set constraint name
			vCell = "B" + str(gSheetRow) + ":D" + str(gSheetRow)
			gSheet.set(vCell, toSheet(keyN[k], "string", iCaller))
			gSheet.mergeCells(vCell)
			gSheet.setAlignment(vCell, "left", "keep")

			# set dimension
			vCell = "E" + str(gSheetRow) + ":G" + str(gSheetRow)
			v = keyV[k].split(";")
			gSheet.set(vCell, toSheet(v[1], v[0], iCaller))
			gSheet.mergeCells(vCell)
			gSheet.setAlignment(vCell, "right", "keep")

			# go to next spreadsheet row
			gSheetRow = gSheetRow + 1

			# go to next constraint
			k = k + 1
	
	if startRow + 2 == gSheetRow:
		gSheetRow = gSheetRow - 2
	else:
		gSheetRow = gSheetRow - 1


# ###################################################################################################################
def codeLink(iCaller="codeLink"):

	global gSheet
	global gSheetRow

	# add empty line separator
	gSheetRow = gSheetRow + 2

	# add link 
	vCell = "A" + str(gSheetRow) + ":G" + str(gSheetRow)
	gSheet.mergeCells(vCell)
	gSheet.set(vCell, "Generated by FreeCAD macro: github.com/dprojects/getDimensions")
	gSheet.setAlignment(vCell, "left", "keep")
	gSheet.setBackground(vCell, gHeadCW)


# ###################################################################################################################
def finalViewSettings(iCaller="finalViewSettings"):

	global gSheet
	global gSheetRow

	# colors
	gSheet.setForeground("A1:G" + str(gSheetRow), (0,0,0))
	
	# reset settings for eco mode
	if sRPQ == "eco":
		if sLTF == "a":
			vCell = "A1" + ":K" + str(gSheetRow)
		else:
			vCell = "A1" + ":G" + str(gSheetRow)
		
		gSheet.setBackground(vCell, (1,1,1))


# ###################################################################################################################
# View selector
# ###################################################################################################################


# ###################################################################################################################
def selectView(iCaller="selectView"):

	global gSheet
	global gSheetRow

	# remove spreadsheet if exists
	if gAD.getObject("toCut"):
		gAD.removeObject("toCut")

	# create empty spreadsheet
	gSheet = gAD.addObject("Spreadsheet::Sheet","toCut")

	# main report - quantity
	if sLTF == "q":
		setViewQ(iCaller)
		
		if sAEI == True:
			setViewEdge(iCaller)

	# main report - name
	if sLTF == "n":
		setViewN(iCaller)
		
		if sAEI == True:
			setViewEdge(iCaller)

	# main report - group
	if sLTF == "g":
		setViewG(iCaller)
		
		if sAEI == True:
			setViewEdge(iCaller)

	# main report - edge extended
	if sLTF == "e":
		setViewE(iCaller)
		
		if sAEI == True:
			setViewEdge(iCaller)

	# main report - detailed holes
	if sLTF == "d":
		setViewD(iCaller)
		
		if sAEI == True:
			setViewEdge(iCaller)

	# main report - constraints (custom report)
	if sLTF == "c":
		setViewC(iCaller)

	# main report - pads (all constraints report)
	if sLTF == "p":
		setViewP(iCaller)
		
	# main report - approximation (raw values calculated from vertex)
	if sLTF == "a":
		setViewA(iCaller)
	
	if sLTF != "a":
		
		setViewAdditional(iCaller)
		codeLink(iCaller)

	finalViewSettings(iCaller)


# ###################################################################################################################
# TechDraw part
# ###################################################################################################################


# ###################################################################################################################
def setTechDraw(iCaller="setTechDraw"):

	global gAD
	global gSheet
	global gSheetRow

	# add empty line at the end of spreadsheet to fix merged cells at TechDraw page
	gSheetRow = gSheetRow + 1

	# remove existing toPrint page
	if gAD.getObject("toPrint"):
		gAD.removeObject("toPrint")

	# create TechDraw page for print
	gPrint = gAD.addObject("TechDraw::DrawPage","toPrint")
	gPrintTemplate = gAD.addObject("TechDraw::DrawSVGTemplate","Template")
	
	if sLTF == "a":
		gPrintTemplate.Template = FreeCAD.getResourceDir() + "Mod/TechDraw/Templates/A4_Landscape_blank.svg"

		templateWidth = float(gPrintTemplate.Width)
		templateHeight = float(gPrintTemplate.Height)

		if templateWidth == 0 or templateHeight == 0:
			templateWidth = float(297)
			templateHeight = float(210)
	else:
		gPrintTemplate.Template = FreeCAD.getResourceDir() + "Mod/TechDraw/Templates/A4_Portrait_blank.svg"

		templateWidth = float(gPrintTemplate.Width)
		templateHeight = float(gPrintTemplate.Height)

		if templateWidth == 0 or templateHeight == 0:
			templateWidth = float(210)
			templateHeight = float(297)
	
	gPrint.Template = gPrintTemplate

	# add spreadsheet to TechDraw page
	gPrintSheet = gAD.addObject("TechDraw::DrawViewSpreadsheet","Sheet")
	gPrintSheet.Source = gAD.toCut
	gPrint.addView(gPrintSheet)

	# set in the center of the template
	gPrintSheet.X = int(templateWidth / 2)
	gPrintSheet.Y = int(templateHeight / 2)

	if gKernelVersion >= 1.1:
		gPrintSheet.Scale = 1

	# try to set fonts
	try:
		gPrintSheet.Font = "DejaVu Sans"
	except:
		gPrintSheet.Font = "Arial"

	gPrintSheet.TextSize = 13

	# turn off grid if any
	try:
		gPrint.ViewObject.ShowGrid = False
	except:
		skip = 1

	# set border line width
	gPrintSheet.LineWidth = 0.10

	# fix FreeCAD bug
	if sLTF == "a":
		gPrintSheet.CellEnd = "K" + str(gSheetRow)
	else:
		gPrintSheet.CellEnd = "G" + str(gSheetRow)


# ###################################################################################################################
# INIT - check status
# ###################################################################################################################


# ###################################################################################################################
def checkStatus():
	
	global gAD
	global gOBs
	global sQT
	global gExecute
	
	skip = 0
	
	try:
	
		gAD = FreeCAD.ActiveDocument
		
		# remove existing Fake Cube object if exists (auto clean after error)
		if gAD.getObject("gFakeCube"):
			gAD.removeObject("gFakeCube")
		
		gOBs = gAD.Objects
		gExecute = "yes"

	except:

		sQT = "no"
		gExecute = "no"
		skip = 1
	
	if skip == 1:
	
		info = ""
		info += translate("getDimensions", "Please create active document and objects to generate cut-list.")

		msg = QtGui.QMessageBox()
		msg.setWindowTitle(translate("getDimensions","getDimensions"))
		msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
		msg.setText(info)
		msg.exec_()


# ###################################################################################################################
# MAIN
# ###################################################################################################################

# check if there is active document and init
checkStatus()

# show Qt GUI
if sQT == "yes":
	showQtGUI()

# if Qt GUI ok button
if gExecute == "yes":

	# create Fake Cube but not call recompute
	gFakeCube = gAD.addObject("Part::Box", "gFakeCube")

	# set language
	initLang()

	# main loop for calculations
	scanObjects(gOBs, "main")

	# select and set view
	selectView("main")

	# set TechDraw page
	setTechDraw("main")

	# remove existing fake Cube object before recompute
	if gAD.getObject("gFakeCube"):
		gAD.removeObject("gFakeCube")

	# reload to see changes
	gAD.recompute()


# ###################################################################################################################

