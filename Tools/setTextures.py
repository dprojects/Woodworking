import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore
from pivy import coin
import math, os

import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# Global definitions
# ############################################################################

# add new items only at the end and change self.selectionList
getMenuIndexSelection = {
	translate('setTextures', 'selected objects')   : "selected",
	translate('setTextures', 'all objects')        : "all" # no comma 
}

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
		gObjectsSelected = []
		
		gBrokenURL = dict()
		gFolderTextures = []
		
		infoStart = translate('setTextures', 'please select valid objects and refresh')
		
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
			toolSW = 334
			toolSH = 710
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('setTextures', 'setTextures'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			self.setMinimumSize(toolSW, toolSH)
			
			# ############################################################################
			# objects
			# ############################################################################

			# screen
			self.oObjectsI = QtGui.QLabel(self.infoStart, self)
			
			# selection
			self.selectionList = (
				translate('setTextures', 'selected objects'),
				translate('setTextures', 'all objects') # no comma 
	
			)
			self.oSelection = QtGui.QComboBox(self)
			self.oSelection.addItems(self.selectionList)
			self.oSelection.setCurrentIndex(0)
			self.oSelection.textActivated[str].connect(self.setSelection)
			
			# button
			self.oObjectsB = QtGui.QPushButton(translate('setTextures', 'refresh selection'), self)
			self.oObjectsB.clicked.connect(self.getSelected)

			# ############################################################################
			# load texture & live preview
			# ############################################################################
			
			# color
			self.oWhiteColor = QtGui.QCheckBox(translate('setTextures', '- set white color'), self)
			self.oWhiteColor.setCheckState(QtCore.Qt.Unchecked)

			# button
			self.oLoadB = QtGui.QPushButton(translate('setTextures', 'load saved'), self)
			self.oLoadB.clicked.connect(self.loadTextures)

			self.oPathURL = QtGui.QPushButton(translate('setTextures', 'load from URL'), self)
			self.oPathURL.clicked.connect(self.loadURLPath)
			
			self.oPathLocal = QtGui.QPushButton(translate('setTextures', 'load from local'), self)
			self.oPathLocal.clicked.connect(self.loadLocalPath)

			# URL
			self.oPathE = QtGui.QLineEdit(self)
			self.oPathE.setPlaceholderText(translate('setTextures', 'set URL or full path to local file'))
			self.oPathE.setText("")

			# browse directory
			self.oBrowseB1 = QtGui.QPushButton("< local file", self)
			self.oBrowseB1.clicked.connect(self.browseP)
			self.oBrowseB1.setAutoRepeat(True)
			
			self.oBrowseB2 = QtGui.QPushButton("local file >", self)
			self.oBrowseB2.clicked.connect(self.browseN)
			self.oBrowseB2.setAutoRepeat(True)

			self.oPreviewTargetL = QtGui.QLabel(translate('setTextures', 'Live preview target:'), self)
			
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
			
			# button
			self.oLoadCustom = QtGui.QPushButton(translate('setTextures', 'preview custom attributes'), self)
			self.oLoadCustom.clicked.connect(self.previewTexture)

			# ############################################################################
			# save texture
			# ############################################################################
			
			# store attributes
			self.oStoreB = QtGui.QPushButton(translate('setTextures', 'save texture'), self)
			self.oStoreB.clicked.connect(self.storeTextures)
			self.oStoreB.setFixedHeight(40)
			
			# ############################################################################
			# status
			# ############################################################################

			self.status = QtGui.QLabel("", self)
			
			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# objects
			self.layObjects = QtGui.QVBoxLayout()
			self.layObjects.addWidget(self.oObjectsI)
			
			self.laySelection = QtGui.QGridLayout()
			self.laySelection.addWidget(self.oSelection, 0, 0)
			self.laySelection.addWidget(self.oObjectsB, 0, 1)

			# preview
			self.layLoad = QtGui.QGridLayout()
			self.layLoad.addWidget(self.oWhiteColor, 0, 0)
			self.layLoad.addWidget(self.oLoadB, 0, 1)
			self.layLoad.addWidget(self.oPathURL, 1, 0)
			self.layLoad.addWidget(self.oPathLocal, 1, 1)
			
			self.layURL = QtGui.QVBoxLayout()
			self.layURL.addWidget(self.oPathE)

			self.layBrowse = QtGui.QGridLayout()
			self.layBrowse.addWidget(self.oBrowseB1, 0, 0)
			self.layBrowse.addWidget(self.oBrowseB2, 0, 1)

			self.layGridPreview1 = QtGui.QGridLayout()
			self.layGridPreview1.addWidget(self.oPreviewTargetL, 0, 0)
			self.layGridPreview1.addWidget(self.oPreviewTarget, 0, 1)
			self.layGridPreview1.addWidget(self.oPreviewStepL, 1, 0)
			self.layGridPreview1.addWidget(self.oPreviewStepE, 1, 1)
			
			self.layGridPreview2 = QtGui.QHBoxLayout()
			self.layGridPreview2.addWidget(self.oPreviewB1)
			self.layGridPreview2.addWidget(self.oPreviewB2)
			
			self.layPreview = QtGui.QVBoxLayout()
			self.layPreview.addLayout(self.layLoad)
			self.layPreview.addLayout(self.layURL)
			self.layPreview.addLayout(self.layBrowse)
			self.layPreview.addSpacing(20)
			self.layPreview.addLayout(self.layGridPreview1)
			self.layPreview.addLayout(self.layGridPreview2)
			
			self.groupPreview = QtGui.QGroupBox(None, self)
			self.groupPreview.setLayout(self.layPreview)

			# attributes
			self.layFit = QtGui.QVBoxLayout()
			self.layFit.addWidget(self.oFit)
			
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
			
			self.layAttributes = QtGui.QVBoxLayout()
			self.layAttributes.addLayout(self.layFit)
			self.layAttributes.addLayout(self.layGrid)
			self.layAttributes.addWidget(self.oLoadCustom)
			self.groupAttributes = QtGui.QGroupBox(None, self)
			self.groupAttributes.setLayout(self.layAttributes)
			
			# save
			self.laySaveTexture = QtGui.QVBoxLayout()
			self.laySaveTexture.addWidget(self.oStoreB)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			
			self.layout.addLayout(self.layObjects)
			self.layout.addLayout(self.laySelection)
			self.layout.addStretch()
			self.layout.addWidget(self.groupPreview)
			self.layout.addStretch()
			self.layout.addWidget(self.groupAttributes)
			self.layout.addStretch()
			self.layout.addWidget(self.status)
			self.layout.addStretch()
			self.layout.addLayout(self.laySaveTexture)
			
			self.setLayout(self.layout)

			# ############################################################################
			# show all
			# ############################################################################

			# set theme
			MagicPanels.setTheme(self)
			
			self.show()
			
			MagicPanels.adjustGUI(self, "right")
			
			# init
			self.getSelected()
			
		# ############################################################################
		# internal functions
		# ############################################################################
		
		# ############################################################################
		def resetGlobals(self):
			self.gObjects = []
			self.gObjectsSelected = []
			self.gBrokenURL = dict()
			self.oRepeatXE.setText("1")
			self.oRepeatYE.setText("1")
			self.oRepeatZE.setText("1")
			self.oRotateAxisXE.setText("0")
			self.oRotateAxisYE.setText("0")
			self.oRotateAxisZE.setText("1")
			self.oRotateAngleE.setText("0")
			self.oObjectsI.setText(self.infoStart)
		
		# ############################################################################
		def setObjects(self):
			
			selection = FreeCADGui.Selection.getSelection()
			if len(selection) < 1:
				self.resetGlobals()

			elif len(selection) == 1:
				self.gObjects = FreeCADGui.Selection.getSelection()
				self.oObjectsI.setText( str(self.gObjects[0].Label) )

			else:
				self.gObjects = FreeCADGui.Selection.getSelection()
				info = translate('setTextures', 'Multi, ') + str(self.gObjects[0].Label)
				self.oObjectsI.setText(info)

		# ############################################################################
		def getObjectAttributes(self, iObj):
		
			[ fit, repeatX, repeatY, repeatZ, axisX, axisY, axisZ, angle ] = [ "", 1, 1, 1, 0, 0, 1, 0 ]
			
			if hasattr(iObj, "Texture_Fit"):
				fit = str(iObj.Texture_Fit)
			
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
			elif hasattr(iObj, "Texture_Rotation"):
				angle = float(iObj.Texture_Rotation)
			else:
				skip = 1

			return [ fit, repeatX, repeatY, repeatZ, axisX, axisY, axisZ, angle ]

		# ############################################################################
		def updateGUIAttributes(self, iFit="", iRepeatX=1, iRepeatY=1, iRepeatZ=1, 
						iAxisX=0, iAxisY=0, iAxisZ=1, iAngle=0):
		
			if iFit != "":
				self.oFit.setCurrentText( str(iFit) )
			
			self.oRepeatXE.setText( str(iRepeatX) )
			self.oRepeatYE.setText( str(iRepeatY) )
			self.oRepeatZE.setText( str(iRepeatZ) )
			self.oRotateAxisXE.setText( str(iAxisX) )
			self.oRotateAxisYE.setText( str(iAxisY) )
			self.oRotateAxisZE.setText( str(iAxisZ) )
			self.oRotateAngleE.setText( str( math.degrees(iAngle) ) )

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
		def printBroken(self):

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
		def showStatus(self, iText):
			self.status.setText(str(iText))

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
		def fitTexture(self, iObj, iType="object"):
		
			rootnode = iObj.ViewObject.RootNode
			
			fit = ""
			if iType == "object":
				if hasattr(iObj, "Texture_Fit"):
					if isinstance(iObj.Texture_Fit, str):
						try:
							fit = getMenuIndexFit[iObj.Texture_Fit]
						except:
							skip = 1
			
			if iType == "chooser":
				try:
					fit = getMenuIndexFit[str(self.oFit.currentText())]
				except:
					skip = 1
			
			if fit == "":
				return
				
			# set coin fit mode
			coordinate = ""
			
			if fit == "biggest":
				coordinate = coin.SoTextureCoordinateDefault()
			
			if fit == "cube":
				coordinate = coin.SoTextureCoordinateCube()

			if fit == "cylinder":
				coordinate = coin.SoTextureCoordinateCylinder()
			
			if fit == "sphere":
				coordinate = coin.SoTextureCoordinateSphere()
			
			if fit == "glass":
				coordinate = coin.SoTextureCoordinateEnvironment()
			
			if fit == "auto":
				
				coordinate = coin.SoTextureCoordinateDefault()
				
				if iObj.isDerivedFrom("Part::Box"):
					coordinate = coin.SoTextureCoordinateCube()
	
				if iObj.isDerivedFrom("Part::Cylinder"):
					coordinate = coin.SoTextureCoordinateCylinder()
				
				if iObj.isDerivedFrom("Part::Sphere"):
					coordinate = coin.SoTextureCoordinateSphere()


			# add fit texture
			if str(coordinate) != "":
				pos = self.getChildPosition(rootnode)
				rootnode.insertChild(coordinate, pos)

		# ############################################################################
		def showTexture(self, iObjects=[], iType="", iFilename="", 
						iRepeatX=1, iRepeatY=1, iRepeatZ=1, iAxisX=0, iAxisY=0, iAxisZ=1, iAngle=0):
			
			for o in iObjects:
				rootnode = o.ViewObject.RootNode
				
				# try update existing node
				updateST2 = False
				updateST3T1 = False
				updateST3T2 = False
				
				try:
					for i in rootnode.getChildren():
						
						# existing filename
						if iFilename != "":
							if str(i).find("SoTexture2") != -1:
								if hasattr(i, "filename"):
									i.filename = iFilename
									updateST2 = True

						if str(i).find("SoTexture3Transform") != -1:
							
							# existing repeat
							if hasattr(i, "scaleFactor"):
								coinSFV = coin.SbVec3f(iRepeatX, iRepeatY, iRepeatZ)
								i.scaleFactor.setValue(coinSFV)
								updateST3T1 = True

							# existing rotate
							if hasattr(i, "rotation"):
								axis = coin.SbVec3f(iAxisX, iAxisY, iAxisZ)
								setRotation = coin.SbRotation( axis, iAngle )
								i.rotation.setValue(setRotation)
								updateST3T2 = True

				except:
					updateST2 = False
					updateST3T1 = False
					updateST3T2 = False
			
				# new repeat
				if updateST3T1 == False:
					trans = coin.SoTexture3Transform()
					coinSFV = coin.SbVec3f(iRepeatX, iRepeatY, iRepeatZ)
					trans.scaleFactor.setValue(coinSFV)
				
				# new rotation
				if updateST3T2 == False:
					trans = coin.SoTexture3Transform()
					axis = coin.SbVec3f(iAxisX, iAxisY, iAxisZ)
					coinRotation = coin.SbRotation( axis, iAngle )
					trans.rotation.setValue(coinRotation)
							
					rootnode.insertChild(trans, 1)
				
				# new filename
				if updateST2 == False and iFilename != "":
					texture =  coin.SoTexture2()
					texture.filename = iFilename
					rootnode.insertChild(texture, 2)
				
				# fit texture
				if iType == "saved":
					self.fitTexture(o, "object")
				
				if iType == "url" or iType == "local" or iType == "preview":
					self.fitTexture(o, "chooser")
					
				# set color
				if self.oWhiteColor.isChecked():
					MagicPanels.setColor(o, 0, (1.0, 1.0, 1.0, 1.0), "color")

			FreeCAD.ActiveDocument.recompute()

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
		# actions - button press
		# ############################################################################

		# ############################################################################
		def setSelection(self, selectedText):
			
			index = getMenuIndexSelection[selectedText]
			
			if index == "selected":
				self.gObjects = self.gObjectsSelected
				self.oObjectsB.setDisabled(False)
				
				if len(self.gObjects) < 1:
					self.oObjectsI.setText(self.infoStart)
				
				elif len(self.gObjects) == 1:
					self.oObjectsI.setText( str(self.gObjects[0].Label) )

				else:
					info = translate('setTextures', 'Multi, ') + str(self.gObjects[0].Label)
					self.oObjectsI.setText(info)

			if index == "all":
				self.gObjects = FreeCAD.ActiveDocument.Objects
				self.oObjectsB.setDisabled(True)
				
				info = translate('setTextures', 'ALL OBJECTS, ') + str(self.gObjects[0].Label)
				self.oObjectsI.setText(info)

		# ############################################################################
		def getSelected(self):
			
			try:
				FreeCAD.ActiveDocument.recompute() # for clean ActiveDocument state
				self.resetGlobals()
			
				if MagicPanels.gCurrentSelection == True:
					self.oObjectsB.setDisabled(True)
					self.oSelection.setDisabled(True)
				else:
					self.oObjectsB.setDisabled(False)
					self.oSelection.setDisabled(False)

				self.setObjects()
				self.gObjectsSelected = self.gObjects
				
				if len(self.gObjects) == 1:
					
					obj = self.gObjects[0]

					if hasattr(obj, "Texture_Fit"):
						self.oFit.setCurrentText(str(obj.Texture_Fit))

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
					elif hasattr(obj, "Texture_Rotation"):
						degree = math.degrees(obj.Texture_Rotation) 
						self.oRotateAngleE.setText(str( round(degree, 4) ))
					else:
						skip = 1

				FreeCADGui.Selection.clearSelection()
			
			except:
				self.oObjectsI.setText(self.infoStart)
				error = translate('setTextures', 'setTextures: Error during refresh selection. Probably invalid object.')
				FreeCAD.Console.PrintMessage(error)

		# ############################################################################
		def loadTextures(self):

			if MagicPanels.gCurrentSelection == True:
				self.setObjects()

			self.gBrokenURL = dict()
			empty = ""
			
			# search all objects and set URL
			for o in self.gObjects:
			
				# if no texture found for object skip it
				textureURL = self.getTextureURL(o)
				if str(textureURL) == "":
					continue
				else:
					empty = "no"

				# chose URL or local HDD
				if textureURL.startswith("http") or textureURL == "ShapeMaterial":
					filename = self.downloadTexture(o, textureURL)
				else:
					filename = str(textureURL)
				
				# should be no empty
				if str(filename) == "":
					continue

				# set texture
				[ fit, repeatX, repeatY, repeatZ, axisX, axisY, axisZ, angle ] = self.getObjectAttributes(o)
				self.showTexture([ o ], "saved", filename, repeatX, repeatY, repeatZ, axisX, axisY, axisZ, angle)
				self.updateGUIAttributes(fit, repeatX, repeatY, repeatZ, axisX, axisY, axisZ, angle)

			# set status
			if empty == "":
				iText = translate('setTextures', 'No textures URLs found.')
				self.showStatus(iText)
			
			else:
				if len(self.gBrokenURL) == 0:
					self.showStatus(translate('setTextures', 'All textures has been loaded.'))
				else:
					self.printBroken()
			
		# ############################################################################		
		def loadURLPath(self):

			url = str(self.oPathE.text())
			filename = self.downloadTexture(self.gObjects[0], url)
			if filename == "":
				self.printBroken()
			else:
				self.showTexture(iObjects=self.gObjects, iType="url", iFilename=filename)
	
		# ############################################################################		
		def loadLocalPath(self):
			
			filename = str(QtGui.QFileDialog.getOpenFileName()[0])
			self.oPathE.setText(filename)
			
			dirname = os.path.dirname(filename)
			self.gFolderTextures = os.listdir(dirname)
			self.gFolderTextures.sort()

			self.showTexture(iObjects=self.gObjects, iType="local", iFilename=filename)
	
		# ############################################################################
		def browseP(self):
			
			try:
				filename = str(self.oPathE.text())
				basename = os.path.basename(filename)

				index = self.gFolderTextures.index(basename)
				if index > 0:
					filename = filename.replace(basename, self.gFolderTextures[index-1])
					self.oPathE.setText(filename)
					self.showTexture(iObjects=self.gObjects, iType="local", iFilename=filename)
			except:
				skip = 1
			
		# ############################################################################
		def browseN(self):
			
			#try:
			filename = str(self.oPathE.text())
			basename = os.path.basename(filename)
		
			index = self.gFolderTextures.index(basename)
			if index < len(self.gFolderTextures)-1:
				filename = filename.replace(basename, self.gFolderTextures[index+1])
				self.oPathE.setText(filename)
				self.showTexture(iObjects=self.gObjects, iType="local", iFilename=filename)
			#except:
				#skip = 1

		# ############################################################################
		def setPreviewTarget(self):
			skip = 1

		# ############################################################################		
		def setPreview1(self):
			
			if MagicPanels.gCurrentSelection == True:
				self.setObjects()
			
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
			
			if MagicPanels.gCurrentSelection == True:
				self.setObjects()

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
		def setTextureFit(self, selectedText):
			skip = 1

		# ############################################################################		
		def previewTexture(self):
			
			repeatX = float(self.oRepeatXE.text())
			repeatY = float(self.oRepeatYE.text())
			repeatZ = float(self.oRepeatZE.text())
			axisX = float(self.oRotateAxisXE.text())
			axisY = float(self.oRotateAxisYE.text())
			axisZ = float(self.oRotateAxisZE.text())
			angle = math.radians( float(self.oRotateAngleE.text()) )
			
			self.showTexture(self.gObjects, "preview", "", repeatX, repeatY, repeatZ, axisX, axisY, axisZ, angle)

		# ############################################################################
		def storeTextures(self):

			if MagicPanels.gCurrentSelection == True:
				self.setObjects()

			# set flag
			skip = 0

			# get texture URL from GUI text form
			textureURL = self.oPathE.text()

			# scan all given objects and set all properties
			for obj in self.gObjects:

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
					error = translate('setTextures', 'setTextures: Skipped object: ') + str(obj.Label)
					FreeCAD.Console.PrintMessage(error)

			FreeCAD.ActiveDocument.recompute()

			# show status
			if skip == 0:
				self.showStatus(translate('setTextures', 'Texture properties has been stored.'))
			else:
				self.showStatus(translate('setTextures', 'Error during setting properties.'))

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
