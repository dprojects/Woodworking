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

		gObj = ""
		gThick = 0
		
		gFace = ""
		gFIndex = 0
		gFAxis = ""
		gFType = ""
		
		gEdge = ""
		gEArr = []
		gEIndex = 0

		gPosition = 0
		gRAxis = ""
		gRAngles = []
		gRIndex = 0

		# should not be reset if object change
		gSides = 0
		gDowels = []
		gDowelLabel = ""
		gDDiameter = 8
		gDSize = 35
		gDSink = 20
		gDNum = 2
		gDOCorner = 50
		gDONext = 32
		gDOEdge = 0
		
		gDSinkSave = 20
		
		gNoSelection = translate('magicDowels', 'please select face')
		
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
			toolSH = 620
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = int( gSW - toolSW )
			gPH = int( gSH - toolSH )

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicDowels', 'magicDowels'))
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
			self.s1B1 = QtGui.QPushButton(translate('magicDowels', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(200)
			self.s1B1.move(10, 40)

			row = 50

			# ############################################################################
			# options - select edge
			# ############################################################################

			row += 30

			# label
			self.s2L = QtGui.QLabel(translate('magicDowels', 'Select edge:'), self)
			self.s2L.move(10, row+3)

			# button
			self.s2B1 = QtGui.QPushButton("<", self)
			self.s2B1.clicked.connect(self.setEdgeP)
			self.s2B1.setFixedWidth(50)
			self.s2B1.move(105, row)
			self.s2B1.setAutoRepeat(True)
			
			# button
			self.s2B2 = QtGui.QPushButton(">", self)
			self.s2B2.clicked.connect(self.setEdgeN)
			self.s2B2.setFixedWidth(50)
			self.s2B2.move(160, row)
			self.s2B2.setAutoRepeat(True)

			# ############################################################################
			# options - adjust position
			# ############################################################################

			row += 30
			
			# label
			self.s3L = QtGui.QLabel(translate('magicDowels', 'Adjust edge:'), self)
			self.s3L.move(10, row+3)

			# button
			self.s3B1 = QtGui.QPushButton("<", self)
			self.s3B1.clicked.connect(self.setPosition)
			self.s3B1.setFixedWidth(50)
			self.s3B1.move(105, row)
			self.s3B1.setAutoRepeat(True)
			
			# button
			self.s3B2 = QtGui.QPushButton(">", self)
			self.s3B2.clicked.connect(self.setPosition)
			self.s3B2.setFixedWidth(50)
			self.s3B2.move(160, row)
			self.s3B2.setAutoRepeat(True)

			# ############################################################################
			# options - adjust sink
			# ############################################################################

			row += 30
			
			# label
			self.s7L = QtGui.QLabel(translate('magicDowels', 'Adjust sink:'), self)
			self.s7L.move(10, row+3)

			# button
			self.s7B1 = QtGui.QPushButton("< >", self)
			self.s7B1.clicked.connect(self.setSink)
			self.s7B1.setFixedWidth(50)
			self.s7B1.move(105, row)
			self.s7B1.setAutoRepeat(True)
			
			# button
			self.s7B2 = QtGui.QPushButton("0", self)
			self.s7B2.clicked.connect(self.setSink0)
			self.s7B2.setFixedWidth(50)
			self.s7B2.move(160, row)
			self.s7B2.setAutoRepeat(True)

			# ############################################################################
			# options - adjust rotation
			# ############################################################################

			row += 30
			
			# label
			self.s4L = QtGui.QLabel(translate('magicDowels', 'Adjust rotation:'), self)
			self.s4L.move(10, row+3)

			# button
			self.s4B1 = QtGui.QPushButton("<", self)
			self.s4B1.clicked.connect(self.setRotationP)
			self.s4B1.setFixedWidth(50)
			self.s4B1.move(105, row)
			self.s4B1.setAutoRepeat(True)
			
			# button
			self.s4B2 = QtGui.QPushButton(">", self)
			self.s4B2.clicked.connect(self.setRotationN)
			self.s4B2.setFixedWidth(50)
			self.s4B2.move(160, row)
			self.s4B2.setAutoRepeat(True)

			# ############################################################################
			# options - select sides
			# ############################################################################

			row += 50

			# label
			self.s5L = QtGui.QLabel(translate('magicDowels', 'Select sides:'), self)
			self.s5L.move(10, row+3)

			# button
			self.s5B1 = QtGui.QPushButton("<", self)
			self.s5B1.clicked.connect(self.setSidesP)
			self.s5B1.setFixedWidth(50)
			self.s5B1.move(105, row)
			self.s5B1.setAutoRepeat(True)
			
			# button
			self.s5B2 = QtGui.QPushButton(">", self)
			self.s5B2.clicked.connect(self.setSidesN)
			self.s5B2.setFixedWidth(50)
			self.s5B2.move(160, row)
			self.s5B2.setAutoRepeat(True)

			# ############################################################################
			# options - mounting samples
			# ############################################################################

			row += 30

			# border options
			self.s6Slist = (
						"Dowel 6 x 35 mm ",
						"Dowel 8 x 35 mm ",
						"Dowel 10 x 35 mm ",
						"Screw 3 x 20 mm ",
						"Screw 4.5 x 40 mm ",
						"Screw 4 x 40 mm ",
						"Screw 5 x 50 mm ",
						"Screw 6 x 60 mm ",
						"Confirmation 7 x 40 mm ",
						"Confirmation 7 x 50 mm ",
						"Confirmation 7 x 70 mm ",
						"Shelf Pin 5 x 16 mm ",
						"Profile Pin 5 x 30 mm ",
						"Profile Pin 8 x 40 mm ",
						"Custom mount point "
						)
			
			self.gDowelLabel = "Dowel 8 x 35 mm "
			self.s6S = QtGui.QComboBox(self)
			self.s6S.addItems(self.s6Slist)
			self.s6S.setCurrentIndex(self.s6Slist.index(self.gDowelLabel))
			self.s6S.activated[str].connect(self.setCustomMount)
			self.s6S.setFixedWidth(200)
			self.s6S.move(10, row)

			# ############################################################################
			# options - mount label
			# ############################################################################

			row += 30
			
			# label
			self.oDowelLabelL = QtGui.QLabel(translate('magicDowels', 'Label:'), self)
			self.oDowelLabelL.move(10, row+3)

			# text input
			self.oDowelLabelE = QtGui.QLineEdit(self)
			self.oDowelLabelE.setText(str(self.gDowelLabel))
			self.oDowelLabelE.setFixedWidth(150)
			self.oDowelLabelE.move(60, row)

			# ############################################################################
			# options - dowels number per side
			# ############################################################################

			row += 30
			
			# label
			self.oDNumL = QtGui.QLabel(translate('magicDowels', 'Dowels per side:'), self)
			self.oDNumL.move(10, row+3)

			# text input
			self.oDNumE = QtGui.QLineEdit(self)
			self.oDNumE.setText(str(self.gDNum))
			self.oDNumE.setFixedWidth(50)
			self.oDNumE.move(160, row)

			# ############################################################################
			# options - dowels diameter
			# ############################################################################
			
			row += 30

			# label
			self.oDDiameterL = QtGui.QLabel(translate('magicDowels', 'Dowels diameter:'), self)
			self.oDDiameterL.move(10, row+3)

			# text input
			self.oDDiameterE = QtGui.QLineEdit(self)
			self.oDDiameterE.setText(str(self.gDDiameter))
			self.oDDiameterE.setFixedWidth(50)
			self.oDDiameterE.move(160, row)

			# ############################################################################
			# options - dowels size
			# ############################################################################

			row += 30
			
			# label
			self.oDSizeL = QtGui.QLabel(translate('magicDowels', 'Dowels size:'), self)
			self.oDSizeL.move(10, row+3)

			# text input
			self.oDSizeE = QtGui.QLineEdit(self)
			self.oDSizeE.setText(str(self.gDSize))
			self.oDSizeE.setFixedWidth(50)
			self.oDSizeE.move(160, row)

			# ############################################################################
			# options - dowels sink
			# ############################################################################

			row += 30

			# label
			self.oDSinkL = QtGui.QLabel(translate('magicDowels', 'Dowels sink:'), self)
			self.oDSinkL.move(10, row+3)

			# text input
			self.oDSinkE = QtGui.QLineEdit(self)
			self.oDSinkE.setText(str(self.gDSink))
			self.oDSinkE.setFixedWidth(50)
			self.oDSinkE.move(160, row)

			# ############################################################################
			# options - offset from corner
			# ############################################################################

			row += 30
			
			# label
			self.oDOCornerL = QtGui.QLabel(translate('magicDowels', 'Offset from corner:'), self)
			self.oDOCornerL.move(10, row+3)

			# text input
			self.oDOCornerE = QtGui.QLineEdit(self)
			self.oDOCornerE.setText(str(self.gDOCorner))
			self.oDOCornerE.setFixedWidth(50)
			self.oDOCornerE.move(160, row)

			# ############################################################################
			# options - offset between dowels
			# ############################################################################

			row += 30
			
			# label
			self.oDONextL = QtGui.QLabel(translate('magicDowels', 'Offset between dowels:'), self)
			self.oDONextL.move(10, row+3)

			# text input
			self.oDONextE = QtGui.QLineEdit(self)
			self.oDONextE.setText(str(self.gDONext))
			self.oDONextE.setFixedWidth(50)
			self.oDONextE.move(160, row)

			# ############################################################################
			# options - offset from edge
			# ############################################################################

			row += 30
			
			# label
			self.oDOEdgeL = QtGui.QLabel(translate('magicDowels', 'Offset from edge:'), self)
			self.oDOEdgeL.move(10, row+3)

			# text input
			self.oDOEdgeE = QtGui.QLineEdit(self)
			self.oDOEdgeE.setText(str(self.gDOEdge))
			self.oDOEdgeE.setFixedWidth(50)
			self.oDOEdgeE.move(160, row)

			# ############################################################################
			# options - end settings
			# ############################################################################

			row += 30

			# button
			self.e1B1 = QtGui.QPushButton(translate('magicDowels', 'set custom values'), self)
			self.e1B1.clicked.connect(self.refreshSettings)
			self.e1B1.setFixedWidth(200)
			self.e1B1.move(10, row)

			row += 40

			# button
			self.e2B1 = QtGui.QPushButton(translate('magicDowels', 'apply dowels to this position'), self)
			self.e2B1.clicked.connect(self.setDowels)
			self.e2B1.setFixedWidth(200)
			self.e2B1.setFixedHeight(40)
			self.e2B1.move(10, row)

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
		def setRotation(self):
			
			reset = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
			for d in self.gDowels:
				d.Placement.Rotation = reset
			
			angle = self.gRAngles[self.gRIndex]
			axis = self.gRAxis

			for d in self.gDowels:
				
				x = d.Placement.Base.x
				y = d.Placement.Base.y
				z = d.Placement.Base.z
			
				center = FreeCAD.Vector(x, y, z)
			
				Draft.rotate(d, angle, center, axis, False)
				
			FreeCADGui.Selection.clearSelection()
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def showDowels(self):
			
			# ############################################################################
			# remove all dowels
			# ############################################################################
			
			if len(self.gDowels) != 0:
				for d in self.gDowels:
					try:
						FreeCAD.activeDocument().removeObject(str(d.Name))
					except:
						skip = 1
			
			self.gDowels = []
			
			# get settings
			[ v1, v2 ] = MagicPanels.getEdgeVertices(self.gEArr[self.gEIndex])
			
			# ############################################################################
			# dowels at 1st side
			# ############################################################################
			
			if self.gSides == 0 or self.gSides == 1:
			
				[ X, Y, Z ] = [ v1[0], v1[1], v1[2] ]
				[ x , y, z ] = [ 0, 0, 0 ]
				
				i = 0
				while i < self.gDNum:
					
					d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","Dowel")
					d.Label = str(self.gDowelLabel)
					
					d.Radius = self.gDDiameter / 2
					d.Height = self.gDSize
					
					# edge along X
					if v1[0] != v2[0]:
						
						if self.gFAxis == "XY" or self.gFAxis == "YX":
							x = X - self.gDOCorner
							if i != 0:
								x = x - ( i * self.gDONext)
							y = Y + self.gDOEdge
							z = Z - self.gDSink
						
						if self.gFAxis == "XZ" or self.gFAxis == "ZX":
							x = X - self.gDOCorner
							if i != 0:
								x = x - ( i * self.gDONext)
							y = Y - self.gDSink
							z = Z + self.gDOEdge
				
						# this should not exist
						if self.gFAxis == "YZ" or self.gFAxis == "ZY":
							[ x, y, z ] = [ X, Y, Z ]

					# edge along Y
					if v1[1] != v2[1]:
						
						if self.gFAxis == "XY" or self.gFAxis == "YX":
							x = X + self.gDOEdge
							y = Y - self.gDOCorner
							if i != 0:
								y = y - ( i * self.gDONext)
							z = Z - self.gDSink
					
						# this should not exist
						if self.gFAxis == "XZ" or self.gFAxis == "ZX":
							[ x, y, z ] = [ X, Y, Z ]
					
						if self.gFAxis == "YZ" or self.gFAxis == "ZY":
							x = X - self.gDSink
							y = Y - self.gDOCorner
							if i != 0:
								y = y - ( i * self.gDONext)
							z = Z + self.gDOEdge

					# edge along Z
					if v1[2] != v2[2]:
						
						if self.gFAxis == "XY" or self.gFAxis == "YX":
							x = X + self.gDOEdge
							y = Y - self.gDSink
							z = Z - self.gDOCorner
							if i != 0:
								z = z - ( i * self.gDONext)
						
						if self.gFAxis == "XZ" or self.gFAxis == "ZX":
							x = X - self.gDOEdge
							y = Y - self.gDSink
							z = Z - self.gDOCorner
							if i != 0:
								z = z - ( i * self.gDONext)
								
						if self.gFAxis == "YZ" or self.gFAxis == "ZY":
							x = X - self.gDSink
							y = Y + self.gDOEdge
							z = Z - self.gDOCorner
							if i != 0:
								z = z - ( i * self.gDONext)

					# final set
					d.Placement.Base.x = x
					d.Placement.Base.y = y
					d.Placement.Base.z = z
					
					colors = [ (0.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0) ]
					d.ViewObject.DiffuseColor = colors
					
					self.gDowels.append(d)
					
					i = i + 1
			
			# ############################################################################
			# dowels at 2nd side
			# ############################################################################

			if self.gSides == 0 or self.gSides == 2:
			
				[ X, Y, Z ] = [ v2[0], v2[1], v2[2] ]
				[ x , y, z ] = [ 0, 0, 0 ]

				i = 0
				while i < self.gDNum:
					
					d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","Dowel")
					d.Label = str(self.gDowelLabel)
					
					d.Radius = self.gDDiameter / 2
					d.Height = self.gDSize
					
					# edge along X
					if v1[0] != v2[0]:
						
						if self.gFAxis == "XY" or self.gFAxis == "YX":
							x = X + self.gDOCorner
							if i != 0:
								x = x + ( i * self.gDONext)
							y = Y + self.gDOEdge
							z = Z - self.gDSink
					
						if self.gFAxis == "XZ" or self.gFAxis == "ZX":
							x = X + self.gDOCorner
							if i != 0:
								x = x + ( i * self.gDONext)
							y = Y - self.gDSink
							z = Z + self.gDOEdge
						
						# this should not exist
						if self.gFAxis == "YZ" or self.gFAxis == "ZY":
							[ x, y, z ] = [ X, Y, Z ]

					# edge along Y
					if v1[1] != v2[1]:
						
						if self.gFAxis == "XY" or self.gFAxis == "YX":
							x = X + self.gDOEdge
							y = Y + self.gDOCorner
							if i != 0:
								y = y + ( i * self.gDONext)
							z = Z - self.gDSink
					
						# this should not exist
						if self.gFAxis == "XZ" or self.gFAxis == "ZX":
							[ x, y, z ] = [ X, Y, Z ]
					
						if self.gFAxis == "YZ" or self.gFAxis == "ZY":
							x = X - self.gDSink
							y = Y + self.gDOCorner
							if i != 0:
								y = y + ( i * self.gDONext)
							z = Z + self.gDOEdge

					# edge along Z
					if v1[2] != v2[2]:
						
						if self.gFAxis == "XY" or self.gFAxis == "YX":
							x = X + self.gDOEdge
							y = Y - self.gDSink
							z = Z + self.gDOCorner
							if i != 0:
								z = z + ( i * self.gDONext)
					
						if self.gFAxis == "XZ" or self.gFAxis == "ZX":
							x = X - self.gDOEdge
							y = Y - self.gDSink
							z = Z + self.gDOCorner
							if i != 0:
								z = z + ( i * self.gDONext)
					
						if self.gFAxis == "YZ" or self.gFAxis == "ZY":
							x = X - self.gDSink
							y = Y + self.gDOEdge
							z = Z + self.gDOCorner
							if i != 0:
								z = z + ( i * self.gDONext)
					
					# final set
					d.Placement.Base.x = x
					d.Placement.Base.y = y
					d.Placement.Base.z = z

					colors = [ (0.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0) ]
					d.ViewObject.DiffuseColor = colors
					
					self.gDowels.append(d)
					
					i = i + 1
				
			# ############################################################################
			# set rotation at dowels
			# ############################################################################

			self.setRotation()

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def resetGlobals(self):

			self.gObj = ""
			self.gThick = 0
			
			self.gFace = ""
			self.gFIndex = 0
			self.gFAxis = ""
			self.gFType = ""
		
			self.gEdge = ""
			self.gEArr = []
			self.gEIndex = 0
		
			self.gPosition = 0
		
			self.gRAxis = ""
			self.gRAngles = []
			self.gRIndex = 0

		# ############################################################################
		def getSelected(self):

			try:

				# ############################################################################
				# global config
				# ############################################################################
				
				self.resetGlobals()

				self.gObj = MagicPanels.getReference()
				self.gFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gFIndex = MagicPanels.getFaceIndex(self.gObj, self.gFace)
				FreeCADGui.Selection.clearSelection()
				
				n = ""
				n += str(self.gObj.Label)
				n += ", "
				n += "Face"
				n += str(self.gFIndex)
				self.s1S.setText(n)
				
				[ self.gFAxis, self.gFType ] = MagicPanels.getDirectionFace(self.gObj, self.gFace)
				
				# ############################################################################
				# set possible edges
				# ############################################################################
				
				sizes = []
				sizes = MagicPanels.getSizes(self.gObj)
				sizes.sort()
				self.gThick = sizes[0]

				e1 = self.gFace.Edges[0]
				e2 = self.gFace.Edges[1]
				e3 = self.gFace.Edges[2]
				e4 = self.gFace.Edges[3]
		
				if self.gFType == "edge":
					
					if int(e1.Length) != int(self.gThick):
						self.gEArr.append(e1)
					
					if int(e2.Length) != int(self.gThick):
						self.gEArr.append(e2)
						
					if int(e3.Length) != int(self.gThick):
						self.gEArr.append(e3)
						
					if int(e4.Length) != int(self.gThick):
						self.gEArr.append(e4)
					
				if self.gFType == "surface" or self.gFType == "equal":
					
					self.gEArr.append(self.gFace.Edges[0])
					self.gEArr.append(self.gFace.Edges[1])
					self.gEArr.append(self.gFace.Edges[2])
					self.gEArr.append(self.gFace.Edges[3])
				
				# ############################################################################
				# set possible rotation 
				# ############################################################################
				
				if self.gFAxis == "XY" or self.gFAxis == "YX":
					self.gRAngles.append(0)
					self.gRAngles.append(180)
				
				if self.gFAxis == "XZ" or self.gFAxis == "ZX":
					self.gRAngles.append(90)
					self.gRAngles.append(270)
				
				if self.gFAxis == "YZ" or self.gFAxis == "ZY":
					self.gRAngles.append(90)
					self.gRAngles.append(270)
				
				if self.gFAxis == "XY" or self.gFAxis == "YX":
					self.gRAxis = FreeCAD.Vector(1, 0, 0)
					
				if self.gFAxis == "XZ" or self.gFAxis == "ZX":
					self.gRAxis = FreeCAD.Vector(1, 0, 0)
					
				if self.gFAxis == "YZ" or self.gFAxis == "ZY":
					self.gRAxis = FreeCAD.Vector(0, 1, 0)
				
				# ############################################################################
				self.gDOEdge = self.gThick / 2
				self.oDOEdgeE.setText(str(self.gDOEdge))
				
				self.showDowels()
			
			except:

				self.s1S.setText(self.gNoSelection)
				return -1
			
		# ############################################################################
		def setSidesP(self):
			
			try:
				if self.gSides - 1 < 0:
					self.gSides = 2
				else:
					self.gSides = self.gSides - 1
					
				self.showDowels()
		
			except:
				self.s1S.setText(self.gNoSelection)
				
		def setSidesN(self):
			
			try:
				if self.gSides + 1 > 2:
					self.gSides = 0
				else:
					self.gSides = self.gSides + 1
					
				self.showDowels()
			
			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def setEdgeP(self):
			
			try:
				if self.gEIndex - 1 < 0:
					self.gEIndex = len(self.gEArr) - 1
				else:
					self.gEIndex = self.gEIndex - 1
					
				self.gEdge = self.gEArr[self.gEIndex]
				
				self.showDowels()
			
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setEdgeN(self):
			
			try:
				if self.gEIndex + 1 > len(self.gEArr) - 1:
					self.gEIndex = 0
				else:
					self.gEIndex = self.gEIndex + 1
					
				self.gEdge = self.gEArr[self.gEIndex]
				
				self.showDowels()
			
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def setSink(self):
			try:
				if self.gDSink == 0:
					self.gDSink = self.gDSinkSave
					
				self.gDSink = - self.gDSink
				self.oDSinkE.setText(str(self.gDSink))
				self.showDowels()
				
			except:
				self.s1S.setText(self.gNoSelection)
		
		def setSink0(self):
			try:
				self.gDSinkSave = self.gDSink
				self.gDSink = 0
				self.oDSinkE.setText(str(self.gDSink))
				self.showDowels()
				
			except:
				self.s1S.setText(self.gNoSelection)
				
		# ############################################################################
		def setPosition(self):
			
			try:
				if self.gPosition == 0:
					self.gPosition = 1
				else:
					self.gPosition = 0
				
				self.gDOEdge = - self.gDOEdge
				self.oDOEdgeE.setText(str(self.gDOEdge))
				self.showDowels()
				
			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def setRotationP(self):
			
			try:
				if self.gRIndex - 1 < 0:
					self.gRIndex = len(self.gRAngles) - 1
				else:
					self.gRIndex = self.gRIndex - 1
					
				self.showDowels()
			
			except:
				self.s1S.setText(self.gNoSelection)
				
		def setRotationN(self):
			
			try:
				if self.gRIndex + 1 > len(self.gRAngles) - 1:
					self.gRIndex = 0
				else:
					self.gRIndex = self.gRIndex + 1
					
				self.showDowels()
			
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def setCustomMount(self, selectedText):
			
			try:
			
				self.gDOEdge = self.gThick / 2
				self.gDowelLabel = selectedText
				self.gSides = 0
				
				if selectedText == "Dowel 6 x 35 mm ":
					self.gDDiameter = 6
					self.gDSize = 35
					self.gDSink = 20
					self.gDNum = 2
					self.gDOCorner = 50
					self.gDONext = 32
					
				if selectedText == "Dowel 8 x 35 mm ":
					self.gDDiameter = 8
					self.gDSize = 35
					self.gDSink = 20
					self.gDNum = 2
					self.gDOCorner = 50
					self.gDONext = 32

				if selectedText == "Dowel 10 x 35 mm ":
					self.gDDiameter = 10
					self.gDSize = 35
					self.gDSink = 20
					self.gDNum = 2
					self.gDOCorner = 50
					self.gDONext = 32
				
				if selectedText == "Screw 3 x 20 mm ":
					self.gDDiameter = 3
					self.gDSize = 20
					self.gDSink = 19
					self.gDNum = 5
					self.gDOCorner = 50
					self.gDONext = 32
					self.gDOEdge = 9
				
				if selectedText == "Screw 4.5 x 40 mm ":
					self.gDDiameter = 4.5
					self.gDSize = 40
					self.gDSink = 25
					self.gDNum = 2
					self.gDOCorner = 50
					self.gDONext = 32

				if selectedText == "Screw 4 x 40 mm ":
					self.gDDiameter = 4
					self.gDSize = 40
					self.gDSink = 25
					self.gDNum = 1
					self.gDOCorner = 50
					self.gDONext = 32

				if selectedText == "Screw 5 x 50 mm ":
					self.gDDiameter = 5
					self.gDSize = 50
					self.gDSink = 35
					self.gDNum = 1
					self.gDOCorner = 50
					self.gDONext = 32

				if selectedText == "Screw 6 x 60 mm ":
					self.gDDiameter = 6
					self.gDSize = 60
					self.gDSink = 45
					self.gDNum = 1
					self.gDOCorner = 50
					self.gDONext = 32
					
				if selectedText == "Confirmation 7 x 40 mm ":
					self.gDDiameter = 7
					self.gDSize = 40
					self.gDSink = 25
					self.gDNum = 1
					self.gDOCorner = 50
					self.gDONext = 32
					
				if selectedText == "Confirmation 7 x 50 mm ":
					self.gDDiameter = 7
					self.gDSize = 50
					self.gDSink = 35
					self.gDNum = 1
					self.gDOCorner = 50
					self.gDONext = 32
					
				if selectedText == "Confirmation 7 x 70 mm ":
					self.gDDiameter = 7
					self.gDSize = 70
					self.gDSink = 55
					self.gDNum = 1
					self.gDOCorner = 50
					self.gDONext = 32
					
				if selectedText == "Shelf Pin 5 x 16 mm ":
					self.gDDiameter = 5
					self.gDSize = 16
					self.gDSink = 8
					self.gDNum = 15
					self.gDOCorner = 50
					self.gDONext = 32
					self.gDOEdge = 50
					self.gSides = 1

				if selectedText == "Profile Pin 5 x 30 mm ":
					self.gDDiameter = 5
					self.gDSize = 30
					self.gDSink = 25
					self.gDNum = 2
					self.gDOCorner = 5
					self.gDONext = 32

				if selectedText == "Profile Pin 8 x 40 mm ":
					self.gDDiameter = 8
					self.gDSize = 40
					self.gDSink = 35
					self.gDNum = 1
					self.gDOCorner = 50
					self.gDONext = 32

				if selectedText == "Custom mount point ":
					self.gDDiameter = 8
					self.gDSize = 35
					self.gDSink = 20
					self.gDNum = 2
					self.gDOCorner = 50
					self.gDONext = 32

				self.oDowelLabelE.setText(str(self.gDowelLabel))
				self.oDDiameterE.setText(str(self.gDDiameter))
				self.oDSizeE.setText(str(self.gDSize))
				self.oDSinkE.setText(str(self.gDSink))
				self.oDNumE.setText(str(self.gDNum))
				self.oDOCornerE.setText(str(self.gDOCorner))
				self.oDONextE.setText(str(self.gDONext))
				self.oDOEdgeE.setText(str(self.gDOEdge))

				self.showDowels()
		
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def refreshSettings(self):
			
			try:
			
				self.gDowelLabel = str(self.oDowelLabelE.text())
				self.gDDiameter = float(self.oDDiameterE.text())
				self.gDSize = float(self.oDSizeE.text())
				self.gDSink = float(self.oDSinkE.text())
				self.gDNum = int(self.oDNumE.text())
				self.gDOCorner = float(self.oDOCornerE.text())
				self.gDONext = float(self.oDONextE.text())
				self.gDOEdge = float(self.oDOEdgeE.text())

				self.showDowels()
			
			except:
				self.s1S.setText(self.gNoSelection)
				
		# ############################################################################
		def setDowels(self):
			
			try:
				if len(self.gDowels) != 0:
					for d in self.gDowels:
						try:
							d.ViewObject.ShapeColor = self.gObj.ViewObject.ShapeColor
						except:
							skip = 1
				
				self.gDowels = []
				FreeCAD.ActiveDocument.recompute()
			
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
		if len(form.gDowels) != 0:
			for d in form.gDowels:
				try:
					FreeCAD.activeDocument().removeObject(str(d.Name))
				except:
					skip = 1
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
