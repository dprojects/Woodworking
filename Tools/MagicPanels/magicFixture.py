import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore
import Draft

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

		gBaseRef = ""
		gObjRef = ""
		
		gFaceRef = ""
		gFaceIndex = 0
		gFPlane = ""
		
		gEdgeRef = ""
		gEdgeArr = []
		gEdgeIndex = 0

		gRoAxisArr = []
		gRoAxis = ""
		
		gRoAnglesArr = []
		gRoAngles = ""
		
		gRoIndex = 0
		
		gStep = 10
		
		gLink = ""
		
		gFxSink = 0
		gFxOCorner = 0
		gFxOEdge = 0
		
		gNoSelection = translate('magicFixture', 'please select fixture and face for link')
		
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
			toolSW = 270
			toolSH = 450
			
			# active screen size (FreeCAD main window)
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
			self.setWindowTitle(translate('magicFixture', 'magicFixture'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			# set grid
			row = 0
			col1 = 100
			col2 = 155
			col3 = 210
			
			# screen
			info = ""
			info += "                                             "
			info += "                                             "
			info += "                                             "
			
			row += 10
			
			# info about base detailed object to link
			self.ob1S = QtGui.QLabel(info, self)
			self.ob1S.move(10, row)
			
			row += 20
			
			# info about selected face to place the link
			self.ob2S = QtGui.QLabel(info, self)
			self.ob2S.move(10, row)
			
			row += 20
			
			# selection status
			self.ob3S = QtGui.QLabel(info, self)
			self.ob3S.move(10, row)
			
			row += 20
			
			# button
			self.s1B1 = QtGui.QPushButton(translate('magicFixture', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(toolSW-20)
			self.s1B1.move(10, row)

			# ############################################################################
			# options - select edge
			# ############################################################################

			row += 30

			# label
			self.s2L = QtGui.QLabel(translate('magicFixture', 'Edge:'), self)
			self.s2L.move(10, row+3)

			# button
			self.s2B1 = QtGui.QPushButton("<", self)
			self.s2B1.clicked.connect(self.setEdgeP)
			self.s2B1.setFixedWidth(50)
			self.s2B1.move(col1, row)
			self.s2B1.setAutoRepeat(True)
			
			# info screen
			self.s2IS = QtGui.QLabel("                                         ", self)
			self.s2IS.move(col2, row+3)
						
			# button
			self.s2B2 = QtGui.QPushButton(">", self)
			self.s2B2.clicked.connect(self.setEdgeN)
			self.s2B2.setFixedWidth(50)
			self.s2B2.move(col3, row)
			self.s2B2.setAutoRepeat(True)

			# ############################################################################
			# options - adjust rotation
			# ############################################################################

			row += 30
			
			# label
			self.s4L = QtGui.QLabel(translate('magicFixture', 'Rotation:'), self)
			self.s4L.move(10, row+3)

			# button
			self.s4B1 = QtGui.QPushButton("<", self)
			self.s4B1.clicked.connect(self.setRoAnglesP)
			self.s4B1.setFixedWidth(50)
			self.s4B1.move(col1, row)
			self.s4B1.setAutoRepeat(True)
			
			# info screen
			self.s4IS = QtGui.QLabel("                                         ", self)
			self.s4IS.move(col2, row+3)
			
			# button
			self.s4B2 = QtGui.QPushButton(">", self)
			self.s4B2.clicked.connect(self.setRoAnglesN)
			self.s4B2.setFixedWidth(50)
			self.s4B2.move(col3, row)
			self.s4B2.setAutoRepeat(True)

			# ############################################################################
			# options - offset from edge
			# ############################################################################

			row += 50
			
			# label
			self.oFxOEdgeL = QtGui.QLabel(translate('magicFixture', 'Edge offset:'), self)
			self.oFxOEdgeL.move(10, row+3)

			# button
			self.gFxOEdgeB1 = QtGui.QPushButton("-", self)
			self.gFxOEdgeB1.clicked.connect(self.setEdgeOffsetP)
			self.gFxOEdgeB1.setFixedWidth(50)
			self.gFxOEdgeB1.move(col1, row)
			self.gFxOEdgeB1.setAutoRepeat(True)

			# text input
			self.oFxOEdgeE = QtGui.QLineEdit(self)
			self.oFxOEdgeE.setText(str(self.gFxOEdge))
			self.oFxOEdgeE.setFixedWidth(50)
			self.oFxOEdgeE.move(col2, row)

			# button
			self.gFxOEdgeB2 = QtGui.QPushButton("+", self)
			self.gFxOEdgeB2.clicked.connect(self.setEdgeOffsetN)
			self.gFxOEdgeB2.setFixedWidth(50)
			self.gFxOEdgeB2.move(col3, row)
			self.gFxOEdgeB2.setAutoRepeat(True)

			# ############################################################################
			# options - offset from corner
			# ############################################################################

			row += 30
			
			# label
			self.oFxOCornerL = QtGui.QLabel(translate('magicFixture', 'Corner offset:'), self)
			self.oFxOCornerL.move(10, row+3)

			# button
			self.oFxOCornerB1 = QtGui.QPushButton("-", self)
			self.oFxOCornerB1.clicked.connect(self.setCornerOffsetP)
			self.oFxOCornerB1.setFixedWidth(50)
			self.oFxOCornerB1.move(col1, row)
			self.oFxOCornerB1.setAutoRepeat(True)

			# text input
			self.oFxOCornerE = QtGui.QLineEdit(self)
			self.oFxOCornerE.setText(str(self.gFxOCorner))
			self.oFxOCornerE.setFixedWidth(50)
			self.oFxOCornerE.move(col2, row)

			# button
			self.oFxOCornerB2 = QtGui.QPushButton("+", self)
			self.oFxOCornerB2.clicked.connect(self.setCornerOffsetN)
			self.oFxOCornerB2.setFixedWidth(50)
			self.oFxOCornerB2.move(col3, row)
			self.oFxOCornerB2.setAutoRepeat(True)

			# ############################################################################
			# options - sink
			# ############################################################################

			row += 30

			# label
			self.oFxSinkL = QtGui.QLabel(translate('magicFixture', 'Sink offset:'), self)
			self.oFxSinkL.move(10, row+3)

			# button
			self.oFxSinkB1 = QtGui.QPushButton("-", self)
			self.oFxSinkB1.clicked.connect(self.setSinkOffsetP)
			self.oFxSinkB1.setFixedWidth(50)
			self.oFxSinkB1.move(col1, row)
			self.oFxSinkB1.setAutoRepeat(True)
			
			# text input
			self.oFxSinkE = QtGui.QLineEdit(self)
			self.oFxSinkE.setText(str(self.gFxSink))
			self.oFxSinkE.setFixedWidth(50)
			self.oFxSinkE.move(col2, row)
			
			# button
			self.oFxSinkB2 = QtGui.QPushButton("+", self)
			self.oFxSinkB2.clicked.connect(self.setSinkOffsetN)
			self.oFxSinkB2.setFixedWidth(50)
			self.oFxSinkB2.move(col3, row)
			self.oFxSinkB2.setAutoRepeat(True)

			# ############################################################################
			# options - step
			# ############################################################################

			row += 30

			# label
			self.oFxStepL = QtGui.QLabel(translate('magicFixture', 'Step:'), self)
			self.oFxStepL.move(10, row+3)

			# text input
			self.oFxStepE = QtGui.QLineEdit(self)
			self.oFxStepE.setText(str(self.gStep))
			self.oFxStepE.setFixedWidth(50)
			self.oFxStepE.move(col2, row)
			
			# ############################################################################
			# options - set custom button
			# ############################################################################

			row += 30

			# button
			self.e1B1 = QtGui.QPushButton(translate('magicFixture', 'set custom values'), self)
			self.e1B1.clicked.connect(self.refreshSettings)
			self.e1B1.setFixedWidth(toolSW-20)
			self.e1B1.move(10, row)

			# ############################################################################
			# options - transform command
			# ############################################################################

			row += 40

			# button
			self.e2B1 = QtGui.QPushButton(translate('magicFixture', 'set manually'), self)
			self.e2B1.clicked.connect(self.setEditModeON)
			self.e2B1.setFixedWidth((toolSW/2)-20)
			self.e2B1.setFixedHeight(40)
			self.e2B1.move(10, row)

			# button
			self.e2B2 = QtGui.QPushButton(translate('magicFixture', 'finish manually'), self)
			self.e2B2.clicked.connect(self.setEditModeOFF)
			self.e2B2.setFixedWidth((toolSW/2)-20)
			self.e2B2.setFixedHeight(40)
			self.e2B2.move((toolSW/2)+10, row)

			# ############################################################################
			# options - final save
			# ############################################################################

			row += 60

			# button
			self.e3B1 = QtGui.QPushButton(translate('magicFixture', 'apply fixture to this position'), self)
			self.e3B1.clicked.connect(self.setFixture)
			self.e3B1.setFixedWidth(toolSW-20)
			self.e3B1.setFixedHeight(40)
			self.e3B1.move(10, row)

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
			self.gLink.Placement.Rotation = reset
			
			angle = self.gRoAnglesArr[self.gRoIndex]
			axis = FreeCAD.Vector(self.gRoAxis)

			x = self.gLink.Placement.Base.x
			y = self.gLink.Placement.Base.y
			z = self.gLink.Placement.Base.z
			
			center = FreeCAD.Vector(x, y, z)
			
			Draft.rotate(self.gLink, angle, center, axis, False)
				
			FreeCADGui.Selection.clearSelection()
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def showFixture(self):
			
			# set info
			
			info = str(self.gEdgeIndex + 1) + " / " + str(len(self.gEdgeArr))
			self.s2IS.setText(info)

			info = str(self.gRoIndex + 1) + " / " + str(len(self.gRoAnglesArr))
			self.s4IS.setText(info)
			
			# ############################################################################
			# remove all
			# ############################################################################
			
			if self.gLink != "":
				try:
					FreeCAD.activeDocument().removeObject(str(self.gLink.Name))
				except:
					skip = 1
			
			self.gLink = ""
			
			# get settings
			[ v1, v2 ] = MagicPanels.getEdgeVertices(self.gEdgeArr[self.gEdgeIndex])
			
			# ############################################################################
			# set link
			# ############################################################################
			
			X, Y, Z = v1[0], v1[1], v1[2]
			x , y, z = 0, 0, 0
			
			linkName = "Link_" + str(self.gBaseRef.Name)
			link = FreeCAD.activeDocument().addObject('App::Link', linkName)
			link.setLink(self.gBaseRef)
			link.Label = "Link, " + self.gBaseRef.Label + " "

			# edge along X
			if v1[0] != v2[0]:
				
				if self.gFPlane == "XY":
					x = X - self.gFxOCorner
					y = Y + self.gFxOEdge
					z = Z - self.gFxSink
				
				if self.gFPlane == "XZ":
					x = X - self.gFxOCorner
					y = Y - self.gFxSink
					z = Z + self.gFxOEdge
		
				# this should not exist
				if self.gFPlane == "YZ":
					x, y, z = X, Y, Z

			# edge along Y
			if v1[1] != v2[1]:
				
				if self.gFPlane == "XY":
					x = X + self.gFxOEdge
					y = Y - self.gFxOCorner
					z = Z - self.gFxSink
			
				# this should not exist
				if self.gFPlane == "XZ":
					[ x, y, z ] = [ X, Y, Z ]
			
				if self.gFPlane == "YZ":
					x = X - self.gFxSink
					y = Y - self.gFxOCorner
					z = Z + self.gFxOEdge

			# edge along Z
			if v1[2] != v2[2]:
				
				if self.gFPlane == "XY":
					x = X + self.gFxOEdge
					y = Y - self.gFxSink
					z = Z - self.gFxOCorner
					
				if self.gFPlane == "XZ":
					x = X - self.gFxOEdge
					y = Y - self.gFxSink
					z = Z - self.gFxOCorner
						
				if self.gFPlane == "YZ":
					x = X - self.gFxSink
					y = Y + self.gFxOEdge
					z = Z - self.gFxOCorner
					
			# final set
			link.Placement.Base.x = x
			link.Placement.Base.y = y
			link.Placement.Base.z = z
			
			self.gLink = link

			# ############################################################################
			# set rotation
			# ############################################################################

			self.setRotation()

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def resetGlobals(self):

			self.gBaseRef = ""
			self.gObjRef = ""
			
			self.gFaceRef = ""
			self.gFaceIndex = 0
			self.gFPlane = ""
		
			self.gEdgeRef = ""
			self.gEdgeArr = []
			self.gEdgeIndex = 0
		
			self.gRoAxisArr = []
			self.gRoAxis = ""
		
			self.gRoAnglesArr = []
			self.gRoAngles = ""
		
			self.gRoIndex = 0

		# ############################################################################
		def getSelected(self):

			try:

				# ############################################################################
				# global config
				# ############################################################################
				
				self.resetGlobals()

				self.gBaseRef = FreeCADGui.Selection.getSelection()[0]
				
				self.gObjRef = FreeCADGui.Selection.getSelection()[1]
				self.gFaceRef = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				self.gFaceIndex = MagicPanels.getFaceIndex(self.gObjRef, self.gFaceRef)
				
				FreeCADGui.Selection.clearSelection()
				
				n = ""
				n += str(self.gBaseRef.Label)
				self.ob1S.setText(n)
				
				n = ""
				n += str(self.gObjRef.Label)
				n += ", "
				n += "Face"
				n += str(self.gFaceIndex)
				self.ob2S.setText(n)
				
				self.gFPlane = MagicPanels.getFacePlane(self.gFaceRef)
				
				# ############################################################################
				# set possible edges
				# ############################################################################
				
				self.gEdgeArr.append(self.gFaceRef.Edges[0])
				self.gEdgeArr.append(self.gFaceRef.Edges[1])
				self.gEdgeArr.append(self.gFaceRef.Edges[2])
				self.gEdgeArr.append(self.gFaceRef.Edges[3])
					
				# ############################################################################
				# set possible rotation 
				# ############################################################################
				
				# X axis
				self.gRoAnglesArr.append(0)
				self.gRoAxisArr.append([1, 0, 0])
				
				self.gRoAnglesArr.append(90)
				self.gRoAxisArr.append([1, 0, 0])
				
				self.gRoAnglesArr.append(180)
				self.gRoAxisArr.append([1, 0, 0])
				
				self.gRoAnglesArr.append(270)
				self.gRoAxisArr.append([1, 0, 0])
				
				# Y axis
				self.gRoAnglesArr.append(0)
				self.gRoAxisArr.append([0, 1, 0])
				
				self.gRoAnglesArr.append(90)
				self.gRoAxisArr.append([0, 1, 0])
				
				self.gRoAnglesArr.append(180)
				self.gRoAxisArr.append([0, 1, 0])
				
				self.gRoAnglesArr.append(270)
				self.gRoAxisArr.append([0, 1, 0])
				
				# Z axis
				self.gRoAnglesArr.append(0)
				self.gRoAxisArr.append([0, 0, 1])
				
				self.gRoAnglesArr.append(90)
				self.gRoAxisArr.append([0, 0, 1])
				
				self.gRoAnglesArr.append(180)
				self.gRoAxisArr.append([0, 0, 1])
				
				self.gRoAnglesArr.append(270)
				self.gRoAxisArr.append([0, 0, 1])
				
				# special 1
				
				self.gRoAnglesArr.append(0)
				self.gRoAxisArr.append([0.71, 0.71, 0])
				
				self.gRoAnglesArr.append(90)
				self.gRoAxisArr.append([0.71, 0.71, 0])
				
				self.gRoAnglesArr.append(180)
				self.gRoAxisArr.append([0.71, 0.71, 0])
				
				self.gRoAnglesArr.append(270)
				self.gRoAxisArr.append([0.71, 0.71, 0])
				
				# special 2
				
				self.gRoAnglesArr.append(120)
				self.gRoAxisArr.append([-0.58, -0.58, 0.58])
				
				self.gRoAnglesArr.append(120)
				self.gRoAxisArr.append([0.58, 0.58, 0.58])
				
				self.gRoAnglesArr.append(180)
				self.gRoAxisArr.append([0.58, 0.58, -0.58])
				
				self.gRoAnglesArr.append(270)
				self.gRoAxisArr.append([0.58, 0.58, -0.58])
				
				self.gRoAnglesArr.append(120)
				self.gRoAxisArr.append([-0.58, 0.58, 0.58])

				# init
				self.gRoAngles = self.gRoAnglesArr[0]
				self.gRoAxis = self.gRoAxisArr[0]
				
				# ############################################################################
				
				self.showFixture()
			
				self.ob3S.setText("")
				
			except:

				self.ob3S.setText(self.gNoSelection)
				return -1
			
		# ############################################################################
		def setEdgeP(self):
			
			try:
				if self.gEdgeIndex - 1 < 0:
					self.gEdgeIndex = len(self.gEdgeArr) - 1
				else:
					self.gEdgeIndex = self.gEdgeIndex - 1
					
				self.gEdgeRef = self.gEdgeArr[self.gEdgeIndex]
				
				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)
			
		def setEdgeN(self):
			
			try:
				if self.gEdgeIndex + 1 > len(self.gEdgeArr) - 1:
					self.gEdgeIndex = 0
				else:
					self.gEdgeIndex = self.gEdgeIndex + 1
					
				self.gEdgeRef = self.gEdgeArr[self.gEdgeIndex]
				
				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)

		# ############################################################################
		def setSinkOffsetP(self):
			
			try:
				self.gStep = int(self.oFxStepE.text())
			
				self.gFxSink -= self.gStep
				self.oFxSinkE.setText(str(self.gFxSink))
				
				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)
			
		def setSinkOffsetN(self):
			
			try:
				self.gStep = int(self.oFxStepE.text())
				
				self.gFxSink += self.gStep
				self.oFxSinkE.setText(str(self.gFxSink))
				
				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)

		# ############################################################################
		def setCornerOffsetP(self):
			
			try:
				self.gStep = int(self.oFxStepE.text())
				
				self.gFxOCorner -= self.gStep
				self.oFxOCornerE.setText(str(self.gFxOCorner))
				
				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)
			
		def setCornerOffsetN(self):
			
			try:
				self.gStep = int(self.oFxStepE.text())
				
				self.gFxOCorner += self.gStep
				self.oFxOCornerE.setText(str(self.gFxOCorner))
				
				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)

		# ############################################################################
		def setEdgeOffsetP(self):
			
			try:
				self.gStep = int(self.oFxStepE.text())
				
				self.gFxOEdge -= self.gStep
				self.oFxOEdgeE.setText(str(self.gFxOEdge))
				
				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)
			
		def setEdgeOffsetN(self):
			
			try:
				self.gStep = int(self.oFxStepE.text())
				
				self.gFxOEdge += self.gStep
				self.oFxOEdgeE.setText(str(self.gFxOEdge))
				
				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)

		# ############################################################################
		def setRoAnglesP(self):
			
			try:
				if self.gRoIndex - 1 < 0:
					self.gRoIndex = len(self.gRoAnglesArr) - 1
				else:
					self.gRoIndex = self.gRoIndex - 1
					
				self.gRoAngles = self.gRoAnglesArr[self.gRoIndex]
				self.gRoAxis = self.gRoAxisArr[self.gRoIndex]
				
				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)
			
		def setRoAnglesN(self):
			
			try:
				if self.gRoIndex + 1 > len(self.gRoAnglesArr) - 1:
					self.gRoIndex = 0
				else:
					self.gRoIndex = self.gRoIndex + 1
					
				self.gRoAngles = self.gRoAnglesArr[self.gRoIndex]
				self.gRoAxis = self.gRoAxisArr[self.gRoIndex]
				
				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)

		# ############################################################################
		def refreshSettings(self):
			
			try:
			
				self.gFxSink = float(self.oFxSinkE.text())
				self.gFxOCorner = float(self.oFxOCornerE.text())
				self.gFxOEdge = float(self.oFxOEdgeE.text())
				self.gStep = int(self.oFxStepE.text())

				self.showFixture()
			
			except:
				self.ob3S.setText(self.gNoSelection)
				
		# ############################################################################
		def setEditModeON(self):
			
			try:
				vo = self.gLink.ViewObject
				vo.Document.setEdit(vo, 1)
				
			except:
				self.ob3S.setText(self.gNoSelection)
		
		def setEditModeOFF(self):
			
			try:
				vo = self.gLink.ViewObject
				vo.Document.resetEdit()
				
			except:
				self.ob3S.setText(self.gNoSelection)
		
		# ############################################################################
		def setFixture(self):
			
			try:
				self.gLink = ""
				
			except:
				self.ob3S.setText(self.gNoSelection)
		
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		if form.gLink != "":
			try:
				FreeCAD.activeDocument().removeObject(str(form.gLink.Name))
			except:
				skip = 1
			
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
