# -*- coding: utf-8 -*-

# This colorManager tool is part of Woodworking workbench. However, you can use it as standalone macro.
# Author: Darek L (github.com/dprojects)

import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore


# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals
		# ############################################################################

		gFace = ""
		gObj = ""
		gMode = ""
		gObjArr = []
		gFaceArr = dict()
		gFaceIndex = -1
		gStep = 5
		
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
			toolSW = 260
			toolSH = 300
			
			# active screen size - FreeCAD main window
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = int( gSW - toolSW - 10 )
			gPH = int( gSH - toolSH )

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle("colorManager")
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			# screen
			info = ""
			info += "                                             "
			info += "                                             "
			info += "                                             "
			self.s1S = QtGui.QLabel(info, self)
			self.s1S.move(10, 10)

			# button
			self.s1B1 = QtGui.QPushButton("refresh selection", self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(240)
			self.s1B1.move(10, 40)

			# button
			self.s1B2 = QtGui.QPushButton("set face colors from spreadsheet", self)
			self.s1B2.clicked.connect(self.setSheet)
			self.s1B2.setFixedWidth(240)
			self.s1B2.move(10, 70)

			# ############################################################################
			# options - red color
			# ############################################################################

			# label
			self.o1L = QtGui.QLabel("Select red:", self)
			self.o1L.move(10, 113)

			# button
			self.o1B1 = QtGui.QPushButton("<", self)
			self.o1B1.clicked.connect(self.setColorO1B1)
			self.o1B1.setFixedWidth(50)
			self.o1B1.move(100, 110)
			self.o1B1.setAutoRepeat(True)
			
			# text input
			self.o1E = QtGui.QLineEdit(self)
			self.o1E.setText("")
			self.o1E.setFixedWidth(50)
			self.o1E.move(150, 110)

			# button
			self.o1B2 = QtGui.QPushButton(">", self)
			self.o1B2.clicked.connect(self.setColorO1B2)
			self.o1B2.setFixedWidth(50)
			self.o1B2.move(200, 110)
			self.o1B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - green color
			# ############################################################################

			# label
			self.o2L = QtGui.QLabel("Select green:", self)
			self.o2L.move(10, 143)

			# button
			self.o2B1 = QtGui.QPushButton("<", self)
			self.o2B1.clicked.connect(self.setColorO2B1)
			self.o2B1.setFixedWidth(50)
			self.o2B1.move(100, 140)
			self.o2B1.setAutoRepeat(True)
			
			# text input
			self.o2E = QtGui.QLineEdit(self)
			self.o2E.setText("")
			self.o2E.setFixedWidth(50)
			self.o2E.move(150, 140)

			# button
			self.o2B2 = QtGui.QPushButton(">", self)
			self.o2B2.clicked.connect(self.setColorO2B2)
			self.o2B2.setFixedWidth(50)
			self.o2B2.move(200, 140)
			self.o2B2.setAutoRepeat(True)

			# ############################################################################
			# options - blue color
			# ############################################################################

			# label
			self.o3L = QtGui.QLabel("Select blue:", self)
			self.o3L.move(10, 173)

			# button
			self.o3B1 = QtGui.QPushButton("<", self)
			self.o3B1.clicked.connect(self.setColorO3B1)
			self.o3B1.setFixedWidth(50)
			self.o3B1.move(100, 170)
			self.o3B1.setAutoRepeat(True)
			
			# text input
			self.o3E = QtGui.QLineEdit(self)
			self.o3E.setText("")
			self.o3E.setFixedWidth(50)
			self.o3E.move(150, 170)

			# button
			self.o3B2 = QtGui.QPushButton(">", self)
			self.o3B2.clicked.connect(self.setColorO3B2)
			self.o3B2.setFixedWidth(50)
			self.o3B2.move(200, 170)
			self.o3B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - update color
			# ############################################################################

			# label
			self.o4L = QtGui.QLabel("Step:", self)
			self.o4L.move(10, 203)

			# text input
			self.o4E = QtGui.QLineEdit(self)
			self.o4E.setText(str(self.gStep))
			self.o4E.setFixedWidth(50)
			self.o4E.move(100, 200)

			# update button
			self.o5B1 = QtGui.QPushButton("update color", self)
			self.o5B1.clicked.connect(self.setColor)
			self.o5B1.setFixedWidth(240)
			self.o5B1.move(10, 250)
			
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

		# ############################################################################
		def getFaceIndex(self):

			index = 1
			for f in self.gObj.Shape.Faces:
				if str(f.BoundBox) == str(self.gFace.BoundBox):
					return index

				index = index + 1
			
			return -1

		# ############################################################################
		def resetFaces(self):

			resetColor = self.gObj.ViewObject.ShapeColor
			faceArr = []
			
			for f in self.gObj.Shape.Faces:
				faceArr.append(resetColor)

			self.gObj.ViewObject.DiffuseColor = faceArr

		# ############################################################################
		def convertToRGB(self, iColor):
			return int(255 * iColor)

		# ############################################################################
		def convertToFreeCADColor(self, iColor):
			return float(iColor/255)

		# ############################################################################
		def convertFromName(self, iColor):
		
			if iColor == "blue":
				return (0.3333333432674408, 0.0, 1.0, 0.0)
		
			if iColor == "black":
				return (0.0, 0.0, 0.0, 0.0)
		
			if iColor == "red":
				return (1.0, 0.0, 0.0, 0.0)
		
			if iColor == "yellow":
				return (1.0, 1.0, 0.0, 0.0)
		
			if iColor == "white":
				return (1.0, 1.0, 1.0, 0.0)
		
			if iColor == "green":
				return (0.0, 1.0, 0.0, 0.0)
		
			return (0.800000011920929, 0.800000011920929, 0.800000011920929, 0.0)

		# ############################################################################
		def getColor(self):

			if self.gMode == "Face":

				# object has single color
				if len(self.gObj.ViewObject.DiffuseColor) == 1:
					
					r = self.gObj.ViewObject.ShapeColor[0]
					g = self.gObj.ViewObject.ShapeColor[1]
					b = self.gObj.ViewObject.ShapeColor[2]

				# faces has its own colors
				else:

					index = self.gFaceIndex
					r = self.gObj.ViewObject.DiffuseColor[index-1][0]
					g = self.gObj.ViewObject.DiffuseColor[index-1][1]
					b = self.gObj.ViewObject.DiffuseColor[index-1][2]

			if self.gMode == "Object":

				r = self.gObj.ViewObject.ShapeColor[0]
				g = self.gObj.ViewObject.ShapeColor[1]
				b = self.gObj.ViewObject.ShapeColor[2]


			if self.gMode == "Multi":

				# first face selected
				if self.gFace == "":

					r = self.gObj.ViewObject.ShapeColor[0]
					g = self.gObj.ViewObject.ShapeColor[1]
					b = self.gObj.ViewObject.ShapeColor[2]

				# first object selected, no face
				else:

					if len(self.gObj.ViewObject.DiffuseColor) == 1:
						
						r = self.gObj.ViewObject.ShapeColor[0]
						g = self.gObj.ViewObject.ShapeColor[1]
						b = self.gObj.ViewObject.ShapeColor[2]

					else:

						index = self.gFaceIndex
						r = self.gObj.ViewObject.DiffuseColor[index-1][0]
						g = self.gObj.ViewObject.DiffuseColor[index-1][1]
						b = self.gObj.ViewObject.DiffuseColor[index-1][2]

			# set GUI form with RGB color values
			cR = self.convertToRGB(r)
			cG = self.convertToRGB(g)
			cB = self.convertToRGB(b)

			self.o1E.setText(str(cR))
			self.o2E.setText(str(cG))
			self.o3E.setText(str(cB))

		# ############################################################################
		def setColor(self):

			try:
			
				if self.gMode == "Face":

					if len(self.gObj.ViewObject.DiffuseColor) == 1:
						self.resetFaces()

					index = self.gFaceIndex
					color = self.gObj.ViewObject.DiffuseColor

					c1 = self.convertToFreeCADColor( int(self.o1E.text()) )
					c2 = self.convertToFreeCADColor( int(self.o2E.text()) )
					c3 = self.convertToFreeCADColor( int(self.o3E.text()) )

					color[index-1] = (c1, c2, c3, 0.0)
					self.gObj.ViewObject.DiffuseColor = color

				if self.gMode == "Object":

					color = self.gObj.ViewObject.ShapeColor

					c1 = self.convertToFreeCADColor( int(self.o1E.text()) )
					c2 = self.convertToFreeCADColor( int(self.o2E.text()) )
					c3 = self.convertToFreeCADColor( int(self.o3E.text()) )

					color = (c1, c2, c3, 0.0)
					self.gObj.ViewObject.ShapeColor = color

				if self.gMode == "Multi":

					# save base selected color
					refObj = self.gObj
					refFace = self.gFace
					refFaceIndex = self.gFaceIndex
					
					for o in self.gObjArr:
						
						# set current object for other functions
						self.gObj = o
						
						# all object, no single faces
						if len(self.gFaceArr[o]) == 0:
							
							color = self.gObj.ViewObject.ShapeColor

							c1 = self.convertToFreeCADColor( int(self.o1E.text()) )
							c2 = self.convertToFreeCADColor( int(self.o2E.text()) )
							c3 = self.convertToFreeCADColor( int(self.o3E.text()) )

							color = (c1, c2, c3, 0.0)
							self.gObj.ViewObject.ShapeColor = color

						# faces selected for object
						else:

							i = 0
							for f in self.gFaceArr[o]:

								# set current face for other functions
								self.gFace = self.gFaceArr[o][i]
								self.gFaceIndex = self.getFaceIndex()
							
								if len(self.gObj.ViewObject.DiffuseColor) == 1:
									self.resetFaces()

								index = self.gFaceIndex
								color = self.gObj.ViewObject.DiffuseColor

								c1 = self.convertToFreeCADColor( int(self.o1E.text()) )
								c2 = self.convertToFreeCADColor( int(self.o2E.text()) )
								c3 = self.convertToFreeCADColor( int(self.o3E.text()) )

								color[index-1] = (c1, c2, c3, 0.0)
								self.gObj.ViewObject.DiffuseColor = color

								i = i + 1

					# get back base color
					self.gObj = refObj
					self.gFace = refFace
					self.gFaceIndex = refFaceIndex
				
			except:
			
				skip = 1

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def getSelected(self):

			try:

				self.gObjArr = []
				self.gFaceArr = dict()
				
				self.gObjArr = FreeCADGui.Selection.getSelection()

				i = 0
				for o in self.gObjArr:
					self.gFaceArr[o] = FreeCADGui.Selection.getSelectionEx()[i].SubObjects
					i = i + 1
			
				if len(self.gObjArr) == 1 and len(self.gFaceArr[self.gObjArr[0]]) == 1:
					
					self.gMode = "Face"
					self.gObj = self.gObjArr[0]
					self.gFace = self.gFaceArr[self.gObj][0]
					FreeCADGui.Selection.clearSelection()
					
					self.gFaceIndex = self.getFaceIndex()
					if self.gFaceIndex == -1:
						raise
					
					self.s1S.setText(str(self.gObj.Label)+", Face"+str(self.gFaceIndex))
					self.getColor()
					return 1
				
				if len(self.gObjArr) == 1 and len(self.gFaceArr[self.gObjArr[0]]) == 0:
					
					self.gMode = "Object"
					self.gObj = self.gObjArr[0]
					self.gFace = ""
					FreeCADGui.Selection.clearSelection()
					
					self.s1S.setText(str(self.gObj.Label))
					self.getColor()
					return 2
				
				if len(self.gObjArr) > 1 or len(self.gFaceArr[self.gObjArr[0]]) > 1:
					
					self.gMode = "Multi"
					self.gObj = self.gObjArr[0]
					try:
						self.gFace = self.gFaceArr[self.gObj][0]
						self.gFaceIndex = self.getFaceIndex()
						if self.gFaceIndex == -1:
							raise
					except:
						self.gFace = ""

					FreeCADGui.Selection.clearSelection()
					
					self.s1S.setText(str(self.gMode))
					self.getColor()
					return 3

				# something other not supported
				raise
				
			except:

				self.s1S.setText("please select objects or faces")
				return -1

		# ############################################################################
		def setColorO1B1(self):
			value = int(self.o1E.text())
			step = int(self.o4E.text())
			
			if value - step <= 0:
				value = 255
			else:
				value = value - step

			self.o1E.setText(str(value)) 
			self.setColor()

		def setColorO1B2(self):
			value = int(self.o1E.text())
			step = int(self.o4E.text())
			
			if value + step >= 255:
				value = 0
			else:
				value = value + step

			self.o1E.setText(str(value)) 
			self.setColor()
			
		def setColorO2B1(self):
			value = int(self.o2E.text())
			step = int(self.o4E.text())
			
			if value - step <= 0:
				value = 255
			else:
				value = value - step

			self.o2E.setText(str(value)) 
			self.setColor()		
		
		def setColorO2B2(self):
			value = int(self.o2E.text())
			step = int(self.o4E.text())
			
			if value + step >= 255:
				value = 0
			else:
				value = value + step

			self.o2E.setText(str(value)) 
			self.setColor()

		def setColorO3B1(self):
			value = int(self.o3E.text())
			step = int(self.o4E.text())
			
			if value - step <= 0:
				value = 255
			else:
				value = value - step

			self.o3E.setText(str(value)) 
			self.setColor()		
		
		def setColorO3B2(self):
			value = int(self.o3E.text())
			step = int(self.o4E.text())
			
			if value + step >= 255:
				value = 0
			else:
				value = value + step

			self.o3E.setText(str(value)) 
			self.setColor()

		# ############################################################################
		def setSheet(self):

			skip = 0
			sheet = ""

			try:
				sheet = FreeCAD.ActiveDocument.getObjectsByLabel("faceColors")[0]
			except:
				skip = 1
				
			if skip == 1:
				sheet = FreeCAD.ActiveDocument.addObject("Spreadsheet::Sheet","faceColors")

				sheet.set("A1",str("Face1"))
				sheet.set("A2",str("Face2"))
				sheet.set("A3",str("Face3"))
				sheet.set("A4",str("Face4"))
				sheet.set("A5",str("Face5"))
				sheet.set("A6",str("Face6"))

				sheet.set("B1",str("black"))
				sheet.set("B2",str("blue"))
				sheet.set("B3",str("red"))
				sheet.set("B4",str("yellow"))
				sheet.set("B5",str("white"))
				sheet.set("B6",str("green"))

				info = ""
				info += "The colorManager tool search all faces at object and try to read "
				info += "exact B row with color name. For example: for Face3 the color at B3 cell will be searched, "
				info += "for Face5 the color at B5 cell will be set. If there is no cell with color, this "
				info += "face will not be set. If you have Array object with 24 faces you need to set 24 rows. "
				info += "by default only first 6 faces will be set, usually it is base element. So you can quickly "
				info += "see where is the default element. You don't have to set A column, only B column is important "
				info += "for the tool. The A column is description for you. Currently only the 6 visible color names are "
				info += "supported. "
				
				sheet.mergeCells("C1:G6")
				sheet.set("D1", info)

				FreeCAD.ActiveDocument.recompute()

			# set colors from shpreadsheet
			for obj in FreeCAD.ActiveDocument.Objects:
				
				try:
					self.gObj = obj
					self.resetFaces()

					i = 1
					for f in self.gObj.Shape.Faces:
						
						try:
							faceColor = sheet.get("B"+str(i))
							color = self.gObj.ViewObject.DiffuseColor
							color[i-1] = self.convertFromName(str(faceColor))
							self.gObj.ViewObject.DiffuseColor = color
						except:
							skipFace = 1 # without color at exact sheet row
							
						i = i + 1 # go to next face
				except:
					skipObject = 1 # spreadsheet, group

			self.s1S.setText("colors from faceColors")

	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
