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
		
		gInfoPath1 = translate('magicMove', 'Rotation X, Y, Z:')
		gInfoPath2 = translate('magicMove', 'Next point step:')

		gNoSelection = translate('magicMove', 'select object to move or copy')
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
			toolSW = 280
			toolSH = 480
			
			area = toolSW - 20          # full gui area
			rside = toolSW - 10         # right side of the GUI
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 0 + 50
			gPH = int( gSH - toolSH ) - 30

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicMove', 'magicMove'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			
			# ############################################################################
			# GUI for header
			# ############################################################################
			
			# screen
			self.s1S = QtGui.QLabel("", self)
			self.s1S.setMaximumWidth(area)
			
			# button
			self.s1B1 = QtGui.QPushButton(translate('magicMove', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedHeight(40)
			
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
			self.sMode.setMinimumWidth(150)
			
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
			self.sCopyType.setMinimumWidth(110)
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
			self.sMirrorType.setMinimumWidth(110)
			self.sMirrorType.hide()
			
			# button
			self.gNewContainerB1 = QtGui.QPushButton(translate('magicMove', 'copy to new container'), self)
			self.gNewContainerB1.clicked.connect(self.setNewContainer)
			self.gNewContainerB1.setFixedHeight(40)
			self.gNewContainerB1.hide()

			# ############################################################################
			# settigns
			# ############################################################################
			
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
			# GUI for Move
			# ############################################################################

			# label
			self.oMove1L = QtGui.QLabel(translate('magicMove', 'Move along X:'), self)

			# button
			self.oMove1B1 = QtGui.QPushButton("X-", self)
			self.oMove1B1.clicked.connect(self.setMoveX1)
			self.oMove1B1.setFixedWidth(btsize)
			self.oMove1B1.setAutoRepeat(True)
			
			# button
			self.oMove1B2 = QtGui.QPushButton("X+", self)
			self.oMove1B2.clicked.connect(self.setMoveX2)
			self.oMove1B2.setFixedWidth(btsize)
			self.oMove1B2.setAutoRepeat(True)
			
			# label
			self.oMove2L = QtGui.QLabel(translate('magicMove', 'Move along Y:'), self)
			
			# button
			self.oMove2B1 = QtGui.QPushButton("Y-", self)
			self.oMove2B1.clicked.connect(self.setMoveY1)
			self.oMove2B1.setFixedWidth(btsize)
			self.oMove2B1.setAutoRepeat(True)
			
			# button
			self.oMove2B2 = QtGui.QPushButton("Y+", self)
			self.oMove2B2.clicked.connect(self.setMoveY2)
			self.oMove2B2.setFixedWidth(btsize)
			self.oMove2B2.setAutoRepeat(True)

			# label
			self.oMove3L = QtGui.QLabel(translate('magicMove', 'Move along Z:'), self)
			
			# button
			self.oMove3B1 = QtGui.QPushButton("Z-", self)
			self.oMove3B1.clicked.connect(self.setMoveZ1)
			self.oMove3B1.setFixedWidth(btsize)
			self.oMove3B1.setAutoRepeat(True)
			
			# button
			self.oMove3B2 = QtGui.QPushButton("Z+", self)
			self.oMove3B2.clicked.connect(self.setMoveZ2)
			self.oMove3B2.setFixedWidth(btsize)
			self.oMove3B2.setAutoRepeat(True)
			
			# label
			self.oMoveStepL = QtGui.QLabel(translate('magicMove', 'Move step:'), self)
			self.oMoveStepL.setFixedWidth(100)
			
			# text input
			self.oMoveStepE = QtGui.QLineEdit(self)
			self.oMoveStepE.setText(MagicPanels.unit2gui(100))
			self.oMoveStepE.setFixedWidth(tfsizeLong)
			
			self.animcb = QtGui.QCheckBox(translate('magicMove', ' - animate move'), self)
			self.animcb.setCheckState(QtCore.Qt.Unchecked)
			
			# ############################################################################
			# GUI for Copy
			# ############################################################################

			# label
			self.oCopy1L = QtGui.QLabel(translate('magicMove', 'Copy along X:'), self)

			# button
			self.oCopy1B1 = QtGui.QPushButton("X-", self)
			self.oCopy1B1.clicked.connect(self.setCopyX1)
			self.oCopy1B1.setFixedWidth(btsize)
			self.oCopy1B1.setAutoRepeat(True)
			
			# button
			self.oCopy1B2 = QtGui.QPushButton("X+", self)
			self.oCopy1B2.clicked.connect(self.setCopyX2)
			self.oCopy1B2.setFixedWidth(btsize)
			self.oCopy1B2.setAutoRepeat(True)
			
			# label
			self.oCopy2L = QtGui.QLabel(translate('magicMove', 'Copy along Y:'), self)
			
			# button
			self.oCopy2B1 = QtGui.QPushButton("Y-", self)
			self.oCopy2B1.clicked.connect(self.setCopyY1)
			self.oCopy2B1.setFixedWidth(btsize)
			self.oCopy2B1.setAutoRepeat(True)
			
			# button
			self.oCopy2B2 = QtGui.QPushButton("Y+", self)
			self.oCopy2B2.clicked.connect(self.setCopyY2)
			self.oCopy2B2.setFixedWidth(btsize)
			self.oCopy2B2.setAutoRepeat(True)

			# label
			self.oCopy3L = QtGui.QLabel(translate('magicMove', 'Copy along Z:'), self)
			
			# button
			self.oCopy3B1 = QtGui.QPushButton("Z-", self)
			self.oCopy3B1.clicked.connect(self.setCopyZ1)
			self.oCopy3B1.setFixedWidth(btsize)
			self.oCopy3B1.setAutoRepeat(True)
			
			# button
			self.oCopy3B2 = QtGui.QPushButton("Z+", self)
			self.oCopy3B2.clicked.connect(self.setCopyZ2)
			self.oCopy3B2.setFixedWidth(btsize)
			self.oCopy3B2.setAutoRepeat(True)
			
			# label
			self.oCopyStepL = QtGui.QLabel(translate('magicMove', 'Copy offset:'), self)
			self.oCopyStepL.setFixedWidth(100)
			
			# text input
			self.oCopyStepE = QtGui.QLineEdit(self)
			self.oCopyStepE.setText(MagicPanels.unit2gui(100))
			self.oCopyStepE.setFixedWidth(tfsizeLong)
			
			# ############################################################################
			# GUI for Move to Equal
			# ############################################################################
			
			self.mte1B = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.mte1B.clicked.connect(self.setMEEdgeStart)
			self.mte1B.setFixedWidth(btsize)
			
			self.mte1L = QtGui.QLabel(self.gNoMEEdgeStart, self)
			self.mte1L.setMaximumWidth(area-100)
			
			self.mte2B = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.mte2B.clicked.connect(self.setMEEdgeEnd)
			self.mte2B.setFixedWidth(btsize)
			
			self.mte2L = QtGui.QLabel(self.gNoMEEdgeEnd, self)
			self.mte2L.setMaximumWidth(area-100)
			
			# button
			self.mte12B = QtGui.QPushButton(translate('magicMove', 'set both edges'), self)
			self.mte12B.clicked.connect(self.setMEEdge)
			self.mte12B.setFixedHeight(40)
			
			# label
			self.mte3L = QtGui.QLabel(translate('magicMove', 'Equal space along X:'), self)

			# button
			self.mte3B = QtGui.QPushButton(translate('magicMove', 'move'), self)
			self.mte3B.clicked.connect(self.createMoveToEqualX)
			self.mte3B.setFixedWidth(btsize2x)
			self.mte3B.setAutoRepeat(False)

			# label
			self.mte4L = QtGui.QLabel(translate('magicMove', 'Equal space along Y:'), self)

			# button
			self.mte4B = QtGui.QPushButton(translate('magicMove', 'move'), self)
			self.mte4B.clicked.connect(self.createMoveToEqualY)
			self.mte4B.setFixedWidth(btsize2x)
			self.mte4B.setAutoRepeat(False)

			# label
			self.mte5L = QtGui.QLabel(translate('magicMove', 'Equal space along Z:'), self)

			# button
			self.mte5B = QtGui.QPushButton(translate('magicMove', 'move'), self)
			self.mte5B.clicked.connect(self.createMoveToEqualZ)
			self.mte5B.setFixedWidth(btsize2x)
			self.mte5B.setAutoRepeat(False)
			
			# ############################################################################
			# GUI for Copy by Edge
			# ############################################################################
			
			self.cbe1B = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.cbe1B.clicked.connect(self.setCopyByEdge)
			self.cbe1B.setFixedWidth(btsize)
			
			self.cbe1L = QtGui.QLabel(self.gNoCopyByEdge, self)
			self.cbe1L.setMaximumWidth(area-100)
			
			# label
			self.cbe2L = QtGui.QLabel(translate('magicMove', 'Copy along X:'), self)

			# button
			self.cbe2B = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.cbe2B.clicked.connect(self.createCopyByEdgeX)
			self.cbe2B.setFixedWidth(btsize2x)
			self.cbe2B.setAutoRepeat(False)

			# label
			self.cbe3L = QtGui.QLabel(translate('magicMove', 'Copy along Y:'), self)

			# button
			self.cbe3B = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.cbe3B.clicked.connect(self.createCopyByEdgeY)
			self.cbe3B.setFixedWidth(btsize2x)
			self.cbe3B.setAutoRepeat(False)

			# label
			self.cbe4L = QtGui.QLabel(translate('magicMove', 'Copy along Z:'), self)

			# button
			self.cbe4B = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.cbe4B.clicked.connect(self.createCopyByEdgeZ)
			self.cbe4B.setFixedWidth(btsize2x)
			self.cbe4B.setAutoRepeat(False)

			# label
			self.cbe5L = QtGui.QLabel(translate('magicMove', 'Additional offset:'), self)

			# text input
			self.cbe5E = QtGui.QLineEdit(self)
			self.cbe5E.setText(MagicPanels.unit2gui(0))
			self.cbe5E.setFixedWidth(tfsizeLong)

			# ############################################################################
			# GUI for Path
			# ############################################################################
			
			self.oPathBS = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.oPathBS.clicked.connect(self.setCopyPath)
			self.oPathBS.setFixedWidth(btsize)
			
			self.oPathCurveL = QtGui.QLabel(self.gNoPathSelection, self)
			self.oPathCurveL.setMaximumWidth(area-100)
			
			self.oPathRotL = QtGui.QLabel(self.gInfoPath1, self)
			
			self.oPathRotXE = QtGui.QLineEdit(self)
			self.oPathRotXE.setText("0")
			self.oPathRotXE.setFixedWidth(rfs)
			
			self.oPathRotYE = QtGui.QLineEdit(self)
			self.oPathRotYE.setText("0")
			self.oPathRotYE.setFixedWidth(rfs)
	
			self.oPathRotZE = QtGui.QLineEdit(self)
			self.oPathRotZE.setText("0")
			self.oPathRotZE.setFixedWidth(rfs)

			self.oPathStepL = QtGui.QLabel(self.gInfoPath2, self)
			
			self.oPathStepE = QtGui.QLineEdit(self)
			self.oPathStepE.setText("1")
			self.oPathStepE.setFixedWidth(65)
			
			self.oPathBC = QtGui.QPushButton(translate('magicMove', 'copy along path'), self)
			self.oPathBC.clicked.connect(self.createPathPanel)
			self.oPathBC.setFixedHeight(40)
			self.oPathBC.setAutoRepeat(True)

			# ############################################################################
			# GUI for Mirror
			# ############################################################################
			
			self.mc1B = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.mc1B.clicked.connect(self.setMirrorPoint)
			self.mc1B.setFixedWidth(btsize)
			
			self.mc1L = QtGui.QLabel(self.gNoMirrorPoint, self)
			self.mc1L.setMaximumWidth(area-100)
			
			self.mc3L = QtGui.QLabel(translate('magicMove', 'Mirror XYZ:'), self)
			
			self.mc31E = QtGui.QLineEdit(self)
			self.mc31E.setText(MagicPanels.unit2gui(0))
			self.mc31E.setFixedWidth(mfsize)
			
			self.mc32E = QtGui.QLineEdit(self)
			self.mc32E.setText(MagicPanels.unit2gui(0))
			self.mc32E.setFixedWidth(mfsize)
			
			self.mc33E = QtGui.QLineEdit(self)
			self.mc33E.setText(MagicPanels.unit2gui(0))
			self.mc33E.setFixedWidth(tfsize)

			# label
			self.mc2L = QtGui.QLabel(translate('magicMove', 'Additional offset:'), self)

			# text input
			self.mc2E = QtGui.QLineEdit(self)
			self.mc2E.setText(MagicPanels.unit2gui(0))
			self.mc2E.setFixedWidth(mfsize)
			
			# label
			self.mc4L = QtGui.QLabel(translate('magicMove', 'Mirror along X:'), self)

			# button
			self.mc4B1 = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.mc4B1.clicked.connect(self.createMirrorX)
			self.mc4B1.setFixedWidth(btsize2x)
			self.mc4B1.setAutoRepeat(False)

			# label
			self.mc5L = QtGui.QLabel(translate('magicMove', 'Mirror along Y:'), self)

			# button
			self.mc5B1 = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.mc5B1.clicked.connect(self.createMirrorY)
			self.mc5B1.setFixedWidth(btsize2x)
			self.mc5B1.setAutoRepeat(False)
			
			# label
			self.mc6L = QtGui.QLabel(translate('magicMove', 'Mirror along Z:'), self)

			# button
			self.mc6B1 = QtGui.QPushButton(translate('magicMove', 'create'), self)
			self.mc6B1.clicked.connect(self.createMirrorZ)
			self.mc6B1.setFixedWidth(btsize2x)
			self.mc6B1.setAutoRepeat(False)
			
			# ############################################################################
			# GUI for common foot
			# ############################################################################
			
			if self.gCornerCrossSupport == True:
			
				# label
				self.cocL = QtGui.QLabel(translate('magicMove', 'Corner cross:'), self)

				# button
				self.cocB1 = QtGui.QPushButton("-", self)
				self.cocB1.clicked.connect(self.setCornerM)
				self.cocB1.setFixedWidth(btsize)
				self.cocB1.setAutoRepeat(True)
				
				# button
				self.cocB2 = QtGui.QPushButton("+", self)
				self.cocB2.clicked.connect(self.setCornerP)
				self.cocB2.setFixedWidth(btsize)
				self.cocB2.setAutoRepeat(True)

			if self.gAxisCrossSupport == True:
				
				# label
				self.cecL = QtGui.QLabel(translate('magicMove', 'Center cross:'), self)

				# button
				self.cecB1 = QtGui.QPushButton(translate('magicMove', 'on'), self)
				self.cecB1.clicked.connect(self.setCenterOn)
				self.cecB1.setFixedWidth(btsize)
				self.cecB1.setAutoRepeat(True)
				
				# button
				self.cecB2 = QtGui.QPushButton(translate('magicMove', 'off'), self)
				self.cecB2.clicked.connect(self.setCenterOff)
				self.cecB2.setFixedWidth(btsize)
				self.cecB2.setAutoRepeat(True)

			if self.gCornerCrossSupport == True or self.gAxisCrossSupport == True:

				self.kccscb = QtGui.QCheckBox(translate('magicMove', ' - keep custom cross settings'), self)
				self.kccscb.setCheckState(QtCore.Qt.Unchecked)
			
			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create header
			self.layoutHeader = QtGui.QVBoxLayout()
			self.row1 = QtGui.QHBoxLayout()
			self.row1.setAlignment(QtGui.Qt.AlignLeft)
			self.row1.addWidget(self.s1S)
			self.layoutHeader.addLayout(self.row1)
			self.row2 = QtGui.QHBoxLayout()
			self.row2.addWidget(self.s1B1)
			self.layoutHeader.addLayout(self.row2)
			self.row3 = QtGui.QHBoxLayout()
			self.row3.addWidget(self.sMode)
			self.row3.addStretch()
			self.row3.addWidget(self.sCopyType)
			self.row3.addWidget(self.sMirrorType)
			self.layoutHeader.addLayout(self.row3)
			self.row4 = QtGui.QHBoxLayout()
			self.row4.addWidget(self.gNewContainerB1)
			self.layoutHeader.addLayout(self.row4)
			
			# body - move
			self.layoutBodyMove = QtGui.QVBoxLayout()
			self.row5 = QtGui.QHBoxLayout()
			self.row5.addWidget(self.oMove1L)
			self.row5.addWidget(self.oMove1B1)
			self.row5.addWidget(self.oMove1B2)
			self.layoutBodyMove.addLayout(self.row5)
			self.row6 = QtGui.QHBoxLayout()
			self.row6.addWidget(self.oMove2L)
			self.row6.addWidget(self.oMove2B1)
			self.row6.addWidget(self.oMove2B2)
			self.layoutBodyMove.addLayout(self.row6)
			self.row7 = QtGui.QHBoxLayout()
			self.row7.addWidget(self.oMove3L)
			self.row7.addWidget(self.oMove3B1)
			self.row7.addWidget(self.oMove3B2)
			self.layoutBodyMove.addLayout(self.row7)
			self.layoutBodyMove.addSpacing(5)
			self.row8 = QtGui.QHBoxLayout()
			self.row8.addWidget(self.oMoveStepL)
			self.row8.addStretch()
			self.row8.addWidget(self.oMoveStepE)
			self.layoutBodyMove.addLayout(self.row8)
			self.layoutBodyMove.addSpacing(20)
			self.row9 = QtGui.QHBoxLayout()
			self.row9.addWidget(self.animcb)
			self.layoutBodyMove.addLayout(self.row9)
			self.groupBodyMove = QtGui.QGroupBox(None, self)
			self.groupBodyMove.setLayout(self.layoutBodyMove)
			
			# body - copy
			self.layoutBodyCopy = QtGui.QVBoxLayout()
			self.rowc5 = QtGui.QHBoxLayout()
			self.rowc5.addWidget(self.oCopy1L)
			self.rowc5.addWidget(self.oCopy1B1)
			self.rowc5.addWidget(self.oCopy1B2)
			self.layoutBodyCopy.addLayout(self.rowc5)
			self.rowc6 = QtGui.QHBoxLayout()
			self.rowc6.addWidget(self.oCopy2L)
			self.rowc6.addWidget(self.oCopy2B1)
			self.rowc6.addWidget(self.oCopy2B2)
			self.layoutBodyCopy.addLayout(self.rowc6)
			self.rowc7 = QtGui.QHBoxLayout()
			self.rowc7.addWidget(self.oCopy3L)
			self.rowc7.addWidget(self.oCopy3B1)
			self.rowc7.addWidget(self.oCopy3B2)
			self.layoutBodyCopy.addLayout(self.rowc7)
			self.layoutBodyCopy.addSpacing(5)
			self.rowc8 = QtGui.QHBoxLayout()
			self.rowc8.addWidget(self.oCopyStepL)
			self.rowc8.addStretch()
			self.rowc8.addWidget(self.oCopyStepE)
			self.layoutBodyCopy.addLayout(self.rowc8)
			self.groupBodyCopy = QtGui.QGroupBox(None, self)
			self.groupBodyCopy.setLayout(self.layoutBodyCopy)
			self.groupBodyCopy.hide()
			
			# body - move to equal
			self.layoutBodyMTE = QtGui.QVBoxLayout()
			self.row10 = QtGui.QHBoxLayout()
			self.row10.setAlignment(QtGui.Qt.AlignLeft)
			self.row10.addWidget(self.mte1B)
			self.row10.addWidget(self.mte1L)
			self.layoutBodyMTE.addLayout(self.row10)
			self.row11 = QtGui.QHBoxLayout()
			self.row11.setAlignment(QtGui.Qt.AlignLeft)
			self.row11.addWidget(self.mte2B)
			self.row11.addWidget(self.mte2L)
			self.layoutBodyMTE.addLayout(self.row11)
			self.row12 = QtGui.QHBoxLayout()
			self.row12.addWidget(self.mte12B)
			self.layoutBodyMTE.addLayout(self.row12)
			self.layoutBodyMTE.addSpacing(20)
			self.row13 = QtGui.QHBoxLayout()
			self.row13.addWidget(self.mte3L)
			self.row13.addWidget(self.mte3B)
			self.layoutBodyMTE.addLayout(self.row13)
			self.row14 = QtGui.QHBoxLayout()
			self.row14.addWidget(self.mte4L)
			self.row14.addWidget(self.mte4B)
			self.layoutBodyMTE.addLayout(self.row14)
			self.row15 = QtGui.QHBoxLayout()
			self.row15.addWidget(self.mte5L)
			self.row15.addWidget(self.mte5B)
			self.layoutBodyMTE.addLayout(self.row15)
			self.groupBodyMTE = QtGui.QGroupBox(None, self)
			self.groupBodyMTE.setLayout(self.layoutBodyMTE)
			self.groupBodyMTE.hide()
			
			# body - copy by edge
			self.layoutBodyCBE = QtGui.QVBoxLayout()
			self.row16 = QtGui.QHBoxLayout()
			self.row16.setAlignment(QtGui.Qt.AlignLeft)
			self.row16.addWidget(self.cbe1B)
			self.row16.addWidget(self.cbe1L)
			self.layoutBodyCBE.addLayout(self.row16)
			self.layoutBodyCBE.addSpacing(20)
			self.row17 = QtGui.QHBoxLayout()
			self.row17.addWidget(self.cbe2L)
			self.row17.addWidget(self.cbe2B)
			self.layoutBodyCBE.addLayout(self.row17)
			self.row18 = QtGui.QHBoxLayout()
			self.row18.addWidget(self.cbe3L)
			self.row18.addWidget(self.cbe3B)
			self.layoutBodyCBE.addLayout(self.row18)
			self.row19 = QtGui.QHBoxLayout()
			self.row19.addWidget(self.cbe4L)
			self.row19.addWidget(self.cbe4B)
			self.layoutBodyCBE.addLayout(self.row19)
			self.layoutBodyCBE.addSpacing(5)
			self.row20 = QtGui.QHBoxLayout()
			self.row20.addWidget(self.cbe5L)
			self.row20.addWidget(self.cbe5E)
			self.layoutBodyCBE.addLayout(self.row20)
			self.groupBodyCBE = QtGui.QGroupBox(None, self)
			self.groupBodyCBE.setLayout(self.layoutBodyCBE)
			self.groupBodyCBE.hide()
			
			# body - path
			self.layoutBodyPath = QtGui.QVBoxLayout()
			self.row21 = QtGui.QHBoxLayout()
			self.row21.setAlignment(QtGui.Qt.AlignLeft)
			self.row21.addWidget(self.oPathBS)
			self.row21.addWidget(self.oPathCurveL)
			self.layoutBodyPath.addLayout(self.row21)
			self.layoutBodyPath.addSpacing(10)
			self.row22 = QtGui.QHBoxLayout()
			self.row22.setAlignment(QtGui.Qt.AlignRight)
			self.row22.addWidget(self.oPathRotL)
			self.row22.addWidget(self.oPathRotXE)
			self.row22.addWidget(self.oPathRotYE)
			self.row22.addWidget(self.oPathRotZE)
			self.layoutBodyPath.addLayout(self.row22)
			self.row23 = QtGui.QHBoxLayout()
			self.row23.addWidget(self.oPathStepL)
			self.row23.addWidget(self.oPathStepE)
			self.layoutBodyPath.addLayout(self.row23)
			self.layoutBodyPath.addSpacing(10)
			self.row24 = QtGui.QHBoxLayout()
			self.row24.addWidget(self.oPathBC)
			self.layoutBodyPath.addLayout(self.row24)
			self.groupBodyPath = QtGui.QGroupBox(None, self)
			self.groupBodyPath.setLayout(self.layoutBodyPath)
			self.groupBodyPath.hide()
			
			# body - mirror copy
			self.layoutBodyMirror = QtGui.QVBoxLayout()
			self.row25 = QtGui.QHBoxLayout()
			self.row25.setAlignment(QtGui.Qt.AlignLeft)
			self.row25.addWidget(self.mc1B)
			self.row25.addWidget(self.mc1L)
			self.layoutBodyMirror.addLayout(self.row25)
			self.layoutBodyMirror.addSpacing(10)
			self.row26 = QtGui.QHBoxLayout()
			self.row26.addWidget(self.mc3L)
			self.layoutBodyMirror.addLayout(self.row26)
			self.row27 = QtGui.QHBoxLayout()
			self.row27.addWidget(self.mc31E)
			self.row27.addStretch()
			self.row27.addWidget(self.mc32E)
			self.row27.addStretch()
			self.row27.addWidget(self.mc33E)
			self.layoutBodyMirror.addLayout(self.row27)
			self.row28 = QtGui.QHBoxLayout()
			self.row28.addWidget(self.mc2L)
			self.row28.addWidget(self.mc2E)
			self.layoutBodyMirror.addLayout(self.row28)
			self.layoutBodyMirror.addSpacing(10)
			self.row29 = QtGui.QHBoxLayout()
			self.row29.addWidget(self.mc4L)
			self.row29.addWidget(self.mc4B1)
			self.layoutBodyMirror.addLayout(self.row29)
			self.row30 = QtGui.QHBoxLayout()
			self.row30.addWidget(self.mc5L)
			self.row30.addWidget(self.mc5B1)
			self.layoutBodyMirror.addLayout(self.row30)
			self.row31 = QtGui.QHBoxLayout()
			self.row31.addWidget(self.mc6L)
			self.row31.addWidget(self.mc6B1)
			self.layoutBodyMirror.addLayout(self.row31)
			self.groupBodyMirror = QtGui.QGroupBox(None, self)
			self.groupBodyMirror.setLayout(self.layoutBodyMirror)
			self.groupBodyMirror.hide()
			
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
			
			# add layout to main window
			self.layout = QtGui.QVBoxLayout()
			self.layout.addLayout(self.layoutHeader)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBodyMove)
			self.layout.addWidget(self.groupBodyCopy)
			self.layout.addWidget(self.groupBodyMTE)
			self.layout.addWidget(self.groupBodyCBE)
			self.layout.addWidget(self.groupBodyPath)
			self.layout.addWidget(self.groupBodyMirror)
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
			
			# init
			if self.gAxisCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			
			if self.gCornerCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(50)
			
			self.getSelected()

		# ############################################################################
		# functions for actions
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
				step = MagicPanels.unit2value(self.oMoveStepE.text())
				
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
				step = MagicPanels.unit2value(self.oCopyStepE.text())
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
				
				FreeCADGui.Selection.clearSelection()
				
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
				toCopy = MagicPanels.getObjectToCopy(o)
				
				[ toCopyX, toCopyY, toCopyZ ] = MagicPanels.getPosition(toCopy, "global")
				v = FreeCAD.Vector(toCopyX, toCopyY, toCopyZ)

				try:
					self.gPathLast[key] = self.gPathPoints.index(v)
					self.gPathInit[key] = False
				except:
					self.gPathLast[key] = 0
					self.gPathInit[key] = True

				self.gPathRotation[key] = toCopy.Placement.Rotation
		
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
					self.oPathCurveL.setText(self.gPathObj.Label)
					self.setLastPathPosition()
				
				# support edges
				else:
					
					sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
					
					if sub.ShapeType != "Edge":
						raise
					
					self.gPathPoints = sub.getPoints(1)[0]
					index = MagicPanels.getEdgeIndex(self.gPathObj, sub)
					self.oPathCurveL.setText(self.gPathObj.Label + ", Edge" + str(index))
					self.setLastPathPosition()
				
				FreeCADGui.Selection.clearSelection()
				
			except:
				self.oPathCurveL.setText(self.gNoPathSelection)

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
				
				FreeCADGui.Selection.clearSelection()
				
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
			self.groupBodyMove.hide()
			self.groupBodyCopy.hide()
			self.groupBodyMTE.hide()
			self.groupBodyCBE.hide()
			self.groupBodyPath.hide()
			self.groupBodyMirror.hide()
			
			self.sCopyType.hide()
			self.sMirrorType.hide()
			self.gNewContainerB1.hide()
			
			
			# Move
			if selectedIndex == 0:
				self.groupBodyMove.show()
			
			# Copy
			if selectedIndex == 1:
				self.sCopyType.show()
				self.gNewContainerB1.show()
				self.groupBodyCopy.show()
			
			# Copy by Path
			if selectedIndex == 2:
				self.sCopyType.show()
				self.gNewContainerB1.show()
				self.groupBodyPath.show()

			# Mirror
			if selectedIndex == 3:
				self.sMirrorType.show()
				self.groupBodyMirror.show()
	
			# Copy by Edge
			if selectedIndex == 4:
				self.sCopyType.show()
				self.groupBodyCBE.show()
			
			# Move to Equal
			if selectedIndex == 5:
				self.groupBodyMTE.show()
			
		# ############################################################################
		def setCopyType(self, selectedText):
			self.gCopyType = getMenuIndex2[selectedText]
		
		# ############################################################################
		def setMirrorType(self, selectedText):
			self.gMirrorType = getMenuIndex3[selectedText]
		
		# ############################################################################
		def setMoveX1(self):
			try:
				self.setMove("Xm")
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setMoveX2(self):
			try:
				self.setMove("Xp")
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setMoveY1(self):
			try:
				self.setMove("Ym")
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setMoveY2(self):
			try:
				self.setMove("Yp")
			except:
				self.s1S.setText(self.gNoSelection)

		def setMoveZ1(self):
			try:
				self.setMove("Zm")
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setMoveZ2(self):
			try:
				self.setMove("Zp")
			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def setCopyX1(self):
			try:
				self.createCopy("Xm")
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setCopyX2(self):
			try:
				self.createCopy("Xp")
			except:
				self.s1S.setText(self.gNoSelection)

		def setCopyY1(self):
			try:
				self.createCopy("Ym")
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setCopyY2(self):
			try:
				self.createCopy("Yp")
			except:
				self.s1S.setText(self.gNoSelection)

		def setCopyZ1(self):
			try:
				self.createCopy("Zm")
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setCopyZ2(self):
			try:
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
		def getSelected(self):

			try:

				self.resetGlobals()
				self.gObjects = FreeCADGui.Selection.getSelection()
				
				sizes = []
				sizes = MagicPanels.getSizes(self.gObjects[0])
				sizes.sort()
					
				self.oMoveStepE.setText(MagicPanels.unit2gui( sizes[0] ))
				self.oCopyStepE.setText(MagicPanels.unit2gui( sizes[0] ))
				
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

