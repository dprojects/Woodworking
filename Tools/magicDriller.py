import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore
import Draft

import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# global default settings
# ############################################################################

# I don't know if there is better solution, probably not... 
# this is problem from category "to eat cake and have cake"... 
# to have translation and custom sub-menu list order...
#
# for main menu add new items only at the end
getMainMenuIndex = {
	
	translate('magicDriller', 'Holes'): [ 
		
		0, # main menu index, not change
		
		( 
			translate('magicDriller', 'Dowel 6 x 35 mm '), 
			translate('magicDriller', 'Dowel 8 x 35 mm '), 
			translate('magicDriller', 'Dowel 10 x 35 mm '), 
			translate('magicDriller', 'Screw 3 x 20 mm '), 
			translate('magicDriller', 'Screw 4 x 40 mm '), 
			translate('magicDriller', 'Screw 4.5 x 40 mm '), 
			translate('magicDriller', 'Screw 5 x 50 mm '), 
			translate('magicDriller', 'Screw 6 x 60 mm '), 
			translate('magicDriller', 'Shelf Pin 5 x 16 mm '), 
			translate('magicDriller', 'Profile Pin 5 x 30 mm '), 
			translate('magicDriller', 'Profile Pin 8 x 40 mm '),
			translate('magicDriller', 'Minifix 15 x 45 mm - top '), 
			translate('magicDriller', 'Minifix 15 x 45 mm - side '), 
			translate('magicDriller', 'Cabinet handle - single hole '), 
			translate('magicDriller', 'Cabinet handle - double hole '), 
			translate('magicDriller', 'Wall cabinet brackets - camar 1 '), 
			translate('magicDriller', 'Wall cabinet brackets - camar 2 ') # no comma
		), # for submenu above copy from getSubMenuIndex, order here can be changed 
		
		1 # default index for submenu
	], 
	
	translate('magicDriller', 'Countersinks'): [
		
		1, # main menu index, not change
		
		(
			translate('magicDriller', 'Screw 4 x 40 mm '), 
			translate('magicDriller', 'Screw 4.5 x 40 mm '), 
			translate('magicDriller', 'Screw 5 x 50 mm '), 
			translate('magicDriller', 'Screw 6 x 60 mm ') # no comma
		), # for submenu above copy from getSubMenuIndex, order here can be changed
		
		0 # no comma, default index for submenu
	],
	
	translate('magicDriller', 'Counterbores'): [
		
		2, # main menu index, not change
		
		(
			translate('magicDriller', 'Screw 4 x 40 mm '), 
			translate('magicDriller', 'Screw 4.5 x 40 mm '), 
			translate('magicDriller', 'Screw 5 x 50 mm '), 
			translate('magicDriller', 'Screw 6 x 60 mm ') # no comma
		), # for submenu above copy from getSubMenuIndex, order here can be changed
		
		0 # no comma, default index for submenu
	],
	
	translate('magicDriller', 'Pocket holes'): [
	
		3, # main menu index, not change
		
		(
			translate('magicDriller', 'Screw 4 x 25 mm '), 
			translate('magicDriller', 'Screw 4 x 30 mm '), 
			translate('magicDriller', 'Screw 4 x 40 mm '), 
			translate('magicDriller', 'Screw 4 x 60 mm ') # no comma
		), # for submenu above copy from getSubMenuIndex, order here can be changed
		
		1 # no comma, default index for submenu
	
	] # no comma
}

# default for main menu
gDefaultMainMenuText = translate('magicDriller', 'Holes')

# reference index for submenu, add new items only here at the end, 
# don't change order here, only above in submenu
getSubMenuIndex = {
	translate('magicDriller', 'Dowel 6 x 35 mm '): 0, 
	translate('magicDriller', 'Dowel 8 x 35 mm '): 1, 
	translate('magicDriller', 'Dowel 10 x 35 mm '): 2, 
	translate('magicDriller', 'Screw 3 x 20 mm '): 3, 
	translate('magicDriller', 'Screw 4.5 x 40 mm '): 4, 
	translate('magicDriller', 'Screw 4 x 40 mm '): 5, 
	translate('magicDriller', 'Screw 5 x 50 mm '): 6, 
	translate('magicDriller', 'Screw 6 x 60 mm '): 7, 
	translate('magicDriller', 'Shelf Pin 5 x 16 mm '): 8, 
	translate('magicDriller', 'Profile Pin 5 x 30 mm '): 9, 
	translate('magicDriller', 'Profile Pin 8 x 40 mm '): 10,
	translate('magicDriller', 'Screw 4 x 25 mm '): 11,
	translate('magicDriller', 'Screw 4 x 30 mm '): 12, 
	translate('magicDriller', 'Screw 4 x 60 mm '): 13, 
	translate('magicDriller', 'Minifix 15 x 45 mm - top '): 14, 
	translate('magicDriller', 'Minifix 15 x 45 mm - side '): 15, 
	translate('magicDriller', 'Cabinet handle - single hole '): 16, 
	translate('magicDriller', 'Cabinet handle - double hole '): 17, 
	translate('magicDriller', 'Wall cabinet brackets - camar 1 '): 18,
	translate('magicDriller', 'Wall cabinet brackets - camar 2 '): 19 # no comma
}

# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals
		# ############################################################################
		
		# tool screen size
		toolSW = 310
		toolSH = 710
		
		# face for drill bit position
		gFacePosition = ""  # face as object
		gFacePositionO = "" # object to which face belongs
		gFacePositionB = "" # base object of the object to which face belongs (Pad not Hole)
		gFPIndex = 0
		gFDPlane = ""
		gFPType = ""
		gFPThick = 0
		
		# face for drilling
		gFaceDrill = ""     # face as object
		gFaceDrillO = ""    # object to which face belongs
		gFaceDrillB = ""    # base object of the object to which face belongs (Pad not Hole)
		gFDIndex = 0
		gFDKey = ""
		gFDSink = ""
		gFDThick = 0

		gEdge = ""
		gEArr = []
		gEIndex = 0

		gPosition = 0
		gRAxis = ""
		gRAngles = []
		gRIndex = 0

		# Holes, Countersinks, Counterbores
		gDBType = "" 

		# should not be reset if object change
		gDBSides = 0
		gDrillBits = []
		gDBLabel = ""
		gDBDiameter = 8
		gDBDiameter2 = 10
		gDBSize = 35
		gDBNum = 2
		gDBOCorner = 50
		gDBONext = 64
		gDBOEdge = 0
		gDBSink = 0 # used for pocket holes only
		gDrillPoint = "Angled"
		
		# settings for pocket holes
		gDBPocketR = 75
		gDBPocketS = -5
		
		gPocketAxis = ""
		gPocketCenter = ""
		
		gInit = 1
		
		gNoFPSelection = translate('magicDriller', 'select face for drill bit position')
		gNoFDSelection = translate('magicDriller', 'select face for drilling into')
		
		# ############################################################################
		# init
		# ############################################################################

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('magicDriller', 'magicDriller'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			
			self.setMaximumSize(self.toolSW, self.toolSH)
			self.setFixedHeight(self.toolSH)

			# ############################################################################
			# options - settings
			# ############################################################################
			
			area = self.toolSW - 20              # gui area
			rside = self.toolSW - 10             # right side of the gui area
			cutLabel = area                      # to cut long label strings

			btsize = 50                          # button size
			btcol1 = rside - btsize - 105        # button column 1 (left)
			btcol2 = rside - btsize - 45         # button column 2 (counter screen)
			btcol3 = rside - btsize              # button column 3 (right)
			
			tfsize = 100                         # text field size
			tfcol = rside - tfsize               # text field column

			# ############################################################################
			# header - selection
			# ############################################################################
			
			
			# button
			self.sFacePositionB = QtGui.QPushButton(translate('magicDriller', 'set'), self)
			self.sFacePositionB.clicked.connect(self.setFacePosition)
			self.sFacePositionB.setFixedWidth(50)
			
			# screen
			self.sFacePositionL = QtGui.QLabel("", self)
			self.sFacePositionL.setFixedWidth(cutLabel - 60)
			
			# button
			self.sFaceDrillB = QtGui.QPushButton(translate('magicDriller', 'set'), self)
			self.sFaceDrillB.clicked.connect(self.setFaceDrill)
			self.sFaceDrillB.setFixedWidth(50)
			
			# screen
			self.sFaceDrillL = QtGui.QLabel("", self)
			self.sFaceDrillL.setFixedWidth(cutLabel - 60)
			
			# button
			self.sFaceAllB = QtGui.QPushButton(translate('magicDriller', 'refresh all faces selection'), self)
			self.sFaceAllB.clicked.connect(self.getSelected)
			self.sFaceAllB.setFixedHeight(40)

			# ############################################################################
			# header - drill bit types
			# ############################################################################
			
			# not write here, copy text from getMainMenuIndex to avoid typo
			self.sMainMenuList = (
				translate('magicDriller', 'Holes'), 
				translate('magicDriller', 'Countersinks'), 
				translate('magicDriller', 'Counterbores'),
				translate('magicDriller', 'Pocket holes') # no comma
			)
			
			self.sMainMenu = QtGui.QComboBox(self)
			self.sMainMenu.addItems(self.sMainMenuList)
			self.sMainMenu.setCurrentIndex(getMainMenuIndex[gDefaultMainMenuText][0])
			self.sMainMenu.textActivated[str].connect(self.setDrillBitType)

			# ############################################################################
			# header - mounting samples
			# ############################################################################

			defaultSubIndex = getMainMenuIndex[gDefaultMainMenuText][2]
			self.sSubMenuList = getMainMenuIndex[gDefaultMainMenuText][1]
			self.gDBLabel = getMainMenuIndex[gDefaultMainMenuText][1][defaultSubIndex]
			self.gDBType = getMainMenuIndex[gDefaultMainMenuText][0]
			
			self.sSubMenu = QtGui.QComboBox(self)
			self.sSubMenu.addItems(self.sSubMenuList)
			self.sSubMenu.setCurrentIndex(defaultSubIndex)
			self.sSubMenu.textActivated[str].connect(self.setCustomDrillbits)

			# ############################################################################
			# body - adjust
			# ############################################################################

			# select edge
			self.s2L = QtGui.QLabel(translate('magicDriller', 'Select edge:'), self)
			
			self.s2B1 = QtGui.QPushButton("<", self)
			self.s2B1.clicked.connect(self.setEdgeP)
			self.s2B1.setFixedWidth(btsize)
			self.s2B1.setAutoRepeat(True)
			
			self.s2IS = QtGui.QLabel("", self)
			
			self.s2B2 = QtGui.QPushButton(">", self)
			self.s2B2.clicked.connect(self.setEdgeN)
			self.s2B2.setFixedWidth(btsize)
			self.s2B2.setAutoRepeat(True)

			# adjust position
			self.s3L = QtGui.QLabel(translate('magicDriller', 'Adjust edge:'), self)

			self.s3B1 = QtGui.QPushButton("<", self)
			self.s3B1.clicked.connect(self.setPosition)
			self.s3B1.setFixedWidth(btsize)
			self.s3B1.setAutoRepeat(True)
			
			self.s3IS = QtGui.QLabel("", self)

			self.s3B2 = QtGui.QPushButton(">", self)
			self.s3B2.clicked.connect(self.setPosition)
			self.s3B2.setFixedWidth(btsize)
			self.s3B2.setAutoRepeat(True)

			# adjust rotation
			self.s4L = QtGui.QLabel(translate('magicDriller', 'Adjust rotation:'), self)

			self.s4B1 = QtGui.QPushButton("<", self)
			self.s4B1.clicked.connect(self.setRotationP)
			self.s4B1.setFixedWidth(btsize)
			self.s4B1.setAutoRepeat(True)
			
			self.s4IS = QtGui.QLabel("", self)

			self.s4B2 = QtGui.QPushButton(">", self)
			self.s4B2.clicked.connect(self.setRotationN)
			self.s4B2.setFixedWidth(btsize)
			self.s4B2.setAutoRepeat(True)

			# select sides
			self.s5L = QtGui.QLabel(translate('magicDriller', 'Select sides:'), self)

			self.s5B1 = QtGui.QPushButton("<", self)
			self.s5B1.clicked.connect(self.setSidesP)
			self.s5B1.setFixedWidth(btsize)
			self.s5B1.setAutoRepeat(True)
			
			self.s5IS = QtGui.QLabel("", self)

			self.s5B2 = QtGui.QPushButton(">", self)
			self.s5B2.clicked.connect(self.setSidesN)
			self.s5B2.setFixedWidth(btsize)
			self.s5B2.setAutoRepeat(True)

			# ############################################################################
			# body - custom settigns - holes
			# ############################################################################

			# holes per side
			self.oDBNumL = QtGui.QLabel(translate('magicDriller', 'Holes per side:'), self)
			self.oDBNumE = QtGui.QLineEdit(self)
			self.oDBNumE.setText(str(self.gDBNum))
			self.oDBNumE.setFixedWidth(tfsize)

			# hole diameter
			self.oDBDiameterL = QtGui.QLabel(translate('magicDriller', 'Hole diameter:'), self)
			self.oDBDiameterE = QtGui.QLineEdit(self)
			self.oDBDiameterE.setText(MagicPanels.unit2gui(self.gDBDiameter))
			self.oDBDiameterE.setFixedWidth(tfsize)

			# hole diameter for countersinks or counterbores
			self.oDBDiameter2L = QtGui.QLabel(translate('magicDriller', 'Countersink diameter:'), self)
			self.oDBDiameter2E = QtGui.QLineEdit(self)
			self.oDBDiameter2E.setText(MagicPanels.unit2gui(self.gDBDiameter2))
			self.oDBDiameter2E.setFixedWidth(tfsize)

			# hole depth
			self.oDBSizeL = QtGui.QLabel(translate('magicDriller', 'Hole depth:'), self)
			self.oDBSizeE = QtGui.QLineEdit(self)
			self.oDBSizeE.setText(MagicPanels.unit2gui(self.gDBSize))
			self.oDBSizeE.setFixedWidth(tfsize)

			# offset from corner
			self.oDBOCornerL = QtGui.QLabel(translate('magicDriller', 'Offset from corner:'), self)
			self.oDBOCornerE = QtGui.QLineEdit(self)
			self.oDBOCornerE.setText(MagicPanels.unit2gui(self.gDBOCorner))
			self.oDBOCornerE.setFixedWidth(tfsize)

			# offset between dowels
			self.oDONextL = QtGui.QLabel(translate('magicDriller', 'Offset between holes:'), self)
			self.oDONextE = QtGui.QLineEdit(self)
			self.oDONextE.setText(MagicPanels.unit2gui(self.gDBONext))
			self.oDONextE.setFixedWidth(tfsize)

			# offset from edge
			self.oDBOEdgeL = QtGui.QLabel(translate('magicDriller', 'Offset from edge:'), self)
			self.oDBOEdgeE = QtGui.QLineEdit(self)
			self.oDBOEdgeE.setText(MagicPanels.unit2gui(self.gDBOEdge))
			self.oDBOEdgeE.setFixedWidth(tfsize)

			# pocket rotation
			self.oDBPocketRL = QtGui.QLabel(translate('magicDriller', 'Pocket rotation:'), self)
			self.oDBPocketRE = QtGui.QLineEdit(self)
			self.oDBPocketRE.setText(str(self.gDBPocketR))
			self.oDBPocketRE.setFixedWidth(tfsize)
			
			# pocket sink
			self.oDBPocketSL = QtGui.QLabel(translate('magicDriller', 'Pocket sink:'), self)
			self.oDBPocketSE = QtGui.QLineEdit(self)
			self.oDBPocketSE.setText(MagicPanels.unit2gui(self.gDBPocketS))
			self.oDBPocketSE.setFixedWidth(tfsize)

			# ############################################################################
			# foot
			# ############################################################################

			# checkbox
			self.kcscb = QtGui.QCheckBox(translate('magicDriller', ' - keep custom settings'), self)
			self.kcscb.setCheckState(QtCore.Qt.Unchecked)

			# button
			self.e1B1 = QtGui.QPushButton(translate('magicDriller', 'show custom settings'), self)
			self.e1B1.clicked.connect(self.refreshSettings)

			# button
			self.e2B1 = QtGui.QPushButton(translate('magicDriller', 'create'), self)
			self.e2B1.clicked.connect(self.drillHoles)
			self.e2B1.setFixedHeight(40)

			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.rowFP = QtGui.QHBoxLayout()
			self.rowFP.setAlignment(QtGui.Qt.AlignLeft)
			self.rowFP.addWidget(self.sFacePositionB)
			self.rowFP.addWidget(self.sFacePositionL)
			
			self.rowFD = QtGui.QHBoxLayout()
			self.rowFD.setAlignment(QtGui.Qt.AlignLeft)
			self.rowFD.addWidget(self.sFaceDrillB)
			self.rowFD.addWidget(self.sFaceDrillL)
			
			self.rowFA = QtGui.QHBoxLayout()
			self.rowFA.addWidget(self.sFaceAllB)
			
			self.header = QtGui.QVBoxLayout()
			self.header.addLayout(self.rowFP)
			self.header.addLayout(self.rowFD)
			self.header.addLayout(self.rowFA)
			self.header.addWidget(self.sMainMenu)
			self.header.addWidget(self.sSubMenu)
			
			self.rowA = QtGui.QGridLayout()
			self.rowA.addWidget(self.s2L, 0, 0)
			self.rowA.addWidget(self.s2B1, 0, 1)
			self.rowA.addWidget(self.s2IS, 0, 2)
			self.rowA.addWidget(self.s2B2, 0, 3)
			self.rowA.addWidget(self.s3L, 1, 0)
			self.rowA.addWidget(self.s3B1, 1, 1)
			self.rowA.addWidget(self.s3IS, 1, 2)
			self.rowA.addWidget(self.s3B2, 1, 3)
			self.rowA.addWidget(self.s4L, 2, 0)
			self.rowA.addWidget(self.s4B1, 2, 1)
			self.rowA.addWidget(self.s4IS, 2, 2)
			self.rowA.addWidget(self.s4B2, 2, 3)
			self.rowA.addWidget(self.s5L, 3, 0)
			self.rowA.addWidget(self.s5B1, 3, 1)
			self.rowA.addWidget(self.s5IS, 3, 2)
			self.rowA.addWidget(self.s5B2, 3, 3)
			self.groupA = QtGui.QGroupBox(None, self)
			self.groupA.setLayout(self.rowA)
			
			self.rowC = QtGui.QGridLayout()
			self.rowC.addWidget(self.oDBNumL, 0, 0)
			self.rowC.addWidget(self.oDBNumE, 0, 1)
			self.rowC.addWidget(self.oDBDiameterL, 1, 0)
			self.rowC.addWidget(self.oDBDiameterE, 1, 1)
			self.rowC.addWidget(self.oDBDiameter2L, 2, 0)
			self.rowC.addWidget(self.oDBDiameter2E, 2, 1)
			self.rowC.addWidget(self.oDBSizeL, 3, 0)
			self.rowC.addWidget(self.oDBSizeE, 3, 1)
			self.rowC.addWidget(self.oDBOCornerL, 4, 0)
			self.rowC.addWidget(self.oDBOCornerE, 4, 1)
			self.rowC.addWidget(self.oDONextL, 5, 0)
			self.rowC.addWidget(self.oDONextE, 5, 1)
			self.rowC.addWidget(self.oDBOEdgeL, 6, 0)
			self.rowC.addWidget(self.oDBOEdgeE, 6, 1)
			self.rowC.addWidget(self.oDBPocketRL, 7, 0)
			self.rowC.addWidget(self.oDBPocketRE, 7, 1)
			self.rowC.addWidget(self.oDBPocketSL, 8, 0)
			self.rowC.addWidget(self.oDBPocketSE, 8, 1)
			self.rowCB = QtGui.QVBoxLayout()
			self.rowCB.addWidget(self.kcscb)
			self.rowCB.addWidget(self.e1B1)
			self.layC = QtGui.QVBoxLayout()
			self.layC.addLayout(self.rowC)
			self.layC.addLayout(self.rowCB)
			self.groupC = QtGui.QGroupBox(None, self)
			self.groupC.setLayout(self.layC)
			
			self.rowCR = QtGui.QVBoxLayout()
			self.rowCR.addWidget(self.e2B1)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			self.layout.addLayout(self.header)
			self.layout.addStretch()
			self.layout.addWidget(self.groupA)
			self.layout.addStretch()
			self.layout.addWidget(self.groupC)
			self.layout.addStretch()
			self.layout.addLayout(self.rowCR)
			self.setLayout(self.layout)
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()
			
			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)

			# set window position
			sw = self.width()
			sh = self.height()
			pw = int( FreeCADGui.getMainWindow().width() - sw ) - 15
			ph = 50
			self.setGeometry(pw, ph, sw, sh)

			# init
			self.getSelected()

		# ############################################################################
		# actions - internal functions
		# ############################################################################

		# ############################################################################
		def setRotation(self):
			
			reset = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
			for d in self.gDrillBits:
				d.Placement.Rotation = reset
			
			angle = self.gRAngles[self.gRIndex]
			axis = self.gRAxis

			for d in self.gDrillBits:
				
				x = d.Placement.Base.x
				y = d.Placement.Base.y
				z = d.Placement.Base.z
			
				center = FreeCAD.Vector(x, y, z)
			
				Draft.rotate(d, angle, center, axis, False)
			
			# Pocket holes
			if self.gDBType == 3:
				
				for d in self.gDrillBits:
				
					axis = self.gPocketAxis
					center = FreeCAD.Vector(x, y, z)
					Draft.rotate(d, self.gDBPocketR, center, axis, False)
			
			
			FreeCADGui.Selection.clearSelection()
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def createDrillBit(self, iX, iY, iZ):
			
			# Holes
			if self.gDBType == 0:

				d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DrillBitHole")
				d.Label = str(self.gDBLabel)

				d.Radius = self.gDBDiameter / 2
				d.Height = self.gDBSize
				
				colors = [ (1.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0) ]
				MagicPanels.setColor(d, 0, colors, "color")

			# Countersinks
			if self.gDBType == 1:

				d = FreeCAD.ActiveDocument.addObject("Part::Cone","DrillBitCountersink")
				d.Label = str(self.gDBLabel)

				d.Radius1 = self.gDBDiameter / 2
				d.Radius2 = self.gDBDiameter2 / 2
				d.Height = self.gDBSize
				
				colors = [ (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0) ]
				MagicPanels.setColor(d, 0, colors, "color")
			
			# Counterbores
			if self.gDBType == 2:

				d = FreeCAD.ActiveDocument.addObject("Part::Cone","DrillBitCounterbore")
				d.Label = str(self.gDBLabel)

				d.Radius1 = self.gDBDiameter / 2
				d.Radius2 = self.gDBDiameter2 / 2
				d.Height = self.gDBSize
				
				colors = [ (0.0, 0.0, 1.0, 1.0), (0.0, 1.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0) ]
				MagicPanels.setColor(d, 0, colors, "color")
			
			# Pocket holes
			if self.gDBType == 3:

				d = FreeCAD.ActiveDocument.addObject("Part::Cone","DrillBitPocket")
				d.Label = str(self.gDBLabel)

				d.Radius1 = self.gDBDiameter / 2
				d.Radius2 = self.gDBDiameter2 / 2
				d.Height = self.gDBSize
				
				colors = [ (0.0, 0.0, 1.0, 1.0), (0.0, 1.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0) ]
				MagicPanels.setColor(d, 0, colors, "color")

			d.Placement.Base.x = iX
			d.Placement.Base.y = iY
			d.Placement.Base.z = iZ

			return d

		# ############################################################################
		def showDrillBits(self):
			
			# ############################################################################
			# remove all dowels
			# ############################################################################
			
			if len(self.gDrillBits) != 0:
				for d in self.gDrillBits:
					try:
						FreeCAD.activeDocument().removeObject(str(d.Name))
					except:
						skip = 1
			
			self.gDrillBits = []
			
			# get settings
			[ v1, v2 ] = MagicPanels.getEdgeVertices(self.gEArr[self.gEIndex])
			
			if not self.gFacePositionO.isDerivedFrom("Part::Box"):
				[ v1, v2 ] = MagicPanels.getEdgeNormalized(v1, v2)
			
			# set sink
			cm = self.gFaceDrill.CenterOfMass
			[ sinkX, sinkY, sinkZ ] = [ cm.x, cm.y, cm.z ]
			[[ sinkX, sinkY, sinkZ ]] = MagicPanels.getVerticesPosition([[ sinkX, sinkY, sinkZ ]], self.gFaceDrillO, "array")
			
			# ############################################################################
			# dowels at 1st side
			# ############################################################################
			
			if self.gDBSides == 0 or self.gDBSides == 1:
			
				[ X, Y, Z ] = [ v1[0], v1[1], v1[2] ]
				[[ X, Y, Z ]] = MagicPanels.getVerticesPosition([[ X, Y, Z ]], self.gFacePositionO, "array")
				
				[ x , y, z ] = [ 0, 0, 0 ]
				
				i = 0
				while i < self.gDBNum:
					
					# edge along X
					if not MagicPanels.equal(v1[0], v2[0]):
						
						if self.gFDPlane == "XY":
							x = X - self.gDBOCorner
							if i != 0:
								x = x - ( i * self.gDBONext)
							y = Y + self.gDBOEdge
							z = sinkZ - self.gDBSink
							
						if self.gFDPlane == "XZ":
							x = X - self.gDBOCorner
							if i != 0:
								x = x - ( i * self.gDBONext)
							y = sinkY - self.gDBSink
							z = Z + self.gDBOEdge
				
						# this should not exist
						if self.gFDPlane == "YZ":
							[ x, y, z ] = [ X, Y, Z ]
						
						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(1, 0, 0)
						
					# edge along Y
					if not MagicPanels.equal(v1[1], v2[1]):
						
						if self.gFDPlane == "XY":
							x = X + self.gDBOEdge
							y = Y - self.gDBOCorner
							if i != 0:
								y = y - ( i * self.gDBONext)
							z = sinkZ - self.gDBSink
					
						# this should not exist
						if self.gFDPlane == "XZ":
							[ x, y, z ] = [ X, Y, Z ]
					
						if self.gFDPlane == "YZ":
							x = sinkX - self.gDBSink
							y = Y - self.gDBOCorner
							if i != 0:
								y = y - ( i * self.gDBONext)
							z = Z + self.gDBOEdge

						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 1, 0)
						
					# edge along Z
					if not MagicPanels.equal(v1[2], v2[2]):
						
						if self.gFDPlane == "XY":
							x = X + self.gDBOEdge
							y = sinkY - self.gDBSink
							z = Z - self.gDBOCorner
							if i != 0:
								z = z - ( i * self.gDBONext)
						
						if self.gFDPlane == "XZ":
							x = X - self.gDBOEdge
							y = sinkY - self.gDBSink
							z = Z - self.gDBOCorner
							if i != 0:
								z = z - ( i * self.gDBONext)
								
						if self.gFDPlane == "YZ":
							x = sinkX - self.gDBSink
							y = Y + self.gDBOEdge
							z = Z - self.gDBOCorner
							if i != 0:
								z = z - ( i * self.gDBONext)

						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 0, 1)

					# ############################################################################
					# create dowel
					# ############################################################################
					
					d = self.createDrillBit(x, y, z)
					self.gDrillBits.append(d)
					
					i = i + 1
			
			# ############################################################################
			# dowels at 2nd side
			# ############################################################################

			if self.gDBSides == 0 or self.gDBSides == 2:
			
				[ X, Y, Z ] = [ v2[0], v2[1], v2[2] ]
				[[ X, Y, Z ]] = MagicPanels.getVerticesPosition([[ X, Y, Z ]], self.gFacePositionO, "array")

				[ x , y, z ] = [ 0, 0, 0 ]

				i = 0
				while i < self.gDBNum:
					
					# edge along X
					if not MagicPanels.equal(v1[0], v2[0]):
						
						if self.gFDPlane == "XY":
							x = X + self.gDBOCorner
							if i != 0:
								x = x + ( i * self.gDBONext)
							y = Y + self.gDBOEdge
							z = sinkZ - self.gDBSink
					
						if self.gFDPlane == "XZ":
							x = X + self.gDBOCorner
							if i != 0:
								x = x + ( i * self.gDBONext)
							y = sinkY - self.gDBSink
							z = Z + self.gDBOEdge
						
						# this should not exist
						if self.gFDPlane == "YZ":
							[ x, y, z ] = [ X, Y, Z ]

						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(1, 0, 0)

					# edge along Y
					if not MagicPanels.equal(v1[1], v2[1]):
						
						if self.gFDPlane == "XY":
							x = X + self.gDBOEdge
							y = Y + self.gDBOCorner
							if i != 0:
								y = y + ( i * self.gDBONext)
							z = sinkZ - self.gDBSink
					
						# this should not exist
						if self.gFDPlane == "XZ":
							[ x, y, z ] = [ X, Y, Z ]
					
						if self.gFDPlane == "YZ":
							x = sinkX - self.gDBSink
							y = Y + self.gDBOCorner
							if i != 0:
								y = y + ( i * self.gDBONext)
							z = Z + self.gDBOEdge
							
						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 1, 0)

					# edge along Z
					if not MagicPanels.equal(v1[2], v2[2]):
						
						if self.gFDPlane == "XY":
							x = X + self.gDBOEdge
							y = sinkY - self.gDBSink
							z = Z + self.gDBOCorner
							if i != 0:
								z = z + ( i * self.gDBONext)
					
						if self.gFDPlane == "XZ":
							x = X - self.gDBOEdge
							y = sinkY - self.gDBSink
							z = Z + self.gDBOCorner
							if i != 0:
								z = z + ( i * self.gDBONext)
					
						if self.gFDPlane == "YZ":
							x = sinkX - self.gDBSink
							y = Y + self.gDBOEdge
							z = Z + self.gDBOCorner
							if i != 0:
								z = z + ( i * self.gDBONext)
					
						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 0, 1)
						
					# ############################################################################
					# create dowel
					# ############################################################################
					
					d = self.createDrillBit(x, y, z)
					self.gDrillBits.append(d)
					
					i = i + 1
				
			# ############################################################################
			# set rotation at dowels
			# ############################################################################

			self.setRotation()
			
		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def resetGlobals(self):

			self.gFacePosition = ""
			self.gFacePositionO = ""
			self.gFacePositionB = ""
			self.gFPIndex = 0
			self.gFPType = ""
			self.gFPThick = 0
			
			self.gFaceDrill = ""
			self.gFaceDrillO = ""
			self.gFaceDrillB = ""
			self.gFDPlane = ""
			self.gFDThick = 0
			
			self.gEdge = ""
			self.gEArr = []
			self.gEIndex = 0
		
			self.gPosition = 0
		
			self.gRAxis = ""
			self.gRAngles = []
			self.gRIndex = 0

		# ############################################################################
		def setConfig(self):

			# ############################################################################
			# set possible edges - drill bit position
			# ############################################################################
			
			[ self.gFPType, 
				arrAll, 
				arrThick, 
				arrShort, 
				arrLong ] = MagicPanels.getFaceEdges(self.gFacePositionO, self.gFacePosition)
			
			if self.gFPType == "edge":
				
				if len(arrShort) == 0:
					self.gEArr = arrLong
				
				if len(arrLong) == 0:
					self.gEArr = arrShort

			if self.gFPType == "surface":
				self.gEArr = arrAll
			
			self.gEdge = self.gEArr[self.gEIndex]
			
			# ############################################################################
			# set possible rotations - drill bit rotation
			# ############################################################################
			
			self.gFDPlane = MagicPanels.getFacePlane(self.gFaceDrill)
			
			if self.gFDPlane == "XY":
				self.gRAngles.append(0)
				self.gRAngles.append(180)
				self.gRAxis = FreeCAD.Vector(1, 0, 0)

			if self.gFDPlane == "XZ":
				self.gRAngles.append(90)
				self.gRAngles.append(270)
				self.gRAxis = FreeCAD.Vector(1, 0, 0)
				
			if self.gFDPlane == "YZ":
				self.gRAngles.append(90)
				self.gRAngles.append(270)
				self.gRAxis = FreeCAD.Vector(0, 1, 0)
			
			# ############################################################################
			# set default
			# ############################################################################

			# set offset from edge
			if not self.kcscb.isChecked():
				
				s = MagicPanels.getSizes(self.gFacePositionB)
				s.sort()
				self.gFPThick = s[0]
				
				self.gDBOEdge = self.gFPThick / 2
				self.oDBOEdgeE.setText(MagicPanels.unit2gui(self.gDBOEdge))
			
			# ############################################################################
			# try auto adjust dowel
			# ############################################################################

			# adjust sink
			self.gFDSink = MagicPanels.getFaceSink(self.gFaceDrillO, self.gFaceDrill)
			self.gRIndex = 0
			
			# adjust rotation
			if self.gFDSink == "+":
				
				if self.gFDPlane == "XY":
					self.gRIndex = 1
					
				if self.gFDPlane == "XZ":
					self.gRIndex = 0
					
				if self.gFDPlane == "YZ":
					self.gRIndex = 1

			else:
			
				if self.gFDPlane == "XY":
					self.gRIndex = 0
					
				if self.gFDPlane == "XZ":
					self.gRIndex = 1
					
				if self.gFDPlane == "YZ":
					self.gRIndex = 0
			
			self.s2IS.setText(str(self.gEIndex+1) + " / " + str(len(self.gEArr)))
			self.s3IS.setText(str(self.gPosition+1) + " / 2")
			self.s4IS.setText(str(self.gRIndex+1) + " / " + str(len(self.gRAngles)))
			self.s5IS.setText(str(self.gDBSides+1) + " / 3")
			
			if not self.kcscb.isChecked():
				self.sMainMenu.setCurrentIndex(getMainMenuIndex[gDefaultMainMenuText][0])
				self.setDrillBitType(gDefaultMainMenuText)
			else:
				self.showDrillBits()
				
			self.gInit = 0

		# ############################################################################
		def setFacePosition(self):
			
			try:
				[ subs, objects ] = MagicPanels.getSelectedSubs("no")

				if len(subs) == 0:
					raise
				
				self.gFacePosition = subs[0]
				self.gFacePositionO = objects[0]
				self.gFacePositionB = MagicPanels.getReference(self.gFacePositionO)
				self.gFPIndex = MagicPanels.getFaceIndex(self.gFacePositionO, self.gFacePosition)
				
				n = ""
				n += str(self.gFacePositionO.Label)
				n += ", "
				n += "Face"
				n += str(self.gFPIndex)
				self.sFacePositionL.setText(n)
				
				if self.gFacePosition != "" and self.gFaceDrill != "":
					self.setConfig()
				
				FreeCADGui.Selection.clearSelection()

			except:
				self.sFacePositionL.setText(self.gNoFPSelection)

		# ############################################################################
		def setFaceDrill(self):
			
			try:
				[ subs, objects ] = MagicPanels.getSelectedSubs("no")

				if len(subs) == 0:
					raise
				
				self.gFaceDrill = subs[0]
				self.gFaceDrillO = objects[0]
				self.gFaceDrillB = MagicPanels.getReference(self.gFaceDrillO)
				self.gFDIndex = MagicPanels.getFaceIndex(self.gFaceDrillO, self.gFaceDrill)
				
				n = ""
				n += str(self.gFaceDrillO.Label)
				n += ", "
				n += "Face"
				n += str(self.gFDIndex)
				self.sFaceDrillL.setText(n)

				if self.gFacePosition != "" and self.gFaceDrill != "":
					self.setConfig()

				FreeCADGui.Selection.clearSelection()
				
			except:
				self.sFaceDrillL.setText(self.gNoFDSelection)

		# ############################################################################
		def getSelected(self):

			try:
				if not self.kcscb.isChecked():
					self.resetGlobals()

				[ subs, objects ] = MagicPanels.getSelectedSubs("no")

				if len(subs) == 0:
					raise
					
				if len(subs) == 1:
					self.gFacePosition = subs[0]
					self.gFacePositionO = objects[0]
					self.gFacePositionB = MagicPanels.getReference(self.gFacePositionO)
					self.gFPIndex = MagicPanels.getFaceIndex(self.gFacePositionO, self.gFacePosition)
					
					self.gFaceDrill = subs[0]
					self.gFaceDrillO = objects[0]
					self.gFaceDrillB = MagicPanels.getReference(self.gFaceDrillO)
					self.gFDIndex = MagicPanels.getFaceIndex(self.gFaceDrillO, self.gFaceDrill)
				
				if len(subs) > 1:
					
					self.gFacePosition = subs[0]
					self.gFacePositionO = objects[0]
					self.gFacePositionB = MagicPanels.getReference(self.gFacePositionO)
					self.gFPIndex = MagicPanels.getFaceIndex(self.gFacePositionO, self.gFacePosition)
					
					self.gFaceDrill = subs[1]
					self.gFaceDrillO = objects[1]
					self.gFaceDrillB = MagicPanels.getReference(self.gFaceDrillO)
					self.gFDIndex = MagicPanels.getFaceIndex(self.gFaceDrillO, self.gFaceDrill)
			
				n = ""
				n += str(self.gFacePositionO.Label)
				n += ", "
				n += "Face"
				n += str(self.gFPIndex)
				self.sFacePositionL.setText(n)
				
				n = ""
				n += str(self.gFaceDrillO.Label)
				n += ", "
				n += "Face"
				n += str(self.gFDIndex)
				self.sFaceDrillL.setText(n)
				
				# set configuration
				if self.gFacePosition != "" and self.gFaceDrill != "":
					self.setConfig()
					if not self.kcscb.isChecked():
						self.autoAdjustPosition()
				else:
					raise

				FreeCADGui.Selection.clearSelection()
			
			except:
				self.sFacePositionL.setText(self.gNoFPSelection)
				self.sFaceDrillL.setText(self.gNoFDSelection)
	
		# ############################################################################
		def getDrillBitAxis(self):

			plane = MagicPanels.getFacePlane(self.gFacePosition)
			[ v1, v2 ] = MagicPanels.getEdgeVertices(self.gEdge)
			
			# edge along X
			if not MagicPanels.equal(v1[0], v2[0]):
				
				if plane == "XY":
					return "Y"
			
				if plane == "XZ":
					return "Z"
				
			# edge along Y
			if not MagicPanels.equal(v1[1], v2[1]):
				
				if plane == "XY":
					return "X"

				if plane == "YZ":
					return "Z"
					
			# edge along Z
			if not MagicPanels.equal(v1[2], v2[2]):
				
				if plane == "XZ":
					return "X"
			
				if plane == "YZ":
					return "Y"
	
		# ############################################################################
		def autoAdjustPosition(self):
		
			if len(self.gDrillBits) > 0:
				d = self.gDrillBits[0]
			else:
				return
			
			centerEdge = self.gEdge.CenterOfMass
			[ centerEdge ] = MagicPanels.getVerticesPosition([ centerEdge ], self.gFacePositionO, "vector")
			
			centerDrillBit = d.Shape.CenterOfMass
			[ centerDrillBit ] = MagicPanels.getVerticesPosition([ centerDrillBit ], d, "vector")
			
			centerObject = self.gFacePositionO.Shape.CenterOfMass
			[ centerObject ] = MagicPanels.getVerticesPosition([ centerObject ], self.gFacePositionO, "vector")
			
			axis = self.getDrillBitAxis()
			
			if axis == "X":
				if centerEdge.x < centerObject.x:
					if centerDrillBit.x < centerEdge.x:
						self.setPosition()
				else:
					if centerDrillBit.x > centerEdge.x:
						self.setPosition()
			
			if axis == "Y":
				if centerEdge.y < centerObject.y:
					if centerDrillBit.y < centerEdge.y:
						self.setPosition()
				else:
					if centerDrillBit.y > centerEdge.y:
						self.setPosition()
			
			if axis == "Z":
				if centerEdge.z < centerObject.z:
					if centerDrillBit.z < centerEdge.z:
						self.setPosition()
				else:
					if centerDrillBit.z > centerEdge.z:
						self.setPosition()

			# pocket holes only
			if self.gDBType == 3:
				
				# adjust rotation
				if len(self.gDrillBits) > 0:
					d = self.gDrillBits[0]
				else:
					return
				
				centerDrillBitFace2 = d.Shape.Faces[1].CenterOfMass
				[ centerDrillBitFace2 ] = MagicPanels.getVerticesPosition([ centerDrillBitFace2 ], d, "vector")
				
				if axis == "X":
					if centerEdge.x < centerObject.x:
						if centerDrillBitFace2.x < centerEdge.x:
							self.gDBPocketR = - self.gDBPocketR
					else:
						if centerDrillBitFace2.x > centerEdge.x:
							self.gDBPocketR = - self.gDBPocketR
				
				if axis == "Y":
					if centerEdge.y < centerObject.y:
						if centerDrillBitFace2.y < centerEdge.y:
							self.gDBPocketR = - self.gDBPocketR
					else:
						if centerDrillBitFace2.y > centerEdge.y:
							self.gDBPocketR = - self.gDBPocketR
				
				if axis == "Z":
					if centerEdge.z < centerObject.z:
						if centerDrillBitFace2.z < centerEdge.z:
							self.gDBPocketR = - self.gDBPocketR
					else:
						if centerDrillBitFace2.z > centerEdge.z:
							self.gDBPocketR = - self.gDBPocketR

				self.oDBPocketRE.setText(str(self.gDBPocketR))
				self.showDrillBits()

				# adjust sink
				if len(self.gDrillBits) > 0:
					d = self.gDrillBits[0]
				else:
					return
				
				centerDrillBitFace3 = d.Shape.Faces[2].CenterOfMass
				[ centerDrillBitFace3 ] = MagicPanels.getVerticesPosition([ centerDrillBitFace3 ], d, "vector")
				
				inside = self.gFacePositionO.Shape.BoundBox.isInside(centerDrillBitFace3)
				
				if inside == True:
					self.gDBPocketS = - self.gDBPocketS
					self.oDBPocketSE.setText(MagicPanels.unit2gui(self.gDBPocketS))
					self.gDBSink = self.gDBPocketS
					self.showDrillBits()

		# ############################################################################
		def setEdgeP(self):
			
			try:
				if self.gEIndex - 1 < 0:
					self.gEIndex = len(self.gEArr) - 1
				else:
					self.gEIndex = self.gEIndex - 1
					
				self.gEdge = self.gEArr[self.gEIndex]
				
				self.showDrillBits()
				self.s2IS.setText(str(self.gEIndex+1) + " / " + str(len(self.gEArr)))
				if not self.kcscb.isChecked():
					self.autoAdjustPosition()
				
			except:
				self.sFacePositionL.setText(self.gNoFPSelection)
			
		def setEdgeN(self):
			
			try:
				if self.gEIndex + 1 > len(self.gEArr) - 1:
					self.gEIndex = 0
				else:
					self.gEIndex = self.gEIndex + 1
					
				self.gEdge = self.gEArr[self.gEIndex]
				
				self.showDrillBits()
				self.s2IS.setText(str(self.gEIndex+1) + " / " + str(len(self.gEArr)))
				if not self.kcscb.isChecked():
					self.autoAdjustPosition()
			
			except:
				self.sFacePositionL.setText(self.gNoFPSelection)
		
		# ############################################################################
		def setPosition(self):
			
			try:
				if self.gPosition == 0:
					self.gPosition = 1
				else:
					self.gPosition = 0
				
				self.gDBOEdge = - self.gDBOEdge
				self.oDBOEdgeE.setText(MagicPanels.unit2gui(self.gDBOEdge))
				
				self.showDrillBits()
				self.s3IS.setText(str(self.gPosition+1) + " / 2")
				
			except:
				self.sFacePositionL.setText(self.gNoFPSelection)

		# ############################################################################
		def setRotationP(self):
			
			try:
				if self.gRIndex - 1 < 0:
					self.gRIndex = len(self.gRAngles) - 1
				else:
					self.gRIndex = self.gRIndex - 1
					
				self.showDrillBits()
				self.s4IS.setText(str(self.gRIndex+1) + " / " + str(len(self.gRAngles)))
				
			except:
				self.sFaceDrillL.setText(self.gNoFDSelection)

		def setRotationN(self):
			
			try:
				if self.gRIndex + 1 > len(self.gRAngles) - 1:
					self.gRIndex = 0
				else:
					self.gRIndex = self.gRIndex + 1
					
				self.showDrillBits()
				self.s4IS.setText(str(self.gRIndex+1) + " / " + str(len(self.gRAngles)))
				
			except:
				self.sFaceDrillL.setText(self.gNoFDSelection)

		# ############################################################################
		def setSidesP(self):
			
			try:
				if self.gDBSides - 1 < 0:
					self.gDBSides = 2
				else:
					self.gDBSides = self.gDBSides - 1
					
				self.showDrillBits()
				self.s5IS.setText(str(self.gDBSides+1) + " / 3")
		
			except:
				self.sFacePositionL.setText(self.gNoFPSelection)
		
		def setSidesN(self):
			
			try:
				if self.gDBSides + 1 > 2:
					self.gDBSides = 0
				else:
					self.gDBSides = self.gDBSides + 1
					
				self.showDrillBits()
				self.s5IS.setText(str(self.gDBSides+1) + " / 3")
			
			except:
				self.sFacePositionL.setText(self.gNoFPSelection)

		# ############################################################################
		def setCustomDrillbits(self, selectedText):
			
			selectedIndex = getSubMenuIndex[selectedText]
			
			try:
			
				# ######################################
				# backup if keep settings
				# ######################################
				
				if self.kcscb.isChecked():
					BKgDBSides = self.gDBSides
					BKgDBNum = self.gDBNum
			
				# ######################################
				# settings for all hole types
				# ######################################
				
				self.gDBOEdge = self.gFPThick / 2
				self.gDBLabel = selectedText
				self.gDBSides = 0
				self.gDBSink = 0
				self.gDrillPoint = "Angled"
				
				# Dowel 6 x 35 mm
				if selectedIndex == 0:
					self.gDBDiameter = 6
					self.gDBDiameter2 = 6
					self.gDBSize = 25
					self.gDBNum = 2
					self.gDBOCorner = 50
					self.gDBONext = 32
				
				# Dowel 8 x 35 mm 
				if selectedIndex == 1:
					self.gDBDiameter = 8
					self.gDBDiameter2 = 8
					self.gDBSize = 25
					self.gDBNum = 2
					self.gDBOCorner = 50
					self.gDBONext = 32

				# Dowel 10 x 35 mm
				if selectedIndex == 2:
					self.gDBDiameter = 10
					self.gDBDiameter2 = 10
					self.gDBSize = 25
					self.gDBNum = 2
					self.gDBOCorner = 50
					self.gDBONext = 32
				
				# Screw 3 x 20 mm
				if selectedIndex == 3:
					self.gDBDiameter = 2
					self.gDBDiameter2 = 6
					self.gDBSize = 20
					self.gDBNum = 5
					self.gDBOCorner = 50
					self.gDBONext = 32
					self.gDBOEdge = 9
				
				# ######################################
				# Holes type only
				# ######################################
		
				if self.gDBType == 0:
					
					# Screw 4.5 x 40 mm
					if selectedIndex == 4:
						self.gDBDiameter = 3
						self.gDBDiameter2 = 10
						self.gDBSize = 40 - self.gFPThick
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64

					# Screw 4 x 40 mm
					if selectedIndex == 5:
						self.gDBDiameter = 3
						self.gDBDiameter2 = 10
						self.gDBSize = 40 - self.gFPThick
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64

					# Screw 5 x 50 mm
					if selectedIndex == 6:
						self.gDBDiameter = 4
						self.gDBDiameter2 = 10
						self.gDBSize = 50 - self.gFPThick
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64

					# Screw 6 x 60 mm
					if selectedIndex == 7:
						self.gDBDiameter = 5
						self.gDBDiameter2 = 10
						self.gDBSize = 60 - self.gFPThick
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64

				# ######################################
				# for other types except Holes
				# ######################################
		
				else:
				
					# Screw 4.5 x 40 mm
					if selectedIndex == 4:
						self.gDBDiameter = 3
						self.gDBDiameter2 = 10
						self.gDBSize = 40
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64

					# Screw 4 x 40 mm
					if selectedIndex == 5:
						self.gDBDiameter = 3
						self.gDBDiameter2 = 10
						self.gDBSize = 40
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64

					# Screw 5 x 50 mm
					if selectedIndex == 6:
						self.gDBDiameter = 4
						self.gDBDiameter2 = 10
						self.gDBSize = 50
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64

					# Screw 6 x 60 mm
					if selectedIndex == 7:
						self.gDBDiameter = 5
						self.gDBDiameter2 = 10
						self.gDBSize = 60
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64
				
				# ######################################
				# continue for all hole types
				# ######################################
				
				# Shelf Pin 5 x 16 mm
				if selectedIndex == 8:
					self.gDBDiameter = 5
					self.gDBDiameter2 = 5
					self.gDBSize = 8
					self.gDBNum = 15
					self.gDBOCorner = 50
					self.gDBONext = 32
					self.gDBOEdge = 50
					self.gDBSides = 1

				# Profile Pin 5 x 30 mm
				if selectedIndex == 9:
					self.gDBDiameter = 5
					self.gDBDiameter2 = 6
					self.gDBSize = 100
					self.gDBNum = 2
					self.gDBOCorner = 5
					self.gDBONext = 32

				# Profile Pin 8 x 40 mm
				if selectedIndex == 10:
					self.gDBDiameter = 8
					self.gDBDiameter2 = 9
					self.gDBSize = 100
					self.gDBNum = 1
					self.gDBOCorner = 50
					self.gDBONext = 32

				# ######################################
				# Pocket holes only
				# ######################################
				
				if self.gDBType == 3:
					
					self.gDBDiameter = 3
					self.gDBDiameter2 = 9.5
					self.gDBNum = 2
					self.gDBOCorner = 50
					self.gDBONext = 32
					
					# Screw 4 x 25 mm
					if selectedIndex == 11:
						self.gDBSize = 75
						self.gDBOEdge = 50
						self.gDBPocketR = 75
						self.gDBPocketS = - 5

					# Screw 4 x 30 mm
					if selectedIndex == 12:
						self.gDBSize = 90
						self.gDBOEdge = 60
						self.gDBPocketR = 75
						self.gDBPocketS = - 6
					
					# Screw 4 x 40 mm
					if selectedIndex == 5:
						self.gDBSize = 120
						self.gDBOEdge = 80
						self.gDBPocketR = 75
						self.gDBPocketS = - 9
					
					# Screw 4 x 60 mm
					if selectedIndex == 13:
						self.gDBSize = 180
						self.gDBOEdge = 120
						self.gDBPocketR = 75
						self.gDBPocketS = - 12
					
					self.gDBSink = self.gDBPocketS
				
				# ######################################
				# continue for all hole types
				# ######################################
				
				# Minifix 15 x 45 mm - top
				if selectedIndex == 14:
					self.gDBDiameter = 8
					self.gDBDiameter2 = 8
					self.gDBSize = 34
					self.gDBNum = 1
					self.gDBOCorner = 50
					self.gDBONext = 32
					self.gDBOEdge = - 6
					self.gDrillPoint = "Flat"
					
				# Minifix 15 x 45 mm - side
				if selectedIndex == 15:
					self.gDBDiameter = 30
					self.gDBDiameter2 = 30
					self.gDBSize = 12.5
					self.gDBNum = 1
					self.gDBOCorner = 50
					self.gDBONext = 32
					self.gDBOEdge = - 33.28
					self.gDrillPoint = "Flat"
				
				# Cabinet handle - single hole
				if selectedIndex == 16:
					self.gDBDiameter = 5
					self.gDBDiameter2 = 5
					self.gDBSize = 40
					self.gDBNum = 1
					self.gDBOCorner = 85
					self.gDBONext = 32
					self.gDBOEdge = 65
					self.gDBSides = 2
				
				# Cabinet handle - double hole
				if selectedIndex == 17:
					self.gDBDiameter = 5
					self.gDBDiameter2 = 5
					self.gDBSize = 40
					self.gDBNum = 2
					self.gDBOCorner = 50
					self.gDBONext = 160
					self.gDBOEdge = 50
					self.gDBSides = 2
				
				# Wall cabinet brackets - camar 1
				if selectedIndex == 18:
					self.gDBDiameter = 11 # because it is better to drill little bigger
					self.gDBDiameter2 = 11
					self.gDBSize = 12 # because it is better to drill little bigger
					self.gDBNum = 2
					self.gDBOCorner = 20
					self.gDBONext = 32
					self.gDBOEdge = self.gFPThick + 8
					self.gDBSides = 1
					self.gDrillPoint = "Flat"

				# Wall cabinet brackets - camar 2
				if selectedIndex == 19:
					self.gDBDiameter = 11 # because it is better to drill little bigger
					self.gDBDiameter2 = 11
					self.gDBSize = 12 # because it is better to drill little bigger
					self.gDBNum = 2
					self.gDBOCorner = 20
					self.gDBONext = 32
					self.gDBOEdge = self.gFPThick + 8 + 64
					self.gDBSides = 1
					self.gDrillPoint = "Flat"
				
				# ######################################
				# restore if keep settings
				# ######################################

				if self.kcscb.isChecked():
					self.gDBSides = BKgDBSides
					self.gDBNum = BKgDBNum

				# ######################################
				# update text fields at GUI & show
				# ######################################

				self.oDBDiameterE.setText(MagicPanels.unit2gui(self.gDBDiameter))
				self.oDBDiameter2E.setText(MagicPanels.unit2gui(self.gDBDiameter2))
				self.oDBSizeE.setText(MagicPanels.unit2gui(self.gDBSize))
				self.oDBNumE.setText(str(self.gDBNum))
				self.oDBOCornerE.setText(MagicPanels.unit2gui(self.gDBOCorner))
				self.oDONextE.setText(MagicPanels.unit2gui(self.gDBONext))
				self.oDBOEdgeE.setText(MagicPanels.unit2gui(self.gDBOEdge))
				self.oDBPocketRE.setText(str(self.gDBPocketR))
				self.oDBPocketSE.setText(MagicPanels.unit2gui(self.gDBPocketS))

				self.showDrillBits()
				if not self.kcscb.isChecked():
					self.autoAdjustPosition()
		
			except:
				self.sFacePositionL.setText(self.gNoFPSelection)
				self.sFaceDrillL.setText(self.gNoFDSelection)
		
		# ############################################################################
		def refreshSettings(self):
			
			try:
			
				self.gDBDiameter = MagicPanels.unit2value(self.oDBDiameterE.text())
				self.gDBDiameter2 = MagicPanels.unit2value(self.oDBDiameter2E.text())
				self.gDBSize = MagicPanels.unit2value(self.oDBSizeE.text())
				self.gDBNum = int(self.oDBNumE.text())
				self.gDBOCorner = MagicPanels.unit2value(self.oDBOCornerE.text())
				self.gDBONext = MagicPanels.unit2value(self.oDONextE.text())
				self.gDBOEdge = MagicPanels.unit2value(self.oDBOEdgeE.text())
				self.gDBPocketR = float(self.oDBPocketRE.text())
				self.gDBPocketS = MagicPanels.unit2value(self.oDBPocketSE.text())
				
				if self.gDBType == 3:
					self.gDBSink = self.gDBPocketS

				self.showDrillBits()

			except:
				self.sFacePositionL.setText(self.gNoFPSelection)
				self.sFaceDrillL.setText(self.gNoFDSelection)

		# ############################################################################
		def setDrillBitType(self, selectedText):
			
			selectedIndex = getMainMenuIndex[selectedText][0]
			
			try:
				
				self.gDBType = selectedIndex
				self.sSubMenuList = getMainMenuIndex[selectedText][1]
				self.sSubMenu.clear()
				self.sSubMenu.addItems(self.sSubMenuList)
				
				index = getMainMenuIndex[selectedText][2]
				
				self.sSubMenu.setCurrentIndex(index)
				self.gDBLabel = self.sSubMenuList[index]

				self.gDBSink = 0
				
				# Holes
				if selectedIndex == 0:
					
					self.oDBDiameter2L.hide()
					self.oDBDiameter2E.hide()
					
					self.oDBPocketRL.hide()
					self.oDBPocketRE.hide()
					self.oDBPocketSL.hide()
					self.oDBPocketSE.hide()
				
				# Countersinks
				if selectedIndex == 1:
					
					self.oDBDiameter2L.show()
					self.oDBDiameter2E.show()
					
					self.oDBPocketRL.hide()
					self.oDBPocketRE.hide()
					self.oDBPocketSL.hide()
					self.oDBPocketSE.hide()
				
				# Counterbores
				if selectedIndex == 2:
					
					self.oDBDiameter2L.show()
					self.oDBDiameter2E.show()
					
					self.oDBPocketRL.hide()
					self.oDBPocketRE.hide()
					self.oDBPocketSL.hide()
					self.oDBPocketSE.hide()
				
				# Pocket holes
				if selectedIndex == 3:
					
					self.oDBDiameter2L.show()
					self.oDBDiameter2E.show()
					
					self.oDBPocketRL.show()
					self.oDBPocketRE.show()
					self.oDBPocketSL.show()
					self.oDBPocketSE.show()
					
				# set other settings and refresh drill bits
				self.setCustomDrillbits(self.gDBLabel)
				if not self.kcscb.isChecked():
					self.autoAdjustPosition()

			except:
				self.sFacePositionL.setText(self.gNoFPSelection)
				self.sFaceDrillL.setText(self.gNoFDSelection)

		# ############################################################################
		def drillHoles(self):
			
			try:
		
				# store face key to find face to drill at new object later
				self.gFDKey = self.gFaceDrill.BoundBox
				
				# set args
				o = []
				if len(self.gDrillBits) != 0:
					for d in self.gDrillBits:
						o.append(d)
				
				# drilling selection
				
				# Holes
				if self.gDBType == 0:
					holes = MagicPanels.makeHoles(self.gFaceDrillO, self.gFaceDrill, o, self.gDrillPoint )

				# Countersinks
				if self.gDBType == 1:
					holes = MagicPanels.makeCountersinks(self.gFaceDrillO, self.gFaceDrill, o )

				# Counterbores
				if self.gDBType == 2:
					holes = MagicPanels.makeCounterbores(self.gFaceDrillO, self.gFaceDrill, o )
				
				# Pocket holes
				if self.gDBType == 3:
					holes = MagicPanels.makePocketHoles(self.gFaceDrillO, self.gFaceDrill, o )

				# get new object from selection
				FreeCADGui.Selection.addSelection(holes[0])
				self.gFaceDrillO = FreeCADGui.Selection.getSelection()[0]
				
				# search for selected face to drill
				index = MagicPanels.getFaceIndexByKey(self.gFaceDrillO, self.gFDKey)
				self.gFaceDrill = self.gFaceDrillO.Shape.Faces[index-1]

				# update status info screen
				face = "Face"+str(MagicPanels.getFaceIndex(self.gFaceDrillO, self.gFaceDrill))
				self.sFaceDrillL.setText(str(self.gFaceDrillO.Label)+", "+face)
				
				# remove selection
				FreeCADGui.Selection.clearSelection()
		
			except:
				self.sFaceDrillL.setText(self.gNoFDSelection)
		
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		if len(form.gDrillBits) != 0:
			for d in form.gDrillBits:
				try:
					FreeCAD.activeDocument().removeObject(str(d.Name))
				except:
					skip = 1
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
