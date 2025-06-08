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

		gDrillBit = ""
		gDrillFace = ""
		
		gDrillFaceKey = ""
		
		gAxisRow1 = 0
		gAxisRow2 = 0

		gObj = ""
		gStep = 9
		
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
			toolSW = 350
			toolSH = 500
			
			cutLabel = toolSW - 80
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 0 + 100
			gPH = int( gSH - toolSH ) - 30

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicCNC', 'magicCNC'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			self.oFaceB = QtGui.QPushButton(translate('magicCNC', 'set'), self)
			self.oFaceB.clicked.connect(self.setFace)
			self.oFaceB.setFixedWidth(50)
			
			self.oFaceL = QtGui.QLabel("", self)
			self.oFaceL.setFixedWidth(cutLabel)
			
			self.oBitB = QtGui.QPushButton(translate('magicCNC', 'set'), self)
			self.oBitB.clicked.connect(self.setDrillBit)
			self.oBitB.setFixedWidth(50)
			
			self.oBitL = QtGui.QLabel("", self)
			self.oBitL.setFixedWidth(cutLabel)

			# button
			self.s1B1 = QtGui.QPushButton(translate('magicCNC', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedHeight(40)

			# ############################################################################
			# options - X axis
			# ############################################################################

			# label
			self.o1L = QtGui.QLabel(translate('magicCNC', 'Move along X:'), self)
			
			# button
			self.o1B1 = QtGui.QPushButton("-", self)
			self.o1B1.clicked.connect(self.setX1)
			self.o1B1.setFixedWidth(50)
			self.o1B1.setAutoRepeat(True)
			
			# button
			self.o1B2 = QtGui.QPushButton("+", self)
			self.o1B2.clicked.connect(self.setX2)
			self.o1B2.setFixedWidth(50)
			self.o1B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - Y axis
			# ############################################################################

			# label
			self.o2L = QtGui.QLabel(translate('magicCNC', 'Move along Y:'), self)
			
			# button
			self.o2B1 = QtGui.QPushButton("-", self)
			self.o2B1.clicked.connect(self.setY1)
			self.o2B1.setFixedWidth(50)
			self.o2B1.setAutoRepeat(True)
			
			# button
			self.o2B2 = QtGui.QPushButton("+", self)
			self.o2B2.clicked.connect(self.setY2)
			self.o2B2.setFixedWidth(50)
			self.o2B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - Z axis
			# ############################################################################

			# label
			self.o3L = QtGui.QLabel(translate('magicCNC', 'Move along Z:'), self)
			
			# button
			self.o3B1 = QtGui.QPushButton("-", self)
			self.o3B1.clicked.connect(self.setZ1)
			self.o3B1.setFixedWidth(50)
			self.o3B1.setAutoRepeat(True)
			
			# button
			self.o3B2 = QtGui.QPushButton("+", self)
			self.o3B2.clicked.connect(self.setZ2)
			self.o3B2.setFixedWidth(50)
			self.o3B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - additional
			# ############################################################################

			# label
			self.o4L = QtGui.QLabel(translate('magicCNC', 'Move step:'), self)

			# text input
			self.o4E = QtGui.QLineEdit(self)
			self.o4E.setText(MagicPanels.unit2gui(self.gStep))

			# ############################################################################
			# options - transform command
			# ############################################################################

			# button
			self.e2B1 = QtGui.QPushButton(translate('magicCNC', 'set manually'), self)
			self.e2B1.clicked.connect(self.setEditModeON)
			self.e2B1.setFixedHeight(40)

			# button
			self.e2B2 = QtGui.QPushButton(translate('magicCNC', 'finish manually'), self)
			self.e2B2.clicked.connect(self.setEditModeOFF)
			self.e2B2.setFixedHeight(40)

			# ############################################################################
			# options - drilling
			# ############################################################################

			# button
			self.o8B1 = QtGui.QPushButton(translate('magicCNC', 'create'), self)
			self.o8B1.clicked.connect(self.runDriller)
			self.o8B1.setFixedHeight(40)

			# ############################################################################
			# GUI for common foot
			# ############################################################################
			
			if self.gCornerCrossSupport == True:
			
				# label
				self.cocL = QtGui.QLabel(translate('magicCNC', 'Corner cross:'), self)

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
				self.cecL = QtGui.QLabel(translate('magicCNC', 'Center cross:'), self)

				# button
				self.cecB1 = QtGui.QPushButton(translate('magicCNC', 'on'), self)
				self.cecB1.clicked.connect(self.setCenterOn)
				self.cecB1.setFixedWidth(50)
				self.cecB1.setAutoRepeat(True)
				
				# button
				self.cecB2 = QtGui.QPushButton(translate('magicCNC', 'off'), self)
				self.cecB2.clicked.connect(self.setCenterOff)
				self.cecB2.setFixedWidth(50)
				self.cecB2.setAutoRepeat(True)

			if self.gCornerCrossSupport == True or self.gAxisCrossSupport == True:

				self.kccscb = QtGui.QCheckBox(translate('magicCNC', ' - keep custom cross settings'), self)
				self.kccscb.setCheckState(QtCore.Qt.Unchecked)
	
			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.row1 = QtGui.QHBoxLayout()
			self.row1.addWidget(self.oFaceB)
			self.row1.addWidget(self.oFaceL)
			
			self.row2 = QtGui.QHBoxLayout()
			self.row2.addWidget(self.oBitB)
			self.row2.addWidget(self.oBitL)
			
			self.row3 = QtGui.QHBoxLayout()
			self.row3.addWidget(self.s1B1)
			
			self.rowBody1 = QtGui.QHBoxLayout()
			self.rowBody1.addWidget(self.o1L)
			self.rowBody1.addWidget(self.o1B1)
			self.rowBody1.addWidget(self.o1B2)
			self.rowBody2 = QtGui.QHBoxLayout()
			self.rowBody2.addWidget(self.o2L)
			self.rowBody2.addWidget(self.o2B1)
			self.rowBody2.addWidget(self.o2B2)
			self.rowBody3 = QtGui.QHBoxLayout()
			self.rowBody3.addWidget(self.o3L)
			self.rowBody3.addWidget(self.o3B1)
			self.rowBody3.addWidget(self.o3B2)
			self.rowBody4 = QtGui.QHBoxLayout()
			self.rowBody4.addWidget(self.o4L)
			self.rowBody4.addStretch()
			self.rowBody4.addWidget(self.o4E)
			self.rowBody5 = QtGui.QHBoxLayout()
			self.rowBody5.addWidget(self.e2B1)
			self.rowBody5.addWidget(self.e2B2)
			
			self.layCB = QtGui.QHBoxLayout()
			self.layCB.addWidget(self.o8B1)
			
			self.layBody1 = QtGui.QVBoxLayout()
			self.layBody1.addLayout(self.rowBody1)
			self.layBody1.addLayout(self.rowBody2)
			self.layBody1.addLayout(self.rowBody3)
			self.layBody1.addLayout(self.rowBody4)
			self.layBody1.addSpacing(20)
			self.layBody1.addLayout(self.rowBody5)
			
			self.groupBody1 = QtGui.QGroupBox(None, self)
			self.groupBody1.setLayout(self.layBody1)
			
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
			self.layout.addLayout(self.layCB)
			self.layout.addStretch()
			self.layout.addLayout(self.layoutFoot)
			self.setLayout(self.layout)
			
			self.o1L.hide()
			self.o1B1.hide()
			self.o1B2.hide()
			self.o2L.hide()
			self.o2B1.hide()
			self.o2B2.hide()
			self.o3L.hide()
			self.o3B1.hide()
			self.o3B2.hide()

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
		def setMove(self, iType):
			
			x = 0
			y = 0
			z = 0
			
			if iType == "Xp":
				x = self.gStep
			
			if iType == "Xm":
				x = - self.gStep

			if iType == "Yp":
				y = self.gStep

			if iType == "Ym":
				y = - self.gStep

			if iType == "Zp":
				z = self.gStep

			if iType == "Zm":
				z = - self.gStep

			[ x, y, z ] = MagicPanels.convertPosition(self.gDrillBit, x, y, z)
			
			[ px, py, pz, r ] = MagicPanels.getPlacement(self.gDrillBit)
			MagicPanels.setPlacement(self.gDrillBit, px+x, py+y, pz+z, r)

			FreeCAD.activeDocument().recompute()

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		def resetInfoScreen(self):
			
			self.oFaceL.setText(translate('magicCNC', 'select face to drill'))
			self.oBitL.setText(translate('magicCNC', 'select drill bit'))

		# ############################################################################
		def hideAxis(self):
			
			plane = MagicPanels.getFacePlane(self.gDrillFace)
			
			if plane == "XY":
				
				self.o1L.show()
				self.o1B1.show()
				self.o1B2.show()
				
				self.o2L.show()
				self.o2B1.show()
				self.o2B2.show()
				
				self.o3L.hide()
				self.o3B1.hide()
				self.o3B2.hide()

			if plane == "XZ":
				
				self.o1L.show()
				self.o1B1.show()
				self.o1B2.show()
				
				self.o2L.hide()
				self.o2B1.hide()
				self.o2B2.hide()
				
				self.o3L.show()
				self.o3B1.show()
				self.o3B2.show()

			if plane == "YZ":
				
				self.o1L.hide()
				self.o1B1.hide()
				self.o1B2.hide()
				
				self.o2L.show()
				self.o2B1.show()
				self.o2B2.show()
				
				self.o3L.show()
				self.o3B1.show()
				self.o3B2.show()

		# ############################################################################
		def setFace(self):

			try:
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				self.gDrillFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				face = "Face"+str(MagicPanels.getFaceIndex(self.gObj, self.gDrillFace))
				self.oFaceL.setText(str(self.gObj.Label)+", "+face)

				if self.gDrillBit != "":
					self.hideAxis()
				
				self.o4E.setText(MagicPanels.unit2gui(self.gStep))
				FreeCADGui.Selection.clearSelection()
				
			except:
				self.oFaceL.setText(translate('magicCNC', 'select face to drill'))
				self.gDrillFace = ""
		
		
		# ############################################################################
		def setDrillBit(self):

			try:
				self.gDrillBit = FreeCADGui.Selection.getSelection()[0]
				self.oBitL.setText(str(self.gDrillBit.Label))
				
				if self.gDrillFace != "":
					self.hideAxis()
				
				self.o4E.setText(MagicPanels.unit2gui(self.gStep))
				FreeCADGui.Selection.clearSelection()

			except:
				self.oBitL.setText(translate('magicCNC', 'select drill bit'))
				self.gDrillBit = ""
		
		# ############################################################################
		def getSelected(self):

			try:
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				self.gDrillFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gDrillBit = FreeCADGui.Selection.getSelection()[1]
				
				face = "Face"+str(MagicPanels.getFaceIndex(self.gObj, self.gDrillFace))
				self.oFaceL.setText(str(self.gObj.Label)+", "+face)
				self.oBitL.setText(str(self.gDrillBit.Label))
				
				self.o4E.setText(MagicPanels.unit2gui(self.gStep))
				FreeCADGui.Selection.clearSelection()
				self.hideAxis()

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
		def setX1(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.o4E.text())
				self.setMove("Xm")
			except:
				self.resetInfoScreen()
			
		def setX2(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.o4E.text())
				self.setMove("Xp")
			except:
				self.resetInfoScreen()
			
		def setY1(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.o4E.text())
				self.setMove("Ym")
			except:
				self.resetInfoScreen()
		
		def setY2(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.o4E.text())
				self.setMove("Yp")
			except:
				self.resetInfoScreen()

		def setZ1(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.o4E.text())
				self.setMove("Zm")
			except:
				self.resetInfoScreen()
		
		def setZ2(self):
			
			try:
				self.gStep = MagicPanels.unit2value(self.o4E.text())
				self.setMove("Zp")
			except:
				self.resetInfoScreen()

		# ############################################################################
		def setEditModeON(self):
			
			try:
				vo = self.gDrillBit.ViewObject
				vo.Document.setEdit(vo, 1)
				
			except:
				self.resetInfoScreen()
		
		def setEditModeOFF(self):
			
			try:
				vo = self.gDrillBit.ViewObject
				vo.Document.resetEdit()
				
			except:
				self.resetInfoScreen()

		# ############################################################################
		def runDriller(self):
			
			try:
			
				# store face key to find face to drill at new object later
				self.gDrillFaceKey = self.gDrillFace.BoundBox
				
				# set args
				s = self.gDrillBit.Label
				o = []
				o.append(self.gDrillBit)
				
				# drilling selection
				
				if s.find("countersink") != -1:
					holes = MagicPanels.makeCountersinks(self.gObj, self.gDrillFace, o )
				
				elif s.find("counterbore") != -1:
					holes = MagicPanels.makeCounterbores(self.gObj, self.gDrillFace, o )
					
				elif s.find("2 sides") != -1:
					holes = MagicPanels.makeCounterbores2x(self.gObj, self.gDrillFace, o )
				
				else:
					holes = MagicPanels.makeHoles(self.gObj, self.gDrillFace, o )

				# get new object from selection
				if s.find("2 sides") != -1:
					FreeCADGui.Selection.addSelection(holes[1])
				else:
					FreeCADGui.Selection.addSelection(holes[0])
					
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				
				# search for selected face to drill
				index = MagicPanels.getFaceIndexByKey(self.gObj, self.gDrillFaceKey)
				self.gDrillFace = self.gObj.Shape.Faces[index-1]

				# update status info screen
				face = "Face"+str(MagicPanels.getFaceIndex(self.gObj, self.gDrillFace))
				self.oFaceL.setText(str(self.gObj.Label)+", "+face)
				
				# remove selection
				FreeCADGui.Selection.clearSelection()
			
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
