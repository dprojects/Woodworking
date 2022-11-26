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
				gGUI.shapeLE1.setText(str(round(gStep, MagicPanels.gRoundPrecision)))
			
			ves = MagicPanels.touchTypo(o.Shape)
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
		gAnchorIndex = 1

		gSizeArr = []
		gSizeIndex = 0
		
		gOffsetTypes = []
		gOffsetIndex = 0
		
		gSelection = ""
		gObj = ""
		gObjThick = 0
		gObjShort = 0
		gObjLong = 0

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
			toolSH = 470
			
			# active screen size - FreeCAD main window
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = int( gSW - toolSW )
			gPH = int( gSH - toolSH )

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicManager', 'magicManager'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options
			# ############################################################################
			
			spaceInfoScreen = ""
			spaceInfoScreen += "                                               "
			spaceInfoScreen += "                                               "
			spaceInfoScreen += "                                               "
			
			col1 = 10
			col2 = 80
			col3 = 140
			col4 = 200
			
			row = 30
			
			# screen
			self.oModeL = QtGui.QLabel(spaceInfoScreen, self)
			self.oModeL.move(col1, 10)

			# button - refresh
			self.oModeB1 = QtGui.QPushButton(translate('magicManager', 'refresh selection'), self)
			self.oModeB1.clicked.connect(self.setMode)
			self.oModeB1.setFixedWidth(toolSW-20)
			self.oModeB1.setFixedHeight(40)
			self.oModeB1.move(col1, row)

			# ############################################################################
			# options - panel
			# ############################################################################

			row += 50

			# label
			self.spL = QtGui.QLabel(translate('magicManager', 'Plane:'), self)
			self.spL.move(col1, row+3)

			# button - previous
			self.spBP = QtGui.QPushButton("<", self)
			self.spBP.clicked.connect(self.setPreviousPanel)
			self.spBP.setFixedWidth(50)
			self.spBP.move(col2, row)
			self.spBP.setAutoRepeat(True)

			# info screen
			self.spIS = QtGui.QLabel(spaceInfoScreen, self)
			self.spIS.move(col3, row+3)

			# button - next
			self.spBN = QtGui.QPushButton(">", self)
			self.spBN.clicked.connect(self.setNextPanel)
			self.spBN.setFixedWidth(50)
			self.spBN.move(col4, row)
			self.spBN.setAutoRepeat(True)

			# ############################################################################
			# options - anchor
			# ############################################################################
			
			row += 30

			# label
			self.saL = QtGui.QLabel(translate('magicManager', 'Anchor:'), self)
			self.saL.move(col1, row+3)

			# button - previous
			self.saBP = QtGui.QPushButton("<", self)
			self.saBP.clicked.connect(self.setPreviousAnchor)
			self.saBP.setFixedWidth(50)
			self.saBP.move(col2, row)
			self.saBP.setAutoRepeat(True)

			# info screen
			self.sainfo = QtGui.QLabel(spaceInfoScreen, self)
			self.sainfo.move(col3, row+3)

			# button - next
			self.saBN = QtGui.QPushButton(">", self)
			self.saBN.clicked.connect(self.setNextAnchor)
			self.saBN.setFixedWidth(50)
			self.saBN.move(col4, row)
			self.saBN.setAutoRepeat(True)

			# ############################################################################
			# options - 3rd size for the panel
			# ############################################################################
			
			row += 30

			# label
			self.ssL = QtGui.QLabel(translate('magicManager', 'Size:'), self)
			self.ssL.move(col1, row+3)

			# button - previous
			self.ssBP = QtGui.QPushButton("<", self)
			self.ssBP.clicked.connect(self.setPreviousSize)
			self.ssBP.setFixedWidth(50)
			self.ssBP.move(col2, row)
			self.ssBP.setAutoRepeat(True)

			# info screen
			self.ssIS = QtGui.QLabel(spaceInfoScreen, self)
			self.ssIS.move(col3, row+3)

			# button - next
			self.ssBN = QtGui.QPushButton(">", self)
			self.ssBN.clicked.connect(self.setNextSize)
			self.ssBN.setFixedWidth(50)
			self.ssBN.move(col4, row)
			self.ssBN.setAutoRepeat(True)

			# ############################################################################
			# options - offset
			# ############################################################################
			
			row += 30

			# label
			self.soL = QtGui.QLabel(translate('magicManager', 'Offset:'), self)
			self.soL.move(col1, row+3)

			# button - previous
			self.soBP = QtGui.QPushButton("<", self)
			self.soBP.clicked.connect(self.setPreviousOffset)
			self.soBP.setFixedWidth(50)
			self.soBP.move(col2, row)
			self.soBP.setAutoRepeat(True)

			# info screen
			self.soIS = QtGui.QLabel(spaceInfoScreen, self)
			self.soIS.move(col3, row+3)

			# button - next
			self.soBN = QtGui.QPushButton(">", self)
			self.soBN.clicked.connect(self.setNextOffset)
			self.soBN.setFixedWidth(50)
			self.soBN.move(col4, row)
			self.soBN.setAutoRepeat(True)

			# ############################################################################
			# options - vertices reader
			# ############################################################################

			row += 50
			
			# info screen
			self.shapeIS = QtGui.QTextEdit(self)
			self.shapeIS.setMinimumSize(toolSW-20, 120)
			self.shapeIS.setMaximumSize(toolSW-20, 120)
			self.shapeIS.move(10, row)
			self.shapeIS.setPlainText(self.gInfoObserverOFF)
			
			row += 120
			
			# button
			w1 = (toolSW-20-5-5) / 4
			self.shapeB1 = QtGui.QPushButton(translate('magicManager', 'ON'), self)
			self.shapeB1.clicked.connect(self.observerON)
			self.shapeB1.setFixedWidth(w1)
			self.shapeB1.setFixedHeight(40)
			self.shapeB1.move(10, row)

			# button
			self.shapeB2 = QtGui.QPushButton(translate('magicManager', 'OFF'), self)
			self.shapeB2.clicked.connect(self.observerOFF)
			self.shapeB2.setFixedWidth(w1)
			self.shapeB2.setFixedHeight(40)
			self.shapeB2.move(10+w1+5, row)
			
			# button
			self.shapeB3 = QtGui.QPushButton(translate('magicManager', 'remove last'), self)
			self.shapeB3.clicked.connect(self.removeLastVertex)
			w2 = 2 * w1
			self.shapeB3.setFixedWidth(w2)
			self.shapeB3.setFixedHeight(40)
			self.shapeB3.move(10+w1+5+w1+5, row)

			row += 50
			
			# screen
			self.shapeLEL1 = QtGui.QLabel(translate('magicManager', 'New object thickness:'), self)
			self.shapeLEL1.move(10, row+3)
			
			# text input
			self.shapeLE1 = QtGui.QLineEdit(self)
			self.shapeLE1.setText(str(gStep))
			self.shapeLE1.setFixedWidth(w1)
			self.shapeLE1.move(10+w1+5+w1+5+w1, row)

			row += 30
			
			# button
			self.shapeB4 = QtGui.QPushButton(translate('magicManager', 'create panel'), self)
			self.shapeB4.clicked.connect(self.createPanel)
			self.shapeB4.setFixedWidth(toolSW-20)
			self.shapeB4.setFixedHeight(40)
			self.shapeB4.move(10, row)
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()

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
			
			self.gSelection = ""
			self.gObj = ""
			self.gObjThick = 0
			self.gObjShort = 0
			self.gObjLong = 0
		
			self.gFace1 = ""
			self.gFace2 = ""
			
			gFace1Plane = ""
			gFace2Plane = ""
			
			self.gAnchorArr = []
			self.gAnchorIndex = 1
			
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
			[ L, W, H ] = MagicPanels.sizesToCubePanel(self.gObj, iType)

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

			# check if panel is valid
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

			# create panel
			self.gPanel = FreeCAD.ActiveDocument.addObject("Part::Box", "panelFace"+iType)
			self.gPanel.Length, self.gPanel.Width, self.gPanel.Height = L, W, H

			# add settings to panel
			self.gPanel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
			self.gPanel.ViewObject.ShapeColor = (0.0, 0.0, 0.0, 0.0)
			self.gPanel.ViewObject.Transparency = 83
			FreeCAD.ActiveDocument.recompute()

		def projectPanelBetween(self, iType):

			# get settings
			size = self.gSizeArr[self.gSizeIndex]
			offset = self.gOffsetTypes[self.gOffsetIndex]
			anchor = self.gAnchorArr[self.gAnchorIndex]
			facesDistance = MagicPanels.getDistanceBetweenFaces(self.gFace1, self.gFace2)
			x, y, z = anchor[0], anchor[1], anchor[2]
			L, W, H = 0, 0, 0

			# set panel sizes
			
			# set panel sizes along X
			if self.gFace1Plane == "YZ":

				if iType == "XY":
					L = facesDistance
					W = size
					H = self.gObjThick

				if iType ==	"XZ":
					L = facesDistance
					W = self.gObjThick
					H = size

			# set panel sizes along Y
			if self.gFace1Plane == "XZ":

				if iType == "XY":
					L = size
					W = facesDistance
					H = self.gObjThick

				if iType == "YZ":
					L = self.gObjThick
					W = facesDistance
					H = size

			# set panel sizes along Z
			if self.gFace1Plane == "XY":

				if iType ==	"XZ":
					L = size
					W = self.gObjThick
					H = facesDistance

				if iType == "YZ":
					L = self.gObjThick
					W = size
					H = facesDistance

			# check if panel is valid
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

			# create panel
			self.gPanel = FreeCAD.ActiveDocument.addObject("Part::Box", "panelBetween"+iType)
			self.gPanel.Length, self.gPanel.Width, self.gPanel.Height = L, W, H

			# add settings to panel
			self.gPanel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
			self.gPanel.ViewObject.ShapeColor = (0.0, 0.0, 0.0, 0.0)
			self.gPanel.ViewObject.Transparency = 83
			FreeCAD.ActiveDocument.recompute()

		def previewPanel(self):

			try:
				FreeCAD.activeDocument().removeObject(str(self.gPanel.Name))
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

		# ############################################################################
		def setMode(self):
			
			try:
				FreeCAD.activeDocument().removeObject(str(self.gPanel.Name))
			except:
				skip = 1
				
			self.setSelection()
			
			if self.gFace1 == "":

				self.gMode = ""
				self.oModeL.setText(translate('magicManager', 'select 1 or 2 faces'))

				return

			if self.gFace2 == "":

				self.gMode = "Face"
				self.oModeL.setText(translate('magicManager', 'Selection: 1 face'))
				
				self.gPanelArr = [ "XY", "YX", "XZ", "ZX", "YZ", "ZY" ]
				self.gPanelIndex = 5
				
			else:
				self.gMode = "Between"
				self.oModeL.setText(translate('magicManager', 'Selection: 2 faces'))
				
				if self.gFace1Plane == "YZ":
					self.gPanelArr = [ "XY", "XZ" ]
				if self.gFace1Plane == "XZ":
					self.gPanelArr = [ "XY", "YZ" ]
				if self.gFace1Plane == "XY":
					self.gPanelArr = [ "XZ", "YZ" ]
				
				self.gPanelIndex = 1

			# init panel
			self.setNextPanel()
		
		def setSelection(self):
			
			self.resetGUIGlobals()
			
			try:
				self.gObj = MagicPanels.getReference()
				self.gSelection = FreeCADGui.Selection.getSelection()[0]
			except:
				skip = 1
				
			try:
				self.gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gFace1Plane = MagicPanels.getFacePlane(self.gFace1)
				
				sizes = MagicPanels.getSizes(self.gObj)
				sizes.sort()
				self.gObjThick = sizes[0]
				self.gObjShort = sizes[1]
				self.gObjLong = sizes[2]

				self.gAnchorArr = MagicPanels.getFaceVertices(self.gFace1, "all")
				[ a1, edges, a2, a3, a4 ] = MagicPanels.getFaceEdges(self.gSelection, self.gFace1)

				noRepeat = dict()
				for e in edges:
					noRepeat[str(e.Length)] = e.Length

				noRepeat[str(self.gObjThick)] = self.gObjThick
				noRepeat[str(self.gObjShort)] = self.gObjShort
				noRepeat[str(self.gObjLong)] = self.gObjLong
				
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
					MagicPanels.copyColors(self.gObj, self.gPanel)
				except:
					skip = 1

				self.gPanel.ViewObject.Transparency = 0
				self.gPanel = ""
		
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
			t = round(float(gGUI.shapeLE1.text()), MagicPanels.gRoundPrecision)
			pad.Length = FreeCAD.Units.Quantity(str(t))
			draftSketch.Visibility = False
			doc.recompute()
			
			# set color of last selected object
			try:
				MagicPanels.copyColors(gLastSelected, pad)
			except:
				skip = 1
			
			# turn off observer after operation
			if gObserver != "":
				self.observerOFF()
			
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
