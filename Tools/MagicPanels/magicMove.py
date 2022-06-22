import FreeCAD, FreeCADGui 
import Draft
from PySide import QtGui, QtCore

import MagicPanels


# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals
		# ############################################################################

		gObj = ""
		gStep = 1
		gNoSelection = "select panel to move"
		
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
			toolSH = 280
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 0
			gPH = int( gSH - toolSH )

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle("magicMove")
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			# screen
			info = ""
			info += "                                             "
			info += "                                             "
			info += "                                             "
			self.s1S = QtGui.QLabel(info, self)
			self.s1S.move(10, 10)

			# button
			self.s1B1 = QtGui.QPushButton("refresh selection", self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(200)
			self.s1B1.move(10, 40)

			# ############################################################################
			# options - X axis
			# ############################################################################

			# label
			self.o1L = QtGui.QLabel("Move along X:", self)
			self.o1L.move(10, 83)

			# button
			self.o1B1 = QtGui.QPushButton("<", self)
			self.o1B1.clicked.connect(self.setX1)
			self.o1B1.setFixedWidth(50)
			self.o1B1.move(105, 80)
			self.o1B1.setAutoRepeat(True)
			
			# button
			self.o1B2 = QtGui.QPushButton(">", self)
			self.o1B2.clicked.connect(self.setX2)
			self.o1B2.setFixedWidth(50)
			self.o1B2.move(160, 80)
			self.o1B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - Y axis
			# ############################################################################

			# label
			self.o2L = QtGui.QLabel("Move along Y:", self)
			self.o2L.move(10, 113)

			# button
			self.o2B1 = QtGui.QPushButton("<", self)
			self.o2B1.clicked.connect(self.setY1)
			self.o2B1.setFixedWidth(50)
			self.o2B1.move(105, 110)
			self.o2B1.setAutoRepeat(True)
			
			# button
			self.o2B2 = QtGui.QPushButton(">", self)
			self.o2B2.clicked.connect(self.setY2)
			self.o2B2.setFixedWidth(50)
			self.o2B2.move(160, 110)
			self.o2B2.setAutoRepeat(True)

			# ############################################################################
			# options - Z axis
			# ############################################################################

			# label
			self.o3L = QtGui.QLabel("Move along Z:", self)
			self.o3L.move(10, 143)

			# button
			self.o3B1 = QtGui.QPushButton("<", self)
			self.o3B1.clicked.connect(self.setZ1)
			self.o3B1.setFixedWidth(50)
			self.o3B1.move(105, 140)
			self.o3B1.setAutoRepeat(True)
			
			# button
			self.o3B2 = QtGui.QPushButton(">", self)
			self.o3B2.clicked.connect(self.setZ2)
			self.o3B2.setFixedWidth(50)
			self.o3B2.move(160, 140)
			self.o3B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - additional
			# ############################################################################

			# label
			self.o4L = QtGui.QLabel("Move step:", self)
			self.o4L.move(10, 173)

			# text input
			self.o4E = QtGui.QLineEdit(self)
			self.o4E.setText(str(self.gStep))
			self.o4E.setFixedWidth(50)
			self.o4E.move(105, 170)

			# ############################################################################
			# options - corner cross
			# ############################################################################

			# label
			self.o0L = QtGui.QLabel("Corner cross:", self)
			self.o0L.move(10, 213)

			# button
			self.o0B1 = QtGui.QPushButton("<", self)
			self.o0B1.clicked.connect(self.setCornerM)
			self.o0B1.setFixedWidth(50)
			self.o0B1.move(105, 210)
			self.o0B1.setAutoRepeat(True)
			
			# button
			self.o0B2 = QtGui.QPushButton(">", self)
			self.o0B2.clicked.connect(self.setCornerP)
			self.o0B2.setFixedWidth(50)
			self.o0B2.move(160, 210)
			self.o0B2.setAutoRepeat(True)

			# ############################################################################
			# options - center cross
			# ############################################################################

			# label
			self.o0L = QtGui.QLabel("Center cross:", self)
			self.o0L.move(10, 243)

			# button
			self.o0B1 = QtGui.QPushButton("on", self)
			self.o0B1.clicked.connect(self.setCenterOn)
			self.o0B1.setFixedWidth(50)
			self.o0B1.move(105, 240)
			self.o0B1.setAutoRepeat(True)
			
			# button
			self.o0B2 = QtGui.QPushButton("off", self)
			self.o0B2.clicked.connect(self.setCenterOff)
			self.o0B2.setFixedWidth(50)
			self.o0B2.move(160, 240)
			self.o0B2.setAutoRepeat(True)
			
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

			[ x, y, z ] = MagicPanels.convertPosition(self.gObj, x, y, z)
			
			[ px, py, pz, r ] = MagicPanels.getPlacement(self.gObj)
			MagicPanels.setPlacement(self.gObj, px+x, py+y, pz+z, r)

			FreeCAD.activeDocument().recompute()

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def getSelected(self):

			try:

				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(50)

				self.gObj = MagicPanels.getReference()
				
				sizes = []
				sizes = MagicPanels.getSizes(self.gObj)
				sizes.sort()
				self.gStep = sizes[0]
				self.o4E.setText(str(self.gStep))
				
				self.s1S.setText(str(self.gObj.Label))
				FreeCADGui.Selection.clearSelection()
				
			except:

				self.s1S.setText(self.gNoSelection)
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
				self.s1S.setText(self.gNoSelection)
			
		def setCornerP(self):
			
			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s+1)
					
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def setCenterOn(self):
			
			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setCenterOff(self):
			
			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(False)
			except:
				self.s1S.setText(self.gNoSelection)
				
		# ############################################################################
		def setX1(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Xm")
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setX2(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Xp")
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setY1(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Ym")
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setY2(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Yp")
			except:
				self.s1S.setText(self.gNoSelection)

		def setZ1(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Zm")
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setZ2(self):
			
			try:
				self.gStep = float(self.o4E.text())
				self.setMove("Zp")
			except:
				self.s1S.setText(self.gNoSelection)

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
