import FreeCAD, FreeCADGui 
import Draft
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

		gObjects = ""
		
		gObj = ""
		gObjRef = ""
		thick = 0
		
		gSphere = ""
		gSphereSize = 0
		
		gCenterVertex = []
		gCenterObj = []
		gCenterIndex = 0
		
		gAngleX = 0
		gAngleY = 0
		gAngleZ = 0
		
		gStep = 15
		
		gNoSelection = translate('magicAngle', 'select containers or panels to rotate')
		
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
			toolSW = 290
			toolSH = 310
			
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
			self.setWindowTitle(translate('magicAngle', 'magicAngle'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			bsize = 50
			roffset = 10 + bsize
			row = 10
			col1 = 10
			col4 = toolSW - roffset
			col3 = col4 - roffset
			col2 = col3 - roffset
			
			# screen
			info = ""
			info += "                                             "
			info += "                                             "
			info += "                                             "
			self.mIS = QtGui.QLabel(info, self)
			self.mIS.move(col1, row)

			row += 20

			# button
			self.rsB1 = QtGui.QPushButton(translate('magicAngle', 'refresh selection'), self)
			self.rsB1.clicked.connect(self.getSelected)
			self.rsB1.setFixedWidth(toolSW-20)
			self.rsB1.setFixedHeight(40)
			self.rsB1.move(col1, row)

			# ############################################################################
			# options - rotation center point size
			# ############################################################################
			
			row += 50

			# label
			self.ssL = QtGui.QLabel(translate('magicAngle', 'Sphere radius:'), self)
			self.ssL.move(col1, row)

			# button
			self.ssB1 = QtGui.QPushButton("- 1", self)
			self.ssB1.clicked.connect(self.setSphereSizeP)
			self.ssB1.setFixedWidth(bsize)
			self.ssB1.move(col2, row)
			self.ssB1.setAutoRepeat(True)
			
			# text input
			self.ssE = QtGui.QLineEdit(self)
			self.ssE.setText("")
			self.ssE.setFixedWidth(bsize)
			self.ssE.move(col3, row)
			
			# button
			self.ssB2 = QtGui.QPushButton("+ 1", self)
			self.ssB2.clicked.connect(self.setSphereSizeN)
			self.ssB2.setFixedWidth(bsize)
			self.ssB2.move(col4, row)
			self.ssB2.setAutoRepeat(True)

			# ############################################################################
			# options - rotation center point selection
			# ############################################################################
			
			row += 30

			# label
			self.rpL = QtGui.QLabel(translate('magicAngle', 'Rotation point:'), self)
			self.rpL.move(col1, row)

			# button
			self.rpB1 = QtGui.QPushButton("<", self)
			self.rpB1.clicked.connect(self.setCenterP)
			self.rpB1.setFixedWidth(bsize)
			self.rpB1.move(col2, row)
			self.rpB1.setAutoRepeat(True)
			
			# label
			self.rpIS = QtGui.QLabel(info, self)
			self.rpIS.move(col3, row+3)

			# button
			self.rpB2 = QtGui.QPushButton(">", self)
			self.rpB2.clicked.connect(self.setCenterN)
			self.rpB2.setFixedWidth(bsize)
			self.rpB2.move(col4, row)
			self.rpB2.setAutoRepeat(True)

			row += 30

			# button
			self.rpB3 = QtGui.QPushButton(translate('magicAngle', 'add selected vertex'), self)
			self.rpB3.clicked.connect(self.addVertex)
			self.rpB3.setFixedWidth(toolSW-col2-10)
			self.rpB3.setFixedHeight(40)
			self.rpB3.move(col2, row)

			# ############################################################################
			# options - X axis
			# ############################################################################

			row += 50

			# label
			self.xaL = QtGui.QLabel(translate('magicAngle', 'X axis (yaw):'), self)
			self.xaL.move(col1, row)

			# button
			self.xaB1 = QtGui.QPushButton("X-", self)
			self.xaB1.clicked.connect(self.setX1)
			self.xaB1.setFixedWidth(bsize)
			self.xaB1.move(col2, row)
			self.xaB1.setAutoRepeat(True)
			
			# label
			self.xaIS = QtGui.QLabel(info, self)
			self.xaIS.move(col3, row+3)

			# button
			self.xaB2 = QtGui.QPushButton("X+", self)
			self.xaB2.clicked.connect(self.setX2)
			self.xaB2.setFixedWidth(bsize)
			self.xaB2.move(col4, row)
			self.xaB2.setAutoRepeat(True)
			
			# ############################################################################
			# options - Y axis
			# ############################################################################
			
			row += 30
			
			# label
			self.yaL = QtGui.QLabel(translate('magicAngle', 'Y axis (pitch):'), self)
			self.yaL.move(col1, row)

			# button
			self.yaB1 = QtGui.QPushButton("Y-", self)
			self.yaB1.clicked.connect(self.setY1)
			self.yaB1.setFixedWidth(bsize)
			self.yaB1.move(col2, row)
			self.yaB1.setAutoRepeat(True)
			
			# label
			self.yaIS = QtGui.QLabel(info, self)
			self.yaIS.move(col3, row+3)

			# button
			self.yaB2 = QtGui.QPushButton("Y+", self)
			self.yaB2.clicked.connect(self.setY2)
			self.yaB2.setFixedWidth(bsize)
			self.yaB2.move(col4, row)
			self.yaB2.setAutoRepeat(True)

			# ############################################################################
			# options - Z axis
			# ############################################################################
			
			row += 30
			
			# label
			self.zaL = QtGui.QLabel(translate('magicAngle', 'Z axis (roll):'), self)
			self.zaL.move(col1, row)

			# button
			self.zaB1 = QtGui.QPushButton("Z-", self)
			self.zaB1.clicked.connect(self.setZ1)
			self.zaB1.setFixedWidth(bsize)
			self.zaB1.move(col2, row)
			self.zaB1.setAutoRepeat(True)
			
			# label
			self.zaIS = QtGui.QLabel(info, self)
			self.zaIS.move(col3, row+3)

			# button
			self.zaB2 = QtGui.QPushButton("Z+", self)
			self.zaB2.clicked.connect(self.setZ2)
			self.zaB2.setFixedWidth(bsize)
			self.zaB2.move(col4, row)
			self.zaB2.setAutoRepeat(True)
			
			# ############################################################################
			# options - additional
			# ############################################################################

			row += 30

			# label
			self.asL = QtGui.QLabel(translate('magicAngle', 'Angle step:'), self)
			self.asL.move(col1, row)

			# text input
			self.asE = QtGui.QLineEdit(self)
			self.asE.setText(str(self.gStep))
			self.asE.setFixedWidth(bsize)
			self.asE.move(col3, row)
			
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

		def resetGlobals(self):
			
			try:
				FreeCAD.activeDocument().removeObject(str(self.gSphere.Name))
			except:
				skip = 1

			self.gObjects = ""
			self.gObj = ""
			self.gObjRef = ""
			self.thick = 0
		
			self.gSphere = ""
			self.gCenterVertex = []
			self.gCenterObj = []
			self.gCenterIndex = 0
			
			self.gAngleX = 0
			self.gAngleY = 0
			self.gAngleZ = 0
		
			self.gStep = 15

		# ############################################################################
		def touchTypo(self, iFaceIndex, iVertexIndex):
			
			f = self.gObj.Shape.Faces[iFaceIndex]
			
			# how to touch the typo so that the typo-snake does not notice it ;-) LOL
			v = getattr(f, "Vertex"+"es")
			
			return v[iVertexIndex]
		
		def setCenterPoints(self):
			
			self.gCenterVertex = []
			
			# you can add new center points here, if needed
			
			if self.gObj.isDerivedFrom("App::LinkGroup"):
				v = self.touchTypo(1, 0)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
				
				v = self.touchTypo(1, 1)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
				
				v = self.touchTypo(1, 2)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)

				v = self.touchTypo(1, 3)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
				
				maxIdx = len(self.gObj.Shape.Faces) - 1
				
				v = self.touchTypo(maxIdx, 0)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
			
				v = self.touchTypo(maxIdx, 1)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)

				v = self.touchTypo(maxIdx, 2)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)

				v = self.touchTypo(maxIdx, 3)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
			
			if self.gObj.isDerivedFrom("Part::Cylinder"):
				
				v = self.touchTypo(1, 0)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
				
				v = self.touchTypo(2, 0)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
			
			if self.gObj.isDerivedFrom("Part::Cone"):
				
				v = self.touchTypo(2, 0)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
				
				v = self.touchTypo(1, 0)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)

			try:
				
				v = self.touchTypo(4, 0)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
			
				v = self.touchTypo(4, 1)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)

				v = self.touchTypo(4, 2)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)

				v = self.touchTypo(4, 3)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)

				v = self.touchTypo(5, 0)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)

				v = self.touchTypo(5, 1)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)

				v = self.touchTypo(5, 2)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)

				v = self.touchTypo(5, 3)
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
		
			except:

				self.gCenterVertex.append(FreeCAD.Vector(float(0.0), float(0.0), float(0.0)))
				self.gCenterObj.append(self.gObj)

			try:
				
				v = self.gObj.Shape.CenterOfMass
				self.gCenterVertex.append(FreeCAD.Vector(float(v.x), float(v.y), float(v.z)))
				self.gCenterObj.append(self.gObj)
				
			except:
			
				skip = 1
				
		def setCenterSphere(self):
			
			info = str(self.gCenterIndex + 1) + " / " + str(len(self.gCenterVertex))
			self.rpIS.setText(info)
			
			v = self.gCenterVertex[self.gCenterIndex]
			vObj = self.gCenterObj[self.gCenterIndex]
			[ v ] = MagicPanels.getVerticesPosition([ v ], vObj)

			self.gSphere.Placement = FreeCAD.Placement(v, FreeCAD.Rotation(0, 0, 0))
			self.gSphere.Radius = float(self.ssE.text())
			
			self.gSphere.recompute()

		def setRotation(self, iAxis, iAngle):
			
			self.xaIS.setText(str(self.gAngleX))
			self.yaIS.setText(str(self.gAngleY))
			self.zaIS.setText(str(self.gAngleZ))
			
			v = self.gCenterVertex[self.gCenterIndex]
			vObj = self.gCenterObj[self.gCenterIndex]
			[ v ] = MagicPanels.getVerticesPosition([ v ], vObj)
			
			for o in self.gObjects:
				Draft.rotate(o, iAngle, v, iAxis, False)
			
			FreeCADGui.Selection.clearSelection()
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def getSelected(self):

			try:
				
				self.resetGlobals()

				self.gObjects = FreeCADGui.Selection.getSelection()
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				
				if len(self.gObjects) > 1:
					self.mIS.setText("Multi, " + str(self.gObj.Label))
				else:
					self.mIS.setText(str(self.gObj.Label))
					
				FreeCADGui.Selection.clearSelection()
				
				self.gObjRef = MagicPanels.getReference(self.gObj)
				s = MagicPanels.getSizes(self.gObjRef)
				s.sort()
				self.thick = s[0]
				
				self.gSphere = FreeCAD.ActiveDocument.addObject("Part::Sphere","magicAnglePoint")
				self.gSphere.ViewObject.ShapeColor = (1.0, 0.0, 0.0, 0.0)
				self.gSphere.Radius = int(self.thick)
				self.gSphereSize = int(self.gSphere.Radius.Value)
				self.ssE.setText(str(self.gSphereSize))
			
				self.setCenterPoints()
				self.setCenterSphere()
		
				self.xaIS.setText(str(self.gAngleX))
				self.yaIS.setText(str(self.gAngleY))
				self.zaIS.setText(str(self.gAngleZ))

			except:
				self.mIS.setText(self.gNoSelection)
				return -1

		# ############################################################################
		def setSphereSizeP(self):
			
			try:
				if self.gSphereSize > 10:
					self.gSphere.Radius = self.gSphereSize - 10
					self.gSphereSize = int(self.gSphere.Radius.Value)
					self.ssE.setText(str(self.gSphereSize))
					self.gSphere.recompute()
			except:
				skip = 1
			
		def setSphereSizeN(self):
			
			try:
				self.gSphere.Radius = self.gSphereSize + 10
				self.gSphereSize = int(self.gSphere.Radius.Value)
				self.ssE.setText(str(self.gSphereSize))
				self.gSphere.recompute()
			except:
				skip = 1

		# ############################################################################
		def setCenterP(self):
			
			try:
				if self.gCenterIndex - 1 < 0:
					self.gCenterIndex = len(self.gCenterVertex) - 1
				else:
					self.gCenterIndex = self.gCenterIndex - 1
					
				self.setCenterSphere()
			except:
				self.mIS.setText(self.gNoSelection)
			
		def setCenterN(self):
			
			try:
				if self.gCenterIndex + 1 > len(self.gCenterVertex) - 1:
					self.gCenterIndex = 0
				else:
					self.gCenterIndex = self.gCenterIndex + 1
					
				self.setCenterSphere()
			except:
				self.mIS.setText(self.gNoSelection)
		
		def addVertex(self):
			
			try:
				skip = 0
				
				vObj = FreeCADGui.Selection.getSelection()[0]
				v = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

				if str(v.ShapeType) == "Vertex":
					v = FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z))
					self.gCenterVertex.append(v)
					self.gCenterObj.append(vObj)
				
				elif str(v.ShapeType) == "Edge":
					[ v, v2 ] = MagicPanels.getEdgeVertices(v)
					v = FreeCAD.Vector(v[0], v[1], v[2])
					self.gCenterVertex.append(v)
					self.gCenterObj.append(vObj)
				
				elif str(v.ShapeType) == "Face":
					v = v.CenterOfMass
					v = FreeCAD.Vector(float(v.x), float(v.y), float(v.z))
					self.gCenterVertex.append(v)
					self.gCenterObj.append(vObj)

				else:
					skip = 1

				if skip == 0:
					self.gCenterIndex = len(self.gCenterVertex) - 1
					self.setCenterSphere()

			except:
				skip = 1
			
		# ############################################################################
		def setX1(self):
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleX = self.gAngleX - self.gStep
				self.setRotation(FreeCAD.Vector(1, 0, 0), self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)
			
		def setX2(self):
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleX = self.gAngleX + self.gStep
				self.setRotation(FreeCAD.Vector(1, 0, 0), -self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)
			
		def setY1(self):
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleY = self.gAngleY - self.gStep
				self.setRotation(FreeCAD.Vector(0, 1, 0), self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)
		
		def setY2(self):
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleY = self.gAngleY + self.gStep
				self.setRotation(FreeCAD.Vector(0, 1, 0), -self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)

		def setZ1(self):
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleZ = self.gAngleZ - self.gStep
				self.setRotation(FreeCAD.Vector(0, 0, 1), self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)
		
		def setZ2(self):
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleZ = self.gAngleZ + self.gStep
				self.setRotation(FreeCAD.Vector(0, 0, 1), -self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)

	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		if form.gSphere != "":
			try:
				FreeCAD.ActiveDocument.removeObject(str(form.gSphere.Name))
			except:
				skip = 1
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
