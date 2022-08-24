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
		gObjBase = ""
		gThick = 0
		
		gDrillFace = ""
		gFIndex = 0
		gFPlane = ""
		gFType = ""
		gDrillFaceKey = ""
		gDrillSink = ""
		
		gEdge = ""
		gEArr = []
		gEIndex = 0

		gPosition = 0
		gRAxis = ""
		gRAngles = []
		gRIndex = 0

		# Holes, Countersinks, Counterbores
		gDBType = "" 

		# should not be reset if object change
		gDBSides = 0
		gDrillBits = []
		gDBLabel = ""
		gDBDiameter = 8
		gDBDiameter2 = 10
		gDBSize = 35
		gDBNum = 2
		gDBOCorner = 50
		gDBONext = 32
		gDBOEdge = 0
		gDBSink = 0 # used for pocket holes only
		
		
		# settings for pocket holes
		gDBPocketR = 75
		gDBPocketS = -5
		
		gPocketAxis = ""
		gPocketCenter = ""
		
		gInit = 1
		
		gNoSelection = translate('magicDriller', 'please select face')
		
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
			toolSH = 640
			
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
			self.setWindowTitle(translate('magicDriller', 'magicDriller'))
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
			self.s1B1 = QtGui.QPushButton(translate('magicDriller', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(200)
			self.s1B1.move(10, 40)

			row = 50

			# ############################################################################
			# options - select edge
			# ############################################################################

			row += 30

			# label
			self.s2L = QtGui.QLabel(translate('magicDriller', 'Select edge:'), self)
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
			self.s3L = QtGui.QLabel(translate('magicDriller', 'Adjust edge:'), self)
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
			# options - adjust rotation
			# ############################################################################

			row += 30
			
			# label
			self.s4L = QtGui.QLabel(translate('magicDriller', 'Adjust rotation:'), self)
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
			self.s5L = QtGui.QLabel(translate('magicDriller', 'Select sides:'), self)
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
			# options - drill bit types
			# ############################################################################
			
			row += 30
			
			# border options
			self.s6Slist = (
						"Holes",
						"Countersinks",
						"Counterbores",
						"Pocket holes"
						)
			
			self.s6S = QtGui.QComboBox(self)
			self.s6S.addItems(self.s6Slist)
			self.s6S.setCurrentIndex(self.s6Slist.index("Holes"))
			self.s6S.activated[str].connect(self.setDrillBitType)
			self.s6S.setFixedWidth(200)
			self.s6S.move(10, row)

			# ############################################################################
			# options - mounting samples
			# ############################################################################

			row += 30

			# border options
			self.s7Slist = (
						"Dowel 6 x 35 mm ",
						"Dowel 8 x 35 mm ",
						"Dowel 10 x 35 mm ",
						"Screw 3 x 20 mm ",
						"Screw 4.5 x 40 mm ",
						"Screw 4 x 40 mm ",
						"Screw 5 x 50 mm ",
						"Screw 6 x 60 mm ",
						"Shelf Pin 5 x 16 mm ",
						"Profile Pin 5 x 30 mm ",
						"Profile Pin 8 x 40 mm "
						)
			
			self.gDBLabel = "Dowel 8 x 35 mm "
			self.s7S = QtGui.QComboBox(self)
			self.s7S.addItems(self.s7Slist)
			self.s7S.setCurrentIndex(self.s7Slist.index(self.gDBLabel))
			self.s7S.activated[str].connect(self.setCustomDrillbits)
			self.s7S.setFixedWidth(200)
			self.s7S.move(10, row)
			self.gDBType = "Holes"
			
			# ############################################################################
			# options - drill bits number per side
			# ############################################################################

			row += 30
			
			# label
			self.oDBNumL = QtGui.QLabel(translate('magicDriller', 'Holes per side:'), self)
			self.oDBNumL.move(10, row+3)

			# text input
			self.oDBNumE = QtGui.QLineEdit(self)
			self.oDBNumE.setText(str(self.gDBNum))
			self.oDBNumE.setFixedWidth(50)
			self.oDBNumE.move(160, row)

			# ############################################################################
			# options - hole diameter
			# ############################################################################
			
			row += 30

			# label
			self.oDBDiameterL = QtGui.QLabel(translate('magicDriller', 'Hole diameter:'), self)
			self.oDBDiameterL.move(10, row+3)

			# text input
			self.oDBDiameterE = QtGui.QLineEdit(self)
			self.oDBDiameterE.setText(str(self.gDBDiameter))
			self.oDBDiameterE.setFixedWidth(50)
			self.oDBDiameterE.move(160, row)

			# ############################################################################
			# options - hole diameter for countersinks or counterbores
			# ############################################################################
			
			row += 30

			# label
			self.oDBDiameter2L = QtGui.QLabel(translate('magicDriller', 'Countersink diameter:'), self)
			self.oDBDiameter2L.move(10, row+3)

			# text input
			self.oDBDiameter2E = QtGui.QLineEdit(self)
			self.oDBDiameter2E.setText(str(self.gDBDiameter2))
			self.oDBDiameter2E.setFixedWidth(50)
			self.oDBDiameter2E.move(160, row)

			self.oDBDiameter2L.hide()
			self.oDBDiameter2E.hide()

			# ############################################################################
			# options - hole depth
			# ############################################################################

			row += 30
			
			# label
			self.oDBSizeL = QtGui.QLabel(translate('magicDriller', 'Hole depth:'), self)
			self.oDBSizeL.move(10, row+3)

			# text input
			self.oDBSizeE = QtGui.QLineEdit(self)
			self.oDBSizeE.setText(str(self.gDBSize))
			self.oDBSizeE.setFixedWidth(50)
			self.oDBSizeE.move(160, row)

			# ############################################################################
			# options - offset from corner
			# ############################################################################

			row += 30
			
			# label
			self.oDBOCornerL = QtGui.QLabel(translate('magicDriller', 'Offset from corner:'), self)
			self.oDBOCornerL.move(10, row+3)

			# text input
			self.oDBOCornerE = QtGui.QLineEdit(self)
			self.oDBOCornerE.setText(str(self.gDBOCorner))
			self.oDBOCornerE.setFixedWidth(50)
			self.oDBOCornerE.move(160, row)

			# ############################################################################
			# options - offset between dowels
			# ############################################################################

			row += 30
			
			# label
			self.oDONextL = QtGui.QLabel(translate('magicDriller', 'Offset between holes:'), self)
			self.oDONextL.move(10, row+3)

			# text input
			self.oDONextE = QtGui.QLineEdit(self)
			self.oDONextE.setText(str(self.gDBONext))
			self.oDONextE.setFixedWidth(50)
			self.oDONextE.move(160, row)

			# ############################################################################
			# options - offset from edge
			# ############################################################################

			row += 30
			
			# label
			self.oDBOEdgeL = QtGui.QLabel(translate('magicDriller', 'Offset from edge:'), self)
			self.oDBOEdgeL.move(10, row+3)

			# text input
			self.oDBOEdgeE = QtGui.QLineEdit(self)
			self.oDBOEdgeE.setText(str(self.gDBOEdge))
			self.oDBOEdgeE.setFixedWidth(50)
			self.oDBOEdgeE.move(160, row)

			# ############################################################################
			# options - pocket rotation
			# ############################################################################

			row += 30
			
			# label
			self.oDBPocketRL = QtGui.QLabel(translate('magicDriller', 'Pocket rotation:'), self)
			self.oDBPocketRL.move(10, row+3)

			# text input
			self.oDBPocketRE = QtGui.QLineEdit(self)
			self.oDBPocketRE.setText(str(self.gDBPocketR))
			self.oDBPocketRE.setFixedWidth(50)
			self.oDBPocketRE.move(160, row)

			self.oDBPocketRL.hide()
			self.oDBPocketRE.hide()
			
			# ############################################################################
			# options - pocket sink
			# ############################################################################

			row += 30
			
			# label
			self.oDBPocketSL = QtGui.QLabel(translate('magicDriller', 'Pocket sink:'), self)
			self.oDBPocketSL.move(10, row+3)

			# text input
			self.oDBPocketSE = QtGui.QLineEdit(self)
			self.oDBPocketSE.setText(str(self.gDBPocketS))
			self.oDBPocketSE.setFixedWidth(50)
			self.oDBPocketSE.move(160, row)

			self.oDBPocketSL.hide()
			self.oDBPocketSE.hide()

			# ############################################################################
			# options - end settings
			# ############################################################################

			row += 30

			# button
			self.e1B1 = QtGui.QPushButton(translate('magicDriller', 'set custom values'), self)
			self.e1B1.clicked.connect(self.refreshSettings)
			self.e1B1.setFixedWidth(200)
			self.e1B1.move(10, row)

			row += 40

			# button
			self.e2B1 = QtGui.QPushButton(translate('magicDriller', 'drill below drill bits'), self)
			self.e2B1.clicked.connect(self.drillHoles)
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
			for d in self.gDrillBits:
				d.Placement.Rotation = reset
			
			angle = self.gRAngles[self.gRIndex]
			axis = self.gRAxis

			for d in self.gDrillBits:
				
				x = d.Placement.Base.x
				y = d.Placement.Base.y
				z = d.Placement.Base.z
			
				center = FreeCAD.Vector(x, y, z)
			
				Draft.rotate(d, angle, center, axis, False)
			
			if self.gDBType == "Pocket holes":
				
				for d in self.gDrillBits:
				
					axis = self.gPocketAxis
					center = FreeCAD.Vector(x, y, z)
					Draft.rotate(d, self.gDBPocketR, center, axis, False)
			
			
			FreeCADGui.Selection.clearSelection()
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def createDrillBit(self, iX, iY, iZ):

			if self.gDBType == "Holes":

				d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DrillBitHole")
				d.Label = str(self.gDBLabel)

				d.Radius = self.gDBDiameter / 2
				d.Height = self.gDBSize
				
				colors = [ (1.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0) ]
				d.ViewObject.DiffuseColor = colors

			if self.gDBType == "Countersinks":

				d = FreeCAD.ActiveDocument.addObject("Part::Cone","DrillBitCountersink")
				d.Label = str(self.gDBLabel)

				d.Radius1 = self.gDBDiameter / 2
				d.Radius2 = self.gDBDiameter2 / 2
				d.Height = self.gDBSize
				
				colors = [ (0.0, 1.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ]
				d.ViewObject.DiffuseColor = colors
			

			if self.gDBType == "Counterbores":

				d = FreeCAD.ActiveDocument.addObject("Part::Cone","DrillBitCounterbore")
				d.Label = str(self.gDBLabel)

				d.Radius1 = self.gDBDiameter / 2
				d.Radius2 = self.gDBDiameter2 / 2
				d.Height = self.gDBSize
				
				colors = [ (0.0, 0.0, 1.0, 0.0), (0.0, 1.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ]
				d.ViewObject.DiffuseColor = colors
				
			if self.gDBType == "Pocket holes":

				d = FreeCAD.ActiveDocument.addObject("Part::Cone","DrillBitPocket")
				d.Label = str(self.gDBLabel)

				d.Radius1 = self.gDBDiameter / 2
				d.Radius2 = self.gDBDiameter2 / 2
				d.Height = self.gDBSize
				
				colors = [ (0.0, 0.0, 1.0, 0.0), (0.0, 1.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ]
				d.ViewObject.DiffuseColor = colors

			d.Placement.Base.x = iX
			d.Placement.Base.y = iY
			d.Placement.Base.z = iZ

			return d

		# ############################################################################
		def showDrillBits(self):
			
			# ############################################################################
			# remove all dowels
			# ############################################################################
			
			if len(self.gDrillBits) != 0:
				for d in self.gDrillBits:
					try:
						FreeCAD.activeDocument().removeObject(str(d.Name))
					except:
						skip = 1
			
			self.gDrillBits = []
			
			# get settings
			[ v1, v2 ] = MagicPanels.getEdgeVertices(self.gEArr[self.gEIndex])
			
			if not self.gObj.isDerivedFrom("Part::Box"):
				[ v1, v2 ] = MagicPanels.getEdgeNormalized(v1, v2)
			
			# ############################################################################
			# dowels at 1st side
			# ############################################################################
			
			if self.gDBSides == 0 or self.gDBSides == 1:
			
				[ X, Y, Z ] = [ v1[0], v1[1], v1[2] ]
				[ x , y, z ] = [ 0, 0, 0 ]
				
				i = 0
				while i < self.gDBNum:
					
					# edge along X
					if not MagicPanels.equal(v1[0], v2[0]):
						
						if self.gFPlane == "XY":
							x = X - self.gDBOCorner
							if i != 0:
								x = x - ( i * self.gDBONext)
							y = Y + self.gDBOEdge
							z = Z - self.gDBSink
							
						if self.gFPlane == "XZ":
							x = X - self.gDBOCorner
							if i != 0:
								x = x - ( i * self.gDBONext)
							y = Y - self.gDBSink
							z = Z + self.gDBOEdge
				
						# this should not exist
						if self.gFPlane == "YZ":
							[ x, y, z ] = [ X, Y, Z ]
						
						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(1, 0, 0)
						
					# edge along Y
					if not MagicPanels.equal(v1[1], v2[1]):
						
						if self.gFPlane == "XY":
							x = X + self.gDBOEdge
							y = Y - self.gDBOCorner
							if i != 0:
								y = y - ( i * self.gDBONext)
							z = Z - self.gDBSink
					
						# this should not exist
						if self.gFPlane == "XZ":
							[ x, y, z ] = [ X, Y, Z ]
					
						if self.gFPlane == "YZ":
							x = X - self.gDBSink
							y = Y - self.gDBOCorner
							if i != 0:
								y = y - ( i * self.gDBONext)
							z = Z + self.gDBOEdge

						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 1, 0)
						
					# edge along Z
					if not MagicPanels.equal(v1[2], v2[2]):
						
						if self.gFPlane == "XY":
							x = X + self.gDBOEdge
							y = Y - self.gDBSink
							z = Z - self.gDBOCorner
							if i != 0:
								z = z - ( i * self.gDBONext)
						
						if self.gFPlane == "XZ":
							x = X - self.gDBOEdge
							y = Y - self.gDBSink
							z = Z - self.gDBOCorner
							if i != 0:
								z = z - ( i * self.gDBONext)
								
						if self.gFPlane == "YZ":
							x = X - self.gDBSink
							y = Y + self.gDBOEdge
							z = Z - self.gDBOCorner
							if i != 0:
								z = z - ( i * self.gDBONext)

						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 0, 1)

					# ############################################################################
					# create dowel
					# ############################################################################
					
					d = self.createDrillBit(x, y, z)
					self.gDrillBits.append(d)
					
					i = i + 1
			
			# ############################################################################
			# dowels at 2nd side
			# ############################################################################

			if self.gDBSides == 0 or self.gDBSides == 2:
			
				[ X, Y, Z ] = [ v2[0], v2[1], v2[2] ]
				[ x , y, z ] = [ 0, 0, 0 ]

				i = 0
				while i < self.gDBNum:
					
					# edge along X
					if not MagicPanels.equal(v1[0], v2[0]):
						
						if self.gFPlane == "XY":
							x = X + self.gDBOCorner
							if i != 0:
								x = x + ( i * self.gDBONext)
							y = Y + self.gDBOEdge
							z = Z - self.gDBSink
					
						if self.gFPlane == "XZ":
							x = X + self.gDBOCorner
							if i != 0:
								x = x + ( i * self.gDBONext)
							y = Y - self.gDBSink
							z = Z + self.gDBOEdge
						
						# this should not exist
						if self.gFPlane == "YZ":
							[ x, y, z ] = [ X, Y, Z ]

						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(1, 0, 0)

					# edge along Y
					if not MagicPanels.equal(v1[1], v2[1]):
						
						if self.gFPlane == "XY":
							x = X + self.gDBOEdge
							y = Y + self.gDBOCorner
							if i != 0:
								y = y + ( i * self.gDBONext)
							z = Z - self.gDBSink
					
						# this should not exist
						if self.gFPlane == "XZ":
							[ x, y, z ] = [ X, Y, Z ]
					
						if self.gFPlane == "YZ":
							x = X - self.gDBSink
							y = Y + self.gDBOCorner
							if i != 0:
								y = y + ( i * self.gDBONext)
							z = Z + self.gDBOEdge
							
						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 1, 0)

					# edge along Z
					if not MagicPanels.equal(v1[2], v2[2]):
						
						if self.gFPlane == "XY":
							x = X + self.gDBOEdge
							y = Y - self.gDBSink
							z = Z + self.gDBOCorner
							if i != 0:
								z = z + ( i * self.gDBONext)
					
						if self.gFPlane == "XZ":
							x = X - self.gDBOEdge
							y = Y - self.gDBSink
							z = Z + self.gDBOCorner
							if i != 0:
								z = z + ( i * self.gDBONext)
					
						if self.gFPlane == "YZ":
							x = X - self.gDBSink
							y = Y + self.gDBOEdge
							z = Z + self.gDBOCorner
							if i != 0:
								z = z + ( i * self.gDBONext)
					
						# settings for pocket holes
						self.gPocketAxis = FreeCAD.Vector(0, 0, 1)
						
					# ############################################################################
					# create dowel
					# ############################################################################
					
					d = self.createDrillBit(x, y, z)
					self.gDrillBits.append(d)
					
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
			
			self.gDrillFace = ""
			self.gFIndex = 0
			self.gFPlane = ""
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

				self.gObjBase = MagicPanels.getReference()
				
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				self.gDrillFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				self.gFIndex = MagicPanels.getFaceIndex(self.gObj, self.gDrillFace)
				FreeCADGui.Selection.clearSelection()
				
				n = ""
				n += str(self.gObj.Label)
				n += ", "
				n += "Face"
				n += str(self.gFIndex)
				self.s1S.setText(n)
				
				# ############################################################################
				# get plane and type
				# ############################################################################
				
				self.gFPlane = MagicPanels.getFacePlane(self.gDrillFace)
				
				[ self.gFType, 
					arrAll, 
					arrThick, 
					arrShort, 
					arrLong ] = MagicPanels.getFaceEdges(self.gObj, self.gDrillFace)
				
				# ############################################################################
				# set possible edges
				# ############################################################################
				
				if self.gFType == "edge":
					
					if len(arrShort) == 0:
						self.gEArr = arrLong
					
					if len(arrLong) == 0:
						self.gEArr = arrShort

				if self.gFType == "surface":
					self.gEArr = arrAll
					
				# ############################################################################
				# set possible rotations
				# ############################################################################
				
				if self.gFPlane == "XY":
					self.gRAngles.append(0)
					self.gRAngles.append(180)
					self.gRAxis = FreeCAD.Vector(1, 0, 0)

				if self.gFPlane == "XZ":
					self.gRAngles.append(90)
					self.gRAngles.append(270)
					self.gRAxis = FreeCAD.Vector(1, 0, 0)
					
				if self.gFPlane == "YZ":
					self.gRAngles.append(90)
					self.gRAngles.append(270)
					self.gRAxis = FreeCAD.Vector(0, 1, 0)
				
				# ############################################################################
				# set default
				# ############################################################################

				s = MagicPanels.getSizes(self.gObjBase)
				s.sort()
				self.gThick = s[0]
				
				self.gDBOEdge = self.gThick / 2
				self.gRIndex = 0
				
				# ############################################################################
				# try auto adjust dowel
				# ############################################################################

				# adjust sink
				self.gDrillSink = MagicPanels.getFaceSink(self.gObj, self.gDrillFace)
				
				# adjust rotation
				if self.gDrillSink == "+":
					
					if self.gFPlane == "XY":
						self.gRIndex = 1
						
					if self.gFPlane == "XZ":
						self.gRIndex = 0
						
					if self.gFPlane == "YZ":
						self.gRIndex = 1

				else:
				
					if self.gFPlane == "XY":
						self.gRIndex = 0
						
					if self.gFPlane == "XZ":
						self.gRIndex = 1
						
					if self.gFPlane == "YZ":
						self.gRIndex = 0
				
				self.oDBOEdgeE.setText(str(self.gDBOEdge))

				self.showDrillBits()
				
				self.gInit = 0
			
			except:

				self.s1S.setText(self.gNoSelection)
				return -1
			
			
		# ############################################################################
		def setSidesP(self):
			
			try:
				if self.gDBSides - 1 < 0:
					self.gDBSides = 2
				else:
					self.gDBSides = self.gDBSides - 1
					
				self.showDrillBits()
		
			except:
				self.s1S.setText(self.gNoSelection)
				
		def setSidesN(self):
			
			try:
				if self.gDBSides + 1 > 2:
					self.gDBSides = 0
				else:
					self.gDBSides = self.gDBSides + 1
					
				self.showDrillBits()
			
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
				
				self.showDrillBits()
			
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setEdgeN(self):
			
			try:
				if self.gEIndex + 1 > len(self.gEArr) - 1:
					self.gEIndex = 0
				else:
					self.gEIndex = self.gEIndex + 1
					
				self.gEdge = self.gEArr[self.gEIndex]
				
				self.showDrillBits()
			
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def setPosition(self):
			
			try:
				if self.gPosition == 0:
					self.gPosition = 1
				else:
					self.gPosition = 0
				
				self.gDBOEdge = - self.gDBOEdge
				self.oDBOEdgeE.setText(str(self.gDBOEdge))
				
				self.showDrillBits()
				
			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def setRotationP(self):
			
			try:
				if self.gRIndex - 1 < 0:
					self.gRIndex = len(self.gRAngles) - 1
				else:
					self.gRIndex = self.gRIndex - 1
					
				self.showDrillBits()
			
			except:
				self.s1S.setText(self.gNoSelection)
				
		def setRotationN(self):
			
			try:
				if self.gRIndex + 1 > len(self.gRAngles) - 1:
					self.gRIndex = 0
				else:
					self.gRIndex = self.gRIndex + 1
					
				self.showDrillBits()
			
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def setCustomDrillbits(self, selectedText):
			
			try:
			
				self.gDBOEdge = self.gThick / 2
				self.gDBLabel = selectedText
				self.gDBSides = 0
				self.gDBSink = 0
				
				if selectedText == "Dowel 6 x 35 mm ":
					self.gDBDiameter = 6
					self.gDBDiameter2 = 6
					self.gDBSize = 25
					self.gDBNum = 2
					self.gDBOCorner = 50
					self.gDBONext = 32
					
				if selectedText == "Dowel 8 x 35 mm ":
					self.gDBDiameter = 8
					self.gDBDiameter2 = 8
					self.gDBSize = 25
					self.gDBNum = 2
					self.gDBOCorner = 50
					self.gDBONext = 32

				if selectedText == "Dowel 10 x 35 mm ":
					self.gDBDiameter = 10
					self.gDBDiameter2 = 10
					self.gDBSize = 25
					self.gDBNum = 2
					self.gDBOCorner = 50
					self.gDBONext = 32
				
				if selectedText == "Screw 3 x 20 mm ":
					self.gDBDiameter = 2
					self.gDBDiameter2 = 6
					self.gDBSize = 20
					self.gDBNum = 5
					self.gDBOCorner = 50
					self.gDBONext = 32
					self.gDBOEdge = 9
				
				if self.gDBType == "Holes":
					
					if selectedText == "Screw 4.5 x 40 mm ":
						self.gDBDiameter = 3
						self.gDBDiameter2 = 10
						self.gDBSize = 40 - self.gThick
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 32

					if selectedText == "Screw 4 x 40 mm ":
						self.gDBDiameter = 3
						self.gDBDiameter2 = 10
						self.gDBSize = 40 - self.gThick
						self.gDBNum = 1
						self.gDBOCorner = 50
						self.gDBONext = 32

					if selectedText == "Screw 5 x 50 mm ":
						self.gDBDiameter = 4
						self.gDBDiameter2 = 10
						self.gDBSize = 50 - self.gThick
						self.gDBNum = 1
						self.gDBOCorner = 50
						self.gDBONext = 32

					if selectedText == "Screw 6 x 60 mm ":
						self.gDBDiameter = 5
						self.gDBDiameter2 = 10
						self.gDBSize = 60 - self.gThick
						self.gDBNum = 1
						self.gDBOCorner = 50
						self.gDBONext = 32

				else:
				
					if selectedText == "Screw 4.5 x 40 mm ":
						self.gDBDiameter = 3
						self.gDBDiameter2 = 10
						self.gDBSize = 40
						self.gDBNum = 2
						self.gDBOCorner = 50
						self.gDBONext = 32

					if selectedText == "Screw 4 x 40 mm ":
						self.gDBDiameter = 3
						self.gDBDiameter2 = 10
						self.gDBSize = 40
						self.gDBNum = 1
						self.gDBOCorner = 50
						self.gDBONext = 32

					if selectedText == "Screw 5 x 50 mm ":
						self.gDBDiameter = 4
						self.gDBDiameter2 = 10
						self.gDBSize = 50
						self.gDBNum = 1
						self.gDBOCorner = 50
						self.gDBONext = 32

					if selectedText == "Screw 6 x 60 mm ":
						self.gDBDiameter = 5
						self.gDBDiameter2 = 10
						self.gDBSize = 60
						self.gDBNum = 1
						self.gDBOCorner = 50
						self.gDBONext = 32
					
				if selectedText == "Shelf Pin 5 x 16 mm ":
					self.gDBDiameter = 5
					self.gDBDiameter2 = 5
					self.gDBSize = 8
					self.gDBNum = 15
					self.gDBOCorner = 50
					self.gDBONext = 32
					self.gDBOEdge = 50
					self.gDBSides = 1

				if selectedText == "Profile Pin 5 x 30 mm ":
					self.gDBDiameter = 5
					self.gDBDiameter2 = 6
					self.gDBSize = 100
					self.gDBNum = 2
					self.gDBOCorner = 5
					self.gDBONext = 32

				if selectedText == "Profile Pin 8 x 40 mm ":
					self.gDBDiameter = 8
					self.gDBDiameter2 = 9
					self.gDBSize = 100
					self.gDBNum = 1
					self.gDBOCorner = 50
					self.gDBONext = 32

				if self.gDBType == "Pocket holes":
					
					self.gDBDiameter = 3
					self.gDBDiameter2 = 9.5
					self.gDBNum = 2
					self.gDBOCorner = 50
					self.gDBONext = 32
						
					if selectedText == "Screw 4 x 25 mm ":
						self.gDBSize = 75
						self.gDBOEdge = 50
						self.gDBPocketR = 75
						self.gDBPocketS = - 5
						
					if selectedText == "Screw 4 x 30 mm ":
						self.gDBSize = 90
						self.gDBOEdge = 60
						self.gDBPocketR = 75
						self.gDBPocketS = - 6
						
					if selectedText == "Screw 4 x 40 mm ":
						self.gDBSize = 120
						self.gDBOEdge = 80
						self.gDBPocketR = 75
						self.gDBPocketS = - 9
					
					if selectedText == "Screw 4 x 60 mm ":
						self.gDBSize = 180
						self.gDBOEdge = 120
						self.gDBPocketR = 75
						self.gDBPocketS = - 12
					
					self.gDBSink = self.gDBPocketS
					
				self.oDBDiameterE.setText(str(self.gDBDiameter))
				self.oDBDiameter2E.setText(str(self.gDBDiameter2))
				self.oDBSizeE.setText(str(self.gDBSize))
				self.oDBNumE.setText(str(self.gDBNum))
				self.oDBOCornerE.setText(str(self.gDBOCorner))
				self.oDONextE.setText(str(self.gDBONext))
				self.oDBOEdgeE.setText(str(self.gDBOEdge))
				self.oDBPocketRE.setText(str(self.gDBPocketR))
				self.oDBPocketSE.setText(str(self.gDBPocketS))

				self.showDrillBits()
		
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def refreshSettings(self):
			
			try:
			
				self.gDBDiameter = float(self.oDBDiameterE.text())
				self.gDBDiameter2 = float(self.oDBDiameter2E.text())
				self.gDBSize = float(self.oDBSizeE.text())
				self.gDBNum = int(self.oDBNumE.text())
				self.gDBOCorner = float(self.oDBOCornerE.text())
				self.gDBONext = float(self.oDONextE.text())
				self.gDBOEdge = float(self.oDBOEdgeE.text())
				self.gDBPocketR = float(self.oDBPocketRE.text())
				self.gDBPocketS = float(self.oDBPocketSE.text())
				
				if self.gDBType == "Pocket holes":
					self.gDBSink = self.gDBPocketS

				self.showDrillBits()
			
			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def setDrillBitType(self, selected):
			
			try:
				
				self.gDBSink = 0
				
				if selected == "Holes":
					self.gDBType = "Holes"
					
					self.s7Slist = (
						"Dowel 6 x 35 mm ",
						"Dowel 8 x 35 mm ",
						"Dowel 10 x 35 mm ",
						"Screw 3 x 20 mm ",
						"Screw 4.5 x 40 mm ",
						"Screw 4 x 40 mm ",
						"Screw 5 x 50 mm ",
						"Screw 6 x 60 mm ",
						"Shelf Pin 5 x 16 mm ",
						"Profile Pin 5 x 30 mm ",
						"Profile Pin 8 x 40 mm "
						)
			
					self.gDBLabel = "Dowel 8 x 35 mm "
					self.s7S.clear()
					self.s7S.addItems(self.s7Slist)
					self.s7S.setCurrentIndex(self.s7Slist.index(self.gDBLabel))
					
					self.oDBDiameter2L.hide()
					self.oDBDiameter2E.hide()
					
					self.oDBPocketRL.hide()
					self.oDBPocketRE.hide()
					self.oDBPocketSL.hide()
					self.oDBPocketSE.hide()
					
				if selected == "Countersinks":
					self.gDBType = "Countersinks"
				
					self.s7Slist = (
						"Screw 4.5 x 40 mm ",
						"Screw 4 x 40 mm ",
						"Screw 5 x 50 mm ",
						"Screw 6 x 60 mm "
						)
			
					self.gDBLabel = "Screw 4 x 40 mm "
					self.s7S.clear()
					self.s7S.addItems(self.s7Slist)
					self.s7S.setCurrentIndex(self.s7Slist.index(self.gDBLabel))
				
					self.oDBDiameter2L.show()
					self.oDBDiameter2E.show()
					
					self.oDBPocketRL.hide()
					self.oDBPocketRE.hide()
					self.oDBPocketSL.hide()
					self.oDBPocketSE.hide()
					
				if selected == "Counterbores":
					self.gDBType = "Counterbores"
					
					self.s7Slist = (
						"Screw 4.5 x 40 mm ",
						"Screw 4 x 40 mm ",
						"Screw 5 x 50 mm ",
						"Screw 6 x 60 mm "
						)
			
					self.gDBLabel = "Screw 4 x 40 mm "
					self.s7S.clear()
					self.s7S.addItems(self.s7Slist)
					self.s7S.setCurrentIndex(self.s7Slist.index(self.gDBLabel))
					
					self.oDBDiameter2L.show()
					self.oDBDiameter2E.show()
					
					self.oDBPocketRL.hide()
					self.oDBPocketRE.hide()
					self.oDBPocketSL.hide()
					self.oDBPocketSE.hide()
					
				if selected == "Pocket holes":
					self.gDBType = "Pocket holes"
					
					self.s7Slist = (
						"Screw 4 x 25 mm ",
						"Screw 4 x 30 mm ",
						"Screw 4 x 40 mm ",
						"Screw 4 x 60 mm "
						)
			
					self.gDBLabel = "Screw 4 x 40 mm "
					self.s7S.clear()
					self.s7S.addItems(self.s7Slist)
					self.s7S.setCurrentIndex(self.s7Slist.index(self.gDBLabel))
					
					self.oDBDiameter2L.show()
					self.oDBDiameter2E.show()
					
					self.oDBPocketRL.show()
					self.oDBPocketRE.show()
					self.oDBPocketSL.show()
					self.oDBPocketSE.show()
					
				# set other settings and refresh drill bits
				self.setCustomDrillbits(self.gDBLabel)

			except:
				self.s1S.setText(self.gNoSelection)

		# ############################################################################
		def drillHoles(self):
			
			try:
		
				# store face key to find face to drill at new object later
				self.gDrillFaceKey = self.gDrillFace.BoundBox
				
				# set args
				o = []
				if len(self.gDrillBits) != 0:
					for d in self.gDrillBits:
						o.append(d)
				
				# drilling selection
				
				if self.gDBType == "Holes":
					holes = MagicPanels.makeHoles(self.gObj, self.gDrillFace, o )

				if self.gDBType == "Countersinks":
					holes = MagicPanels.makeCountersinks(self.gObj, self.gDrillFace, o )

				if self.gDBType == "Counterbores":
					holes = MagicPanels.makeCounterbores(self.gObj, self.gDrillFace, o )

				if self.gDBType == "Pocket holes":
					holes = MagicPanels.makePocketHoles(self.gObj, self.gDrillFace, o )

				# get new object from selection
				FreeCADGui.Selection.addSelection(holes[0])
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				
				# search for selected face to drill
				index = MagicPanels.getFaceIndexByKey(self.gObj, self.gDrillFaceKey)
				self.gDrillFace = self.gObj.Shape.Faces[index]

				# update status info screen
				face = "Face"+str(MagicPanels.getFaceIndex(self.gObj, self.gDrillFace))
				self.s1S.setText(str(self.gObj.Label)+", "+face)
				
				# remove selection
				FreeCADGui.Selection.clearSelection()
		
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
		if len(form.gDrillBits) != 0:
			for d in form.gDrillBits:
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
