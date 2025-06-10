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

		gFixture = ""
		
		gVectorCurrent = ""
		gVectorObj = []
		gVectorArr = []
		gVectorIndex = 0

		gRoAxisArr = []
		gRoAxis = ""
		
		gRoAnglesArr = []
		gRoAngles = ""
		gRoIndex = 0
		
		gStep = 10
		gLink = ""
		
		gOffsetX = 0
		gOffsetY = 0
		gOffsetZ = 0
		
		gNoSelection = translate('magicFixture', 'please select fixture object and face')
		
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
			toolSW = 300
			toolSH = 650
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 0 + 200
			gPH = 50

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicFixture', 'magicFixture'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - settings
			# ############################################################################
			
			area = toolSW - 20
			cutLabel = toolSW - 80
			btsize = 50                                    # button size
			btoffset = 5                                   # button offset
			bc1 = area - (2 * btsize) - btoffset + 5       # button column 1
			bc2 = area - btsize + btoffset + 5             # button column 2
			
			col1 = 100
			col2 = 155
			col3 = 240
			
			# ############################################################################
			# options - selection mode
			# ############################################################################
		
			# button
			self.oFixtureB = QtGui.QPushButton(translate('magicFixture', 'set'), self)
			self.oFixtureB.clicked.connect(self.setFixture)
			self.oFixtureB.setFixedWidth(50)
			
			# label
			self.oFixtureL = QtGui.QLabel("", self)
			self.oFixtureL.setFixedWidth(cutLabel)
			
			# button
			self.oAnchorB = QtGui.QPushButton(translate('magicFixture', 'set'), self)
			self.oAnchorB.clicked.connect(self.setAnchor)
			self.oAnchorB.setFixedWidth(50)
		
			# label
			self.oAnchorL = QtGui.QLabel("", self)
			self.oAnchorL.setFixedWidth(cutLabel)
			
			# button
			self.s1B1 = QtGui.QPushButton(translate('magicFixture', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedHeight(40)

			# ############################################################################
			# options - select edge
			# ############################################################################

			# label
			self.s2L = QtGui.QLabel(translate('magicFixture', 'Anchor:'), self)

			# button
			self.s2B1 = QtGui.QPushButton("<", self)
			self.s2B1.clicked.connect(self.setReferenceP)
			self.s2B1.setFixedWidth(50)
			self.s2B1.setAutoRepeat(True)
			
			# info screen
			self.s2IS = QtGui.QLabel("", self)

			# button
			self.s2B2 = QtGui.QPushButton(">", self)
			self.s2B2.clicked.connect(self.setReferenceN)
			self.s2B2.setFixedWidth(50)
			self.s2B2.setAutoRepeat(True)

			# ############################################################################
			# options - adjust rotation
			# ############################################################################

			# label
			self.s4L = QtGui.QLabel(translate('magicFixture', 'Rotation:'), self)

			# button
			self.s4B1 = QtGui.QPushButton("<", self)
			self.s4B1.clicked.connect(self.setRoAnglesP)
			self.s4B1.setFixedWidth(50)
			self.s4B1.setAutoRepeat(True)
			
			self.s4IS = QtGui.QLabel("", self)
			
			# button
			self.s4B2 = QtGui.QPushButton(">", self)
			self.s4B2.clicked.connect(self.setRoAnglesN)
			self.s4B2.setFixedWidth(50)
			self.s4B2.setAutoRepeat(True)

			# ############################################################################
			# options - add reference
			# ############################################################################

			# button
			self.oAddRefB = QtGui.QPushButton(translate('magicFixture', 'add selected anchor'), self)
			self.oAddRefB.clicked.connect(self.addReference)

			# ############################################################################
			# options - offset from edge
			# ############################################################################

			# label
			self.oOffsetXL = QtGui.QLabel(translate('magicFixture', 'X offset:'), self)

			# button
			self.oOffsetXB1 = QtGui.QPushButton("-", self)
			self.oOffsetXB1.clicked.connect(self.setOffsetXP)
			self.oOffsetXB1.setFixedWidth(50)
			self.oOffsetXB1.setAutoRepeat(True)

			# text input
			self.oOffsetXE = QtGui.QLineEdit(self)
			self.oOffsetXE.setText(MagicPanels.unit2gui(self.gOffsetX))
			self.oOffsetXE.setFixedWidth(80)

			# button
			self.oOffsetXB2 = QtGui.QPushButton("+", self)
			self.oOffsetXB2.clicked.connect(self.setOffsetXN)
			self.oOffsetXB2.setFixedWidth(50)
			self.oOffsetXB2.setAutoRepeat(True)

			# ############################################################################
			# options - offset from corner
			# ############################################################################

			# label
			self.oOffsetYL = QtGui.QLabel(translate('magicFixture', 'Y offset:'), self)

			# button
			self.oOffsetYB1 = QtGui.QPushButton("-", self)
			self.oOffsetYB1.clicked.connect(self.setOffsetYP)
			self.oOffsetYB1.setFixedWidth(50)
			self.oOffsetYB1.setAutoRepeat(True)

			# text input
			self.oOffsetYE = QtGui.QLineEdit(self)
			self.oOffsetYE.setText(MagicPanels.unit2gui(self.gOffsetY))
			self.oOffsetYE.setFixedWidth(80)

			# button
			self.oOffsetYB2 = QtGui.QPushButton("+", self)
			self.oOffsetYB2.clicked.connect(self.setOffsetYN)
			self.oOffsetYB2.setFixedWidth(50)
			self.oOffsetYB2.setAutoRepeat(True)

			# ############################################################################
			# options - sink
			# ############################################################################

			# label
			self.oOffsetZL = QtGui.QLabel(translate('magicFixture', 'Z offset:'), self)

			# button
			self.oOffsetZB1 = QtGui.QPushButton("-", self)
			self.oOffsetZB1.clicked.connect(self.setOffsetZP)
			self.oOffsetZB1.setFixedWidth(50)
			self.oOffsetZB1.setAutoRepeat(True)
			
			# text input
			self.oOffsetZE = QtGui.QLineEdit(self)
			self.oOffsetZE.setText(MagicPanels.unit2gui(self.gOffsetZ))
			self.oOffsetZE.setFixedWidth(80)
			
			# button
			self.oOffsetZB2 = QtGui.QPushButton("+", self)
			self.oOffsetZB2.clicked.connect(self.setOffsetZN)
			self.oOffsetZB2.setFixedWidth(50)
			self.oOffsetZB2.setAutoRepeat(True)

			# ############################################################################
			# options - step
			# ############################################################################

			# label
			self.oFxStepL = QtGui.QLabel(translate('magicFixture', 'Step:'), self)

			# text input
			self.oFxStepE = QtGui.QLineEdit(self)
			self.oFxStepE.setText(MagicPanels.unit2gui(self.gStep))
			self.oFxStepE.setFixedWidth(80)
			
			# ############################################################################
			# options - set custom button
			# ############################################################################

			# button
			self.e1B1 = QtGui.QPushButton(translate('magicFixture', 'show custom settings'), self)
			self.e1B1.clicked.connect(self.refreshSettings)

			# ############################################################################
			# options - transform command
			# ############################################################################

			# button
			self.e2B1 = QtGui.QPushButton(translate('magicFixture', 'set manually'), self)
			self.e2B1.clicked.connect(self.setEditModeON)

			# button
			self.e2B2 = QtGui.QPushButton(translate('magicFixture', 'finish manually'), self)
			self.e2B2.clicked.connect(self.setEditModeOFF)

			# ############################################################################
			# options - final save
			# ############################################################################

			# radio buttons
			
			self.rb1 = QtGui.QRadioButton(self)
			self.rb1.setText(translate('magicFixture', 'Link'))
			self.rb1.toggled.connect(self.selectRadioButton1)

			self.rb2 = QtGui.QRadioButton(self)
			self.rb2.setText(translate('magicFixture', 'Clone for drilling'))
			self.rb2.toggled.connect(self.selectRadioButton2)

			# apply button
			self.e3B1 = QtGui.QPushButton(translate('magicFixture', 'create'), self)
			self.e3B1.clicked.connect(self.createFixture)
			self.e3B1.setFixedHeight(40)

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
			self.row1.setAlignment(QtGui.Qt.AlignLeft)
			self.row1.addWidget(self.oFixtureB)
			self.row1.addWidget(self.oFixtureL)
			
			self.row2 = QtGui.QHBoxLayout()
			self.row2.setAlignment(QtGui.Qt.AlignLeft)
			self.row2.addWidget(self.oAnchorB)
			self.row2.addWidget(self.oAnchorL)
			
			self.row3 = QtGui.QHBoxLayout()
			self.row3.addWidget(self.s1B1)

			self.row4 = QtGui.QGridLayout()
			self.row4.addWidget(self.s2L, 0, 0)
			self.row4.addWidget(self.s2B1, 0, 1)
			self.row4.addWidget(self.s2IS, 0, 2)
			self.row4.addWidget(self.s2B2, 0, 3)
			self.row4.addWidget(self.s4L, 1, 0)
			self.row4.addWidget(self.s4B1, 1, 1)
			self.row4.addWidget(self.s4IS, 1, 2)
			self.row4.addWidget(self.s4B2, 1, 3)
			self.row5 = QtGui.QHBoxLayout()
			self.row5.addWidget(self.oAddRefB)
			self.rowBody1 = QtGui.QVBoxLayout()
			self.rowBody1.addLayout(self.row4)
			self.rowBody1.addLayout(self.row5)
			self.groupBody1 = QtGui.QGroupBox(None, self)
			self.groupBody1.setLayout(self.rowBody1)

			self.row6 = QtGui.QGridLayout()
			self.row6.addWidget(self.oOffsetXL, 0, 0)
			self.row6.addWidget(self.oOffsetXB1, 0, 1)
			self.row6.addWidget(self.oOffsetXE, 0, 2)
			self.row6.addWidget(self.oOffsetXB2, 0, 3)
			self.row6.addWidget(self.oOffsetYL, 1, 0)
			self.row6.addWidget(self.oOffsetYB1, 1, 1)
			self.row6.addWidget(self.oOffsetYE, 1, 2)
			self.row6.addWidget(self.oOffsetYB2, 1, 3)
			self.row6.addWidget(self.oOffsetZL, 2, 0)
			self.row6.addWidget(self.oOffsetZB1, 2, 1)
			self.row6.addWidget(self.oOffsetZE, 2, 2)
			self.row6.addWidget(self.oOffsetZB2, 2, 3)
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
			
			self.row9 = QtGui.QHBoxLayout()
			self.row9.addWidget(self.rb1)
			self.row9.addWidget(self.rb2)
			self.row10 = QtGui.QHBoxLayout()
			self.row10.addWidget(self.e3B1)
			self.rowBody3 = QtGui.QVBoxLayout()
			self.rowBody3.addLayout(self.row9)
			self.rowBody3.addSpacing(10)
			self.rowBody3.addLayout(self.row10)
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

			# show window
			self.show()
			
			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)

			if self.gAxisCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			
			if self.gCornerCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(50)
			
			# init
			self.getSelected()

		# ############################################################################
		# actions - internal functions
		# ############################################################################

		# ############################################################################
		def setRotation(self):
			
			angle = self.gRoAnglesArr[self.gRoIndex]
			axis = FreeCAD.Vector(self.gRoAxis)

			self.gLink.Placement.Rotation = FreeCAD.Rotation(axis, angle)
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def showFixture(self, iType="show"):
			
			# set info
			
			info = str(self.gVectorIndex + 1) + " / " + str(len(self.gVectorArr))
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
			v = self.gVectorArr[self.gVectorIndex]
			[ v ] = MagicPanels.getVerticesOffset([ v ], self.gVectorObj[self.gVectorIndex], "vector")
			
			# ############################################################################
			# set link
			# ############################################################################
			
			X, Y, Z = v.x, v.y, v.z
			x, y, z = 0, 0, 0

			# ############################################################################
			# choose object type to set
			# ############################################################################

			if self.rb1.isChecked() == True:
				linkName = "Link_" + str(self.gFixture.Name)
				link = FreeCAD.activeDocument().addObject('App::Link', linkName)
				link.setLink(self.gFixture)
				link.Label = "Link, " + self.gFixture.Label + " "

			if self.rb2.isChecked() == True:
				import Draft
				link = Draft.make_clone(self.gFixture)
				link.Label = "Clone, " + self.gFixture.Label + " "

			# ############################################################################
			# set object into position
			# ############################################################################

			x = X + self.gOffsetX
			y = Y + self.gOffsetY
			z = Z + self.gOffsetZ	
			
			# final set
			link.Placement.Base.x = x
			link.Placement.Base.y = y
			link.Placement.Base.z = z
			
			self.gLink = link
			
			# ############################################################################
			# set rotation
			# ############################################################################

			self.setRotation()
			FreeCADGui.Selection.clearSelection()
			
		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def resetInfoScreen(self):
			self.oFixtureL.setText(translate('magicFixture', 'fixture to apply'))
			self.oAnchorL.setText(translate('magicFixture', 'face, edge, hole or vertex'))
			
		# ############################################################################
		def resetGlobals(self):

			self.gFixture = ""
			
			self.gVectorObj = []
			self.gVectorArr = []
			self.gVectorIndex = 0
			self.gVectorCurrent = ""
		
			self.gRoAxisArr = []
			self.gRoAxis = ""
		
			self.gRoAnglesArr = []
			self.gRoAngles = ""
		
			self.gRoIndex = 0

		# ############################################################################
		def createAnchor(self, iObj, iSub):

			if iSub.ShapeType == "Edge":

				if iSub.Curve.isDerivedFrom("Part::GeomLine"):
					[ v1, v2 ] = MagicPanels.getEdgeVectors(iSub)
					
					self.gVectorArr.append(v1)
					self.gVectorObj.append(iObj)
					
					self.gVectorArr.append(v2)
					self.gVectorObj.append(iObj)
					
					self.gVectorArr.append(iSub.CenterOfMass)
					self.gVectorObj.append(iObj)

				elif iSub.Curve.isDerivedFrom("Part::GeomCircle"):
					self.gVectorArr.append(iSub.Curve.Center)
					self.gVectorObj.append(iObj)

			if iSub.ShapeType == "Face":
				
				vectors = MagicPanels.getFaceVertices(iSub, "vector")
				self.gVectorArr += vectors
				for i in range(0, len(vectors)):
					self.gVectorObj.append(iObj)
					
				self.gVectorArr.append(iSub.CenterOfMass)
				self.gVectorObj.append(iObj)

			if iSub.ShapeType == "Vertex":
				self.gVectorArr.append(FreeCAD.Vector(iSub.X, iSub.Y, iSub.Z))
				self.gVectorObj.append(iObj)

		# ############################################################################
		def getSelected(self):

			try:
				
				# init
				self.resetGlobals()
				self.rb1.setChecked(True)
				
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
				
				self.gRoAnglesArr.append(240)
				self.gRoAxisArr.append([-0.58, 0.58, -0.58])
				
				self.gRoAnglesArr.append(120)
				self.gRoAxisArr.append([-0.58, -0.58, 0.58])
				
				self.gRoAnglesArr.append(120)
				self.gRoAxisArr.append([0.58, 0.58, 0.58])
				
				self.gRoAnglesArr.append(120)
				self.gRoAxisArr.append([0.58, -0.58, -0.58])
				
				self.gRoAnglesArr.append(180)
				self.gRoAxisArr.append([0.58, 0.58, -0.58])
				
				self.gRoAnglesArr.append(270)
				self.gRoAxisArr.append([0.58, 0.58, -0.58])
				
				self.gRoAnglesArr.append(120)
				self.gRoAxisArr.append([-0.58, 0.58, 0.58])

				self.gRoAnglesArr.append(180)
				self.gRoAxisArr.append([0, 0.71, 0.71])
				
				# X and Y axis
				self.gRoAnglesArr.append(0)
				self.gRoAxisArr.append([1, 1, 0])
				
				self.gRoAnglesArr.append(90)
				self.gRoAxisArr.append([1, 1, 0])
				
				self.gRoAnglesArr.append(180)
				self.gRoAxisArr.append([1, 1, 0])
				
				self.gRoAnglesArr.append(270)
				self.gRoAxisArr.append([1, 1, 0])
				
				# X and Z axis
				self.gRoAnglesArr.append(0)
				self.gRoAxisArr.append([1, 0, 1])
				
				self.gRoAnglesArr.append(90)
				self.gRoAxisArr.append([1, 0, 1])
				
				self.gRoAnglesArr.append(180)
				self.gRoAxisArr.append([1, 0, 1])
				
				self.gRoAnglesArr.append(270)
				self.gRoAxisArr.append([1, 0, 1])
				
				# Y and Z axis
				self.gRoAnglesArr.append(0)
				self.gRoAxisArr.append([0, 1, 1])
				
				self.gRoAnglesArr.append(90)
				self.gRoAxisArr.append([0, 1, 1])
				
				self.gRoAnglesArr.append(180)
				self.gRoAxisArr.append([0, 1, 1])
				
				self.gRoAnglesArr.append(270)
				self.gRoAxisArr.append([0, 1, 1])
			
				# init
				self.gRoAngles = self.gRoAnglesArr[0]
				self.gRoAxis = self.gRoAxisArr[0]
				
				# ############################################################################
				# read objects
				# ############################################################################
				
				# fixture
				self.gFixture = FreeCADGui.Selection.getSelection()[0]
				self.oFixtureL.setText(str(self.gFixture.Label))
				
				# anchor
				obj = FreeCADGui.Selection.getSelection()[1]
				sub = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				self.createAnchor(obj, sub)
				
				self.gVectorIndex = 0
				self.gVectorCurrent = self.gVectorArr[self.gVectorIndex]
				self.oAnchorL.setText(str(self.gVectorCurrent))
				
				FreeCADGui.Selection.clearSelection()
				
				# ############################################################################
				# show fixture if everything was fine
				# ############################################################################
				
				self.showFixture()

			except:

				self.resetInfoScreen()
				return -1
		
		# ############################################################################
		def setFixture(self):
			
			try:
				self.gFixture = FreeCADGui.Selection.getSelection()[0]
				self.oFixtureL.setText(str(self.gFixture.Label))
				
				FreeCADGui.Selection.clearSelection()

				if self.gFixture != "" and self.gVectorCurrent != "":
					self.showFixture()
			
			except:
			
				self.oFixtureL.setText(translate('magicFixture', 'fixture to apply'))
		
		# ############################################################################
		def setAnchor(self):
			
			try:
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				self.gVectorObj = []
				self.gVectorArr = []
				self.gVectorIndex = 0
				self.gVectorCurrent = ""
				
				self.createAnchor(obj, sub)
					
				self.gVectorIndex = 0
				self.gVectorCurrent = self.gVectorArr[self.gVectorIndex]
				self.oAnchorL.setText(str(self.gVectorCurrent))
				
				FreeCADGui.Selection.clearSelection()
				
				if self.gFixture != "" and self.gVectorCurrent != "":
					self.showFixture()
				
			except:
				self.oAnchorL.setText(translate('magicFixture', 'face, edge, hole or vertex'))

		# ############################################################################
		def addReference(self):
			
			try:
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
			
				self.createAnchor(obj, sub)
				
				FreeCADGui.Selection.clearSelection()
				self.showFixture()
				
			except:
				skip = 1
		
		# ############################################################################
		def setReferenceP(self):

			try:
				if self.gVectorIndex - 1 < 0:
					self.gVectorIndex = len(self.gVectorArr) - 1
				else:
					self.gVectorIndex = self.gVectorIndex - 1
					
				self.gVectorCurrent = self.gVectorArr[self.gVectorIndex]
				self.oAnchorL.setText(str(self.gVectorCurrent))
				
				self.showFixture()
			
			except:
				self.resetInfoScreen()
			
		def setReferenceN(self):

			try:
				if self.gVectorIndex + 1 > len(self.gVectorArr) - 1:
					self.gVectorIndex = 0
				else:
					self.gVectorIndex = self.gVectorIndex + 1
					
				self.gVectorCurrent = self.gVectorArr[self.gVectorIndex]
				self.oAnchorL.setText(str(self.gVectorCurrent))
				
				self.showFixture()
			
			except:
				self.resetInfoScreen()

		# ############################################################################
		def setOffsetXP(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gOffsetX -= self.gStep
				self.oOffsetXE.setText(MagicPanels.unit2gui(self.gOffsetX))
				
				self.showFixture()
			
			except:
				self.resetInfoScreen()
			
		def setOffsetXN(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gOffsetX += self.gStep
				self.oOffsetXE.setText(MagicPanels.unit2gui(self.gOffsetX))
				
				self.showFixture()
			
			except:
				self.resetInfoScreen()

		# ############################################################################
		def setOffsetYP(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gOffsetY -= self.gStep
				self.oOffsetYE.setText(MagicPanels.unit2gui(self.gOffsetY))
				
				self.showFixture()
			
			except:
				self.resetInfoScreen()
			
		def setOffsetYN(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gOffsetY += self.gStep
				self.oOffsetYE.setText(MagicPanels.unit2gui(self.gOffsetY))
				
				self.showFixture()
			
			except:
				self.resetInfoScreen()

		# ############################################################################
		def setOffsetZP(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
			
				self.gOffsetZ -= self.gStep
				self.oOffsetZE.setText(MagicPanels.unit2gui(self.gOffsetZ))
				
				self.showFixture()
			
			except:
				self.resetInfoScreen()
			
		def setOffsetZN(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())
				
				self.gOffsetZ += self.gStep
				self.oOffsetZE.setText(MagicPanels.unit2gui(self.gOffsetZ))
				
				self.showFixture()
			
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
				
				self.showFixture()
			
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
				
				self.showFixture()
			
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
		def refreshSettings(self):
			
			try:
			
				self.gOffsetZ = MagicPanels.unit2value(self.oOffsetZE.text())
				self.gOffsetY = MagicPanels.unit2value(self.oOffsetYE.text())
				self.gOffsetX = MagicPanels.unit2value(self.oOffsetXE.text())
				self.gStep = MagicPanels.unit2value(self.oFxStepE.text())

				self.showFixture()
			
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
		def selectRadioButton1(self, selected):
			try:
				if selected:
					self.showFixture()
			except:
				self.resetInfoScreen()
		
		def selectRadioButton2(self, selected):
			try:
				if selected:
					self.showFixture()
			except:
				self.resetInfoScreen()
				
		# ############################################################################
		def createFixture(self):

			self.gLink = ""
		
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
				
		if not form.kccscb.isChecked():

			if form.gAxisCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(form.gAxisCrossOrig)
				
			if form.gCornerCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(form.gCornerCrossOrig)

		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
