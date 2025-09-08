import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore
from pivy import coin

import MagicPanels

translate = FreeCAD.Qt.translate


# ###################################################################################################################
# Qt GUI
# ###################################################################################################################


def showQtMain():

	class QtMainClass(QtGui.QDialog):

		# ############################################################################
		# globals
		# ############################################################################

		gFit = ""
		gBrokenURL = dict()

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
			toolSH = 550
			
			# active screen size - FreeCAD main window
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
			self.setWindowTitle(translate('setTextures', 'setTextures'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# header
			# ############################################################################

			# button
			self.initBA = QtGui.QPushButton(translate('setTextures', 'show stored textures for all objects'), self)
			self.initBA.clicked.connect(self.loadAll)
			self.initBA.setFixedHeight(40)
			
			# ############################################################################
			# body - settings
			# ############################################################################

			# fit mode
			self.fitList = (
				"biggest surface",
				"fit to Cube",
				"fit to Cylinder",
				"fit to Sphere",
				"auto fit",
				"glass mirror effect"
			)
			self.gFit = "biggest surface"
			
			self.fitO = QtGui.QComboBox(self)
			self.fitO.addItems(self.fitList)
			self.fitO.setCurrentIndex(self.fitList.index(self.gFit))
			self.fitO.textActivated[str].connect(self.setCoordinate)
			
			# color
			self.checkColor = QtGui.QCheckBox(translate('setTextures', '- set white color'), self)
			self.checkColor.setCheckState(QtCore.Qt.Checked)
			
			# URL
			self.urlL = QtGui.QLabel(translate('setTextures', 'Texture URL or local HDD path:'), self)
			
			# text input
			self.urlO = QtGui.QLineEdit(self)
			self.urlO.setText("")
			
			self.urlHDD = QtGui.QPushButton("...", self)
			self.urlHDD.clicked.connect(self.loadCustomFile)
			
			# repeat
			self.repeatXO = QtGui.QLineEdit(self)
			self.repeatXO.setText("1.0")
			self.repeatXO.setFixedWidth(50)
			
			self.repeatXL = QtGui.QLabel(translate('setTextures', '- repeat X, set 1 to not repeat'), self)
			
			self.repeatYO = QtGui.QLineEdit(self)
			self.repeatYO.setText("1.0")
			self.repeatYO.setFixedWidth(50)
			
			self.repeatYL = QtGui.QLabel(translate('setTextures', '- repeat Y, set 1 to not repeat'), self)
			
			# rotation
			self.rotateO = QtGui.QLineEdit(self)
			self.rotateO.setText("0.0")
			self.rotateO.setFixedWidth(50)
			
			self.rotateL = QtGui.QLabel(translate('setTextures', '- rotation, set 0 to not rotate'), self)
			
			# ############################################################################
			# body - store & load buttons
			# ############################################################################

			self.storeBS = QtGui.QPushButton(translate('setTextures', 'selected only'), self)
			self.storeBS.clicked.connect(self.storeSelected)
			self.storeBS.setFixedHeight(40)
			
			self.storeBA = QtGui.QPushButton(translate('setTextures', 'all objects'), self)
			self.storeBA.clicked.connect(self.storeAll)
			self.storeBA.setFixedHeight(40)
			
			self.loadBS = QtGui.QPushButton(translate('setTextures', 'selected only'), self)
			self.loadBS.clicked.connect(self.loadSelected)
			self.loadBS.setFixedHeight(40)
			
			self.loadBA = QtGui.QPushButton(translate('setTextures', 'all objects'), self)
			self.loadBA.clicked.connect(self.loadAll)
			self.loadBA.setFixedHeight(40)
			
			# ############################################################################
			# status
			# ############################################################################

			self.status = QtGui.QLabel("", self)
			
			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.head = QtGui.QHBoxLayout()
			self.head.addWidget(self.initBA)
			
			self.row1 = QtGui.QVBoxLayout()
			self.row1.addWidget(self.fitO)
			self.row1.addSpacing(20)
			self.row1.addWidget(self.urlL)
			
			self.row2 = QtGui.QHBoxLayout()
			self.row2.addWidget(self.urlO)
			self.row2.addWidget(self.urlHDD)
			
			self.row3 = QtGui.QGridLayout()
			self.row3.addWidget(self.repeatXO, 0, 0)
			self.row3.addWidget(self.repeatXL, 0, 1)
			self.row3.addWidget(self.repeatYO, 1, 0)
			self.row3.addWidget(self.repeatYL, 1, 1)
			self.row3.addWidget(self.rotateO, 2, 0)
			self.row3.addWidget(self.rotateL, 2, 1)
			
			self.row4 = QtGui.QVBoxLayout()
			self.row4.addSpacing(20)
			self.row4.addWidget(self.checkColor)
			
			self.layBody1 = QtGui.QVBoxLayout()
			self.layBody1.addLayout(self.row1)
			self.layBody1.addLayout(self.row2)
			self.layBody1.addLayout(self.row3)
			self.layBody1.addLayout(self.row4)
			self.groupBody1 = QtGui.QGroupBox(None, self)
			self.groupBody1.setLayout(self.layBody1)
			
			self.rowB1 = QtGui.QHBoxLayout()
			self.rowB1.addWidget(self.storeBS)
			self.rowB1.addWidget(self.storeBA)
			self.groupBodyB1 = QtGui.QGroupBox(translate('setTextures', 'Store texture properties for:'), self)
			self.groupBodyB1.setLayout(self.rowB1)
			
			self.rowB2 = QtGui.QHBoxLayout()
			self.rowB2.addWidget(self.loadBS)
			self.rowB2.addWidget(self.loadBA)
			self.groupBodyB2 = QtGui.QGroupBox(translate('setTextures', 'Refresh texture for:'), self)
			self.groupBodyB2.setLayout(self.rowB2)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			
			self.layout.addLayout(self.head)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody1)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBodyB1)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBodyB2)
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
			
		# ############################################################################
		# actions - status
		# ############################################################################
		
		def showStatus(self, iText):
			self.status.setText(str(iText))

		# ############################################################################
		# actions - store
		# ############################################################################
		
		def loadCustomFile(self):
			hdd = str(QtGui.QFileDialog.getOpenFileName()[0])
			self.urlO.setText(hdd)
		
		def storeTextures(self, iSearch, iSelect):

			# set flag
			skip = 0

			# get texture URL from GUI text form
			textureURL = self.urlO.text()

			# scan all given objects and set all properties
			for obj in iSearch:

				# skip everything except supported parts
				if (
					iSelect != "selected" and 
					not obj.isDerivedFrom("Part::Box") and 
					not obj.isDerivedFrom("Part::Cylinder") and 
					not obj.isDerivedFrom("Part::Sphere") and 
					not obj.isDerivedFrom("PartDesign::Pad")
				):
					continue

				# set properties
				try:

					if not hasattr(obj, "Texture_URL"):
						info = "Texture URL or HDD local path."
						obj.addProperty("App::PropertyString", "Texture_URL", "Texture", info)

					if not hasattr(obj, "Texture_Repeat_X"):
						info = "How many times reapeat the texture to X direction. Float 1.0 is default value for no repeat."
						obj.addProperty("App::PropertyFloat", "Texture_Repeat_X", "Texture", info)

					if not hasattr(obj, "Texture_Repeat_Y"):
						info = "How many times reapeat the texture to Y direction. Float 1.0 is default value for no repeat."
						obj.addProperty("App::PropertyFloat", "Texture_Repeat_Y", "Texture", info)

					if not hasattr(obj, "Texture_Rotation"):
						info = "Texture rotation. Float 0 is default value for no rotation."
						obj.addProperty("App::PropertyFloat", "Texture_Rotation", "Texture", info)
					
					if not hasattr(obj, "Texture_Fit"):
						info = "Texture coordinate to fit object shape better."
						obj.addProperty("App::PropertyString", "Texture_Fit", "Texture", info)

					if str(textureURL) != "":
						obj.Texture_URL = str(textureURL)
						
					if str(self.repeatXO.text()) != "":
						obj.Texture_Repeat_X = float(self.repeatXO.text())
						
					if str(self.repeatYO.text()) != "":
						obj.Texture_Repeat_Y = float(self.repeatYO.text())
						
					if str(self.rotateO.text()) != "":
						obj.Texture_Rotation = float(self.rotateO.text())
					
					obj.Texture_Fit = str(self.gFit)
					
				except:
					skip = 1
		
			# show status
			if skip == 0:
				self.showStatus(translate('setTextures', 'Texture properties has been stored.'))
			else:
				self.showStatus(translate('setTextures', 'Error during setting properties.'))


		# ############################################################################
		# actions - load internal functions
		# ############################################################################


		def getChildPosition(self, iRootnode):
			
			pos = 0
			for c in iRootnode.getChildren():
				if str(c).find("SoSwitch") != -1:
					return pos
					break

				pos = pos + 1

			return -1
			
			
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
		
			# no texture URL set
			return ""
			
		
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
			textureFilename = os.path.basename(iURL)
			textureFilePath = os.path.join(tmpDir, textureFilename)

			# check if file already exists and skip slow downloading
			if not os.path.exists(textureFilePath):

				try:
					# get image from URL
					data = urllib.request.urlopen(iURL)
				except:
					# if broken URL or removed image
					self.gBrokenURL[str(iObj.Label)] = iURL
					return ""

				# create temp file with image
				out = open(str(textureFilePath), "wb")
				out.write(data.read())
				out.close()

			return textureFilePath

		
		def setTexture(self, iObj, iFile):
		
			rootnode = iObj.ViewObject.RootNode
			
			# set flag
			setTrans = 0

			# set X repeat factor
			if hasattr(iObj, "Texture_Repeat_X"):
				if isinstance(iObj.Texture_Repeat_X, float):
					repeatX = float(iObj.Texture_Repeat_X)
					setTrans = setTrans + 1

			# set Y repeat factor
			if hasattr(iObj, "Texture_Repeat_Y"):
				if isinstance(iObj.Texture_Repeat_Y, float):
					repeatY = float(iObj.Texture_Repeat_Y)
					setTrans = setTrans + 1

			# set rotation factor
			if hasattr(iObj, "Texture_Rotation"):
				if isinstance(iObj.Texture_Rotation, float):
					rotation = float(iObj.Texture_Rotation)
					setTrans = setTrans + 1

			# update if there is transformation child
			skip = 0
			counter = 0
			
			for i in rootnode.getChildren():
				
				if hasattr(i, "filename"):

					# replace texure URL
					i.filename = ""
					i.filename = iFile
					skip = 1

				if hasattr(i, "scaleFactor") and hasattr(i, "rotation"):
					counter = counter + 1
					if counter == 2:
						if setTrans == 3:
							i.scaleFactor.setValue(repeatX, repeatY)
							i.rotation.setValue(rotation)

			# add new if there is no transformation child
			if skip == 0:

				if setTrans == 3:
					# set transform
					trans = coin.SoTexture2Transform()
					trans.scaleFactor.setValue(repeatX, repeatY)
					trans.rotation.setValue(rotation)
					rootnode.insertChild(trans, 1)

				# set texture with URL
				texture =  coin.SoTexture2()
				texture.filename = iFile
				rootnode.insertChild(texture, 2)


		def fitTexture(self, iObj):
		
			rootnode = iObj.ViewObject.RootNode
		
			if hasattr(iObj, "Texture_Fit"):
				if isinstance(iObj.Texture_Fit, str):
					cr = str(iObj.Texture_Fit)
					
					coordinate = ""
					
					if cr == "biggest surface":
						coordinate = coin.SoTextureCoordinateDefault()
					
					if cr == "fit to Cube":
						coordinate = coin.SoTextureCoordinateCube()

					if cr == "fit to Cylinder":
						coordinate = coin.SoTextureCoordinateCylinder()
					
					if cr == "fit to Sphere":
						coordinate = coin.SoTextureCoordinateSphere()
					
					if cr == "glass mirror effect":
						coordinate = coin.SoTextureCoordinateEnvironment()
					
					if cr == "auto fit":
						
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
		# actions - load
		# ############################################################################


		def loadTextures(self, iSearch):

			self.gBrokenURL = dict()
			empty = ""
			
			# search all objects and set URL
			for obj in iSearch:
				
				# try set color
				if self.checkColor.isChecked():
					if MagicPanels.gKernelVersion >= 1.0:
						try:
							m = obj.ViewObject.ShapeAppearance[0]
							m.DiffuseColor = (1.0, 1.0, 1.0, 0.0)
							obj.ViewObject.ShapeAppearance = ( m )
						except:
							skip = 1
					else:
						try:
							obj.ViewObject.ShapeColor = (1.0, 1.0, 1.0, 0.0)
							obj.ViewObject.DiffuseColor = (1.0, 1.0, 1.0, 0.0)
						except:
							skip = 1
					
				textureURL = self.getTextureURL(obj)

				# if no texture found for object skip it
				if str(textureURL) == "":
					continue
				else:
					empty = "no"

				# chose URL or local HDD
				if textureURL.startswith("http"):
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
		# actions - caller selection
		# ############################################################################


		def checkSelected(self, iOperation, iSelection):

			# set objects to search
			if iSelection == "selected":
				selected = FreeCADGui.Selection.getSelection()
				if len(selected) == 0:
					iText = translate('setTextures', 'Please select objects and try again.')
					self.showStatus(iText)
					return
				else:
					searchObjects = selected
			else:
				searchObjects = FreeCAD.ActiveDocument.Objects

			if iOperation == "store":
				self.storeTextures(searchObjects, iSelection)
			
			if iOperation == "load":
				if iSelection == "selected":
					FreeCADGui.Selection.clearSelection()
				
				self.loadTextures(searchObjects)


		# ############################################################################
		# actions - select
		# ############################################################################


		def storeSelected(self):
			self.checkSelected("store", "selected")

		def storeAll(self):
			self.checkSelected("store", "all")

		def loadSelected(self):
			self.checkSelected("load", "selected")

		def loadAll(self):
			self.checkSelected("load", "all")


		# ############################################################################
		# actions - Coordinate
		# ############################################################################


		def setCoordinate(self, selectedText):
			self.gFit = str(selectedText)


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
