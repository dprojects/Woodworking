# ###################################################################################################################
'''

This colorManager macro allows to set face colors for all objects from spreadsheet. Also you can browse colors for 
manually selected faces or objects and see the effect at 3D model in real-time.

Note: This FreeCAD macro is part of Woodworking workbench. However, it can be used as standalone macro.

Author: Darek L (github.com/dprojects)
Latest version: https://github.com/dprojects/Woodworking/blob/master/Tools/colorManager.py

Certified platform:
https://github.com/dprojects/Woodworking

'''
# ###################################################################################################################


import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore

translate = FreeCAD.Qt.translate

# ############################################################################
# Global definitions
# ############################################################################

# add new items only at the end and change self.sColorsList
getMenuIndex = {
	"Select predefined color:": 0, 
	"reset": 1, 
	"Wood - white": 2, 
	"Wood - black": 3, 
	"Wood - pink": 4, 
	"Wood - plywood": 5, 
	"Wood - beech": 6, 
	"Wood - oak": 7, 
	"Wood - mahogany": 8, 
	"Wood 1": 9, 
	"Wood 2": 10, 
	"Wood 3": 11, 
	"Wood 4": 12, 
	"Wood 5": 13, 
	"Wood 6": 14, 
	"set colors from spreadsheet": 15, 
	"Wood - red": 16, 
	"Wood - green": 17, 
	"Wood - blue": 18
}

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
			toolSH = 280
			
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
			self.setWindowTitle(translate('colorManager', 'colorManager'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			row = 10
			
			# screen
			info = ""
			info += "                                             "
			info += "                                             "
			info += "                                             "
			self.s1S = QtGui.QLabel(info, self)
			self.s1S.move(10, row)

			row += 20
			
			# button
			self.s1B1 = QtGui.QPushButton(translate('colorManager', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(toolSW-20)
			self.s1B1.setFixedHeight(40)
			self.s1B1.move(10, row)

			# ############################################################################
			# options - predefined colors
			# ############################################################################

			row += 50

			# not write here, copy text from getMenuIndex to avoid typo
			self.sColorsList = (
						"Select predefined color:", 
						"reset", 
						"Wood - white", 
						"Wood - red", 
						"Wood - green", 
						"Wood - blue", 
						"Wood - black", 
						"Wood - pink", 
						"Wood - plywood", 
						"Wood - beech", 
						"Wood - oak", 
						"Wood - mahogany", 
						"Wood 1", 
						"Wood 2", 
						"Wood 3", 
						"Wood 4", 
						"Wood 5", 
						"Wood 6", 
						"set colors from spreadsheet" 
			)
			
			self.sColors = QtGui.QComboBox(self)
			self.sColors.addItems(self.sColorsList)
			self.sColors.setCurrentIndex(self.sColorsList.index("Select predefined color:"))
			self.sColors.activated[str].connect(self.setPredefinedColors)
			self.sColors.setFixedWidth(toolSW-20)
			self.sColors.move(10, row)

			# ############################################################################
			# options - red color
			# ############################################################################

			row += 30

			# label
			self.o1L = QtGui.QLabel(translate('colorManager', 'Select red:'), self)
			self.o1L.move(10, row+3)

			# button
			self.o1B1 = QtGui.QPushButton("<", self)
			self.o1B1.clicked.connect(self.setColorO1B1)
			self.o1B1.setFixedWidth(50)
			self.o1B1.move(100, row)
			self.o1B1.setAutoRepeat(True)
			
			# text input
			self.o1E = QtGui.QLineEdit(self)
			self.o1E.setText("")
			self.o1E.setFixedWidth(50)
			self.o1E.move(150, row)

			# button
			self.o1B2 = QtGui.QPushButton(">", self)
			self.o1B2.clicked.connect(self.setColorO1B2)
			self.o1B2.setFixedWidth(50)
			self.o1B2.move(200, row)
			self.o1B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - green color
			# ############################################################################

			row += 30
			
			# label
			self.o2L = QtGui.QLabel(translate('colorManager', 'Select green:'), self)
			self.o2L.move(10, row+3)

			# button
			self.o2B1 = QtGui.QPushButton("<", self)
			self.o2B1.clicked.connect(self.setColorO2B1)
			self.o2B1.setFixedWidth(50)
			self.o2B1.move(100, row)
			self.o2B1.setAutoRepeat(True)
			
			# text input
			self.o2E = QtGui.QLineEdit(self)
			self.o2E.setText("")
			self.o2E.setFixedWidth(50)
			self.o2E.move(150, row)

			# button
			self.o2B2 = QtGui.QPushButton(">", self)
			self.o2B2.clicked.connect(self.setColorO2B2)
			self.o2B2.setFixedWidth(50)
			self.o2B2.move(200, row)
			self.o2B2.setAutoRepeat(True)

			# ############################################################################
			# options - blue color
			# ############################################################################

			row += 30
			
			# label
			self.o3L = QtGui.QLabel(translate('colorManager', 'Select blue:'), self)
			self.o3L.move(10, row+3)

			# button
			self.o3B1 = QtGui.QPushButton("<", self)
			self.o3B1.clicked.connect(self.setColorO3B1)
			self.o3B1.setFixedWidth(50)
			self.o3B1.move(100, row)
			self.o3B1.setAutoRepeat(True)
			
			# text input
			self.o3E = QtGui.QLineEdit(self)
			self.o3E.setText("")
			self.o3E.setFixedWidth(50)
			self.o3E.move(150, row)

			# button
			self.o3B2 = QtGui.QPushButton(">", self)
			self.o3B2.clicked.connect(self.setColorO3B2)
			self.o3B2.setFixedWidth(50)
			self.o3B2.move(200, row)
			self.o3B2.setAutoRepeat(True)
			
			# ############################################################################
			# options - update color
			# ############################################################################

			row += 30
			
			# label
			self.o4L = QtGui.QLabel(translate('colorManager', 'Step:'), self)
			self.o4L.move(10, row+3)

			# text input
			self.o4E = QtGui.QLineEdit(self)
			self.o4E.setText(str(self.gStep))
			self.o4E.setFixedWidth(50)
			self.o4E.move(100, row)

			row += 30
			
			# update button
			self.o5B1 = QtGui.QPushButton(translate('colorManager', 'set custom color'), self)
			self.o5B1.clicked.connect(self.setColor)
			self.o5B1.setFixedWidth(toolSW-20)
			self.o5B1.setFixedHeight(40)
			self.o5B1.move(10, row)

			# ############################################################################
			# show & init defaults
			# ############################################################################

			row -= 120
			
			info = translate('colorManager', 'This button below will set face colors from spreadsheet for all objects in active document. If the faceColors spreadsheet is not available, it will be created. Make sure you want to overwrite existing colors for all objects. There is no undo option for that. ')
			
			self.sheetInfo = QtGui.QLabel(info, self)
			self.sheetInfo.setFixedWidth(toolSW-20)
			self.sheetInfo.move(10, row+3)
			self.sheetInfo.setWordWrap(True)
			
			row += 110
			
			# button
			self.sheetB1 = QtGui.QPushButton(translate('colorManager', 'set face colors from spreadsheet'), self)
			self.sheetB1.clicked.connect(self.setSheet)
			self.sheetB1.setFixedWidth(toolSW-20)
			self.sheetB1.setFixedHeight(40)
			self.sheetB1.move(10, row)

			# ############################################################################
			# show & init defaults
			# ############################################################################

			self.o1L.show()
			self.o1B1.show()
			self.o1E.show()
			self.o1B2.show()
			
			self.o2L.show()
			self.o2B1.show()
			self.o2E.show()
			self.o2B2.show()
			
			self.o3L.show()
			self.o3B1.show()
			self.o3E.show()
			self.o3B2.show()
			
			self.o4L.show()
			self.o4E.show()
			self.o5B1.show()
			
			self.sheetInfo.hide()
			self.sheetB1.hide()

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

			if len(self.gObj.ViewObject.DiffuseColor) == 1:
				resetColor = self.gObj.ViewObject.DiffuseColor[0]
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

				self.s1S.setText(translate('colorManager', 'please select objects or faces'))
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
				info += translate('colorManager', 'The colorManager tool search all faces at object and try to read exact B row with color name. For example: for Face3 the color at B3 cell will be searched, for Face5 the color at B5 cell will be set. If there is no cell with color, this face will not be set. If you have Array object with 24 faces you need to set 24 rows. By default only first 6 faces will be set, usually it is base element. So you can quickly see where is the default element. You do not have to set A column, only B column is important for the tool. The A column is description for you. Currently only the 6 visible color names are supported.')
				
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

			self.s1S.setText(translate('colorManager', 'colors from faceColors'))

		# ############################################################################
		def setPredefinedColors(self, selectedText):
			
			selectedIndex = getMenuIndex[selectedText]
			
			self.o1L.show()
			self.o1B1.show()
			self.o1E.show()
			self.o1B2.show()
			
			self.o2L.show()
			self.o2B1.show()
			self.o2E.show()
			self.o2B2.show()
			
			self.o3L.show()
			self.o3B1.show()
			self.o3E.show()
			self.o3B2.show()
			
			self.o4L.show()
			self.o4E.show()
			self.o5B1.show()
			
			self.sheetInfo.hide()
			self.sheetB1.hide()
			
			if selectedIndex == 1:
				self.o1E.setText("204")
				self.o2E.setText("204")
				self.o3E.setText("204")
				self.setColor()
			
			if selectedIndex == 2:
				self.o1E.setText("255")
				self.o2E.setText("255")
				self.o3E.setText("255")
				self.setColor()
			
			if selectedIndex == 3:
				self.o1E.setText("0")
				self.o2E.setText("0")
				self.o3E.setText("0")
				self.setColor()
			
			if selectedIndex == 4:
				self.o1E.setText("255")
				self.o2E.setText("0")
				self.o3E.setText("255")
				self.setColor()
				
			if selectedIndex == 5:
				self.o1E.setText("222")
				self.o2E.setText("184")
				self.o3E.setText("135")
				self.setColor()
		
			if selectedIndex == 6:
				self.o1E.setText("247")
				self.o2E.setText("185")
				self.o3E.setText("108")
				self.setColor()

			if selectedIndex == 7:
				self.o1E.setText("174")
				self.o2E.setText("138")
				self.o3E.setText("105")
				self.setColor()
				
			if selectedIndex == 8:
				self.o1E.setText("175")
				self.o2E.setText("91")
				self.o3E.setText("76")
				self.setColor()
				
			if selectedIndex == 9:
				self.o1E.setText("205")
				self.o2E.setText("170")
				self.o3E.setText("125")
				self.setColor()
		
			if selectedIndex == 10:
				self.o1E.setText("207")
				self.o2E.setText("141")
				self.o3E.setText("91")
				self.setColor()
		
			if selectedIndex == 11:
				self.o1E.setText("163")
				self.o2E.setText("104")
				self.o3E.setText("70")
				self.setColor()
				
			if selectedIndex == 12:
				self.o1E.setText("125")
				self.o2E.setText("83")
				self.o3E.setText("62")
				self.setColor()
		
			if selectedIndex == 13:
				self.o1E.setText("68")
				self.o2E.setText("48")
				self.o3E.setText("40")
				self.setColor()
		
			if selectedIndex == 14:
				self.o1E.setText("63")
				self.o2E.setText("25")
				self.o3E.setText("17")
				self.setColor()
			
			if selectedIndex == 15:
				
				self.o1L.hide()
				self.o1B1.hide()
				self.o1E.hide()
				self.o1B2.hide()
				
				self.o2L.hide()
				self.o2B1.hide()
				self.o2E.hide()
				self.o2B2.hide()
				
				self.o3L.hide()
				self.o3B1.hide()
				self.o3E.hide()
				self.o3B2.hide()
				
				self.o4L.hide()
				self.o4E.hide()
				self.o5B1.hide()
				
				self.sheetInfo.show()
				self.sheetB1.show()
			
			if selectedIndex == 16:
				self.o1E.setText("255")
				self.o2E.setText("0")
				self.o3E.setText("0")
				self.setColor()
			
			if selectedIndex == 17:
				self.o1E.setText("0")
				self.o2E.setText("255")
				self.o3E.setText("0")
				self.setColor()
			
			if selectedIndex == 18:
				self.o1E.setText("0")
				self.o2E.setText("0")
				self.o3E.setText("255")
				self.setColor()
				
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
