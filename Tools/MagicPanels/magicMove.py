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

		gInfoPath1 = translate('magicMove', 'Rotation X, Y, Z:')
		gInfoPath2 = translate('magicMove', 'Next point step:')

		gInfoMirrorX = translate('magicMove', 'Mirror along X:')
		gInfoMirrorY = translate('magicMove', 'Mirror along Y:')
		gInfoMirrorZ = translate('magicMove', 'Mirror along Z:')
		gInfoMirrorStep = translate('magicMove', 'Mirror offset:')
		
		gNoSelection = translate('magicMove', 'select panel or container')
		gNoPathSelection = translate('magicMove', 'select copy path')
		gNoPathSelection += "                         "
		
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
		
		gNewFolder = False
		gToCopy = dict()
		
		gCrossCorner = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
		gCrossCenter = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()

		gCopyPathObj = ""
		gCopyPathStep = 1
		gCopyPathPoints = []
		gCopyPathRotation = dict() # last rotation
		gCopyPathLast = dict() # last path position
		gCopyPathInit = dict() # if init from 0 or last selected panel
		
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
			toolSH = 360
			
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
						"Copy Path",
						"Mirror"
						)
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(self.sModeList.index("Move"))
			self.sMode.activated[str].connect(self.setModeType)
			self.sMode.setFixedWidth(90)
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
			# options - new folder
			# ############################################################################

			row += 30

			# button
			self.oNewFolderB1 = QtGui.QPushButton(translate('magicMove', 'copy to new container'), self)
			self.oNewFolderB1.clicked.connect(self.setNewFolder)
			self.oNewFolderB1.setFixedWidth(200)
			self.oNewFolderB1.setFixedHeight(20)
			self.oNewFolderB1.move(10, row)
			self.oNewFolderB1.hide()
			
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
			# options - step
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

			rowNoPath = row
			
			# ############################################################################
			# options - copy along path
			# ############################################################################
			
			row -= 90
			
			self.pathL1 = QtGui.QLabel(self.gInfoPath1, self)
			self.pathL1.move(10, row+3)
			self.pathL1.hide()
			
			self.pathE1 = QtGui.QLineEdit(self)
			self.pathE1.setText("0")
			self.pathE1.setFixedWidth(30)
			self.pathE1.move(toolSW-10-100, row)
			self.pathE1.hide()
			
			self.pathE2 = QtGui.QLineEdit(self)
			self.pathE2.setText("0")
			self.pathE2.setFixedWidth(30)
			self.pathE2.move(toolSW-10-65, row)
			self.pathE2.hide()
	
			self.pathE3 = QtGui.QLineEdit(self)
			self.pathE3.setText("0")
			self.pathE3.setFixedWidth(30)
			self.pathE3.move(toolSW-10-30, row)
			self.pathE3.hide()

			row += 30
			
			self.pathL2 = QtGui.QLabel(self.gInfoPath2, self)
			self.pathL2.move(10, row+3)
			self.pathL2.hide()
			
			self.pathE4 = QtGui.QLineEdit(self)
			self.pathE4.setText("1")
			self.pathE4.setFixedWidth(65)
			self.pathE4.move(toolSW-10-65, row)
			self.pathE4.hide()

			row += 30
			
			self.pathB1 = QtGui.QPushButton(translate('magicMove', 'set'), self)
			self.pathB1.clicked.connect(self.setCopyPath)
			self.pathB1.setFixedWidth(60)
			self.pathB1.setFixedHeight(20)
			self.pathB1.move(10, row)
			self.pathB1.hide()
			
			self.pathL3 = QtGui.QLabel(self.gNoPathSelection, self)
			self.pathL3.move(80, row+3)
			self.pathL3.hide()

			row += 30
			
			self.pathB2 = QtGui.QPushButton(translate('magicMove', 'copy along path'), self)
			self.pathB2.clicked.connect(self.createPathPanel)
			self.pathB2.setFixedWidth(toolSW-20)
			self.pathB2.setFixedHeight(20)
			self.pathB2.move(10, row)
			self.pathB2.setAutoRepeat(True)
			self.pathB2.hide()

			# ############################################################################
			# options - corner cross
			# ############################################################################

			row = rowNoPath
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
			
			self.gLCPX = dict() 
			self.gLCPY = dict() 
			self.gLCPZ = dict() 
			self.gLCPR = dict()

			gNewFolder = False
			gToCopy = dict()

		# ############################################################################
		def setLastPosition(self):
			for o in self.gObjects:
				toMove = MagicPanels.getObjectToMove(o)
				key = str(o.Name)
				[ 	self.gLCPX[key], 
					self.gLCPY[key], 
					self.gLCPZ[key], 
					self.gLCPR[key] ] = MagicPanels.getContainerPlacement(toMove, "clean")

		def setFolderCopies(self):
			for o in self.gObjects:
				self.gToCopy[str(o.Name)] = o

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
		def createCopy(self, iType):
			
			container = ""
			
			for o in self.gObjects:

				key = str(o.Name)
				x, y, z, r = self.gLCPX[key], self.gLCPY[key], self.gLCPZ[key], self.gLCPR[key]

				self.gStep = float(self.o4E.text())

				if self.gCopyType == "copyObject":
					copy = FreeCAD.ActiveDocument.copyObject(o)
					copy.Label = MagicPanels.getNestingLabel(o, "Copy")
					
				if self.gCopyType == "Clone":
					import Draft
					copy = Draft.make_clone(o)
					copy.Label = MagicPanels.getNestingLabel(o, "Clone")
					
				if self.gCopyType == "Link":
					copy = FreeCAD.ActiveDocument.addObject('App::Link', "Link")
					copy.setLink(o)
					copy.Label = str(o.Label)
					copy.Label = MagicPanels.getNestingLabel(o, "Link")
					
				if self.gNewFolder == True:
					self.gToCopy[str(o.Name)] = copy
					if container == "":
						container = MagicPanels.createContainer([ copy ])
						containerRef = copy
					else:
						MagicPanels.moveToParent([ copy ], containerRef)
				else:
					MagicPanels.moveToParent([ copy ], self.gToCopy[str(o.Name)])

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
			
			# end of the loop, after copy all objects
			if self.gNewFolder == True:
				self.gNewFolder = False
				self.oNewFolderB1.setDisabled(False)

		# ############################################################################
		def createMirror(self, iType):
			
			for o in self.gObjects:
				
				# get placement for object not from container
				# the placement for new created container will be (0, 0, 0)
				[ x, y, z, r ] = MagicPanels.getContainerPlacement(o, "clean")
				mx, my, mz = 0, 0, 0
				
				# not create mirror directly at object because 
				# it will not be managed, extended later
				# create LinkGroup and move the object to the LinkGroup
				# and create Mirror at LinkGroup instead
				if not o.isDerivedFrom("App::LinkGroup"):
					o = MagicPanels.createContainer([o])

				# calculate
				self.gStep = float(self.o4E.text())
				
				if iType == "Xp":
					mx = self.gStep
					direction = (1, 0, 0)
					x = x + self.gMaxX

				if iType == "Xm":
					mx = - self.gStep
					direction = (1, 0, 0)
					
				if iType == "Yp":
					my = self.gStep
					direction = (0, 1, 0)
					y = y + self.gMaxY
					
				if iType == "Ym":
					my = - self.gStep
					direction = (0, 1, 0)

				if iType == "Zp":
					mz = self.gStep
					direction = (0, 0, 1)
					z = z + self.gMaxZ
					
				if iType == "Zm":
					mz = - self.gStep
					direction = (0, 0, 1)
					
				mirror = FreeCAD.ActiveDocument.addObject('Part::Mirroring', "mirror")
				mirror.Label = "Mirror, " + str(o.Label) + " "
				mirror.Source = FreeCAD.ActiveDocument.getObject(o.Name)
				mirror.Normal = direction
				mirror.Base = (x, y, z)
				
				[ cx, cy, cz, r ] = MagicPanels.getContainerPlacement(mirror, "clean")
				MagicPanels.setContainerPlacement(mirror, cx+mx, cy+my, cz+mz, 0, "clean")
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
				
				if self.gCopyType == "copyObject":
					copy = FreeCAD.ActiveDocument.copyObject(o)
					copy.Label = MagicPanels.getNestingLabel(o, "Copy")
					
				if self.gCopyType == "Clone":
					import Draft
					copy = Draft.make_clone(o)
					copy.Label = MagicPanels.getNestingLabel(o, "Clone")
					
				if self.gCopyType == "Link":
					copy = FreeCAD.ActiveDocument.addObject('App::Link', "Link")
					copy.setLink(o)
					copy.Label = str(o.Label)
					copy.Label = MagicPanels.getNestingLabel(o, "Link")
					
				if self.gNewFolder == True:
					self.gToCopy[str(o.Name)] = copy
					if container == "":
						container = MagicPanels.createContainer([ copy ])
						containerRef = copy
					else:
						MagicPanels.moveToParent([ copy ], containerRef)
				else:
					MagicPanels.moveToParent([ copy ], self.gToCopy[str(o.Name)])

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

			# end of the loop, after copy all objects
			if self.gNewFolder == True:
				self.gNewFolder = False
				self.oNewFolderB1.setDisabled(False)

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

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
				self.setFolderCopies()
				
				if self.gCopyPathObj != "":
					self.setLastPathPosition()

			except:

				self.s1S.setText(self.gNoSelection)
				return -1
			
		# ############################################################################	
		def setModeType(self, selectedText):
			
			self.gModeType = selectedText

			self.pathE1.hide()
			self.pathE2.hide()
			self.pathE3.hide()
			self.pathE4.hide()
			self.pathB1.hide()
			self.pathB2.hide()
			self.pathL1.hide()
			self.pathL2.hide()
			self.pathL3.hide()
			
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
			
			if selectedText == "Move":
				self.o1L.setText(self.gInfoMoveX)
				self.o2L.setText(self.gInfoMoveY)
				self.o3L.setText(self.gInfoMoveZ)
				self.o4L.setText(self.gInfoMoveStep)
				self.sCopyType.hide()
				self.oNewFolderB1.hide()
				self.setLastPosition()

			if selectedText == "Copy":
				self.o1L.setText(self.gInfoCopyX)
				self.o2L.setText(self.gInfoCopyY)
				self.o3L.setText(self.gInfoCopyZ)
				self.o4L.setText(self.gInfoCopyStep)
				self.sCopyType.show()
				self.oNewFolderB1.show()
				self.setLastPosition()

			if selectedText == "Copy Path":
				
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
				
				self.pathE1.show()
				self.pathE2.show()
				self.pathE3.show()
				self.pathE4.show()
				self.pathB1.show()
				self.pathB2.show()
				self.pathL1.show()
				self.pathL2.show()
				self.pathL3.show()

				self.sCopyType.show()
				self.oNewFolderB1.show()
				self.setLastPosition()

			if selectedText == "Mirror":
				self.o1L.setText(self.gInfoMirrorX)
				self.o2L.setText(self.gInfoMirrorY)
				self.o3L.setText(self.gInfoMirrorZ)
				self.o4L.setText(self.gInfoMirrorStep)
				self.sCopyType.hide()
				self.oNewFolderB1.hide()
				self.setLastPosition()

		def setCopyType(self, selectedText):
			self.gCopyType = selectedText
		
		def setNewFolder(self):
			self.gNewFolder = True
			self.oNewFolderB1.setDisabled(True)

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

