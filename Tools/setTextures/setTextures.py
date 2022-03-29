# -*- coding: utf-8 -*-

# FreeCAD macro for woodworking to apply and store textures
# Author: Darek L (aka dprojects)
# Version: 5.0
# Latest version: https://github.com/dprojects/setTextures

import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore
from pivy import coin
import urllib.request
import tempfile
import os


# ###################################################################################################################
# Support for Qt GUI
# ###################################################################################################################


def showQtMain():

	# ############################################################################
	# Qt Main Class
	# ############################################################################
	
	class QtMainClass(QtGui.QDialog):

		# init 
		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):
			
			# window
			self.result = userCancelled
			self.setGeometry(400, 250, 800, 350)
			self.setWindowTitle("setTextures")
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# texture URL path
			# ############################################################################

			# label
			info = ""
			info += "If you want to load all stored textures, please go to Step 3, without selection, and click load button."
			self.step0 = QtGui.QLabel(info, self)
			self.step0.move(10, 10)

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

			# label
			info = ""
			info += "Step 2. Store given URL at property named Texture"
			info += ", if no URL this property will be set to empty string:"
			self.step2 = QtGui.QLabel(info, self)
			self.step2.move(10, 100)

			# button
			self.pathS = QtGui.QPushButton("store", self)
			self.pathS.clicked.connect(self.setTextureProperty)
			self.pathS.move(10, 120)
			self.pathS.resize(80, 40)

			# label
			info = ""
			info += "- Selected objects - if objects selected e.g. good to change texture for single object only"
			self.step2a = QtGui.QLabel(info, self)
			self.step2a.move(100, 123)

			# label
			info = ""
			info += "- All objects - if no objects selected e.g. good for merged projects and many objects"
			self.step2b = QtGui.QLabel(info, self)
			self.step2b.move(100, 143)


			# label
			info = ""
			info += "Step 3. Download and apply textures from stored URLs:"
			self.step3 = QtGui.QLabel(info, self)
			self.step3.move(10, 200)

			# button
			self.pathG = QtGui.QPushButton("load", self)
			self.pathG.clicked.connect(self.loadStoredTextures)
			self.pathG.move(10, 220)
			self.pathG.resize(80, 40)

			# label
			info = ""
			info += "- Selected objects - if objects selected e.g. good to refresh changed textures"
			self.step3a = QtGui.QLabel(info, self)
			self.step3a.move(100, 223)

			# label
			info = ""
			info += "- All objects - if no objects selected e.g. good to load all stored textures"
			self.step3b = QtGui.QLabel(info, self)
			self.step3b.move(100, 243)


			# label
			space = ""
			space += "                                                                                        "
			space += "                                                                                        "
			space += "                                                                                        "
			self.Status = QtGui.QLabel(space, self)
			self.Status.move(10, 320)

			# ############################################################################
			# show
			# ############################################################################

			self.show()

		# ############################################################################
		# actions
		# ############################################################################
		
		def onCancel(self):
			self.result = userCancelled
			self.close()
		def onOk(self):
			self.result = userOK
			self.close()

		def showStatus(self, iText):
		
			# show info
			QtGui.QMessageBox.information(None,"setTextures",str(iText))

		def setTextureProperty(self):

			# check if for selected only or all
			selected = FreeCADGui.Selection.getSelection()
			selectedLen = len(selected)

			if selectedLen > 0:
				searchObjects = selected
			else:
				searchObjects = FreeCAD.activeDocument().Objects

		
			textureURL = self.pathI.text()

			for obj in searchObjects:

				# skip everything except furniture parts if for all
				if (
					selectedLen == 0 and
					not obj.isDerivedFrom("Part::Box") and 
					not obj.isDerivedFrom("PartDesign::Pad")
				):
					continue

				# set property
				try:
					if not hasattr(obj, "Texture"):
						obj.addProperty("App::PropertyString", "Texture", "Base", "")
					
					obj.Texture = str(textureURL)
				except:
					skip = 1
		
			self.Status.setText("You should find the given URL at Texture property for all selected objects.")
		
		def loadStoredTextures(self):

			# set flag
			empty = ""

			# create temp directory
			tmpDir = tempfile.gettempdir()
			tmpDir = os.path.join(tmpDir, "FreeCAD_Textures")
			if not os.path.exists(tmpDir):
				os.makedirs(tmpDir)

			# check if for selected only or all
			selected = FreeCADGui.Selection.getSelection()
			selectedLen = len(selected)

			if selectedLen > 0:
				searchObjects = selected
			else:
				searchObjects = FreeCAD.activeDocument().Objects

			# search all objects
			for obj in searchObjects:
				
				textureURL = ""
	
				# support for texture URL stored at objects description	
				try:
					ref = str(obj.Label2)
					if ref != "" and ref.startswith("http"):
						textureURL = ref
				except:
					skip = 1
	
				# support for texture URL stored at objects Texture property
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

					# get image from URL
					data = urllib.request.urlopen(textureURL)
			
					# create temp file with image
					out = open(str(textureFilePath), "wb")
					out.write(data.read())
					out.close()
		
				# apply texture
				rootnode = obj.ViewObject.RootNode
				texture =  coin.SoTexture2()
				texture.filename = textureFilePath
		
				# check if already texure is applied
				skip = 0
				for i in rootnode.getChildren():
					if hasattr(i, "filename"):
						
						# replace texure
						i.filename = ""
						i.filename = textureFilePath
						skip = 1
		
				# set texture as new if not applied
				if skip == 0:
					rootnode.insertChild(texture, 1)

			if empty == "":
				iText = ""
				iText += "No textures URLs found. \n" 
				iText += "Please see the documentation to find out how to store textures. \n"
				self.showStatus(iText)
			else:
				self.Status.setText("All textures has been loaded from stored URLs.")


	# ############################################################################
	# final settings
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
