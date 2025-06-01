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

		gObj = ""
		
		gNearSubObj = ""
		gNearSub = ""
		
		gResizeObj = ""
		gResizeVal = 0
		
		gStep = 1

		gMoveFlag = False
		gMoveAxis = ""
		gDest = 0

		gNoSelection1 = translate('magicResizer', 'select edge to resize')
		gNoSelection2 = translate('magicResizer', 'select face, edge or vertex')
		
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
			toolSW = 230
			toolSH = 250
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 0 + 300
			gPH = int( gSH - toolSH ) - 50

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicResizer', 'magicResizer'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			self.s1S = QtGui.QLabel("", self)
			self.s1S.setFixedWidth(toolSW-20)
			self.s2S = QtGui.QLabel("", self)
			self.s2S.setFixedWidth(toolSW-20)
			
			# button
			self.s1B1 = QtGui.QPushButton(translate('magicResizer', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(toolSW-20)
			self.s1B1.setFixedHeight(40)
			
			# ############################################################################
			# options - step
			# ############################################################################
			
			# label
			self.oStepL = QtGui.QLabel(translate('magicResizer', 'Resize step:'), self)
			
			# text input
			self.oStepE = QtGui.QLineEdit(self)
			self.oStepE.setText(MagicPanels.unit2gui(self.gStep))
			self.oStepE.setFixedWidth((toolSW/2)-15)
			
			# ############################################################################
			# options - resize buttons
			# ############################################################################

			# button
			self.o1B1 = QtGui.QPushButton(translate('magicResizer', 'resize -'), self)
			self.o1B1.clicked.connect(self.setM)
			self.o1B1.setFixedWidth((toolSW/2)-15)
			self.o1B1.setFixedHeight(40)
			self.o1B1.setAutoRepeat(True)
			
			# button
			self.o1B2 = QtGui.QPushButton(translate('magicResizer', 'resize +'), self)
			self.o1B2.clicked.connect(self.setP)
			self.o1B2.setFixedWidth((toolSW/2)-15)
			self.o1B2.setFixedHeight(40)
			self.o1B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - resize to face button
			# ############################################################################
			
			# button
			self.s2B1 = QtGui.QPushButton(translate('magicResizer', 'resize to nearest'), self)
			self.s2B1.clicked.connect(self.resizeToFace)
			self.s2B1.setFixedWidth(toolSW-20)
			self.s2B1.setFixedHeight(40)
			
			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.row1 = QtGui.QHBoxLayout()
			self.row1.setAlignment(QtGui.Qt.AlignLeft)
			self.row1.addWidget(self.s1S)
			
			self.row2 = QtGui.QHBoxLayout()
			self.row2.setAlignment(QtGui.Qt.AlignLeft)
			self.row2.addWidget(self.s2S)
			
			self.row3 = QtGui.QHBoxLayout()
			self.row3.addWidget(self.s1B1)
			
			self.row4 = QtGui.QHBoxLayout()
			self.row4.addWidget(self.oStepL)
			self.row4.addStretch()
			self.row4.addWidget(self.oStepE)
			
			self.row5 = QtGui.QHBoxLayout()
			self.row5.addWidget(self.o1B1)
			self.row5.addStretch()
			self.row5.addWidget(self.o1B2)
			
			self.row6 = QtGui.QHBoxLayout()
			self.row6.addWidget(self.s2B1)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			
			self.layout.addLayout(self.row1)
			self.layout.addLayout(self.row2)
			self.layout.addLayout(self.row3)
			self.layout.addStretch()
			self.layout.addLayout(self.row4)
			self.layout.addLayout(self.row5)
			self.layout.addStretch()
			self.layout.addLayout(self.row6)
			
			self.setLayout(self.layout)
			
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
		
		def resetGlobals(self):
			
			self.gObj = ""
			self.gNearSubObj = ""
			self.gNearSub = ""
			self.gResizeObj = ""
			self.gResizeVal = 0
			self.gStep = 1
			self.gMoveFlag = False
			self.gMoveAxis = ""
			self.gDest = 0
		
		# ############################################################################
		def resetScreen(self):
			
			self.s1S.setText(self.gNoSelection1)
			self.s2S.setText(self.gNoSelection2)

		# ############################################################################
		def setEdgeSize(self):
			
			self.gResizeObj = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
			
			if self.gResizeObj.ShapeType == "Edge":
				if self.gResizeObj.Curve.isDerivedFrom("Part::GeomLine"):
					self.gResizeVal = self.gResizeObj.Length
					
			info = MagicPanels.unit2gui(self.gResizeVal) + " | " + str(self.gObj.Label)
			self.s1S.setText(info)

		# ############################################################################
		def setSize(self, iType):
			
			self.setEdgeSize()
			
			if self.gObj.isDerivedFrom("Part::Box"):
				
				if iType == "+":
					
					if MagicPanels.equal(self.gObj.Width.Value, self.gResizeVal):
						self.gObj.Width = self.gObj.Width.Value + self.gStep
					
					if MagicPanels.equal(self.gObj.Height.Value, self.gResizeVal):
						self.gObj.Height = self.gObj.Height.Value + self.gStep
						
					if MagicPanels.equal(self.gObj.Length.Value, self.gResizeVal):
						self.gObj.Length = self.gObj.Length.Value + self.gStep

				if iType == "-":
					
					if MagicPanels.equal(self.gObj.Width.Value, self.gResizeVal):
						if self.gObj.Width.Value - self.gStep > 0:
							self.gObj.Width = self.gObj.Width.Value - self.gStep
					
					if MagicPanels.equal(self.gObj.Height.Value, self.gResizeVal):
						if self.gObj.Height.Value - self.gStep > 0:
							self.gObj.Height = self.gObj.Height.Value - self.gStep
						
					if MagicPanels.equal(self.gObj.Length.Value, self.gResizeVal):
						if self.gObj.Length.Value - self.gStep > 0:
							self.gObj.Length = self.gObj.Length.Value - self.gStep

			if self.gObj.isDerivedFrom("PartDesign::Pad"):

				if iType == "+":
					
					if MagicPanels.equal(self.gObj.Length.Value, self.gResizeVal):
						self.gObj.Length = self.gObj.Length.Value + self.gStep
						
					i = 0
					sketch = self.gObj.Profile[0]
					for c in sketch.Constraints:

						if MagicPanels.equal(c.Value, self.gResizeVal):
							v = c.Value + self.gStep
							sketch.setDatum(i, FreeCAD.Units.Quantity(v))
						
						i = i + 1
			
				if iType == "-":
					
					if MagicPanels.equal(self.gObj.Length.Value, self.gResizeVal):
						if self.gObj.Length.Value - self.gStep > 0:
							self.gObj.Length = self.gObj.Length.Value - self.gStep
						
					i = 0
					sketch = self.gObj.Profile[0]
					for c in sketch.Constraints:

						if MagicPanels.equal(c.Value, self.gResizeVal):
							v = c.Value - self.gStep
							if v > 0:
								sketch.setDatum(i, FreeCAD.Units.Quantity(v))
						
						i = i + 1

			# move object if the face is before 0 vertex
			if self.gMoveFlag == True:
				
				[ x, y, z, r ] = MagicPanels.getPlacement(self.gObj)
				
				if self.gMoveAxis == "X":
					x = self.gDest
				
				if self.gMoveAxis == "Y":
					y = self.gDest
					
				if self.gMoveAxis == "Z":
					z = self.gDest
					
				MagicPanels.setPlacement(self.gObj, x, y, z, r)
				self.gMoveFlag = False

			FreeCAD.ActiveDocument.recompute()
			self.setEdgeSize()
			
		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		def getNearSub(self):
			
			try:

				self.gNearSubObj = FreeCADGui.Selection.getSelection()[1]
				self.gNearSub = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]

				if self.gNearSub.ShapeType == "Face":
					ves = MagicPanels.getFaceVertices(self.gNearSub)
					ves = MagicPanels.getVerticesPosition(ves, self.gNearSubObj)
					v = ves[0]

				if self.gNearSub.ShapeType == "Edge":
					ves = [ self.gNearSub.CenterOfMass ]
					ves = MagicPanels.getVerticesPosition(ves, self.gNearSubObj)
					v = [ ves[0].x, ves[0].y, ves[0].z ]

				if self.gNearSub.ShapeType == "Vertex":
					ves = MagicPanels.touchTypo(self.gNearSub)
					ves = MagicPanels.getVerticesPosition(ves, self.gNearSubObj)
					v = [ ves[0].X, ves[0].Y, ves[0].Z ]

				[ edgeV1, edgeV2 ] = MagicPanels.getEdgeVertices(self.gResizeObj)
				plane = MagicPanels.getEdgePlane(self.gNearSubObj, self.gResizeObj)

				if plane == "X":
					self.gDest = v[0]
					vStart1 = edgeV1[0]
					vStart2 = edgeV2[0]
					self.gMoveAxis = "X"

				if plane == "Y":
					self.gDest = v[1]
					vStart1 = edgeV1[1]
					vStart2 = edgeV2[1]
					self.gMoveAxis = "Y"

				if plane == "Z":
					self.gDest = v[2]
					vStart1 = edgeV1[2]
					vStart2 = edgeV2[2]
					self.gMoveAxis = "Z"
					
				road1 = MagicPanels.getVertexAxisCross(self.gDest, vStart1)
				road2 = MagicPanels.getVertexAxisCross(self.gDest, vStart2)

				if road1 < road2:
					self.gStep = road1
				else:
					self.gStep = road2
				
				self.oStepE.setText(MagicPanels.unit2gui(self.gStep))

				info = MagicPanels.unit2gui(self.gStep) + " | " + self.gNearSubObj.Label
				self.s2S.setText(info)
				
				# check if movement is needed
				
				if self.gDest < vStart1 and self.gDest < vStart2:
					self.gMoveFlag = True

			except:

				self.s2S.setText(self.gNoSelection2)
				return -1


		# ############################################################################
		def getSelected(self):

			try:

				self.resetGlobals()
				self.resetScreen()
				
				selection = FreeCADGui.Selection.getSelection()[0]
				self.gObj = MagicPanels.getReference(selection)

				sizes = []
				sizes = MagicPanels.getSizesFromVertices(self.gObj)
				sizes.sort()
				self.gStep = sizes[0]
				self.oStepE.setText(MagicPanels.unit2gui(self.gStep))

				self.setEdgeSize()
				self.getNearSub()
				
				if self.gResizeVal == 0:
					raise
				
			except:

				self.s1S.setText(self.gNoSelection1)
				return -1


		# ############################################################################
		def setM(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oStepE.text())
				self.setSize("-")
			except:
				self.resetScreen()
			
		def setP(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oStepE.text())
				self.setSize("+")
			except:
				self.resetScreen()
		
		def resizeToFace(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oStepE.text())
				self.setSize("+")
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
