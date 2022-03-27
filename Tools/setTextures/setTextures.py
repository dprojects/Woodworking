# -*- coding: utf-8 -*-

# FreeCAD macro for woodworking to apply and store textures
# Author: Darek L (aka dprojects)
# Version: 2.0 (improved locations)
# Latest version: https://github.com/dprojects/setTextures

import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore
from pivy import coin
import urllib.request
import tempfile
import os

empty = ""

# create temp directory
with tempfile.TemporaryDirectory() as tmpDir:

	FreeCAD.Console.PrintMessage("\n\n")
	FreeCAD.Console.PrintMessage("Directory: "+tmpDir)

	# search all objects
	for obj in FreeCAD.activeDocument().Objects:
		
		textureURL = ""

		try:
			
			# support for texture URL stored at objects description
			if textureURL == "":
				ref = str(obj.Label2)
				if ref != "" and ref.startswith("http"):
					textureURL = ref

			# support for texture URL stored at objects Texture property	
			if textureURL == "":
				ref = str(obj.Texture)
				if ref != "" and ref.startswith("http"):
					textureURL = ref

			# support for texture URL stored at Material Card TexturePath
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

		# get image from URL
		data = urllib.request.urlopen(textureURL)

		# create temp file with image
		texFilename = os.path.join(tmpDir, obj.Label)
		out = open(str(texFilename), "wb")
		out.write(data.read())
		out.close()

		FreeCAD.Console.PrintMessage("\n")	
		FreeCAD.Console.PrintMessage("File: "+texFilename)

		# apply texture
		rootnode = obj.ViewObject.RootNode
		texture =  coin.SoTexture2()
		texture.filename = texFilename

		# check if already texure is applied
		skip = 0
		for i in rootnode.getChildren():
			if hasattr(i, "filename"):
				
				# replace texure
				i.filename = ""
				i.filename = texFilename
				skip = 1

		# set texture as new if not applied
		if skip == 0:
			rootnode.insertChild(texture, 1)

# if no textures show info
if empty == ""	:
	iText = ""
	iText += "No textures URLs found. \n" 
	iText += "Please see the documentation to find out how to store textures. \n"
	QtGui.QMessageBox.information(None,"setTextures",str(iText))