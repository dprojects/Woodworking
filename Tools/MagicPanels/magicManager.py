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

gObserver = ""
gVertices = []
gVerticesInfo = []
gStep = 1


# ###################################################################################################################
#
# Observer class - irregular shapes, non-rectangle
#
# ###################################################################################################################


class SelectionObserver:
	
	def addSelection(self, doc, obj, sub, pos):
		
		global gVertices, gStep, gVerticesInfo
		
		if sub.find("Edge") != -1 or sub.find("Face") != -1:
			
			vpos = FreeCAD.Vector(pos)
			o = FreeCAD.ActiveDocument.getObject(obj)
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
		gPanelTypes = []
		gPanelIndex = 0
		
		gEdgeTypes = []
		gEdgeIndex = 0
		
		gVertexTypes = []
		gVertexIndex = 0
		
		gObj = ""
		gFace1 = ""
		gFace2 = ""
		gFace3 = ""
		gColor = ""
		
		gInfoObserverOFF = translate('magicManager', 'Reading vertices: OFF')
		gInfoObserverOFF += "\n\n"
		gInfoObserverOFF += translate('magicManager', 'To create panel with non-rectangle shape from vertices, click "ON" button to start reading vertices with selection order.')
		
		gInfoObserverON = translate('magicManager', 'Reading vertices: ON')
		gInfoObserverON += "\n\n"
		gInfoObserverON += translate('magicManager', 'Please select vertices in correct order to create shape.')

		
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
			toolSW = 220
			toolSH = 480
			
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
			
			row = 30
			
			# screen
			self.oModeL = QtGui.QLabel("                                          ", self)
			self.oModeL.move(10, 10)

			# button - refresh
			self.oModeB1 = QtGui.QPushButton(translate('magicManager', 'refresh selection'), self)
			self.oModeB1.clicked.connect(self.setMode)
			self.oModeB1.setFixedWidth(toolSW-20)
			self.oModeB1.move(10, row)

			# ############################################################################
			# options - panel
			# ############################################################################

			row += 40

			# label
			self.spL = QtGui.QLabel(translate('magicManager', 'Select panel:'), self)
			self.spL.move(10, row+3)

			# button - previous
			self.spBP = QtGui.QPushButton("<", self)
			self.spBP.clicked.connect(self.setPreviousPanel)
			self.spBP.setFixedWidth(50)
			self.spBP.move(toolSW-120, row)
			self.spBP.setAutoRepeat(True)

			# button - next
			self.spBN = QtGui.QPushButton(">", self)
			self.spBN.clicked.connect(self.setNextPanel)
			self.spBN.setFixedWidth(50)
			self.spBN.move(toolSW-60, row)
			self.spBN.setAutoRepeat(True)

			# ############################################################################
			# options - edge
			# ############################################################################

			row += 30

			# label
			self.seL = QtGui.QLabel(translate('magicManager', 'Select edge:'), self)
			self.seL.move(10, row+3)

			# button - previous
			self.seBP = QtGui.QPushButton("<", self)
			self.seBP.clicked.connect(self.setPreviousEdge)
			self.seBP.setFixedWidth(50)
			self.seBP.move(toolSW-120, row)
			self.seBP.setAutoRepeat(True)

			# button - next
			self.seBN = QtGui.QPushButton(">", self)
			self.seBN.clicked.connect(self.setNextEdge)
			self.seBN.setFixedWidth(50)
			self.seBN.move(toolSW-60, row)
			self.seBN.setAutoRepeat(True)

			# ############################################################################
			# options - vertex
			# ############################################################################
			
			row += 30

			# label
			self.svL = QtGui.QLabel(translate('magicManager', 'Select vertex:'), self)
			self.svL.move(10, row+3)

			# button - previous
			self.svBP = QtGui.QPushButton("<", self)
			self.svBP.clicked.connect(self.setPreviousVertex)
			self.svBP.setFixedWidth(50)
			self.svBP.move(toolSW-120, row)
			self.svBP.setAutoRepeat(True)

			# button - next
			self.svBN = QtGui.QPushButton(">", self)
			self.svBN.clicked.connect(self.setNextVertex)
			self.svBN.setFixedWidth(50)
			self.svBN.move(toolSW-60, row)
			self.svBN.setAutoRepeat(True)

			# ############################################################################
			# options - apply
			# ############################################################################

			row += 30

			# button - apply
			self.oSetB = QtGui.QPushButton(translate('magicManager', 'apply panel to this position'), self)
			self.oSetB.clicked.connect(self.setPanel)
			self.oSetB.setFixedWidth(toolSW-20)
			self.oSetB.setFixedHeight(40)
			self.oSetB.move(10, row)

			
			# ############################################################################
			# options - vertices reader
			# ############################################################################

			row += 60
			
			# info screen
			self.shapeIS = QtGui.QTextEdit(self)
			self.shapeIS.setMinimumSize(toolSW-20, 120)
			self.shapeIS.setMaximumSize(toolSW-20, 120)
			self.shapeIS.move(10, row)
			self.shapeIS.setPlainText(self.gInfoObserverOFF)
			
			row += 120
			
			# button
			self.shapeB1 = QtGui.QPushButton(translate('magicManager', 'ON'), self)
			self.shapeB1.clicked.connect(self.observerON)
			self.shapeB1.setFixedWidth(50)
			self.shapeB1.setFixedHeight(40)
			self.shapeB1.move(10, row)

			# button
			self.shapeB2 = QtGui.QPushButton(translate('magicManager', 'OFF'), self)
			self.shapeB2.clicked.connect(self.observerOFF)
			self.shapeB2.setFixedWidth(50)
			self.shapeB2.setFixedHeight(40)
			self.shapeB2.move(65, row)
			
			# button
			self.shapeB3 = QtGui.QPushButton(translate('magicManager', 'remove last'), self)
			self.shapeB3.clicked.connect(self.removeLastVertex)
			self.shapeB3.setFixedWidth(90)
			self.shapeB3.setFixedHeight(40)
			self.shapeB3.move(120, row)

			row += 50
			
			# screen
			self.shapeLEL1 = QtGui.QLabel(translate('magicManager', 'New object thickness:'), self)
			self.shapeLEL1.move(10, row+3)
			
			# text input
			self.shapeLE1 = QtGui.QLineEdit(self)
			self.shapeLE1.setText(str(gStep))
			self.shapeLE1.setFixedWidth(60)
			self.shapeLE1.move(150, row)

			row += 30
			
			# button
			self.shapeB4 = QtGui.QPushButton(translate('magicManager', 'create panel from vertices'), self)
			self.shapeB4.clicked.connect(self.setPanelFromVertices)
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
		# actions - internal functions
		# ############################################################################

		# ############################################################################
		def resetGUIGlobals(self):
			
			self.gMode = ""

			self.gPanel = ""
			self.gPanelTypes = [ "XY", "YX", "XZ", "ZX", "YZ", "ZY" ]
			self.gPanelIndex = 5
			
			self.gObj = ""
			self.gFace1 = ""
			self.gFace2 = ""
			
			self.gEdgeTypes = [ 0, 1, 2, 3 ]
			self.gEdgeIndex = 0
		
			self.gVertexTypes = [ 0, 1 ]
			self.gVertexIndex = 1
		
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
		def projectPanelFace(self, iType):

			self.gPanel = FreeCAD.activeDocument().addObject("Part::Box", "panelFace"+iType)
			[ self.gPanel.Length, self.gPanel.Width, self.gPanel.Height ] = MagicPanels.sizesToCubePanel(self.gObj, iType)

			edge = self.gEdgeTypes[self.gEdgeIndex]
			vertex = self.gVertexTypes[self.gVertexIndex]
			[ x, y, z ] = MagicPanels.getVertex(self.gFace1, edge, vertex)

			self.gPanel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
			self.gPanel.ViewObject.ShapeColor = (0.0, 0.0, 0.0, 0.0)
			self.gPanel.ViewObject.Transparency = 83
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def projectPanelBetween(self, iType):

			[ x1, y1, z1 ] = MagicPanels.getVertex(self.gFace1, 0, 1)
			[ x2, y2, z2 ] = MagicPanels.getVertex(self.gFace2, 0, 1)

			x = abs(x2 - x1)
			y = abs(y2 - y1)
			z = abs(z2 - z1)

			self.gPanel = FreeCAD.activeDocument().addObject("Part::Box", "panelBetween"+iType)
			[ self.gPanel.Length, self.gPanel.Width, self.gPanel.Height ] = MagicPanels.sizesToCubePanel(self.gObj, iType)

			z1 = z1 + self.gObj.Height.Value - self.gPanel.Height.Value
			
			if x > 0:
				self.gPanel.Length = x
			
			if y > 0:
				self.gPanel.Width = y
				
			if z > 0:
				self.gPanel.Height = z

			self.gPanel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z1), FreeCAD.Rotation(0, 0, 0))
			self.gPanel.ViewObject.ShapeColor = (0.0, 0.0, 0.0, 0.0)
			self.gPanel.ViewObject.Transparency = 83
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def setSelection(self):
			
			self.resetGUIGlobals()
			
			try:
				self.gObj = MagicPanels.getReference()
			except:
				skip = 1
				
			try:
				self.gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
			except:
				skip = 1
			
			try:
				self.gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
			except:
				skip = 1

			FreeCADGui.Selection.clearSelection()
			
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
				
				self.seL.hide()
				self.seBP.hide()
				self.seBN.hide()
				
				self.svL.hide()
				self.svBP.hide()
				self.svBN.hide()
				
				return

			if self.gFace2 == "":

				self.gMode = "Face"
				self.oModeL.setText(translate('magicManager', 'Selection: 1 face'))
				
				self.seL.show()
				self.seBP.show()
				self.seBN.show()
				
				self.svL.show()
				self.svBP.show()
				self.svBN.show()
				
			else:
				self.gMode = "Between"
				self.oModeL.setText(translate('magicManager', 'Selection: 2 faces'))
				
				self.seL.hide()
				self.seBP.hide()
				self.seBN.hide()
				
				self.svL.hide()
				self.svBP.hide()
				self.svBN.hide()

			# init panel
			self.setNextPanel()
			
		
		# ############################################################################
		# actions - buttons functions
		# ############################################################################

		# ############################################################################
		def previewPanel(self):
			
			try:
				FreeCAD.activeDocument().removeObject(str(self.gPanel.Name))
			except:
				skip = 1

			if self.gMode == "Face":
				self.projectPanelFace(self.gPanelTypes[self.gPanelIndex])

			if self.gMode == "Between":
				self.projectPanelBetween(self.gPanelTypes[self.gPanelIndex])

		# ############################################################################
		def setPreviousPanel(self):
			if self.gPanelIndex == 0:
				self.gPanelIndex = 5
			else:
				self.gPanelIndex = self.gPanelIndex - 1
			self.previewPanel()
			
		def setNextPanel(self):
			if self.gPanelIndex == 5:
				self.gPanelIndex = 0
			else:
				self.gPanelIndex = self.gPanelIndex + 1
			self.previewPanel()
			
		# ############################################################################
		def setPreviousEdge(self):
			if self.gEdgeIndex == 0:
				self.gEdgeIndex = 3
			else:
				self.gEdgeIndex = self.gEdgeIndex - 1
			self.previewPanel()

		def setNextEdge(self):
			if self.gEdgeIndex == 3:
				self.gEdgeIndex = 0
			else:
				self.gEdgeIndex = self.gEdgeIndex + 1
			self.previewPanel()
			
		# ############################################################################
		def setPreviousVertex(self):
			if self.gVertexIndex == 0:
				self.gVertexIndex = 1
			else:
				self.gVertexIndex = 0
			self.previewPanel()
			
		def setNextVertex(self):
			if self.gVertexIndex == 0:
				self.gVertexIndex = 1
			else:
				self.gVertexIndex = 0
			self.previewPanel()

		# ############################################################################
		def setPanel(self):
			if self.gPanel != "":
				try:
					MagicPanels.copyColors(self.gObj, self.gPanel)
				except:
					skip = 1

				self.gPanel.ViewObject.Transparency = 0
				self.gPanel = ""
		
		# ############################################################################
		def removeLastVertex(self):
			
			global gVertices, gVerticesInfo
			
			if len(gVerticesInfo) > 0:
				gVertices.pop()
				gVerticesInfo.pop()
				gGUI.refreshVerticesInfo()
				
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
			
			# ser color of last selected object
			try:
				MagicPanels.copyColors(FreeCADGui.Selection.getSelection()[0], pad)
			except:
				skip = 1
			
			# turn off observer after operation
			if gObserver != "":
				self.observerOFF()
			
		
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
				FreeCAD.activeDocument().removeObject(str(form.gPanel.Name))
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
