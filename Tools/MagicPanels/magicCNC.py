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
		
		gNoSelection = translate('magicCNC', 'select face to drill and drill bit')
		
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
			toolSH = 350
			
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
			self.setWindowTitle(translate('magicCNC', 'magicCNC'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			# screen
			info = ""
			info += "                                             "
			info += "                                             "
			info += "                                             "
			
			self.s1S1 = QtGui.QLabel(info, self)
			self.s1S1.move(10, 10)
			
			self.s1S2 = QtGui.QLabel(info, self)
			self.s1S2.move(10, 30)
			
			self.s1S = QtGui.QLabel(info, self)
			self.s1S.move(10, 30)
			
			row = 50

			# button
			self.s1B1 = QtGui.QPushButton(translate('magicCNC', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(toolSW-20)
			self.s1B1.move(10, row)

			# ############################################################################
			# options - changed axes
			# ############################################################################

			self.OPTlayout = QtGui.QVBoxLayout()
			self.OPTlayout.setAlignment(QtGui.Qt.AlignTop)

			# ############################################################################
			# options - X axis
			# ############################################################################

			# label
			self.o1L = QtGui.QLabel(translate('magicCNC', 'Move along X:'), self)
			self.o1L.move(10, row+3)
			self.o1L.hide()
			
			# button
			self.o1B1 = QtGui.QPushButton("<", self)
			self.o1B1.clicked.connect(self.setX1)
			self.o1B1.setFixedWidth(50)
			self.o1B1.move(105, row)
			self.o1B1.setAutoRepeat(True)
			self.o1B1.hide()
			
			# button
			self.o1B2 = QtGui.QPushButton(">", self)
			self.o1B2.clicked.connect(self.setX2)
			self.o1B2.setFixedWidth(50)
			self.o1B2.move(160, row)
			self.o1B2.setAutoRepeat(True)
			self.o1B2.hide()
			
			# ############################################################################
			# options - Y axis
			# ############################################################################

			# label
			self.o2L = QtGui.QLabel(translate('magicCNC', 'Move along Y:'), self)
			self.o2L.move(10, row+3)
			self.o2L.hide()
			
			# button
			self.o2B1 = QtGui.QPushButton("<", self)
			self.o2B1.clicked.connect(self.setY1)
			self.o2B1.setFixedWidth(50)
			self.o2B1.move(105, row)
			self.o2B1.setAutoRepeat(True)
			self.o2B1.hide()
			
			# button
			self.o2B2 = QtGui.QPushButton(">", self)
			self.o2B2.clicked.connect(self.setY2)
			self.o2B2.setFixedWidth(50)
			self.o2B2.move(160, row)
			self.o2B2.setAutoRepeat(True)
			self.o2B2.hide()
			
			# ############################################################################
			# options - Z axis
			# ############################################################################

			# label
			self.o3L = QtGui.QLabel(translate('magicCNC', 'Move along Z:'), self)
			self.o3L.move(10, row+3)
			self.o3L.hide()
			
			# button
			self.o3B1 = QtGui.QPushButton("<", self)
			self.o3B1.clicked.connect(self.setZ1)
			self.o3B1.setFixedWidth(50)
			self.o3B1.move(105, row)
			self.o3B1.setAutoRepeat(True)
			self.o3B1.hide()
			
			# button
			self.o3B2 = QtGui.QPushButton(">", self)
			self.o3B2.clicked.connect(self.setZ2)
			self.o3B2.setFixedWidth(50)
			self.o3B2.move(160, row)
			self.o3B2.setAutoRepeat(True)
			self.o3B2.hide()
			
			# ############################################################################
			# options - additional
			# ############################################################################

			row += 30
			self.gAxisRow1 = row
			
			row += 30
			self.gAxisRow2 = row

			row += 30
			
			# label
			self.o4L = QtGui.QLabel(translate('magicCNC', 'Move step:'), self)
			self.o4L.move(10, row+3)

			# text input
			self.o4E = QtGui.QLineEdit(self)
			self.o4E.setText(str(self.gStep))
			self.o4E.setFixedWidth(50)
			self.o4E.move(105, row)

			# ############################################################################
			# options - manually move
			# ############################################################################
			
			row += 30
			
			# label
			self.o5L = QtGui.QLabel(translate('magicCNC', 'Transform:'), self)
			self.o5L.move(10, row+3)
			
			# button
			self.o5B1 = QtGui.QPushButton(translate('magicCNC', 'on'), self)
			self.o5B1.clicked.connect(self.setEditModeON)
			self.o5B1.setFixedWidth(50)
			self.o5B1.move(105, row)

			# button
			self.o5B2 = QtGui.QPushButton(translate('magicCNC', 'off'), self)
			self.o5B2.clicked.connect(self.setEditModeOFF)
			self.o5B2.setFixedWidth(50)
			self.o5B2.move(160, row)

			# ############################################################################
			# options - corner cross
			# ############################################################################

			row += 40

			# label
			self.o6L = QtGui.QLabel(translate('magicCNC', 'Corner cross:'), self)
			self.o6L.move(10, row+3)

			# button
			self.o6B1 = QtGui.QPushButton("-", self)
			self.o6B1.clicked.connect(self.setCornerM)
			self.o6B1.setFixedWidth(50)
			self.o6B1.move(105, row)
			self.o6B1.setAutoRepeat(True)
			
			# button
			self.o6B2 = QtGui.QPushButton("+", self)
			self.o6B2.clicked.connect(self.setCornerP)
			self.o6B2.setFixedWidth(50)
			self.o6B2.move(160, row)
			self.o6B2.setAutoRepeat(True)

			# ############################################################################
			# options - center cross
			# ############################################################################

			row += 30

			# label
			self.o7L = QtGui.QLabel(translate('magicCNC', 'Center cross:'), self)
			self.o7L.move(10, row+3)

			# button
			self.o7B1 = QtGui.QPushButton(translate('magicCNC', 'on'), self)
			self.o7B1.clicked.connect(self.setCenterOn)
			self.o7B1.setFixedWidth(50)
			self.o7B1.move(105, row)
			self.o7B1.setAutoRepeat(True)
			
			# button
			self.o7B2 = QtGui.QPushButton(translate('magicCNC', 'off'), self)
			self.o7B2.clicked.connect(self.setCenterOff)
			self.o7B2.setFixedWidth(50)
			self.o7B2.move(160, row)
			self.o7B2.setAutoRepeat(True)

			# ############################################################################
			# options - drilling
			# ############################################################################

			row += 40

			# button
			self.o8B1 = QtGui.QPushButton(translate('magicCNC', 'drill below drill bit'), self)
			self.o8B1.clicked.connect(self.runDriller)
			self.o8B1.setFixedWidth(toolSW-20)
			self.o8B1.setFixedHeight(40)
			self.o8B1.move(10, row)
			
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
			
			self.s1S1.setText("")
			self.s1S2.setText("")
			self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def hideAxis(self):
			
			plane = MagicPanels.getFacePlane(self.gDrillFace)
			
			if plane == "XY":
				
				self.o1L.show()
				self.o1B1.show()
				self.o1B2.show()
				
				self.o1L.move(10, self.gAxisRow1+3)
				self.o1B1.move(105, self.gAxisRow1)
				self.o1B2.move(160, self.gAxisRow1)
				
				self.o2L.show()
				self.o2B1.show()
				self.o2B2.show()
				
				self.o2L.move(10, self.gAxisRow2+3)
				self.o2B1.move(105, self.gAxisRow2)
				self.o2B2.move(160, self.gAxisRow2)
				
				self.o3L.hide()
				self.o3B1.hide()
				self.o3B2.hide()
				
			if plane == "XZ":
				
				self.o1L.show()
				self.o1B1.show()
				self.o1B2.show()
				
				self.o1L.move(10, self.gAxisRow1+3)
				self.o1B1.move(105, self.gAxisRow1)
				self.o1B2.move(160, self.gAxisRow1)
				
				self.o2L.hide()
				self.o2B1.hide()
				self.o2B2.hide()

				self.o3L.show()
				self.o3B1.show()
				self.o3B2.show()
				
				self.o3L.move(10, self.gAxisRow2+3)
				self.o3B1.move(105, self.gAxisRow2)
				self.o3B2.move(160, self.gAxisRow2)

			if plane == "YZ":

				self.o1L.hide()
				self.o1B1.hide()
				self.o1B2.hide()

				self.o2L.show()
				self.o2B1.show()
				self.o2B2.show()
				
				self.o2L.move(10, self.gAxisRow1+3)
				self.o2B1.move(105, self.gAxisRow1)
				self.o2B2.move(160, self.gAxisRow1)
				
				self.o3L.show()
				self.o3B1.show()
				self.o3B2.show()
				
				self.o3L.move(10, self.gAxisRow2+3)
				self.o3B1.move(105, self.gAxisRow2)
				self.o3B2.move(160, self.gAxisRow2)
	

		# ############################################################################
		def getSelected(self):

			try:

				self.gObj = FreeCADGui.Selection.getSelection()[0]
				self.gDrillFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gDrillBit = FreeCADGui.Selection.getSelection()[1]
				
				face = "Face"+str(MagicPanels.getFaceIndex(self.gObj, self.gDrillFace))
				self.s1S1.setText(str(self.gObj.Label)+", "+face)
				self.s1S2.setText(str(self.gDrillBit.Label))
				self.s1S.setText("")
				
				self.o4E.setText(str(self.gStep))
				
				FreeCADGui.Selection.clearSelection()
				
				self.hideAxis()
				
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(50)
			
			except:

				self.resetInfoScreen()
				return -1
			
			
		# ############################################################################
		def setCornerM(self):
			
			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				if s - 1 < 0:
					FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(0)
				else:
					FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s-1)

			except:
				self.resetInfoScreen()
			
		def setCornerP(self):
			
			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s+1)
					
			except:
				self.resetInfoScreen()
		
		# ############################################################################
		def setCenterOn(self):
			
			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			except:
				self.resetInfoScreen()
			
		def setCenterOff(self):
			
			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(False)
			except:
				self.resetInfoScreen()
				
		# ############################################################################
		def setX1(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Xm")
			except:
				self.resetInfoScreen()
			
		def setX2(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Xp")
			except:
				self.resetInfoScreen()
			
		def setY1(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Ym")
			except:
				self.resetInfoScreen()
		
		def setY2(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Yp")
			except:
				self.resetInfoScreen()

		def setZ1(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Zm")
			except:
				self.resetInfoScreen()
		
		def setZ2(self):
			
			try:
				self.gStep = float(self.o4E.text())
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
				
				else:
					holes = MagicPanels.makeHoles(self.gObj, self.gDrillFace, o )

				# get new object from selection
				FreeCADGui.Selection.addSelection(holes[0])
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				
				# search for selected face to drill
				index = MagicPanels.getFaceIndexByKey(self.gObj, self.gDrillFaceKey)
				self.gDrillFace = self.gObj.Shape.Faces[index]

				# update status info screen
				face = "Face"+str(MagicPanels.getFaceIndex(self.gObj, self.gDrillFace))
				self.s1S1.setText(str(self.gObj.Label)+", "+face)
				
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
		try:
			FreeCADGui.ActiveDocument.ActiveView.setAxisCross(False)
			FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(10)
		except:
			skip = 1
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
