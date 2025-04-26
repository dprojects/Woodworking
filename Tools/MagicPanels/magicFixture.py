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
			toolSH = 620
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 0 + 200
			gPH = int( gSH - toolSH )

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
			
			# set grid
			row = 10
			
			area = toolSW - 20
			btsize = 50                                    # button size
			btoffset = 5                                   # button offset
			bc1 = area - (2 * btsize) - btoffset + 5       # button column 1
			bc2 = area - btsize + btoffset + 5             # button column 2
			
			col1 = 100
			col2 = 155
			col3 = 240
			
			# looks funny but if you resize screen you have the long string
			info = ""
			info += "                                             "
			info += "                                             "
			info += "                                             "
			
			# ############################################################################
			# options - selection mode
			# ############################################################################
		
			# label
			self.oi1L = QtGui.QLabel(translate('magicFixture', 'Fixture:'), self)
			self.oi1L.move(10, row+3)
			
			# label
			self.ob1S = QtGui.QLabel(info, self)
			self.ob1S.move(60, row+3)
			
			row += 20
			
			# label
			self.oi2L = QtGui.QLabel(translate('magicFixture', 'Anchor:'), self)
			self.oi2L.move(10, row+3)

			# label
			self.ob2S = QtGui.QLabel(info, self)
			self.ob2S.move(60, row+3)
			
			row += 20
			
			# button
			self.s1B1 = QtGui.QPushButton(translate('magicFixture', 'refresh selections'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(area)
			self.s1B1.setFixedHeight(40)
			self.s1B1.move(10, row)

			# ############################################################################
			# options - select edge
			# ############################################################################

			row += 50

			# label
			self.s2L = QtGui.QLabel(translate('magicFixture', 'Anchor:'), self)
			self.s2L.move(10, row+3)

			# button
			self.s2B1 = QtGui.QPushButton("<", self)
			self.s2B1.clicked.connect(self.setReferenceP)
			self.s2B1.setFixedWidth(50)
			self.s2B1.move(col1, row)
			self.s2B1.setAutoRepeat(True)
			
			# info screen
			self.s2IS = QtGui.QLabel("                                         ", self)
			self.s2IS.move(col2, row+3)

			# button
			self.s2B2 = QtGui.QPushButton(">", self)
			self.s2B2.clicked.connect(self.setReferenceN)
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
			info = ""
			info += "                                                           "
			info += "                                                           "
			info += "                                                           "
			self.s4IS = QtGui.QLabel(info, self)
			self.s4IS.move(col2, row+3)
			
			# button
			self.s4B2 = QtGui.QPushButton(">", self)
			self.s4B2.clicked.connect(self.setRoAnglesN)
			self.s4B2.setFixedWidth(50)
			self.s4B2.move(col3, row)
			self.s4B2.setAutoRepeat(True)

			# ############################################################################
			# options - add reference
			# ############################################################################

			row += 30
			
			# button
			self.oAddRefB = QtGui.QPushButton(translate('magicFixture', 'add selected anchor'), self)
			self.oAddRefB.clicked.connect(self.addReference)
			self.oAddRefB.setFixedWidth(area)
			self.oAddRefB.setFixedHeight(40)
			self.oAddRefB.move(10, row)

			# ############################################################################
			# options - offset from edge
			# ############################################################################

			row += 50
			
			# label
			self.oOffsetXL = QtGui.QLabel(translate('magicFixture', 'X offset:'), self)
			self.oOffsetXL.move(10, row+3)

			# button
			self.oOffsetXB1 = QtGui.QPushButton("-", self)
			self.oOffsetXB1.clicked.connect(self.setOffsetXP)
			self.oOffsetXB1.setFixedWidth(50)
			self.oOffsetXB1.move(col1, row)
			self.oOffsetXB1.setAutoRepeat(True)

			# text input
			self.oOffsetXE = QtGui.QLineEdit(self)
			self.oOffsetXE.setText(MagicPanels.unit2gui(self.gOffsetX))
			self.oOffsetXE.setFixedWidth(80)
			self.oOffsetXE.move(col2, row)

			# button
			self.oOffsetXB2 = QtGui.QPushButton("+", self)
			self.oOffsetXB2.clicked.connect(self.setOffsetXN)
			self.oOffsetXB2.setFixedWidth(50)
			self.oOffsetXB2.move(col3, row)
			self.oOffsetXB2.setAutoRepeat(True)

			# ############################################################################
			# options - offset from corner
			# ############################################################################

			row += 30
			
			# label
			self.oOffsetYL = QtGui.QLabel(translate('magicFixture', 'Y offset:'), self)
			self.oOffsetYL.move(10, row+3)

			# button
			self.oOffsetYB1 = QtGui.QPushButton("-", self)
			self.oOffsetYB1.clicked.connect(self.setOffsetYP)
			self.oOffsetYB1.setFixedWidth(50)
			self.oOffsetYB1.move(col1, row)
			self.oOffsetYB1.setAutoRepeat(True)

			# text input
			self.oOffsetYE = QtGui.QLineEdit(self)
			self.oOffsetYE.setText(MagicPanels.unit2gui(self.gOffsetY))
			self.oOffsetYE.setFixedWidth(80)
			self.oOffsetYE.move(col2, row)

			# button
			self.oOffsetYB2 = QtGui.QPushButton("+", self)
			self.oOffsetYB2.clicked.connect(self.setOffsetYN)
			self.oOffsetYB2.setFixedWidth(50)
			self.oOffsetYB2.move(col3, row)
			self.oOffsetYB2.setAutoRepeat(True)

			# ############################################################################
			# options - sink
			# ############################################################################

			row += 30

			# label
			self.oOffsetZL = QtGui.QLabel(translate('magicFixture', 'Z offset:'), self)
			self.oOffsetZL.move(10, row+3)

			# button
			self.oOffsetZB1 = QtGui.QPushButton("-", self)
			self.oOffsetZB1.clicked.connect(self.setOffsetZP)
			self.oOffsetZB1.setFixedWidth(50)
			self.oOffsetZB1.move(col1, row)
			self.oOffsetZB1.setAutoRepeat(True)
			
			# text input
			self.oOffsetZE = QtGui.QLineEdit(self)
			self.oOffsetZE.setText(MagicPanels.unit2gui(self.gOffsetZ))
			self.oOffsetZE.setFixedWidth(80)
			self.oOffsetZE.move(col2, row)
			
			# button
			self.oOffsetZB2 = QtGui.QPushButton("+", self)
			self.oOffsetZB2.clicked.connect(self.setOffsetZN)
			self.oOffsetZB2.setFixedWidth(50)
			self.oOffsetZB2.move(col3, row)
			self.oOffsetZB2.setAutoRepeat(True)

			# ############################################################################
			# options - step
			# ############################################################################

			row += 30

			# label
			self.oFxStepL = QtGui.QLabel(translate('magicFixture', 'Step:'), self)
			self.oFxStepL.move(10, row+3)

			# text input
			self.oFxStepE = QtGui.QLineEdit(self)
			self.oFxStepE.setText(MagicPanels.unit2gui(self.gStep))
			self.oFxStepE.setFixedWidth(80)
			self.oFxStepE.move(col2, row)
			
			# ############################################################################
			# options - set custom button
			# ############################################################################

			row += 30

			# button
			self.e1B1 = QtGui.QPushButton(translate('magicFixture', 'show custom settings'), self)
			self.e1B1.clicked.connect(self.refreshSettings)
			self.e1B1.setFixedWidth(area)
			self.e1B1.setFixedHeight(40)
			self.e1B1.move(10, row)

			# ############################################################################
			# options - transform command
			# ############################################################################

			row += 50

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

			row += 70

			# radio buttons
			
			self.rb1 = QtGui.QRadioButton(self)
			self.rb1.setText(translate('magicFixture', 'Link'))
			self.rb1.toggled.connect(self.selectRadioButton1)
			self.rb1.move(10, row)

			self.rb2 = QtGui.QRadioButton(self)
			self.rb2.setText(translate('magicFixture', 'Clone for drilling'))
			self.rb2.toggled.connect(self.selectRadioButton2)
			self.rb2.move(80, row)

			row += 30

			# apply button
			self.e3B1 = QtGui.QPushButton(translate('magicFixture', 'create'), self)
			self.e3B1.clicked.connect(self.setFixture)
			self.e3B1.setFixedWidth(area)
			self.e3B1.setFixedHeight(40)
			self.e3B1.move(10, row)

			# ############################################################################
			# GUI for common foot (visible by default)
			# ############################################################################
			
			row = toolSH - 90
			
			if self.gCornerCrossSupport == True:
			
				# label
				self.cocL = QtGui.QLabel(translate('magicFixture', 'Corner cross:'), self)
				self.cocL.move(10, row+3)

				# button
				self.cocB1 = QtGui.QPushButton("-", self)
				self.cocB1.clicked.connect(self.setCornerM)
				self.cocB1.setFixedWidth(btsize)
				self.cocB1.move(bc1, row)
				self.cocB1.setAutoRepeat(True)
				
				# button
				self.cocB2 = QtGui.QPushButton("+", self)
				self.cocB2.clicked.connect(self.setCornerP)
				self.cocB2.setFixedWidth(btsize)
				self.cocB2.move(bc2, row)
				self.cocB2.setAutoRepeat(True)

			if self.gAxisCrossSupport == True:
				
				row += 30
				
				# label
				self.cecL = QtGui.QLabel(translate('magicFixture', 'Center cross:'), self)
				self.cecL.move(10, row+3)

				# button
				self.cecB1 = QtGui.QPushButton(translate('magicFixture', 'on'), self)
				self.cecB1.clicked.connect(self.setCenterOn)
				self.cecB1.setFixedWidth(btsize)
				self.cecB1.move(bc1, row)
				self.cecB1.setAutoRepeat(True)
				
				# button
				self.cecB2 = QtGui.QPushButton(translate('magicFixture', 'off'), self)
				self.cecB2.clicked.connect(self.setCenterOff)
				self.cecB2.setFixedWidth(btsize)
				self.cecB2.move(bc2, row)
				self.cecB2.setAutoRepeat(True)

			if self.gCornerCrossSupport == True or self.gAxisCrossSupport == True:
				
				row += 25
				
				self.kccscb = QtGui.QCheckBox(translate('magicFixture', ' - keep custom cross settings'), self)
				self.kccscb.setCheckState(QtCore.Qt.Unchecked)
				self.kccscb.move(10, row+3)

			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()
			
			# init axis cross
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

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def resetInfoScreen(self):
			self.ob1S.setText(translate('magicFixture', 'select fixture container to apply'))
			self.ob2S.setText(translate('magicFixture', 'select face, edge, hole or vertex'))
			
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
		def getSelected(self):

			try:
				# ############################################################################
				# init settings
				# ############################################################################
				
				self.resetGlobals()
				
				# fixture
				self.gFixture = FreeCADGui.Selection.getSelection()[0]
				self.ob1S.setText(str(self.gFixture.Label))
				
				# anchor
				obj = FreeCADGui.Selection.getSelection()[1]
				sub = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
			
				if sub.ShapeType == "Edge":

					if sub.Curve.isDerivedFrom("Part::GeomLine"):
						[ v1, v2 ] = MagicPanels.getEdgeVectors(sub)
						
						self.gVectorArr.append(v1)
						self.gVectorObj.append(obj)
						
						self.gVectorArr.append(v2)
						self.gVectorObj.append(obj)
						
						self.gVectorArr.append(sub.CenterOfMass)
						self.gVectorObj.append(obj)

					elif sub.Curve.isDerivedFrom("Part::GeomCircle"):
						self.gVectorArr.append(sub.Curve.Center)
						self.gVectorObj.append(obj)

				if sub.ShapeType == "Face":
					
					vectors = MagicPanels.getFaceVertices(sub, "vector")
					self.gVectorArr += vectors
					for i in range(0, len(vectors)):
						self.gVectorObj.append(obj)
					
					self.gVectorArr.append(sub.CenterOfMass)
					self.gVectorObj.append(obj)

				if sub.ShapeType == "Vertex":
					self.gVectorArr.append(FreeCAD.Vector(sub.X, sub.Y, sub.Z))
					self.gVectorObj.append(obj)
				
				self.gVectorIndex = 0
				self.gVectorCurrent = self.gVectorArr[self.gVectorIndex]
				self.ob2S.setText(str(self.gVectorCurrent))
				
				FreeCADGui.Selection.clearSelection()
				
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
				
				self.rb1.setChecked(True)
				self.showFixture()

			except:

				self.resetInfoScreen()
				return -1
		
		# ############################################################################
		def addReference(self):
			
			try:
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
			
				if sub.ShapeType == "Edge":

					if sub.Curve.isDerivedFrom("Part::GeomLine"):
						[ v1, v2 ] = MagicPanels.getEdgeVectors(sub)
						
						self.gVectorArr.append(v1)
						self.gVectorObj.append(obj)
						
						self.gVectorArr.append(v2)
						self.gVectorObj.append(obj)
						
						self.gVectorArr.append(sub.CenterOfMass)
						self.gVectorObj.append(obj)

					elif sub.Curve.isDerivedFrom("Part::GeomCircle"):
						self.gVectorArr.append(sub.Curve.Center)
						self.gVectorObj.append(obj)

				if sub.ShapeType == "Face":
					
					vectors = MagicPanels.getFaceVertices(sub, "vector")
					self.gVectorArr += vectors
					for i in range(0, len(vectors)):
						self.gVectorObj.append(obj)
						
					self.gVectorArr.append(sub.CenterOfMass)
					self.gVectorObj.append(obj)

				if sub.ShapeType == "Vertex":
					self.gVectorArr.append(FreeCAD.Vector(sub.X, sub.Y, sub.Z))
					self.gVectorObj.append(obj)
				
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
				self.ob2S.setText(str(self.gVectorCurrent))
				
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
				self.ob2S.setText(str(self.gVectorCurrent))
				
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
				self.s1S.setText(self.gNoSelection)
			
		def setCornerP(self):

			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s+1)
				self.gCornerCross = s+1
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def setCenterOn(self):
			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
				self.gAxisCross = True
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setCenterOff(self):

			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(False)
				self.gAxisCross = False
			except:
				self.s1S.setText(self.gNoSelection)
		
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
		def setFixture(self):

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
