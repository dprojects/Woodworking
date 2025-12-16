import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore
from pivy import coin
import math

import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# Global definitions
# ############################################################################

# add new items only at the end and change self.fitList
getMenuIndexFit = {
	translate('setTextures', 'biggest surface')     : "biggest",
	translate('setTextures', 'fit to Cube')         : "cube",
	translate('setTextures', 'fit to Cylinder')     : "cylinder",
	translate('setTextures', 'fit to Sphere')       : "sphere",
	translate('setTextures', 'auto fit')            : "auto",
	translate('setTextures', 'glass mirror effect') : "glass" # no comma 
}

# add new items only at the end and change self.previewTargetList
getMenuIndexPreview = {
	translate('setTextures', 'repeat X axis')   : "repeatX",
	translate('setTextures', 'repeat Y axis')   : "repeatY",
	translate('setTextures', 'repeat Z axis')   : "repeatZ",
	translate('setTextures', 'rotation X axis') : "rotateX",
	translate('setTextures', 'rotation Y axis') : "rotateY",
	translate('setTextures', 'rotation Z axis') : "rotateZ" # no comma 
}

# ###################################################################################################################
# Qt GUI
# ###################################################################################################################


def showQtMain():

	class QtMainClass(QtGui.QDialog):

		# ############################################################################
		# globals
		# ############################################################################

		gObjects = []
		gBrokenURL = dict()
		
		infoSO = translate('setTextures', 'Settings for: SELECTED objects')
		infoAO = translate('setTextures', 'Settings for: ALL objects')
		
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
			toolSW = 300
			toolSH = 700
			
			# active screen size - FreeCAD main window
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = int( gSW - toolSW )
			gPH = int( gSH - toolSH )

			area = toolSW - 20     # area for info
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('setTextures', 'setTextures'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# objects
			# ############################################################################

			# screen
			self.oObjectsI = QtGui.QLabel(self.infoAO, self)
			self.oObjectsI.setMaximumWidth(area)
			
			# button
			self.oObjectsB = QtGui.QPushButton(translate('setTextures', 'refresh selection'), self)
			self.oObjectsB.clicked.connect(self.getSelected)
			self.oObjectsB.setFixedHeight(40)

			# ############################################################################
			# attributes
			# ############################################################################

			# you can change order here
			self.fitList = (
				translate('setTextures', 'biggest surface'),
				translate('setTextures', 'fit to Cube'),
				translate('setTextures', 'fit to Cylinder'),
				translate('setTextures', 'fit to Sphere'),
				translate('setTextures', 'auto fit'),
				translate('setTextures', 'glass mirror effect') # no comma 
			)
			
			self.oFit = QtGui.QComboBox(self)
			self.oFit.addItems(self.fitList)
			self.oFit.setCurrentIndex(0) # to not complicate things always 0 by default
			self.oFit.textActivated[str].connect(self.setTextureFit)
			
			# URL
			self.oURLInfo = QtGui.QLabel(translate('setTextures', 'Texture URL or local HDD path:'), self)
			
			self.oURLPath = QtGui.QLineEdit(self)
			self.oURLPath.setText("")
			
			self.oURLHDD = QtGui.QPushButton("...", self)
			self.oURLHDD.clicked.connect(self.loadCustomFile)
			self.oURLHDD.setFixedWidth(20)
			
			# repeat X
			self.oRepeatXL = QtGui.QLabel(translate('setTextures', 'Repeat X:'), self)
			self.oRepeatXE = QtGui.QLineEdit(self)
			self.oRepeatXE.setText("1.0")

			# repeat Y
			self.oRepeatYL = QtGui.QLabel(translate('setTextures', 'Repeat Y:'), self)
			self.oRepeatYE = QtGui.QLineEdit(self)
			self.oRepeatYE.setText("1.0")

			# repeat Z
			self.oRepeatZL = QtGui.QLabel(translate('setTextures', 'Repeat Z:'), self)
			self.oRepeatZE = QtGui.QLineEdit(self)
			self.oRepeatZE.setText("1.0")

			# rotation X axis
			self.oRotateAxisXL = QtGui.QLabel(translate('setTextures', 'Rotation X axis:'), self)
			self.oRotateAxisXE = QtGui.QLineEdit(self)
			self.oRotateAxisXE.setText("0.0")
			
			# rotation Y axis
			self.oRotateAxisYL = QtGui.QLabel(translate('setTextures', 'Rotation Y axis:'), self)
			self.oRotateAxisYE = QtGui.QLineEdit(self)
			self.oRotateAxisYE.setText("0.0")
			
			# rotation Z axis
			self.oRotateAxisZL = QtGui.QLabel(translate('setTextures', 'Rotation Z axis:'), self)
			self.oRotateAxisZE = QtGui.QLineEdit(self)
			self.oRotateAxisZE.setText("1.0")
			
			# rotation angle
			self.oRotateAngleL = QtGui.QLabel(translate('setTextures', 'Rotation angle (degrees):'), self)
			self.oRotateAngleE = QtGui.QLineEdit(self)
			self.oRotateAngleE.setText("0.0")
		
			# color
			self.oWhiteColor = QtGui.QCheckBox(translate('setTextures', '- set white color'), self)
			self.oWhiteColor.setCheckState(QtCore.Qt.Unchecked)

			# store attributes
			self.oStoreB = QtGui.QPushButton(translate('setTextures', 'set texture attributes'), self)
			self.oStoreB.clicked.connect(self.storeTextures)
			self.oStoreB.setFixedHeight(40)
			
			# ############################################################################
			# live preview
			# ############################################################################
			
			# you can change order here
			
			self.oPreviewTargetL = QtGui.QLabel(translate('setTextures', 'Live preview:'), self)
			
			self.previewTargetList = (
				translate('setTextures', 'repeat X axis'),
				translate('setTextures', 'repeat Y axis'),
				translate('setTextures', 'repeat Z axis'),
				translate('setTextures', 'rotation X axis'),
				translate('setTextures', 'rotation Y axis'),
				translate('setTextures', 'rotation Z axis') # no comma
			)
			self.oPreviewTarget = QtGui.QComboBox(self)
			self.oPreviewTarget.addItems(self.previewTargetList)
			self.oPreviewTarget.setCurrentIndex(5)
			self.oPreviewTarget.textActivated[str].connect(self.setPreviewTarget)
			
			# step
			self.oPreviewStepL = QtGui.QLabel(translate('setTextures', 'Step:'), self)

			self.oPreviewStepE = QtGui.QLineEdit(self)
			self.oPreviewStepE.setText("1")

			# adjust buttons
			self.oPreviewB1 = QtGui.QPushButton("-", self)
			self.oPreviewB1.clicked.connect(self.setPreview1)
			self.oPreviewB1.setAutoRepeat(True)
			
			self.oPreviewB2 = QtGui.QPushButton("+", self)
			self.oPreviewB2.clicked.connect(self.setPreview2)
			self.oPreviewB2.setAutoRepeat(True)

			# ############################################################################
			# load texture
			# ############################################################################
			
			# button
			self.oLoadB = QtGui.QPushButton(translate('setTextures', 'show textures'), self)
			self.oLoadB.clicked.connect(self.loadTextures)
			self.oLoadB.setFixedHeight(40)
			
			# ############################################################################
			# status
			# ############################################################################

			self.status = QtGui.QLabel("", self)
			
			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.layObjects = QtGui.QVBoxLayout()
			self.layObjects.addWidget(self.oObjectsI)
			self.layObjects.addWidget(self.oObjectsB)
			
			self.layFit = QtGui.QVBoxLayout()
			self.layFit.addWidget(self.oFit)
			self.layFit.addSpacing(20)
			self.layFit.addWidget(self.oURLInfo)
			
			self.layURL = QtGui.QHBoxLayout()
			self.layURL.addWidget(self.oURLPath)
			self.layURL.addWidget(self.oURLHDD)
			
			self.layGrid = QtGui.QGridLayout()
			self.layGrid.addWidget(self.oRepeatXL, 0, 0)
			self.layGrid.addWidget(self.oRepeatXE, 0, 1)
			self.layGrid.addWidget(self.oRepeatYL, 1, 0)
			self.layGrid.addWidget(self.oRepeatYE, 1, 1)
			self.layGrid.addWidget(self.oRepeatZL, 2, 0)
			self.layGrid.addWidget(self.oRepeatZE, 2, 1)
			self.layGrid.addWidget(self.oRotateAxisXL, 3, 0)
			self.layGrid.addWidget(self.oRotateAxisXE, 3, 1)
			self.layGrid.addWidget(self.oRotateAxisYL, 4, 0)
			self.layGrid.addWidget(self.oRotateAxisYE, 4, 1)
			self.layGrid.addWidget(self.oRotateAxisZL, 5, 0)
			self.layGrid.addWidget(self.oRotateAxisZE, 5, 1)
			self.layGrid.addWidget(self.oRotateAngleL, 6, 0)
			self.layGrid.addWidget(self.oRotateAngleE, 6, 1)
			
			self.layStoreB = QtGui.QVBoxLayout()
			self.layStoreB.addWidget(self.oStoreB)
			
			self.layStore = QtGui.QVBoxLayout()
			self.layStore.addLayout(self.layFit)
			self.layStore.addLayout(self.layURL)
			self.layStore.addLayout(self.layGrid)
			self.layStore.addLayout(self.layStoreB)
			self.groupAdjust = QtGui.QGroupBox(None, self)
			self.groupAdjust.setLayout(self.layStore)
			
			self.layGridPreview1 = QtGui.QGridLayout()
			self.layGridPreview1.addWidget(self.oPreviewTargetL, 0, 0)
			self.layGridPreview1.addWidget(self.oPreviewTarget, 0, 1)
			self.layGridPreview1.addWidget(self.oPreviewStepL, 1, 0)
			self.layGridPreview1.addWidget(self.oPreviewStepE, 1, 1)
			
			self.layGridPreview2 = QtGui.QHBoxLayout()
			self.layGridPreview2.addWidget(self.oPreviewB1)
			self.layGridPreview2.addWidget(self.oPreviewB2)
			
			self.layPreview = QtGui.QVBoxLayout()
			self.layPreview.addLayout(self.layGridPreview1)
			self.layPreview.addLayout(self.layGridPreview2)
			
			self.groupPreview = QtGui.QGroupBox(None, self)
			self.groupPreview.setLayout(self.layPreview)
			
			self.layLoad = QtGui.QVBoxLayout()
			self.layLoad.addWidget(self.oWhiteColor)
			self.layLoad.addWidget(self.oLoadB)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			
			self.layout.addLayout(self.layObjects)
			self.layout.addStretch()
			self.layout.addWidget(self.groupAdjust)
			self.layout.addStretch()
			self.layout.addWidget(self.groupPreview)
			self.layout.addStretch()
			self.layout.addLayout(self.layLoad)
			self.layout.addStretch()
			self.layout.addWidget(self.status)
			
			self.setLayout(self.layout)

			# ############################################################################
			# show all
			# ############################################################################

			self.show()
			
			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)
			
			# init
			self.getSelected()
			
		# ############################################################################
		# internal functions
		# ############################################################################
		
		# ############################################################################
		def resetGlobals(self):
			self.gBrokenURL = dict()
			self.oRepeatXE.setText("1")
			self.oRepeatYE.setText("1")
			self.oRepeatZE.setText("1")
			self.oRotateAxisXE.setText("0")
			self.oRotateAxisYE.setText("0")
			self.oRotateAxisZE.setText("1")
			self.oRotateAngleE.setText("0")
		
		# ############################################################################
		def showStatus(self, iText):
			self.status.setText(str(iText))

		# ############################################################################
		# actions
		# ############################################################################

		# ############################################################################
		def setTextureFit(self, selectedText):
			skip = 1

		# ############################################################################		
		def loadCustomFile(self):
			hdd = str(QtGui.QFileDialog.getOpenFileName()[0])
			self.oURLPath.setText(hdd)
		
		# ############################################################################
		def getSelected(self):
			
			try:
				if MagicPanels.gCurrentSelection == True:
					self.oObjectsB.setDisabled(True)
				else:
					self.oObjectsB.setDisabled(False)

				self.gObjects = FreeCADGui.Selection.getSelection()
				if len(self.gObjects) < 1:
					self.gObjects = FreeCAD.ActiveDocument.Objects
					self.oObjectsI.setText(self.infoAO)
				else:
					self.oObjectsI.setText(self.infoSO)

				self.resetGlobals()
				
				if len(self.gObjects) == 1:
					
					obj = self.gObjects[0]
					
					if hasattr(obj, "Texture_Repeat_X"):
						self.oRepeatXE.setText(str( obj.Texture_Repeat_X ))

					if hasattr(obj, "Texture_Repeat_Y"):
						self.oRepeatYE.setText(str( obj.Texture_Repeat_Y ))
					
					if hasattr(obj, "Texture_Repeat_Z"):
						self.oRepeatZE.setText(str( obj.Texture_Repeat_Z ))
						
					if hasattr(obj, "Texture_Rotation_Axis_X"):
						self.oRotateAxisXE.setText(str( round(obj.Texture_Rotation_Axis_X, 4) ))
					
					if hasattr(obj, "Texture_Rotation_Axis_Y"):
						self.oRotateAxisYE.setText(str( round(obj.Texture_Rotation_Axis_Y, 4) ))
						
					if hasattr(obj, "Texture_Rotation_Axis_Z"):
						self.oRotateAxisZE.setText(str( round(obj.Texture_Rotation_Axis_Z, 4) ))

					if hasattr(obj, "Texture_Rotation_Angle"):
						self.oRotateAngleE.setText(str( round(obj.Texture_Rotation_Angle, 4) ))
				
				FreeCADGui.Selection.clearSelection()
			except:
				self.oObjectsI.setText(self.infoAO)

		# ############################################################################
		# store texture attributes
		# ############################################################################
		
		# ############################################################################
		def storeTextures(self):

			# set flag
			skip = 0

			# get texture URL from GUI text form
			textureURL = self.oURLPath.text()

			# scan all given objects and set all properties
			for obj in self.gObjects:

				# skip everything except supported parts
				if (
					not obj.isDerivedFrom("Part::Box") and 
					not obj.isDerivedFrom("Part::Cylinder") and 
					not obj.isDerivedFrom("Part::Sphere") and 
					not obj.isDerivedFrom("PartDesign::Pad")
				):
					continue

				# set properties
				try:

					if not hasattr(obj, "Texture_Fit"):
						info = "Texture coordinate to fit object shape better."
						obj.addProperty("App::PropertyString", "Texture_Fit", "Texture", info)

					if not hasattr(obj, "Texture_URL"):
						info = "Texture URL or HDD local path."
						obj.addProperty("App::PropertyString", "Texture_URL", "Texture", info)

					if not hasattr(obj, "Texture_Repeat_X"):
						info = "How many times reapeat the texture to X direction. Float 1.0 is default value for no repeat."
						obj.addProperty("App::PropertyFloat", "Texture_Repeat_X", "Texture", info)

					if not hasattr(obj, "Texture_Repeat_Y"):
						info = "How many times reapeat the texture to Y direction. Float 1.0 is default value for no repeat."
						obj.addProperty("App::PropertyFloat", "Texture_Repeat_Y", "Texture", info)
					
					if not hasattr(obj, "Texture_Repeat_Z"):
						info = "How many times reapeat the texture to Z direction. Float 1.0 is default value for no repeat."
						obj.addProperty("App::PropertyFloat", "Texture_Repeat_Z", "Texture", info)
						
					if not hasattr(obj, "Texture_Rotation_Axis_X"):
						info = 'Texture rotation X axis value. Float 0 means not rotate around this axis. Float 1 means rotate.'
						obj.addProperty("App::PropertyFloat", "Texture_Rotation_Axis_X", "Texture", info)
					
					if not hasattr(obj, "Texture_Rotation_Axis_Y"):
						info = 'Texture rotation Y axis value. Float 0 means not rotate around this axis. Float 1 means rotate.'
						obj.addProperty("App::PropertyFloat", "Texture_Rotation_Axis_Y", "Texture", info)
						
					if not hasattr(obj, "Texture_Rotation_Axis_Z"):
						info = 'Texture rotation Z axis value. Float 0 means not rotate around this axis. Float 1 means rotate.'
						obj.addProperty("App::PropertyFloat", "Texture_Rotation_Axis_Z", "Texture", info)

					if not hasattr(obj, "Texture_Rotation_Angle"):
						info = "Texture rotation in degrees. Float 0 is default value for no rotation."
						obj.addProperty("App::PropertyFloat", "Texture_Rotation_Angle", "Texture", info)
					
					obj.Texture_Fit = str(self.oFit.currentText())
					
					if str(textureURL) != "":
						obj.Texture_URL = str(textureURL)
						
					if str(self.oRepeatXE.text()) != "":
						obj.Texture_Repeat_X = float(self.oRepeatXE.text())
					
					if str(self.oRepeatYE.text()) != "":
						obj.Texture_Repeat_Y = float(self.oRepeatYE.text())
					
					if str(self.oRepeatZE.text()) != "":
						obj.Texture_Repeat_Z = float(self.oRepeatZE.text())
					
					if str(self.oRotateAxisXE.text()) != "":
						obj.Texture_Rotation_Axis_X = float(self.oRotateAxisXE.text())
					
					if str(self.oRotateAxisYE.text()) != "":
						obj.Texture_Rotation_Axis_Y = float(self.oRotateAxisYE.text())
					
					if str(self.oRotateAxisZE.text()) != "":
						obj.Texture_Rotation_Axis_Z = float(self.oRotateAxisZE.text())
					
					if str(self.oRotateAngleE.text()) != "":
						obj.Texture_Rotation_Angle = float(self.oRotateAngleE.text())
				
				except:
					skip = 1

			FreeCAD.ActiveDocument.recompute()

			# show status
			if skip == 0:
				self.showStatus(translate('setTextures', 'Texture properties has been stored.'))
			else:
				self.showStatus(translate('setTextures', 'Error during setting properties.'))

		# ############################################################################
		# Preview
		# ############################################################################
		
		# ############################################################################
		def setPreviewTarget(self):
			skip = 1
		
		# ############################################################################		
		def updatePreview(self, iTarget, repeatX, repeatY, repeatZ, rotateX, rotateY, rotateZ, step):
			
			for o in self.gObjects:
				rootnode = o.ViewObject.RootNode
				for i in rootnode.getChildren():
					if str(i).find("SoTexture3Transform") != -1:
						if hasattr(i, "scaleFactor") and hasattr(i, "rotation"):
							
							# repeat
							if iTarget.startswith("repeat"):
								coinSFV = coin.SbVec3f(repeatX, repeatY, repeatZ)
								i.scaleFactor.setValue(coinSFV)
								
								# set new values to gui form
								self.oRepeatXE.setText(str(repeatX))
								self.oRepeatYE.setText(str(repeatY))
								self.oRepeatZE.setText(str(repeatZ))
								
							# rotation
							if iTarget.startswith("rotate"):
								[ q1, q2, q3, q4 ] = i.rotation.getValue().getValue()
								currentRotation = FreeCAD.Rotation(q1, q2, q3, q4)
								addRotation = FreeCAD.Rotation( FreeCAD.Vector(rotateX, rotateY, rotateZ), step)
								newRotation = addRotation * currentRotation
								
								axisX = newRotation.Axis.x
								axisY = newRotation.Axis.y
								axisZ = newRotation.Axis.z
								angle = newRotation.Angle
								axis = coin.SbVec3f(axisX, axisY, axisZ)
								setRotation = coin.SbRotation( axis, angle )
								i.rotation.setValue(setRotation)
								
								# set new values to gui form
								self.oRotateAxisXE.setText(str( round(axisX, 4) ))
								self.oRotateAxisYE.setText(str( round(axisY, 4) ))
								self.oRotateAxisZE.setText(str( round(axisZ, 4) ))
								self.oRotateAngleE.setText(str( round(math.degrees(angle), 4) ))

			FreeCAD.ActiveDocument.recompute()
	
		# ############################################################################		
		def setPreview1(self):
			
			target = getMenuIndexPreview[self.oPreviewTarget.currentText()]
			
			repeatX = float(self.oRepeatXE.text())
			repeatY = float(self.oRepeatYE.text())
			repeatZ = float(self.oRepeatZE.text())
			rotateX = 0
			rotateY = 0
			rotateZ = 0
			rotateAngle = float(self.oRotateAngleE.text())
			
			if target == "repeatX":
				repeatX = repeatX - float(self.oPreviewStepE.text())

			if target == "repeatY":
				repeatY = repeatY - float(self.oPreviewStepE.text())
	
			if target == "repeatZ":
				repeatZ = repeatZ - float(self.oPreviewStepE.text())
				
			if target == "rotateX":
				rotateX = 1
				rotateAngle = - float(self.oPreviewStepE.text())

			if target == "rotateY":
				rotateY = 1
				rotateAngle = - float(self.oPreviewStepE.text())

			if target == "rotateZ":
				rotateZ = 1
				rotateAngle = - float(self.oPreviewStepE.text())
				
			self.updatePreview(target, repeatX, repeatY, repeatZ, rotateX, rotateY, rotateZ, rotateAngle)
			
		# ############################################################################		
		def setPreview2(self):
			
			target = getMenuIndexPreview[self.oPreviewTarget.currentText()]
			
			repeatX = float(self.oRepeatXE.text())
			repeatY = float(self.oRepeatYE.text())
			repeatZ = float(self.oRepeatZE.text())
			rotateX = 0
			rotateY = 0
			rotateZ = 0
			rotateAngle = float(self.oRotateAngleE.text())
			
			if target == "repeatX":
				repeatX = repeatX + float(self.oPreviewStepE.text())

			if target == "repeatY":
				repeatY = repeatY + float(self.oPreviewStepE.text())
	
			if target == "repeatZ":
				repeatZ = repeatZ + float(self.oPreviewStepE.text())
				
			if target == "rotateX":
				rotateX = 1
				rotateAngle = float(self.oPreviewStepE.text())

			if target == "rotateY":
				rotateY = 1
				rotateAngle = float(self.oPreviewStepE.text())

			if target == "rotateZ":
				rotateZ = 1
				rotateAngle = float(self.oPreviewStepE.text())
				
			self.updatePreview(target, repeatX, repeatY, repeatZ, rotateX, rotateY, rotateZ, rotateAngle)
			
		# ############################################################################
		# load textures
		# ############################################################################
		
		# ############################################################################
		def getTextureURL(self, iObj):
			
			# support for texture URL stored at objects Texture_URL property
			try:
				textureURL = str(iObj.Texture_URL)
				if textureURL != "":
					return textureURL
			except:
				skip = 1

			# support for texture URL stored at objects description
			try:
				textureURL = str(iObj.Label2)
				if textureURL != "":
					return textureURL
			except:
				skip = 1

			# backward compatibility and support for manually added to Texture property
			try:
				textureURL = str(iObj.Texture)
				if textureURL != "":
					return textureURL
			except:
				skip = 1

			# support for texture URL stored at Material Card TexturePath
			try:
				textureURL = str(iObj.Material.Material["TexturePath"])
				if textureURL != "":
					return textureURL
			except:
				skip = 1
			
			# support for texture URL stored at Material properties
			try:
				if iObj.ShapeMaterial.Name != "Default":
					return "ShapeMaterial"
			except:
				skip = 1
			
			# no texture URL set
			return ""
			
		# ############################################################################
		def downloadTexture(self, iObj, iURL):
			
			import urllib.request
			import tempfile
			import os
			
			# create temp directory
			tmpDir = tempfile.gettempdir()
			tmpDir = os.path.join(tmpDir, "FreeCAD_Textures")
			if not os.path.exists(tmpDir):
				os.makedirs(tmpDir)

			# get texture filename
			if iURL == "ShapeMaterial":
				textureFilename = str(iObj.Name) + "_" + str(iObj.ShapeMaterial.Name)
			else:
				textureFilename = os.path.basename(iURL)
			
			textureFilePath = os.path.join(tmpDir, textureFilename)

			# check if file already exists and skip slow downloading
			if not os.path.exists(textureFilePath):

				# get image from URL
				try:
					if iURL == "ShapeMaterial":
						import base64
						img = iObj.ShapeMaterial.getAppearanceValue("TextureImage")
						img = img.encode('utf-8')
						data = base64.b64decode(img)
					else:
						data = urllib.request.urlopen(iURL).read()
				except:
					self.gBrokenURL[str(iObj.Label)] = iURL
					return ""
				
				# create temp file with image
				out = open(str(textureFilePath), "wb")
				out.write(data)
				out.close()

			return textureFilePath

		# ############################################################################
		def setTexture(self, iObj, iFile):
		
			# init with default to allow texture loading without attributes
			repeatX = 1
			repeatY = 1
			repeatZ = 1
			axisX = 0
			axisY = 0
			axisZ = 1
			angle = 0
		
			# ovewrite if there are attributes
			if hasattr(iObj, "Texture_Repeat_X"):
				repeatX = float(iObj.Texture_Repeat_X)
			
			if hasattr(iObj, "Texture_Repeat_Y"):
				repeatY = float(iObj.Texture_Repeat_Y)
			
			if hasattr(iObj, "Texture_Repeat_Z"):
				repeatZ = float(iObj.Texture_Repeat_Z)
				
			if hasattr(iObj, "Texture_Rotation_Axis_X"):
				axisX = float(iObj.Texture_Rotation_Axis_X)
			
			if hasattr(iObj, "Texture_Rotation_Axis_Y"):
				axisY = float(iObj.Texture_Rotation_Axis_Y)
				
			if hasattr(iObj, "Texture_Rotation_Axis_Z"):
				axisZ = float(iObj.Texture_Rotation_Axis_Z)
			
			if hasattr(iObj, "Texture_Rotation_Angle"):
				angle = math.radians(float(iObj.Texture_Rotation_Angle))
					
			# set node
			rootnode = iObj.ViewObject.RootNode
			
			# try update existing node
			updateST2 = False
			updateST3T = False
			try:
				for i in rootnode.getChildren():
					
					if str(i).find("SoTexture2") != -1:
						
						if hasattr(i, "filename"):
							i.filename = iFile
							updateST2 = True
					
					if str(i).find("SoTexture3Transform") != -1:
						
						if hasattr(i, "scaleFactor") and hasattr(i, "rotation"):
							
							# repeat
							coinSFV = coin.SbVec3f(repeatX, repeatY, repeatZ)
							i.scaleFactor.setValue(coinSFV)
							
							# rotation
							axis = coin.SbVec3f(axisX, axisY, axisZ)
							coinRotation = coin.SbRotation( axis, angle )
							i.rotation.setValue(coinRotation)
							updateST3T = True
			except:
				updateST2 = False
				updateST3T = False
			
			# add new if there is no transformation child
			if updateST3T == False:

				trans = coin.SoTexture3Transform()
				
				# repeat
				coinSFV = coin.SbVec3f(repeatX, repeatY, repeatZ)
				trans.scaleFactor.setValue(coinSFV)
				
				# rotation
				axis = coin.SbVec3f(axisX, axisY, axisZ)
				coinRotation = coin.SbRotation( axis, angle )
				trans.rotation.setValue(coinRotation)
						
				rootnode.insertChild(trans, 1)
			
			if updateST2 == False:
				
				# set texture with URL
				texture =  coin.SoTexture2()
				texture.filename = iFile
				rootnode.insertChild(texture, 2)

			# reset gui values
			self.oRepeatXE.setText("1")
			self.oRepeatYE.setText("1")
			self.oRepeatZE.setText("1")
			self.oRotateAxisXE.setText("0")
			self.oRotateAxisYE.setText("0")
			self.oRotateAxisZE.setText("1")
			self.oRotateAngleE.setText("0")

		# ############################################################################
		def getChildPosition(self, iRootnode):
			
			pos = 0
			for c in iRootnode.getChildren():
				if str(c).find("SoSwitch") != -1:
					return pos
					break

				pos = pos + 1

			return -1

		# ############################################################################
		def fitTexture(self, iObj):
		
			rootnode = iObj.ViewObject.RootNode
		
			if hasattr(iObj, "Texture_Fit"):
				if isinstance(iObj.Texture_Fit, str):
					cr = getMenuIndexFit[iObj.Texture_Fit]
					
					coordinate = ""
					
					if cr == "biggest":
						coordinate = coin.SoTextureCoordinateDefault()
					
					if cr == "cube":
						coordinate = coin.SoTextureCoordinateCube()

					if cr == "cylinder":
						coordinate = coin.SoTextureCoordinateCylinder()
					
					if cr == "sphere":
						coordinate = coin.SoTextureCoordinateSphere()
					
					if cr == "glass":
						coordinate = coin.SoTextureCoordinateEnvironment()
					
					if cr == "auto":
						
						coordinate = coin.SoTextureCoordinateDefault()
						
						if iObj.isDerivedFrom("Part::Box"):
							coordinate = coin.SoTextureCoordinateCube()
			
						if iObj.isDerivedFrom("Part::Cylinder"):
							coordinate = coin.SoTextureCoordinateCylinder()
						
						if iObj.isDerivedFrom("Part::Sphere"):
							coordinate = coin.SoTextureCoordinateSphere()

					# add fit texture
					pos = self.getChildPosition(rootnode)
					rootnode.insertChild(coordinate, pos)
					
		# ############################################################################
		def loadTextures(self):

			self.gBrokenURL = dict()
			empty = ""
			
			# search all objects and set URL
			for obj in self.gObjects:
				
				# try set color
				if self.oWhiteColor.isChecked():
					MagicPanels.setColor(obj, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
				textureURL = self.getTextureURL(obj)
				
				# if no texture found for object skip it
				if str(textureURL) == "":
					continue
				else:
					empty = "no"

				# chose URL or local HDD
				if textureURL.startswith("http") or textureURL == "ShapeMaterial":
					filename = self.downloadTexture(obj, textureURL)
				else:
					filename = str(textureURL)
				
				# should be no empty
				if str(filename) == "":
					continue

				# set texture
				self.setTexture(obj, filename)
				self.fitTexture(obj)

			# set status
			if empty == "":
				
				iText = translate('setTextures', 'No textures URLs found.')
				self.showStatus(iText)
			
			else:
			
				if len(self.gBrokenURL) == 0:
					
					self.showStatus(translate('setTextures', 'All textures has been loaded.'))
				
				else:
					
					FreeCAD.Console.PrintMessage("\n ====================== \n")
					for n, b in self.gBrokenURL.items():
						FreeCAD.Console.PrintMessage("\n")
						FreeCAD.Console.PrintMessage(translate('setTextures', 'Object Label') + ': '+n)
						FreeCAD.Console.PrintMessage("\n")
						FreeCAD.Console.PrintMessage(translate('setTextures', 'Broken URL') + ': '+b)
						FreeCAD.Console.PrintMessage("\n")
					FreeCAD.Console.PrintMessage("\n ====================== \n")

					info = ""
					info += translate('setTextures', 'See console for broken URLs.')
					self.showStatus(info)

	# ############################################################################
	# final settings, if needed
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		pass
	
	if form.result == userOK:
		pass


# ###################################################################################################################
# Main
# ###################################################################################################################


showQtMain()


# ###################################################################################################################
