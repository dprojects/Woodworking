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
		toolSW = 270
		toolSH = 690
		
		gObj = ""
		gObjBase = ""
		gThick = 0
		
		gDrillFace = ""
		gFIndex = 0
		gFPlane = ""
		gFType = ""
		gDrillFaceKey = ""
		gDrillSink = ""
		
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
		
		gNoSelection = translate('magicDriller', 'please select face')
		
		# ############################################################################
		# init
		# ############################################################################

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):

			# ############################################################################
			# set screen
			# ############################################################################
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = int( gSW - self.toolSW )
			gPH = int( gSH - self.toolSH )

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, self.toolSW, self.toolSH)
			self.setWindowTitle(translate('magicDriller', 'magicDriller'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - settings
			# ############################################################################
			
			row = 10                             # row
			area = self.toolSW - 20              # gui area
			rside = self.toolSW - 10             # right side of the gui area
			
			btsize = 50                          # button size
			btcol1 = rside - btsize - 105        # button column 1 (left)
			btcol2 = rside - btsize - 45         # button column 2 (counter screen)
			btcol3 = rside - btsize              # button column 3 (right)
			
			tfsize = 100                         # text field size
			tfcol = rside - tfsize               # text field column

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			# screen
			info = ""
			info += "                                             "
			info += "                                             "
			info += "                                             "
			self.s1S = QtGui.QLabel(info, self)
			self.s1S.move(10, row)

			row += 20
			
			# button
			self.s1B1 = QtGui.QPushButton(translate('magicDriller', 'refresh face selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(area)
			self.s1B1.setFixedHeight(40)
			self.s1B1.move(10, row)

			# ############################################################################
			# options - select edge
			# ############################################################################

			row += 50

			# label
			self.s2L = QtGui.QLabel(translate('magicDriller', 'Select edge:'), self)
			self.s2L.move(10, row+3)

			# button
			self.s2B1 = QtGui.QPushButton("<", self)
			self.s2B1.clicked.connect(self.setEdgeP)
			self.s2B1.setFixedWidth(btsize)
			self.s2B1.move(btcol1, row)
			self.s2B1.setAutoRepeat(True)
			
			# label
			self.s2IS = QtGui.QLabel("                  ", self)
			self.s2IS.move(btcol2, row+3)
			
			# button
			self.s2B2 = QtGui.QPushButton(">", self)
			self.s2B2.clicked.connect(self.setEdgeN)
			self.s2B2.setFixedWidth(btsize)
			self.s2B2.move(btcol3, row)
			self.s2B2.setAutoRepeat(True)

			# ############################################################################
			# options - adjust position
			# ############################################################################

			row += 30
			
			# label
			self.s3L = QtGui.QLabel(translate('magicDriller', 'Adjust edge:'), self)
			self.s3L.move(10, row+3)

			# button
			self.s3B1 = QtGui.QPushButton("<", self)
			self.s3B1.clicked.connect(self.setPosition)
			self.s3B1.setFixedWidth(btsize)
			self.s3B1.move(btcol1, row)
			self.s3B1.setAutoRepeat(True)
			
			# label
			self.s3IS = QtGui.QLabel("                  ", self)
			self.s3IS.move(btcol2, row+3)

			# button
			self.s3B2 = QtGui.QPushButton(">", self)
			self.s3B2.clicked.connect(self.setPosition)
			self.s3B2.setFixedWidth(btsize)
			self.s3B2.move(btcol3, row)
			self.s3B2.setAutoRepeat(True)

			# ############################################################################
			# options - adjust rotation
			# ############################################################################

			row += 30
			
			# label
			self.s4L = QtGui.QLabel(translate('magicDriller', 'Adjust rotation:'), self)
			self.s4L.move(10, row+3)

			# button
			self.s4B1 = QtGui.QPushButton("<", self)
			self.s4B1.clicked.connect(self.setRotationP)
			self.s4B1.setFixedWidth(btsize)
			self.s4B1.move(btcol1, row)
			self.s4B1.setAutoRepeat(True)
			
			# label
			self.s4IS = QtGui.QLabel("                  ", self)
			self.s4IS.move(btcol2, row+3)

			# button
			self.s4B2 = QtGui.QPushButton(">", self)
			self.s4B2.clicked.connect(self.setRotationN)
			self.s4B2.setFixedWidth(btsize)
			self.s4B2.move(btcol3, row)
			self.s4B2.setAutoRepeat(True)

			# ############################################################################
			# options - select sides
			# ############################################################################

			row += 50

			# label
			self.s5L = QtGui.QLabel(translate('magicDriller', 'Select sides:'), self)
			self.s5L.move(10, row+3)

			# button
			self.s5B1 = QtGui.QPushButton("<", self)
			self.s5B1.clicked.connect(self.setSidesP)
			self.s5B1.setFixedWidth(btsize)
			self.s5B1.move(btcol1, row)
			self.s5B1.setAutoRepeat(True)
			
			# label
			self.s5IS = QtGui.QLabel("                  ", self)
			self.s5IS.move(btcol2, row+3)

			# button
			self.s5B2 = QtGui.QPushButton(">", self)
			self.s5B2.clicked.connect(self.setSidesN)
			self.s5B2.setFixedWidth(btsize)
			self.s5B2.move(btcol3, row)
			self.s5B2.setAutoRepeat(True)

			# ############################################################################
			# options - drill bit types
			# ############################################################################
			
			row += 30
			
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
			self.sMainMenu.setFixedWidth(area)
			self.sMainMenu.move(10, row)

			# ############################################################################
			# options - mounting samples
			# ############################################################################

			row += 30

			# submenu list
			
			self.sSubMenuList = getMainMenuIndex[gDefaultMainMenuText][1]
			
			defaultSubIndex = getMainMenuIndex[gDefaultMainMenuText][2]
			self.gDBLabel = getMainMenuIndex[gDefaultMainMenuText][1][defaultSubIndex]
			self.sSubMenu = QtGui.QComboBox(self)
			self.sSubMenu.addItems(self.sSubMenuList)
			self.sSubMenu.setCurrentIndex(defaultSubIndex)
			self.sSubMenu.textActivated[str].connect(self.setCustomDrillbits)
			self.sSubMenu.setFixedWidth(area)
			self.sSubMenu.move(10, row)
			self.gDBType = getMainMenuIndex[gDefaultMainMenuText][0]
			
			# ############################################################################
			# options - drill bits number per side
			# ############################################################################

			row += 30
			
			# label
			self.oDBNumL = QtGui.QLabel(translate('magicDriller', 'Holes per side:'), self)
			self.oDBNumL.move(10, row+3)

			# text input
			self.oDBNumE = QtGui.QLineEdit(self)
			self.oDBNumE.setText(str(self.gDBNum))
			self.oDBNumE.setFixedWidth(tfsize)
			self.oDBNumE.move(tfcol, row)

			# ############################################################################
			# options - hole diameter
			# ############################################################################
			
			row += 30

			# label
			self.oDBDiameterL = QtGui.QLabel(translate('magicDriller', 'Hole diameter:'), self)
			self.oDBDiameterL.move(10, row+3)

			# text input
			self.oDBDiameterE = QtGui.QLineEdit(self)
			self.oDBDiameterE.setText(MagicPanels.unit2gui(self.gDBDiameter))
			self.oDBDiameterE.setFixedWidth(tfsize)
			self.oDBDiameterE.move(tfcol, row)

			# ############################################################################
			# options - hole diameter for countersinks or counterbores
			# ############################################################################
			
			row += 30

			# label
			self.oDBDiameter2L = QtGui.QLabel(translate('magicDriller', 'Countersink diameter:'), self)
			self.oDBDiameter2L.move(10, row+3)

			# text input
			self.oDBDiameter2E = QtGui.QLineEdit(self)
			self.oDBDiameter2E.setText(MagicPanels.unit2gui(self.gDBDiameter2))
			self.oDBDiameter2E.setFixedWidth(tfsize)
			self.oDBDiameter2E.move(tfcol, row)

			self.oDBDiameter2L.hide()
			self.oDBDiameter2E.hide()

			# ############################################################################
			# options - hole depth
			# ############################################################################

			row += 30
			
			# label
			self.oDBSizeL = QtGui.QLabel(translate('magicDriller', 'Hole depth:'), self)
			self.oDBSizeL.move(10, row+3)

			# text input
			self.oDBSizeE = QtGui.QLineEdit(self)
			self.oDBSizeE.setText(MagicPanels.unit2gui(self.gDBSize))
			self.oDBSizeE.setFixedWidth(tfsize)
			self.oDBSizeE.move(tfcol, row)

			# ############################################################################
			# options - offset from corner
			# ############################################################################

			row += 30
			
			# label
			self.oDBOCornerL = QtGui.QLabel(translate('magicDriller', 'Offset from corner:'), self)
			self.oDBOCornerL.move(10, row+3)

			# text input
			self.oDBOCornerE = QtGui.QLineEdit(self)
			self.oDBOCornerE.setText(MagicPanels.unit2gui(self.gDBOCorner))
			self.oDBOCornerE.setFixedWidth(tfsize)
			self.oDBOCornerE.move(tfcol, row)

			# ############################################################################
			# options - offset between dowels
			# ############################################################################

			row += 30
			
			# label
			self.oDONextL = QtGui.QLabel(translate('magicDriller', 'Offset between holes:'), self)
			self.oDONextL.move(10, row+3)

			# text input
			self.oDONextE = QtGui.QLineEdit(self)
			self.oDONextE.setText(MagicPanels.unit2gui(self.gDBONext))
			self.oDONextE.setFixedWidth(tfsize)
			self.oDONextE.move(tfcol, row)

			# ############################################################################
			# options - offset from edge
			# ############################################################################

			row += 30
			
			# label
			self.oDBOEdgeL = QtGui.QLabel(translate('magicDriller', 'Offset from edge:'), self)
			self.oDBOEdgeL.move(10, row+3)

			# text input
			self.oDBOEdgeE = QtGui.QLineEdit(self)
			self.oDBOEdgeE.setText(MagicPanels.unit2gui(self.gDBOEdge))
			self.oDBOEdgeE.setFixedWidth(tfsize)
			self.oDBOEdgeE.move(tfcol, row)

			# ############################################################################
			# options - pocket rotation
			# ############################################################################

			row += 30
			
			# label
			self.oDBPocketRL = QtGui.QLabel(translate('magicDriller', 'Pocket rotation:'), self)
			self.oDBPocketRL.move(10, row+3)

			# text input
			self.oDBPocketRE = QtGui.QLineEdit(self)
			self.oDBPocketRE.setText(str(self.gDBPocketR))
			self.oDBPocketRE.setFixedWidth(tfsize)
			self.oDBPocketRE.move(tfcol, row)

			self.oDBPocketRL.hide()
			self.oDBPocketRE.hide()
			
			# ############################################################################
			# options - pocket sink
			# ############################################################################

			row += 30
			
			# label
			self.oDBPocketSL = QtGui.QLabel(translate('magicDriller', 'Pocket sink:'), self)
			self.oDBPocketSL.move(10, row+3)

			# text input
			self.oDBPocketSE = QtGui.QLineEdit(self)
			self.oDBPocketSE.setText(MagicPanels.unit2gui(self.gDBPocketS))
			self.oDBPocketSE.setFixedWidth(tfsize)
			self.oDBPocketSE.move(tfcol, row)

			self.oDBPocketSL.hide()
			self.oDBPocketSE.hide()

			# ############################################################################
			# options - keep custom settings checkbox
			# ############################################################################

			row += 30

			self.kcscb = QtGui.QCheckBox(translate('magicDriller', ' - keep custom settings'), self)
			self.kcscb.setCheckState(QtCore.Qt.Unchecked)
			self.kcscb.move(10, row+3)

			# ############################################################################
			# options - end settings
			# ############################################################################

			row += 40

			# button
			self.e1B1 = QtGui.QPushButton(translate('magicDriller', 'show custom settings'), self)
			self.e1B1.clicked.connect(self.refreshSettings)
			self.e1B1.setFixedWidth(area)
			self.e1B1.setFixedHeight(40)
			self.e1B1.move(10, row)

			row += 50

			# button
			self.e2B1 = QtGui.QPushButton(translate('magicDriller', 'create'), self)
			self.e2B1.clicked.connect(self.drillHoles)
			self.e2B1.setFixedWidth(area)
			self.e2B1.setFixedHeight(40)
			self.e2B1.move(10, row)

			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()

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
			
			if not self.gObj.isDerivedFrom("Part::Box"):
				[ v1, v2 ] = MagicPanels.getEdgeNormalized(v1, v2)
			
			# ############################################################################
			# dowels at 1st side
			# ############################################################################
			
			if self.gDBSides == 0 or self.gDBSides == 1:
			
				[ X, Y, Z ] = [ v1[0], v1[1], v1[2] ]
				[ x , y, z ] = [ 0, 0, 0 ]
				
				i = 0
				while i < self.gDBNum:
					
					# edge along X
					if not MagicPanels.equal(v1[0], v2[0]):
						
						if self.gFPlane == "XY":
							x = X - self.gDBOCorner
							if i != 0:
								x = x - ( i * self.gDBONext)
							y = Y + self.gDBOEdge
							z = Z - self.gDBSink
							
						if self.gFPlane == "XZ":
							x = X - self.gDBOCorner
							if i != 0:
								x = x - ( i * self.gDBONext)
							y = Y - self.gDBSink
							z = Z + self.gDBOEdge
				
						# this should not exist
						if self.gFPlane == "YZ":
							[ x, y, z ] = [ X, Y, Z ]
						
						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(1, 0, 0)
						
					# edge along Y
					if not MagicPanels.equal(v1[1], v2[1]):
						
						if self.gFPlane == "XY":
							x = X + self.gDBOEdge
							y = Y - self.gDBOCorner
							if i != 0:
								y = y - ( i * self.gDBONext)
							z = Z - self.gDBSink
					
						# this should not exist
						if self.gFPlane == "XZ":
							[ x, y, z ] = [ X, Y, Z ]
					
						if self.gFPlane == "YZ":
							x = X - self.gDBSink
							y = Y - self.gDBOCorner
							if i != 0:
								y = y - ( i * self.gDBONext)
							z = Z + self.gDBOEdge

						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 1, 0)
						
					# edge along Z
					if not MagicPanels.equal(v1[2], v2[2]):
						
						if self.gFPlane == "XY":
							x = X + self.gDBOEdge
							y = Y - self.gDBSink
							z = Z - self.gDBOCorner
							if i != 0:
								z = z - ( i * self.gDBONext)
						
						if self.gFPlane == "XZ":
							x = X - self.gDBOEdge
							y = Y - self.gDBSink
							z = Z - self.gDBOCorner
							if i != 0:
								z = z - ( i * self.gDBONext)
								
						if self.gFPlane == "YZ":
							x = X - self.gDBSink
							y = Y + self.gDBOEdge
							z = Z - self.gDBOCorner
							if i != 0:
								z = z - ( i * self.gDBONext)

						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 0, 1)

					# ############################################################################
					# create dowel
					# ############################################################################
					
					[[ x, y, z ]] = MagicPanels.getVerticesPosition([[ x, y, z ]], self.gObj, "array")
			
					d = self.createDrillBit(x, y, z)
					self.gDrillBits.append(d)
					
					i = i + 1
			
			# ############################################################################
			# dowels at 2nd side
			# ############################################################################

			if self.gDBSides == 0 or self.gDBSides == 2:
			
				[ X, Y, Z ] = [ v2[0], v2[1], v2[2] ]
				[ x , y, z ] = [ 0, 0, 0 ]

				i = 0
				while i < self.gDBNum:
					
					# edge along X
					if not MagicPanels.equal(v1[0], v2[0]):
						
						if self.gFPlane == "XY":
							x = X + self.gDBOCorner
							if i != 0:
								x = x + ( i * self.gDBONext)
							y = Y + self.gDBOEdge
							z = Z - self.gDBSink
					
						if self.gFPlane == "XZ":
							x = X + self.gDBOCorner
							if i != 0:
								x = x + ( i * self.gDBONext)
							y = Y - self.gDBSink
							z = Z + self.gDBOEdge
						
						# this should not exist
						if self.gFPlane == "YZ":
							[ x, y, z ] = [ X, Y, Z ]

						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(1, 0, 0)

					# edge along Y
					if not MagicPanels.equal(v1[1], v2[1]):
						
						if self.gFPlane == "XY":
							x = X + self.gDBOEdge
							y = Y + self.gDBOCorner
							if i != 0:
								y = y + ( i * self.gDBONext)
							z = Z - self.gDBSink
					
						# this should not exist
						if self.gFPlane == "XZ":
							[ x, y, z ] = [ X, Y, Z ]
					
						if self.gFPlane == "YZ":
							x = X - self.gDBSink
							y = Y + self.gDBOCorner
							if i != 0:
								y = y + ( i * self.gDBONext)
							z = Z + self.gDBOEdge
							
						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 1, 0)

					# edge along Z
					if not MagicPanels.equal(v1[2], v2[2]):
						
						if self.gFPlane == "XY":
							x = X + self.gDBOEdge
							y = Y - self.gDBSink
							z = Z + self.gDBOCorner
							if i != 0:
								z = z + ( i * self.gDBONext)
					
						if self.gFPlane == "XZ":
							x = X - self.gDBOEdge
							y = Y - self.gDBSink
							z = Z + self.gDBOCorner
							if i != 0:
								z = z + ( i * self.gDBONext)
					
						if self.gFPlane == "YZ":
							x = X - self.gDBSink
							y = Y + self.gDBOEdge
							z = Z + self.gDBOCorner
							if i != 0:
								z = z + ( i * self.gDBONext)
					
						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 0, 1)
						
					# ############################################################################
					# create dowel
					# ############################################################################
					
					[[ x, y, z ]] = MagicPanels.getVerticesPosition([[ x, y, z ]], self.gObj, "array")
					
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

			self.gObj = ""
			self.gThick = 0
			
			self.gDrillFace = ""
			self.gFIndex = 0
			self.gFPlane = ""
			self.gFType = ""
		
			self.gEdge = ""
			self.gEArr = []
			self.gEIndex = 0
		
			self.gPosition = 0
		
			self.gRAxis = ""
			self.gRAngles = []
			self.gRIndex = 0

		# ############################################################################
		def getSelected(self):

			try:

				# ############################################################################
				# global config
				# ############################################################################
				
				if not self.kcscb.isChecked():
					self.resetGlobals()

				self.gObjBase = MagicPanels.getReference()
				
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				self.gDrillFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gFIndex = MagicPanels.getFaceIndex(self.gObj, self.gDrillFace)
				FreeCADGui.Selection.clearSelection()
				
				n = ""
				n += str(self.gObj.Label)
				n += ", "
				n += "Face"
				n += str(self.gFIndex)
				self.s1S.setText(n)
				
				# ############################################################################
				# get plane and type
				# ############################################################################
				
				self.gFPlane = MagicPanels.getFacePlane(self.gDrillFace)
				
				[ self.gFType, 
					arrAll, 
					arrThick, 
					arrShort, 
					arrLong ] = MagicPanels.getFaceEdges(self.gObj, self.gDrillFace)
				
				# ############################################################################
				# set possible edges
				# ############################################################################
				
				if self.gFType == "edge":
					
					if len(arrShort) == 0:
						self.gEArr = arrLong
					
					if len(arrLong) == 0:
						self.gEArr = arrShort

				if self.gFType == "surface":
					self.gEArr = arrAll
					
				# ############################################################################
				# set possible rotations
				# ############################################################################
				
				if self.gFPlane == "XY":
					self.gRAngles.append(0)
					self.gRAngles.append(180)
					self.gRAxis = FreeCAD.Vector(1, 0, 0)

				if self.gFPlane == "XZ":
					self.gRAngles.append(90)
					self.gRAngles.append(270)
					self.gRAxis = FreeCAD.Vector(1, 0, 0)
					
				if self.gFPlane == "YZ":
					self.gRAngles.append(90)
					self.gRAngles.append(270)
					self.gRAxis = FreeCAD.Vector(0, 1, 0)
				
				# ############################################################################
				# set default
				# ############################################################################
				
				if not self.kcscb.isChecked():
					
					s = MagicPanels.getSizes(self.gObjBase)
					s.sort()
					self.gThick = s[0]
					
					self.gDBOEdge = self.gThick / 2
					self.oDBOEdgeE.setText(MagicPanels.unit2gui(self.gDBOEdge))
				
				# ############################################################################
				# try auto adjust dowel
				# ############################################################################

				# adjust sink
				self.gDrillSink = MagicPanels.getFaceSink(self.gObj, self.gDrillFace)
				self.gRIndex = 0
				
				# adjust rotation
				if self.gDrillSink == "+":
					
					if self.gFPlane == "XY":
						self.gRIndex = 1
						
					if self.gFPlane == "XZ":
						self.gRIndex = 0
						
					if self.gFPlane == "YZ":
						self.gRIndex = 1

				else:
				
					if self.gFPlane == "XY":
						self.gRIndex = 0
						
					if self.gFPlane == "XZ":
						self.gRIndex = 1
						
					if self.gFPlane == "YZ":
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
				
			except:

				self.s1S.setText(self.gNoSelection)
				return -1
			
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
				
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setEdgeN(self):
			
			try:
				if self.gEIndex + 1 > len(self.gEArr) - 1:
					self.gEIndex = 0
				else:
					self.gEIndex = self.gEIndex + 1
					
				self.gEdge = self.gEArr[self.gEIndex]
				
				self.showDrillBits()
				self.s2IS.setText(str(self.gEIndex+1) + " / " + str(len(self.gEArr)))
			
			except:
				self.s1S.setText(self.gNoSelection)
		
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
				self.s1S.setText(self.gNoSelection)

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
				self.s1S.setText(self.gNoSelection)
				
		def setRotationN(self):
			
			try:
				if self.gRIndex + 1 > len(self.gRAngles) - 1:
					self.gRIndex = 0
				else:
					self.gRIndex = self.gRIndex + 1
					
				self.showDrillBits()
				self.s4IS.setText(str(self.gRIndex+1) + " / " + str(len(self.gRAngles)))
				
			except:
				self.s1S.setText(self.gNoSelection)
		
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
				self.s1S.setText(self.gNoSelection)
				
		def setSidesN(self):
			
			try:
				if self.gDBSides + 1 > 2:
					self.gDBSides = 0
				else:
					self.gDBSides = self.gDBSides + 1
					
				self.showDrillBits()
				self.s5IS.setText(str(self.gDBSides+1) + " / 3")
			
			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def setCustomDrillbits(self, selectedText):
			
			selectedIndex = getSubMenuIndex[selectedText]
			
			try:
			
				self.gDBOEdge = self.gThick / 2
				self.gDBLabel = selectedText
				self.gDBSides = 0
				self.gDBSink = 0
				self.gDrillPoint = "Angled"
				
				# ######################################
				# settings for all hole types
				# ######################################
				
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
						self.gDBSize = 40 - self.gThick
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64

					# Screw 4 x 40 mm
					if selectedIndex == 5:
						self.gDBDiameter = 3
						self.gDBDiameter2 = 10
						self.gDBSize = 40 - self.gThick
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64

					# Screw 5 x 50 mm
					if selectedIndex == 6:
						self.gDBDiameter = 4
						self.gDBDiameter2 = 10
						self.gDBSize = 50 - self.gThick
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 64

					# Screw 6 x 60 mm
					if selectedIndex == 7:
						self.gDBDiameter = 5
						self.gDBDiameter2 = 10
						self.gDBSize = 60 - self.gThick
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
					self.gDBDiameter = 30
					self.gDBDiameter2 = 30
					self.gDBSize = 12.5
					self.gDBNum = 1
					self.gDBOCorner = 50
					self.gDBONext = 32
					self.gDBOEdge = - 33.28
					self.gDrillPoint = "Flat"

				# Wall cabinet brackets - camar 2
				if selectedIndex == 19:
					self.gDBDiameter = 30
					self.gDBDiameter2 = 30
					self.gDBSize = 12.5
					self.gDBNum = 1
					self.gDBOCorner = 50
					self.gDBONext = 32
					self.gDBOEdge = - 33.28
					self.gDrillPoint = "Flat"
					
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
		
			except:
				self.s1S.setText(self.gNoSelection)
		
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
				self.s1S.setText(self.gNoSelection)

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

			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def drillHoles(self):
			
			try:
		
				# store face key to find face to drill at new object later
				self.gDrillFaceKey = self.gDrillFace.BoundBox
				
				# set args
				o = []
				if len(self.gDrillBits) != 0:
					for d in self.gDrillBits:
						o.append(d)
				
				# drilling selection
				
				# Holes
				if self.gDBType == 0:
					holes = MagicPanels.makeHoles(self.gObj, self.gDrillFace, o, self.gDrillPoint )

				# Countersinks
				if self.gDBType == 1:
					holes = MagicPanels.makeCountersinks(self.gObj, self.gDrillFace, o )

				# Counterbores
				if self.gDBType == 2:
					holes = MagicPanels.makeCounterbores(self.gObj, self.gDrillFace, o )
				
				# Pocket holes
				if self.gDBType == 3:
					holes = MagicPanels.makePocketHoles(self.gObj, self.gDrillFace, o )

				# get new object from selection
				FreeCADGui.Selection.addSelection(holes[0])
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				
				# search for selected face to drill
				index = MagicPanels.getFaceIndexByKey(self.gObj, self.gDrillFaceKey)
				self.gDrillFace = self.gObj.Shape.Faces[index-1]

				# update status info screen
				face = "Face"+str(MagicPanels.getFaceIndex(self.gObj, self.gDrillFace))
				self.s1S.setText(str(self.gObj.Label)+", "+face)
				
				# remove selection
				FreeCADGui.Selection.clearSelection()
		
			except:
				self.s1S.setText(self.gNoSelection)
		
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
