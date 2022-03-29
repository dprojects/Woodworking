# -*- coding: utf-8 -*-

# FreeCAD macro for woodworking to apply and store textures
# Author: Darek L (aka dprojects)
# Version: 4.0
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

	global gExecute

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
			self.setGeometry(400, 250, 800, 250)
			self.setWindowTitle("setTextures")
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# texture URL path
			# ############################################################################

			# label
			self.pathL = QtGui.QLabel("Texture URL path:", self)
			self.pathL.move(10, 40)

			# text input
			self.pathI = QtGui.QLineEdit(self)
			self.pathI.setText(str(""))
			self.pathI.setFixedWidth(750)
			self.pathI.move(10, 63)

			# label
			self.pathSL = QtGui.QLabel("Store given URL to all selected objects at property named Texture (if no URL this property will be empty).", self)
			self.pathSL.move(100, 103)

			# button
			self.pathS = QtGui.QPushButton("store", self)
			self.pathS.clicked.connect(self.setTextureProperty)
			self.pathS.move(10, 100)

			# label
			self.pathGL = QtGui.QLabel("Download and apply textures from stored URLs (for all objects or selected only).", self)
			self.pathGL.move(100, 133)

			# button
			self.pathG = QtGui.QPushButton("load", self)
			self.pathG.clicked.connect(self.loadStoredTextures)
			self.pathG.move(10, 130)

			# label
			space = ""
			space += "                                                                                        "
			space += "                                                                                        "
			space += "                                                                                        "
			self.Status = QtGui.QLabel(space, self)
			self.Status.move(10, 200)

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

			selected = FreeCADGui.Selection.getSelection()
			selectedLen = len(selected)

			if selectedLen == 0:
				iText = ""
				iText += "No selected objects found. \n" 
				iText += "Please select objects to add property. \n"
				self.showStatus(iText)
		
			textureURL = self.pathI.text()

			for obj in selected:
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

			# check if load for selected only or all
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
					if textureURL == "":
						ref = str(obj.Label2)
						if ref != "" and ref.startswith("http"):
							textureURL = ref
				except:
					textureURL = ""
	
				# support for texture URL stored at objects Texture property
				try:
					if textureURL == "":
						ref = str(obj.Texture)
						if ref != "" and ref.startswith("http"):
							textureURL = ref
				except:
					textureURL = ""
	
				# support for texture URL stored at Material Card TexturePath
				try:
					if textureURL == "":
						ref = str(obj.Material.Material["TexturePath"])
						if ref != "" and ref.startswith("http"):
							textureURL = ref
				except:
					textureURL = ""
		
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
