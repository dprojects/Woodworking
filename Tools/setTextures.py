# -*- coding: utf-8 -*-

# FreeCAD macro for woodworking to apply and store textures
# Author: Darek L (aka dprojects)
# Version: 6.4
# Latest version: https://github.com/dprojects/setTextures

import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore
from pivy import coin
import urllib.request
import tempfile
import os


# ###################################################################################################################
# Qt GUI
# ###################################################################################################################

def showQtMain():

	class QtMainClass(QtGui.QDialog):

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):
			
			# main window
			self.setGeometry(400, 250, 800, 450)
			self.setWindowTitle("setTextures")
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# info
			info = ""
			info += "If you want to load all stored textures, please go to Step 4 "
			info += "and click \"load - all objects\" button."
			self.step0 = QtGui.QLabel(info, self)
			self.step0.move(10, 10)

			# ############################################################
			# step 1
			# ############################################################

			# label
			info = ""
			info += "Step 1. Add texture URL path:"
			self.step1 = QtGui.QLabel(info, self)
			self.step1.move(10, 40)

			# text input
			self.pathI = QtGui.QLineEdit(self)
			self.pathI.setText(str(""))
			self.pathI.setFixedWidth(750)
			self.pathI.move(10, 60)

			# ############################################################
			# step 2
			# ############################################################

			# label
			info = ""
			info += "Step 2. Set texture properties:"
			self.step2 = QtGui.QLabel(info, self)
			self.step2.move(10, 100)

			# text input
			self.factorX = QtGui.QLineEdit(self)
			self.factorX.setText(str("1.0"))
			self.factorX.setFixedWidth(50)
			self.factorX.move(10, 120)

			# label
			info = ""
			info += " - repeat X direction fator, leave it 1.0, if you do not want to repeat texture"
			self.step2a = QtGui.QLabel(info, self)
			self.step2a.move(70, 123)

			# text input
			self.factorY = QtGui.QLineEdit(self)
			self.factorY.setText(str("1.0"))
			self.factorY.setFixedWidth(50)
			self.factorY.move(10, 150)

			# label
			info = ""
			info += " - repeat Y direction fator, leave it 1.0, if you do not want to repeat texture"
			self.step2b = QtGui.QLabel(info, self)
			self.step2b.move(70, 153)

			# text input
			self.factorRotation = QtGui.QLineEdit(self)
			self.factorRotation.setText(str("0.0"))
			self.factorRotation.setFixedWidth(50)
			self.factorRotation.move(10, 180)

			# label
			info = ""
			info += " - rotation texture factor, leave it 0.0, if you do not want to rotate texture"
			self.step2c = QtGui.QLabel(info, self)
			self.step2c.move(70, 183)

			# ############################################################
			# step 3
			# ############################################################

			# label
			info = ""
			info += "Step 3. Store texture properties, if no URL this property will be set to empty string:"
			self.step3 = QtGui.QLabel(info, self)
			self.step3.move(10, 230)

			# button
			self.step3a = QtGui.QPushButton("store - selected objects only", self)
			self.step3a.clicked.connect(lambda: self.checkSelected("store", "selected"))
			self.step3a.move(100, 250)
			self.step3a.resize(200, 40)

			# button
			self.step3b = QtGui.QPushButton("store - all objects", self)
			self.step3b.clicked.connect(lambda: self.checkSelected("store", "all"))
			self.step3b.move(400, 250)
			self.step3b.resize(200, 40)

			# ############################################################
			# step 4
			# ############################################################

			# label
			info = ""
			info += "Step 4. Download and apply textures from stored URLs:"
			self.step4 = QtGui.QLabel(info, self)
			self.step4.move(10, 300)

			# button
			self.step4a = QtGui.QPushButton("load - selected objects only", self)
			self.step4a.clicked.connect(lambda: self.checkSelected("load", "selected"))
			self.step4a.move(100, 320)
			self.step4a.resize(200, 40)

			# button
			self.step4b = QtGui.QPushButton("load - all objects", self)
			self.step4b.clicked.connect(lambda: self.checkSelected("load", "all"))
			self.step4b.move(400, 320)
			self.step4b.resize(200, 40)

			# ############################################################
			# status
			# ############################################################

			# label
			space = ""
			space += "                                                                                        "
			space += "                                                                                        "
			space += "                                                                                        "
			self.Status = QtGui.QLabel(space, self)
			self.Status.move(10, 420)

			# ############################################################
			# show all
			# ############################################################

			self.show()

		# ############################################################
		# actions - status
		# ############################################################
		
		def showStatus(self, iText):
			self.Status.setText(str(iText))

		# ############################################################
		# actions - store
		# ############################################################
		
		def setTextureProperty(self, iSearch, iSelect):

			# set flag
			skip = 0

			# get texture URL from GUI text form
			textureURL = self.pathI.text()

			# scan all given objects and set all properties
			for obj in iSearch:

				# skip everything except furniture parts if for all
				if (
					iSelect != "selected" and
					not obj.isDerivedFrom("Part::Box") and 
					not obj.isDerivedFrom("PartDesign::Pad")
				):
					continue

				# set properties
				try:

					if not hasattr(obj, "Texture_URL"):
						obj.addProperty("App::PropertyString", "Texture_URL", "Texture", "Texture URL, need to star with http, cannot be disk file.")

					if not hasattr(obj, "Texture_Repeat_X"):
						obj.addProperty("App::PropertyFloat", "Texture_Repeat_X", "Texture", "How many times reapeat the texture to X direction. Float 1.0 is default value for no repeat.")

					if not hasattr(obj, "Texture_Repeat_Y"):
						obj.addProperty("App::PropertyFloat", "Texture_Repeat_Y", "Texture", "How many times reapeat the texture to Y direction. Float 1.0 is default value for no repeat.")

					if not hasattr(obj, "Texture_Rotation"):
						obj.addProperty("App::PropertyFloat", "Texture_Rotation", "Texture", "Texture rotation. Float 0 is default value for no rotation.")
					
					obj.Texture_URL = str(textureURL)
					obj.Texture_Repeat_X = float(self.factorX.text())
					obj.Texture_Repeat_Y = float(self.factorY.text())
					obj.Texture_Rotation = float(self.factorRotation.text())
				except:
					skip = 1
		
			# show status
			if skip == 0:
				self.showStatus("Texture properties has been stored.")
			else:
				self.showStatus("Error during setting properties.")
		
		# ############################################################
		# actions - load
		# ############################################################
		
		def loadStoredTextures(self, iSearch):

			# variables
			empty = ""
			brokenURL = dict()

			# create temp directory
			tmpDir = tempfile.gettempdir()
			tmpDir = os.path.join(tmpDir, "FreeCAD_Textures")
			if not os.path.exists(tmpDir):
				os.makedirs(tmpDir)

			# search all objects
			for obj in iSearch:
				
				textureURL = ""

				# support for texture URL stored at objects Texture_URL property
				try:
					ref = str(obj.Texture_URL)
					if ref != "" and ref.startswith("http"):
						textureURL = ref
				except:
					skip = 1
	
				# support for texture URL stored at objects description	
				try:
					ref = str(obj.Label2)
					if ref != "" and ref.startswith("http"):
						textureURL = ref
				except:
					skip = 1
	
				# backward compatibility and support for manually added to Texture property
				try:
					ref = str(obj.Texture)
					if ref != "" and ref.startswith("http"):
						textureURL = ref
				except:
					skip = 1
	
				# support for texture URL stored at Material Card TexturePath
				try:
					ref = str(obj.Material.Material["TexturePath"])
					if ref != "" and ref.startswith("http"):
						textureURL = ref
				except:
					skip = 1
		
				# if no texture found for object skip it
				if str(textureURL) == "":
					continue
		
				# mark found
				empty = textureURL

				# get texture filename
				textureFilename = os.path.basename(textureURL)
				textureFilePath = os.path.join(tmpDir, textureFilename)

				# check if file already exists and skip slow downloading
				if not os.path.exists(textureFilePath):

					try:
						# get image from URL
						data = urllib.request.urlopen(textureURL)
					except:
						# if broken URL or removed image
						brokenURL[str(obj.Label)] = textureURL
						continue

					# create temp file with image
					out = open(str(textureFilePath), "wb")
					out.write(data.read())
					out.close()
		
				# set search reference
				rootnode = obj.ViewObject.RootNode

				# set flag
				setTrans = 0

				# set X repeat factor
				if hasattr(obj, "Texture_Repeat_X"):
					if isinstance(obj.Texture_Repeat_X, float):
						repeatX = float(obj.Texture_Repeat_X)
						setTrans = setTrans + 1

				# set Y repeat factor
				if hasattr(obj, "Texture_Repeat_Y"):
					if isinstance(obj.Texture_Repeat_Y, float):
						repeatY = float(obj.Texture_Repeat_Y)
						setTrans = setTrans + 1

				# set rotation factor
				if hasattr(obj, "Texture_Rotation"):
					if isinstance(obj.Texture_Rotation, float):
						rotation = float(obj.Texture_Rotation)
						setTrans = setTrans + 1

				# check if already texure is applied
				skip = 0
				counter = 0
				for i in rootnode.getChildren():
					if hasattr(i, "filename"):

						# replace texure URL
						i.filename = ""
						i.filename = textureFilePath
						skip = 1

					if hasattr(i, "scaleFactor") and hasattr(i, "rotation"):
						counter = counter + 1
						if counter == 2:
							if setTrans == 3:
								i.scaleFactor.setValue(repeatX, repeatY)
								i.rotation.setValue(rotation)
		
				# set texture as new if not applied
				if skip == 0:

					# set texture transformation
					trans = coin.SoTexture2Transform()
					if setTrans == 3:
						trans.scaleFactor.setValue(repeatX, repeatY)
						trans.rotation.setValue(rotation)

					rootnode.insertChild(trans, 1)

					# set texture with URL
					texture =  coin.SoTexture2()
					texture.filename = textureFilePath
					rootnode.insertChild(texture, 2)

			if empty == "":
				iText = "No textures URLs found. " 
				self.showStatus(iText)
			else:
				if len(brokenURL) == 0:
					self.showStatus("All textures has been loaded from stored URLs.")
				else:
					FreeCAD.Console.PrintMessage("\n ====================== \n")
					for n, b in brokenURL.items():
						FreeCAD.Console.PrintMessage("\n")
						FreeCAD.Console.PrintMessage("Object Label: "+n)
						FreeCAD.Console.PrintMessage("\n")
						FreeCAD.Console.PrintMessage("Broken URL: "+b)
						FreeCAD.Console.PrintMessage("\n")
					FreeCAD.Console.PrintMessage("\n ====================== \n")

					info = ""
					info += "Some textures has been removed or URL is broken. "
					info += "See Report view (Console) for more info."
					self.showStatus(info)

		# ############################################################
		# actions - caller selection
		# ############################################################
		
		def checkSelected(self, iOperation, iSelection):

			# check selected
			selected = FreeCADGui.Selection.getSelection()
			selectedLen = len(selected)

			if iSelection == "selected" and selectedLen == 0:
				iText = "No objects selected. Please select objects and try again."
				self.showStatus(iText)
			else:

				# set objects to search
				if iSelection == "selected":
					searchObjects = selected
				else:
					searchObjects = FreeCAD.activeDocument().Objects

				if iOperation == "store":
					self.setTextureProperty(searchObjects, iSelection)
				if iOperation == "load":
					self.loadStoredTextures(searchObjects)

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
