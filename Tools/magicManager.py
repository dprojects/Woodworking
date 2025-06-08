import FreeCAD, FreeCADGui, Part
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate

# ###################################################################################################################
#
# Globals
#
# ###################################################################################################################


gGUI = ""

gLastSelected = ""
gObserver = ""
gVertices = []
gVerticesInfo = []
gStep = "first"


# ###################################################################################################################
#
# Observer class - irregular shapes, non-rectangle
#
# ###################################################################################################################


class SelectionObserver:
	
	def addSelection(self, doc, obj, sub, pos):
		
		global gVertices, gStep, gVerticesInfo, gLastSelected
		
		if sub.find("Edge") != -1 or sub.find("Face") != -1:
			
			vpos = FreeCAD.Vector(pos)
			
			o = FreeCAD.ActiveDocument.getObject(obj)
			gLastSelected = o
			
			ves = MagicPanels.touchTypo(o.Shape)
			ves = MagicPanels.getVerticesPosition(ves, o, "vertex")
			
			minVertexName = ""
			minOffset = ""
			
			i = 0
			for v in ves:
				
				fv = FreeCAD.Vector(v.X, v.Y, v.Z)
				offset = vpos.distanceToPoint(fv)

				if minOffset == "":
					minOffset = offset
					minVertexName = "Vertex"+str(i+1)
			
				else:
					if offset < minOffset:
						minOffset = offset
						minVertexName = "Vertex"+str(i+1)
						
				i = i + 1
				
			FreeCADGui.Selection.clearSelection()
			
			# not add vertex here to global variable 
			# the selection will call the sub vertex "if" below 
			# and will add the vertex there 
			FreeCADGui.Selection.addSelection(o, minVertexName)
			
		if sub.find("Vertex") != -1:
			
			o = FreeCAD.ActiveDocument.getObject(obj)
			gLastSelected = o
			
			if str(gGUI.shapeLE1.text()) == "first":
				sizes = MagicPanels.getSizesFromVertices(o)
				sizes.sort()
				gStep = sizes[0]
				gGUI.shapeLE1.setText(MagicPanels.unit2gui(gStep))
			
			ves = MagicPanels.touchTypo(o.Shape)
			ves = MagicPanels.getVerticesPosition(ves, o, "vertex")
			index = int(sub.replace("Vertex",""))
			v = ves[index-1]
			
			gVertices.append(( v.X, v.Y, v.Z ))
			gVerticesInfo.append(str(o.Label) + ", " + str(sub) + "\n")
			gGUI.refreshVerticesInfo()
			
	def setPreselection(self, doc, obj, sub):
		
		skip = 1

# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals
		# ############################################################################

		gMode = ""
		
		gPanel = ""
		gPanelArr = []
		gPanelIndex = 0

		gAnchorArr = []
		gAnchorIndex = 0

		gSizeArr = []
		gSizeIndex = 0
		
		gOffsetTypes = []
		gOffsetIndex = 0
		
		gSelection1 = ""
		gObj1 = ""
		gObj1Thick = 0
		gObj1Short = 0
		gObj1Long = 0

		gSelection2 = ""
		gObj2 = ""

		gFace1 = ""
		gFace2 = ""

		gFace1Plane = ""
		gFace2Plane = ""
		
		gInfoObserverOFF = translate('magicManager', 'Reading vertices: OFF')
		gInfoObserverOFF += "\n\n"
		gInfoObserverOFF += translate('magicManager', 'To create panel from vertices, click "ON" button to start reading vertices with exact order.')
		
		gInfoObserverON = translate('magicManager', 'Reading vertices: ON')
		gInfoObserverON += "\n\n"
		gInfoObserverON += translate('magicManager', 'Please select vertices in correct order to create shape. First selected vertex is automatically added to the end to close the wire.')

		
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
			
			# tool screen size
			toolSW = 260
			toolSH = 490
			
			cutLabel = toolSW - 20
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('magicManager', 'magicManager'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options
			# ############################################################################
			
			self.oModeL1 = QtGui.QLabel("", self)
			self.oModeL1.setFixedWidth(cutLabel)
			
			self.oModeL2 = QtGui.QLabel("", self)
			self.oModeL2.setFixedWidth(cutLabel)
			
			self.oModeB1 = QtGui.QPushButton(translate('magicManager', 'refresh selection'), self)
			self.oModeB1.clicked.connect(self.setMode)
			self.oModeB1.setFixedHeight(40)

			# ############################################################################
			# options - panel
			# ############################################################################

			self.spL = QtGui.QLabel(translate('magicManager', 'Plane:'), self)

			self.spBP = QtGui.QPushButton("<", self)
			self.spBP.clicked.connect(self.setPreviousPanel)
			self.spBP.setFixedWidth(50)
			self.spBP.setAutoRepeat(True)

			self.spIS = QtGui.QLabel("", self)

			self.spBN = QtGui.QPushButton(">", self)
			self.spBN.clicked.connect(self.setNextPanel)
			self.spBN.setFixedWidth(50)
			self.spBN.setAutoRepeat(True)

			# ############################################################################
			# options - anchor
			# ############################################################################
			
			self.saL = QtGui.QLabel(translate('magicManager', 'Anchor:'), self)

			self.saBP = QtGui.QPushButton("<", self)
			self.saBP.clicked.connect(self.setPreviousAnchor)
			self.saBP.setFixedWidth(50)
			self.saBP.setAutoRepeat(True)

			self.sainfo = QtGui.QLabel("", self)

			self.saBN = QtGui.QPushButton(">", self)
			self.saBN.clicked.connect(self.setNextAnchor)
			self.saBN.setFixedWidth(50)
			self.saBN.setAutoRepeat(True)

			# ############################################################################
			# options - 3rd size for the panel
			# ############################################################################
			
			self.ssL = QtGui.QLabel(translate('magicManager', 'Size:'), self)

			# button - previous
			self.ssBP = QtGui.QPushButton("<", self)
			self.ssBP.clicked.connect(self.setPreviousSize)
			self.ssBP.setFixedWidth(50)
			self.ssBP.setAutoRepeat(True)

			self.ssIS = QtGui.QLabel("", self)

			self.ssBN = QtGui.QPushButton(">", self)
			self.ssBN.clicked.connect(self.setNextSize)
			self.ssBN.setFixedWidth(50)
			self.ssBN.setAutoRepeat(True)

			# ############################################################################
			# options - offset
			# ############################################################################
			
			self.soL = QtGui.QLabel(translate('magicManager', 'Offset:'), self)

			self.soBP = QtGui.QPushButton("<", self)
			self.soBP.clicked.connect(self.setPreviousOffset)
			self.soBP.setFixedWidth(50)
			self.soBP.setAutoRepeat(True)

			self.soIS = QtGui.QLabel("", self)

			self.soBN = QtGui.QPushButton(">", self)
			self.soBN.clicked.connect(self.setNextOffset)
			self.soBN.setFixedWidth(50)
			self.soBN.setAutoRepeat(True)

			# ############################################################################
			# options - vertices reader
			# ############################################################################

			self.shapeIS = QtGui.QTextEdit(self)
			self.shapeIS.setFixedHeight(120)
			self.shapeIS.setPlainText(self.gInfoObserverOFF)
			
			self.shapeB1 = QtGui.QPushButton(translate('magicManager', 'ON'), self)
			self.shapeB1.clicked.connect(self.observerON)
			self.shapeB1.setFixedHeight(40)

			self.shapeB2 = QtGui.QPushButton(translate('magicManager', 'OFF'), self)
			self.shapeB2.clicked.connect(self.observerOFF)
			self.shapeB2.setFixedHeight(40)
			
			self.shapeB3 = QtGui.QPushButton(translate('magicManager', 'remove last'), self)
			self.shapeB3.clicked.connect(self.removeLastVertex)
			self.shapeB3.setFixedHeight(40)

			self.shapeLEL1 = QtGui.QLabel(translate('magicManager', 'New object thickness:'), self)
			
			self.shapeLE1 = QtGui.QLineEdit(self)
			self.shapeLE1.setText(str(gStep))

			self.shapeB4 = QtGui.QPushButton(translate('magicManager', 'create panel'), self)
			self.shapeB4.clicked.connect(self.createPanel)
			self.shapeB4.setFixedHeight(40)

			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.head = QtGui.QVBoxLayout()
			self.head.addWidget(self.oModeL1)
			self.head.addWidget(self.oModeL2)
			self.head.addWidget(self.oModeB1)
			
			self.body1 = QtGui.QGridLayout()
			self.body1.addWidget(self.spL, 0, 0)
			self.body1.addWidget(self.spBP, 0, 1)
			self.body1.addWidget(self.spIS, 0, 2)
			self.body1.addWidget(self.spBN, 0, 3)
			self.body1.addWidget(self.saL, 1, 0)
			self.body1.addWidget(self.saBP, 1, 1)
			self.body1.addWidget(self.sainfo, 1, 2)
			self.body1.addWidget(self.saBN, 1, 3)
			self.body1.addWidget(self.ssL, 2, 0)
			self.body1.addWidget(self.ssBP, 2, 1)
			self.body1.addWidget(self.ssIS, 2, 2)
			self.body1.addWidget(self.ssBN, 2, 3)
			self.body1.addWidget(self.soL, 3, 0)
			self.body1.addWidget(self.soBP, 3, 1)
			self.body1.addWidget(self.soIS, 3, 2)
			self.body1.addWidget(self.soBN, 3, 3)
			self.groupBody1 = QtGui.QGroupBox(None, self)
			self.groupBody1.setLayout(self.body1)
			
			self.body2 = QtGui.QVBoxLayout()
			self.body2.addWidget(self.shapeIS)
			self.body3 = QtGui.QHBoxLayout()
			self.body3.addWidget(self.shapeB1)
			self.body3.addWidget(self.shapeB2)
			self.body3.addWidget(self.shapeB3)
			self.body4 = QtGui.QHBoxLayout()
			self.body4.addWidget(self.shapeLEL1)
			self.body4.addWidget(self.shapeLE1)
			
			self.layBody2 = QtGui.QVBoxLayout()
			self.layBody2.addLayout(self.body2)
			self.layBody2.addLayout(self.body3)
			self.layBody2.addLayout(self.body4)
			self.groupBody2 = QtGui.QGroupBox(None, self)
			self.groupBody2.setLayout(self.layBody2)
			
			self.body5 = QtGui.QHBoxLayout()
			self.body5.addWidget(self.shapeB4)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			
			self.layout.addLayout(self.head)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody1)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody2)
			self.layout.addStretch()
			self.layout.addLayout(self.body5)
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
			pw = int( FreeCADGui.getMainWindow().width() - sw ) - 5
			ph = int( FreeCADGui.getMainWindow().height() - sh ) + 30
			self.setGeometry(pw, ph, sw, sh)

			# init
			self.resetGUIGlobals()
			self.setMode()
			
		# ############################################################################
		# actions - internal functions - observer
		# ############################################################################

		# ############################################################################
		def resetGUIGlobals(self):
			
			if self.gPanel != "":
				try:
					FreeCAD.ActiveDocument.removeObject(str(self.gPanel.Name))
				except:
					skip = 1
			
			self.gMode = ""

			self.gPanel = ""
			self.gPanelArr = []
			self.gPanelIndex = 0
			
			self.gSelection1 = ""
			self.gObj1 = ""
			self.gObj1Thick = 0
			self.gObj1Short = 0
			self.gObj1Long = 0
		
			self.gSelection2 = ""
			self.gObj2 = ""
		
			self.gFace1 = ""
			self.gFace2 = ""
			
			gFace1Plane = ""
			gFace2Plane = ""
			
			self.gAnchorArr = []
			self.gAnchorIndex = 0
			
			self.gSizeArr = []
			self.gSizeIndex = 0
		
			self.gOffsetTypes = [ 1, 2, 3, 4, 5, 6, 7 ]
			self.gOffsetIndex = 0
		
		def observerON(self):
			
			global gObserver, gVertices, gVerticesInfo, gGUI
			
			if gObserver == "":
				
				self.resetGUIGlobals()
				gVertices = []
				gVerticesInfo = []
				gGUI = self
				gObserver = SelectionObserver()
				FreeCADGui.Selection.addObserver(gObserver)
				self.shapeIS.setPlainText(self.gInfoObserverON)
		
		def observerOFF(self):
			
			global gObserver, gVertices, gVerticesInfo
			
			if gObserver != "":
			
				self.resetGUIGlobals()
				FreeCADGui.Selection.removeObserver(gObserver)
				gObserver = ""
				gVertices = []
				gVerticesInfo = []
				self.shapeIS.setPlainText(self.gInfoObserverOFF)
		
		def refreshVerticesInfo(self):
			
			info = ""
			for i in gVerticesInfo:
				info += i
				
			self.shapeIS.setPlainText(info)
		
		# ############################################################################
		# actions - internal functions
		# ############################################################################

		# ############################################################################
		def projectPanelFace(self, iType):

			# get settings
			size = self.gSizeArr[self.gSizeIndex]
			offset = self.gOffsetTypes[self.gOffsetIndex]
			anchor = self.gAnchorArr[self.gAnchorIndex]
			x, y, z = anchor[0], anchor[1], anchor[2]
			[ L, W, H ] = MagicPanels.sizesToCubePanel(self.gObj1, iType)
			[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(self.gSelection1)

			# set custom sizes for short edge

			if iType == "XY":
				W = size
			if iType == "YX":
				L = size
			if iType == "XZ":
				H = size
			if iType == "ZX":
				L = size
			if iType == "YZ":
				H = size
			if iType == "ZY":
				W = size

			# check if panel is valid and show only valid panels
			if L <= 0 or W <= 0 or H <= 0:
				return -1
			
			# set offsets
			if offset == 2:
				x = x - size
			if offset == 3:
				x = x + size
			if offset == 4:
				y = y - size
			if offset == 5:
				y = y + size
			if offset == 6:
				z = z - size
			if offset == 7:
				z = z + size

			# add cointainer offset
			x = x + coX
			y = y + coY
			z = z + coZ

			# create panel
			self.gPanel = FreeCAD.ActiveDocument.addObject("Part::Box", "panelFace"+iType)
			self.gPanel.Length, self.gPanel.Width, self.gPanel.Height = L, W, H

			# add settings to panel
			self.gPanel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
			MagicPanels.setColor(self.gPanel, 0, (0.0, 0.0, 0.0, 1.0), "color")
			MagicPanels.setColor(self.gPanel, 0, 83, "trans", "RGBA")
			
			MagicPanels.addRotation(self.gObj1, [ self.gPanel ])
			
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def projectPanelBetween(self, iType):

			# get settings
			size = self.gSizeArr[self.gSizeIndex]
			offset = self.gOffsetTypes[self.gOffsetIndex]
			anchor = self.gAnchorArr[self.gAnchorIndex]

			if self.gSelection1.isDerivedFrom("Part::Cut"):
				c1 = self.gSelection1
			else:
				c1 = self.gObj1
				
			if self.gSelection2.isDerivedFrom("Part::Cut"):
				c2 = self.gSelection2
			else:
				c2 = self.gObj2

			facesDistance = MagicPanels.getDistanceBetweenFaces(c1, c2, self.gFace1, self.gFace2)

			x, y, z = anchor[0], anchor[1], anchor[2]
			L, W, H = 0, 0, 0

			# set panel sizes along X
			if self.gFace1Plane == "YZ":

				if iType == "XY":
					L = facesDistance
					W = size
					H = self.gObj1Thick

				if iType ==	"XZ":
					L = facesDistance
					W = self.gObj1Thick
					H = size

			# set panel sizes along Y
			if self.gFace1Plane == "XZ":

				if iType == "XY":
					L = size
					W = facesDistance
					H = self.gObj1Thick

				if iType == "YZ":
					L = self.gObj1Thick
					W = facesDistance
					H = size

			# set panel sizes along Z
			if self.gFace1Plane == "XY":

				if iType ==	"XZ":
					L = size
					W = self.gObj1Thick
					H = facesDistance

				if iType == "YZ":
					L = self.gObj1Thick
					W = size
					H = facesDistance

			# check if panel is valid and show only valid panels
			if L <= 0 or W <= 0 or H <= 0:
				return -1

			# set offsets
			if offset == 2:
				x = x - size
			if offset == 3:
				x = x + size
			if offset == 4:
				y = y - size
			if offset == 5:
				y = y + size
			if offset == 6:
				z = z - size
			if offset == 7:
				z = z + size

			# add cointainer offset for PartDesign object and skip Cut
			if self.gSelection1.isDerivedFrom("Part::Cut"):
				skip = 1
			else:
				[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(self.gObj1)
				x = x + coX
				y = y + coY
				z = z + coZ

			# create panel
			self.gPanel = FreeCAD.ActiveDocument.addObject("Part::Box", "panelBetween"+iType)
			self.gPanel.Visibility = False
			self.gPanel.Length, self.gPanel.Width, self.gPanel.Height = L, W, H

			# add settings to panel
			self.gPanel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
			MagicPanels.setColor(self.gPanel, 0, (0.0, 0.0, 0.0, 1.0), "color")
			MagicPanels.setColor(self.gPanel, 0, 83, "trans", "RGBA")
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def previewPanel(self):

			try:
				FreeCAD.ActiveDocument.removeObject(str(self.gPanel.Name))
			except:
				skip = 1

			# update info screens

			info = str(self.gPanelIndex + 1) + " / " + str(len(self.gPanelArr))
			self.spIS.setText(info)
			
			info = str(self.gAnchorIndex + 1) + " / " + str(len(self.gAnchorArr))
			self.sainfo.setText(info)
			
			info = str(self.gSizeIndex + 1) + " / " + str(len(self.gSizeArr))
			self.ssIS.setText(info)

			info = str(self.gOffsetIndex + 1) + " / " + str(len(self.gOffsetTypes))
			self.soIS.setText(info)

			# show panel
			
			if self.gMode == "Face":
				self.projectPanelFace(self.gPanelArr[self.gPanelIndex])

			if self.gMode == "Between":
				self.projectPanelBetween(self.gPanelArr[self.gPanelIndex])

			# move to container

			if self.gMode == "Between" and self.gSelection2.isDerivedFrom("Part::Mirroring"):
				MagicPanels.moveToClean([ self.gPanel ], self.gObj1)
			else:
				MagicPanels.moveToFirst([ self.gPanel ], self.gObj1)

			self.gPanel.Visibility = True

		# ############################################################################
		def setMode(self):
			
			try:
				FreeCAD.ActiveDocument.removeObject(str(self.gPanel.Name))
			except:
				skip = 1
				
			self.setSelection()
			
			if self.gFace1 == "":

				self.gMode = ""
				self.oModeL1.setText(translate('magicManager', '1. select single face for panel at face'))
				self.oModeL2.setText(translate('magicManager', '2. select 2 faces for panel between'))

				return

			if self.gFace2 == "":

				self.gMode = "Face"
				
				index = MagicPanels.getFaceIndex(self.gSelection1, self.gFace1)
				info = str(self.gSelection1.Label) + ", " + "Face" + str(index)
				
				self.oModeL1.setText(info)
				self.oModeL2.setText("")
				
				self.gPanelArr = [ "XY", "YX", "XZ", "ZX", "YZ", "ZY" ]
				self.gPanelIndex = 5
				
			else:
				self.gMode = "Between"
				index1 = MagicPanels.getFaceIndex(self.gSelection1, self.gFace1)
				index2 = MagicPanels.getFaceIndex(self.gSelection2, self.gFace2)
				
				info = ""
				info += str(self.gSelection1.Label)
				info += ", " + "Face" + str(index1)
				self.oModeL1.setText(info)
				
				info = ""
				info += str(self.gSelection2.Label)
				info += ", " + "Face" + str(index2)
				self.oModeL2.setText(info)
				
				if self.gFace1Plane == "YZ":
					self.gPanelArr = [ "XY", "XZ" ]
				if self.gFace1Plane == "XZ":
					self.gPanelArr = [ "XY", "YZ" ]
				if self.gFace1Plane == "XY":
					self.gPanelArr = [ "XZ", "YZ" ]
				
				self.gPanelIndex = 1

			# init panel
			self.setNextPanel()
		
		# ############################################################################
		def setSelection(self):
			
			self.resetGUIGlobals()
			
			try:
				self.gSelection1 = FreeCADGui.Selection.getSelection()[0]
				
				if MagicPanels.isType(self.gSelection1, "Clone"):
					self.gObj1 = self.gSelection1
				else:
					self.gObj1 = MagicPanels.getReference(self.gSelection1)
			except:
				return

			try:
				self.gSelection2 = FreeCADGui.Selection.getSelection()[1]
				
				if MagicPanels.isType(self.gSelection2, "Clone"):
					self.gObj2 = self.gSelection2
				else:
					self.gObj2 = MagicPanels.getReference(self.gSelection2)
			except:
				skip = 1

			try:
				self.gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gFace1Plane = MagicPanels.getFacePlane(self.gFace1)
				
				if MagicPanels.isType(self.gSelection1, "Clone"):
					sizes = MagicPanels.getSizesFromVertices(self.gObj1)
				else:
					sizes = MagicPanels.getSizes(self.gObj1)

				sizes.sort()
				self.gObj1Thick = sizes[0]
				self.gObj1Short = sizes[1]
				self.gObj1Long = sizes[2]

				self.gAnchorArr = MagicPanels.getFaceVertices(self.gFace1, "all")
				[ a1, edges, a2, a3, a4 ] = MagicPanels.getFaceEdges(self.gSelection1, self.gFace1)

				noRepeat = dict()
				for e in edges:
					noRepeat[str(e.Length)] = e.Length

				noRepeat[str(self.gObj1Thick)] = self.gObj1Thick
				noRepeat[str(self.gObj1Short)] = self.gObj1Short
				noRepeat[str(self.gObj1Long)] = self.gObj1Long
				
				self.gSizeArr = list(noRepeat.values())

			except:
				skip = 1
			
			try:
				self.gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				self.gFace2Plane = MagicPanels.getFacePlane(self.gFace2)
			except:
				skip = 1

			FreeCADGui.Selection.clearSelection()

		# ############################################################################
		# actions - buttons functions
		# ############################################################################

		# ############################################################################
		def setPreviousPanel(self):
			if self.gPanelIndex == 0:
				self.gPanelIndex = len(self.gPanelArr) - 1
			else:
				self.gPanelIndex = self.gPanelIndex - 1
			self.previewPanel()

		def setNextPanel(self):
			if self.gPanelIndex == len(self.gPanelArr) - 1:
				self.gPanelIndex = 0
			else:
				self.gPanelIndex = self.gPanelIndex + 1
			self.previewPanel()

		# ############################################################################
		def setPreviousOffset(self):
			if self.gOffsetIndex == 0:
				self.gOffsetIndex = len(self.gOffsetTypes) - 1
			else:
				self.gOffsetIndex = self.gOffsetIndex - 1
			self.previewPanel()

		def setNextOffset(self):
			if self.gOffsetIndex == len(self.gOffsetTypes) - 1:
				self.gOffsetIndex = 0
			else:
				self.gOffsetIndex = self.gOffsetIndex + 1
			self.previewPanel()

		# ############################################################################
		def setPreviousAnchor(self):
			if self.gAnchorIndex == 0:
				self.gAnchorIndex = len(self.gAnchorArr) - 1
			else:
				self.gAnchorIndex = self.gAnchorIndex - 1
			self.previewPanel()

		def setNextAnchor(self):
			if self.gAnchorIndex == len(self.gAnchorArr) - 1:
				self.gAnchorIndex = 0
			else:
				self.gAnchorIndex = self.gAnchorIndex + 1
			self.previewPanel()
		
		# ############################################################################
		def setPreviousSize(self):
			if self.gSizeIndex == 0:
				self.gSizeIndex = len(self.gSizeArr) - 1
			else:
				self.gSizeIndex = self.gSizeIndex - 1
			self.previewPanel()

		def setNextSize(self):
			if self.gSizeIndex == len(self.gSizeArr) - 1:
				self.gSizeIndex = 0
			else:
				self.gSizeIndex = self.gSizeIndex + 1
			self.previewPanel()

		# ############################################################################
		def removeLastVertex(self):
			
			global gVertices, gVerticesInfo
			
			if len(gVerticesInfo) > 0:
				gVertices.pop()
				gVerticesInfo.pop()
				gGUI.refreshVerticesInfo()
		
		# ############################################################################
		def setPanel(self):
			
			if self.gPanel != "":
				
				try:
					if self.gSelection1.isDerivedFrom("Part::Cut"):
						MagicPanels.copyColors(self.gSelection1, self.gPanel)
					else:
						MagicPanels.copyColors(self.gObj1, self.gPanel)
				except:
					skip = 1

				MagicPanels.setColor(self.gPanel, 0, 0, "trans", "RGBA")
				self.gPanel = ""
		
		# ############################################################################
		def setPanelFromVertices(self):
			
			global gVertices, gVerticesInfo
			import Draft
			
			doc = FreeCAD.ActiveDocument
			
			# create face from vertices
			if len(gVertices) > 0:
				gVertices.append(gVertices[0])
			
			shape = Part.makePolygon(gVertices)
			face = Part.Face(shape)
			
			# first create Part, Body structure
			part = doc.addObject('App::Part', 'Part')
			part.Label = "Part, vertices2panel "
			body = doc.addObject('PartDesign::Body', 'Body')
			body.Label = "Body, vertices2panel "
			part.addObject(body)
			
			# create Sketch and move it to the Body
			draftSketch = Draft.make_sketch(face, autoconstraints = True)
			draftSketch.Label = "Pattern, magicPanel "
			
			draftSketch.adjustRelativeLinks(body)
			body.ViewObject.dropObject(draftSketch,None,'',[])
			doc.recompute()
			
			# create Pad with the Sketch
			pad = body.newObject('PartDesign::Pad', "magicpanel")
			pad.Label = "magicPanel "
			pad.Profile = draftSketch
			t = MagicPanels.unit2value(gGUI.shapeLE1.text())
			pad.Length = FreeCAD.Units.Quantity(str(t))
			draftSketch.Visibility = False
			doc.recompute()
			
			MagicPanels.moveToFirstWithInverse([ part ], gLastSelected)
			
			# set color of last selected object
			try:
				MagicPanels.copyColors(gLastSelected, pad)
			except:
				skip = 1
			
			# turn off observer after operation
			if gObserver != "":
				self.observerOFF()
		
		# ############################################################################
		def createPanel(self):

			if gObserver != "":
				self.setPanelFromVertices()
			else:
				self.setPanel()
		
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		
		if form.gPanel != "":
			try:
				FreeCAD.ActiveDocument.removeObject(str(form.gPanel.Name))
			except:
				skip = 1
		
		if gObserver != "":
			try:
				FreeCADGui.Selection.removeObserver(gObserver)
			except:
				skip = 1
		
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
