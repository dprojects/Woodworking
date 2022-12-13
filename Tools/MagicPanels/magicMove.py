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
		
		gModeType = "Move"
		gCopyType = "copyObject"
		
		gInfoMoveX = translate('magicMove', 'Move along X:')
		gInfoMoveY = translate('magicMove', 'Move along Y:')
		gInfoMoveZ = translate('magicMove', 'Move along Z:')
		gInfoMoveStep = translate('magicMove', 'Move step:')

		gInfoCopyX = translate('magicMove', 'Copy along X:')
		gInfoCopyY = translate('magicMove', 'Copy along Y:')
		gInfoCopyZ = translate('magicMove', 'Copy along Z:')
		gInfoCopyStep = translate('magicMove', 'Copy offset:')

		gInfoMirrorX = translate('magicMove', 'Mirror along X:')
		gInfoMirrorY = translate('magicMove', 'Mirror along Y:')
		gInfoMirrorZ = translate('magicMove', 'Mirror along Z:')
		gInfoMirrorStep = translate('magicMove', 'Mirror offset:')
		
		gObj = ""
		gThick = 0
		gStep = 1

		gMaxX = 0
		gMaxY = 0
		gMaxZ = 0
		
		gLCPX = 0 # Last Copy Position X
		gLCPY = 0 # Last Copy Position Y
		gLCPZ = 0 # Last Copy Position Z
		gLCPR = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00) # Last Copy Position Rotation
		
		gCrossCorner = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
		gCrossCenter = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()

		gNoSelection = translate('magicMove', 'select panel or container')
		
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
			toolSH = 330
			
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
			self.setWindowTitle(translate('magicMove', 'magicMove'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			row = 10
			
			# screen
			info = ""
			info += "                                             "
			info += "                                             "
			info += "                                             "
			self.s1S = QtGui.QLabel(info, self)
			self.s1S.move(10, row)

			row += 30

			# button
			self.s1B1 = QtGui.QPushButton(translate('magicMove', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(200)
			self.s1B1.setFixedHeight(40)
			self.s1B1.move(10, row)

			# ############################################################################
			# options - mode selector
			# ############################################################################
			
			row += 50
			
			self.sModeList = (
						"Move",
						"Copy",
						"Mirror"
						)
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(self.sModeList.index("Move"))
			self.sMode.activated[str].connect(self.setModeType)
			self.sMode.setFixedWidth(80)
			self.sMode.move(10, row)

			self.sCopyTypeList = (
						"copyObject",
						"Clone",
						"Link"
						)
			
			self.sCopyType = QtGui.QComboBox(self)
			self.sCopyType.addItems(self.sCopyTypeList)
			self.sCopyType.setCurrentIndex(self.sCopyTypeList.index("copyObject"))
			self.sCopyType.activated[str].connect(self.setCopyType)
			self.sCopyType.setFixedWidth(105)
			self.sCopyType.move(105, row)
			self.sCopyType.hide()
			
			# ############################################################################
			# options - X axis
			# ############################################################################

			row += 40

			# label
			self.o1L = QtGui.QLabel(self.gInfoMoveX, self)
			self.o1L.move(10, row+3)

			# button
			self.o1B1 = QtGui.QPushButton("X-", self)
			self.o1B1.clicked.connect(self.setX1)
			self.o1B1.setFixedWidth(50)
			self.o1B1.move(105, row)
			self.o1B1.setAutoRepeat(True)
			
			# button
			self.o1B2 = QtGui.QPushButton("X+", self)
			self.o1B2.clicked.connect(self.setX2)
			self.o1B2.setFixedWidth(50)
			self.o1B2.move(160, row)
			self.o1B2.setAutoRepeat(True)

			# ############################################################################
			# options - Y axis
			# ############################################################################

			row += 30

			# label
			self.o2L = QtGui.QLabel(self.gInfoMoveY, self)
			self.o2L.move(10, row+3)

			# button
			self.o2B1 = QtGui.QPushButton("Y-", self)
			self.o2B1.clicked.connect(self.setY1)
			self.o2B1.setFixedWidth(50)
			self.o2B1.move(105, row)
			self.o2B1.setAutoRepeat(True)
			
			# button
			self.o2B2 = QtGui.QPushButton("Y+", self)
			self.o2B2.clicked.connect(self.setY2)
			self.o2B2.setFixedWidth(50)
			self.o2B2.move(160, row)
			self.o2B2.setAutoRepeat(True)

			# ############################################################################
			# options - Z axis
			# ############################################################################

			row += 30
			
			# label
			self.o3L = QtGui.QLabel(self.gInfoMoveZ, self)
			self.o3L.move(10, row+3)

			# button
			self.o3B1 = QtGui.QPushButton("Z-", self)
			self.o3B1.clicked.connect(self.setZ1)
			self.o3B1.setFixedWidth(50)
			self.o3B1.move(105, row)
			self.o3B1.setAutoRepeat(True)
			
			# button
			self.o3B2 = QtGui.QPushButton("Z+", self)
			self.o3B2.clicked.connect(self.setZ2)
			self.o3B2.setFixedWidth(50)
			self.o3B2.move(160, row)
			self.o3B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - additional
			# ############################################################################
			
			row += 30
			
			# label
			self.o4L = QtGui.QLabel(self.gInfoMoveStep+"               ", self)
			self.o4L.move(10, row+3)

			# text input
			self.o4E = QtGui.QLineEdit(self)
			self.o4E.setText(str(self.gStep))
			self.o4E.setFixedWidth(50)
			self.o4E.move(160, row)

			# ############################################################################
			# options - corner cross
			# ############################################################################

			row += 40
			
			# label
			self.o0L = QtGui.QLabel(translate('magicMove', 'Corner cross:'), self)
			self.o0L.move(10, row+3)

			# button
			self.o0B1 = QtGui.QPushButton("-", self)
			self.o0B1.clicked.connect(self.setCornerM)
			self.o0B1.setFixedWidth(50)
			self.o0B1.move(105, row)
			self.o0B1.setAutoRepeat(True)
			
			# button
			self.o0B2 = QtGui.QPushButton("+", self)
			self.o0B2.clicked.connect(self.setCornerP)
			self.o0B2.setFixedWidth(50)
			self.o0B2.move(160, row)
			self.o0B2.setAutoRepeat(True)

			# ############################################################################
			# options - center cross
			# ############################################################################
			
			row += 30
			
			# label
			self.o0L = QtGui.QLabel(translate('magicMove', 'Center cross:'), self)
			self.o0L.move(10, row+3)

			# button
			self.o0B1 = QtGui.QPushButton(translate('magicMove', 'on'), self)
			self.o0B1.clicked.connect(self.setCenterOn)
			self.o0B1.setFixedWidth(50)
			self.o0B1.move(105, row)
			self.o0B1.setAutoRepeat(True)
			
			# button
			self.o0B2 = QtGui.QPushButton(translate('magicMove', 'off'), self)
			self.o0B2.clicked.connect(self.setCenterOff)
			self.o0B2.setFixedWidth(50)
			self.o0B2.move(160, row)
			self.o0B2.setAutoRepeat(True)

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
		# actions - internal functions
		# ############################################################################

		# ############################################################################
		def resetGlobals(self):
			
			self.gMaxX = 0
			self.gMaxY = 0
			self.gMaxZ = 0
			
			self.gLCPX = 0
			self.gLCPY = 0
			self.gLCPZ = 0
			self.gLCPR = 0
		
		# ############################################################################
		def setLastPosition(self):
			
			if self.gObj.isDerivedFrom("Sketcher::SketchObject"):
				[ self.gLCPX, self.gLCPY, self.gLCPZ, self.gLCPR ] = MagicPanels.getSketchPlacement(self.gObj, "global")
			else:
				[ self.gLCPX, self.gLCPY, self.gLCPZ, self.gLCPR ] = MagicPanels.getPlacement(self.gObj)
		
		# ############################################################################
		def setMove(self, iType):
			
			self.gStep = float(self.o4E.text())
			
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
			
			if self.gObj.isDerivedFrom("Sketcher::SketchObject"):
				
				gp = self.gObj.getGlobalPlacement()
				px = gp.Base.x
				py = gp.Base.y
				pz = gp.Base.z
				r = gp.Rotation
			
			else:
				
				try:
					[ x, y, z ] = MagicPanels.convertPosition(self.gObj, x, y, z)
				except:
					skip = 1
				
				[ px, py, pz, r ] = MagicPanels.getPlacement(self.gObj)
			
			MagicPanels.setPlacement(self.gObj, px+x, py+y, pz+z, r)
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def createCopy(self, iType):
			
			self.gStep = float(self.o4E.text())
			
			if self.gCopyType == "copyObject":
				copy = FreeCAD.ActiveDocument.copyObject(self.gObj)
				copy.Label = "Copy, " + str(self.gObj.Label) + " "
			
			if self.gCopyType == "Clone":
				import Draft
				copy = Draft.make_clone(self.gObj)
				copy.Label = "Clone, " + str(self.gObj.Label) + " "
			
			if self.gCopyType == "Link":
				copyName = "Link_" + str(self.gObj.Name)
				copy = FreeCAD.ActiveDocument.addObject('App::Link', copyName)
				copy.setLink(self.gObj)
				copy.Label = "Link, " + str(self.gObj.Label) + " "
			
			x, y, z, r = self.gLCPX, self.gLCPY, self.gLCPZ, self.gLCPR
			
			if iType == "Xp":
				x = x + self.gMaxX + self.gStep
			
			if iType == "Xm":
				x = x - self.gMaxX - self.gStep

			if iType == "Yp":
				y = y + self.gMaxY + self.gStep

			if iType == "Ym":
				y = y - self.gMaxY - self.gStep

			if iType == "Zp":
				z = z + self.gMaxZ + self.gStep

			if iType == "Zm":
				z = z - self.gMaxX - self.gStep
			
			if copy.isDerivedFrom("Sketcher::SketchObject"):
				
				MagicPanels.setSketchPlacement(copy, x, y, z, r, "global")
				FreeCAD.ActiveDocument.recompute()
				[ self.gLCPX, self.gLCPY, self.gLCPZ, self.gLCPR ] = MagicPanels.getSketchPlacement(copy, "global")
			
			else:
			
				MagicPanels.setPlacement(copy, x, y, z, r)
				FreeCAD.ActiveDocument.recompute()
				[ self.gLCPX, self.gLCPY, self.gLCPZ, self.gLCPR ] = MagicPanels.getPlacement(copy)
			
			try:
				MagicPanels.copyColors(self.gObj, copy)
			except:
				skip = 1

		# ############################################################################
		def createMirror(self, iType):
			
			self.gStep = float(self.o4E.text())
			
			[ x, y, z, r ] = MagicPanels.getPlacement(self.gObj)
			mx, my, mz = 0, 0, 0
			
			if iType == "Xp":
				x = x + self.gMaxX
				mx = self.gStep
				direction = (1, 0, 0)
			
			if iType == "Xm":
				mx = - self.gStep
				direction = (1, 0, 0)
				
			if iType == "Yp":
				y = y + self.gMaxY
				my = self.gStep
				direction = (0, 1, 0)
				
			if iType == "Ym":
				my = - self.gStep
				direction = (0, 1, 0)

			if iType == "Zp":
				z = z + self.gMaxZ
				mz = self.gStep
				direction = (0, 0, 1)
				
			if iType == "Zm":
				mz = - self.gStep
				direction = (0, 0, 1)

			mirror = FreeCAD.ActiveDocument.addObject('Part::Mirroring', "mirror")
			mirror.Label = "Mirror, " + str(self.gObj.Label) + " "
			mirror.Source = FreeCAD.ActiveDocument.getObject(self.gObj.Name)
			mirror.Normal = direction
			mirror.Base = (x, y, z)
			
			FreeCAD.activeDocument().recompute()
			
			[ cx, cy, cz, r ] = MagicPanels.getPlacement(mirror)
			MagicPanels.setPlacement(mirror, cx+mx, cy+my, cz+mz, r)
			
			try:
				MagicPanels.copyColors(self.gObj, mirror)
			except:
				skip = 1
			
		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def getSelected(self):

			try:

				self.resetGlobals()
				
				self.gObj = MagicPanels.getReference()
				
				sizes = []
				sizes = MagicPanels.getSizes(self.gObj)
				sizes.sort()
				self.gStep = sizes[0]
				self.gThick = sizes[0]
				self.o4E.setText(str(self.gStep))
				
				self.s1S.setText(str(self.gObj.Label))
				FreeCADGui.Selection.clearSelection()
				
				[ self.gMaxX, self.gMaxY, self.gMaxZ ] = MagicPanels.getSizesFromVertices(self.gObj)
				self.setLastPosition()

			except:

				self.s1S.setText(self.gNoSelection)
				return -1
		
		def setModeType(self, selectedText):
			
			self.gModeType = selectedText
			
			if selectedText == "Move":
				self.o1L.setText(self.gInfoMoveX)
				self.o2L.setText(self.gInfoMoveY)
				self.o3L.setText(self.gInfoMoveZ)
				self.o4L.setText(self.gInfoMoveStep)
				self.sCopyType.hide()
				self.setLastPosition()

			if selectedText == "Copy":
				self.o1L.setText(self.gInfoCopyX)
				self.o2L.setText(self.gInfoCopyY)
				self.o3L.setText(self.gInfoCopyZ)
				self.o4L.setText(self.gInfoCopyStep)
				self.sCopyType.show()
				self.setLastPosition()

			if selectedText == "Mirror":
				self.o1L.setText(self.gInfoMirrorX)
				self.o2L.setText(self.gInfoMirrorY)
				self.o3L.setText(self.gInfoMirrorZ)
				self.o4L.setText(self.gInfoMirrorStep)
				self.sCopyType.hide()
				self.setLastPosition()

		def setCopyType(self, selectedText):
			
			self.gCopyType = selectedText
			
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
				if self.gModeType == "Move":
					self.setMove("Xm")
					
				if self.gModeType == "Copy":
					self.createCopy("Xm")
				
				if self.gModeType == "Mirror":
					self.createMirror("Xm")
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setX2(self):
			
			try:
				if self.gModeType == "Move":
					self.setMove("Xp")
					
				if self.gModeType == "Copy":
					self.createCopy("Xp")

				if self.gModeType == "Mirror":
					self.createMirror("Xp")
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setY1(self):
			
			try:
				if self.gModeType == "Move":
					self.setMove("Ym")
					
				if self.gModeType == "Copy":
					self.createCopy("Ym")
			
				if self.gModeType == "Mirror":
					self.createMirror("Ym")
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setY2(self):
			
			try:
				if self.gModeType == "Move":
					self.setMove("Yp")
					
				if self.gModeType == "Copy":
					self.createCopy("Yp")

				if self.gModeType == "Mirror":
					self.createMirror("Yp")
			except:
				self.s1S.setText(self.gNoSelection)

		def setZ1(self):
			
			try:
				if self.gModeType == "Move":
					self.setMove("Zm")
					
				if self.gModeType == "Copy":
					self.createCopy("Zm")
				
				if self.gModeType == "Mirror":
					self.createMirror("Zm")
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setZ2(self):
			
			try:
				if self.gModeType == "Move":
					self.setMove("Zp")
					
				if self.gModeType == "Copy":
					self.createCopy("Zp")
				
				if self.gModeType == "Mirror":
					self.createMirror("Zp")
			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		
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

		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
