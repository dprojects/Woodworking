# ###################################################################################################################
'''

FreeCAD macro for woodworking to apply and store textures
Author: Darek L (github.com/dprojects)
Latest version: https://github.com/dprojects/setTextures

Certified platform:

OS: Ubuntu 22.04 LTS (XFCE/xubuntu)
Word size of FreeCAD: 64-bit
Version: 0.20.29177 (Git) AppImage
Build type: Release
Branch: (HEAD detached at 0.20)
Hash: 68e337670e227889217652ddac593c93b5e8dc94
Python 3.9.13, Qt 5.12.9, Coin 4.0.0, Vtk 9.1.0, OCC 7.5.3
Locale: English/United States (en_US)
Installed mods: 
  * Woodworking 0.20.29177

https://github.com/dprojects/Woodworking

'''
# ###################################################################################################################


import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore
from pivy import coin

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
			toolSH = 450
			
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
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - init button
			# ############################################################################

			# button
			self.initBA = QtGui.QPushButton(translate('setTextures', 'show stored textures for all objects'), self)
			self.initBA.clicked.connect(self.loadAll)
			self.initBA.resize(280, 40)
			self.initBA.move(10, 10)

			# ############################################################################
			# options - store textures
			# ############################################################################

			# label
			info = ""
			info += translate('setTextures', 'Set new textures or change:')
			self.storeL = QtGui.QLabel(info, self)
			self.storeL.move(10, 70)

			# color
			# ############################################################################

			self.checkColor = QtGui.QCheckBox(translate('setTextures', '- set white color'), self)
			self.checkColor.setCheckState(QtCore.Qt.Checked)
			self.checkColor.move(10, 100)

			# URL
			# ############################################################################

			# label
			info = ""
			info += translate('setTextures', 'Texture URL or local HDD path:')
			self.urlL = QtGui.QLabel(info, self)
			self.urlL.move(10, 130)

			# text input
			self.urlO = QtGui.QLineEdit(self)
			self.urlO.setText(str(""))
			self.urlO.setFixedWidth(235)
			self.urlO.move(10, 150)

			# button
			self.urlHDD = QtGui.QPushButton("...", self)
			self.urlHDD.clicked.connect(self.loadCustomFile)
			self.urlHDD.setFixedWidth(40)
			self.urlHDD.move(250, 150)

			# repeat
			# ############################################################################

			# text input
			self.repeatXO = QtGui.QLineEdit(self)
			self.repeatXO.setText(str("1.0"))
			self.repeatXO.setFixedWidth(50)
			self.repeatXO.move(10, 180)

			# label
			info = ""
			info += translate('setTextures', '- repeat X, set 1 to not repeat')
			self.repeatXL = QtGui.QLabel(info, self)
			self.repeatXL.move(70, 183)

			# text input
			self.repeatYO = QtGui.QLineEdit(self)
			self.repeatYO.setText(str("1.0"))
			self.repeatYO.setFixedWidth(50)
			self.repeatYO.move(10, 200)

			# label
			info = ""
			info += translate('setTextures', '- repeat Y, set 1 to not repeat')
			self.repeatYL = QtGui.QLabel(info, self)
			self.repeatYL.move(70, 203)

			# rotation
			# ############################################################################

			# text input
			self.rotateO = QtGui.QLineEdit(self)
			self.rotateO.setText(str("0.0"))
			self.rotateO.setFixedWidth(50)
			self.rotateO.move(10, 220)

			# label
			info = ""
			info += translate('setTextures', '- rotation, set 0 to not rotate')
			self.rotateL = QtGui.QLabel(info, self)
			self.rotateL.move(70, 223)

			# fit mode
			# ############################################################################

			# options
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
			self.fitO.activated[str].connect(self.setCoordinate)
			self.fitO.setFixedWidth(150)
			self.fitO.move(10, 250)
			
			# label
			self.fitL = QtGui.QLabel(translate('setTextures', '- fit mode'), self)
			self.fitL.move(170, 253)
			
			# store & load buttons
			# ############################################################################

			# label
			info = ""
			info += translate('setTextures', 'Store texture properties for:')
			self.storeL = QtGui.QLabel(info, self)
			self.storeL.move(10, 280)

			# button
			self.storeBS = QtGui.QPushButton(translate('setTextures', 'selected objects only'), self)
			self.storeBS.clicked.connect(self.storeSelected)
			self.storeBS.resize(150, 40)
			self.storeBS.move(10, 300)

			# button
			self.storeBA = QtGui.QPushButton(translate('setTextures', 'all objects'), self)
			self.storeBA.clicked.connect(self.storeAll)
			self.storeBA.resize(100, 40)
			self.storeBA.move(190, 300)

			# label
			info = ""
			info += translate('setTextures', 'Refresh texture for:')
			self.loadL = QtGui.QLabel(info, self)
			self.loadL.move(10, 350)

			# button
			self.loadBS = QtGui.QPushButton(translate('setTextures', 'selected objects only'), self)
			self.loadBS.clicked.connect(self.loadSelected)
			self.loadBS.resize(150, 40)
			self.loadBS.move(10, 370)

			# button
			self.loadBA = QtGui.QPushButton(translate('setTextures', 'all objects'), self)
			self.loadBA.clicked.connect(self.loadAll)
			self.loadBA.resize(100, 40)
			self.loadBA.move(190, 370)

			# ############################################################################
			# status
			# ############################################################################

			# label
			space = ""
			space += "                                                "
			space += "                                                "
			space += "                                                "
			space += "                                                "
			space += "                                                "
			space += "                                                "
			self.status = QtGui.QLabel(space, self)
			self.status.move(10, 420)

			# ############################################################################
			# show all
			# ############################################################################

			self.show()

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
						info = "Amount of times to repeat the texture in the X direction. Float 1.0 is default value for no repeat."
						obj.addProperty("App::PropertyFloat", "Texture_Repeat_X", "Texture", info)

					if not hasattr(obj, "Texture_Repeat_Y"):
						info = "Amount of times to repeat the texture in the Y direction. Float 1.0 is default value for no repeat."
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
				self.showStatus(translate('setTextures', 'Texture properties have been stored.'))
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

					# replace texture URL
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

			# check selected
			selected = FreeCADGui.Selection.getSelection()
			selectedLen = len(selected)

			if iSelection == "selected" and selectedLen == 0:
				iText = translate('setTextures', 'Please select objects and try again.')
				self.showStatus(iText)
			else:

				# set objects to search
				if iSelection == "selected":
					searchObjects = selected
				else:
					searchObjects = FreeCAD.activeDocument().Objects

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
			try:
				self.checkSelected("store", "selected")
			except:
				iText = translate('setTextures', 'Please select objects and try again.')
				self.showStatus(iText)

		def storeAll(self):
			try:
				self.checkSelected("store", "all")
			except:
				iText = translate('setTextures', 'Please select objects and try again.')
				self.showStatus(iText)

		def loadSelected(self):
			try:
				self.checkSelected("load", "selected")
			except:
				iText = translate('setTextures', 'Please select objects and try again.')
				self.showStatus(iText)

		def loadAll(self):
			try:
				self.checkSelected("load", "all")
			except:
				iText = translate('setTextures', 'Please select objects and try again.')
				self.showStatus(iText)


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
