import FreeCAD, FreeCADGui 
import Draft, time
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
			toolSW = 280
			toolSH = 400
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('magicAngle', 'magicAngle'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			bsize = 50
			area = toolSW - 20
			roffset = 10 + bsize
			row = 10
			col1 = 10
			col4 = toolSW - roffset
			col3 = col4 - roffset
			col2 = col3 - roffset
			
			# screen
			self.mIS = QtGui.QLabel("", self)
			self.mIS.setFixedWidth(area)
			
			# button
			self.rsB1 = QtGui.QPushButton(translate('magicAngle', 'refresh selection'), self)
			self.rsB1.clicked.connect(self.getSelected)
			self.rsB1.setFixedHeight(40)

			# ############################################################################
			# options - rotation center point size
			# ############################################################################
			
			# label
			self.ssL = QtGui.QLabel(translate('magicAngle', 'Sphere radius:'), self)

			# button
			self.ssB1 = QtGui.QPushButton("- 1", self)
			self.ssB1.clicked.connect(self.setSphereSizeP)
			self.ssB1.setFixedWidth(bsize)
			self.ssB1.setAutoRepeat(True)
			
			# text input
			self.ssE = QtGui.QLineEdit(self)
			self.ssE.setText("")
			self.ssE.setFixedWidth(bsize)
			
			# button
			self.ssB2 = QtGui.QPushButton("+ 1", self)
			self.ssB2.clicked.connect(self.setSphereSizeN)
			self.ssB2.setFixedWidth(bsize)
			self.ssB2.setAutoRepeat(True)

			# ############################################################################
			# options - rotation center point selection
			# ############################################################################
			
			# label
			self.rpL = QtGui.QLabel(translate('magicAngle', 'Rotation point:'), self)

			# button
			self.rpB1 = QtGui.QPushButton("<", self)
			self.rpB1.clicked.connect(self.setCenterP)
			self.rpB1.setFixedWidth(bsize)
			self.rpB1.setAutoRepeat(True)
			
			# label
			self.rpIS = QtGui.QLabel("", self)

			# button
			self.rpB2 = QtGui.QPushButton(">", self)
			self.rpB2.clicked.connect(self.setCenterN)
			self.rpB2.setFixedWidth(bsize)
			self.rpB2.setAutoRepeat(True)

			# button
			self.rpB3 = QtGui.QPushButton(translate('magicAngle', 'add selected vertex, edge or face'), self)
			self.rpB3.clicked.connect(self.addVertex)
			self.rpB3.setFixedHeight(40)

			# ############################################################################
			# options - X axis
			# ############################################################################

			# label
			self.xaL = QtGui.QLabel(translate('magicAngle', 'X axis (yaw):'), self)

			# button
			self.xaB1 = QtGui.QPushButton("X-", self)
			self.xaB1.clicked.connect(self.setX1)
			self.xaB1.setFixedWidth(bsize)
			self.xaB1.setAutoRepeat(True)
			
			# label
			self.xaIS = QtGui.QLabel("", self)

			# button
			self.xaB2 = QtGui.QPushButton("X+", self)
			self.xaB2.clicked.connect(self.setX2)
			self.xaB2.setFixedWidth(bsize)
			self.xaB2.setAutoRepeat(True)
			
			# ############################################################################
			# options - Y axis
			# ############################################################################
			
			# label
			self.yaL = QtGui.QLabel(translate('magicAngle', 'Y axis (pitch):'), self)

			# button
			self.yaB1 = QtGui.QPushButton("Y-", self)
			self.yaB1.clicked.connect(self.setY1)
			self.yaB1.setFixedWidth(bsize)
			self.yaB1.setAutoRepeat(True)
			
			# label
			self.yaIS = QtGui.QLabel("", self)

			# button
			self.yaB2 = QtGui.QPushButton("Y+", self)
			self.yaB2.clicked.connect(self.setY2)
			self.yaB2.setFixedWidth(bsize)
			self.yaB2.setAutoRepeat(True)

			# ############################################################################
			# options - Z axis
			# ############################################################################
			
			# label
			self.zaL = QtGui.QLabel(translate('magicAngle', 'Z axis (roll):'), self)

			# button
			self.zaB1 = QtGui.QPushButton("Z-", self)
			self.zaB1.clicked.connect(self.setZ1)
			self.zaB1.setFixedWidth(bsize)
			self.zaB1.setAutoRepeat(True)
			
			# label
			self.zaIS = QtGui.QLabel("", self)

			# button
			self.zaB2 = QtGui.QPushButton("Z+", self)
			self.zaB2.clicked.connect(self.setZ2)
			self.zaB2.setFixedWidth(bsize)
			self.zaB2.setAutoRepeat(True)
			
			# ############################################################################
			# options - additional
			# ############################################################################

			# label
			self.asL = QtGui.QLabel(translate('magicAngle', 'Angle step:'), self)

			# text input
			self.asE = QtGui.QLineEdit(self)
			self.asE.setText(str(self.gStep))
			self.asE.setFixedWidth(bsize)
			
			# ############################################################################
			# animation checkbox
			# ############################################################################

			self.animcb = QtGui.QCheckBox(translate('magicAngle', ' - animate rotation'), self)
			self.animcb.setCheckState(QtCore.Qt.Unchecked)
			
			# ############################################################################
			# build GUI layout
			# ############################################################################
		
			# create structure
			self.row1 = QtGui.QHBoxLayout()
			self.row1.setAlignment(QtGui.Qt.AlignLeft)
			self.row1.addWidget(self.mIS)
			
			self.row2 = QtGui.QHBoxLayout()
			self.row2.addWidget(self.rsB1)
			
			self.row3 = QtGui.QGridLayout()
			self.row3.addWidget(self.ssL, 0, 0)
			self.row3.addWidget(self.ssB1, 0, 1)
			self.row3.addWidget(self.ssE, 0, 2)
			self.row3.addWidget(self.ssB2, 0, 3)
			
			self.row3.addWidget(self.rpL, 1, 0)
			self.row3.addWidget(self.rpB1, 1, 1)
			self.row3.addWidget(self.rpIS, 1, 2)
			self.row3.addWidget(self.rpB2, 1, 3)
			
			self.groupBody1 = QtGui.QGroupBox(None, self)
			self.groupBody1.setLayout(self.row3)
			
			self.row4 = QtGui.QHBoxLayout()
			self.row4.addWidget(self.rpB3)
			
			self.row5 = QtGui.QGridLayout()
			self.row5.addWidget(self.xaL, 0, 0)
			self.row5.addWidget(self.xaB1, 0, 1)
			self.row5.addWidget(self.xaIS, 0, 2)
			self.row5.addWidget(self.xaB2, 0, 3)
			
			self.row5.addWidget(self.yaL, 1, 0)
			self.row5.addWidget(self.yaB1, 1, 1)
			self.row5.addWidget(self.yaIS, 1, 2)
			self.row5.addWidget(self.yaB2, 1, 3)
			
			self.row5.addWidget(self.zaL, 2, 0)
			self.row5.addWidget(self.zaB1, 2, 1)
			self.row5.addWidget(self.zaIS, 2, 2)
			self.row5.addWidget(self.zaB2, 2, 3)
			
			self.row5.addWidget(self.asL, 3, 0)
			self.row5.addWidget(self.asE, 3, 2)
			
			self.groupBody2 = QtGui.QGroupBox(None, self)
			self.groupBody2.setLayout(self.row5)
			
			self.row6 = QtGui.QHBoxLayout()
			self.row6.addWidget(self.animcb)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			
			self.layout.addLayout(self.row1)
			self.layout.addLayout(self.row2)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody1)
			self.layout.addStretch()
			self.layout.addLayout(self.row4)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody2)
			self.layout.addStretch()
			self.layout.addLayout(self.row6)
			
			self.setLayout(self.layout)
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()
			
			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)
			
			# set window position
			sw = self.width()
			sh = self.height()
			pw = int( FreeCADGui.getMainWindow().width() - sw ) - 5
			ph = int( FreeCADGui.getMainWindow().height() - sh ) + 30
			self.setGeometry(pw, ph, sw, sh)

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
		def initRotationPoint(self, iFaceIndex, iVertexIndex):
			
			try:
				f = self.gObj.Shape.Faces[iFaceIndex]
				v = getattr(f, "Vertex"+"es")
				self.gCenterVertex.append(FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)))
				self.gCenterObj.append(self.gObj)
				return v[iVertexIndex]
				
			except:
				return -1
		
		def setCenterPoints(self):
			
			self.gCenterVertex = []
			
			# you can add new center points here, if needed
			
			if self.gObj.isDerivedFrom("App::LinkGroup"):
				
				self.initRotationPoint(1, 0)
				self.initRotationPoint(1, 1)
				self.initRotationPoint(1, 2)
				self.initRotationPoint(1, 3)
				
				maxIdx = len(self.gObj.Shape.Faces) - 1
				self.initRotationPoint(maxIdx, 0)
				self.initRotationPoint(maxIdx, 1)
				self.initRotationPoint(maxIdx, 2)
				self.initRotationPoint(maxIdx, 3)
				
			if self.gObj.isDerivedFrom("Part::Cylinder"):
				
				self.initRotationPoint(1, 0)
				self.initRotationPoint(2, 0)
				
			if self.gObj.isDerivedFrom("Part::Cone"):
				
				self.initRotationPoint(2, 0)
				self.initRotationPoint(1, 0)
				
				self.initRotationPoint(4, 0)
				self.initRotationPoint(4, 1)
				self.initRotationPoint(4, 2)
				self.initRotationPoint(4, 3)
				self.initRotationPoint(5, 0)
				self.initRotationPoint(5, 1)
				self.initRotationPoint(5, 2)
				self.initRotationPoint(5, 3)
				
			try:
				# init with all vertices
				vertices = MagicPanels.touchTypo(self.gObj.Shape)
				self.gCenterVertex = MagicPanels.vertices2vectors(vertices)
				for v in vertices:
					self.gCenterObj.append(self.gObj)

				# try to add CenterOfMass
				v = self.gObj.Shape.CenterOfMass
				self.gCenterVertex.append(FreeCAD.Vector(float(v.x), float(v.y), float(v.z)))
				self.gCenterObj.append(self.gObj)
				
			except:
				self.gCenterVertex.append(FreeCAD.Vector(float(0.0), float(0.0), float(0.0)))
				self.gCenterObj.append(self.gObj)

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
			
			if self.animcb.isChecked():
				
				if iAngle > 0:
					angle = 1
				else:
					angle = -1

				for o in self.gObjects:
					
					restore = o.Placement
					
					scope = abs(iAngle)
					for i in range(1, scope):
						
						if i < scope/2:
							anim = 0.001
						elif i < 4*scope/5:
							anim = 0.05
						else:
							anim = 0.08
						
						time.sleep(anim)
						Draft.rotate(o, angle, v, iAxis, False)
						FreeCADGui.Selection.clearSelection()
						FreeCADGui.updateGui()
					
					o.Placement = restore
					Draft.rotate(o, iAngle, v, iAxis, False)
					FreeCADGui.Selection.clearSelection()
			else:
				
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
				MagicPanels.setColor(self.gSphere, 0, (1.0, 0.0, 0.0, 1.0), "color")
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
				
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

				if str(sub.ShapeType) == "Vertex":
					v = FreeCAD.Vector(float(sub.X), float(sub.Y), float(sub.Z))
					self.gCenterVertex.append(v)
					self.gCenterObj.append(obj)
				
				elif str(sub.ShapeType) == "Edge":
					[ v1, v2 ] = MagicPanels.getEdgeVertices(sub)
					self.gCenterVertex.append(FreeCAD.Vector(v1[0], v1[1], v1[2]))
					self.gCenterObj.append(obj)
					self.gCenterVertex.append(FreeCAD.Vector(v2[0], v2[1], v2[2]))
					self.gCenterObj.append(obj)
					self.gCenterVertex.append(sub.CenterOfMass)
					self.gCenterObj.append(obj)
				
				elif str(sub.ShapeType) == "Face":
					vertices = MagicPanels.touchTypo(sub)
					self.gCenterVertex += MagicPanels.vertices2vectors(vertices)
					for v in vertices:
						self.gCenterObj.append(obj)
						
					self.gCenterVertex.append(sub.CenterOfMass)
					self.gCenterObj.append(obj)

				else:
					skip = 1

				if skip == 0:
					self.gCenterIndex = len(self.gCenterVertex) - 1
					self.setCenterSphere()

				FreeCADGui.Selection.clearSelection()
				
			except:
				skip = 1
			
		# ############################################################################
		def setX1(self):
			
			FreeCAD.ActiveDocument.openTransaction("magicAngleX1")
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleX = self.gAngleX - self.gStep
				self.setRotation(FreeCAD.Vector(1, 0, 0), self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)
			
			FreeCAD.ActiveDocument.commitTransaction()
			
		def setX2(self):
			
			FreeCAD.ActiveDocument.openTransaction("magicAngleX2")
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleX = self.gAngleX + self.gStep
				self.setRotation(FreeCAD.Vector(1, 0, 0), -self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)
			
			FreeCAD.ActiveDocument.commitTransaction()
			
		def setY1(self):
			
			FreeCAD.ActiveDocument.openTransaction("magicAngleY1")
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleY = self.gAngleY - self.gStep
				self.setRotation(FreeCAD.Vector(0, 1, 0), self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)
			
			FreeCAD.ActiveDocument.commitTransaction()
			
		def setY2(self):
			
			FreeCAD.ActiveDocument.openTransaction("magicAngleY2")
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleY = self.gAngleY + self.gStep
				self.setRotation(FreeCAD.Vector(0, 1, 0), -self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)
	
			FreeCAD.ActiveDocument.commitTransaction()
			
		def setZ1(self):
			
			FreeCAD.ActiveDocument.openTransaction("magicAngleZ1")
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleZ = self.gAngleZ - self.gStep
				self.setRotation(FreeCAD.Vector(0, 0, 1), self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)
				
			FreeCAD.ActiveDocument.commitTransaction()
		
		def setZ2(self):
			
			FreeCAD.ActiveDocument.openTransaction("magicAngleZ2")
			
			try:
				self.gStep = int(self.asE.text())
				self.gAngleZ = self.gAngleZ + self.gStep
				self.setRotation(FreeCAD.Vector(0, 0, 1), -self.gStep)
			except:
				self.mIS.setText(self.gNoSelection)
			
			FreeCAD.ActiveDocument.commitTransaction()

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
