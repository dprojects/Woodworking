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

		# 1st selected object - sketch
		gObj1 = ""
		gObj1Visible = ""
		
		# 2nd selected object - auto Tenon
		gObj2 = ""
		gObj2Face = ""
		gObj2FaceIndex = 0
		
		# 3rd selected object - auto Mortise
		gObj3 = ""
		gObj3Face = ""
		gObj3FaceIndex = 0

		gAnchorCurrent = ""
		gAnchorArr = []
		gAnchorIndex = 0 
		
		gRoAxisArr = []
		gRoAxis = ""
		
		gRoAnglesArr = []
		gRoAngles = ""
		
		gRoIndex = 0
		
		gStep = 32
		gDepth = 15
		
		gLink = ""

		gMaxX = 0
		gMaxY = 0
		gMaxZ = 0
		
		gAxisX = 0
		gAxisY = 0
		gAxisZ = 0
		
		gCrossCorner = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
		gCrossCenter = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()

		gNoSelection1 = translate('magicJoints', '1. select Sketch pattern')
		gNoSelection2 = translate('magicJoints', '2. select face to map Sketch')
		gNoSelection3 = translate('magicJoints', '3. select face for Mortise')
		
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
			toolSH = 500
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 0 + 300
			gPH = int( gSH - toolSH ) - 30

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicJoints', 'magicJoints'))
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
			
			# ############################################################################
			# options - 1st object
			# ############################################################################

			# button
			self.ob1B1 = QtGui.QPushButton(translate('magicJoints', 'set'), self)
			self.ob1B1.clicked.connect(self.setObj1)
			self.ob1B1.setFixedWidth(30)
			self.ob1B1.setFixedHeight(20)
			self.ob1B1.move(10, row)

			# screen
			self.ob1S = QtGui.QLabel(info, self)
			self.ob1S.move(50, row+3)
			
			# ############################################################################
			# options - 2nd object
			# ############################################################################
			
			row += 20

			# button
			self.ob2B1 = QtGui.QPushButton(translate('magicJoints', 'set'), self)
			self.ob2B1.clicked.connect(self.setObj2)
			self.ob2B1.setFixedWidth(30)
			self.ob2B1.setFixedHeight(20)
			self.ob2B1.move(10, row)
			
			# screen
			self.ob2S = QtGui.QLabel(info, self)
			self.ob2S.move(50, row+3)

			# ############################################################################
			# options - 3rd object
			# ############################################################################
			
			row += 20
			
			# button
			self.ob3B1 = QtGui.QPushButton(translate('magicJoints', 'set'), self)
			self.ob3B1.clicked.connect(self.setObj3)
			self.ob3B1.setFixedWidth(30)
			self.ob3B1.setFixedHeight(20)
			self.ob3B1.move(10, row)
			
			# screen
			self.ob3S = QtGui.QLabel(info, self)
			self.ob3S.move(50, row+3)
			
			# ############################################################################
			# options - refresh all
			# ############################################################################

			row += 20
			
			# button
			self.s1B1 = QtGui.QPushButton(translate('magicJoints', 'refresh all selections'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(toolSW-20)
			self.s1B1.setFixedHeight(40)
			self.s1B1.move(10, row)

			# ############################################################################
			# options - select edge
			# ############################################################################

			row += 50

			# label
			self.s2L = QtGui.QLabel(translate('magicJoints', 'Anchor:'), self)
			self.s2L.move(10, row+3)

			# button
			self.s2B1 = QtGui.QPushButton("<", self)
			self.s2B1.clicked.connect(self.setAnchorP)
			self.s2B1.setFixedWidth(50)
			self.s2B1.move(col1, row)
			self.s2B1.setAutoRepeat(True)
			
			# info screen
			self.s2IS = QtGui.QLabel(info, self)
			self.s2IS.move(col2, row+3)

			# button
			self.s2B2 = QtGui.QPushButton(">", self)
			self.s2B2.clicked.connect(self.setAnchorN)
			self.s2B2.setFixedWidth(50)
			self.s2B2.move(col3, row)
			self.s2B2.setAutoRepeat(True)

			# ############################################################################
			# options - adjust rotation
			# ############################################################################

			row += 30
			
			# label
			self.s4L = QtGui.QLabel(translate('magicJoints', 'Rotation:'), self)
			self.s4L.move(10, row+3)

			# button
			self.s4B1 = QtGui.QPushButton("<", self)
			self.s4B1.clicked.connect(self.setRoAnglesP)
			self.s4B1.setFixedWidth(50)
			self.s4B1.move(col1, row)
			self.s4B1.setAutoRepeat(True)
			
			# info screen
			self.s4IS = QtGui.QLabel(info, self)
			self.s4IS.move(col2, row+3)
			
			# button
			self.s4B2 = QtGui.QPushButton(">", self)
			self.s4B2.clicked.connect(self.setRoAnglesN)
			self.s4B2.setFixedWidth(50)
			self.s4B2.move(col3, row)
			self.s4B2.setAutoRepeat(True)

			# ############################################################################
			# options - X axis
			# ############################################################################

			row += 40
			
			# label
			self.oAxisXL = QtGui.QLabel(translate('magicJoints', 'X axis:'), self)
			self.oAxisXL.move(10, row+3)

			# button
			self.oAxisXB1 = QtGui.QPushButton("-", self)
			self.oAxisXB1.clicked.connect(self.setXm)
			self.oAxisXB1.setFixedWidth(50)
			self.oAxisXB1.move(col1, row)
			self.oAxisXB1.setAutoRepeat(True)

			# text input
			self.oAxisXE = QtGui.QLineEdit(self)
			self.oAxisXE.setText(str(self.gAxisX))
			self.oAxisXE.setFixedWidth(50)
			self.oAxisXE.move(col2, row)

			# button
			self.oAxisXB2 = QtGui.QPushButton("+", self)
			self.oAxisXB2.clicked.connect(self.setXp)
			self.oAxisXB2.setFixedWidth(50)
			self.oAxisXB2.move(col3, row)
			self.oAxisXB2.setAutoRepeat(True)

			# ############################################################################
			# options - Y axis
			# ############################################################################

			row += 30
			
			# label
			self.oAxisYL = QtGui.QLabel(translate('magicJoints', 'Y axis:'), self)
			self.oAxisYL.move(10, row+3)

			# button
			self.gAxisYB1 = QtGui.QPushButton("-", self)
			self.gAxisYB1.clicked.connect(self.setYm)
			self.gAxisYB1.setFixedWidth(50)
			self.gAxisYB1.move(col1, row)
			self.gAxisYB1.setAutoRepeat(True)

			# text input
			self.oAxisYE = QtGui.QLineEdit(self)
			self.oAxisYE.setText(str(self.gAxisY))
			self.oAxisYE.setFixedWidth(50)
			self.oAxisYE.move(col2, row)

			# button
			self.gAxisYB2 = QtGui.QPushButton("+", self)
			self.gAxisYB2.clicked.connect(self.setYp)
			self.gAxisYB2.setFixedWidth(50)
			self.gAxisYB2.move(col3, row)
			self.gAxisYB2.setAutoRepeat(True)

			# ############################################################################
			# options - Z axis
			# ############################################################################

			row += 30
			
			# label
			self.oAxisZL = QtGui.QLabel(translate('magicJoints', 'Z axis:'), self)
			self.oAxisZL.move(10, row+3)

			# button
			self.gAxisZB1 = QtGui.QPushButton("-", self)
			self.gAxisZB1.clicked.connect(self.setZm)
			self.gAxisZB1.setFixedWidth(50)
			self.gAxisZB1.move(col1, row)
			self.gAxisZB1.setAutoRepeat(True)

			# text input
			self.oAxisZE = QtGui.QLineEdit(self)
			self.oAxisZE.setText(str(self.gAxisZ))
			self.oAxisZE.setFixedWidth(50)
			self.oAxisZE.move(col2, row)

			# button
			self.gAxisZB2 = QtGui.QPushButton("+", self)
			self.gAxisZB2.clicked.connect(self.setZp)
			self.gAxisZB2.setFixedWidth(50)
			self.gAxisZB2.move(col3, row)
			self.gAxisZB2.setAutoRepeat(True)

			# ############################################################################
			# options - step
			# ############################################################################

			row += 30

			# label
			self.oFxStepL = QtGui.QLabel(translate('magicJoints', 'Step:'), self)
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
			self.e1B1 = QtGui.QPushButton(translate('magicJoints', 'set custom values'), self)
			self.e1B1.clicked.connect(self.refreshSettings)
			self.e1B1.setFixedWidth(toolSW-20)
			self.e1B1.move(10, row)

			# ############################################################################
			# options - transform command
			# ############################################################################

			row += 30

			# button
			self.e2B1 = QtGui.QPushButton(translate('magicJoints', 'set manually'), self)
			self.e2B1.clicked.connect(self.setEditModeON)
			self.e2B1.setFixedWidth((toolSW/2)-20)
			self.e2B1.setFixedHeight(20)
			self.e2B1.move(10, row)

			# button
			self.e2B2 = QtGui.QPushButton(translate('magicJoints', 'finish manually'), self)
			self.e2B2.clicked.connect(self.setEditModeOFF)
			self.e2B2.setFixedWidth((toolSW/2)-20)
			self.e2B2.setFixedHeight(20)
			self.e2B2.move((toolSW/2)+10, row)

			# ############################################################################
			# options - depth
			# ############################################################################

			row += 40

			# label
			self.oFxDepthL = QtGui.QLabel(translate('magicJoints', 'Mortise depth and Tenon height:'), self)
			self.oFxDepthL.move(10, row+3)

			# text input
			self.oFxDepthE = QtGui.QLineEdit(self)
			self.oFxDepthE.setText(str(self.gDepth))
			self.oFxDepthE.setFixedWidth(50)
			self.oFxDepthE.move(col3, row)

			# ############################################################################
			# options - final save
			# ############################################################################

			row += 30

			# apply button
			self.e3B1 = QtGui.QPushButton(translate('magicJoints', 'create Mortise'), self)
			self.e3B1.clicked.connect(self.setMortise)
			self.e3B1.setFixedWidth((toolSW/2)-20)
			self.e3B1.setFixedHeight(20)
			self.e3B1.move(10, row)

			# apply button
			self.e3B2 = QtGui.QPushButton(translate('magicJoints', 'create Tenon'), self)
			self.e3B2.clicked.connect(self.setTenon)
			self.e3B2.setFixedWidth((toolSW/2)-20)
			self.e3B2.setFixedHeight(20)
			self.e3B2.move((toolSW/2)+10, row)

			# ############################################################################
			# options - final save both
			# ############################################################################

			row += 30

			# apply button
			self.e3B3 = QtGui.QPushButton(translate('magicJoints', 'create Tenon and Mortise'), self)
			self.e3B3.clicked.connect(self.setJoints)
			self.e3B3.setFixedWidth(toolSW-20)
			self.e3B3.setFixedHeight(40)
			self.e3B3.move(10, row)

			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()

			# init
			FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(50)
			self.getSelected()

		# ############################################################################
		# actions - internal functions, no error handling
		# ############################################################################

		# ############################################################################
		def resetInfoScreen(self):

			self.ob1S.setText(self.gNoSelection1)
			self.ob2S.setText(self.gNoSelection2)
			self.ob3S.setText(self.gNoSelection3)
		
		# ############################################################################
		def refreshInfoScreens(self):
			
			try:
				n = ""
				n += str(self.gObj1.Label)
				self.ob1S.setText(n)
			except:
				self.ob1S.setText(self.gNoSelection1)

			try:
				n = ""
				n += str(self.gObj2.Label)
				n += ", "
				n += "Face"
				n += str(self.gObj2FaceIndex)
				self.ob2S.setText(n)
			except:
				self.ob2S.setText(self.gNoSelection2)
			
			try:
				n = ""
				n += str(self.gObj3.Label)
				n += ", "
				n += "Face"
				n += str(self.gObj3FaceIndex)
				self.ob3S.setText(n)
			except:
				self.ob3S.setText(self.gNoSelection3)
				
		# ############################################################################
		def resetGlobals(self):

			self.gObj1 = ""
			
			self.gObj2 = ""
			self.gObj2Face = ""
			self.gObj2FaceIndex = 0
		
			self.gObj3 = ""
			self.gObj3Face = ""
			self.gObj3FaceIndex = 0
			
			self.gAnchorCurrent = ""
			self.gAnchorArr = []
			self.gAnchorIndex = 0
		
			self.gRoAxisArr = []
			self.gRoAxis = ""
		
			self.gRoAnglesArr = []
			self.gRoAngles = ""
		
			self.gRoIndex = 0
			
			self.gAxisX = 0
			self.gAxisY = 0
			self.gAxisZ = 0
			
			self.oAxisXE.setText(str(self.gAxisX))
			self.oAxisYE.setText(str(self.gAxisY))
			self.oAxisZE.setText(str(self.gAxisZ))
			
		# ############################################################################
		def setRotation(self):
			
			reset = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
			self.gLink.Placement.Rotation = reset
			
			angle = self.gRoAngles
			axis = FreeCAD.Vector(self.gRoAxis)

			x = self.gLink.Placement.Base.x
			y = self.gLink.Placement.Base.y
			z = self.gLink.Placement.Base.z
			
			center = FreeCAD.Vector(x, y, z)
			
			Draft.rotate(self.gLink, angle, center, axis, False)
				
			FreeCADGui.Selection.clearSelection()
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def setSketchRotations(self):
			
			import math
			
			self.gRoAnglesArr = []
			self.gRoAxisArr = []
			
			[ x, y, z, r ] = MagicPanels.getSketchPlacement(self.gObj1, "global")

			# init state
			self.gRoAnglesArr.append( math.degrees(r.Angle) )
			self.gRoAxisArr.append( [ r.Axis.x, r.Axis.y, r.Axis.z ] )
			
			# Z axis
			self.gRoAnglesArr.append(0)
			self.gRoAxisArr.append([0, 0, 1])
			
			self.gRoAnglesArr.append(90)
			self.gRoAxisArr.append([0, 0, 1])
			
			self.gRoAnglesArr.append(180)
			self.gRoAxisArr.append([0, 0, 1])
			
			self.gRoAnglesArr.append(270)
			self.gRoAxisArr.append([0, 0, 1])
			
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

			self.gRoAnglesArr.append(180)
			self.gRoAxisArr.append([0, 0.71, 0.71])
			
			# init
			self.gRoAngles = self.gRoAnglesArr[0]
			self.gRoAxis = self.gRoAxisArr[0]
		
		# ############################################################################
		def setSketchAnchors(self):
			
			[ x, y, z, r ] = MagicPanels.getSketchPlacement(self.gObj1, "global")
			[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(self.gObj2Face)
		
			self.gAnchorArr = []
			self.gAnchorArr.append([x, y, z])
			self.gAnchorArr.append(v1)
			self.gAnchorArr.append(v2)
			self.gAnchorArr.append(v3)
			self.gAnchorArr.append(v4)
			
			self.gAnchorCurrent = self.gAnchorArr[self.gAnchorIndex]
		
		# ############################################################################
		def setSelectionData(self):
		
			try:
				self.setSketchAnchors()
			except:
				skip = 1
			
			try:
				self.setSketchRotations()
			except:
				skip = 1
				
			try:
				self.showJoints()
			except:
				skip = 1
			
		# ############################################################################
		def showJoints(self):
			
			# set info screen
			
			info = str(self.gAnchorIndex + 1) + " / " + str(len(self.gAnchorArr))
			self.s2IS.setText(info)

			info = str(self.gRoIndex + 1) + " / " + str(len(self.gRoAnglesArr))
			self.s4IS.setText(info)
			
			# remove all
			
			if self.gLink != "":
				try:
					FreeCAD.activeDocument().removeObject(str(self.gLink.Name))
				except:
					skip = 1
			
			self.gLink = ""
			
			# set anchor
			
			X, Y, Z = self.gAnchorCurrent[0], self.gAnchorCurrent[1], self.gAnchorCurrent[2]
			x, y, z = 0, 0, 0

			# copy Sketch

			link = Draft.make_clone(self.gObj1)
			link.Label = "Pattern from " + str(self.gObj1.Label) + " "
			
			link.ViewObject.LineWidth = 6.00
			link.ViewObject.LineColor = (1.00,0.00,0.00)
			self.gObj1.Visibility = False

			# set object into position

			x = X + self.gAxisX
			y = Y + self.gAxisY
			z = Z + self.gAxisZ

			link.Placement.Base.x = x
			link.Placement.Base.y = y
			link.Placement.Base.z = z
			
			self.gLink = link

			# set current rotation
			
			self.setRotation()

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def setObj1(self):

			try:
				self.gObj1 = FreeCADGui.Selection.getSelection()[0]
				self.gObj1Visible = self.gObj1.Visibility

				FreeCADGui.Selection.clearSelection()
				self.refreshInfoScreens()
				self.setSelectionData()
				
			except:
				self.resetInfoScreen()

		def setObj2(self):
			
			try:
				self.gObj2 = FreeCADGui.Selection.getSelection()[0]
				self.gObj2Face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gObj2FaceIndex = MagicPanels.getFaceIndex(self.gObj2, self.gObj2Face)

				FreeCADGui.Selection.clearSelection()
				self.refreshInfoScreens()
				self.setSelectionData()

			except:
				self.resetInfoScreen()

		def setObj3(self):
			
			try:
				self.gObj3 = FreeCADGui.Selection.getSelection()[0]
				self.gObj3Face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gObj3FaceIndex = MagicPanels.getFaceIndex(self.gObj3, self.gObj3Face)

				FreeCADGui.Selection.clearSelection()
				self.refreshInfoScreens()
				self.setSelectionData()
				
			except:
				self.resetInfoScreen()

		# ############################################################################
		def getSelected(self):

			try:

				# update face of 2nd object only
				if self.gObj1 != "" and len(FreeCADGui.Selection.getSelection()) == 1:
					
					# update face data
					self.gObj2 = FreeCADGui.Selection.getSelection()[0]
					self.gObj2Face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
					self.gObj2FaceIndex = MagicPanels.getFaceIndex(self.gObj2, self.gObj2Face)
					FreeCADGui.Selection.clearSelection()
					
					# update info screen for face only
					n = ""
					n += str(self.gObj2.Label)
					n += ", "
					n += "Face"
					n += str(self.gObj2FaceIndex)
					self.ob2S.setText(n)
					
					# load new face anchors but not refresh sketch to keep the same place
					self.setSketchAnchors()
				
					return
				
				# init
				self.resetGlobals()

				# get all objects
				self.gObj1 = FreeCADGui.Selection.getSelection()[0]
				self.gObj1Visible = self.gObj1.Visibility

				self.gObj2 = FreeCADGui.Selection.getSelection()[1]
				self.gObj2Face = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				self.gObj2FaceIndex = MagicPanels.getFaceIndex(self.gObj2, self.gObj2Face)
				
				try:
					self.gObj3 = FreeCADGui.Selection.getSelection()[2]
					self.gObj3Face = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
					self.gObj3FaceIndex = MagicPanels.getFaceIndex(self.gObj3, self.gObj3Face)
				except:
					skip = 1

				self.refreshInfoScreens()

				self.setSketchAnchors()
				self.setSketchRotations()
				self.showJoints()

			except:
				self.resetInfoScreen()
				return -1

		# ############################################################################
		def setAnchorP(self):
			
			try:
				if self.gAnchorIndex - 1 < 0:
					self.gAnchorIndex = len(self.gAnchorArr) - 1
				else:
					self.gAnchorIndex = self.gAnchorIndex - 1
					
				self.gAnchorCurrent = self.gAnchorArr[self.gAnchorIndex]
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()

		def setAnchorN(self):
			
			try:
				if self.gAnchorIndex + 1 > len(self.gAnchorArr) - 1:
					self.gAnchorIndex = 0
				else:
					self.gAnchorIndex = self.gAnchorIndex + 1
					
				self.gAnchorCurrent = self.gAnchorArr[self.gAnchorIndex]
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()

		# ############################################################################
		def setXm(self):
			
			try:
				self.gStep = float(self.oFxStepE.text())
				
				self.gAxisX -= self.gStep
				self.oAxisXE.setText(str(self.gAxisX))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()
			
		def setXp(self):
			
			try:
				self.gStep = float(self.oFxStepE.text())
				
				self.gAxisX += self.gStep
				self.oAxisXE.setText(str(self.gAxisX))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()

		# ############################################################################
		def setYm(self):
			
			try:
				self.gStep = float(self.oFxStepE.text())
				
				self.gAxisY -= self.gStep
				self.oAxisYE.setText(str(self.gAxisY))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()
			
		def setYp(self):
			
			try:
				self.gStep = float(self.oFxStepE.text())
				
				self.gAxisY += self.gStep
				self.oAxisYE.setText(str(self.gAxisY))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()

		# ############################################################################
		def setZm(self):
			
			try:
				self.gStep = float(self.oFxStepE.text())
				
				self.gAxisZ -= self.gStep
				self.oAxisZE.setText(str(self.gAxisZ))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()
			
		def setZp(self):
			
			try:
				self.gStep = float(self.oFxStepE.text())
				
				self.gAxisZ += self.gStep
				self.oAxisZE.setText(str(self.gAxisZ))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()

		# ############################################################################
		def setRoAnglesP(self):
			
			try:
				if self.gRoIndex - 1 < 0:
					self.gRoIndex = len(self.gRoAnglesArr) - 1
				else:
					self.gRoIndex = self.gRoIndex - 1
					
				self.gRoAngles = self.gRoAnglesArr[self.gRoIndex]
				self.gRoAxis = self.gRoAxisArr[self.gRoIndex]
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()
			
		def setRoAnglesN(self):
			
			try:
				if self.gRoIndex + 1 > len(self.gRoAnglesArr) - 1:
					self.gRoIndex = 0
				else:
					self.gRoIndex = self.gRoIndex + 1
					
				self.gRoAngles = self.gRoAnglesArr[self.gRoIndex]
				self.gRoAxis = self.gRoAxisArr[self.gRoIndex]
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()

		# ############################################################################
		def refreshSettings(self):
			
			try:
				self.gAxisX = float(self.oAxisXE.text())
				self.gAxisY = float(self.oAxisYE.text())
				self.gAxisZ = float(self.oAxisZE.text())
				self.gStep = float(self.oFxStepE.text())

				self.showJoints()
			
			except:
				self.resetInfoScreen()
				
		# ############################################################################
		def setEditModeON(self):
			
			try:
				vo = self.gLink.ViewObject
				vo.Document.setEdit(vo, 1)
				
			except:
				self.resetInfoScreen()
		
		def setEditModeOFF(self):
			
			try:
				vo = self.gLink.ViewObject
				vo.Document.resetEdit()
				
			except:
				self.resetInfoScreen()
		
		# ############################################################################
		def setMortise(self):
			
			try:
				self.gDepth = float(self.oFxDepthE.text())
				t2 = self.gObj2.ViewObject.Transparency
				
				[ self.gObj2, self.gObj2Face ] = MagicPanels.makeMortise(self.gLink, self.gDepth, self.gObj2, self.gObj2Face)
				self.gObj2FaceIndex = MagicPanels.getFaceIndex(self.gObj2, self.gObj2Face)
				
				n = ""
				n += str(self.gObj2.Label)
				n += ", "
				n += "Face"
				n += str(self.gObj2FaceIndex)
				self.ob2S.setText(n)
				
				self.gObj2.ViewObject.Transparency = t2
				
			except:
				self.resetInfoScreen()
				
		def setTenon(self):
			
			try:
				self.gDepth = float(self.oFxDepthE.text())
				t2 = self.gObj2.ViewObject.Transparency
				
				[ self.gObj2, self.gObj2Face ] = MagicPanels.makeTenon(self.gLink, self.gDepth, self.gObj2, self.gObj2Face)
				self.gObj2FaceIndex = MagicPanels.getFaceIndex(self.gObj2, self.gObj2Face)
				
				n = ""
				n += str(self.gObj2.Label)
				n += ", "
				n += "Face"
				n += str(self.gObj2FaceIndex)
				self.ob2S.setText(n)
				
				self.gObj2.ViewObject.Transparency = t2
			
			except:
				self.resetInfoScreen()
		
		def setJoints(self):
			
			try:

				self.gDepth = float(self.oFxDepthE.text())
				
				t2 = self.gObj2.ViewObject.Transparency
				t3 = self.gObj3.ViewObject.Transparency
				
				[ self.gObj2, self.gObj2Face ] = MagicPanels.makeTenon(self.gLink, self.gDepth, self.gObj2, self.gObj2Face)
				self.gObj2FaceIndex = MagicPanels.getFaceIndex(self.gObj2, self.gObj2Face)
				
				[ self.gObj3, self.gObj3Face ] = MagicPanels.makeMortise(self.gLink, self.gDepth, self.gObj3, self.gObj3Face)
				self.gObj3FaceIndex = MagicPanels.getFaceIndex(self.gObj3, self.gObj3Face)
				
				self.refreshInfoScreens()
			
				self.gObj2.ViewObject.Transparency = t2
				self.gObj3.ViewObject.Transparency = t3
		
			except:
				self.resetInfoScreen()
			
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		
		FreeCADGui.ActiveDocument.ActiveView.setAxisCross(form.gCrossCenter)
		FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(form.gCrossCorner)

		try:
			FreeCAD.ActiveDocument.removeObject(str(form.gLink.Name))
			if form.gObj1Visible == True:
				form.gObj1.Visibility = True
			else:
				form.gObj1.Visibility = False
		except:
			skip = 1

		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
