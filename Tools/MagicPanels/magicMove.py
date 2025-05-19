import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore
import time

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

# add new items only at the end and change self.sMirrorTypeList
getMenuIndex3 = {
	translate('magicMove', 'auto'): 0, 
	translate('magicMove', 'LinkGroup'): 1, 
	translate('magicMove', 'Clone'): 2 # no comma
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
		gMirrorType = getMenuIndex3[translate('magicMove', 'auto')]
		
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
		gNoCopyByEdge = translate('magicMove', 'select edge or face')
		gNoMirrorPoint = translate('magicMove', 'edge, face or vertex')
		gNoMEEdgeStart = translate('magicMove', 'select start edge')
		gNoMEEdgeEnd = translate('magicMove', 'select end edge')
		
		gObjects = ""
		
		gLCPX = dict() # Last Copy Position X
		gLCPY = dict() # Last Copy Position Y
		gLCPZ = dict() # Last Copy Position Z
		gLCPR = dict() # Last Copy Position Rotation
		
		gNewContainerON = False
		gContainerRef = "root"
		
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
		
		gPathObj = ""
		gPathStep = 1
		gPathPoints = []
		gPathRotation = dict() # last rotation
		gPathLast = dict() # last path position
		gPathInit = dict() # if init from 0 or last selected panel
		
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
			toolSW = 280
			toolSH = 450
			
			area = toolSW - 20          # full gui area
			rside = toolSW - 10         # right side of the GUI
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 0 + 200
			gPH = int( gSH - toolSH ) - 40

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
			self.s1S.setFixedWidth(area-10)
			self.s1S.move(10, row)

			row += 20

			# button
			self.s1B1 = QtGui.QPushButton(translate('magicMove', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(area)
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
			self.sMode.textActivated[str].connect(self.setModeType)
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
			self.sCopyType.textActivated[str].connect(self.setCopyType)
			self.sCopyType.setFixedWidth(95)
			self.sCopyType.move(area - 85, row)
			self.sCopyType.hide()

			# not write here, copy text from getMenuIndex3 to avoid typo
			self.sMirrorTypeList = (
				translate('magicMove', 'auto'), 
				translate('magicMove', 'LinkGroup'), 
				translate('magicMove', 'Clone') # no comma
			)
			
			self.sMirrorType = QtGui.QComboBox(self)
			self.sMirrorType.addItems(self.sMirrorTypeList)
			self.sMirrorType.setCurrentIndex(0) # default
			self.sMirrorType.textActivated[str].connect(self.setMirrorType)
			self.sMirrorType.setFixedWidth(95)
			self.sMirrorType.move(area - 85, row)
			self.sMirrorType.hide()

			# ############################################################################
			# settigns for custom GUI
			# ############################################################################

			rowcbe = row                                   # row for copy by edge
			rowmte = row                                   # row for move to equal
			rowmc = row                                    # row for mirror copy
			rowpath = row + 80                             # row to copy along path
			
			btsize = 50                                    # button size
			btsize2x = 2 * btsize + 10                     # button size 2x normal
			btoffset = 5                                   # button offset
			bc1 = area - (2 * btsize) - btoffset + 5       # button column 1
			bc2 = area - btsize + btoffset + 5             # button column 2
			
			tfsize = 80                                    # text field size
			tfsizeLong = 2 * btsize + 10                   # longer text field size for step
			
			rfs = 50                                       # rotation field size
			rfo = 5                                        # rotation field offset
			
			mfoffset = 10                                  # mirror text field offset
			mfsize = (area - (2 * mfoffset)) / 3           # mirror text field size
			
			# ############################################################################
			# GUI for Move and Copy (visible for Move by default)
			# ############################################################################
			
			row += 30

			# button
			self.gNewContainerB1 = QtGui.QPushButton(translate('magicMove', 'copy to new container'), self)
			self.gNewContainerB1.clicked.connect(self.setNewContainer)
			self.gNewContainerB1.setFixedWidth(area)
			self.gNewContainerB1.setFixedHeight(40)
			self.gNewContainerB1.move(10, row)
			self.gNewContainerB1.hide()

			row += 50

			# label
			self.o1L = QtGui.QLabel(self.gInfoMoveX, self)
			self.o1L.move(10, row+3)

			# button
			self.o1B1 = QtGui.QPushButton("X-", self)
			self.o1B1.clicked.connect(self.setX1)
			self.o1B1.setFixedWidth(btsize)
			self.o1B1.move(bc1, row)
			self.o1B1.setAutoRepeat(True)
			
			# button
			self.o1B2 = QtGui.QPushButton("X+", self)
			self.o1B2.clicked.connect(self.setX2)
			self.o1B2.setFixedWidth(btsize)
			self.o1B2.move(bc2, row)
			self.o1B2.setAutoRepeat(True)

			row += 30

			# label
			self.o2L = QtGui.QLabel(self.gInfoMoveY, self)
			self.o2L.move(10, row+3)

			# button
			self.o2B1 = QtGui.QPushButton("Y-", self)
			self.o2B1.clicked.connect(self.setY1)
			self.o2B1.setFixedWidth(btsize)
			self.o2B1.move(bc1, row)
			self.o2B1.setAutoRepeat(True)
			
			# button
			self.o2B2 = QtGui.QPushButton("Y+", self)
			self.o2B2.clicked.connect(self.setY2)
			self.o2B2.setFixedWidth(btsize)
			self.o2B2.move(bc2, row)
			self.o2B2.setAutoRepeat(True)

			row += 30
			
			# label
			self.o3L = QtGui.QLabel(self.gInfoMoveZ, self)
			self.o3L.move(10, row+3)

			# button
			self.o3B1 = QtGui.QPushButton("Z-", self)
			self.o3B1.clicked.connect(self.setZ1)
			self.o3B1.setFixedWidth(btsize)
			self.o3B1.move(bc1, row)
			self.o3B1.setAutoRepeat(True)
			
			# button
			self.o3B2 = QtGui.QPushButton("Z+", self)
			self.o3B2.clicked.connect(self.setZ2)
			self.o3B2.setFixedWidth(btsize)
			self.o3B2.move(bc2, row)
			self.o3B2.setAutoRepeat(True)

			row += 40
			
			# label
			self.oStepL = QtGui.QLabel(self.gInfoMoveStep, self)
			self.oStepL.setFixedWidth(100)
			self.oStepL.move(10, row+3)

			# text input
			self.oStepE = QtGui.QLineEdit(self)
			self.oStepE.setText(MagicPanels.unit2gui(100))
			self.oStepE.setFixedWidth(tfsizeLong)
			self.oStepE.move(rside-tfsizeLong, row)

			# ############################################################################
			# animation checkbox
			# ############################################################################

			row += 30
				
			self.animcb = QtGui.QCheckBox(translate('magicMove', ' - animate move'), self)
			self.animcb.setCheckState(QtCore.Qt.Unchecked)
			self.animcb.move(10, row+3)

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
			self.mte1L.setFixedWidth(area - 80)
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
			self.mte2L.setFixedWidth(area - 80)
			self.mte2L.move(80, rowmte+3)
			self.mte2L.hide()

			rowmte += 30
			
			# button
			self.mte12B = QtGui.QPushButton(translate('magicMove', 'set both edges'), self)
			self.mte12B.clicked.connect(self.setMEEdge)
			self.mte12B.setFixedWidth(area)
			self.mte12B.setFixedHeight(40)
			self.mte12B.move(10, rowmte)

			rowmte += 50
			
			# label
			self.mte3L = QtGui.QLabel(translate('magicMove', 'Equal space along X:'), self)
			self.mte3L.move(10, rowmte+3)

			# button
			self.mte3B = QtGui.QPushButton(translate('magicMove', 'move'), self)
			self.mte3B.clicked.connect(self.createMoveToEqualX)
			self.mte3B.setFixedWidth(btsize2x)
			self.mte3B.move(rside-btsize2x, rowmte)
			self.mte3B.setAutoRepeat(False)
			
			rowmte += 30

			# label
			self.mte4L = QtGui.QLabel(translate('magicMove', 'Equal space along Y:'), self)
			self.mte4L.move(10, rowmte+3)

			# button
			self.mte4B = QtGui.QPushButton(translate('magicMove', 'move'), self)
			self.mte4B.clicked.connect(self.createMoveToEqualY)
			self.mte4B.setFixedWidth(btsize2x)
			self.mte4B.move(rside-btsize2x, rowmte)
			self.mte4B.setAutoRepeat(False)
	
			rowmte += 30
			
			# label
			self.mte5L = QtGui.QLabel(translate('magicMove', 'Equal space along Z:'), self)
			self.mte5L.move(10, rowmte+3)

			# button
			self.mte5B = QtGui.QPushButton(translate('magicMove', 'move'), self)
			self.mte5B.clicked.connect(self.createMoveToEqualZ)
			self.mte5B.setFixedWidth(btsize2x)
			self.mte5B.move(rside-btsize2x, rowmte)
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
			self.cbe1L.setFixedWidth(area - 80)
			self.cbe1L.move(80, rowcbe+3)
			self.cbe1L.hide()

			rowcbe += 30
			
			# label
			self.cbe2L = QtGui.QLabel(self.gInfoCopyX, self)
			self.cbe2L.move(10, rowcbe+3)

			# button
			self.cbe2B = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.cbe2B.clicked.connect(self.createCopyByEdgeX)
			self.cbe2B.setFixedWidth(btsize2x)
			self.cbe2B.move(bc1, rowcbe)
			self.cbe2B.setAutoRepeat(False)
			
			rowcbe += 30

			# label
			self.cbe3L = QtGui.QLabel(self.gInfoCopyY, self)
			self.cbe3L.move(10, rowcbe+3)

			# button
			self.cbe3B = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.cbe3B.clicked.connect(self.createCopyByEdgeY)
			self.cbe3B.setFixedWidth(btsize2x)
			self.cbe3B.move(bc1, rowcbe)
			self.cbe3B.setAutoRepeat(False)
	
			rowcbe += 30
			
			# label
			self.cbe4L = QtGui.QLabel(self.gInfoCopyZ, self)
			self.cbe4L.move(10, rowcbe+3)

			# button
			self.cbe4B = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.cbe4B.clicked.connect(self.createCopyByEdgeZ)
			self.cbe4B.setFixedWidth(btsize2x)
			self.cbe4B.move(bc1, rowcbe)
			self.cbe4B.setAutoRepeat(False)
			
			rowcbe += 40
			
			# label
			self.cbe5L = QtGui.QLabel(translate('magicMove', 'Additional offset:'), self)
			self.cbe5L.move(10, rowcbe+3)

			# text input
			self.cbe5E = QtGui.QLineEdit(self)
			self.cbe5E.setText(MagicPanels.unit2gui(0))
			self.cbe5E.setFixedWidth(tfsizeLong)
			self.cbe5E.move(rside-tfsizeLong, rowcbe)

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
			
			self.pathB1 = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.pathB1.clicked.connect(self.setCopyPath)
			self.pathB1.setFixedWidth(60)
			self.pathB1.setFixedHeight(20)
			self.pathB1.move(10, rowpath)
			self.pathB1.hide()
			
			self.oPathRotZL = QtGui.QLabel(self.gNoPathSelection, self)
			self.oPathRotZL.setFixedWidth(area-80)
			self.oPathRotZL.move(80, rowpath+3)
			self.oPathRotZL.hide()
			
			rowpath += 40
			
			self.oPathRotXL = QtGui.QLabel(self.gInfoPath1, self)
			self.oPathRotXL.move(10, rowpath+3)
			self.oPathRotXL.hide()
			
			self.oPathRotXE = QtGui.QLineEdit(self)
			self.oPathRotXE.setText("0")
			self.oPathRotXE.setFixedWidth(rfs)
			self.oPathRotXE.move(rside - (3 * rfs) - (2 * rfo), rowpath)
			self.oPathRotXE.hide()
			
			self.oPathRotYE = QtGui.QLineEdit(self)
			self.oPathRotYE.setText("0")
			self.oPathRotYE.setFixedWidth(rfs)
			self.oPathRotYE.move(rside - (2 * rfs) - (1 * rfo), rowpath)
			self.oPathRotYE.hide()
	
			self.oPathRotZE = QtGui.QLineEdit(self)
			self.oPathRotZE.setText("0")
			self.oPathRotZE.setFixedWidth(rfs)
			self.oPathRotZE.move(rside-rfs, rowpath)
			self.oPathRotZE.hide()

			rowpath += 30
			
			self.oPathRotYL = QtGui.QLabel(self.gInfoPath2, self)
			self.oPathRotYL.move(10, rowpath+3)
			self.oPathRotYL.hide()
			
			self.oPathStepE = QtGui.QLineEdit(self)
			self.oPathStepE.setText("1")
			self.oPathStepE.setFixedWidth(65)
			self.oPathStepE.move(area - 55, rowpath)
			self.oPathStepE.hide()

			rowpath += 50
			
			self.pathB2 = QtGui.QPushButton(translate('magicMove', 'copy along path'), self)
			self.pathB2.clicked.connect(self.createPathPanel)
			self.pathB2.setFixedWidth(area)
			self.pathB2.setFixedHeight(40)
			self.pathB2.move(10, rowpath)
			self.pathB2.setAutoRepeat(True)
			self.pathB2.hide()

			# ############################################################################
			# GUI for Mirror copy (hidden by default)
			# ############################################################################
			
			rowmc += 30
			
			self.mc1B = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.mc1B.clicked.connect(self.setMirrorPoint)
			self.mc1B.setFixedWidth(60)
			self.mc1B.setFixedHeight(20)
			self.mc1B.move(10, rowmc)
			self.mc1B.hide()
			
			self.mc1L = QtGui.QLabel(self.gNoMirrorPoint, self)
			self.mc1L.setFixedWidth(area - 80)
			self.mc1L.move(80, rowmc+3)
			self.mc1L.hide()

			rowmc += 30

			self.mc3L = QtGui.QLabel(translate('magicMove', 'Mirror XYZ:'), self)
			self.mc3L.move(10, rowmc+3)
			self.mc3L.hide()
			
			rowmc += 20
			
			self.mc31E = QtGui.QLineEdit(self)
			self.mc31E.setText(MagicPanels.unit2gui(0))
			self.mc31E.setFixedWidth(mfsize)
			self.mc31E.move(rside-mfsize, rowmc)
			self.mc31E.hide()
			
			self.mc32E = QtGui.QLineEdit(self)
			self.mc32E.setText(MagicPanels.unit2gui(0))
			self.mc32E.setFixedWidth(mfsize)
			self.mc32E.move(rside - (2 * mfsize) - (1 * mfoffset), rowmc)
			self.mc32E.hide()
	
			self.mc33E = QtGui.QLineEdit(self)
			self.mc33E.setText(MagicPanels.unit2gui(0))
			self.mc33E.setFixedWidth(tfsize)
			self.mc33E.move(rside - (3 * mfsize) - (2 * mfoffset), rowmc)
			self.mc33E.hide()
			
			rowmc += 30
			
			# label
			self.mc2L = QtGui.QLabel(translate('magicMove', 'Additional offset:'), self)
			self.mc2L.move(10, rowmc+3)

			# text input
			self.mc2E = QtGui.QLineEdit(self)
			self.mc2E.setText(MagicPanels.unit2gui(0))
			self.mc2E.setFixedWidth(mfsize)
			self.mc2E.move(rside-mfsize, rowmc)

			rowmc += 50
			
			# label
			self.mc4L = QtGui.QLabel(translate('magicMove', 'Mirror along X:'), self)
			self.mc4L.move(10, rowmc+3)

			# button
			self.mc4B1 = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.mc4B1.clicked.connect(self.createMirrorX)
			self.mc4B1.setFixedWidth(btsize2x)
			self.mc4B1.move(bc1, rowmc)
			self.mc4B1.setAutoRepeat(False)
	
			rowmc += 30

			# label
			self.mc5L = QtGui.QLabel(translate('magicMove', 'Mirror along Y:'), self)
			self.mc5L.move(10, rowmc+3)

			# button
			self.mc5B1 = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.mc5B1.clicked.connect(self.createMirrorY)
			self.mc5B1.setFixedWidth(btsize2x)
			self.mc5B1.move(bc1, rowmc)
			self.mc5B1.setAutoRepeat(False)

			rowmc += 30
			
			# label
			self.mc6L = QtGui.QLabel(translate('magicMove', 'Mirror along Z:'), self)
			self.mc6L.move(10, rowmc+3)

			# button
			self.mc6B1 = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.mc6B1.clicked.connect(self.createMirrorZ)
			self.mc6B1.setFixedWidth(btsize2x)
			self.mc6B1.move(bc1, rowmc)
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
			
			if self.gCornerCrossSupport == True:
			
				# label
				self.cocL = QtGui.QLabel(translate('magicMove', 'Corner cross:'), self)
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
				self.cecL = QtGui.QLabel(translate('magicMove', 'Center cross:'), self)
				self.cecL.move(10, row+3)

				# button
				self.cecB1 = QtGui.QPushButton(translate('magicMove', 'on'), self)
				self.cecB1.clicked.connect(self.setCenterOn)
				self.cecB1.setFixedWidth(btsize)
				self.cecB1.move(bc1, row)
				self.cecB1.setAutoRepeat(True)
				
				# button
				self.cecB2 = QtGui.QPushButton(translate('magicMove', 'off'), self)
				self.cecB2.clicked.connect(self.setCenterOff)
				self.cecB2.setFixedWidth(btsize)
				self.cecB2.move(bc2, row)
				self.cecB2.setAutoRepeat(True)

			if self.gCornerCrossSupport == True or self.gAxisCrossSupport == True:
				
				row += 25
				
				self.kccscb = QtGui.QCheckBox(translate('magicMove', ' - keep custom cross settings'), self)
				self.kccscb.setCheckState(QtCore.Qt.Unchecked)
				self.kccscb.move(10, row+3)
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()

			# init
			if self.gAxisCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			
			if self.gCornerCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(50)
			
			self.getSelected()

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def resetGlobals(self):
			
			self.gLCPX = dict() 
			self.gLCPY = dict() 
			self.gLCPZ = dict() 
			self.gLCPR = dict()

			self.gNewContainerON = False
			self.gContainerRef = "root"

		# ############################################################################
		def setNewContainer(self):
			self.gNewContainerON = True
			self.gNewContainerB1.setDisabled(True)

		# ############################################################################
		def toContainer(self, iCopy, iObject):
			
			# create new container with copy inside
			if self.gNewContainerON == True:

				container = MagicPanels.createContainer([ iCopy ])
				
				# if you want sub-container
				#if self.gContainerRef != "root":
				#	MagicPanels.moveToContainer([ container ], self.gContainerRef)
				
				# I guess it will be better to keep the same container level
				MagicPanels.moveToContainer([ container ], iObject, "LinkGroup")
				
				self.gContainerRef = container
				self.gNewContainerON = False
				self.gNewContainerB1.setDisabled(False)
			
			# copy to existing container
			else:
			
				if self.gContainerRef != "root":
					MagicPanels.moveToContainer([ iCopy ], self.gContainerRef)
				else:
					MagicPanels.moveToContainer([ iCopy ], iObject, "LinkGroup")

		# ############################################################################
		def setMove(self, iType):
			
			for o in self.gObjects:

				# calculate step
				step = MagicPanels.unit2value(self.oStepE.text())
				
				[ x, y, z ] = [ 0, 0, 0 ]
				
				if iType == "Xp":
					x = step
				
				if iType == "Xm":
					x = - step

				if iType == "Yp":
					y = step

				if iType == "Ym":
					y = - step

				if iType == "Zp":
					z = step

				if iType == "Zm":
					z = - step
				
				# get safe object to move
				toMove = MagicPanels.getObjectToMove(o)
				
				# set offset to object
				if self.animcb.isChecked():
					
					# store the position to avoid step problem after animation
					[ backupX, backupY, backupZ ] = MagicPanels.getPosition(toMove, "local")
					
					# run animation just for fun
					[ stepX, stepY, stepZ ] = [ 0, 0, 0 ]
					
					if x != 0:
						stepX = x/100
					if y != 0:
						stepY = y/100
					if z != 0:
						stepZ = z/100
					
					for i in range(1, 100):
						
						if i < 50:
							anim = 0.001
						elif i < 80:
							anim = 0.05
						else:
							anim = 0.08
						
						MagicPanels.setPosition(toMove, stepX, stepY, stepZ, "offset")
						time.sleep(anim)
						FreeCADGui.updateGui()
					
					# set correct position
					MagicPanels.setPosition(toMove, backupX, backupY, backupZ, "local")
					MagicPanels.setPosition(toMove, x, y, z, "offset")
					
				else:
				
					MagicPanels.setPosition(toMove, x, y, z, "offset")

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
			
			# start point
			sx = float(self.gMTESEdge.CenterOfMass.x)
			sy = float(self.gMTESEdge.CenterOfMass.y)
			sz = float(self.gMTESEdge.CenterOfMass.z)
			[[ sx, sy, sz ]] = MagicPanels.getVerticesPosition([[sx, sy, sz]], self.gMTESObj, "array")
			
			# end point
			ex = float(self.gMTEEEdge.CenterOfMass.x)
			ey = float(self.gMTEEEdge.CenterOfMass.y)
			ez = float(self.gMTEEEdge.CenterOfMass.z)
			[[ ex, ey, ez ]] = MagicPanels.getVerticesPosition([[ex, ey, ez]], self.gMTEEObj, "array")
			
			# calculate the gap for axis
			if iType == "X":
				gap = abs(ex - sx)
		
			if iType == "Y":
				gap = abs(ey - sy)
			
			if iType == "Z":
				gap = abs(ez - sz)
		
			# calculate the equal space between objects for axis
			num = len(self.gObjects)
			thick = 0
			
			for o in self.gObjects:
				
				[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)
				
				if iType == "X":
					thick = thick + sizeX
				
				if iType == "Y":
					thick = thick + sizeY
				
				if iType == "Z":
					thick = thick + sizeZ

			offset = (gap - thick) / (num + 1)
			
			# set equal space to objects
			i = 0
			for o in self.gObjects:
				
				# get object data
				[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)
				toMove = MagicPanels.getObjectToMove(o)
				
				# calculate start point for axis
				[ startX, startY, startZ ] = MagicPanels.getPosition(o, "global")
			
				if iType == "X":
					startX = sx
			
				if iType == "Y":
					startY = sy
				
				if iType == "Z":
					startZ = sz
	
				# move to start point
				MagicPanels.setPosition(toMove, startX, startY, startZ, "global")
				
				# calculate offset for axis and move object
				[ offsetX, offsetY, offsetZ ] = [ 0, 0, 0 ]
				
				if iType == "X":
					offsetX = ((i + 1) * offset) + (i * sizeX)
				
				if iType == "Y":
					offsetY = ((i + 1) * offset) + (i * sizeY)
				
				if iType == "Z":
					offsetZ = ((i + 1) * offset) + (i * sizeZ)
				
				MagicPanels.setPosition(toMove, offsetX, offsetY, offsetZ, "offset")
				i = i + 1

			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createCopy(self, iType):
			
			for o in self.gObjects:
				
				# get safe object to copy
				toCopy = MagicPanels.getObjectToCopy(o)
				
				# create copy
				if self.gCopyType == 0:
					copy = MagicPanels.copyPanel([ toCopy ], "copyObject")[0]
				if self.gCopyType == 1:
					copy = MagicPanels.copyPanel([ toCopy ], "Clone")[0]
				if self.gCopyType == 2:
					copy = MagicPanels.copyPanel([ toCopy ], "Link")[0]
				if self.gCopyType == 3:
					copy = MagicPanels.copyPanel([ toCopy ], "auto")[0]

				# move copy to container to update its global position
				if (
					o.isDerivedFrom("Sketcher::SketchObject") or 
					o.isDerivedFrom("Part::Part2DObjectPython") 
				):
					containers = MagicPanels.getContainers(o)
					MagicPanels.moveToContainer([ copy ], containers[0])
				else:
					self.toContainer(copy, o)
				
				# move copy to object position
				if o.isDerivedFrom("Sketcher::SketchObject"):
					[ toCopyX, toCopyY, toCopyZ ] = MagicPanels.getPosition(copy, "global")
				else:
					[ toCopyX, toCopyY, toCopyZ ] = MagicPanels.getPosition(toCopy, "global")
				
				MagicPanels.setPosition(copy, toCopyX, toCopyY, toCopyZ, "global")
				
				# set colors to copy from selected object
				MagicPanels.copyColors(o, copy)
				
				# not use getSizes because you need occupied space along axis
				[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)
				
				# calculate offset
				step = MagicPanels.unit2value(self.oStepE.text())
				key = str(o.Name)
		
				try:
					[ x, y, z ] = [ self.gLCPX[key], self.gLCPY[key], self.gLCPZ[key] ]
				except:
					[ x, y, z ] = [ 0, 0, 0 ] 
				
				if iType == "Xp":
					x = x + sizeX + step
				
				if iType == "Xm":
					x = x - sizeX - step

				if iType == "Yp":
					y = y + sizeY + step

				if iType == "Ym":
					y = y - sizeY - step

				if iType == "Zp":
					z = z + sizeZ + step

				if iType == "Zm":
					z = z - sizeZ - step

				# set offset to copy
				MagicPanels.setPosition(copy, x, y, z, "offset")
				
				# save copy offset, not position
				[ self.gLCPX[key], self.gLCPY[key], self.gLCPZ[key] ] = [ x, y, z ]

			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def setCopyByEdge(self):
			
			try:
				self.gCBEObj = FreeCADGui.Selection.getSelection()[0]
				self.gCBEEdge = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				if self.gCBEEdge.ShapeType == "Edge":
					index = MagicPanels.getEdgeIndex(self.gCBEObj, self.gCBEEdge)
					self.cbe1L.setText(self.gCBEObj.Label + ", Edge" + str(index))
				
				elif self.gCBEEdge.ShapeType == "Face":
					index = MagicPanels.getFaceIndex(self.gCBEObj, self.gCBEEdge)
					self.cbe1L.setText(self.gCBEObj.Label + ", Face" + str(index))
				
				else:
					raise
				
			except:
				self.cbe1L.setText(self.gNoCopyByEdge)
				
		# ############################################################################
		def createCopyByEdge(self, iType):
			
			offset = MagicPanels.unit2value(self.cbe5E.text())
			
			for o in self.gObjects:
				
				# get object to copy to avoid PartDesign object destruction (only in auto mode)
				if self.gCopyType == 3:
					toCopy = MagicPanels.getObjectToCopy(o)
				else:
					toCopy = o
				
				# create copy
				if self.gCopyType == 0:
					copy = MagicPanels.copyPanel([ toCopy ], "copyObject")[0]
				if self.gCopyType == 1:
					copy = MagicPanels.copyPanel([ toCopy ], "Clone")[0]
				if self.gCopyType == 2:
					copy = MagicPanels.copyPanel([ toCopy ], "Link")[0]
				if self.gCopyType == 3:
					copy = MagicPanels.copyPanel([ toCopy ], "auto")[0]

				# move copy to container to update its global position
				if (
					o.isDerivedFrom("Sketcher::SketchObject") or 
					o.isDerivedFrom("Part::Part2DObjectPython") 
				):
					containers = MagicPanels.getContainers(o)
					MagicPanels.moveToContainer([ copy ], containers[0])
				else:
					self.toContainer(copy, o)
				
				# move copy to object position
				if o.isDerivedFrom("Sketcher::SketchObject"):
					[ toCopyX, toCopyY, toCopyZ ] = MagicPanels.getPosition(copy, "global")
				else:
					[ toCopyX, toCopyY, toCopyZ ] = MagicPanels.getPosition(toCopy, "global")
				
				MagicPanels.setPosition(copy, toCopyX, toCopyY, toCopyZ, "global")
				
				# set colors to copy from selected object
				MagicPanels.copyColors(o, copy)
				
				# set the center copy by edge point
				ex = float(self.gCBEEdge.CenterOfMass.x)
				ey = float(self.gCBEEdge.CenterOfMass.y)
				ez = float(self.gCBEEdge.CenterOfMass.z)
				[[ ex, ey, ez ]] = MagicPanels.getVerticesPosition([[ex, ey, ez]], self.gCBEObj, "array")
				
				# not use getSizes because you need occupied space along axis
				[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)
				
				# calculate offset
				[ x, y, z ] = [ 0, 0, 0 ]
				
				if iType == "X":

					diff = abs(ex - toCopyX)
					destination = 2 * diff
				
					# copy from left side to right
					if toCopyX < ex:
						x = destination - sizeX + offset

					# copy from right side to left
					else:
						x = - destination - sizeX - offset
					
				if iType == "Y":
					
					diff = abs(ey - toCopyY)
					destination = 2 * diff
					
					# copy from left side to right
					if toCopyY < ey:
						y = destination - sizeY + offset
					
					# copy from right side to left
					else:
						y = - destination - sizeY - offset
					
				if iType == "Z":
					
					diff = abs(ez - toCopyZ)
					destination = 2 * diff

					# copy from left side to right
					if toCopyZ < ez:
						z = destination - sizeZ + offset
					
					# copy from right side to left
					else:
						z = - destination - sizeZ - offset
				
				# set offset to copy
				MagicPanels.setPosition(copy, x, y, z, "offset")
			
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def setLastPathPosition(self):
			for o in self.gObjects:
				
				key = str(o.Name)
				toCopy = MagicPanels.getObjectToMove(o)
				
				[ x, y, z, r ] = MagicPanels.getContainerPlacement(toCopy, "clean")
				v = FreeCAD.Vector(x, y, z)
				inside = self.gPathObj.Shape.isInside(v, 0, True)
				
				if inside:
					self.gPathLast[key] = self.gPathPoints.index(v)
					self.gPathInit[key] = False
				else:
					self.gPathLast[key] = 0
					self.gPathInit[key] = True

				self.gPathRotation[key] = r
		
		# ############################################################################
		def setCopyPath(self):
			
			try:
				self.gPathObj = FreeCADGui.Selection.getSelection()[0]
				
				# support wire, sketch, helix
				test1 = self.gPathObj.isDerivedFrom("Sketcher::SketchObject")
				test2 = self.gPathObj.isDerivedFrom("Part::Part2DObjectPython")
				test3 = self.gPathObj.isDerivedFrom("Part::Helix")
				
				if test1 or test2 or test3:
					
					self.gPathPoints = self.gPathObj.Shape.getPoints(1)[0]
					self.oPathRotZL.setText(self.gPathObj.Label)
					self.setLastPathPosition()
				
				# support edges
				else:
					
					sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
					
					if sub.ShapeType != "Edge":
						raise
					
					self.gPathPoints = sub.getPoints(1)[0]
					index = MagicPanels.getEdgeIndex(self.gPathObj, sub)
					self.oPathRotZL.setText(self.gPathObj.Label + ", Edge" + str(index))
					self.setLastPathPosition()
			
			except:
				self.oPathRotZL.setText(self.gNoPathSelection)

		# ############################################################################
		def createPathPanel(self):
			
			for o in self.gObjects:
				
				# get safe object to copy
				toCopy = MagicPanels.getObjectToCopy(o)
					
				if self.gCopyType == 0:
					copy = MagicPanels.copyPanel([ toCopy ], "copyObject")[0]
				if self.gCopyType == 1:
					copy = MagicPanels.copyPanel([ toCopy ], "Clone")[0]
				if self.gCopyType == 2:
					copy = MagicPanels.copyPanel([ toCopy ], "Link")[0]
				if self.gCopyType == 3:
					copy = MagicPanels.copyPanel([ toCopy ], "auto")[0]

				# move copy to container to update its global position
				self.toContainer(copy, o)
				
				# set colors to copy from selected object
				MagicPanels.copyColors(o, copy)
				
				# calculate position
				key = str(o.Name)
				index = self.gPathLast[key]
				
				# you could add step after object select
				# but it is more comfortable for user 
				# first add object, than change step and click create
				# so the create function must recalculate the step
				if self.gPathInit[key] == False:
					step = int(self.oPathStepE.text())
					self.gPathLast[key] = int(self.gPathLast[key] + step)
					index = index + step

				if index > len(self.gPathPoints) - 1:
					return
			
				x = self.gPathPoints[index].x
				y = self.gPathPoints[index].y
				z = self.gPathPoints[index].z
				[[ x, y, z ]] = MagicPanels.getVerticesPosition([[x, y, z]], self.gPathObj, "array")
				
				# move copy to object position
				MagicPanels.setPosition(copy, x, y, z, "global")
				
				# set rotation
				angleX = float(self.oPathRotXE.text())
				angleY = float(self.oPathRotYE.text())
				angleZ = float(self.oPathRotZE.text())
				
				rotX = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), angleX)
				rotY = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), angleY)
				rotZ = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), angleZ)
				
				copy.Placement.Rotation = self.gPathRotation[key] * rotX * rotY * rotZ
				
				# save rotation and position
				step = int(self.oPathStepE.text())
				self.gPathRotation[key] = copy.Placement.Rotation
				self.gPathLast[key] = int(self.gPathLast[key] + step)
				self.gPathInit[key] = True
				
			FreeCAD.ActiveDocument.recompute()
			
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
				
				[[ x, y, z ]] = MagicPanels.getVerticesPosition([[x, y, z]], self.gMObj, "array")
				
				self.mc1L.setText(info)
				self.mc31E.setText(MagicPanels.unit2gui(x))
				self.mc32E.setText(MagicPanels.unit2gui(y))
				self.mc33E.setText(MagicPanels.unit2gui(z))

			except:
				self.mc1L.setText(self.gNoMirrorPoint)
		
		# ############################################################################
		def createMirror(self, iType):
			
			for o in self.gObjects:
				
				# init
				extraOffset = MagicPanels.unit2value(self.mc2E.text())
				centerX = MagicPanels.unit2value(self.mc31E.text())
				centerY = MagicPanels.unit2value(self.mc32E.text())
				centerZ = MagicPanels.unit2value(self.mc33E.text())

				# get safe object to copy
				toCopy = MagicPanels.getObjectToCopy(o)
				
				# set auto type
				auto = 0
				if self.gMirrorType == 0:
					if toCopy.isDerivedFrom("Part::Box"):
						auto = 1
					else:
						auto = 2
					
				# ############################################################################
				# mirror using LinkGroup container
				# ############################################################################
				if self.gMirrorType == 1 or auto == 1:
					
					if iType == "X":
						direction = (1, 0, 0)
						offX = extraOffset
						offY = 0
						offZ = 0
					
					if iType == "Y":
						direction = (0, 1, 0)
						offX = 0
						offY = extraOffset
						offZ = 0
					
					if iType == "Z":
						direction = (0, 0, 1)
						offX = 0
						offY = 0
						offZ = extraOffset
			
					# not create mirror directly at object because 
					# it will not be managed, extended later
					# create LinkGroup and move the object to the LinkGroup
					# and create Mirror at LinkGroup instead
					if (
						o.isDerivedFrom("Part::Box") or 
						o.isDerivedFrom("App::Part") 
						):
						o = MagicPanels.createContainer([o])
					else:
						info = "\n"
						info += str(o.Label) + " " 
						info += translate('magicMove', 'is not supported. Currently supported objects are only Part::Box and App::Part. If you want to create this parametric mirror for PartDesign object, please select Part container. \n')
						FreeCAD.Console.PrintMessage(info)
						info = translate('magicMove', 'select Part::Box or App::Part instead')
						self.s1S.setText(info)
						continue

					mirror = FreeCAD.ActiveDocument.addObject('Part::Mirroring', "mirror")
					mirror.Label = "Mirror, " + str(o.Label) + " "
					mirror.Source = FreeCAD.ActiveDocument.getObject(o.Name)
					mirror.Normal = direction
					mirror.Base = (centerX, centerY, centerZ)
					
					MagicPanels.setContainerPlacement(mirror, offX, offY, offZ, 0, "clean")
					
					# try to copy colors
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

					FreeCAD.ActiveDocument.recompute()
				
				# ############################################################################
				# mirror with Clone
				# ############################################################################
				if self.gMirrorType == 2 or auto == 2:
					
					# create mirror clone
					copy = MagicPanels.copyPanel([ toCopy ], "Clone")[0]
					if iType == "X":
						copy.Scale.x = -1
					if iType == "Y":
						copy.Scale.y = -1
					if iType == "Z":
						copy.Scale.z = -1
					
					# move copy to container to update its global position
					if (
						o.isDerivedFrom("Sketcher::SketchObject") or 
						o.isDerivedFrom("Part::Part2DObjectPython") 
					):
						containers = MagicPanels.getContainers(o)
						MagicPanels.moveToContainer([ copy ], containers[0])
					else:
						self.toContainer(copy, o)
					
					# move copy to object position
					# mirror Clone is reflected from the center of the (0, 0, 0) XYZ
					# so mirror will be in a different place
					[ X, Y, Z ] = MagicPanels.getPosition(o, "global")
					MagicPanels.setPosition(copy, X, Y, Z, "global")
					
					# set colors to copy from selected object
					MagicPanels.copyColors(o, copy)
					
					# not use getSizes because you need occupied space along axis
					[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)

					# calculate offset
					[ x, y, z ] = [ 0, 0, 0 ]
					
					if iType == "X":
						
						diff = abs(centerX - X)
						pos = 2 * diff
					
						# copy from left side to right
						if X < centerX:
							x = pos - sizeX + extraOffset

						# copy from right side to left
						else:
							x = - pos - sizeX - extraOffset
						
					if iType == "Y":
						
						diff = abs(centerY - Y)
						pos = 2 * diff
						
						# copy from left side to right
						if Y < centerY:
							y = pos - sizeY + extraOffset
						
						# copy from right side to left
						else:
							y = - pos - sizeY - extraOffset
						
					if iType == "Z":
						
						diff = abs(centerZ - Z)
						pos = 2 * diff

						# copy from left side to right
						if Z < centerZ:
							z = pos - sizeZ + extraOffset
						
						# copy from right side to left
						else:
							z = - pos - sizeZ - extraOffset
					
					# set offset to copy
					MagicPanels.setPosition(copy, x, y, z, "offset")
					FreeCAD.ActiveDocument.recompute()

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
			
			self.oPathStepE.hide()
			self.pathB1.hide()
			self.pathB2.hide()
			self.oPathRotXL.hide()
			self.oPathRotYL.hide()
			self.oPathRotZL.hide()
			self.oPathRotXE.hide()
			self.oPathRotYE.hide()
			self.oPathRotZE.hide()
			
			self.o1L.hide()
			self.o1B1.hide()
			self.o1B2.hide()
			
			self.o2L.hide()
			self.o2B1.hide()
			self.o2B2.hide()
			
			self.o3L.hide()
			self.o3B1.hide()
			self.o3B2.hide()
			
			self.oStepL.hide()
			self.oStepE.hide()
			
			self.animcb.hide()
			
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
			self.sMirrorType.hide()
			self.gNewContainerB1.hide()
			
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
				
				self.oStepL.show()
				self.oStepE.show()
				
				self.animcb.show()
				
				self.o1L.setText(self.gInfoMoveX)
				self.o2L.setText(self.gInfoMoveY)
				self.o3L.setText(self.gInfoMoveZ)
				self.oStepL.setText(self.gInfoMoveStep)

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
				
				self.oStepL.show()
				self.oStepE.show()
				
				self.o1L.setText(self.gInfoCopyX)
				self.o2L.setText(self.gInfoCopyY)
				self.o3L.setText(self.gInfoCopyZ)
				self.oStepL.setText(self.gInfoCopyStep)
				
				self.sCopyType.show()
				self.gNewContainerB1.show()

			# Copy by Path
			if selectedIndex == 2:
				
				self.oPathRotXL.show()
				self.oPathRotXE.show()
				
				self.oPathRotYL.show()
				self.oPathRotYE.show()
				
				self.oPathRotZL.show()
				self.oPathRotZE.show()
				
				self.oPathStepE.show()
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
				
				self.sMirrorType.show()
	
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
		def setMirrorType(self, selectedText):
			self.gMirrorType = getMenuIndex3[selectedText]
		
		# ############################################################################
		def setX1(self):
			
			try:
				if self.gModeType == 0:
					self.setMove("Xm")
					
				if self.gModeType == 1:
					self.createCopy("Xm")

			except:
				self.s1S.setText(self.gNoSelection)
			
		def setX2(self):
			
			try:
				if self.gModeType == 0:
					self.setMove("Xp")
					
				if self.gModeType == 1:
					self.createCopy("Xp")

			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def setY1(self):
			
			try:
				if self.gModeType == 0:
					self.setMove("Ym")
					
				if self.gModeType == 1:
					self.createCopy("Ym")
			
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setY2(self):
			
			try:
				if self.gModeType == 0:
					self.setMove("Yp")
					
				if self.gModeType == 1:
					self.createCopy("Yp")

			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def setZ1(self):
			
			try:
				if self.gModeType == 0:
					self.setMove("Zm")
					
				if self.gModeType == 1:
					self.createCopy("Zm")
				
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setZ2(self):
			
			try:
				if self.gModeType == 0:
					self.setMove("Zp")
					
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
		def getSelected(self):

			try:

				self.resetGlobals()
				self.gObjects = FreeCADGui.Selection.getSelection()
				
				sizes = []
				sizes = MagicPanels.getSizes(self.gObjects[0])
				sizes.sort()
					
				self.oStepE.setText(MagicPanels.unit2gui( sizes[0] ))
				
				if len(self.gObjects) > 1:
					self.s1S.setText("Multi, "+str(self.gObjects[0].Label))
				else:
					self.s1S.setText(str(self.gObjects[0].Label))
				
				self.oPathStepE.setText(str(self.gPathStep))
				self.gPathStep = sizes[1]
				
				if self.gPathObj != "":
					self.setLastPathPosition()

				FreeCADGui.Selection.clearSelection()

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

