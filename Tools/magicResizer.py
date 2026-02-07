import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals
		# ############################################################################

		toolSW = 300
		toolSH = 300

		gResizeObj = ""
		gResizeSub = ""
		gResizeSubIndex = 0
		gResizeVal = 0
		
		gNearSubObj = ""
		gNearSub = ""
		gNearSubIndex = 0
		gNearType = ""
		gDest = 0
		
		gStep = 1
		gMoveFlag = False
		gMoveAxis = ""

		gNoSelection1 = translate('magicResizer', 'select edge to resize')
		gNoSelection2 = translate('magicResizer', 'select face, edge or vertex as destination')
		
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
			self.setWindowTitle(translate('magicResizer', 'magicResizer'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			self.setMinimumSize(self.toolSW, self.toolSH)
			
			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			self.s1B = QtGui.QPushButton(translate('magicResizer', 'set'), self)
			self.s1B.clicked.connect(self.getResizeObject)
			self.s1B.setFixedWidth(50)
			
			# label
			self.s1S = QtGui.QLabel("", self)
			
			# button
			self.s2B = QtGui.QPushButton(translate('magicResizer', 'set'), self)
			self.s2B.clicked.connect(self.getNearSub)
			self.s2B.setFixedWidth(50)
		
			# label
			self.s2S = QtGui.QLabel("", self)
			
			# button
			self.sBR = QtGui.QPushButton(translate('magicResizer', 'refresh selection'), self)
			self.sBR.clicked.connect(self.getSelected)
			self.sBR.setFixedHeight(40)
			
			# ############################################################################
			# options - step
			# ############################################################################
			
			# label
			self.oStepL = QtGui.QLabel(translate('magicResizer', 'Resize step:'), self)
			
			# text input
			self.oStepE = QtGui.QLineEdit(self)
			self.oStepE.setText(MagicPanels.unit2gui(self.gStep))
			
			# ############################################################################
			# options - resize buttons
			# ############################################################################

			# button
			self.o1B1 = QtGui.QPushButton(translate('magicResizer', 'resize -'), self)
			self.o1B1.clicked.connect(self.setM)
			self.o1B1.setFixedHeight(40)
			self.o1B1.setAutoRepeat(True)
			
			# button
			self.o1B2 = QtGui.QPushButton(translate('magicResizer', 'resize +'), self)
			self.o1B2.clicked.connect(self.setP)
			self.o1B2.setFixedHeight(40)
			self.o1B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - resize to nearest
			# ############################################################################
			
			# button
			self.s2B1 = QtGui.QPushButton(translate('magicResizer', 'resize to nearest'), self)
			self.s2B1.clicked.connect(self.setNear)
			self.s2B1.setFixedHeight(40)
			
			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.row1 = QtGui.QHBoxLayout()
			self.row1.setAlignment(QtGui.Qt.AlignLeft)
			self.row1.addWidget(self.s1B)
			self.row1.addWidget(self.s1S)
			
			self.row2 = QtGui.QHBoxLayout()
			self.row2.setAlignment(QtGui.Qt.AlignLeft)
			self.row2.addWidget(self.s2B)
			self.row2.addWidget(self.s2S)
			
			self.row3 = QtGui.QHBoxLayout()
			self.row3.addWidget(self.sBR)
			
			self.row4 = QtGui.QHBoxLayout()
			self.row4.addWidget(self.oStepL)
			self.row4.addWidget(self.oStepE)
			
			self.row5 = QtGui.QHBoxLayout()
			self.row5.addWidget(self.o1B1)
			self.row5.addWidget(self.o1B2)
			
			self.layBody = QtGui.QVBoxLayout()
			self.layBody.addLayout(self.row4)
			self.layBody.addLayout(self.row5)
			self.groupBody = QtGui.QGroupBox(None, self)
			self.groupBody.setLayout(self.layBody)
			
			self.row6 = QtGui.QHBoxLayout()
			self.row6.addWidget(self.s2B1)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			
			self.layout.addLayout(self.row1)
			self.layout.addLayout(self.row2)
			self.layout.addLayout(self.row3)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody)
			self.layout.addStretch()
			self.layout.addLayout(self.row6)
			
			self.setLayout(self.layout)
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)

			# show window
			self.show()

			MagicPanels.adjustGUI(self, "left-offset")
			
			# init
			self.getSelected()
			
		# ############################################################################
		# functions
		# ############################################################################
		
		# ############################################################################
		def resetGlobals(self):
			
			self.gResizeObj = ""
			self.gResizeSub = ""
			self.gResizeSubIndex = 0
			self.gResizeVal = 0
			
			self.gNearSubObj = ""
			self.gNearSub = ""
			self.gNearSubIndex = 0
			self.gNearType = ""
			self.gDest = 0
			
			self.gStep = 1
			self.gMoveFlag = False
			self.gMoveAxis = ""
		
		# ############################################################################
		def resetScreen(self):
			
			self.s1S.setText(self.gNoSelection1)
			self.s2S.setText(self.gNoSelection2)

		# ############################################################################
		def setSize(self, iType):
			
			FreeCAD.ActiveDocument.openTransaction("magicResize.setSize"+str(iType))
			
			if self.gResizeObj.isDerivedFrom("Part::Box"):
				
				if iType == "+":
					
					if MagicPanels.equal(self.gResizeObj.Width.Value, self.gResizeVal):
						self.gResizeObj.Width = self.gResizeObj.Width.Value + self.gStep
					
					if MagicPanels.equal(self.gResizeObj.Height.Value, self.gResizeVal):
						self.gResizeObj.Height = self.gResizeObj.Height.Value + self.gStep
						
					if MagicPanels.equal(self.gResizeObj.Length.Value, self.gResizeVal):
						self.gResizeObj.Length = self.gResizeObj.Length.Value + self.gStep

				if iType == "-":
					
					if MagicPanels.equal(self.gResizeObj.Width.Value, self.gResizeVal):
						if self.gResizeObj.Width.Value - self.gStep > 0:
							self.gResizeObj.Width = self.gResizeObj.Width.Value - self.gStep
					
					if MagicPanels.equal(self.gResizeObj.Height.Value, self.gResizeVal):
						if self.gResizeObj.Height.Value - self.gStep > 0:
							self.gResizeObj.Height = self.gResizeObj.Height.Value - self.gStep
						
					if MagicPanels.equal(self.gResizeObj.Length.Value, self.gResizeVal):
						if self.gResizeObj.Length.Value - self.gStep > 0:
							self.gResizeObj.Length = self.gResizeObj.Length.Value - self.gStep

			if self.gResizeObj.isDerivedFrom("PartDesign::Pad"):

				if iType == "+":
					
					if MagicPanels.equal(self.gResizeObj.Length.Value, self.gResizeVal):
						self.gResizeObj.Length = self.gResizeObj.Length.Value + self.gStep
						
					i = 0
					sketch = self.gResizeObj.Profile[0]
					for c in sketch.Constraints:

						if MagicPanels.equal(c.Value, self.gResizeVal):
							v = c.Value + self.gStep
							sketch.setDatum(i, FreeCAD.Units.Quantity(v))
						
						i = i + 1
			
				if iType == "-":
					
					if MagicPanels.equal(self.gResizeObj.Length.Value, self.gResizeVal):
						if self.gResizeObj.Length.Value - self.gStep > 0:
							self.gResizeObj.Length = self.gResizeObj.Length.Value - self.gStep
						
					i = 0
					sketch = self.gResizeObj.Profile[0]
					for c in sketch.Constraints:

						if MagicPanels.equal(c.Value, self.gResizeVal):
							v = c.Value - self.gStep
							if v > 0:
								sketch.setDatum(i, FreeCAD.Units.Quantity(v))
						
						i = i + 1

			FreeCAD.ActiveDocument.recompute()
			FreeCAD.ActiveDocument.commitTransaction()
			
		# ############################################################################
		def setSizeToNear(self, iType):
			
			self.setSize(iType)
			
			# move object if the face is before 0 vertex
			if self.gMoveFlag == True:
				
				toMove = MagicPanels.getObjectToMove(self.gResizeObj)
				[ x, y, z ] = MagicPanels.getPosition(toMove, "global")
				
				if self.gMoveAxis == "X":
					x = self.gDest
				
				if self.gMoveAxis == "Y":
					y = self.gDest
					
				if self.gMoveAxis == "Z":
					z = self.gDest
					
				MagicPanels.setPosition(toMove, x, y, z, "global")
				self.gMoveFlag = False

			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def updateEdgeSize(self):
			
			if self.gResizeSub.ShapeType == "Edge":
				if self.gResizeSub.Curve.isDerivedFrom("Part::GeomLine"):
					self.gResizeVal = self.gResizeSub.Length
			
			info = ""
			info += MagicPanels.unit2gui(self.gResizeVal)
			info += " | "
			info += str(self.gResizeObj.Label)
			info += ", Edge"
			info += str(self.gResizeSubIndex)
			self.s1S.setText(info)

		# ############################################################################
		def getResizeObject(self):
			
			selection = FreeCADGui.Selection.getSelection()[0]
			self.gResizeObj = MagicPanels.getReference(selection)
			self.gResizeSub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
			self.gResizeSubIndex = MagicPanels.getEdgeIndex(self.gResizeObj, self.gResizeSub)
			self.updateEdgeSize()
			
		# ############################################################################
		def setEdgeSize(self):
			
			self.gResizeObj = FreeCAD.ActiveDocument.getObject(self.gResizeObj.Name)
			self.gResizeSub = self.gResizeObj.Shape.Edges[self.gResizeSubIndex-1]
			self.updateEdgeSize()
		
		# ############################################################################
		def getNearSub(self):
			
			selection = FreeCADGui.Selection.getSelection()
			if len(selection) == 2:
				self.gNearSubObj = FreeCADGui.Selection.getSelection()[1]
				self.gNearSub = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
			else:
				self.gNearSubObj = FreeCADGui.Selection.getSelection()[0]
				self.gNearSub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

			if self.gNearSub.ShapeType == "Face":
				ves = MagicPanels.getFaceVertices(self.gNearSub)
				ves = MagicPanels.getVerticesPosition(ves, self.gNearSubObj)
				v = ves[0]
				self.gNearSubIndex = MagicPanels.getFaceIndex(self.gNearSubObj, self.gNearSub)
				subType = "Face"
				
			if self.gNearSub.ShapeType == "Edge":
				ves = [ self.gNearSub.CenterOfMass ]
				ves = MagicPanels.getVerticesPosition(ves, self.gNearSubObj)
				v = [ ves[0].x, ves[0].y, ves[0].z ]
				self.gNearSubIndex = MagicPanels.getEdgeIndex(self.gNearSubObj, self.gNearSub)
				subType = "Edge"
				
			if self.gNearSub.ShapeType == "Vertex":
				ves = MagicPanels.touchTypo(self.gNearSub)
				ves = MagicPanels.getVerticesPosition(ves, self.gNearSubObj)
				v = [ ves[0].X, ves[0].Y, ves[0].Z ]
				self.gNearSubIndex = MagicPanels.getVertexIndex(self.gNearSubObj, self.gNearSub)
				subType = "Vertex"

			[ edgeV1, edgeV2 ] = MagicPanels.getEdgeVertices(self.gResizeSub)
			[ edgeV1, edgeV2 ] = MagicPanels.getVerticesPosition([ edgeV1, edgeV2 ], self.gResizeObj, "array")
			plane = MagicPanels.getEdgePlane(self.gResizeObj, self.gResizeSub)

			if plane == "X":
				self.gDest = v[0]
				self.gMoveAxis = "X"
				if edgeV1[0] < edgeV2[0]:
					vStart1 = edgeV1[0]
					vStart2 = edgeV2[0]
				else:
					vStart2 = edgeV1[0]
					vStart1 = edgeV2[0]

			if plane == "Y":
				self.gDest = v[1]
				self.gMoveAxis = "Y"
				if edgeV1[1] < edgeV2[1]:
					vStart1 = edgeV1[1]
					vStart2 = edgeV2[1]
				else:
					vStart2 = edgeV1[1]
					vStart1 = edgeV2[1]

			if plane == "Z":
				self.gDest = v[2]
				self.gMoveAxis = "Z"
				if edgeV1[2] < edgeV2[2]:
					vStart1 = edgeV1[2]
					vStart2 = edgeV2[2]
				else:
					vStart2 = edgeV1[2]
					vStart1 = edgeV2[2]
				
			road1 = MagicPanels.getVertexAxisCross(self.gDest, vStart1)
			road2 = MagicPanels.getVertexAxisCross(self.gDest, vStart2)

			# set resize to nearest type and move
			if self.gDest > vStart1 and self.gDest < vStart2:
				self.gNearType = "-"
			else:
				self.gNearType = "+"

			# set if object move is needed
			if road1 < road2:
				self.gMoveFlag = True
			else:
				self.gMoveFlag = False
				
			# set step and info at the end
			if road1 < road2:
				self.gStep = road1
			else:
				self.gStep = road2
			
			self.oStepE.setText(MagicPanels.unit2gui(self.gStep))

			info = ""
			info += MagicPanels.unit2gui(self.gStep)
			info += " | "
			info += self.gNearSubObj.Label
			info += ", " + subType
			info += str(self.gNearSubIndex)
			self.s2S.setText(info)

		# ############################################################################
		def getSelected(self):

			try:
				self.resetGlobals()
				self.resetScreen()
				
				selection = FreeCADGui.Selection.getSelection()[0]
				self.gResizeObj = MagicPanels.getReference(selection)

				sizes = []
				sizes = MagicPanels.getSizesFromVertices(self.gResizeObj)
				sizes.sort()
				self.gStep = sizes[0]
				self.oStepE.setText(MagicPanels.unit2gui(self.gStep))

				self.getResizeObject()
				self.getNearSub()
				
				if self.gResizeVal == 0:
					raise
				
			except:
				self.s1S.setText(self.gNoSelection1)

		# ############################################################################
		def setM(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oStepE.text())
				self.setSize("-")
				self.setEdgeSize()
			except:
				self.resetScreen()
			
		def setP(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oStepE.text())
				self.setSize("+")
				self.setEdgeSize()
			except:
				self.resetScreen()
		
		def setNear(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oStepE.text())
				self.setSizeToNear(self.gNearType)
				self.setEdgeSize()
			except:
				self.resetScreen()

	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
