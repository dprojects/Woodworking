import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# Global definitions
# ############################################################################

# add new items only at the end and change self.sModeList
getMenuIndex1 = {
	translate('magicMove', 'Move'): 0, 
	translate('magicMove', 'Copy'): 1, 
	translate('magicMove', 'Copy by Path'): 2, 
	translate('magicMove', 'Mirror'): 3, 
	translate('magicMove', 'Copy by Edge'): 4, 
	translate('magicMove', 'Move to Equal'): 5 # no comma 
}

# add new items only at the end and change self.sCopyTypeList
getMenuIndex2 = {
	translate('magicMove', 'copyObject'): 0, 
	translate('magicMove', 'Clone'): 1, 
	translate('magicMove', 'Link'): 2, 
	translate('magicMove', 'auto'): 3 # no comma 
}

# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals
		# ############################################################################
		
		gModeType = getMenuIndex1[translate('magicMove', 'Move')]
		gCopyType = getMenuIndex2[translate('magicMove', 'auto')]
		
		gInfoMoveX = translate('magicMove', 'Move along X:')
		gInfoMoveY = translate('magicMove', 'Move along Y:')
		gInfoMoveZ = translate('magicMove', 'Move along Z:')
		gInfoMoveStep = translate('magicMove', 'Move step:')

		gInfoCopyX = translate('magicMove', 'Copy along X:')
		gInfoCopyY = translate('magicMove', 'Copy along Y:')
		gInfoCopyZ = translate('magicMove', 'Copy along Z:')
		gInfoCopyStep = translate('magicMove', 'Copy offset:')

		gInfoPath1 = translate('magicMove', 'Rotation X, Y, Z:')
		gInfoPath2 = translate('magicMove', 'Next point step:')

		gNoSelection = translate('magicMove', 'select panel or container')
		gNoPathSelection = translate('magicMove', 'select copy path')
		gNoCopyByEdge = translate('magicMove', 'please select edge')
		gNoMirrorPoint = translate('magicMove', 'edge, face or vertex')
		gNoMEEdgeStart = translate('magicMove', 'select start edge')
		gNoMEEdgeEnd = translate('magicMove', 'select end edge')
		
		gObjects = ""
		
		gObj = ""
		gThick = 0
		gStep = 1

		gMaxX = 0
		gMaxY = 0
		gMaxZ = 0
		
		gLCPX = dict() # Last Copy Position X
		gLCPY = dict() # Last Copy Position Y
		gLCPZ = dict() # Last Copy Position Z
		gLCPR = dict() # Last Copy Position Rotation
		
		gNewContainerON = False
		gContainerRef = "root"
		
		gCrossCorner = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
		gCrossCenter = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()
		gCrossCornerOrig = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
		gCrossCenterOrig = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()

		gCopyPathObj = ""
		gCopyPathStep = 1
		gCopyPathPoints = []
		gCopyPathRotation = dict() # last rotation
		gCopyPathLast = dict() # last path position
		gCopyPathInit = dict() # if init from 0 or last selected panel
		
		# move to equal start
		gMTESObj = ""
		gMTESEdge = ""
		# move to equal end
		gMTEEObj = ""
		gMTEEEdge = ""
		
		# copy by edge
		gCBEObj = ""
		gCBEEdge = ""
		
		# mirror copy
		gMObj = ""
		gMSub = ""
		
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
			toolSW = 250
			toolSH = 420
			
			rside = toolSW - 20
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 0 + 200
			gPH = int( gSH - toolSH ) - 30

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicMove', 'magicMove'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# GUI for common selection part (visible by default)
			# ############################################################################

			row = 10
			
			# screen
			info = ""
			self.s1S = QtGui.QLabel(info, self)
			self.s1S.setFixedWidth(rside-10)
			self.s1S.move(10, row)

			row += 30

			# button
			self.s1B1 = QtGui.QPushButton(translate('magicMove', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(rside)
			self.s1B1.setFixedHeight(40)
			self.s1B1.move(10, row)

			row += 50
			
			# not write here, copy text from getMenuIndex1 to avoid typo
			self.sModeList = (
						translate('magicMove', 'Move'), # default
						translate('magicMove', 'Move to Equal'), 
						translate('magicMove', 'Copy'), 
						translate('magicMove', 'Copy by Edge'), 
						translate('magicMove', 'Copy by Path'), 
						translate('magicMove', 'Mirror')
						)
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(0) # default
			self.sMode.activated[str].connect(self.setModeType)
			self.sMode.setFixedWidth(125)
			self.sMode.move(10, row)

			# not write here, copy text from getMenuIndex2 to avoid typo
			self.sCopyTypeList = (
						translate('magicMove', 'auto'), # default
						translate('magicMove', 'copyObject'), 
						translate('magicMove', 'Clone'), 
						translate('magicMove', 'Link')
						)
			
			self.sCopyType = QtGui.QComboBox(self)
			self.sCopyType.addItems(self.sCopyTypeList)
			self.sCopyType.setCurrentIndex(0) # default
			self.sCopyType.activated[str].connect(self.setCopyType)
			self.sCopyType.setFixedWidth(95)
			self.sCopyType.move(rside - 85, row)
			self.sCopyType.hide()

			# ############################################################################
			# settigns for custom GUI
			# ############################################################################

			rowcbe = row
			rowmte = row
			rowmc = row
			rowpath = row + 70
			
			btsize = 50
			btoffset = 5
			cbt1 = rside - (2 * btsize) - btoffset + 5
			cbt2 = rside - btsize + btoffset + 5
	
			# ############################################################################
			# GUI for Move and Copy (visible for Move by default)
			# ############################################################################
			
			row += 30

			# button
			self.gNewContainerB1 = QtGui.QPushButton(translate('magicMove', 'copy to new container'), self)
			self.gNewContainerB1.clicked.connect(self.setNewContainer)
			self.gNewContainerB1.setFixedWidth(rside)
			self.gNewContainerB1.setFixedHeight(30)
			self.gNewContainerB1.move(10, row)
			self.gNewContainerB1.hide()

			row += 40

			# label
			self.o1L = QtGui.QLabel(self.gInfoMoveX, self)
			self.o1L.move(10, row+3)

			# button
			self.o1B1 = QtGui.QPushButton("X-", self)
			self.o1B1.clicked.connect(self.setX1)
			self.o1B1.setFixedWidth(btsize)
			self.o1B1.move(cbt1, row)
			self.o1B1.setAutoRepeat(True)
			
			# button
			self.o1B2 = QtGui.QPushButton("X+", self)
			self.o1B2.clicked.connect(self.setX2)
			self.o1B2.setFixedWidth(btsize)
			self.o1B2.move(cbt2, row)
			self.o1B2.setAutoRepeat(True)

			row += 30

			# label
			self.o2L = QtGui.QLabel(self.gInfoMoveY, self)
			self.o2L.move(10, row+3)

			# button
			self.o2B1 = QtGui.QPushButton("Y-", self)
			self.o2B1.clicked.connect(self.setY1)
			self.o2B1.setFixedWidth(btsize)
			self.o2B1.move(cbt1, row)
			self.o2B1.setAutoRepeat(True)
			
			# button
			self.o2B2 = QtGui.QPushButton("Y+", self)
			self.o2B2.clicked.connect(self.setY2)
			self.o2B2.setFixedWidth(btsize)
			self.o2B2.move(cbt2, row)
			self.o2B2.setAutoRepeat(True)

			row += 30
			
			# label
			self.o3L = QtGui.QLabel(self.gInfoMoveZ, self)
			self.o3L.move(10, row+3)

			# button
			self.o3B1 = QtGui.QPushButton("Z-", self)
			self.o3B1.clicked.connect(self.setZ1)
			self.o3B1.setFixedWidth(btsize)
			self.o3B1.move(cbt1, row)
			self.o3B1.setAutoRepeat(True)
			
			# button
			self.o3B2 = QtGui.QPushButton("Z+", self)
			self.o3B2.clicked.connect(self.setZ2)
			self.o3B2.setFixedWidth(btsize)
			self.o3B2.move(cbt2, row)
			self.o3B2.setAutoRepeat(True)

			row += 30
			
			# label
			self.o4L = QtGui.QLabel(self.gInfoMoveStep, self)
			self.o4L.move(10, row+3)

			# text input
			self.o4E = QtGui.QLineEdit(self)
			self.o4E.setText(str(self.gStep))
			self.o4E.setFixedWidth(btsize)
			self.o4E.move(cbt2, row)

			# ############################################################################
			# settigns for custom GUI
			# ############################################################################
			
			rbs = 30
			rbo = 5
			rbc = rside - (3 * rbs) - (2 * rbo) + 10

			# ############################################################################
			# GUI for Move to Equal (hidden by default)
			# ############################################################################
			
			rowmte += 40
			
			self.mte1B = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.mte1B.clicked.connect(self.setMEEdgeStart)
			self.mte1B.setFixedWidth(60)
			self.mte1B.setFixedHeight(20)
			self.mte1B.move(10, rowmte)
			self.mte1B.hide()
			
			self.mte1L = QtGui.QLabel(self.gNoMEEdgeStart, self)
			self.mte1L.setFixedWidth(rside - 80)
			self.mte1L.move(80, rowmte+3)
			self.mte1L.hide()

			rowmte += 30
			
			self.mte2B = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.mte2B.clicked.connect(self.setMEEdgeEnd)
			self.mte2B.setFixedWidth(60)
			self.mte2B.setFixedHeight(20)
			self.mte2B.move(10, rowmte)
			self.mte2B.hide()
			
			self.mte2L = QtGui.QLabel(self.gNoMEEdgeEnd, self)
			self.mte2L.setFixedWidth(rside - 80)
			self.mte2L.move(80, rowmte+3)
			self.mte2L.hide()

			rowmte += 30
			
			# button
			self.mte12B = QtGui.QPushButton(translate('magicMove', 'set both edges'), self)
			self.mte12B.clicked.connect(self.setMEEdge)
			self.mte12B.setFixedWidth(rside)
			self.mte12B.setFixedHeight(20)
			self.mte12B.move(10, rowmte)

			rowmte += 30
			
			# label
			self.mte3L = QtGui.QLabel(translate('magicMove', 'Equal space along X:'), self)
			self.mte3L.move(10, rowmte+3)

			# button
			self.mte3B = QtGui.QPushButton(translate('magicMove', 'move'), self)
			self.mte3B.clicked.connect(self.createMoveToEqualX)
			self.mte3B.setFixedWidth(btsize+20)
			self.mte3B.move(cbt2-20, rowmte)
			self.mte3B.setAutoRepeat(False)
			
			rowmte += 30

			# label
			self.mte4L = QtGui.QLabel(translate('magicMove', 'Equal space along Y:'), self)
			self.mte4L.move(10, rowmte+3)

			# button
			self.mte4B = QtGui.QPushButton(translate('magicMove', 'move'), self)
			self.mte4B.clicked.connect(self.createMoveToEqualY)
			self.mte4B.setFixedWidth(btsize+20)
			self.mte4B.move(cbt2-20, rowmte)
			self.mte4B.setAutoRepeat(False)
	
			rowmte += 30
			
			# label
			self.mte5L = QtGui.QLabel(translate('magicMove', 'Equal space along Z:'), self)
			self.mte5L.move(10, rowmte+3)

			# button
			self.mte5B = QtGui.QPushButton(translate('magicMove', 'move'), self)
			self.mte5B.clicked.connect(self.createMoveToEqualZ)
			self.mte5B.setFixedWidth(btsize+20)
			self.mte5B.move(cbt2-20, rowmte)
			self.mte5B.setAutoRepeat(False)
			
			# hide by default
			self.mte1L.hide()
			self.mte1B.hide()
			self.mte2L.hide()
			self.mte2B.hide()
			self.mte12B.hide()
			self.mte3L.hide()
			self.mte3B.hide()
			self.mte4L.hide()
			self.mte4B.hide()
			self.mte5L.hide()
			self.mte5B.hide()
			
			# ############################################################################
			# GUI for Copy by Edge (hidden by default)
			# ############################################################################
			
			rowcbe += 40
			
			self.cbe1B = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.cbe1B.clicked.connect(self.setCopyByEdge)
			self.cbe1B.setFixedWidth(60)
			self.cbe1B.setFixedHeight(20)
			self.cbe1B.move(10, rowcbe)
			self.cbe1B.hide()
			
			self.cbe1L = QtGui.QLabel(self.gNoCopyByEdge, self)
			self.cbe1L.setFixedWidth(rside - 80)
			self.cbe1L.move(80, rowcbe+3)
			self.cbe1L.hide()

			rowcbe += 30
			
			# label
			self.cbe2L = QtGui.QLabel(self.gInfoCopyX, self)
			self.cbe2L.move(10, rowcbe+3)

			# button
			self.cbe2B = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.cbe2B.clicked.connect(self.createCopyByEdgeX)
			self.cbe2B.setFixedWidth(2 * btsize + 10)
			self.cbe2B.move(cbt1, rowcbe)
			self.cbe2B.setAutoRepeat(False)
			
			rowcbe += 30

			# label
			self.cbe3L = QtGui.QLabel(self.gInfoCopyY, self)
			self.cbe3L.move(10, rowcbe+3)

			# button
			self.cbe3B = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.cbe3B.clicked.connect(self.createCopyByEdgeY)
			self.cbe3B.setFixedWidth(2 * btsize + 10)
			self.cbe3B.move(cbt1, rowcbe)
			self.cbe3B.setAutoRepeat(False)
	
			rowcbe += 30
			
			# label
			self.cbe4L = QtGui.QLabel(self.gInfoCopyZ, self)
			self.cbe4L.move(10, rowcbe+3)

			# button
			self.cbe4B = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.cbe4B.clicked.connect(self.createCopyByEdgeZ)
			self.cbe4B.setFixedWidth(2 * btsize + 10)
			self.cbe4B.move(cbt1, rowcbe)
			self.cbe4B.setAutoRepeat(False)
			
			rowcbe += 30
			
			# label
			self.cbe5L = QtGui.QLabel(translate('magicMove', 'Additional offset'), self)
			self.cbe5L.move(10, rowcbe+3)

			# text input
			self.cbe5E = QtGui.QLineEdit(self)
			self.cbe5E.setText("0")
			self.cbe5E.setFixedWidth(btsize)
			self.cbe5E.move(cbt2, rowcbe)

			# hide by default
			self.cbe1L.hide()
			self.cbe1B.hide()
			self.cbe2L.hide()
			self.cbe2B.hide()
			self.cbe3L.hide()
			self.cbe3B.hide()
			self.cbe4L.hide()
			self.cbe4B.hide()
			self.cbe5L.hide()
			self.cbe5E.hide()
			
			# ############################################################################
			# GUI for Copy by Path (hidden by default)
			# ############################################################################
			
			self.pathL1 = QtGui.QLabel(self.gInfoPath1, self)
			self.pathL1.move(10, rowpath+3)
			self.pathL1.hide()
			
			self.pathE1 = QtGui.QLineEdit(self)
			self.pathE1.setText("0")
			self.pathE1.setFixedWidth(rbs)
			self.pathE1.move(rbc, rowpath)
			self.pathE1.hide()
			
			self.pathE2 = QtGui.QLineEdit(self)
			self.pathE2.setText("0")
			self.pathE2.setFixedWidth(rbs)
			self.pathE2.move(rbc + rbs + rbo, rowpath)
			self.pathE2.hide()
	
			self.pathE3 = QtGui.QLineEdit(self)
			self.pathE3.setText("0")
			self.pathE3.setFixedWidth(rbs)
			self.pathE3.move(rbc + (2 * rbs) + (2 * rbo), rowpath)
			self.pathE3.hide()

			rowpath += 30
			
			self.pathL2 = QtGui.QLabel(self.gInfoPath2, self)
			self.pathL2.move(10, rowpath+3)
			self.pathL2.hide()
			
			self.pathE4 = QtGui.QLineEdit(self)
			self.pathE4.setText("1")
			self.pathE4.setFixedWidth(65)
			self.pathE4.move(rside - 55, rowpath)
			self.pathE4.hide()

			rowpath += 30
			
			self.pathB1 = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.pathB1.clicked.connect(self.setCopyPath)
			self.pathB1.setFixedWidth(60)
			self.pathB1.setFixedHeight(20)
			self.pathB1.move(10, rowpath)
			self.pathB1.hide()
			
			self.pathL3 = QtGui.QLabel(self.gNoPathSelection, self)
			self.pathL3.setFixedWidth(rside-80)
			self.pathL3.move(80, rowpath+3)
			self.pathL3.hide()

			rowpath += 30
			
			self.pathB2 = QtGui.QPushButton(translate('magicMove', 'copy along path'), self)
			self.pathB2.clicked.connect(self.createPathPanel)
			self.pathB2.setFixedWidth(rside)
			self.pathB2.setFixedHeight(30)
			self.pathB2.move(10, rowpath)
			self.pathB2.setAutoRepeat(True)
			self.pathB2.hide()

			# ############################################################################
			# GUI for Mirror copy (hidden by default)
			# ############################################################################
			
			rowmc += 40
			
			self.mc1B = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.mc1B.clicked.connect(self.setMirrorPoint)
			self.mc1B.setFixedWidth(60)
			self.mc1B.setFixedHeight(20)
			self.mc1B.move(10, rowmc)
			self.mc1B.hide()
			
			self.mc1L = QtGui.QLabel(self.gNoMirrorPoint, self)
			self.mc1L.setFixedWidth(rside - 80)
			self.mc1L.move(80, rowmc+3)
			self.mc1L.hide()

			rowmc += 30

			self.mc3L = QtGui.QLabel(translate('magicMove', 'Mirror XYZ:'), self)
			self.mc3L.move(10, rowmc+3)
			self.mc3L.hide()
			
			rmc = rbc - 45
			rms = rbs + 15
			
			self.mc31E = QtGui.QLineEdit(self)
			self.mc31E.setText("0")
			self.mc31E.setFixedWidth(rms)
			self.mc31E.move(rmc, rowmc)
			self.mc31E.hide()
			
			self.mc32E = QtGui.QLineEdit(self)
			self.mc32E.setText("0")
			self.mc32E.setFixedWidth(rms)
			self.mc32E.move(rmc + rms + rbo, rowmc)
			self.mc32E.hide()
	
			self.mc33E = QtGui.QLineEdit(self)
			self.mc33E.setText("0")
			self.mc33E.setFixedWidth(rms)
			self.mc33E.move(rmc + (2 * rms) + (2 * rbo), rowmc)
			self.mc33E.hide()
			
			rowmc += 30
			
			# label
			self.mc2L = QtGui.QLabel(translate('magicMove', 'Additional offset:'), self)
			self.mc2L.move(10, rowmc+3)

			# text input
			self.mc2E = QtGui.QLineEdit(self)
			self.mc2E.setText("0")
			self.mc2E.setFixedWidth(btsize)
			self.mc2E.move(cbt2, rowmc)

			rowmc += 30
			
			# label
			self.mc4L = QtGui.QLabel(translate('magicMove', 'Mirror along X:'), self)
			self.mc4L.move(10, rowmc+3)

			# button
			self.mc4B1 = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.mc4B1.clicked.connect(self.createMirrorX)
			self.mc4B1.setFixedWidth(2 * btsize + 10)
			self.mc4B1.move(cbt1, rowmc)
			self.mc4B1.setAutoRepeat(False)
	
			rowmc += 30

			# label
			self.mc5L = QtGui.QLabel(translate('magicMove', 'Mirror along Y:'), self)
			self.mc5L.move(10, rowmc+3)

			# button
			self.mc5B1 = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.mc5B1.clicked.connect(self.createMirrorY)
			self.mc5B1.setFixedWidth(2 * btsize + 10)
			self.mc5B1.move(cbt1, rowmc)
			self.mc5B1.setAutoRepeat(False)

			rowmc += 30
			
			# label
			self.mc6L = QtGui.QLabel(translate('magicMove', 'Mirror along Z:'), self)
			self.mc6L.move(10, rowmc+3)

			# button
			self.mc6B1 = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.mc6B1.clicked.connect(self.createMirrorZ)
			self.mc6B1.setFixedWidth(2 * btsize + 10)
			self.mc6B1.move(cbt1, rowmc)
			self.mc6B1.setAutoRepeat(False)
			
			# hide by default
			self.mc1B.hide()
			self.mc1L.hide()
			self.mc2L.hide()
			self.mc2E.hide()
			self.mc3L.hide()
			self.mc31E.hide()
			self.mc32E.hide()
			self.mc33E.hide()
			self.mc4L.hide()
			self.mc4B1.hide()
			self.mc5L.hide()
			self.mc5B1.hide()
			self.mc6L.hide()
			self.mc6B1.hide()
		
			# ############################################################################
			# GUI for common foot (visible by default)
			# ############################################################################
			
			row = toolSH - 90
			
			# label
			self.o0L = QtGui.QLabel(translate('magicMove', 'Corner cross:'), self)
			self.o0L.move(10, row+3)

			# button
			self.o0B1 = QtGui.QPushButton("-", self)
			self.o0B1.clicked.connect(self.setCornerM)
			self.o0B1.setFixedWidth(btsize)
			self.o0B1.move(cbt1, row)
			self.o0B1.setAutoRepeat(True)
			
			# button
			self.o0B2 = QtGui.QPushButton("+", self)
			self.o0B2.clicked.connect(self.setCornerP)
			self.o0B2.setFixedWidth(btsize)
			self.o0B2.move(cbt2, row)
			self.o0B2.setAutoRepeat(True)

			row += 30
			
			# label
			self.o0L = QtGui.QLabel(translate('magicMove', 'Center cross:'), self)
			self.o0L.move(10, row+3)

			# button
			self.o0B1 = QtGui.QPushButton(translate('magicMove', 'on'), self)
			self.o0B1.clicked.connect(self.setCenterOn)
			self.o0B1.setFixedWidth(btsize)
			self.o0B1.move(cbt1, row)
			self.o0B1.setAutoRepeat(True)
			
			# button
			self.o0B2 = QtGui.QPushButton(translate('magicMove', 'off'), self)
			self.o0B2.clicked.connect(self.setCenterOff)
			self.o0B2.setFixedWidth(btsize)
			self.o0B2.move(cbt2, row)
			self.o0B2.setAutoRepeat(True)

			row += 25
			
			self.kccscb = QtGui.QCheckBox(translate('magicDowels', ' - keep custom cross settings'), self)
			self.kccscb.setCheckState(QtCore.Qt.Unchecked)
			self.kccscb.move(10, row+3)
			
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
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def resetGlobals(self):
			
			self.gMaxX = 0
			self.gMaxY = 0
			self.gMaxZ = 0
			
			self.gLCPX = dict() 
			self.gLCPY = dict() 
			self.gLCPZ = dict() 
			self.gLCPR = dict()

			self.gNewContainerON = False
			self.gContainerRef = "root"

		# ############################################################################
		def setLastPosition(self):
			for o in self.gObjects:
				toMove = MagicPanels.getObjectToMove(o)
				key = str(o.Name)
				[ 	self.gLCPX[key], 
					self.gLCPY[key], 
					self.gLCPZ[key], 
					self.gLCPR[key] ] = MagicPanels.getContainerPlacement(toMove, "clean")
		
		# ############################################################################
		def setNewContainer(self):
			self.gNewContainerON = True
			self.gNewContainerB1.setDisabled(True)

		# ############################################################################
		def setMove(self, iType):
			
			for o in self.gObjects:

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
				
				[ px, py, pz, r ] = MagicPanels.getContainerPlacement(o, "clean")
				MagicPanels.setContainerPlacement(o, px+x, py+y, pz+z, 0, "clean")

			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def setMEEdgeStart(self):
			
			try:
				self.gMTESObj = FreeCADGui.Selection.getSelection()[0]
				self.gMTESEdge = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				if self.gMTESEdge.ShapeType != "Edge":
					raise
				
				index = MagicPanels.getEdgeIndex(self.gMTESObj, self.gMTESEdge)
				self.mte1L.setText(self.gMTESObj.Label + ", Edge" + str(index))
				
				FreeCADGui.Selection.clearSelection()

			except:
				self.mte1L.setText(self.gNoMEEdgeStart)
		
		# ############################################################################
		def setMEEdgeEnd(self):
			
			try:
				self.gMTEEObj = FreeCADGui.Selection.getSelection()[0]
				self.gMTEEEdge = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				if self.gMTEEEdge.ShapeType != "Edge":
					raise
				
				index = MagicPanels.getEdgeIndex(self.gMTEEObj, self.gMTEEEdge)
				self.mte2L.setText(self.gMTEEObj.Label + ", Edge" + str(index))
				
				FreeCADGui.Selection.clearSelection()

			except:
				self.mte2L.setText(self.gNoMEEdgeEnd)
		
		# ############################################################################
		def setMEEdge(self):
			
			try:
			
				self.gMTESObj = FreeCADGui.Selection.getSelection()[0]
				self.gMTESEdge = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gMTEEObj = FreeCADGui.Selection.getSelection()[1]
				self.gMTEEEdge = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				if self.gMTESEdge.ShapeType != "Edge":
					raise
				
				if self.gMTEEEdge.ShapeType != "Edge":
					raise
				
				index = MagicPanels.getEdgeIndex(self.gMTESObj, self.gMTESEdge)
				self.mte1L.setText(self.gMTESObj.Label + ", Edge" + str(index))
				
				index = MagicPanels.getEdgeIndex(self.gMTEEObj, self.gMTEEEdge)
				self.mte2L.setText(self.gMTEEObj.Label + ", Edge" + str(index))
				
				FreeCADGui.Selection.clearSelection()

			except:
				self.mte1L.setText(self.gNoMEEdgeStart)
				self.mte2L.setText(self.gNoMEEdgeEnd)
			
		# ############################################################################
		def createMoveToEqual(self, iType):
			
			num = len(self.gObjects)
			thick = 0
			
			if iType == "X":
				gap = abs(float(self.gMTEEEdge.CenterOfMass.x) - float(self.gMTESEdge.CenterOfMass.x))
				start = float(self.gMTESEdge.CenterOfMass.x)
			
			if iType == "Y":
				gap = abs(float(self.gMTEEEdge.CenterOfMass.y) - float(self.gMTESEdge.CenterOfMass.y))
				start = float(self.gMTESEdge.CenterOfMass.y)
			
			if iType == "Z":
				gap = abs(float(self.gMTEEEdge.CenterOfMass.z) - float(self.gMTESEdge.CenterOfMass.z))
				start = float(self.gMTESEdge.CenterOfMass.z)
	
			for o in self.gObjects:
				
				[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)
				
				if iType == "X":
					thick = thick + sizeX
				
				if iType == "Y":
					thick = thick + sizeY
				
				if iType == "Z":
					thick = thick + sizeZ

			offset = (gap - thick) / (num + 1)
			
			i = 0
			for o in self.gObjects:
				
				[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)
				
				oRef = MagicPanels.getReference(o)
				toMove = MagicPanels.getObjectToMove(oRef)
				[ X, Y, Z, R ] = MagicPanels.getContainerPlacement(toMove, "clean")

				if iType == "X":
					X = start + ((i + 1) * offset) + (i * sizeX)
				
				if iType == "Y":
					Y = start + ((i + 1) * offset) + (i * sizeY)
				
				if iType == "Z":
					Z = start + ((i + 1) * offset) + (i * sizeZ)
				
				MagicPanels.setContainerPlacement(toMove, X, Y, Z, 0, "clean")
				i = i + 1

			FreeCAD.ActiveDocument.recompute()
				
		
		# ############################################################################
		def createCopy(self, iType):
			
			for o in self.gObjects:
				
				key = str(o.Name)
				x, y, z, r = self.gLCPX[key], self.gLCPY[key], self.gLCPZ[key], self.gLCPR[key]

				self.gStep = float(self.o4E.text())
				
				if self.gCopyType == 0:
					copy = MagicPanels.copyPanel([ o ], "copyObject")[0]
				if self.gCopyType == 1:
					copy = MagicPanels.copyPanel([ o ], "Clone")[0]
				if self.gCopyType == 2:
					copy = MagicPanels.copyPanel([ o ], "Link")[0]
				if self.gCopyType == 3:
					copy = MagicPanels.copyPanel([ o ], "auto")[0]
				
				# create new container with copy inside
				if self.gNewContainerON == True:
					container = MagicPanels.createContainer([ copy ])
					self.gContainerRef = container
					self.gNewContainerON = False
					self.gNewContainerB1.setDisabled(False)
					MagicPanels.moveToParent([ container ], o)
				
				# move copy to container if there is current container
				else:
					if self.gContainerRef != "root":
						MagicPanels.moveToContainer([ copy ], self.gContainerRef)
					
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
					z = z - self.gMaxZ - self.gStep

				MagicPanels.setContainerPlacement(copy, x, y, z, 0, "clean")
				FreeCAD.ActiveDocument.recompute()
				
				try:
					MagicPanels.copyColors(o, copy)
				except:
					skip = 1

				[ 	self.gLCPX[key], 
					self.gLCPY[key], 
					self.gLCPZ[key], 
					self.gLCPR[key] ] = MagicPanels.getContainerPlacement(copy, "clean")
				
				if self.gContainerRef == "root":
					MagicPanels.moveToParent([ copy ], o)

		# ############################################################################
		def setCopyByEdge(self):
			
			try:
				self.gCBEObj = FreeCADGui.Selection.getSelection()[0]
				self.gCBEEdge = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				if self.gCBEEdge.ShapeType != "Edge":
					raise
				
				index = MagicPanels.getEdgeIndex(self.gCBEObj, self.gCBEEdge)
				self.cbe1L.setText(self.gCBEObj.Label + ", Edge" + str(index))

			except:
				self.cbe1L.setText(self.gNoCopyByEdge)
				
		# ############################################################################
		def createCopyByEdge(self, iType):
			
			offset = float(self.cbe5E.text())
			
			for o in self.gObjects:
				
				[ sizex, sizey, sizez ] = MagicPanels.getSizesFromVertices(o)
				[ x, y, z, r ] = MagicPanels.getGlobalPlacement(o, "BoundBox")
				
				if iType == "X":
					
					ex = float(self.gCBEEdge.CenterOfMass.x)
					diff = abs(ex - x)
				
					# copy from left side to right
					if x < ex:
						x = ex + diff - sizex
						x = x + offset
					
					# copy from right side to left
					else:
						x = ex - diff - sizex
						x = x - offset
					
				if iType == "Y":
					
					ey = float(self.gCBEEdge.CenterOfMass.y)
					diff = abs(ey - y)
					
					# copy from left side to right
					if y < ey:
						y = ey + diff - sizey
						y = y + offset
					
					# copy from right side to left
					else:
						y = ey - diff - sizey
						y = y - offset
					
				if iType == "Z":
					
					ez = float(self.gCBEEdge.CenterOfMass.z)
					diff = abs(ez - z)

					# copy from left side to right
					if z < ez:
						z = ez + diff - sizez
						z = z + offset
					
					# copy from right side to left
					else:
						z = ez - diff - sizez
						z = z - offset
					
				if self.gCopyType == 0:
					copy = MagicPanels.copyPanel([ o ], "copyObject")[0]
				if self.gCopyType == 1:
					copy = MagicPanels.copyPanel([ o ], "Clone")[0]
				if self.gCopyType == 2:
					copy = MagicPanels.copyPanel([ o ], "Link")[0]
				if self.gCopyType == 3:
					copy = MagicPanels.copyPanel([ o ], "auto")[0]
				
				if not o.isDerivedFrom("Part::Box"):
					if self.gCopyType == 1 or self.gCopyType == 3:
						[ x, y, z ] = MagicPanels.adjustClonePosition(o, x, y, z)

				MagicPanels.setContainerPlacement(copy, x, y, z, 0, "clean")
				FreeCAD.ActiveDocument.recompute()
				
				try:
					MagicPanels.copyColors(o, copy)
				except:
					skip = 1

				MagicPanels.moveToParent([ copy ], o)

			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def setLastPathPosition(self):
			for o in self.gObjects:
				key = str(o.Name)
				
				[ x, y, z, r ] = MagicPanels.getContainerPlacement(o, "clean")
				v = FreeCAD.Vector(x, y, z)
				inside = self.gCopyPathObj.Shape.isInside(v, 0, True)
				
				if inside:
					self.gCopyPathLast[key] = self.gCopyPathPoints.index(v)
					self.gCopyPathInit[key] = False
				else:
					self.gCopyPathLast[key] = 0
					self.gCopyPathInit[key] = True

				self.gCopyPathRotation[key] = r
		
		# ############################################################################
		def setCopyPath(self):
			
			try:
				self.gCopyPathObj = FreeCADGui.Selection.getSelection()[0]
				
				# support wire, sketch, helix
				test1 = self.gCopyPathObj.isDerivedFrom("Sketcher::SketchObject")
				test2 = self.gCopyPathObj.isDerivedFrom("Part::Part2DObjectPython")
				test3 = self.gCopyPathObj.isDerivedFrom("Part::Helix")
				
				if test1 or test2 or test3:
					
					self.gCopyPathPoints = self.gCopyPathObj.Shape.getPoints(1)[0]
					self.pathL3.setText(self.gCopyPathObj.Label)
					self.setLastPathPosition()
				
				# support edges
				else:
					
					sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
					
					if sub.ShapeType != "Edge":
						raise
					
					self.gCopyPathPoints = sub.getPoints(1)[0]
					index = MagicPanels.getEdgeIndex(self.gCopyPathObj, sub)
					self.pathL3.setText(self.gCopyPathObj.Label + ", Edge" + str(index))
					self.setLastPathPosition()
			
			except:
				self.pathL3.setText(self.gNoPathSelection)

		# ############################################################################
		def createPathPanel(self):
			
			container = ""
			
			for o in self.gObjects:
				
				key = str(o.Name)
				index = self.gCopyPathLast[key]
				
				# you could add step after object select
				# bt it is more comfortable for user 
				# first add object, than change step and click create
				# so the create function must recalculate the step
				if self.gCopyPathInit[key] == False:
					step = int(float(self.pathE4.text()))
					self.gCopyPathLast[key] = int(self.gCopyPathLast[key] + step)
					index = index + step

				if index > len(self.gCopyPathPoints) - 1:
					return
			
				x = self.gCopyPathPoints[index].x
				y = self.gCopyPathPoints[index].y
				z = self.gCopyPathPoints[index].z
				
				if self.gCopyType == 0:
					copy = MagicPanels.copyPanel([ o ], "copyObject")[0]
				if self.gCopyType == 1:
					copy = MagicPanels.copyPanel([ o ], "Clone")[0]
				if self.gCopyType == 2:
					copy = MagicPanels.copyPanel([ o ], "Link")[0]
				if self.gCopyType == 3:
					copy = MagicPanels.copyPanel([ o ], "auto")[0]

				# create new container with copy inside
				if self.gNewContainerON == True:
					container = MagicPanels.createContainer([ copy ])
					self.gContainerRef = container
					self.gNewContainerON = False
					self.gNewContainerB1.setDisabled(False)
					MagicPanels.moveToParent([ container ], o)
				
				# move copy to container if there is current container
				else:
					if self.gContainerRef != "root":
						MagicPanels.moveToContainer([ copy ], self.gContainerRef)

				if not o.isDerivedFrom("Part::Box"):
					if self.gCopyType == 1 or self.gCopyType == 3:
						[ x, y, z ] = MagicPanels.adjustClonePosition(o, x, y, z)

				MagicPanels.setContainerPlacement(copy, x, y, z, 0, "clean")
				FreeCAD.ActiveDocument.recompute()
				
				angleX = float(self.pathE1.text())
				angleY = float(self.pathE2.text())
				angleZ = float(self.pathE3.text())
				
				rotX = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), angleX)
				rotY = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), angleY)
				rotZ = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), angleZ)
				
				copy.Placement.Rotation = self.gCopyPathRotation[key] * rotX * rotY * rotZ
				self.gCopyPathRotation[key] = copy.Placement.Rotation
				
				try:
					MagicPanels.copyColors(o, copy)
				except:
					skip = 1

				FreeCAD.ActiveDocument.recompute()
				
				# set next position
				step = int(float(self.pathE4.text()))
				self.gCopyPathLast[key] = int(self.gCopyPathLast[key] + step)
				self.gCopyPathInit[key] = True

				if self.gContainerRef == "root":
					MagicPanels.moveToParent([ copy ], o)

		# ############################################################################
		def setMirrorPoint(self):
			
			try:
				self.gMObj = FreeCADGui.Selection.getSelection()[0]
				self.gMSub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				if self.gMSub.ShapeType == "Edge":
					
					index = MagicPanels.getEdgeIndex(self.gMObj, self.gMSub)
					info = self.gMObj.Label + ", Edge" + str(index)
					
					x = float(self.gMSub.CenterOfMass.x)
					y = float(self.gMSub.CenterOfMass.y)
					z = float(self.gMSub.CenterOfMass.z)
					
				elif self.gMSub.ShapeType == "Face":
					
					index = MagicPanels.getFaceIndex(self.gMObj, self.gMSub)
					info = self.gMObj.Label + ", Face" + str(index)
					
					x = float(self.gMSub.CenterOfMass.x)
					y = float(self.gMSub.CenterOfMass.y)
					z = float(self.gMSub.CenterOfMass.z)
					
				elif self.gMSub.ShapeType == "Vertex":
				
					index = MagicPanels.getVertexIndex(self.gMObj, self.gMSub)
					info = self.gMObj.Label + ", Vertex" + str(index)
					
					x = float(self.gMSub.X)
					y = float(self.gMSub.Y)
					z = float(self.gMSub.Z)
					
				else:
					raise
				
				self.mc1L.setText(info)
				self.mc31E.setText(str(x))
				self.mc32E.setText(str(y))
				self.mc33E.setText(str(z))

			except:
				self.mc1L.setText(self.gNoMirrorPoint)
		
		# ############################################################################
		def createMirror(self, iType):
			
			for o in self.gObjects:
				
				# not create mirror directly at object because 
				# it will not be managed, extended later
				# create LinkGroup and move the object to the LinkGroup
				# and create Mirror at LinkGroup instead
				if not o.isDerivedFrom("App::LinkGroup"):
					o = MagicPanels.createContainer([o])

				# calculate
				offset = float(self.mc2E.text())
				x = float(self.mc31E.text())
				y = float(self.mc32E.text())
				z = float(self.mc33E.text())
				
				if iType == "X":
					direction = (1, 0, 0)
					offX = offset
					offY = 0
					offZ = 0
				
				if iType == "Y":
					direction = (0, 1, 0)
					offX = 0
					offY = offset
					offZ = 0
				
				if iType == "Z":
					direction = (0, 0, 1)
					offX = 0
					offY = 0
					offZ = offset
				
				mirror = FreeCAD.ActiveDocument.addObject('Part::Mirroring', "mirror")
				mirror.Label = "Mirror, " + str(o.Label) + " "
				mirror.Source = FreeCAD.ActiveDocument.getObject(o.Name)
				mirror.Normal = direction
				mirror.Base = (x, y, z)
				
				MagicPanels.setContainerPlacement(mirror, offX, offY, offZ, 0, "clean")
				FreeCAD.ActiveDocument.recompute()
				
				# hehe ;-)
				if len(o.OutListRecursive) == 0:
					MagicPanels.copyColors(o, mirror)
				else:
					
					# try to copy colors from container content
					try:
						for o in o.OutListRecursive:
							s = str(o.getAllDerivedFrom()[0])
							
							if s.startswith("Part::") or s.startswith("PartDesign::"):
								MagicPanels.copyColors(o, mirror)
								raise
					except:
						skip = 1

		# ############################################################################	
		def setModeType(self, selectedText):
			
			selectedIndex = getMenuIndex1[selectedText]
			self.gModeType = selectedIndex

			# first hide all
			
			self.mte1L.hide()
			self.mte1B.hide()
			self.mte2L.hide()
			self.mte2B.hide()
			self.mte12B.hide()
			self.mte3L.hide()
			self.mte3B.hide()
			self.mte4L.hide()
			self.mte4B.hide()
			self.mte5L.hide()
			self.mte5B.hide()
			
			self.cbe1L.hide()
			self.cbe1B.hide()
			self.cbe2L.hide()
			self.cbe2B.hide()
			self.cbe3L.hide()
			self.cbe3B.hide()
			self.cbe4L.hide()
			self.cbe4B.hide()
			self.cbe5L.hide()
			self.cbe5E.hide()
			
			self.pathE1.hide()
			self.pathE2.hide()
			self.pathE3.hide()
			self.pathE4.hide()
			self.pathB1.hide()
			self.pathB2.hide()
			self.pathL1.hide()
			self.pathL2.hide()
			self.pathL3.hide()
			
			self.o1L.hide()
			self.o1B1.hide()
			self.o1B2.hide()
			
			self.o2L.hide()
			self.o2B1.hide()
			self.o2B2.hide()
			
			self.o3L.hide()
			self.o3B1.hide()
			self.o3B2.hide()
			
			self.o4L.hide()
			self.o4E.hide()
			
			self.mc1B.hide()
			self.mc1L.hide()
			self.mc2L.hide()
			self.mc2E.hide()
			self.mc3L.hide()
			self.mc31E.hide()
			self.mc32E.hide()
			self.mc33E.hide()
			self.mc4L.hide()
			self.mc4B1.hide()
			self.mc5L.hide()
			self.mc5B1.hide()
			self.mc6L.hide()
			self.mc6B1.hide()
			
			self.sCopyType.hide()
			self.gNewContainerB1.hide()

			# default settings
			self.setLastPosition()
			
			# Move
			if selectedIndex == 0:
				
				self.o1L.show()
				self.o1B1.show()
				self.o1B2.show()
				
				self.o2L.show()
				self.o2B1.show()
				self.o2B2.show()
				
				self.o3L.show()
				self.o3B1.show()
				self.o3B2.show()
				
				self.o4L.show()
				self.o4E.show()
				
				self.o1L.setText(self.gInfoMoveX)
				self.o2L.setText(self.gInfoMoveY)
				self.o3L.setText(self.gInfoMoveZ)
				self.o4L.setText(self.gInfoMoveStep)
				self.o4E.setText(str(self.gStep))
				
			# Copy
			if selectedIndex == 1:
				
				self.o1L.show()
				self.o1B1.show()
				self.o1B2.show()
				
				self.o2L.show()
				self.o2B1.show()
				self.o2B2.show()
				
				self.o3L.show()
				self.o3B1.show()
				self.o3B2.show()
				
				self.o4L.show()
				self.o4E.show()
				
				self.o1L.setText(self.gInfoCopyX)
				self.o2L.setText(self.gInfoCopyY)
				self.o3L.setText(self.gInfoCopyZ)
				self.o4L.setText(self.gInfoCopyStep)
				self.o4E.setText(str(self.gStep))
				
				self.sCopyType.show()
				self.gNewContainerB1.show()

			# Copy by Path
			if selectedIndex == 2:
				
				self.pathL1.show()
				self.pathE1.show()
				
				self.pathL2.show()
				self.pathE2.show()
				
				self.pathL3.show()
				self.pathE3.show()
				
				self.pathE4.show()
				self.pathB1.show()
				self.pathB2.show()
				
				self.sCopyType.show()
				self.gNewContainerB1.show()

			# Mirror
			if selectedIndex == 3:
				
				self.mc1B.show()
				self.mc1L.show()
				self.mc2L.show()
				self.mc2E.show()
				self.mc3L.show()
				self.mc31E.show()
				self.mc32E.show()
				self.mc33E.show()
				self.mc4L.show()
				self.mc4B1.show()
				self.mc5L.show()
				self.mc5B1.show()
				self.mc6L.show()
				self.mc6B1.show()
	
			# Copy by Edge
			if selectedIndex == 4:

				self.cbe1L.show()
				self.cbe1B.show()

				self.cbe2L.show()
				self.cbe2B.show()

				self.cbe3L.show()
				self.cbe3B.show()

				self.cbe4L.show()
				self.cbe4B.show()
				
				self.cbe5L.show()
				self.cbe5E.show()
				
				self.sCopyType.show()
			
			
			# Move to Equal
			if selectedIndex == 5:

				self.mte1L.show()
				self.mte1B.show()
				self.mte2L.show()
				self.mte2B.show()
				self.mte12B.show()
				self.mte3L.show()
				self.mte3B.show()
				self.mte4L.show()
				self.mte4B.show()
				self.mte5L.show()
				self.mte5B.show()
			
		# ############################################################################
		def setCopyType(self, selectedText):
			self.gCopyType = getMenuIndex2[selectedText]
		
		# ############################################################################
		def setX1(self):
			
			try:
				# Move
				if self.gModeType == 0:
					self.setMove("Xm")
					
				# Copy
				if self.gModeType == 1:
					self.createCopy("Xm")

			except:
				self.s1S.setText(self.gNoSelection)
			
		def setX2(self):
			
			try:
				# Move
				if self.gModeType == 0:
					self.setMove("Xp")
					
				# Copy
				if self.gModeType == 1:
					self.createCopy("Xp")

			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def setY1(self):
			
			try:
				# Move
				if self.gModeType == 0:
					self.setMove("Ym")
					
				# Copy
				if self.gModeType == 1:
					self.createCopy("Ym")
			
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setY2(self):
			
			try:
				# Move
				if self.gModeType == 0:
					self.setMove("Yp")
					
				# Copy
				if self.gModeType == 1:
					self.createCopy("Yp")

			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def setZ1(self):
			
			try:
				# Move
				if self.gModeType == 0:
					self.setMove("Zm")
					
				# Copy
				if self.gModeType == 1:
					self.createCopy("Zm")
				
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setZ2(self):
			
			try:
				# Move
				if self.gModeType == 0:
					self.setMove("Zp")
					
				# Copy
				if self.gModeType == 1:
					self.createCopy("Zp")

			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def createMoveToEqualX(self):
			self.createMoveToEqual("X")
			
		def createMoveToEqualY(self):
			self.createMoveToEqual("Y")
			
		def createMoveToEqualZ(self):
			self.createMoveToEqual("Z")

		# ############################################################################
		def createCopyByEdgeX(self):
			self.createCopyByEdge("X")
			
		def createCopyByEdgeY(self):
			self.createCopyByEdge("Y")
			
		def createCopyByEdgeZ(self):
			self.createCopyByEdge("Z")

		# ############################################################################
		def createMirrorX(self):
			self.createMirror("X")
			
		def createMirrorY(self):
			self.createMirror("Y")
			
		def createMirrorZ(self):
			self.createMirror("Z")

		# ############################################################################
		def setCornerM(self):

			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				if s - 1 < 0:
					FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(0)
				else:
					FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s-1)
					self.gCrossCorner = s-1
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setCornerP(self):

			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s+1)
				self.gCrossCorner = s+1
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def setCenterOn(self):
			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
				self.gCrossCenter = True
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setCenterOff(self):

			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(False)
				self.gCrossCenter = False
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def getSelected(self):

			try:

				self.resetGlobals()
				
				self.gObjects = FreeCADGui.Selection.getSelection()
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				
				sizes = []
				sizes = MagicPanels.getSizes(self.gObj)
				sizes.sort()
				self.gStep = sizes[0]
				self.gThick = sizes[0]
				self.gCopyPathStep = sizes[1]
				
				self.o4E.setText(str(self.gStep))
				self.pathE4.setText(str(self.gCopyPathStep))
				
				if len(self.gObjects) > 1:
					self.s1S.setText("Multi, "+str(self.gObj.Label))
				else:
					self.s1S.setText(str(self.gObj.Label))
				
				FreeCADGui.Selection.clearSelection()
				
				[ self.gMaxX, self.gMaxY, self.gMaxZ ] = MagicPanels.getSizesFromVertices(self.gObj)
				self.setLastPosition()
				
				if self.gCopyPathObj != "":
					self.setLastPathPosition()

				# copyObject of LinkGroup is visible as single object, so set Link copy mode
				if self.gModeType == 1:
					for o in self.gObjects:
						if o.isDerivedFrom("App::LinkGroup"):
							self.sCopyType.setCurrentIndex(2)
							break

			except:

				self.s1S.setText(self.gNoSelection)
				return -1
	
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		
		if not form.kccscb.isChecked():
			FreeCADGui.ActiveDocument.ActiveView.setAxisCross(form.gCrossCenterOrig)
			FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(form.gCrossCornerOrig)

		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################

