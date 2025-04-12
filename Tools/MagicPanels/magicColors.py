import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore
import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# Global definitions
# ############################################################################

# add new items only at the end and change self.sTargetsList
getMenuIndex1 = {
	translate('magicColors', 'Select target property:'): 0, 
	translate('magicColors', 'DiffuseColor'): 1, 
	translate('magicColors', 'Transparency'): 2, 
	translate('magicColors', 'AmbientColor'): 3, 
	translate('magicColors', 'EmissiveColor'): 4, 
	translate('magicColors', 'Shininess'): 5, 
	translate('magicColors', 'SpecularColor'): 6 # no comma
}

# add new items only at the end and change self.sColorsList
getMenuIndex2 = {
	translate('magicColors', 'custom'): 0, 
	translate('magicColors', 'reset'): 1, 
	translate('magicColors', 'Wood - white'): 2, 
	translate('magicColors', 'Wood - black'): 3, 
	translate('magicColors', 'Wood - pink'): 4, 
	translate('magicColors', 'Wood - plywood'): 5, 
	translate('magicColors', 'Wood - beech'): 6, 
	translate('magicColors', 'Wood - oak'): 7, 
	translate('magicColors', 'Wood - mahogany'): 8, 
	translate('magicColors', 'Wood 1'): 9, 
	translate('magicColors', 'Wood 2'): 10, 
	translate('magicColors', 'Wood 3'): 11, 
	translate('magicColors', 'Wood 4'): 12, 
	translate('magicColors', 'Wood 5'): 13, 
	translate('magicColors', 'Wood 6'): 14, 
	translate('magicColors', 'from spreadsheet'): 15, 
	translate('magicColors', 'Wood - red'): 16, 
	translate('magicColors', 'Wood - green'): 17, 
	translate('magicColors', 'Wood - blue'): 18, 
	translate('magicColors', 'Woodworking - default'): 19  # no comma
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
		gStepAlpha = 0.10
		gStepSingle = 0.10
		gColorTarget = "DiffuseColor"
		gColorToSet = 0
		gKernelVersion = MagicPanels.gKernelVersion
		
		# ############################################################################
		# screen settings
		# ############################################################################

		# tool GUI size
		toolSW = 320
		toolSH = 430
		
		# active screen size - FreeCAD main window
		gSW = FreeCADGui.getMainWindow().width()
		gSH = FreeCADGui.getMainWindow().height()

		# tool screen position
		gPW = int( gSW - toolSW )
		gPH = int( gSH - toolSH )
		
		# ############################################################################
		# init
		# ############################################################################

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):

			# ############################################################################
			# settings
			# ############################################################################

			size = 50
			offset = 10
			
			col3 = self.toolSW - 10 - size
			col2 = col3 - offset - size
			col1 = col2 - offset - size

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(self.gPW, self.gPH, self.toolSW, self.toolSH)
			self.setWindowTitle(translate('magicColors', 'magicColors'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection mode
			# ############################################################################
			
			row = 10
			
			# screen
			self.s1S = QtGui.QLabel("", self)
			self.s1S.setFixedWidth(self.toolSW-20)
			self.s1S.move(10, row)

			row += 20
			
			# button
			self.s1B1 = QtGui.QPushButton(translate('magicColors', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(self.toolSW-20)
			self.s1B1.setFixedHeight(40)
			self.s1B1.move(10, row)

			# ############################################################################
			# options - target attribute
			# ############################################################################

			row += 50

			# label
			self.sTargetsL = QtGui.QLabel(translate('magicColors', 'Color property:'), self)
			self.sTargetsL.setFixedWidth(col1-offset)
			self.sTargetsL.move(10, row+13)

			# not write here, copy text from getMenuIndex1 to avoid typo
			
			if self.gKernelVersion >= 1.0:
				
				self.sTargetsList = (
					translate('magicColors', 'DiffuseColor'), 
					translate('magicColors', 'AmbientColor'), 
					translate('magicColors', 'EmissiveColor'), 
					translate('magicColors', 'SpecularColor'), 
					translate('magicColors', 'Shininess'), 
					translate('magicColors', 'Transparency') # no comma
				)
			
			else:
			
				self.sTargetsList = (
					translate('magicColors', 'DiffuseColor'), 
					translate('magicColors', 'Transparency') # no comma
				)
				
			self.sTargets = QtGui.QComboBox(self)
			self.sTargets.addItems(self.sTargetsList)
			self.sTargets.setCurrentIndex(0)
			self.sTargets.textActivated[str].connect(self.setTargetProperty)
			self.sTargets.setFixedWidth(self.toolSW-col1-10)
			self.sTargets.setFixedHeight(40)
			self.sTargets.move(col1, row)

			# ############################################################################
			# options - predefined colors
			# ############################################################################

			row += 50

			# label
			self.sColorsL = QtGui.QLabel(translate('magicColors', 'Predefined schema:'), self)
			self.sColorsL.setFixedWidth(col1-offset)
			self.sColorsL.move(10, row+13)

			# not write here, copy text from getMenuIndex2 to avoid typo
			self.sColorsList = (
				translate('magicColors', 'custom'), 
				translate('magicColors', 'Woodworking - default'), 
				translate('magicColors', 'reset'), 
				translate('magicColors', 'Wood - white'), 
				translate('magicColors', 'Wood - red'), 
				translate('magicColors', 'Wood - green'), 
				translate('magicColors', 'Wood - blue'), 
				translate('magicColors', 'Wood - black'), 
				translate('magicColors', 'Wood - pink'), 
				translate('magicColors', 'Wood - plywood'), 
				translate('magicColors', 'Wood - beech'), 
				translate('magicColors', 'Wood - oak'), 
				translate('magicColors', 'Wood - mahogany'), 
				translate('magicColors', 'Wood 1'), 
				translate('magicColors', 'Wood 2'), 
				translate('magicColors', 'Wood 3'), 
				translate('magicColors', 'Wood 4'), 
				translate('magicColors', 'Wood 5'), 
				translate('magicColors', 'Wood 6'), 
				translate('magicColors', 'from spreadsheet') # no comma
			)
			
			self.sColors = QtGui.QComboBox(self)
			self.sColors.addItems(self.sColorsList)
			self.sColors.setCurrentIndex(0)
			self.sColors.textActivated[str].connect(self.setPredefinedColors)
			self.sColors.setFixedWidth(self.toolSW-col1-10)
			self.sColors.setFixedHeight(40)
			self.sColors.move(col1, row)

			# ############################################################################
			# radio buttons
			# ############################################################################
			
			row += 50
			
			self.rb1 = QtGui.QRadioButton(self)
			self.rb1.setText(translate('magicColors', 'simple buttons'))
			self.rb1.toggled.connect(self.selectRadioButton1)
			self.rb1.move(10, row)
			
			self.rb2 = QtGui.QRadioButton(self)
			self.rb2.setText(translate('magicColors', 'extended live chooser'))
			self.rb2.toggled.connect(self.selectRadioButton2)
			self.rb2.move(140, row)
			self.rb1.setChecked(False)
			
			# ############################################################################
			# options - settings
			# ############################################################################

			row += 50
			rowSingle = row
			rowChooser = row
		
			# ############################################################################
			# options - red color
			# ############################################################################

			# label
			self.oRedL = QtGui.QLabel(translate('magicColors', 'Set red color:'), self)
			self.oRedL.move(10, row+3)

			# button
			self.oRedB1 = QtGui.QPushButton("-", self)
			self.oRedB1.clicked.connect(self.setColorRedB1)
			self.oRedB1.setFixedWidth(size)
			self.oRedB1.move(col1, row)
			self.oRedB1.setAutoRepeat(True)
			
			# text input
			self.oRedE = QtGui.QLineEdit(self)
			self.oRedE.setText("")
			self.oRedE.setFixedWidth(size)
			self.oRedE.move(col2, row)

			# button
			self.oRedB2 = QtGui.QPushButton("+", self)
			self.oRedB2.clicked.connect(self.setColorRedB2)
			self.oRedB2.setFixedWidth(size)
			self.oRedB2.move(col3, row)
			self.oRedB2.setAutoRepeat(True)
			
			# ############################################################################
			# options - green color
			# ############################################################################

			row += 30
			
			# label
			self.oGreenL = QtGui.QLabel(translate('magicColors', 'Set green color:'), self)
			self.oGreenL.move(10, row+3)

			# button
			self.oGreenB1 = QtGui.QPushButton("-", self)
			self.oGreenB1.clicked.connect(self.setColorGreenB1)
			self.oGreenB1.setFixedWidth(size)
			self.oGreenB1.move(col1, row)
			self.oGreenB1.setAutoRepeat(True)
			
			# text input
			self.oGreenE = QtGui.QLineEdit(self)
			self.oGreenE.setText("")
			self.oGreenE.setFixedWidth(size)
			self.oGreenE.move(col2, row)

			# button
			self.oGreenB2 = QtGui.QPushButton("+", self)
			self.oGreenB2.clicked.connect(self.setColorGreenB2)
			self.oGreenB2.setFixedWidth(size)
			self.oGreenB2.move(col3, row)
			self.oGreenB2.setAutoRepeat(True)

			# ############################################################################
			# options - blue color
			# ############################################################################

			row += 30
			
			# label
			self.oBlueL = QtGui.QLabel(translate('magicColors', 'Set blue color:'), self)
			self.oBlueL.move(10, row+3)

			# button
			self.oBlueB1 = QtGui.QPushButton("-", self)
			self.oBlueB1.clicked.connect(self.setColorBlueB1)
			self.oBlueB1.setFixedWidth(size)
			self.oBlueB1.move(col1, row)
			self.oBlueB1.setAutoRepeat(True)
			
			# text input
			self.oBlueE = QtGui.QLineEdit(self)
			self.oBlueE.setText("")
			self.oBlueE.setFixedWidth(size)
			self.oBlueE.move(col2, row)

			# button
			self.oBlueB2 = QtGui.QPushButton("+", self)
			self.oBlueB2.clicked.connect(self.setColorBlueB2)
			self.oBlueB2.setFixedWidth(size)
			self.oBlueB2.move(col3, row)
			self.oBlueB2.setAutoRepeat(True)
			
			# ############################################################################
			# options - alpha
			# ############################################################################

			row += 30
			
			# label
			self.oAlphaL = QtGui.QLabel(translate('magicColors', 'Set alpha channel:'), self)
			self.oAlphaL.move(10, row+3)

			# button
			self.oAlphaB1 = QtGui.QPushButton("-", self)
			self.oAlphaB1.clicked.connect(self.setColorAlphaB1)
			self.oAlphaB1.setFixedWidth(size)
			self.oAlphaB1.move(col1, row)
			self.oAlphaB1.setAutoRepeat(True)
			
			# text input
			self.oAlphaE = QtGui.QLineEdit(self)
			self.oAlphaE.setText("")
			self.oAlphaE.setFixedWidth(size)
			self.oAlphaE.move(col2, row)

			# button
			self.oAlphaB2 = QtGui.QPushButton("+", self)
			self.oAlphaB2.clicked.connect(self.setColorAlphaB2)
			self.oAlphaB2.setFixedWidth(size)
			self.oAlphaB2.move(col3, row)
			self.oAlphaB2.setAutoRepeat(True)
			
			# ############################################################################
			# options - shininess
			# ############################################################################

			# label
			self.oShineL = QtGui.QLabel(translate('magicColors', 'Shininess:'), self)
			self.oShineL.move(10, rowSingle+3)

			# button
			self.oShineB1 = QtGui.QPushButton("-", self)
			self.oShineB1.clicked.connect(self.setColorShineB1)
			self.oShineB1.setFixedWidth(size)
			self.oShineB1.move(col1, rowSingle)
			self.oShineB1.setAutoRepeat(True)
			
			# text input
			self.oShineE = QtGui.QLineEdit(self)
			self.oShineE.setText("")
			self.oShineE.setFixedWidth(size)
			self.oShineE.move(col2, rowSingle)

			# button
			self.oShineB2 = QtGui.QPushButton("+", self)
			self.oShineB2.clicked.connect(self.setColorShineB2)
			self.oShineB2.setFixedWidth(size)
			self.oShineB2.move(col3, rowSingle)
			self.oShineB2.setAutoRepeat(True)
			
			# hide by default
			self.oShineL.hide()
			self.oShineB1.hide()
			self.oShineE.hide()
			self.oShineB2.hide()

			# ############################################################################
			# options - transparency
			# ############################################################################

			# label
			self.oTransL = QtGui.QLabel(translate('magicColors', 'Transparency:'), self)
			self.oTransL.move(10, rowSingle+3)

			# button
			self.oTransB1 = QtGui.QPushButton("-", self)
			self.oTransB1.clicked.connect(self.setColorTransB1)
			self.oTransB1.setFixedWidth(size)
			self.oTransB1.move(col1, rowSingle)
			self.oTransB1.setAutoRepeat(True)
			
			# text input
			self.oTransE = QtGui.QLineEdit(self)
			self.oTransE.setText("")
			self.oTransE.setFixedWidth(size)
			self.oTransE.move(col2, rowSingle)

			# button
			self.oTransB2 = QtGui.QPushButton("+", self)
			self.oTransB2.clicked.connect(self.setColorTransB2)
			self.oTransB2.setFixedWidth(size)
			self.oTransB2.move(col3, rowSingle)
			self.oTransB2.setAutoRepeat(True)
			
			# hide by default
			self.oTransL.hide()
			self.oTransB1.hide()
			self.oTransE.hide()
			self.oTransB2.hide()
			
			# ############################################################################
			# options - step
			# ############################################################################

			row += 30
			
			# label
			self.oStepL1 = QtGui.QLabel(translate('magicColors', 'Set step:'), self)
			self.oStepL1.move(10, row+3)
			
			# label
			self.oStepL2 = QtGui.QLabel(translate('magicColors', 'RGB:'), self)
			self.oStepL2.move(col1-offset-30, row+3)
			
			# text input
			self.oStepE = QtGui.QLineEdit(self)
			self.oStepE.setText(str(self.gStep))
			self.oStepE.setFixedWidth(size)
			self.oStepE.move(col1, row)
			
			# label
			self.oStepAlphaL = QtGui.QLabel(translate('magicColors', 'Alpha:'), self)
			self.oStepAlphaL.move(col3-offset-40, row+3)

			# text input
			self.oStepAlphaE = QtGui.QLineEdit(self)
			self.oStepAlphaE.setText(str(self.gStepAlpha))
			self.oStepAlphaE.setFixedWidth(size)
			self.oStepAlphaE.move(col3, row)
			
			rowSingle += 30
			
			# label
			self.oStepSingleL = QtGui.QLabel(translate('magicColors', 'Step:'), self)
			self.oStepSingleL.move(10, rowSingle+3)

			# text input
			self.oStepSingleE = QtGui.QLineEdit(self)
			self.oStepSingleE.setText(str(self.gStepSingle))
			self.oStepSingleE.setFixedWidth(size)
			self.oStepSingleE.move(col1, rowSingle)
			
			# hide by default
			self.oStepSingleL.hide()
			self.oStepSingleE.hide()
			
			# ############################################################################
			# options - update color
			# ############################################################################

			row += 30
			
			# update button
			self.oCustomB = QtGui.QPushButton(translate('magicColors', 'set custom color'), self)
			self.oCustomB.clicked.connect(self.setColor)
			self.oCustomB.setFixedWidth(self.toolSW-20)
			self.oCustomB.setFixedHeight(40)
			self.oCustomB.move(10, row)

			# ############################################################################
			# show & init defaults
			# ############################################################################

			row -= 120
			
			info = translate('magicColors', 'This button below will set face colors from spreadsheet for all objects in active document. If the faceColors spreadsheet is not available, it will be created. Make sure you want to overwrite existing colors for all objects. There is no undo option for that. ')
			
			self.sheetInfo = QtGui.QLabel(info, self)
			self.sheetInfo.setFixedWidth(self.toolSW-20)
			self.sheetInfo.move(10, row+3)
			self.sheetInfo.setWordWrap(True)
			self.sheetInfo.hide()

			row += 110
			
			# button
			self.sheetB1 = QtGui.QPushButton(translate('magicColors', 'set face colors from spreadsheet'), self)
			self.sheetB1.clicked.connect(self.setSheet)
			self.sheetB1.setFixedWidth(self.toolSW-20)
			self.sheetB1.setFixedHeight(40)
			self.sheetB1.move(10, row)
			self.sheetB1.hide()

			# ############################################################################
			# real-time color chooser
			# ############################################################################
			
			row += 50

			self.rtcc = QtGui.QColorDialog("",self)
			self.rtcc.blockSignals(True)
			self.rtcc.currentColorChanged.connect(self.getColorFromChooser)
			self.rtcc.blockSignals(False)
			self.rtcc.move(10, rowChooser)
			self.rtcc.setOption(QtGui.QColorDialog.ColorDialogOption.NoButtons, True)
			self.rtcc.setOption(QtGui.QColorDialog.ColorDialogOption.ShowAlphaChannel, True)
			self.rtcc.setWindowFlags(QtCore.Qt.SubWindow)
			
			# hide by default
			self.rtcc.hide()

			# ############################################################################
			# show & init defaults
			# ############################################################################
	
			# show window
			self.show()
			self.rb1.setChecked(True)

			# init
			self.getSelected()

		# ############################################################################
		# actions - internal functions
		# ############################################################################

		def getColorFromChooser(self, color):
	
			self.oRedE.setText(str( int(color.red()) ))
			self.oGreenE.setText(str( int(color.green()) ))
			self.oBlueE.setText(str( int(color.blue()) ))
			self.oAlphaE.setText(str( int(color.alphaF()) ))
			
			self.oShineE.setText(str( round( float( color.valueF() ), 2) ))
			self.oTransE.setText(str( round( float( color.valueF() ), 2) ))
			
			self.setColor()

		# ############################################################################
		def convertToRGB(self, iColor):
			return int(255 * iColor)

		# ############################################################################
		def convertToFreeCADColor(self, iColor):
			return float(iColor/255)

		# ############################################################################
		def convertFromName(self, iColor):
		
			if iColor == "blue":
				return (0.3333333432674408, 0.0, 1.0, 1.0)
		
			if iColor == "black":
				return (0.0, 0.0, 0.0, 1.0)
		
			if iColor == "red":
				return (1.0, 0.0, 0.0, 1.0)
		
			if iColor == "yellow":
				return (1.0, 1.0, 0.0, 1.0)
		
			if iColor == "white":
				return (1.0, 1.0, 1.0, 1.0)
		
			if iColor == "green":
				return (0.0, 1.0, 0.0, 1.0)
		
			return (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)

		# ############################################################################
		def getColor(self):

			try:
				if self.gMode == "Face":
					self.gColorToSet = MagicPanels.getColor(self.gObj, self.gFaceIndex, self.gColorTarget)

				if self.gMode == "Object":
					self.gColorToSet = MagicPanels.getColor(self.gObj, 0, self.gColorTarget)

				if self.gMode == "Multi":

					# first face selected
					if self.gFace == "":
						self.gColorToSet = MagicPanels.getColor(self.gObj, self.gFaceIndex, self.gColorTarget)

					# first object selected, no face
					else:
						self.gColorToSet = MagicPanels.getColor(self.gObj, 0, self.gColorTarget)
				
				if self.gColorTarget == "Shininess":
					
					if self.gColorToSet == "":
						color = 0.0
					else:
						color = round(float(self.gColorToSet), 2)
						
					self.oShineE.setText(str(color))

				elif self.gColorTarget == "Transparency":
					
					if self.gColorToSet == "":
						color = 1.0
					else:
						color = round(float(self.gColorToSet), 2)
						
					self.oTransE.setText(str(color))
				
				else:
					color = self.gColorToSet
					if self.gColorToSet == "":
						[ r, g, b, a ] = [ 0.0, 0.0, 0.0, 1.0 ]
					else:
						[ r, g, b, a ] = [ color[0], color[1], color[2], color[3] ]

					# set GUI form with RGB color values
					cR = self.convertToRGB(r)
					cG = self.convertToRGB(g)
					cB = self.convertToRGB(b)
					cA = round(float(a), 2)

					self.oRedE.setText(str(cR))
					self.oGreenE.setText(str(cG))
					self.oBlueE.setText(str(cB))
					self.oAlphaE.setText(str(cA))

			except:
				self.s1S.setText(translate('magicColors', 'please select objects or faces'))
				return -1
				
		# ############################################################################
		def setColor(self):

			try:
				# create color
				if self.gColorTarget == "Shininess":
					self.gColorToSet = round(float( self.oShineE.text() ), 2)
				
				elif self.gColorTarget == "Transparency":
					if MagicPanels.gKernelVersion >= 1.0:
						self.gColorToSet = round( float(self.oTransE.text()), 2 )
					else:
						self.gColorToSet = int( float(self.oTransE.text()) * 100)
				else:
					c1 = self.convertToFreeCADColor( int(self.oRedE.text()) )
					c2 = self.convertToFreeCADColor( int(self.oGreenE.text()) )
					c3 = self.convertToFreeCADColor( int(self.oBlueE.text()) )
					cA = round(float(self.oAlphaE.text()), 2)
					
					self.gColorToSet = (c1, c2, c3, cA)

				# setting color
				if self.gMode == "Face":
					MagicPanels.setColor(self.gObj, self.gFaceIndex, self.gColorToSet, self.gColorTarget)

				if self.gMode == "Object":
					MagicPanels.setColor(self.gObj, 0, self.gColorToSet, self.gColorTarget)

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
							MagicPanels.setColor(self.gObj, 0, self.gColorToSet, self.gColorTarget)

						# faces selected for object
						else:

							i = 0
							for f in self.gFaceArr[o]:

								# set current face for other functions
								self.gFace = self.gFaceArr[o][i]
								self.gFaceIndex = MagicPanels.getFaceIndex(self.gObj, self.gFace)
							
								MagicPanels.setColor(self.gObj, self.gFaceIndex, self.gColorToSet, self.gColorTarget)

								i = i + 1

					# get back base color
					self.gObj = refObj
					self.gFace = refFace
					self.gFaceIndex = refFaceIndex
					
				FreeCAD.ActiveDocument.recompute()

			except:
				self.s1S.setText(translate('magicColors', 'please select objects or faces'))
				return -1

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
					
					self.gFaceIndex = MagicPanels.getFaceIndex(self.gObj, self.gFace)
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
						self.gFaceIndex = MagicPanels.getFaceIndex(self.gObj, self.gFace)
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

				self.s1S.setText(translate('magicColors', 'please select objects or faces'))
				return -1

		# ############################################################################
		def setColorRedB1(self):
			value = int(self.oRedE.text())
			step = int(self.oStepE.text())
			
			if value - step <= 0:
				value = 255
			else:
				value = value - step

			self.oRedE.setText(str(value)) 
			self.setColor()

		def setColorRedB2(self):
			value = int(self.oRedE.text())
			step = int(self.oStepE.text())
			
			if value + step >= 255:
				value = 0
			else:
				value = value + step

			self.oRedE.setText(str(value)) 
			self.setColor()
			
		def setColorGreenB1(self):
			value = int(self.oGreenE.text())
			step = int(self.oStepE.text())
			
			if value - step <= 0:
				value = 255
			else:
				value = value - step

			self.oGreenE.setText(str(value)) 
			self.setColor()
		
		def setColorGreenB2(self):
			value = int(self.oGreenE.text())
			step = int(self.oStepE.text())
			
			if value + step >= 255:
				value = 0
			else:
				value = value + step

			self.oGreenE.setText(str(value)) 
			self.setColor()

		def setColorBlueB1(self):
			value = int(self.oBlueE.text())
			step = int(self.oStepE.text())
			
			if value - step <= 0:
				value = 255
			else:
				value = value - step

			self.oBlueE.setText(str(value)) 
			self.setColor()
		
		def setColorBlueB2(self):
			value = int(self.oBlueE.text())
			step = int(self.oStepE.text())
			
			if value + step >= 255:
				value = 0
			else:
				value = value + step

			self.oBlueE.setText(str(value)) 
			self.setColor()
		
		def setColorAlphaB1(self):
			value = float(self.oAlphaE.text())
			step = float(self.oStepAlphaE.text())
			
			if value - step <= 0:
				value = 1
			else:
				value = value - step

			self.oAlphaE.setText(str(round(float(value), 2)))
			self.setColor()
		
		def setColorAlphaB2(self):
			value = float(self.oAlphaE.text())
			step = float(self.oStepAlphaE.text())
			
			if value + step >= 1:
				value = 0
			else:
				value = value + step

			self.oAlphaE.setText(str(round(float(value), 2)))
			self.setColor()
		
		def setColorShineB1(self):
			value = float(self.oShineE.text())
			step = float(self.oStepSingleE.text())
			
			if value - step <= 0:
				value = 1
			else:
				value = value - step

			self.oShineE.setText(str(round(float(value), 2))) 
			self.setColor()
		
		def setColorShineB2(self):
			value = float(self.oShineE.text())
			step = float(self.oStepSingleE.text())
			
			if value + step >= 1:
				value = 0
			else:
				value = value + step

			self.oShineE.setText(str(round(float(value), 2))) 
			self.setColor()

		def setColorTransB1(self):
			value = float(self.oTransE.text())
			step = float(self.oStepSingleE.text())
			
			if value - step <= 0:
				value = 1
			else:
				value = value - step

			self.oTransE.setText(str(round(float(value), 2)))
			self.setColor()
		
		def setColorTransB2(self):
			value = float(self.oTransE.text())
			step = float(self.oStepSingleE.text())
			
			if value + step >= 1:
				value = 0
			else:
				value = value + step

			self.oTransE.setText(str(round(float(value), 2)))
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
				info += translate('magicColors', 'The tool search all faces at object and try to read exact B row with color name. For example: for Face3 the color at B3 cell will be searched, for Face5 the color at B5 cell will be set. If there is no cell with color, this face will not be set. If you have Array object with 24 faces you need to set 24 rows. By default only first 6 faces will be set, usually it is base element. So you can quickly see where is the default element. You do not have to set A column, only B column is important for the tool. The A column is description for you. Currently only the 6 visible color names are supported.')
				
				sheet.mergeCells("C1:G6")
				sheet.set("D1", info)

				FreeCAD.ActiveDocument.recompute()

			# set colors from shpreadsheet
			for obj in FreeCAD.ActiveDocument.Objects:
				
				try:
					self.gObj = obj
					
					i = 1
					for f in self.gObj.Shape.Faces:
						
						try:
							faceColor = sheet.get("B"+str(i))
							color = self.convertFromName(str(faceColor))
							MagicPanels.setColor(self.gObj, i, color, "DiffuseColor")
						except:
							skipFace = 1 # without color at exact sheet row
							
						i = i + 1 # go to next face
				except:
					skipObject = 1 # spreadsheet, group

			self.s1S.setText(translate('magicColors', 'colors from faceColors'))

		# ############################################################################
		def showDefaultGUI(self):
			
			self.oRedL.show()
			self.oRedB1.show()
			self.oRedE.show()
			self.oRedB2.show()
			
			self.oGreenL.show()
			self.oGreenB1.show()
			self.oGreenE.show()
			self.oGreenB2.show()
			
			self.oBlueL.show()
			self.oBlueB1.show()
			self.oBlueE.show()
			self.oBlueB2.show()
			
			self.oAlphaL.show()
			self.oAlphaB1.show()
			self.oAlphaE.show()
			self.oAlphaB2.show()
			
			self.oShineL.hide()
			self.oShineB1.hide()
			self.oShineE.hide()
			self.oShineB2.hide()
			
			self.oTransL.hide()
			self.oTransB1.hide()
			self.oTransE.hide()
			self.oTransB2.hide()
			
			self.oStepL1.show()
			self.oStepL2.show()
			self.oStepE.show()
			self.oStepAlphaL.show()
			self.oStepAlphaE.show()
			
			self.oStepSingleL.hide()
			self.oStepSingleE.hide()

			self.oCustomB.show()
			
			self.sheetInfo.hide()
			self.sheetB1.hide()
		
		# ############################################################################
		def hideGUI(self):
			
			self.oRedL.hide()
			self.oRedB1.hide()
			self.oRedE.hide()
			self.oRedB2.hide()
			
			self.oGreenL.hide()
			self.oGreenB1.hide()
			self.oGreenE.hide()
			self.oGreenB2.hide()
			
			self.oBlueL.hide()
			self.oBlueB1.hide()
			self.oBlueE.hide()
			self.oBlueB2.hide()
			
			self.oAlphaL.hide()
			self.oAlphaB1.hide()
			self.oAlphaE.hide()
			self.oAlphaB2.hide()
			
			self.oShineL.hide()
			self.oShineB1.hide()
			self.oShineE.hide()
			self.oShineB2.hide()
			
			self.oTransL.hide()
			self.oTransB1.hide()
			self.oTransE.hide()
			self.oTransB2.hide()
			
			self.oStepL1.hide()
			self.oStepL2.hide()
			self.oStepE.hide()
			self.oStepAlphaL.hide()
			self.oStepAlphaE.hide()
			
			self.oStepSingleL.hide()
			self.oStepSingleE.hide()

			self.oCustomB.hide()
			
			self.sheetInfo.hide()
			self.sheetB1.hide()

		# ############################################################################
		def setTargetProperty(self, selectedText):
			
			# get current index
			selectedIndex = getMenuIndex1[selectedText]
			
			# set color target, do not get it from translation
			if selectedIndex == 0:
				self.gColorTarget = "DiffuseColor"
				self.getColor()
			
			if selectedIndex == 1:
				self.gColorTarget = "DiffuseColor"
				self.getColor()
				
			if selectedIndex == 2:
				self.gColorTarget = "Transparency"
				self.getColor()
				
			if selectedIndex == 3:
				self.gColorTarget = "AmbientColor"
				self.getColor()
				
			if selectedIndex == 4:
				self.gColorTarget = "EmissiveColor"
				self.getColor()
				
			if selectedIndex == 5:
				self.gColorTarget = "Shininess"
				self.getColor()
				
			if selectedIndex == 6:
				self.gColorTarget = "SpecularColor"
				self.getColor()
		
			# if real-time chooser is selected not switch GUI
			if self.rb2.isChecked() == True:
				return ""
			
			# set default GUI
			self.showDefaultGUI()
			
			# actions for selected item
			if selectedIndex == 5:
				
				self.hideGUI()

				self.oShineL.show()
				self.oShineB1.show()
				self.oShineE.show()
				self.oShineB2.show()

				self.oStepSingleL.show()
				self.oStepSingleE.show()
				
				self.oCustomB.show()

			if selectedIndex == 2:
				
				self.hideGUI()
				
				self.oTransL.show()
				self.oTransB1.show()
				self.oTransE.show()
				self.oTransB2.show()
				
				self.oStepSingleL.show()
				self.oStepSingleE.show()
				
				self.oCustomB.show()
		
			# set predefined schema to default state
			self.sColors.setCurrentIndex(0)
			
		# ############################################################################
		def setPredefinedColors(self, selectedText):
			
			# get selection index and set screen size
			selectedIndex = getMenuIndex2[selectedText]
			
			# set default color structure, [ RGB int, alpha float ]
			Material = { 
				"DiffuseColor": [ 204, 204, 204, 1.0 ], 
				"AmbientColor": [ 85, 85, 85, 1.0 ], 
				"SpecularColor": [ 136, 136, 136, 1.0 ], 
				"EmissiveColor": [ 0, 0, 0, 1.0 ], 
				"Shininess": 0.9, 
				"Transparency": 0.0 # no comma
			}

			if selectedIndex == 2:
				Material["DiffuseColor"] = [ 255, 255, 255, 1.0 ]

			if selectedIndex == 3:
				Material["DiffuseColor"] = [ 0, 0, 0, 1.0 ]
			
			if selectedIndex == 4:
				Material["DiffuseColor"] = [ 255, 0, 255, 1.0 ]

			if selectedIndex == 5:
				Material["DiffuseColor"] = [ 222, 184, 135, 1.0 ]
		
			if selectedIndex == 6:
				Material["DiffuseColor"] = [ 247, 185, 108, 1.0 ]

			if selectedIndex == 7:
				Material["DiffuseColor"] = [ 174, 138, 105, 1.0 ]

			if selectedIndex == 8:
				Material["DiffuseColor"] = [ 175, 91, 76, 1.0 ]

			if selectedIndex == 9:
				Material["DiffuseColor"] = [ 205, 170, 125, 1.0 ]
		
			if selectedIndex == 10:
				Material["DiffuseColor"] = [ 207, 141, 91, 1.0 ]
		
			if selectedIndex == 11:
				Material["DiffuseColor"] = [ 163, 104, 70, 1.0 ]

			if selectedIndex == 12:
				Material["DiffuseColor"] = [ 125, 83, 62, 1.0 ]
		
			if selectedIndex == 13:
				Material["DiffuseColor"] = [ 68, 48, 40, 1.0 ]
		
			if selectedIndex == 14:
				Material["DiffuseColor"] = [ 63, 25, 17, 1.0 ]
			
			# setting colors from spreadsheet
			if selectedIndex == 15:
				
				self.oRedL.hide()
				self.oRedB1.hide()
				self.oRedE.hide()
				self.oRedB2.hide()
				
				self.oGreenL.hide()
				self.oGreenB1.hide()
				self.oGreenE.hide()
				self.oGreenB2.hide()
				
				self.oBlueL.hide()
				self.oBlueB1.hide()
				self.oBlueE.hide()
				self.oBlueB2.hide()
				
				self.oAlphaL.hide()
				self.oAlphaB1.hide()
				self.oAlphaE.hide()
				self.oAlphaB2.hide()
				
				self.oShineL.hide()
				self.oShineB1.hide()
				self.oShineE.hide()
				self.oShineB2.hide()
				
				self.oTransL.hide()
				self.oTransB1.hide()
				self.oTransE.hide()
				self.oTransB2.hide()
				
				self.oStepL1.hide()
				self.oStepL2.hide()
				self.oStepE.hide()
				self.oStepAlphaL.hide()
				self.oStepAlphaE.hide()
				self.oStepSingleL.hide()
				self.oStepSingleE.hide()

				self.oCustomB.hide()

				self.sheetInfo.show()
				self.sheetB1.show()
			
			if selectedIndex == 16:
				Material["DiffuseColor"] = [ 255, 0, 0, 1.0 ]
			
			if selectedIndex == 17:
				Material["DiffuseColor"] = [ 0, 255, 0, 1.0 ]
			
			if selectedIndex == 18:
				Material["DiffuseColor"] = [ 0, 0, 255, 1.0 ]
			
			if selectedIndex == 19:
				[ r, g, b, a ] = MagicPanels.gDefaultColor
				cR = self.convertToRGB(r)
				cG = self.convertToRGB(g)
				cB = self.convertToRGB(b)
				Material["DiffuseColor"] = [ cR, cG, cB, a ]
				
			# update color
			if selectedIndex != 0 and selectedIndex != 15:
				
				# update text fields
				if self.gColorTarget == "Shininess":
					color = round(float(Material["Shininess"]), 2)
					self.oShineE.setText(str(color))

				elif self.gColorTarget == "Transparency":
					color = round(float(Material["Transparency"]), 2)
					self.oTransE.setText(str(color))
				
				else:
					color = Material[self.gColorTarget]
					[ r, g, b, a ] = [ int(color[0]), int(color[1]), int(color[2]), round(float(color[3]), 2) ]

					# set GUI form with RGB color values
					self.oRedE.setText(str(r))
					self.oGreenE.setText(str(g))
					self.oBlueE.setText(str(b))
					self.oAlphaE.setText(str(a))
				
				# update color for selected target
				self.setColor()
				self.getColor()
			
		# ############################################################################
		def selectRadioButton1(self):
			self.rtcc.hide()
			self.setGeometry(self.gPW, self.gPH, self.toolSW, self.toolSH)
			self.showDefaultGUI()
			self.sTargets.setCurrentIndex(0)
			self.sColors.setCurrentIndex(0)
		
		def selectRadioButton2(self):
			self.hideGUI()
			self.resize(540, 650)
			self.rtcc.open()
			self.sTargets.setCurrentIndex(0)
			self.sColors.setCurrentIndex(0)

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
