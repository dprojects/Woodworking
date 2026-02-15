import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore
import Draft

import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# global default settings
# ############################################################################

gDS = {
	"gDowelLabel": translate('magicDowels', 'Dowel 8 x 35 mm '),
	"gDOFESet": 9,             # dowel offset from edge (adjust edge)
	"gDOFSSet": 20,            # dowel offset from surface (adjust sink)
	"gSides": 0,               # adjust sides
	"gDDiameter": 8,           # dowel diameter
	"gDSize": 35,              # dowel long size
	"gDNum": 2,                # dowel numbers per side
	"gDOCorner": 50,           # dowel offset from corner
	"gDONext": 64,             # space to next dowel (32 mm woodworking system)
	"gDShape": 0,              # dowel shape (cylinder 0 or box 1)
	"gTenonT": 6,              # tenon thickness size
	"gTenonL": 50,             # tenon long size
	"gTenonH": 20 # no comma   # tenon height size (sink)
}

# add new items only at the end and change self.dtslist
getMenuIndex = {
	translate('magicDowels', 'Dowel 6 x 35 mm '): 0, 
	translate('magicDowels', 'Dowel 8 x 35 mm '): 1, 
	translate('magicDowels', 'Dowel 10 x 35 mm '): 2, 
	translate('magicDowels', 'Biscuits 16 x 48 mm '): 3, 
	translate('magicDowels', 'Biscuits 21 x 54 mm '): 4, 
	translate('magicDowels', 'Biscuits 24 x 57 mm '): 5, 
	translate('magicDowels', 'Screw 3 x 20 mm '): 6, 
	translate('magicDowels', 'Screw 4.5 x 40 mm '): 7, 
	translate('magicDowels', 'Screw 4 x 40 mm '): 8, 
	translate('magicDowels', 'Screw 5 x 50 mm '): 9, 
	translate('magicDowels', 'Screw 6 x 60 mm '): 10, 
	translate('magicDowels', 'Confirmation 7 x 40 mm '): 11, 
	translate('magicDowels', 'Confirmation 7 x 50 mm '): 12, 
	translate('magicDowels', 'Confirmation 7 x 70 mm '): 13, 
	translate('magicDowels', 'Shelf Pin 5 x 16 mm '): 14, 
	translate('magicDowels', 'Profile Pin 5 x 30 mm '): 15, 
	translate('magicDowels', 'Profile Pin 8 x 40 mm '): 16, 
	translate('magicDowels', 'Tenon joint '): 17, 
	translate('magicDowels', 'Custom mount point '): 18, 
	translate('magicDowels', 'Minifix 15 x 45 mm '): 19, 
	translate('magicDowels', 'Cabinet handle - single hole '): 20,
	translate('magicDowels', 'Cabinet handle - double hole '): 21, 
	translate('magicDowels', 'magicSettings'): 22 # no comma
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

		# object settings
		gObj = ""
		gObjBase = ""
		gThick = 0
		
		# face settings
		gFace = ""
		gFIndex = 0
		gFPlane = ""
		gFType = ""
		
		# select edge
		gEdgeIndex = 0
		gEdgeArr = []
		gEdge = ""

		# dowel offset from edge (adjust edge)
		gDOFEIndex = 0
		gDOFEArr = []
		gDOFESet = gDS["gDOFESet"]

		# adjust rotation
		gRotationIndex = 0
		gRotationArr = []
		gRotation = ""
		
		# dowel offset from surface (adjust sink)
		gDOFSIndex = 0
		gDOFSArr = []
		gDOFSSet = gDS["gDOFSSet"]
		
		# adjust sides
		gSidesIndex = 0
		gSidesArr = []
		gSides = gDS["gSides"]
		
		# current visible dowels
		gDowels = []
		
		# for tenon
		gDSizeX = 0  # tenon cube size along X axis
		gDSizeY = 0  # tenon cube size along Y axis
		gDSizeZ = 0  # tenon cube size along Z axis
		
		gNoSelection = translate('magicDowels', 'please select face')

		gDowelLabel = gDS["gDowelLabel"]
		gDDiameter = gDS["gDDiameter"]
		gDSize = gDS["gDSize"]
		gDNum = gDS["gDNum"]
		gDOCorner = gDS["gDOCorner"]
		gDONext = gDS["gDONext"]
		gDShape = gDS["gDShape"]
		gTenonL = gDS["gTenonL"]
		gTenonH = gDS["gTenonH"]
		gTenonT = gDS["gTenonT"]
		gCurrentSelection = 2

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
			self.setWindowTitle(translate('magicDowels', 'magicDowels'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			
			self.setMinimumSize(self.toolSW, self.toolSH)
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show GUI
			self.setGUI("init")
			
			# set theme
			MagicPanels.setTheme(self)
			
			# show window
			self.show()
			
			MagicPanels.adjustGUI(self, "right")
			
		# ############################################################################
		# actions - internal functions
		# ############################################################################

		# ############################################################################
		def setGUI(self, schema="init"):
			
			if schema == "init":

				# ############################################################################
				# options - settings
				# ############################################################################
				
				btsize = 50                          # button size
				tfsize = 100                         # text field size
				
				# ############################################################################
				# header - selection
				# ############################################################################
				
				self.faceinfo = QtGui.QLabel("", self)
				
				self.faceinfoB1 = QtGui.QPushButton(translate('magicDowels', 'refresh face selection'), self)
				self.faceinfoB1.clicked.connect(self.setFaceSettins)
				self.faceinfoB1.setFixedHeight(40)
				
				# ############################################################################
				# body - auto adjust
				# ############################################################################
				
				# not write here, copy text from getMenuIndex to avoid typo
				self.dtslist = (
					translate('magicDowels', 'magicSettings'), 
					translate('magicDowels', 'Dowel 6 x 35 mm '), 
					translate('magicDowels', 'Dowel 8 x 35 mm '), 
					translate('magicDowels', 'Dowel 10 x 35 mm '), 
					translate('magicDowels', 'Biscuits 16 x 48 mm '), 
					translate('magicDowels', 'Biscuits 21 x 54 mm '), 
					translate('magicDowels', 'Biscuits 24 x 57 mm '), 
					translate('magicDowels', 'Screw 3 x 20 mm '), 
					translate('magicDowels', 'Screw 4.5 x 40 mm '), 
					translate('magicDowels', 'Screw 4 x 40 mm '), 
					translate('magicDowels', 'Screw 5 x 50 mm '), 
					translate('magicDowels', 'Screw 6 x 60 mm '), 
					translate('magicDowels', 'Confirmation 7 x 40 mm '), 
					translate('magicDowels', 'Confirmation 7 x 50 mm '), 
					translate('magicDowels', 'Confirmation 7 x 70 mm '), 
					translate('magicDowels', 'Minifix 15 x 45 mm '), 
					translate('magicDowels', 'Shelf Pin 5 x 16 mm '), 
					translate('magicDowels', 'Cabinet handle - single hole '), 
					translate('magicDowels', 'Cabinet handle - double hole '), 
					translate('magicDowels', 'Profile Pin 5 x 30 mm '), 
					translate('magicDowels', 'Profile Pin 8 x 40 mm '), 
					translate('magicDowels', 'Tenon joint '), 
					translate('magicDowels', 'Custom mount point ') # no comma 
				)
				
				self.dts = QtGui.QComboBox(self)
				self.dts.addItems(self.dtslist)
				self.dts.textActivated[str].connect(self.setMenuItem)
				if MagicPanels.gPreferCustomSettings == True:
					self.setMenuItem(translate('magicDowels', 'magicSettings'))
				else:
					self.dts.setCurrentIndex(self.gCurrentSelection)
				
				# select edge
				self.seL = QtGui.QLabel(translate('magicDowels', 'Select edge:'), self)
				
				self.seB1 = QtGui.QPushButton("<", self)
				self.seB1.clicked.connect(self.selectEdgeP)
				self.seB1.setFixedWidth(btsize)
				self.seB1.setFixedHeight(20)
				self.seB1.setAutoRepeat(True)
				
				self.seIS = QtGui.QLabel("", self)
				
				self.seB2 = QtGui.QPushButton(">", self)
				self.seB2.clicked.connect(self.selectEdgeN)
				self.seB2.setFixedWidth(btsize)
				self.seB2.setFixedHeight(20)
				self.seB2.setAutoRepeat(True)

				# autodetect checkbox
				self.pacb = QtGui.QCheckBox(translate('magicDowels', ' - position autodetect'), self)
				self.pacb.setCheckState(QtCore.Qt.Checked)
				
				# ############################################################################
				# body - manual adjust
				# ############################################################################
				
				# adjust edge
				self.aeL = QtGui.QLabel(translate('magicDowels', 'Adjust edge:'), self)
			
				self.aeB1 = QtGui.QPushButton("<", self)
				self.aeB1.clicked.connect(self.adjustEdgeP)
				self.aeB1.setFixedWidth(btsize)
				self.aeB1.setFixedHeight(20)
				self.aeB1.setAutoRepeat(True)
				
				self.aeIS = QtGui.QLabel("", self)

				self.aeB2 = QtGui.QPushButton(">", self)
				self.aeB2.clicked.connect(self.adjustEdgeN)
				self.aeB2.setFixedWidth(btsize)
				self.aeB2.setFixedHeight(20)
				self.aeB2.setAutoRepeat(True)

				# adjust sink
				self.asL = QtGui.QLabel(translate('magicDowels', 'Adjust sink:'), self)
				
				self.asB1 = QtGui.QPushButton("<", self)
				self.asB1.clicked.connect(self.adjustSinkP)
				self.asB1.setFixedWidth(btsize)
				self.asB1.setFixedHeight(20)
				self.asB1.setAutoRepeat(True)
				
				self.asIS = QtGui.QLabel("", self)
				
				self.asB2 = QtGui.QPushButton(">", self)
				self.asB2.clicked.connect(self.adjustSinkN)
				self.asB2.setFixedWidth(btsize)
				self.asB2.setFixedHeight(20)
				self.asB2.setAutoRepeat(True)

				# adjust rotation
				self.arL = QtGui.QLabel(translate('magicDowels', 'Adjust rotation:'), self)
				
				self.arB1 = QtGui.QPushButton("<", self)
				self.arB1.clicked.connect(self.setRotationP)
				self.arB1.setFixedWidth(btsize)
				self.arB1.setFixedHeight(20)
				self.arB1.setAutoRepeat(True)
				
				self.arIS = QtGui.QLabel("", self)
				
				self.arB2 = QtGui.QPushButton(">", self)
				self.arB2.clicked.connect(self.setRotationN)
				self.arB2.setFixedWidth(btsize)
				self.arB2.setFixedHeight(20)
				self.arB2.setAutoRepeat(True)

				# select sides
				self.ssL = QtGui.QLabel(translate('magicDowels', 'Select sides:'), self)
				
				self.ssB1 = QtGui.QPushButton("<", self)
				self.ssB1.clicked.connect(self.selectSidesP)
				self.ssB1.setFixedWidth(btsize)
				self.ssB1.setFixedHeight(20)
				self.ssB1.setAutoRepeat(True)
				
				self.ssIS = QtGui.QLabel("", self)

				self.ssB2 = QtGui.QPushButton(">", self)
				self.ssB2.clicked.connect(self.selectSidesN)
				self.ssB2.setFixedWidth(btsize)
				self.ssB2.setFixedHeight(20)
				self.ssB2.setAutoRepeat(True)

				# ############################################################################
				# body - custom settings
				# ############################################################################

				# label
				self.oDowelLabelL = QtGui.QLabel(translate('magicDowels', 'Label:'), self)
				self.oDowelLabelE = QtGui.QLineEdit(self)
				self.oDowelLabelE.setText(str(self.gDowelLabel))
				self.oDowelLabelE.setFixedWidth(tfsize)
				
				# dowels number per side
				self.oDNumL = QtGui.QLabel(translate('magicDowels', 'Dowels per side:'), self)
				self.oDNumLT = QtGui.QLabel(translate('magicDowels', 'Tenons per side:'), self)
				self.oDNumE = QtGui.QLineEdit(self)
				self.oDNumE.setText(str(self.gDNum))
				self.oDNumE.setFixedWidth(tfsize)
				
				# tenon long
				self.oTenonLL = QtGui.QLabel(translate('magicDowels', 'Tenon long:'), self)
				self.oTenonLE = QtGui.QLineEdit(self)
				self.oTenonLE.setText(MagicPanels.unit2gui(self.gTenonL))
				self.oTenonLE.setFixedWidth(tfsize)
				
				# dowels diameter & tenon thick
				self.oDDiameterL = QtGui.QLabel(translate('magicDowels', 'Dowels diameter:'), self)
				self.oDDiameterE = QtGui.QLineEdit(self)
				self.oDDiameterE.setText(MagicPanels.unit2gui(self.gDDiameter))
				self.oDDiameterE.setFixedWidth(tfsize)
				
				# tenon thick
				self.oTenonTL = QtGui.QLabel(translate('magicDowels', 'Tenon thick:'), self)
				self.oTenonTE = QtGui.QLineEdit(self)
				self.oTenonTE.setText(MagicPanels.unit2gui(self.gTenonT))
				self.oTenonTE.setFixedWidth(tfsize)
				
				# dowels size
				self.oDSizeL = QtGui.QLabel(translate('magicDowels', 'Dowels size:'), self)
				self.oDSizeE = QtGui.QLineEdit(self)
				self.oDSizeE.setText(MagicPanels.unit2gui(self.gDSize))
				self.oDSizeE.setFixedWidth(tfsize)
				
				# tenon depth
				self.oTenonHL = QtGui.QLabel(translate('magicDowels', 'Tenon depth:'), self)
				self.oTenonHE = QtGui.QLineEdit(self)
				self.oTenonHE.setText(MagicPanels.unit2gui(self.gTenonH))
				self.oTenonHE.setFixedWidth(tfsize)
				
				# dowels sink
				self.oDSinkL = QtGui.QLabel(translate('magicDowels', 'Dowels sink:'), self)
				self.oDSinkLT = QtGui.QLabel(translate('magicDowels', 'Tenons sink:'), self)
				self.oDSinkE = QtGui.QLineEdit(self)
				self.oDSinkE.setText(MagicPanels.unit2gui(self.gDOFSSet))
				self.oDSinkE.setFixedWidth(tfsize)
				
				# offset from corner
				self.oDOCornerL = QtGui.QLabel(translate('magicDowels', 'Offset from corner:'), self)
				self.oDOCornerE = QtGui.QLineEdit(self)
				self.oDOCornerE.setText(MagicPanels.unit2gui(self.gDOCorner))
				self.oDOCornerE.setFixedWidth(tfsize)
				
				# offset between dowels
				self.oDONextL = QtGui.QLabel(translate('magicDowels', 'Offset between dowels:'), self)
				self.oDONextLT = QtGui.QLabel(translate('magicDowels', 'Offset between tenons:'), self)
				self.oDONextE = QtGui.QLineEdit(self)
				self.oDONextE.setText(MagicPanels.unit2gui(self.gDONext))
				self.oDONextE.setFixedWidth(tfsize)
				
				# offset from edge
				self.oDOEdgeL = QtGui.QLabel(translate('magicDowels', 'Offset from edge:'), self)
				self.oDOEdgeE = QtGui.QLineEdit(self)
				self.oDOEdgeE.setText(MagicPanels.unit2gui(self.gDOFESet))
				self.oDOEdgeE.setFixedWidth(tfsize)
				
				# keep custom settings checkbox
				self.kcscb = QtGui.QCheckBox(translate('magicDowels', ' - keep custom settings'), self)
				self.kcscb.setCheckState(QtCore.Qt.Unchecked)
				
				# custom settings button
				self.e1B1 = QtGui.QPushButton(translate('magicDowels', 'show custom settings'), self)
				self.e1B1.clicked.connect(self.setCustomValues)
				
				# ############################################################################
				# create
				# ############################################################################

				self.e2B1 = QtGui.QPushButton(translate('magicDowels', 'create'), self)
				self.e2B1.clicked.connect(self.setDowels)
				self.e2B1.setFixedHeight(40)
				
				# ############################################################################
				# build GUI layout
				# ############################################################################
				
				# create structure
				self.header = QtGui.QVBoxLayout()
				self.header.addWidget(self.faceinfo)
				self.header.addWidget(self.faceinfoB1)
				
				self.rowAA1 = QtGui.QVBoxLayout()
				self.rowAA1.addWidget(self.dts)
				self.rowAA2 = QtGui.QGridLayout()
				self.rowAA2.addWidget(self.seL, 0, 0)
				self.rowAA2.addWidget(self.seB1, 0, 1)
				self.rowAA2.addWidget(self.seIS, 0, 2)
				self.rowAA2.addWidget(self.seB2, 0, 3)
				self.rowAA3 = QtGui.QVBoxLayout()
				self.rowAA3.addWidget(self.pacb)
				self.layAA = QtGui.QVBoxLayout()
				self.layAA.addLayout(self.rowAA1)
				self.layAA.addLayout(self.rowAA2)
				self.layAA.addLayout(self.rowAA3)
				self.groupAA = QtGui.QGroupBox(None, self)
				self.groupAA.setLayout(self.layAA)
				
				self.rowMA = QtGui.QGridLayout()
				self.rowMA.addWidget(self.aeL, 0, 0)
				self.rowMA.addWidget(self.aeB1, 0, 1)
				self.rowMA.addWidget(self.aeIS, 0, 2)
				self.rowMA.addWidget(self.aeB2, 0, 3)
				self.rowMA.addWidget(self.asL, 1, 0)
				self.rowMA.addWidget(self.asB1, 1, 1)
				self.rowMA.addWidget(self.asIS, 1, 2)
				self.rowMA.addWidget(self.asB2, 1, 3)
				self.rowMA.addWidget(self.arL, 2, 0)
				self.rowMA.addWidget(self.arB1, 2, 1)
				self.rowMA.addWidget(self.arIS, 2, 2)
				self.rowMA.addWidget(self.arB2, 2, 3)
				self.rowMA.addWidget(self.ssL, 3, 0)
				self.rowMA.addWidget(self.ssB1, 3, 1)
				self.rowMA.addWidget(self.ssIS, 3, 2)
				self.rowMA.addWidget(self.ssB2, 3, 3)
				self.groupMA = QtGui.QGroupBox(None, self)
				self.groupMA.setLayout(self.rowMA)
				
				self.rowCS = QtGui.QGridLayout()
				self.rowCS.addWidget(self.oDowelLabelL, 0, 0)
				self.rowCS.addWidget(self.oDowelLabelE, 0, 1)
				self.rowCS.addWidget(self.oDNumL, 1, 0)
				self.rowCS.addWidget(self.oDNumLT, 1, 0)
				self.rowCS.addWidget(self.oDNumE, 1, 1)
				self.rowCS.addWidget(self.oTenonLL, 2, 0)
				self.rowCS.addWidget(self.oTenonLE, 2, 1)
				self.rowCS.addWidget(self.oDDiameterL, 3, 0)
				self.rowCS.addWidget(self.oDDiameterE, 3, 1)
				self.rowCS.addWidget(self.oTenonTL, 4, 0)
				self.rowCS.addWidget(self.oTenonTE, 4, 1)
				self.rowCS.addWidget(self.oDSizeL, 5, 0)
				self.rowCS.addWidget(self.oDSizeE, 5, 1)
				self.rowCS.addWidget(self.oTenonHL, 6, 0)
				self.rowCS.addWidget(self.oTenonHE, 6, 1)
				self.rowCS.addWidget(self.oDSinkL, 7, 0)
				self.rowCS.addWidget(self.oDSinkLT, 7, 0)
				self.rowCS.addWidget(self.oDSinkE, 7, 1)
				self.rowCS.addWidget(self.oDOCornerL, 8, 0)
				self.rowCS.addWidget(self.oDOCornerE, 8, 1)
				self.rowCS.addWidget(self.oDONextL, 9, 0)
				self.rowCS.addWidget(self.oDONextLT, 9, 0)
				self.rowCS.addWidget(self.oDONextE, 9, 1)
				self.rowCS.addWidget(self.oDOEdgeL, 10, 0)
				self.rowCS.addWidget(self.oDOEdgeE, 10, 1)
				self.rowCSB = QtGui.QVBoxLayout()
				self.rowCSB.addWidget(self.kcscb)
				self.rowCSB.addWidget(self.e1B1)
				self.layCS = QtGui.QVBoxLayout()
				self.layCS.addLayout(self.rowCS)
				self.layCS.addLayout(self.rowCSB)
				self.groupCS = QtGui.QGroupBox(None, self)
				self.groupCS.setLayout(self.layCS)
				
				self.rowCR = QtGui.QVBoxLayout()
				self.rowCR.addWidget(self.e2B1)
				
				# set layout to main window
				self.layout = QtGui.QVBoxLayout()
				self.layout.addLayout(self.header)
				self.layout.addWidget(self.groupAA)
				self.layout.addWidget(self.groupMA)
				self.layout.addWidget(self.groupCS)
				self.layout.addStretch()
				self.layout.addLayout(self.rowCR)
				self.setLayout(self.layout)
				
				# ############################################################################
				# set if face is selected before GUI open
				# ############################################################################
				
				self.setFaceSettins()
			
			# ############################################################################
			# GUI for init & dowel
			# ############################################################################
			
			if schema == "init" or schema == "dowel":
				
				self.oTenonLL.hide()
				self.oTenonLE.hide()
				self.oTenonTL.hide()
				self.oTenonTE.hide()
				self.oTenonHL.hide()
				self.oTenonHE.hide()
				self.oDNumLT.hide()
				self.oDSinkLT.hide()
				self.oDONextLT.hide()
				
				self.oDDiameterL.show()
				self.oDDiameterE.show()
				self.oDSizeL.show()
				self.oDSizeE.show()
				self.oDNumL.show()
				self.oDSinkL.show()
				self.oDONextL.show()
			
			# ############################################################################
			# GUI for tenon
			# ############################################################################
			
			if schema == "tenon":
				
				self.oTenonLL.show()
				self.oTenonLE.show()
				self.oTenonTL.show()
				self.oTenonTE.show()
				self.oTenonHL.show()
				self.oTenonHE.show()
				self.oDNumLT.show()
				self.oDSinkLT.show()
				self.oDONextLT.show()
				
				self.oDDiameterL.hide()
				self.oDDiameterE.hide()
				self.oDSizeL.hide()
				self.oDSizeE.hide()
				self.oDNumL.hide()
				self.oDSinkL.hide()
				self.oDONextL.hide()

		# ############################################################################
		def setRotation(self):
			
			reset = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
			for d in self.gDowels:
				d.Placement.Rotation = reset
			
			angle = self.gRotationArr[self.gRotationIndex]
			axis = self.gRotation

			for d in self.gDowels:
				
				x = d.Placement.Base.x
				y = d.Placement.Base.y
				z = d.Placement.Base.z
			
				center = FreeCAD.Vector(x, y, z)
			
				Draft.rotate(d, angle, center, axis, False)
				
			FreeCADGui.Selection.clearSelection()
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def showDowels(self):

			# remove all dowels
			
			if len(self.gDowels) != 0:
				for d in self.gDowels:
					try:
						FreeCAD.activeDocument().removeObject(str(d.Name))
					except:
						skip = 1
			
			self.gDowels = []
			
			# get vertices info
			
			[ v1, v2 ] = MagicPanels.getEdgeVertices(self.gEdgeArr[self.gEdgeIndex])
			
			if not self.gObj.isDerivedFrom("Part::Box"):
				[ v1, v2 ] = MagicPanels.getEdgeNormalized(v1, v2)
			
			# dowels for 1st side
			
			if self.gSides == 0 or self.gSides == 1:
			
				[ X, Y, Z ] = [ v1[0], v1[1], v1[2] ]
				[ x , y, z ] = [ 0, 0, 0 ]
				
				i = 0
				while i < self.gDNum:
					
					# edge along X
					if not MagicPanels.equal(v1[0], v2[0]):
						
						if self.gFPlane == "XY":
							x = X - self.gDOCorner
							if i != 0:
								x = x - ( i * self.gDONext)
							y = Y + self.gDOFESet
							z = Z - self.gDOFSSet
							
							self.gDSizeX = self.gTenonL
							self.gDSizeY = self.gTenonT
							self.gDSizeZ = self.gTenonH
						
						if self.gFPlane == "XZ":
							x = X - self.gDOCorner
							if i != 0:
								x = x - ( i * self.gDONext)
							y = Y - self.gDOFSSet
							z = Z + self.gDOFESet
				
							self.gDSizeX = self.gTenonL
							self.gDSizeY = self.gTenonT
							self.gDSizeZ = self.gTenonH
				
						# this should not exist
						if self.gFPlane == "YZ":
							[ x, y, z ] = [ X, Y, Z ]
							
							self.gDSizeX = self.gTenonT
							self.gDSizeY = self.gTenonL
							self.gDSizeZ = self.gTenonH

					# edge along Y
					if not MagicPanels.equal(v1[1], v2[1]):
						
						if self.gFPlane == "XY":
							x = X + self.gDOFESet
							y = Y - self.gDOCorner
							if i != 0:
								y = y - ( i * self.gDONext)
							z = Z - self.gDOFSSet
					
							self.gDSizeX = self.gTenonT
							self.gDSizeY = self.gTenonL
							self.gDSizeZ = self.gTenonH
					
						# this should not exist
						if self.gFPlane == "XZ":
							[ x, y, z ] = [ X, Y, Z ]
							
							self.gDSizeX = self.gTenonL
							self.gDSizeY = self.gTenonH
							self.gDSizeZ = self.gTenonT
					
						if self.gFPlane == "YZ":
							x = X - self.gDOFSSet
							y = Y - self.gDOCorner
							if i != 0:
								y = y - ( i * self.gDONext)
							z = Z + self.gDOFESet

							self.gDSizeX = self.gTenonT
							self.gDSizeY = self.gTenonL
							self.gDSizeZ = self.gTenonH

					# edge along Z
					if not MagicPanels.equal(v1[2], v2[2]):
						
						if self.gFPlane == "XY":
							x = X + self.gDOFESet
							y = Y - self.gDOFSSet
							z = Z - self.gDOCorner
							if i != 0:
								z = z - ( i * self.gDONext)
						
							self.gDSizeX = self.gTenonH
							self.gDSizeY = self.gTenonL
							self.gDSizeZ = self.gTenonT
						
						if self.gFPlane == "XZ":
							x = X - self.gDOFESet
							y = Y - self.gDOFSSet
							z = Z - self.gDOCorner
							if i != 0:
								z = z - ( i * self.gDONext)
							
							self.gDSizeX = self.gTenonT
							self.gDSizeY = self.gTenonL
							self.gDSizeZ = self.gTenonH
							
						if self.gFPlane == "YZ":
							x = X - self.gDOFSSet
							y = Y + self.gDOFESet
							z = Z - self.gDOCorner
							if i != 0:
								z = z - ( i * self.gDONext)

							self.gDSizeX = self.gTenonL
							self.gDSizeY = self.gTenonT
							self.gDSizeZ = self.gTenonH
					
					# create dowels
					
					[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(self.gObj)
					x = x + coX
					y = y + coY
					z = z + coZ
			
					if self.gDShape == 0:
						d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","Dowel")
					else:
						d = FreeCAD.ActiveDocument.addObject("Part::Box","Tenon")
					
					d.Label = str(self.gDowelLabel)
					d.Placement.Base.x = x
					d.Placement.Base.y = y
					d.Placement.Base.z = z
					
					if self.gDShape == 0:
						d.Radius = self.gDDiameter / 2
						d.Height = self.gDSize
						colors = [ (0.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0) ]
					else:
						d.Width = self.gDSizeY
						d.Height = self.gDSizeZ
						d.Length = self.gDSizeX
						colors = [ (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0),
									(0.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0) ]
						
					MagicPanels.setColor(d, 0, colors, "color") 
					
					self.gDowels.append(d)
					
					i = i + 1
			
			# dowels for 2nd side
			
			if self.gSides == 0 or self.gSides == 2:
			
				[ X, Y, Z ] = [ v2[0], v2[1], v2[2] ]
				[ x , y, z ] = [ 0, 0, 0 ]

				i = 0
				while i < self.gDNum:
					
					# edge along X
					if not MagicPanels.equal(v1[0], v2[0]):

						if self.gFPlane == "XY":
							x = X + self.gDOCorner
							if i != 0:
								x = x + ( i * self.gDONext)
							y = Y + self.gDOFESet
							z = Z - self.gDOFSSet
					
							self.gDSizeX = self.gTenonL
							self.gDSizeY = self.gTenonT
							self.gDSizeZ = self.gTenonH
						
						if self.gFPlane == "XZ":
							x = X + self.gDOCorner
							if i != 0:
								x = x + ( i * self.gDONext)
							y = Y - self.gDOFSSet
							z = Z + self.gDOFESet
						
							self.gDSizeX = self.gTenonL
							self.gDSizeY = self.gTenonT
							self.gDSizeZ = self.gTenonH
				
						# this should not exist
						if self.gFPlane == "YZ":
							[ x, y, z ] = [ X, Y, Z ]
							
							self.gDSizeX = self.gTenonT
							self.gDSizeY = self.gTenonL
							self.gDSizeZ = self.gTenonH

					# edge along Y
					if not MagicPanels.equal(v1[1], v2[1]):

						if self.gFPlane == "XY":
							x = X + self.gDOFESet
							y = Y + self.gDOCorner
							if i != 0:
								y = y + ( i * self.gDONext)
							z = Z - self.gDOFSSet
					
							self.gDSizeX = self.gTenonT
							self.gDSizeY = self.gTenonL
							self.gDSizeZ = self.gTenonH
					
						# this should not exist
						if self.gFPlane == "XZ":
							[ x, y, z ] = [ X, Y, Z ]
							
							self.gDSizeX = self.gTenonL
							self.gDSizeY = self.gTenonH
							self.gDSizeZ = self.gTenonT
					
						if self.gFPlane == "YZ":
							x = X - self.gDOFSSet
							y = Y + self.gDOCorner
							if i != 0:
								y = y + ( i * self.gDONext)
							z = Z + self.gDOFESet

							self.gDSizeX = self.gTenonT
							self.gDSizeY = self.gTenonL
							self.gDSizeZ = self.gTenonH

					# edge along Z
					if not MagicPanels.equal(v1[2], v2[2]):

						if self.gFPlane == "XY":
							x = X + self.gDOFESet
							y = Y - self.gDOFSSet
							z = Z + self.gDOCorner
							if i != 0:
								z = z + ( i * self.gDONext)
					
							self.gDSizeX = self.gTenonH
							self.gDSizeY = self.gTenonL
							self.gDSizeZ = self.gTenonT
					
						if self.gFPlane == "XZ":
							x = X - self.gDOFESet
							y = Y - self.gDOFSSet
							z = Z + self.gDOCorner
							if i != 0:
								z = z + ( i * self.gDONext)
					
							self.gDSizeX = self.gTenonT
							self.gDSizeY = self.gTenonL
							self.gDSizeZ = self.gTenonH
					
						if self.gFPlane == "YZ":
							x = X - self.gDOFSSet
							y = Y + self.gDOFESet
							z = Z + self.gDOCorner
							if i != 0:
								z = z + ( i * self.gDONext)
								
							self.gDSizeX = self.gTenonL
							self.gDSizeY = self.gTenonT
							self.gDSizeZ = self.gTenonH

					# create dowels
					
					[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(self.gObj)
					x = x + coX
					y = y + coY
					z = z + coZ
					
					if self.gDShape == 0:
						d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","Dowel")
					else:
						d = FreeCAD.ActiveDocument.addObject("Part::Box","Tenon")
					
					d.Label = str(self.gDowelLabel)
					d.Placement.Base.x = x
					d.Placement.Base.y = y
					d.Placement.Base.z = z
					
					if self.gDShape == 0:
						d.Radius = self.gDDiameter / 2
						d.Height = self.gDSize
						colors = [ (0.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0) ]
					else:
						d.Width = self.gDSizeY
						d.Height = self.gDSizeZ
						d.Length = self.gDSizeX
						colors = [ (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0),
									(0.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0) ]
						
					MagicPanels.setColor(d, 0, colors, "color")
					
					self.gDowels.append(d)
					
					i = i + 1
				
			# set rotations
			
			self.setRotation()
			MagicPanels.moveToFirst(self.gDowels, self.gObj)

		# ############################################################################
		def setDowelsSettings(self, selectedIndex):
			
			try:
			
				# ########################################################
				#  settings
				# ########################################################
		
				self.gCurrentSelection = selectedIndex
				
				# set GUI view
				
				if self.gCurrentSelection == 17:
					self.setGUI("tenon")
				else:
					self.setGUI("dowel")
			
				# offset from edge

				self.gDOFEArr = []
				self.gDOFESet = self.gThick / 2
				self.gDOFEArr.append(self.gDOFESet)
				self.gDOFEArr.append(-self.gDOFESet)
				self.gDOFEIndex = 0
				self.gDOFESet = self.gDOFEArr[self.gDOFEIndex]
			
				# sink
				
				[ self.gFType, 
						arrAll, 
						arrThick, 
						arrShort, 
						arrLong ] = MagicPanels.getFaceEdges(self.gObj, self.gFace)
					
				if self.gFType == "surface":
					self.gDOFSSet = 15
				
				if self.gFType == "edge":
					self.gDOFSSet = 20
			
				self.gDOFSArr = []
				self.gDOFSArr.append(self.gDOFSSet)
				self.gDOFSArr.append(-self.gDOFSSet)
				self.gDOFSArr.append(0)
				self.gDOFSArr.append(self.gDSize)
				self.gDOFSArr.append(-self.gDSize)
				self.gDOFSArr.append(self.gDSize - self.gDOFSSet)
				self.gDOFSArr.append(-self.gDSize + self.gDOFSSet)
				self.gDOFSIndex = 0
				self.gDOFSSet = self.gDOFSArr[self.gDOFSIndex]

				# sides
				
				self.gSidesArr = []
				self.gSidesArr.append(0)
				self.gSidesArr.append(1)
				self.gSidesArr.append(2)
				self.gSidesIndex = 0
				self.gSides = self.gSidesArr[self.gSidesIndex]
				
				# refresh text fields
				self.oDOEdgeE.setText(MagicPanels.unit2gui(self.gDOFESet))
				self.oDSinkE.setText(MagicPanels.unit2gui(self.gDOFSSet))
				
				# refresh info screens
				self.asIS.setText(str(self.gDOFSIndex+1) + " / " + str(len(self.gDOFSArr)))
				self.aeIS.setText(str(self.gDOFEIndex+1) + " / " + str(len(self.gDOFEArr)))
				self.ssIS.setText(str(self.gSidesIndex+1) + " / " + str(len(self.gSidesArr)))
		
				# overwrite later if needed
				self.gDowelLabel = str(self.dts.currentText())
				self.gDDiameter = gDS["gDDiameter"]
				self.gDSize = gDS["gDSize"]
				self.gDNum = gDS["gDNum"]
				self.gDOCorner = gDS["gDOCorner"]
				self.gDONext = gDS["gDONext"]
				self.gDShape = gDS["gDShape"]
				self.gSides = gDS["gSides"]
				
				# ########################################################
				# custom settings
				# ########################################################
				
				# Dowel 6 x 35 mm
				if self.gCurrentSelection == 0: 
					self.gDDiameter = 6
					self.gDONext = 32
				
				# Dowel 8 x 35 mm
				if self.gCurrentSelection == 1:
					self.gDONext = 32

				# Dowel 10 x 35 mm
				if self.gCurrentSelection == 2:
					self.gDDiameter = 10
					self.gDONext = 32
				
				# Biscuits 16 x 48 mm
				if self.gCurrentSelection == 3:
					self.gDDiameter = 4
					self.gDSize = 16
					self.gDOFSSet = 8
					self.gDNum = 4
					self.gDONext = 64
				
				# Biscuits 21 x 54 mm
				if self.gCurrentSelection == 4:
					self.gDDiameter = 4
					self.gDSize = 21
					self.gDOFSSet = 11
					self.gDNum = 4
					self.gDONext = 64
				
				# Biscuits 24 x 57 mm
				if self.gCurrentSelection == 5:
					self.gDDiameter = 4
					self.gDSize = 24
					self.gDOFSSet = 12
					self.gDNum = 4
					self.gDONext = 64

				# Screw 3 x 20 mm
				if self.gCurrentSelection == 6:
					self.gDDiameter = 3
					self.gDSize = 20
					self.gDOFSSet = 19
					
					# reset offsets from edge
					self.gDOFESet = 9
					self.gDOFEArr = []
					self.gDOFEArr.append(self.gDOFESet)
					self.gDOFEArr.append(-self.gDOFESet)
					self.gDOFEIndex = 0
					self.gDOFESet = self.gDOFEArr[self.gDOFEIndex]
					self.oDOEdgeE.setText(MagicPanels.unit2gui(self.gDOFESet))
					self.aeIS.setText(str(self.gDOFEIndex+1) + " / " + str(len(self.gDOFEArr)))

					self.gDNum = int((float(self.gEdge.Length) / 64) - 1)
				
				# Screw 4.5 x 40 mm
				if self.gCurrentSelection == 7:
					self.gDDiameter = 4.5
					self.gDSize = 40
					self.gDOFSSet = 23
					self.gDNum = 2
					self.gDONext = 64

				# Screw 4 x 40 mm
				if self.gCurrentSelection == 8:
					self.gDDiameter = 4
					self.gDSize = 40
					self.gDOFSSet = 23
					self.gDNum = 2
					self.gDONext = 64

				# Screw 5 x 50 mm
				if self.gCurrentSelection == 9:
					self.gDDiameter = 5
					self.gDSize = 50
					self.gDOFSSet = 33
					self.gDNum = 2
					self.gDONext = 64
				
				# Screw 6 x 60 mm
				if self.gCurrentSelection == 10:
					self.gDDiameter = 6
					self.gDSize = 60
					self.gDOFSSet = 45
					self.gDNum = 2
					self.gDONext = 64
				
				# Confirmation 7 x 40 mm
				if self.gCurrentSelection == 11:
					self.gDDiameter = 7
					self.gDSize = 40
					self.gDOFSSet = 25
					self.gDNum = 1
				
				# Confirmation 7 x 50 mm
				if self.gCurrentSelection == 12:
					self.gDDiameter = 7
					self.gDSize = 50
					self.gDOFSSet = 35
					self.gDNum = 1
				
				# Confirmation 7 x 70 mm
				if self.gCurrentSelection == 13:
					self.gDDiameter = 7
					self.gDSize = 70
					self.gDOFSSet = 55
					self.gDNum = 1
				
				# Shelf Pin 5 x 16 mm
				if self.gCurrentSelection == 14:
					self.gDDiameter = 5
					self.gDSize = 16
					self.gDOFSSet = 8
					self.gSides = 1
					self.gDOCorner = 32
					
					self.gDOFEArr = []
					self.gDOFEArr.append(64)
					self.gDOFEArr.append(-64)
					self.gDOFEIndex = 0
					self.gDOFESet = self.gDOFEArr[self.gDOFEIndex]
					
					self.gDNum = int((float(self.gEdge.Length) / 32) - 1)

				# Profile Pin 5 x 30 mm
				if self.gCurrentSelection == 15:
					self.gDDiameter = 5
					self.gDSize = 30
					self.gDOFSSet = 25
					self.gDOCorner = 5

				# Profile Pin 8 x 40 mm
				if self.gCurrentSelection == 16:
					self.gDDiameter = 8
					self.gDSize = 40
					self.gDOFSSet = 35
					self.gDNum = 1

				# Tenon joint
				if self.gCurrentSelection == 17:
					self.gDShape = 1
					self.gDNum = 1
					self.gDOCorner = 32
					self.gDONext = 100
					self.gSides = 2
					
					self.gTenonT = float(self.gThick) / 2
					self.gTenonL = float(self.gEdge.Length) - (2 * self.gDOCorner)
					self.gTenonH = float(self.gThick)
					self.gDSize = self.gTenonH
					
					self.oTenonLE.setText(MagicPanels.unit2gui(self.gTenonL))
					self.oTenonTE.setText(MagicPanels.unit2gui(self.gTenonT))
					self.oTenonHE.setText(MagicPanels.unit2gui(self.gTenonH))
					
					# adjust edge
					self.gDOFEArr = []
					self.gDOFEArr.append(  (float(self.gThick) / 4) )
					self.gDOFEArr.append( -(float(self.gThick) / 4) )
					self.gDOFEArr.append(  ((float(self.gThick) / 4) + float(self.gTenonT)) )
					self.gDOFEArr.append( -((float(self.gThick) / 4) + float(self.gTenonT)) )
					
					self.gDOFEIndex = 0
					self.gDOFESet = self.gDOFEArr[self.gDOFEIndex]
					
					self.seIS.setText(str(self.gEdgeIndex+1) + " / " + str(len(self.gEdgeArr)))
					
					# sink
					self.gDOFSSet = self.gTenonH / 2
					
				# Custom mount point
				if self.gCurrentSelection == 18:
					skip = 1
				
				# Minifix 15 x 45 mm
				if self.gCurrentSelection == 19:
					self.gDDiameter = 8
					self.gDSize = 45
					self.gDOFSSet = 11
					self.gDNum = 1
					
					# reset offsets from edge
					self.gDOFESet = float(self.gThick) - 6 # because the thickness of minifix is 13, and not in the center
					self.gDOFEArr = []
					self.gDOFEArr.append(self.gDOFESet)
					self.gDOFEArr.append(-self.gDOFESet)
					self.gDOFEIndex = 0
					self.gDOFESet = self.gDOFEArr[self.gDOFEIndex]
					self.oDOEdgeE.setText(MagicPanels.unit2gui(self.gDOFESet))
					self.aeIS.setText(str(self.gDOFEIndex+1) + " / " + str(len(self.gDOFEArr)))

				# Cabinet handle - single hole
				if self.gCurrentSelection == 20:
					self.gDDiameter = 38
					self.gDSize = 25
					self.gDOFSSet = 0
					self.gDNum = 1
					self.gSides = 1
					self.gDOCorner = 65
					
					# reset offsets from edge
					self.gDOFESet = 85
					self.gDOFEArr = []
					self.gDOFEArr.append(self.gDOFESet)
					self.gDOFEArr.append(-self.gDOFESet)
					self.gDOFEIndex = 0
					self.gDOFESet = self.gDOFEArr[self.gDOFEIndex]
					self.oDOEdgeE.setText(MagicPanels.unit2gui(self.gDOFESet))
					self.aeIS.setText(str(self.gDOFEIndex+1) + " / " + str(len(self.gDOFEArr)))

				# Cabinet handle - double hole
				if self.gCurrentSelection == 21:
					self.gDDiameter = 5
					self.gDSize = 36
					self.gDOFSSet = 0
					self.gDNum = 1
					self.gSides = 1
					self.gDOCorner = 50
					
					# reset offsets from edge
					self.gDOFESet = 130 
					self.gDOFEArr = []
					self.gDOFEArr.append(self.gDOFESet)
					self.gDOFEArr.append(-self.gDOFESet)
					self.gDOFEIndex = 0
					self.gDOFESet = self.gDOFEArr[self.gDOFEIndex]
					self.oDOEdgeE.setText(MagicPanels.unit2gui(self.gDOFESet))
					self.aeIS.setText(str(self.gDOFEIndex+1) + " / " + str(len(self.gDOFEArr)))

				if self.gCurrentSelection == 22:
					self.gDowelLabel = translate('magicDowels','Custom dowel ')
					self.gDDiameter = MagicPanels.gDowelDiameter
					self.gDSize = MagicPanels.gDowelSize
					self.gDOFSSet = MagicPanels.gDowelSink
					self.gSides = MagicPanels.gOffsetSides
					self.gDNum = MagicPanels.gOffsetItemsPerSide
					self.gDOCorner = MagicPanels.gOffsetFromCorner
					self.gDONext = MagicPanels.gOffsetBetween
					
					self.gDOFEArr = []
					self.gDOFEArr.append(MagicPanels.gOffsetFromEdge)
					self.gDOFEArr.append(-MagicPanels.gOffsetFromEdge)
					self.gDOFEIndex = 0
					self.gDOFESet = self.gDOFEArr[self.gDOFEIndex]
					
				# ########################################################
				# set custom value 
				# ########################################################

				# set adjust sink
				self.gDOFSArr = []
				self.gDOFSArr.append(self.gDOFSSet)
				self.gDOFSArr.append(-self.gDOFSSet)
				self.gDOFSArr.append(0)
				self.gDOFSArr.append(self.gDSize)
				self.gDOFSArr.append(-self.gDSize)
				self.gDOFSArr.append(self.gDSize - self.gDOFSSet)
				self.gDOFSArr.append(-self.gDSize + self.gDOFSSet)
				self.gDOFSIndex = 0

				# set current sides
				self.gSidesIndex = self.gSides
				self.ssIS.setText(str(self.gSidesIndex+1) + " / " + str(len(self.gSidesArr)))

				# set custom settings to GUI fields
				self.oDowelLabelE.setText(str(self.gDowelLabel))
				self.oDDiameterE.setText(MagicPanels.unit2gui(self.gDDiameter))
				self.oDSizeE.setText(MagicPanels.unit2gui(self.gDSize))
				self.oDSinkE.setText(MagicPanels.unit2gui(self.gDOFSSet))
				self.oDNumE.setText(str(self.gDNum))
				self.oDOCornerE.setText(MagicPanels.unit2gui(self.gDOCorner))
				self.oDONextE.setText(MagicPanels.unit2gui(self.gDONext))
				self.oDOEdgeE.setText(MagicPanels.unit2gui(self.gDOFESet))
				
				# show dowels with default settings after menu change
				self.showDowels()
				
				# try autodetect dowels position
				if self.pacb.isChecked():
					self.autodetectDowelsPosition()
		
			except:
				self.faceinfo.setText(self.gNoSelection)
		
		# ############################################################################
		def setMenuItem(self, selectedText):
			selectedIndex = getMenuIndex[selectedText]
			self.setDowelsSettings(selectedIndex)

		# ############################################################################
		def setCustomValues(self):
			
			try:
			
				# set custom settings to GUI fields
				self.gDowelLabel = str(self.oDowelLabelE.text())
				self.gDDiameter = MagicPanels.unit2value(self.oDDiameterE.text())
				self.gDSize = MagicPanels.unit2value(self.oDSizeE.text())
				self.gDOFSSet = MagicPanels.unit2value(self.oDSinkE.text())
				self.gDNum = int(self.oDNumE.text())
				self.gDOCorner = MagicPanels.unit2value(self.oDOCornerE.text())
				self.gDONext = MagicPanels.unit2value(self.oDONextE.text())
				self.gDOFESet = MagicPanels.unit2value(self.oDOEdgeE.text())
				self.gTenonL = MagicPanels.unit2value(self.oTenonLE.text())
				self.gTenonT = MagicPanels.unit2value(self.oTenonTE.text())
				self.gTenonH = MagicPanels.unit2value(self.oTenonHE.text())
				
				# show dowels with custom settings
				self.showDowels()
			
			except:
				self.faceinfo.setText(self.gNoSelection)

		# ############################################################################
		def setDowels(self):
			
			try:
				if len(self.gDowels) != 0:
					for d in self.gDowels:
						try:
							color = MagicPanels.getColor(self.gObj, self.gFIndex, "color")
							MagicPanels.setColor(d, 0, color, "color")
						except:
							skip = 1

				self.gDowels = []
				FreeCAD.ActiveDocument.recompute()
			
			except:
				self.faceinfo.setText(self.gNoSelection)

		# ############################################################################
		def selectEdgeP(self):
			
			try:
				if self.gEdgeIndex - 1 < 0:
					self.gEdgeIndex = len(self.gEdgeArr) - 1
				else:
					self.gEdgeIndex = self.gEdgeIndex - 1
					
				self.gEdge = self.gEdgeArr[self.gEdgeIndex]
				self.seIS.setText(str(self.gEdgeIndex+1) + " / " + str(len(self.gEdgeArr)))
				
				if not self.kcscb.isChecked():

					if self.gCurrentSelection == 6:
						self.gDNum = int((float(self.gEdge.Length) / 64) - 1)
						self.oDNumE.setText(str(self.gDNum))

					if self.gCurrentSelection == 14:
						self.gDNum = int((float(self.gEdge.Length) / 32) - 1)
						self.oDNumE.setText(str(self.gDNum))
				
					if self.gCurrentSelection == 17:
						self.gTenonL = float(self.gEdge.Length) - (2 * self.gDOCorner)
				
				self.showDowels()
				
				if self.pacb.isChecked():
					self.autodetectDowelsPosition()

			except:
				self.faceinfo.setText(self.gNoSelection)
			
		def selectEdgeN(self):
			
			try:
				if self.gEdgeIndex + 1 > len(self.gEdgeArr) - 1:
					self.gEdgeIndex = 0
				else:
					self.gEdgeIndex = self.gEdgeIndex + 1
					
				self.gEdge = self.gEdgeArr[self.gEdgeIndex]
				self.seIS.setText(str(self.gEdgeIndex+1) + " / " + str(len(self.gEdgeArr)))
				
				if not self.kcscb.isChecked():
					
					if self.gCurrentSelection == 6:
						self.gDNum = int((float(self.gEdge.Length) / 64) - 1)
						self.oDNumE.setText(str(self.gDNum))
						
					if self.gCurrentSelection == 14:
						self.gDNum = int((float(self.gEdge.Length) / 32) - 1)
						self.oDNumE.setText(str(self.gDNum))
						
					if self.gCurrentSelection == 17:
						self.gTenonL = float(self.gEdge.Length) - (2 * self.gDOCorner)

				self.showDowels()
				
				if self.pacb.isChecked():
					self.autodetectDowelsPosition()

			except:
				self.faceinfo.setText(self.gNoSelection)

		# ############################################################################
		def adjustEdgeP(self):
			
			try:
				if self.gDOFEIndex - 1 < 0:
					self.gDOFEIndex = len(self.gDOFEArr) - 1
				else:
					self.gDOFEIndex = self.gDOFEIndex - 1
					
				self.gDOFESet = self.gDOFEArr[self.gDOFEIndex]
				self.aeIS.setText(str(self.gDOFEIndex+1) + " / " + str(len(self.gDOFEArr)))
				self.oDOEdgeE.setText(MagicPanels.unit2gui(self.gDOFESet))
				
				self.showDowels()
			
			except:
				self.faceinfo.setText(self.gNoSelection)

		def adjustEdgeN(self):
		
			try:
				if self.gDOFEIndex + 1 > len(self.gDOFEArr) - 1:
					self.gDOFEIndex = 0
				else:
					self.gDOFEIndex = self.gDOFEIndex + 1
					
				self.gDOFESet = self.gDOFEArr[self.gDOFEIndex]
				self.aeIS.setText(str(self.gDOFEIndex+1) + " / " + str(len(self.gDOFEArr)))
				self.oDOEdgeE.setText(MagicPanels.unit2gui(self.gDOFESet))
				
				self.showDowels()
			
			except:
				self.faceinfo.setText(self.gNoSelection)

		# ############################################################################
		def adjustSinkP(self):
			
			try:
				if self.gDOFSIndex - 1 < 0:
					self.gDOFSIndex = len(self.gDOFSArr) - 1
				else:
					self.gDOFSIndex = self.gDOFSIndex - 1
					
				self.gDOFSSet = self.gDOFSArr[self.gDOFSIndex]
				self.asIS.setText(str(self.gDOFSIndex+1) + " / " + str(len(self.gDOFSArr)))
				self.oDSinkE.setText(MagicPanels.unit2gui(self.gDOFSSet))
				
				self.showDowels()
			
			except:
				self.faceinfo.setText(self.gNoSelection)
			
		def adjustSinkN(self):
			
			try:
				if self.gDOFSIndex + 1 > len(self.gDOFSArr) - 1:
					self.gDOFSIndex = 0
				else:
					self.gDOFSIndex = self.gDOFSIndex + 1
					
				self.gDOFSSet = self.gDOFSArr[self.gDOFSIndex]
				self.asIS.setText(str(self.gDOFSIndex+1) + " / " + str(len(self.gDOFSArr)))
				self.oDSinkE.setText(MagicPanels.unit2gui(self.gDOFSSet))
				
				self.showDowels()
			
			except:
				self.faceinfo.setText(self.gNoSelection)
	
		# ############################################################################
		def setRotationP(self):
			
			try:
				if self.gRotationIndex - 1 < 0:
					self.gRotationIndex = len(self.gRotationArr) - 1
				else:
					self.gRotationIndex = self.gRotationIndex - 1
					
				self.arIS.setText(str(self.gRotationIndex+1) + " / " + str(len(self.gRotationArr)))
				
				self.showDowels()
			
			except:
				self.faceinfo.setText(self.gNoSelection)
				
		def setRotationN(self):
			
			try:
				if self.gRotationIndex + 1 > len(self.gRotationArr) - 1:
					self.gRotationIndex = 0
				else:
					self.gRotationIndex = self.gRotationIndex + 1
				
				self.arIS.setText(str(self.gRotationIndex+1) + " / " + str(len(self.gRotationArr)))
				
				self.showDowels()
			
			except:
				self.faceinfo.setText(self.gNoSelection)

		# ############################################################################
		def selectSidesP(self):
			
			try:
				if self.gSidesIndex - 1 < 0:
					self.gSidesIndex = len(self.gSidesArr) - 1
				else:
					self.gSidesIndex = self.gSidesIndex - 1
					
				self.gSides = self.gSidesArr[self.gSidesIndex]
				self.ssIS.setText(str(self.gSidesIndex+1) + " / " + str(len(self.gSidesArr)))
				
				self.showDowels()
			
			except:
				self.faceinfo.setText(self.gNoSelection)
			
		def selectSidesN(self):
			
			try:
				if self.gSidesIndex + 1 > len(self.gSidesArr) - 1:
					self.gSidesIndex = 0
				else:
					self.gSidesIndex = self.gSidesIndex + 1
					
				self.gSides = self.gSidesArr[self.gSidesIndex]
				self.ssIS.setText(str(self.gSidesIndex+1) + " / " + str(len(self.gSidesArr)))
				
				self.showDowels()
			
			except:
				self.faceinfo.setText(self.gNoSelection)
	
		# ############################################################################	
		def searchDowelInside(self):
			
			# try auto-reposition dowels
			for r in range(len(self.gRotationArr)):
				inside = self.gObj.Shape.BoundBox.isInside(self.gDowels[0].Placement.Base)
				if inside == True:
					return
				
				for s in range(len(self.gDOFSArr)):
					inside = self.gObj.Shape.BoundBox.isInside(self.gDowels[0].Placement.Base)
					if inside == True:
						return
					
					for e in range(len(self.gDOFEArr)):
						inside = self.gObj.Shape.BoundBox.isInside(self.gDowels[0].Placement.Base)
						if inside == True:
							return
				
						self.adjustEdgeN()
					self.adjustSinkN()
				self.setRotationN()

		# ############################################################################
		def autodetectDowelsPosition(self):
		
			# first set dowels inside selected face
			if not self.gCurrentSelection == 17:
				self.searchDowelInside()
			
			# try adjust only sink for screws (screw head should be flat with the surface)
			if ( 
				self.gCurrentSelection == 6 or 
				self.gCurrentSelection == 7 or 
				self.gCurrentSelection == 8 or 
				self.gCurrentSelection == 9 or 
				self.gCurrentSelection == 10 or 
				self.gCurrentSelection == 11 or 
				self.gCurrentSelection == 12 or 
				self.gCurrentSelection == 13 
				):
			
				# if CenterOfMass of selected face will be the same as CenterOfMass of dowel face3
				# this will not be working (bug) but currently I do not see better solution, 
				# let me know (open issue) if you know better solution
				
				for s in range(len(self.gDOFSArr)):
					
					fx = self.gFace.CenterOfMass.x
					dx = self.gDowels[0].Shape.Faces[2].CenterOfMass.x
				
					fy = self.gFace.CenterOfMass.y
					dy = self.gDowels[0].Shape.Faces[2].CenterOfMass.y
					
					fz = self.gFace.CenterOfMass.z
					dz = self.gDowels[0].Shape.Faces[2].CenterOfMass.z
					
					if MagicPanels.equal(fx, dx) or MagicPanels.equal(fy, dy) or MagicPanels.equal(fz, dz):
						return
					
					self.adjustSinkN()
			
			# try adjust tenons
			if self.gCurrentSelection == 17:
				
				# skip both sides option
				self.gSidesArr = []
				self.gSidesArr.append(1)
				self.gSidesArr.append(2)
				self.gSidesIndex = 0
				self.gSides = self.gSidesArr[self.gSidesIndex]
				self.ssIS.setText(str(self.gSidesIndex+1) + " / " + str(len(self.gSidesArr)))

				for sink in range(len(self.gDOFSArr)):
					for side in range(len(self.gSidesArr)):
						for e in range(len(self.gDOFEArr)):
							
							x0 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[0].X
							y0 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[0].Y
							z0 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[0].Z
							
							x1 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[1].X
							y1 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[1].Y
							z1 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[1].Z
							
							x2 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[2].X
							y2 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[2].Y
							z2 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[2].Z
							
							x3 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[3].X
							y3 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[3].Y
							z3 = MagicPanels.touchTypo(self.gDowels[0].Shape.Faces[4])[3].Z
							
							inside0 = self.gObj.Shape.BoundBox.isInside(FreeCAD.Vector(x0, y0, z0))
							inside1 = self.gObj.Shape.BoundBox.isInside(FreeCAD.Vector(x1, y1, z1))
							inside2 = self.gObj.Shape.BoundBox.isInside(FreeCAD.Vector(x2, y2, z2))
							inside3 = self.gObj.Shape.BoundBox.isInside(FreeCAD.Vector(x3, y3, z3))
							
							if inside0 == True and inside1 == True and inside2 == True and inside3 == True:
								return
					
							self.adjustEdgeN()
						self.selectSidesN()
					self.adjustSinkN()

		# ############################################################################
		def setFaceSettins(self):

			try:
			
				# remove dowels if there is no init state
				
				if len(self.gDowels) != 0:
					for d in self.gDowels:
						try:
							FreeCAD.activeDocument().removeObject(str(d.Name))
						except:
							skip = 1
			
				self.gDowels = []
			
				# read selected face info
				
				self.gObjBase = MagicPanels.getReference()
				
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				self.gFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gFIndex = MagicPanels.getFaceIndex(self.gObj, self.gFace)
				FreeCADGui.Selection.clearSelection()
				
				n = ""
				n += str(self.gObj.Label)
				n += ", "
				n += "Face"
				n += str(self.gFIndex)
				self.faceinfo.setText(n)
				
				# set thickness
				s = MagicPanels.getSizes(self.gObjBase)
				s.sort()
				self.gThick = s[0]
				
				# get plane and type
				
				self.gFPlane = MagicPanels.getFacePlane(self.gFace)
				
				[ self.gFType, 
					arrAll, 
					arrThick, 
					arrShort, 
					arrLong ] = MagicPanels.getFaceEdges(self.gObj, self.gFace)
				
				# set possible edges
				
				self.gEdgeArr = []
				
				if self.gFType == "edge":
					
					if len(arrShort) == 0:
						self.gEdgeArr = arrLong
					
					if len(arrLong) == 0:
						self.gEdgeArr = arrShort

				if self.gFType == "surface":
					self.gEdgeArr = arrAll
				
				self.gEdgeIndex = 0
				self.gEdge = self.gEdgeArr[self.gEdgeIndex]
				self.seIS.setText(str(self.gEdgeIndex+1) + " / " + str(len(self.gEdgeArr)))
				
				# get face sink
				sink = MagicPanels.getFaceSink(self.gObj, self.gFace)
				
				# set possible rotations

				self.gRotationArr = []
				
				if self.gFPlane == "XY":
					self.gRotationArr.append(0)
					self.gRotationArr.append(180)
					self.gRotation = FreeCAD.Vector(1, 0, 0)

				if self.gFPlane == "XZ":
					self.gRotationArr.append(90)
					self.gRotationArr.append(270)
					self.gRotation = FreeCAD.Vector(1, 0, 0)
					
				if self.gFPlane == "YZ":
					self.gRotationArr.append(90)
					self.gRotationArr.append(270)
					self.gRotation = FreeCAD.Vector(0, 1, 0)
				
				self.gRotationIndex = 0

				# adjust rotation
				
				if sink == "+":
					
					if self.gFPlane == "XY":
						self.gRotationIndex = 1
						
					if self.gFPlane == "XZ":
						self.gRotationIndex = 0
						
					if self.gFPlane == "YZ":
						self.gRotationIndex = 1

				else:
				
					if self.gFPlane == "XY":
						self.gRotationIndex = 0
						
					if self.gFPlane == "XZ":
						self.gRotationIndex = 1
						
					if self.gFPlane == "YZ":
						self.gRotationIndex = 0
				
				self.arIS.setText(str(self.gRotationIndex+1) + " / " + str(len(self.gRotationArr)))

				# set other settings related to dowels not face
				if not self.kcscb.isChecked():
					self.setDowelsSettings( getMenuIndex[self.dts.currentText()] )
					
				# show dowels
				self.showDowels()

				# try autodetect dowels position
				if self.pacb.isChecked():
					self.autodetectDowelsPosition()
		
			except:

				self.faceinfo.setText(self.gNoSelection)
				return -1

	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		if len(form.gDowels) != 0:
			for d in form.gDowels:
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
