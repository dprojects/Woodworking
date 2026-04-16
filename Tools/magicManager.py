import FreeCAD, FreeCADGui, Part
from PySide import QtGui, QtCore

import MagicPanels

MagicPanels.initConfig()
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
gSketch = []
gCurve = []

gVerticesInfo = []
gSketchInfo = []
gCurveInfo = []

gVerticesThickness = "first"

# add new items only at the end and change self.sModeList
getMenuIndex1 = {
	translate('magicManager', 'regular rectangle panel'): 0, 
	translate('magicManager', 'panel from vertices (irregular)'): 1, 
	translate('magicManager', 'sketch from vertices (curve pattern)'): 2, 
	translate('magicManager', 'panel along curve (based on sketch)'): 3 # no comma
}

# ###################################################################################################################
#
# Observer class - irregular shapes, non-rectangle
#
# ###################################################################################################################


class SelectionObserver:
	
	def addSelection(self, doc, obj, sub, pos):
		
		global gVertices, gSketch, gCurve
		global gVerticesInfo, gSketchInfo, gCurveInfo
		global gVerticesThickness, gLastSelected
		
		# set reference
		o = FreeCAD.ActiveDocument.getObject(obj)
		
		if gGUI.gModeType == 1:
			objects = gVertices
			info = gVerticesInfo
		
		if gGUI.gModeType == 2:
			objects = gSketch
			info = gSketchInfo
		
		if gGUI.gModeType == 3:
			objects = gCurve
			info = gCurveInfo

		# read selection
		if gGUI.gModeType == 1 or gGUI.gModeType == 2:
			
			# if edge or face has been selected instead of vertex
			# search for minimum distance to vertex from selection
			if sub.find("Edge") != -1 or sub.find("Face") != -1:
	
				gLastSelected = o
				vpos = FreeCAD.Vector(pos)
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
			
			# at this level the vertex should be selected by user or by selection helper above
			if sub.find("Vertex") != -1:
				
				gLastSelected = o
				
				if str(gGUI.oVerticesThicknessE.text()) == "first":
					sizes = MagicPanels.getSizesFromVertices(o)
					sizes.sort()
					gVerticesThickness = sizes[0]
					gGUI.oVerticesThicknessE.setText(MagicPanels.unit2gui(gVerticesThickness))
				
				ves = MagicPanels.touchTypo(o.Shape)
				ves = MagicPanels.getVerticesPosition(ves, o, "vertex")
				index = int(sub.replace("Vertex",""))
				v = ves[index-1]
				
				objects.append(( v.X, v.Y, v.Z ))
				info.append(str(o.Label) + ", " + str(sub) + "\n")
				gGUI.refreshInfo()
			
		if gGUI.gModeType == 3:
			
			if o.isDerivedFrom("Sketcher::SketchObject"):
				objects.append(str(o.Name))
				info.append(str(o.Label) + "\n")
				gGUI.refreshInfo()
			
			if sub.find("Edge") != -1 and not o.isDerivedFrom("Sketcher::SketchObject"):
				objects.append(str(o.Name)+":"+str(sub))
				info.append(str(o.Label) + ", " + str(sub) + "\n")
				gGUI.refreshInfo()
			
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

		gModeType = 0
		
		gSimpleType = ""
		gSimpleInfo1 = translate('magicManager', 'select single face for panel at face')
		gSimpleInfo2 = translate('magicManager', 'select two faces for panel between')
		
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
		
		gVerticesObserverOFF = translate('magicManager', 'Reading vertices: OFF')
		gVerticesObserverOFF += "\n\n"
		gVerticesObserverOFF += translate('magicManager', 'To create panel from vertices, click "turn it on" button to start reading vertices with exact order.')
		
		gVerticesObserverON = translate('magicManager', 'Reading vertices: ON')
		gVerticesObserverON += "\n\n"
		gVerticesObserverON += translate('magicManager', 'Please select vertices in correct order to create shape. First selected vertex is automatically added to the end to close the entire edge.')

		gSketchObserverOFF = translate('magicManager', 'Reading vertices: OFF')
		gSketchObserverOFF += "\n\n"
		gSketchObserverOFF += translate('magicManager', 'To create sketch pattern for panel along curve option, click "turn it on" button to start reading vertices with exact order.')
		
		gSketchObserverON = translate('magicManager', 'Reading vertices: ON')
		gSketchObserverON += "\n\n"
		gSketchObserverON += translate('magicManager', 'Please select vertices in correct order to create sketch. First selected vertex is automatically added to the end to close the entire edge.')

		gCurveObserverOFF = translate('magicManager', 'Reading edges: OFF')
		gCurveObserverOFF += "\n\n"
		gCurveObserverOFF += translate('magicManager', 'To create panel along curve, click "turn it on" button to start reading sketch pattern and edges as curve path for panel.')
		
		gCurveObserverON = translate('magicManager', 'Reading edges: ON')
		gCurveObserverON += "\n\n"
		gCurveObserverON += translate('magicManager', 'Please select sketch and edges in correct order to create curve path. First selected should be sketch and next edges with exact order to create correct curve path for panel.')

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
			toolSW = 301
			toolSH = 380
			
			cutLabel = toolSW - 20
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('magicManager', 'magicManager'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			self.setMinimumSize(toolSW, toolSH)

			# ############################################################################
			# selection
			# ############################################################################
			
			self.sModeList = (
				translate('magicManager', 'regular rectangle panel'), 
				translate('magicManager', 'panel from vertices (irregular)'), 
				translate('magicManager', 'sketch from vertices (curve pattern)'), 
				translate('magicManager', 'panel along curve (based on sketch)') # no comma
			)

			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(0) # default
			self.sMode.textActivated[str].connect(self.setModeType)

			# ############################################################################
			# simple panel
			# ############################################################################
			
			self.oSimpleInfo1 = QtGui.QLabel("", self)
			self.oSimpleInfo1.setFixedWidth(cutLabel)
			
			self.oSimpleInfo2 = QtGui.QLabel("", self)
			self.oSimpleInfo2.setFixedWidth(cutLabel)
			
			self.oSimpleInfoB1 = QtGui.QPushButton(translate('magicManager', 'refresh selection'), self)
			self.oSimpleInfoB1.clicked.connect(self.simpleRefresh)
			self.oSimpleInfoB1.setFixedHeight(40)

			self.oSimpleSurfaceL = QtGui.QLabel(translate('magicManager', 'Surface:'), self)

			self.oSimpleSurfaceBP = QtGui.QPushButton("<", self)
			self.oSimpleSurfaceBP.clicked.connect(self.setPreviousPanel)
			self.oSimpleSurfaceBP.setFixedWidth(50)
			self.oSimpleSurfaceBP.setAutoRepeat(True)

			self.oSimpleSurfaceInfo = QtGui.QLabel("", self)

			self.oSimpleSurfaceBN = QtGui.QPushButton(">", self)
			self.oSimpleSurfaceBN.clicked.connect(self.setNextPanel)
			self.oSimpleSurfaceBN.setFixedWidth(50)
			self.oSimpleSurfaceBN.setAutoRepeat(True)

			self.oSimpleAnchorL = QtGui.QLabel(translate('magicManager', 'Anchor:'), self)

			self.oSimpleAnchorBP = QtGui.QPushButton("<", self)
			self.oSimpleAnchorBP.clicked.connect(self.setPreviousAnchor)
			self.oSimpleAnchorBP.setFixedWidth(50)
			self.oSimpleAnchorBP.setAutoRepeat(True)

			self.oSimpleAnchorInfo = QtGui.QLabel("", self)

			self.oSimpleAnchorBN = QtGui.QPushButton(">", self)
			self.oSimpleAnchorBN.clicked.connect(self.setNextAnchor)
			self.oSimpleAnchorBN.setFixedWidth(50)
			self.oSimpleAnchorBN.setAutoRepeat(True)

			self.oSimpleSizeL = QtGui.QLabel(translate('magicManager', 'Size:'), self)

			# button - previous
			self.oSimpleSizeBP = QtGui.QPushButton("<", self)
			self.oSimpleSizeBP.clicked.connect(self.setPreviousSize)
			self.oSimpleSizeBP.setFixedWidth(50)
			self.oSimpleSizeBP.setAutoRepeat(True)

			self.oSimpleSizeInfo = QtGui.QLabel("", self)

			self.oSimpleSizeBN = QtGui.QPushButton(">", self)
			self.oSimpleSizeBN.clicked.connect(self.setNextSize)
			self.oSimpleSizeBN.setFixedWidth(50)
			self.oSimpleSizeBN.setAutoRepeat(True)

			self.oSimpleOffsetL = QtGui.QLabel(translate('magicManager', 'Offset:'), self)

			self.oSimpleOffsetBP = QtGui.QPushButton("<", self)
			self.oSimpleOffsetBP.clicked.connect(self.setPreviousOffset)
			self.oSimpleOffsetBP.setFixedWidth(50)
			self.oSimpleOffsetBP.setAutoRepeat(True)

			self.oSimpleOffsetInfo = QtGui.QLabel("", self)

			self.oSimpleOffsetBN = QtGui.QPushButton(">", self)
			self.oSimpleOffsetBN.clicked.connect(self.setNextOffset)
			self.oSimpleOffsetBN.setFixedWidth(50)
			self.oSimpleOffsetBN.setAutoRepeat(True)

			# ############################################################################
			# panel from vertices
			# ############################################################################

			self.oVerticesInfo = QtGui.QTextEdit(self)
			self.oVerticesInfo.setFixedHeight(180)
			self.oVerticesInfo.setPlainText(self.gVerticesObserverOFF)
			
			self.oVerticesON = QtGui.QPushButton(translate('magicManager', 'turn it on'), self)
			self.oVerticesON.clicked.connect(self.setVerticesObserverON)
			self.oVerticesON.setFixedHeight(40)

			self.oVerticesOFF = QtGui.QPushButton(translate('magicManager', 'turn it off'), self)
			self.oVerticesOFF.clicked.connect(self.setVerticesObserverOFF)
			self.oVerticesOFF.setFixedHeight(40)
			
			self.oVerticesREMOVE = QtGui.QPushButton(translate('magicManager', 'remove last'), self)
			self.oVerticesREMOVE.clicked.connect(self.removeVerticesVertex)
			self.oVerticesREMOVE.setFixedHeight(40)

			self.oVerticesThicknessL = QtGui.QLabel(translate('magicManager', 'New object thickness:'), self)
			
			self.oVerticesThicknessE = QtGui.QLineEdit(self)
			self.oVerticesThicknessE.setText(str(gVerticesThickness))

			# ############################################################################
			# sketch from vertices
			# ############################################################################

			self.oSketchInfo = QtGui.QTextEdit(self)
			self.oSketchInfo.setFixedHeight(180)
			self.oSketchInfo.setPlainText(self.gSketchObserverOFF)
			
			self.oSketchON = QtGui.QPushButton(translate('magicManager', 'turn it on'), self)
			self.oSketchON.clicked.connect(self.setSketchObserverON)
			self.oSketchON.setFixedHeight(40)

			self.oSketchOFF = QtGui.QPushButton(translate('magicManager', 'turn it off'), self)
			self.oSketchOFF.clicked.connect(self.setSketchObserverOFF)
			self.oSketchOFF.setFixedHeight(40)
			
			self.oSketchREMOVE = QtGui.QPushButton(translate('magicManager', 'remove last'), self)
			self.oSketchREMOVE.clicked.connect(self.removeSketchVertex)
			self.oSketchREMOVE.setFixedHeight(40)

			# ############################################################################
			# panel along curve
			# ############################################################################

			self.oCurveInfo = QtGui.QTextEdit(self)
			self.oCurveInfo.setFixedHeight(180)
			self.oCurveInfo.setPlainText(self.gCurveObserverOFF)
			
			self.oCurveON = QtGui.QPushButton(translate('magicManager', 'turn it on'), self)
			self.oCurveON.clicked.connect(self.setCurveObserverON)
			self.oCurveON.setFixedHeight(40)

			self.oCurveOFF = QtGui.QPushButton(translate('magicManager', 'turn it off'), self)
			self.oCurveOFF.clicked.connect(self.setCurveObserverOFF)
			self.oCurveOFF.setFixedHeight(40)
			
			self.oCurveREMOVE = QtGui.QPushButton(translate('magicManager', 'remove last'), self)
			self.oCurveREMOVE.clicked.connect(self.removeCurveVertex)
			self.oCurveREMOVE.setFixedHeight(40)

			# ############################################################################
			# create button
			# ############################################################################
			
			self.oCreateButton = QtGui.QPushButton(translate('magicManager', 'create'), self)
			self.oCreateButton.clicked.connect(self.createPanel)
			self.oCreateButton.setFixedHeight(40)

			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# selection
			self.laySelection = QtGui.QVBoxLayout()
			self.laySelection.addWidget(self.sMode)
			
			# simple panel
			self.laySimple1 = QtGui.QVBoxLayout()
			self.laySimple1.addWidget(self.oSimpleInfo1)
			self.laySimple1.addWidget(self.oSimpleInfo2)
			self.laySimple1.addWidget(self.oSimpleInfoB1)
			
			self.laySimple2 = QtGui.QGridLayout()
			self.laySimple2.addWidget(self.oSimpleSurfaceL, 0, 0)
			self.laySimple2.addWidget(self.oSimpleSurfaceBP, 0, 1)
			self.laySimple2.addWidget(self.oSimpleSurfaceInfo, 0, 2)
			self.laySimple2.addWidget(self.oSimpleSurfaceBN, 0, 3)
			self.laySimple2.addWidget(self.oSimpleAnchorL, 1, 0)
			self.laySimple2.addWidget(self.oSimpleAnchorBP, 1, 1)
			self.laySimple2.addWidget(self.oSimpleAnchorInfo, 1, 2)
			self.laySimple2.addWidget(self.oSimpleAnchorBN, 1, 3)
			self.laySimple2.addWidget(self.oSimpleSizeL, 2, 0)
			self.laySimple2.addWidget(self.oSimpleSizeBP, 2, 1)
			self.laySimple2.addWidget(self.oSimpleSizeInfo, 2, 2)
			self.laySimple2.addWidget(self.oSimpleSizeBN, 2, 3)
			self.laySimple2.addWidget(self.oSimpleOffsetL, 3, 0)
			self.laySimple2.addWidget(self.oSimpleOffsetBP, 3, 1)
			self.laySimple2.addWidget(self.oSimpleOffsetInfo, 3, 2)
			self.laySimple2.addWidget(self.oSimpleOffsetBN, 3, 3)
			self.groupSimple2 = QtGui.QGroupBox(None, self)
			self.groupSimple2.setLayout(self.laySimple2)
			
			# panel from vertices
			self.layVertices1 = QtGui.QVBoxLayout()
			self.layVertices1.addWidget(self.oVerticesInfo)
			self.layVertices2 = QtGui.QHBoxLayout()
			self.layVertices2.addWidget(self.oVerticesON)
			self.layVertices2.addWidget(self.oVerticesOFF)
			self.layVertices3 = QtGui.QVBoxLayout()
			self.layVertices3.addWidget(self.oVerticesREMOVE)
			self.layVertices4 = QtGui.QHBoxLayout()
			self.layVertices4.addWidget(self.oVerticesThicknessL)
			self.layVertices4.addWidget(self.oVerticesThicknessE)
			
			self.layVertices = QtGui.QVBoxLayout()
			self.layVertices.addLayout(self.layVertices1)
			self.layVertices.addLayout(self.layVertices2)
			self.layVertices.addLayout(self.layVertices3)
			self.layVertices.addLayout(self.layVertices4)
			self.groupVertices = QtGui.QGroupBox(None, self)
			self.groupVertices.setLayout(self.layVertices)
			
			# sketch from vertices
			self.laySketch1 = QtGui.QVBoxLayout()
			self.laySketch1.addWidget(self.oSketchInfo)
			self.laySketch2 = QtGui.QHBoxLayout()
			self.laySketch2.addWidget(self.oSketchON)
			self.laySketch2.addWidget(self.oSketchOFF)
			self.laySketch3 = QtGui.QVBoxLayout()
			self.laySketch3.addWidget(self.oSketchREMOVE)
			
			self.laySketch = QtGui.QVBoxLayout()
			self.laySketch.addLayout(self.laySketch1)
			self.laySketch.addLayout(self.laySketch2)
			self.laySketch.addLayout(self.laySketch3)
			self.groupSketch = QtGui.QGroupBox(None, self)
			self.groupSketch.setLayout(self.laySketch)
			
			# panel along curve
			self.layCurve1 = QtGui.QVBoxLayout()
			self.layCurve1.addWidget(self.oCurveInfo)
			self.layCurve2 = QtGui.QHBoxLayout()
			self.layCurve2.addWidget(self.oCurveON)
			self.layCurve2.addWidget(self.oCurveOFF)
			self.layCurve3 = QtGui.QVBoxLayout()
			self.layCurve3.addWidget(self.oCurveREMOVE)
			
			self.layCurve = QtGui.QVBoxLayout()
			self.layCurve.addLayout(self.layCurve1)
			self.layCurve.addLayout(self.layCurve2)
			self.layCurve.addLayout(self.layCurve3)
			self.groupCurve = QtGui.QGroupBox(None, self)
			self.groupCurve.setLayout(self.layCurve)
			
			# create button
			self.layCreate = QtGui.QHBoxLayout()
			self.layCreate.addWidget(self.oCreateButton)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			self.layout.addLayout(self.laySelection)
			self.layout.addStretch()
			self.layout.addLayout(self.laySimple1)
			self.layout.addStretch()
			self.layout.addWidget(self.groupSimple2)
			self.layout.addStretch()
			self.layout.addWidget(self.groupVertices)
			self.layout.addStretch()
			self.layout.addWidget(self.groupSketch)
			self.layout.addStretch()
			self.layout.addWidget(self.groupCurve)
			self.layout.addStretch()
			self.layout.addLayout(self.layCreate)
			self.setLayout(self.layout)

			# hide
			self.groupVertices.hide()
			self.groupSketch.hide()
			self.groupCurve.hide()
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# set theme
			MagicPanels.setTheme(self)
			
			# show window
			self.show()

			MagicPanels.adjustGUI(self, "right-bottom")

			# init
			self.resetGUIGlobals()
			self.simpleRefresh()
			
		# ############################################################################
		# actions - internal functions - observer
		# ############################################################################

		# ############################################################################
		def resetGUIGlobals(self):
			
			global gVertices, gVerticesInfo
			global gSketch, gSketchInfo
			global gCurve, gCurveInfo
			
			if self.gPanel != "":
				try:
					FreeCAD.ActiveDocument.removeObject(str(self.gPanel.Name))
				except:
					skip = 1
			
			self.gSimpleType = ""

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
		
			gVertices = []
			gVerticesInfo = []
			
			gSketch = []
			gSketchInfo = []
			
			gCurve = []
			gCurveInfo = []
			
		# ############################################################################
		def refreshInfo(self):
			
			if self.gModeType == 1:
				
				info = ""
				for i in gVerticesInfo:
					info += i
					
				self.oVerticesInfo.setPlainText(info)
		
			if self.gModeType == 2:
				
				info = ""
				for i in gSketchInfo:
					info += i
					
				self.oSketchInfo.setPlainText(info)
			
			if self.gModeType == 3:
				
				info = ""
				for i in gCurveInfo:
					info += i
					
				self.oCurveInfo.setPlainText(info)
				
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
			self.oSimpleSurfaceInfo.setText(info)
			
			info = str(self.gAnchorIndex + 1) + " / " + str(len(self.gAnchorArr))
			self.oSimpleAnchorInfo.setText(info)
			
			info = str(self.gSizeIndex + 1) + " / " + str(len(self.gSizeArr))
			self.oSimpleSizeInfo.setText(info)

			info = str(self.gOffsetIndex + 1) + " / " + str(len(self.gOffsetTypes))
			self.oSimpleOffsetInfo.setText(info)

			# show panel
			
			if self.gSimpleType == "Face":
				self.projectPanelFace(self.gPanelArr[self.gPanelIndex])

			if self.gSimpleType == "Between":
				self.projectPanelBetween(self.gPanelArr[self.gPanelIndex])

			# move to container

			if self.gSimpleType == "Between" and self.gSelection2.isDerivedFrom("Part::Mirroring"):
				MagicPanels.moveToClean([ self.gPanel ], self.gObj1)
			else:
				MagicPanels.moveToFirst([ self.gPanel ], self.gObj1)

			self.gPanel.Visibility = True

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
			t = MagicPanels.unit2value(gGUI.oVerticesThicknessE.text())
			pad.Length = FreeCAD.Units.Quantity(str(t))
			draftSketch.Visibility = False
			doc.recompute()
			
			MagicPanels.moveToFirstWithInverse([ part ], gLastSelected)
			
			# set color of last selected object
			MagicPanels.copyColors(gLastSelected, pad)
			MagicPanels.copyColors(gLastSelected, body)
			
			# turn off observer after operation
			if gObserver != "":
				self.setVerticesObserverOFF()
		
		# ############################################################################
		def setSketchFromVertices(self):
			
			global gVertices, gVerticesInfo
			import Draft
			
			doc = FreeCAD.ActiveDocument
			
			# create face from vertices
			if len(gSketch) > 0:
				gSketch.append(gSketch[0])
			
			shape = Part.makePolygon(gSketch)
			face = Part.Face(shape)
			
			# first create Part, Body structure
			part = doc.addObject('App::Part', 'Part')
			part.Label = "Part, vertices2sketch "
			body = doc.addObject('PartDesign::Body', 'Body')
			body.Label = "Body, vertices2sketch "
			part.addObject(body)
			
			# create Sketch and move it to the Body
			draftSketch = Draft.make_sketch(face, autoconstraints = True)
			draftSketch.Label = "Pattern, vertices2sketch "
			
			draftSketch.adjustRelativeLinks(body)
			body.ViewObject.dropObject(draftSketch,None,'',[])
			doc.recompute()
			
			# set color of last selected object
			MagicPanels.copyColors(gLastSelected, body)
			
			# turn off observer after operation
			if gObserver != "":
				self.setSketchObserverOFF()
		
		# ############################################################################
		def setPanelAlongCurve(self):

			FreeCADGui.Selection.clearSelection()
			
			for item in gCurve:
				split = item.split(":")
				o = FreeCAD.ActiveDocument.getObject(split[0])
				
				if o.isDerivedFrom("Sketcher::SketchObject"):
					sketch = o
					body = MagicPanels.getBody(sketch)
				
				if len(split) == 2:
					edge = split[1]
					FreeCADGui.Selection.addSelection(o, edge)
			
			FreeCADGui.ActiveDocument.ActiveView.setActiveObject('pdbody', body)
			FreeCADGui.runCommand("PartDesign_SubShapeBinder", 0)

			objects = FreeCAD.ActiveDocument.Objects
			binder = objects[len(objects)-1]
			binder.Label = translate('magicManager', 'curve')

			FreeCADGui.ActiveDocument.ActiveView.setActiveObject('pdbody', None)
			FreeCADGui.Selection.clearSelection()
			FreeCAD.ActiveDocument.recompute()

			panel = body.newObject('PartDesign::AdditivePipe','curve2panel')
			panel.Profile = sketch
			sketch.Visibility = False
			
			sizes = MagicPanels.getSizes(sketch)
			sizes.sort()
			Height = sizes[1]
			Width = sizes[2]
			Length = 0
			
			for e in binder.Shape.Edges:
				Length = Length + e.Length
			
			edges = []
			for i in range(1, len(binder.Shape.Edges)+1):
				edges.append( 'Edge'+str(i) )
		
			panel.Spine = (binder, edges)
			FreeCAD.ActiveDocument.recompute()
			panel.Visibility = True
			binder.Visibility = False
			
			MagicPanels.copyColors(body, panel)
		
			info = translate("magicManager", "Height means thickness.")
			panel.addProperty("App::PropertyLength", "Woodworking_Height", "Woodworking", info)
			panel.Woodworking_Height = Height
			
			info = translate("magicManager", "Width means the second size of the panel.")
			panel.addProperty("App::PropertyLength", "Woodworking_Width", "Woodworking", info)
			panel.Woodworking_Width = Width
			
			info = translate("magicManager", "Length means thickness.")
			panel.addProperty("App::PropertyLength", "Woodworking_Length", "Woodworking", info)
			panel.Woodworking_Length = Length

			FreeCAD.ActiveDocument.recompute()
			
			if gObserver != "":
				self.setCurveObserverOFF()
			
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
		def setModeType(self, selectedText):
			
			selectedIndex = getMenuIndex1[selectedText]
			self.gModeType = selectedIndex
	
			# first hide all
			self.oSimpleInfo1.hide()
			self.oSimpleInfo2.hide()
			self.oSimpleInfoB1.hide()
			self.groupSimple2.hide()
			self.groupVertices.hide()
			self.groupSketch.hide()
			self.groupCurve.hide()
			self.oCreateButton.hide()
			
			# simple panel
			if self.gModeType == 0:
				self.oSimpleInfo1.show()
				self.oSimpleInfo2.show()
				self.oSimpleInfoB1.show()
				self.groupSimple2.show()
				self.oCreateButton.show()
			
			# panel from vertices
			if self.gModeType == 1:
				self.groupVertices.show()
				self.oCreateButton.show()
			
			# sketch from vertices
			if self.gModeType == 2:
				self.groupSketch.show()
				self.oCreateButton.show()

			# panel along curve
			if self.gModeType == 3:
				self.groupCurve.show()
				self.oCreateButton.show()
		
		# ############################################################################
		def simpleRefresh(self):
			
			try:
				try:
					FreeCAD.ActiveDocument.removeObject(str(self.gPanel.Name))
				except:
					skip = 1
					
				self.setSelection()
				
				if self.gFace1 == "":

					self.gSimpleType = ""
					self.oSimpleInfo1.setText(self.gSimpleInfo1)
					self.oSimpleInfo2.setText(self.gSimpleInfo2)

					return

				if self.gFace2 == "":

					self.gSimpleType = "Face"
					
					index = MagicPanels.getFaceIndex(self.gSelection1, self.gFace1)
					info = str(self.gSelection1.Label) + ", " + "Face" + str(index)
					
					self.oSimpleInfo1.setText(info)
					self.oSimpleInfo2.setText("")
					
					self.gPanelArr = [ "XY", "YX", "XZ", "ZX", "YZ", "ZY" ]
					self.gPanelIndex = 5
					
				else:
					self.gSimpleType = "Between"
					index1 = MagicPanels.getFaceIndex(self.gSelection1, self.gFace1)
					index2 = MagicPanels.getFaceIndex(self.gSelection2, self.gFace2)
					
					info = ""
					info += str(self.gSelection1.Label)
					info += ", " + "Face" + str(index1)
					self.oSimpleInfo1.setText(info)
					
					info = ""
					info += str(self.gSelection2.Label)
					info += ", " + "Face" + str(index2)
					self.oSimpleInfo2.setText(info)
					
					if self.gFace1Plane == "YZ":
						self.gPanelArr = [ "XY", "XZ" ]
					if self.gFace1Plane == "XZ":
						self.gPanelArr = [ "XY", "YZ" ]
					if self.gFace1Plane == "XY":
						self.gPanelArr = [ "XZ", "YZ" ]
					
					self.gPanelIndex = 1

				# init panel
				self.setNextPanel()

			except:
				self.oSimpleInfo1.setText(self.gSimpleInfo1)
				self.oSimpleInfo2.setText(self.gSimpleInfo2)

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
		def setVerticesObserverON(self):
			
			global gObserver, gVertices, gVerticesInfo, gGUI
			
			if gObserver == "":
				
				self.resetGUIGlobals()
				gVertices = []
				gVerticesInfo = []
				gGUI = self
				gObserver = SelectionObserver()
				FreeCADGui.Selection.addObserver(gObserver)
				self.oVerticesInfo.setPlainText(self.gVerticesObserverON)
		
		def setVerticesObserverOFF(self):
			
			global gObserver, gVertices, gVerticesInfo
			
			if gObserver != "":
			
				self.resetGUIGlobals()
				FreeCADGui.Selection.removeObserver(gObserver)
				gObserver = ""
				gVertices = []
				gVerticesInfo = []
				self.oVerticesInfo.setPlainText(self.gVerticesObserverOFF)
		
		def removeVerticesVertex(self):
			
			global gVertices, gVerticesInfo
			
			if len(gVerticesInfo) > 0:
				gVertices.pop()
				gVerticesInfo.pop()
				gGUI.refreshInfo()
		
		# ############################################################################
		def setSketchObserverON(self):
			
			global gObserver, gSketch, gSketchInfo, gGUI
			
			if gObserver == "":
				
				self.resetGUIGlobals()
				gSketch = []
				gSketchInfo = []
				gGUI = self
				gObserver = SelectionObserver()
				FreeCADGui.Selection.addObserver(gObserver)
				self.oSketchInfo.setPlainText(self.gSketchObserverON)
		
		def setSketchObserverOFF(self):
			
			global gObserver, gSketch, gSketchInfo
			
			if gObserver != "":
			
				self.resetGUIGlobals()
				FreeCADGui.Selection.removeObserver(gObserver)
				gObserver = ""
				gSketch = []
				gSketchInfo = []
				self.oSketchInfo.setPlainText(self.gSketchObserverOFF)
		
		def removeSketchVertex(self):
			
			global gSketch, gSketchInfo
			
			if len(gSketchInfo) > 0:
				gSketch.pop()
				gSketchInfo.pop()
				gGUI.refreshInfo()
		
		# ############################################################################
		def setCurveObserverON(self):
			
			global gObserver, gCurve, gCurveInfo, gGUI
			
			if gObserver == "":
				
				self.resetGUIGlobals()
				gCurve = []
				gCurveInfo = []
				gGUI = self
				gObserver = SelectionObserver()
				FreeCADGui.Selection.addObserver(gObserver)
				self.oCurveInfo.setPlainText(self.gCurveObserverON)
		
		def setCurveObserverOFF(self):
			
			global gObserver, gCurve, gCurveInfo
			
			if gObserver != "":
			
				self.resetGUIGlobals()
				FreeCADGui.Selection.removeObserver(gObserver)
				gObserver = ""
				gCurve = []
				gCurveInfo = []
				self.oCurveInfo.setPlainText(self.gCurveObserverOFF)
		
		def removeCurveVertex(self):
			
			global gCurve, gCurveInfo
			
			if len(gCurveInfo) > 0:
				gCurve.pop()
				gCurveInfo.pop()
				gGUI.refreshInfo()
		
		# ############################################################################
		def createPanel(self):

			if self.gModeType == 0:
				self.setPanel()
			
			if self.gModeType == 1:
				self.setPanelFromVertices()
			
			if self.gModeType == 2:
				self.setSketchFromVertices()
			
			if self.gModeType == 3:
				self.setPanelAlongCurve()
		
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
