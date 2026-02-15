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
		
		gNoSelection1 = translate('magicJoints', '1: select Sketch pattern')
		gNoSelection2 = translate('magicJoints', '2: select face for pattern position')
		gNoSelection3 = translate('magicJoints', '3 (optional): select face for Mortise')
		
		# foot
		gCornerCrossSupport = True
		gAxisCrossSupport = True
		
		try:
			gCornerCross = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
			gCornerCrossOrig = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
		except:
			gCornerCrossSupport = False
			
		try:
			gAxisCross = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()
			gAxisCrossOrig = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()
		except:
			gAxisCrossSupport = False
		
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
			toolSW = 393
			toolSH = 690
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('magicJoints', 'magicJoints'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			
			self.setMinimumSize(toolSW, toolSH)

			# ############################################################################
			# options - 1st object
			# ############################################################################

			# button
			self.ob1B1 = QtGui.QPushButton(translate('magicJoints', 'set'), self)
			self.ob1B1.clicked.connect(self.setObj1)
			self.ob1B1.setFixedWidth(50)
			
			# screen
			self.ob1S = QtGui.QLabel("", self)
			
			# ############################################################################
			# options - 2nd object
			# ############################################################################
			
			# button
			self.ob2B1 = QtGui.QPushButton(translate('magicJoints', 'set'), self)
			self.ob2B1.clicked.connect(self.setObj2)
			self.ob2B1.setFixedWidth(50)
			
			# screen
			self.ob2S = QtGui.QLabel("", self)
			
			# ############################################################################
			# options - 3rd object
			# ############################################################################
			
			# button
			self.ob3B1 = QtGui.QPushButton(translate('magicJoints', 'set'), self)
			self.ob3B1.clicked.connect(self.setObj3)
			self.ob3B1.setFixedWidth(50)
			
			# screen
			self.ob3S = QtGui.QLabel("", self)
			
			# ############################################################################
			# options - refresh all
			# ############################################################################

			# button
			self.s1B1 = QtGui.QPushButton(translate('magicJoints', 'refresh all selections'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedHeight(40)
			
			# ############################################################################
			# options - select edge
			# ############################################################################

			# label
			self.s2L = QtGui.QLabel(translate('magicJoints', 'Anchor:'), self)
			
			# button
			self.s2B1 = QtGui.QPushButton("<", self)
			self.s2B1.clicked.connect(self.setAnchorP)
			self.s2B1.setFixedWidth(50)
			self.s2B1.setAutoRepeat(True)
			
			# info screen
			self.s2IS = QtGui.QLabel("", self)
			
			# button
			self.s2B2 = QtGui.QPushButton(">", self)
			self.s2B2.clicked.connect(self.setAnchorN)
			self.s2B2.setFixedWidth(50)
			self.s2B2.setAutoRepeat(True)

			# ############################################################################
			# options - adjust rotation
			# ############################################################################

			# label
			self.s4L = QtGui.QLabel(translate('magicJoints', 'Rotation:'), self)
			
			# button
			self.s4B1 = QtGui.QPushButton("<", self)
			self.s4B1.clicked.connect(self.setRoAnglesP)
			self.s4B1.setFixedWidth(50)
			self.s4B1.setAutoRepeat(True)
			
			# info screen
			self.s4IS = QtGui.QLabel("", self)
			
			# button
			self.s4B2 = QtGui.QPushButton(">", self)
			self.s4B2.clicked.connect(self.setRoAnglesN)
			self.s4B2.setFixedWidth(50)
			self.s4B2.setAutoRepeat(True)

			# ############################################################################
			# options - X axis
			# ############################################################################

			# label
			self.oAxisXL = QtGui.QLabel(translate('magicJoints', 'X axis:'), self)
			
			# button
			self.oAxisXB1 = QtGui.QPushButton("-", self)
			self.oAxisXB1.clicked.connect(self.setXm)
			self.oAxisXB1.setFixedWidth(50)
			self.oAxisXB1.setAutoRepeat(True)

			# text input
			self.oAxisXE = QtGui.QLineEdit(self)
			self.oAxisXE.setText(MagicPanels.unit2gui(self.gAxisX))
			self.oAxisXE.setFixedWidth(80)
			
			# button
			self.oAxisXB2 = QtGui.QPushButton("+", self)
			self.oAxisXB2.clicked.connect(self.setXp)
			self.oAxisXB2.setFixedWidth(50)
			self.oAxisXB2.setAutoRepeat(True)

			# ############################################################################
			# options - Y axis
			# ############################################################################

			# label
			self.oAxisYL = QtGui.QLabel(translate('magicJoints', 'Y axis:'), self)
			
			# button
			self.gAxisYB1 = QtGui.QPushButton("-", self)
			self.gAxisYB1.clicked.connect(self.setYm)
			self.gAxisYB1.setFixedWidth(50)
			self.gAxisYB1.setAutoRepeat(True)

			# text input
			self.oAxisYE = QtGui.QLineEdit(self)
			self.oAxisYE.setText(MagicPanels.unit2gui(self.gAxisY))
			self.oAxisYE.setFixedWidth(80)
			
			# button
			self.gAxisYB2 = QtGui.QPushButton("+", self)
			self.gAxisYB2.clicked.connect(self.setYp)
			self.gAxisYB2.setFixedWidth(50)
			self.gAxisYB2.setAutoRepeat(True)

			# ############################################################################
			# options - Z axis
			# ############################################################################

			# label
			self.oAxisZL = QtGui.QLabel(translate('magicJoints', 'Z axis:'), self)
			
			# button
			self.gAxisZB1 = QtGui.QPushButton("-", self)
			self.gAxisZB1.clicked.connect(self.setZm)
			self.gAxisZB1.setFixedWidth(50)
			self.gAxisZB1.setAutoRepeat(True)

			# text input
			self.oAxisZE = QtGui.QLineEdit(self)
			self.oAxisZE.setText(MagicPanels.unit2gui(self.gAxisZ))
			self.oAxisZE.setFixedWidth(80)
			
			# button
			self.gAxisZB2 = QtGui.QPushButton("+", self)
			self.gAxisZB2.clicked.connect(self.setZp)
			self.gAxisZB2.setFixedWidth(50)
			self.gAxisZB2.setAutoRepeat(True)

			# ############################################################################
			# options - step
			# ############################################################################

			# label
			self.oFxStepL = QtGui.QLabel(translate('magicJoints', 'Step:'), self)
			
			# text input
			self.oFxStepE = QtGui.QLineEdit(self)
			self.oFxStepE.setText(MagicPanels.unit2gui(self.gStep))
			self.oFxStepE.setFixedWidth(80)
			
			# ############################################################################
			# options - set custom button
			# ############################################################################

			# button
			self.e1B1 = QtGui.QPushButton(translate('magicJoints', 'set custom values'), self)
			self.e1B1.clicked.connect(self.refreshSettings)
			
			# ############################################################################
			# options - transform command
			# ############################################################################

			# button
			self.e2B1 = QtGui.QPushButton(translate('magicJoints', 'set manually'), self)
			self.e2B1.clicked.connect(self.setEditModeON)
			
			# button
			self.e2B2 = QtGui.QPushButton(translate('magicJoints', 'finish manually'), self)
			self.e2B2.clicked.connect(self.setEditModeOFF)
			
			# ############################################################################
			# options - depth
			# ############################################################################

			# label
			self.oFxDepthL = QtGui.QLabel(translate('magicJoints', 'Mortise and Tenon size:'), self)
			
			# text input
			self.oFxDepthE = QtGui.QLineEdit(self)
			self.oFxDepthE.setText(MagicPanels.unit2gui(self.gDepth))
			
			# ############################################################################
			# options - final save
			# ############################################################################

			# apply button
			self.e3B1 = QtGui.QPushButton(translate('magicJoints', 'create Mortise'), self)
			self.e3B1.clicked.connect(self.setMortise)
			
			# apply button
			self.e3B2 = QtGui.QPushButton(translate('magicJoints', 'create Tenon'), self)
			self.e3B2.clicked.connect(self.setTenon)
			
			# ############################################################################
			# options - final save both
			# ############################################################################

			# apply button
			self.e3B3 = QtGui.QPushButton(translate('magicJoints', 'create Tenon and Mortise'), self)
			self.e3B3.clicked.connect(self.setJoints)
			self.e3B3.setFixedHeight(40)
			
			# ############################################################################
			# GUI for common foot
			# ############################################################################
			
			if self.gCornerCrossSupport == True:
			
				# label
				self.cocL = QtGui.QLabel(translate('magicJoints', 'Corner cross:'), self)

				# button
				self.cocB1 = QtGui.QPushButton("-", self)
				self.cocB1.clicked.connect(self.setCornerM)
				self.cocB1.setFixedWidth(50)
				self.cocB1.setAutoRepeat(True)
				
				# button
				self.cocB2 = QtGui.QPushButton("+", self)
				self.cocB2.clicked.connect(self.setCornerP)
				self.cocB2.setFixedWidth(50)
				self.cocB2.setAutoRepeat(True)

			if self.gAxisCrossSupport == True:
				
				# label
				self.cecL = QtGui.QLabel(translate('magicJoints', 'Center cross:'), self)

				# button
				self.cecB1 = QtGui.QPushButton(translate('magicJoints', 'on'), self)
				self.cecB1.clicked.connect(self.setCenterOn)
				self.cecB1.setFixedWidth(50)
				self.cecB1.setAutoRepeat(True)
				
				# button
				self.cecB2 = QtGui.QPushButton(translate('magicJoints', 'off'), self)
				self.cecB2.clicked.connect(self.setCenterOff)
				self.cecB2.setFixedWidth(50)
				self.cecB2.setAutoRepeat(True)

			if self.gCornerCrossSupport == True or self.gAxisCrossSupport == True:

				self.kccscb = QtGui.QCheckBox(translate('magicJoints', ' - keep custom cross settings'), self)
				self.kccscb.setCheckState(QtCore.Qt.Unchecked)
	
			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.row1 = QtGui.QHBoxLayout()
			self.row1.addWidget(self.ob1B1)
			self.row1.addWidget(self.ob1S)
			
			self.row2 = QtGui.QHBoxLayout()
			self.row2.addWidget(self.ob2B1)
			self.row2.addWidget(self.ob2S)
			
			self.row3 = QtGui.QHBoxLayout()
			self.row3.addWidget(self.ob3B1)
			self.row3.addWidget(self.ob3S)
			
			self.row4 = QtGui.QHBoxLayout()
			self.row4.addWidget(self.s1B1)
			
			self.row5 = QtGui.QGridLayout()
			self.row5.addWidget(self.s2L, 0, 0)
			self.row5.addWidget(self.s2B1, 0, 1)
			self.row5.addWidget(self.s2IS, 0, 2)
			self.row5.addWidget(self.s2B2, 0, 3)
			self.row5.addWidget(self.s4L, 1, 0)
			self.row5.addWidget(self.s4B1, 1, 1)
			self.row5.addWidget(self.s4IS, 1, 2)
			self.row5.addWidget(self.s4B2, 1, 3)
			self.groupBody1 = QtGui.QGroupBox(None, self)
			self.groupBody1.setLayout(self.row5)
			
			self.row6 = QtGui.QGridLayout()
			self.row6.addWidget(self.oAxisXL, 0, 0)
			self.row6.addWidget(self.oAxisXB1, 0, 1)
			self.row6.addWidget(self.oAxisXE, 0, 2)
			self.row6.addWidget(self.oAxisXB2, 0, 3)
			self.row6.addWidget(self.oAxisYL, 1, 0)
			self.row6.addWidget(self.gAxisYB1, 1, 1)
			self.row6.addWidget(self.oAxisYE, 1, 2)
			self.row6.addWidget(self.gAxisYB2, 1, 3)
			self.row6.addWidget(self.oAxisZL, 2, 0)
			self.row6.addWidget(self.gAxisZB1, 2, 1)
			self.row6.addWidget(self.oAxisZE, 2, 2)
			self.row6.addWidget(self.gAxisZB2, 2, 3)
			self.row6.addWidget(self.oFxStepL, 3, 0)
			self.row6.addWidget(self.oFxStepE, 3, 2)
			self.row7 = QtGui.QHBoxLayout()
			self.row7.addWidget(self.e1B1)
			self.row8 = QtGui.QHBoxLayout()
			self.row8.addWidget(self.e2B1)
			self.row8.addWidget(self.e2B2)
			self.rowBody2 = QtGui.QVBoxLayout()
			self.rowBody2.addLayout(self.row6)
			self.rowBody2.addLayout(self.row7)
			self.rowBody2.addLayout(self.row8)
			self.groupBody2 = QtGui.QGroupBox(None, self)
			self.groupBody2.setLayout(self.rowBody2)
			
			
			self.row9 = QtGui.QGridLayout()
			self.row9.addWidget(self.oFxDepthL, 0, 0)
			self.row9.addWidget(self.oFxDepthE, 0, 1)
			self.row10 = QtGui.QHBoxLayout()
			self.row10.addWidget(self.e3B1)
			self.row10.addWidget(self.e3B2)
			self.row11 = QtGui.QHBoxLayout()
			self.row11.addWidget(self.e3B3)
			self.rowBody3 = QtGui.QVBoxLayout()
			self.rowBody3.addLayout(self.row9)
			self.rowBody3.addLayout(self.row10)
			self.rowBody3.addLayout(self.row11)
			self.groupBody3 = QtGui.QGroupBox(None, self)
			self.groupBody3.setLayout(self.rowBody3)
			
			# create foot
			self.layoutFoot = QtGui.QVBoxLayout()
			
			self.rowFoot1 = QtGui.QHBoxLayout()
			self.rowFoot1.addWidget(self.cocL)
			self.rowFoot1.addWidget(self.cocB1)
			self.rowFoot1.addWidget(self.cocB2)
			self.layoutFoot.addLayout(self.rowFoot1)

			self.rowFoot2 = QtGui.QHBoxLayout()
			self.rowFoot2.addWidget(self.cecL)
			self.rowFoot2.addWidget(self.cecB1)
			self.rowFoot2.addWidget(self.cecB2)
			self.layoutFoot.addLayout(self.rowFoot2)
			
			self.rowFoot3 = QtGui.QHBoxLayout()
			self.rowFoot3.addWidget(self.kccscb)
			self.layoutFoot.addLayout(self.rowFoot3)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			
			self.layout.addLayout(self.row1)
			self.layout.addLayout(self.row2)
			self.layout.addLayout(self.row3)
			self.layout.addLayout(self.row4)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody1)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody2)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody3)
			self.layout.addStretch()
			self.layout.addLayout(self.layoutFoot)
			self.setLayout(self.layout)
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# set theme
			MagicPanels.setTheme(self)

			if self.gAxisCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			
			if self.gCornerCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(50)
			
			# init
			self.show()
			
			MagicPanels.adjustGUI(self, "left-offset")
			
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
			
			self.oAxisXE.setText(MagicPanels.unit2gui(self.gAxisX))
			self.oAxisYE.setText(MagicPanels.unit2gui(self.gAxisY))
			self.oAxisZE.setText(MagicPanels.unit2gui(self.gAxisZ))
			
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
			
			self.gAnchorArr = []
			
			# add current Sketch position
			[ x, y, z ] = MagicPanels.getPosition(self.gObj1, "global")
			self.gAnchorArr.append([x, y, z])
			
			# add CenterOfMass of the face
			try:
				v = [ self.gObj2Face.CenterOfMass.x, self.gObj2Face.CenterOfMass.y, self.gObj2Face.CenterOfMass.z ]
				[ v ] = MagicPanels.getVerticesOffset([ v ], self.gObj2, "array")
				self.gAnchorArr.append(v)
			except:
				skip = 1
			
			# add face vertices
			[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(self.gObj2Face)
			[ v1, v2, v3, v4 ] = MagicPanels.getVerticesOffset([ v1, v2, v3, v4 ], self.gObj2, "array")
			self.gAnchorArr.append(v1)
			self.gAnchorArr.append(v2)
			self.gAnchorArr.append(v3)
			self.gAnchorArr.append(v4)

			# add CenterOfMass for each edge of the face
			[ faceType, arrAll, arrThick, arrShort, arrLong ] = MagicPanels.getFaceEdges(self.gObj2, self.gObj2Face)
			for e in arrAll:
				try:
					v = [ e.CenterOfMass.x, e.CenterOfMass.y, e.CenterOfMass.z ]
					[ v ] = MagicPanels.getVerticesOffset([ v ], self.gObj2, "array")
					self.gAnchorArr.append(v)
				except:
					skip = 1
			
			# set default
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
			clone = Draft.make_clone(self.gObj1)
			clone.Label = "Pattern from " + str(self.gObj1.Label) + " "
			clone.ViewObject.LineWidth = 6.00
			clone.ViewObject.LineColor = (1.00,0.00,0.00)
			self.gObj1.Visibility = False

			# set object into position
			x = X + self.gAxisX
			y = Y + self.gAxisY
			z = Z + self.gAxisZ
			
			MagicPanels.setPosition(clone, x, y, z, "global")
			self.gLink = clone

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
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gAxisX -= self.gStep
				self.oAxisXE.setText(MagicPanels.unit2gui(self.gAxisX))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()
			
		def setXp(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gAxisX += self.gStep
				self.oAxisXE.setText(MagicPanels.unit2gui(self.gAxisX))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()

		# ############################################################################
		def setYm(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gAxisY -= self.gStep
				self.oAxisYE.setText(MagicPanels.unit2gui(self.gAxisY))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()
			
		def setYp(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gAxisY += self.gStep
				self.oAxisYE.setText(MagicPanels.unit2gui(self.gAxisY))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()

		# ############################################################################
		def setZm(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gAxisZ -= self.gStep
				self.oAxisZE.setText(MagicPanels.unit2gui(self.gAxisZ))
				
				self.showJoints()
			
			except:
				self.resetInfoScreen()
			
		def setZp(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gAxisZ += self.gStep
				self.oAxisZE.setText(MagicPanels.unit2gui(self.gAxisZ))
				
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
				self.gAxisX = MagicPanels.unit2value(self.oAxisXE.text())
				self.gAxisY = MagicPanels.unit2value(self.oAxisYE.text())
				self.gAxisZ = MagicPanels.unit2value(self.oAxisZE.text())
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())

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
				self.gDepth = MagicPanels.unit2value(self.oFxDepthE.text())
				
				if self.gObj3Face != "":
					
					t3 = MagicPanels.getColor(self.gObj3, 0, "trans", "RGBA")
					
					[ self.gObj3, self.gObj3Face ] = MagicPanels.makeMortise(self.gLink, self.gDepth, self.gObj3, self.gObj3Face)
					self.gObj3FaceIndex = MagicPanels.getFaceIndex(self.gObj3, self.gObj3Face)
					
					n = ""
					n += str(self.gObj3.Label)
					n += ", "
					n += "Face"
					n += str(self.gObj3FaceIndex)
					self.ob3S.setText(n)
					
					MagicPanels.setColor(self.gObj3, 0, t3, "trans", "RGBA")
					
				else:
					t2 = MagicPanels.getColor(self.gObj2, 0, "trans", "RGBA")
				
					[ self.gObj2, self.gObj2Face ] = MagicPanels.makeMortise(self.gLink, self.gDepth, self.gObj2, self.gObj2Face)
					self.gObj2FaceIndex = MagicPanels.getFaceIndex(self.gObj2, self.gObj2Face)
				
					n = ""
					n += str(self.gObj2.Label)
					n += ", "
					n += "Face"
					n += str(self.gObj2FaceIndex)
					self.ob2S.setText(n)
					
					MagicPanels.setColor(self.gObj2, 0, t2, "trans", "RGBA")
				
			except:
				self.resetInfoScreen()
				
		def setTenon(self):
			
			try:
				self.gDepth = MagicPanels.unit2value(self.oFxDepthE.text())
				t2 = MagicPanels.getColor(self.gObj2, 0, "trans", "RGBA")
				
				[ self.gObj2, self.gObj2Face ] = MagicPanels.makeTenon(self.gLink, self.gDepth, self.gObj2, self.gObj2Face)
				self.gObj2FaceIndex = MagicPanels.getFaceIndex(self.gObj2, self.gObj2Face)
				
				n = ""
				n += str(self.gObj2.Label)
				n += ", "
				n += "Face"
				n += str(self.gObj2FaceIndex)
				self.ob2S.setText(n)
				
				MagicPanels.setColor(self.gObj2, 0, t2, "trans", "RGBA")
				
			except:
				self.resetInfoScreen()
		
		def setJoints(self):
			
			try:

				self.gDepth = MagicPanels.unit2value(self.oFxDepthE.text())
				
				t2 = MagicPanels.getColor(self.gObj2, 0, "trans", "RGBA")
				t3 = MagicPanels.getColor(self.gObj3, 0, "trans", "RGBA")
				
				[ self.gObj2, self.gObj2Face ] = MagicPanels.makeTenon(self.gLink, self.gDepth, self.gObj2, self.gObj2Face)
				self.gObj2FaceIndex = MagicPanels.getFaceIndex(self.gObj2, self.gObj2Face)
				
				[ self.gObj3, self.gObj3Face ] = MagicPanels.makeMortise(self.gLink, self.gDepth, self.gObj3, self.gObj3Face)
				self.gObj3FaceIndex = MagicPanels.getFaceIndex(self.gObj3, self.gObj3Face)
				
				self.refreshInfoScreens()
			
				MagicPanels.setColor(self.gObj2, 0, t2, "trans", "RGBA")
				MagicPanels.setColor(self.gObj3, 0, t3, "trans", "RGBA")
		
			except:
				self.resetInfoScreen()
		
		# ############################################################################
		def setCornerM(self):

			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				if s - 1 < 0:
					FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(0)
				else:
					FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s-1)
					self.gCornerCross = s-1
			except:
				skip = 1
			
		def setCornerP(self):

			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s+1)
				self.gCornerCross = s+1
			except:
				skip = 1
		
		def setCenterOn(self):
			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
				self.gAxisCross = True
			except:
				skip = 1
			
		def setCenterOff(self):

			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(False)
				self.gAxisCross = False
			except:
				skip = 1
		
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		
		if not form.kccscb.isChecked():

			if form.gAxisCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(form.gAxisCrossOrig)
				
			if form.gCornerCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(form.gCornerCrossOrig)

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
