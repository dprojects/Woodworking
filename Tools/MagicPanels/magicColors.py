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
	translate('magicColors', 'SpecularColor'): 6, 
	translate('magicColors', "let's slide all"): 7 # no comma
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
		gStepAlpha = 5
		gStepSingle = 5
		
		gKernelVersion = MagicPanels.gKernelVersion
		
		gColorToSet = {
			"DiffuseColor": [ 204, 204, 204, 255 ], 
			"AmbientColor": [ 85, 85, 85, 255 ], 
			"SpecularColor": [ 136, 136, 136, 255 ], 
			"EmissiveColor": [ 0, 0, 0, 255 ], 
			"Shininess": 90, 
			"Transparency": 0 # no comma
		}
		gColorTarget = "DiffuseColor"
		
		# ############################################################################
		# screen settings
		# ############################################################################

		# tool GUI size
		toolSW = 250
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
			
			area = self.toolSW - 20
			offset = 10
			size = 50
			size2x = size + size + offset
			
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
			self.s1S.setFixedWidth(area)
			self.s1S.move(10, row)

			row += 20
			
			# button
			self.s1B1 = QtGui.QPushButton(translate('magicColors', 'refresh selection'), self)
			self.s1B1.clicked.connect(self.getSelected)
			self.s1B1.setFixedWidth(area)
			self.s1B1.setFixedHeight(40)
			self.s1B1.move(10, row)

			# ############################################################################
			# options - target attribute
			# ############################################################################

			row += 50

			# label
			self.sTargetsL = QtGui.QLabel(translate('magicColors', 'Target:'), self)
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
					translate('magicColors', 'Transparency'), 
					translate('magicColors', "let's slide all") # no comma
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
			self.sColorsL = QtGui.QLabel(translate('magicColors', 'Sample:'), self)
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
			self.rb1.setText(translate('magicColors', 'simple'))
			self.rb1.toggled.connect(self.selectRadioButton1)
			self.rb1.move(10, row)
			
			self.rb2 = QtGui.QRadioButton(self)
			self.rb2.setText(translate('magicColors', 'extended'))
			self.rb2.toggled.connect(self.selectRadioButton2)
			self.rb2.move(100, row)
			self.rb1.setChecked(False)
			
			# ############################################################################
			# options - settings
			# ############################################################################

			row += 50
			rowShine = row
			rowTrans = row
			rowSheet = row
			rowChooser = row
			rowAll = row
		
			# ############################################################################
			# options - red color
			# ############################################################################

			# label
			self.oRedL = QtGui.QLabel(translate('magicColors', 'Red:'), self)
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
			self.oGreenL = QtGui.QLabel(translate('magicColors', 'Green:'), self)
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
			self.oBlueL = QtGui.QLabel(translate('magicColors', 'Blue:'), self)
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
			self.oAlphaL = QtGui.QLabel(translate('magicColors', 'Alpha:'), self)
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
			self.oShineL.move(10, rowShine+3)

			rowShine += 30

			self.oShineSlide = QtGui.QSlider(self)
			self.oShineSlide.setRange(0, 100)
			self.oShineSlide.setValue(90)
			self.oShineSlide.setOrientation(QtCore.Qt.Horizontal)
			self.oShineSlide.setFixedWidth(area)
			self.oShineSlide.valueChanged[int].connect(self.setShineSlide)
			self.oShineSlide.move(10, rowShine)
			self.oShineSlide.hide()
		
			rowShine += 50

			# button
			self.oShineB1 = QtGui.QPushButton("-", self)
			self.oShineB1.clicked.connect(self.setColorShineB1)
			self.oShineB1.setFixedWidth(size)
			self.oShineB1.move(col1, rowShine)
			self.oShineB1.setAutoRepeat(True)
			
			# text input
			self.oShineE = QtGui.QLineEdit(self)
			self.oShineE.setText("90")
			self.oShineE.setFixedWidth(size)
			self.oShineE.move(col2, rowShine)

			# button
			self.oShineB2 = QtGui.QPushButton("+", self)
			self.oShineB2.clicked.connect(self.setColorShineB2)
			self.oShineB2.setFixedWidth(size)
			self.oShineB2.move(col3, rowShine)
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
			self.oTransL.move(10, rowTrans+3)

			rowTrans += 30

			self.oTransSlide = QtGui.QSlider(self)
			self.oTransSlide.setRange(0, 100)
			self.oTransSlide.setValue(90)
			self.oTransSlide.setOrientation(QtCore.Qt.Horizontal)
			self.oTransSlide.setFixedWidth(area)
			self.oTransSlide.valueChanged[int].connect(self.setTransSlide)
			self.oTransSlide.move(10, rowTrans)
			self.oTransSlide.hide()
			
			rowTrans += 50

			# button
			self.oTransB1 = QtGui.QPushButton("-", self)
			self.oTransB1.clicked.connect(self.setColorTransB1)
			self.oTransB1.setFixedWidth(size)
			self.oTransB1.move(col1, rowTrans)
			self.oTransB1.setAutoRepeat(True)
			
			# text input
			self.oTransE = QtGui.QLineEdit(self)
			self.oTransE.setText("0")
			self.oTransE.setFixedWidth(size)
			self.oTransE.move(col2, rowTrans)

			# button
			self.oTransB2 = QtGui.QPushButton("+", self)
			self.oTransB2.clicked.connect(self.setColorTransB2)
			self.oTransB2.setFixedWidth(size)
			self.oTransB2.move(col3, rowTrans)
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
			self.oStepL1 = QtGui.QLabel(translate('magicColors', 'RGBA step:'), self)
			self.oStepL1.move(10, row+3)
			
			# text input
			self.oStepE = QtGui.QLineEdit(self)
			self.oStepE.setText(str(self.gStep))
			self.oStepE.setFixedWidth(size)
			self.oStepE.move(col2, row)
			
			rowSingle = rowShine
			rowSingle += 30
			
			# label
			self.oStepSingleL = QtGui.QLabel(translate('magicColors', 'Step:'), self)
			self.oStepSingleL.move(10, rowSingle+3)

			# text input
			self.oStepSingleE = QtGui.QLineEdit(self)
			self.oStepSingleE.setText(str(self.gStepSingle))
			self.oStepSingleE.setFixedWidth(size)
			self.oStepSingleE.move(col2, rowSingle)
			
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
			self.oCustomB.setFixedWidth(area)
			self.oCustomB.setFixedHeight(40)
			self.oCustomB.move(10, row)

			# ############################################################################
			# color from sheet
			# ############################################################################

			info = translate('magicColors', 'This button below will set face colors from spreadsheet for all objects in active document. If the faceColors spreadsheet is not available, it will be created. Make sure you want to overwrite existing colors for all objects. There is no undo option for that. ')
			
			self.sheetInfo = QtGui.QLabel(info, self)
			self.sheetInfo.setFixedWidth(area)
			self.sheetInfo.move(10, rowSheet+3)
			self.sheetInfo.setWordWrap(True)
			self.sheetInfo.hide()

			rowSheet += 140
			
			# button
			self.sheetB1 = QtGui.QPushButton(translate('magicColors', 'set face colors from spreadsheet'), self)
			self.sheetB1.clicked.connect(self.setSheet)
			self.sheetB1.setFixedWidth(area)
			self.sheetB1.setFixedHeight(40)
			self.sheetB1.move(10, rowSheet)
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
			self.rtcc.hide()

			# ############################################################################
			# all-in-one - settings
			# ############################################################################
			
			rowAll -= 40
			groupWidth = area
			sliderWidth = area-50
			
			# ############################################################################
			# all-in-one - DiffuseColor
			# ############################################################################
			
			self.groupDiffuseColor = QtGui.QGroupBox('Color:', self)
			self.groupDiffuseColor.move(10, rowAll)
			self.groupDiffuseColor.setFixedWidth(groupWidth)
			self.groupDiffuseColor.hide()
			
			self.sliderDCR = QtGui.QSlider(self)
			self.sliderDCR.setRange(0, 255)
			self.sliderDCR.setValue(0)
			self.sliderDCR.setOrientation(QtCore.Qt.Horizontal)
			self.sliderDCR.setFixedWidth(sliderWidth)
			self.sliderDCR.valueChanged[int].connect(self.setAllInOne)
			
			self.sliderDCG = QtGui.QSlider(self)
			self.sliderDCG.setRange(0, 255)
			self.sliderDCG.setValue(0)
			self.sliderDCG.setOrientation(QtCore.Qt.Horizontal)
			self.sliderDCG.setFixedWidth(sliderWidth)
			self.sliderDCG.valueChanged[int].connect(self.setAllInOne)
			
			self.sliderDCB = QtGui.QSlider(self)
			self.sliderDCB.setRange(0, 255)
			self.sliderDCB.setValue(0)
			self.sliderDCB.setOrientation(QtCore.Qt.Horizontal)
			self.sliderDCB.setFixedWidth(sliderWidth)
			self.sliderDCB.valueChanged[int].connect(self.setAllInOne)
			
			self.layoutDiffuseColor = QtGui.QFormLayout(self.groupDiffuseColor)
			self.layoutDiffuseColor.addRow("R :", self.sliderDCR)
			self.layoutDiffuseColor.addRow("G :", self.sliderDCG)
			self.layoutDiffuseColor.addRow("B :", self.sliderDCB)
			
			# ############################################################################
			# all-in-one - AmbientColor
			# ############################################################################
			
			rowAll += 100
			
			self.groupAmbientColor = QtGui.QGroupBox('Ambient:', self)
			self.groupAmbientColor.move(10, rowAll)
			self.groupAmbientColor.setFixedWidth(groupWidth)
			self.groupAmbientColor.hide()
			
			self.sliderACR = QtGui.QSlider(self)
			self.sliderACR.setRange(0, 255)
			self.sliderACR.setValue(0)
			self.sliderACR.setOrientation(QtCore.Qt.Horizontal)
			self.sliderACR.setFixedWidth(sliderWidth)
			self.sliderACR.valueChanged[int].connect(self.setAllInOne)
			
			self.sliderACG = QtGui.QSlider(self)
			self.sliderACG.setRange(0, 255)
			self.sliderACG.setValue(0)
			self.sliderACG.setOrientation(QtCore.Qt.Horizontal)
			self.sliderACG.setFixedWidth(sliderWidth)
			self.sliderACG.valueChanged[int].connect(self.setAllInOne)
			
			self.sliderACB = QtGui.QSlider(self)
			self.sliderACB.setRange(0, 255)
			self.sliderACB.setValue(0)
			self.sliderACB.setOrientation(QtCore.Qt.Horizontal)
			self.sliderACB.setFixedWidth(sliderWidth)
			self.sliderACB.valueChanged[int].connect(self.setAllInOne)
			
			self.layoutAmbientColor = QtGui.QFormLayout(self.groupAmbientColor)
			self.layoutAmbientColor.addRow("R :", self.sliderACR)
			self.layoutAmbientColor.addRow("G :", self.sliderACG)
			self.layoutAmbientColor.addRow("B :", self.sliderACB)
			
			# ############################################################################
			# all-in-one - EmissiveColor
			# ############################################################################
			
			rowAll += 100
			
			self.groupEmissiveColor = QtGui.QGroupBox('Emissive:', self)
			self.groupEmissiveColor.move(10, rowAll)
			self.groupEmissiveColor.setFixedWidth(groupWidth)
			self.groupEmissiveColor.hide()
			
			self.sliderECR = QtGui.QSlider(self)
			self.sliderECR.setRange(0, 255)
			self.sliderECR.setValue(0)
			self.sliderECR.setOrientation(QtCore.Qt.Horizontal)
			self.sliderECR.setFixedWidth(sliderWidth)
			self.sliderECR.valueChanged[int].connect(self.setAllInOne)
			
			self.sliderECG = QtGui.QSlider(self)
			self.sliderECG.setRange(0, 255)
			self.sliderECG.setValue(0)
			self.sliderECG.setOrientation(QtCore.Qt.Horizontal)
			self.sliderECG.setFixedWidth(sliderWidth)
			self.sliderECG.valueChanged[int].connect(self.setAllInOne)
			
			self.sliderECB = QtGui.QSlider(self)
			self.sliderECB.setRange(0, 255)
			self.sliderECB.setValue(0)
			self.sliderECB.setOrientation(QtCore.Qt.Horizontal)
			self.sliderECB.setFixedWidth(sliderWidth)
			self.sliderECB.valueChanged[int].connect(self.setAllInOne)
			
			self.layoutEmissiveColor = QtGui.QFormLayout(self.groupEmissiveColor)
			self.layoutEmissiveColor.addRow("R :", self.sliderECR)
			self.layoutEmissiveColor.addRow("G :", self.sliderECG)
			self.layoutEmissiveColor.addRow("B :", self.sliderECB)
			
			# ############################################################################
			# all-in-one - SpecularColor
			# ############################################################################
			
			rowAll += 100
			
			self.groupSpecularColor = QtGui.QGroupBox('Specular:', self)
			self.groupSpecularColor.move(10, rowAll)
			self.groupSpecularColor.setFixedWidth(groupWidth)
			self.groupSpecularColor.hide()
			
			self.sliderSCR = QtGui.QSlider(self)
			self.sliderSCR.setRange(0, 255)
			self.sliderSCR.setValue(0)
			self.sliderSCR.setOrientation(QtCore.Qt.Horizontal)
			self.sliderSCR.setFixedWidth(sliderWidth)
			self.sliderSCR.valueChanged[int].connect(self.setAllInOne)
			
			self.sliderSCG = QtGui.QSlider(self)
			self.sliderSCG.setRange(0, 255)
			self.sliderSCG.setValue(0)
			self.sliderSCG.setOrientation(QtCore.Qt.Horizontal)
			self.sliderSCG.setFixedWidth(sliderWidth)
			self.sliderSCG.valueChanged[int].connect(self.setAllInOne)
			
			self.sliderSCB = QtGui.QSlider(self)
			self.sliderSCB.setRange(0, 255)
			self.sliderSCB.setValue(0)
			self.sliderSCB.setOrientation(QtCore.Qt.Horizontal)
			self.sliderSCB.setFixedWidth(sliderWidth)
			self.sliderSCB.valueChanged[int].connect(self.setAllInOne)
			
			self.layoutSpecularColor = QtGui.QFormLayout(self.groupSpecularColor)
			self.layoutSpecularColor.addRow("R :", self.sliderSCR)
			self.layoutSpecularColor.addRow("G :", self.sliderSCG)
			self.layoutSpecularColor.addRow("B :", self.sliderSCB)
			
			# ############################################################################
			# all-in-one - Shininess
			# ############################################################################
			
			rowAll += 100
			
			self.groupShininess = QtGui.QGroupBox('Shininess:', self)
			self.groupShininess.move(10, rowAll)
			self.groupShininess.setFixedWidth(groupWidth)
			self.groupShininess.hide()
			
			self.sliderShCR = QtGui.QSlider(self)
			self.sliderShCR.setRange(0, 100)
			self.sliderShCR.setValue(0)
			self.sliderShCR.setOrientation(QtCore.Qt.Horizontal)
			self.sliderShCR.setFixedWidth(sliderWidth)
			self.sliderShCR.valueChanged[int].connect(self.setAllInOne)
			
			self.layoutShininess = QtGui.QFormLayout(self.groupShininess)
			self.layoutShininess.addRow("S :", self.sliderShCR)
			
			# ############################################################################
			# all-in-one - Transparency
			# ############################################################################
	
			rowAll += 60
	
			self.groupTransparency = QtGui.QGroupBox('Transparency:', self)
			self.groupTransparency.move(10, rowAll)
			self.groupTransparency.setFixedWidth(groupWidth)
			self.groupTransparency.hide()
			
			self.sliderTrCR = QtGui.QSlider(self)
			self.sliderTrCR.setRange(0, 100)
			self.sliderTrCR.setValue(0)
			self.sliderTrCR.setOrientation(QtCore.Qt.Horizontal)
			self.sliderTrCR.setFixedWidth(sliderWidth)
			self.sliderTrCR.valueChanged[int].connect(self.setAllInOne)
			
			self.layoutTransparency = QtGui.QFormLayout(self.groupTransparency)
			self.layoutTransparency.addRow("T :", self.sliderTrCR)
			
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
		
		# ############################################################################
		def setAllSliders(self):
		
			try:
				[ r, g, b, a ] = self.gColorToSet["DiffuseColor"]
				self.sliderDCR.setValue(r)
				self.sliderDCG.setValue(g)
				self.sliderDCB.setValue(b)
			except:
				skip = 1
				
			try:
				[ r, g, b, a ] = self.gColorToSet["AmbientColor"]
				self.sliderACR.setValue(r)
				self.sliderACG.setValue(g)
				self.sliderACB.setValue(b)
			except:
				skip = 1
				
			try:
				[ r, g, b, a ] = self.gColorToSet["EmissiveColor"]
				self.sliderECR.setValue(r)
				self.sliderECG.setValue(g)
				self.sliderECB.setValue(b)
			except: 
				skip = 1
			
			try:
				[ r, g, b, a ] = self.gColorToSet["SpecularColor"]
				self.sliderSCR.setValue(r)
				self.sliderSCG.setValue(g)
				self.sliderSCB.setValue(b)
			except:
				skip = 1
				
			try:	
				self.sliderShCR.setValue( self.gColorToSet["Shininess"] )
			except:
				skip = 1
				
			try:
				self.sliderTrCR.setValue( self.gColorToSet["Transparency"] )
			except:
				skip = 1

		# ############################################################################
		def setAllInOne(self):
			
			backupColorToSet = self.gColorToSet
			backupColorTarget = self.gColorTarget
			
			backupR = self.oRedE.text()
			backupG = self.oGreenE.text()
			backupB = self.oBlueE.text()
			backupA = self.oAlphaE.text()
			backupSh = self.oShineE.text()
			backupTr = self.oTransE.text()
			
			# DiffuseColor
			[ r, g, b, a ] = [ self.sliderDCR.value(), self.sliderDCG.value(), self.sliderDCB.value(), 255 ]
			self.gColorTarget = "DiffuseColor"
			self.gColorToSet[self.gColorTarget] = [ r, g, b, a ]
			self.oRedE.setText(str(r))
			self.oGreenE.setText(str(g))
			self.oBlueE.setText(str(b))
			self.oAlphaE.setText(str(255))
			self.setColor()
			
			# AmbientColor
			[ r, g, b, a ] = [ self.sliderACR.value(), self.sliderACG.value(), self.sliderACB.value(), 255 ]
			self.gColorTarget = "AmbientColor"
			self.gColorToSet[self.gColorTarget] = [ r, g, b, a ]
			self.oRedE.setText(str(r))
			self.oGreenE.setText(str(g))
			self.oBlueE.setText(str(b))
			self.oAlphaE.setText(str(a))
			self.setColor()
			
			# EmissiveColor
			[ r, g, b, a ] = [ self.sliderECR.value(), self.sliderECG.value(), self.sliderECB.value(), 255 ]
			self.gColorTarget = "EmissiveColor"
			self.gColorToSet[self.gColorTarget] = [ r, g, b, a ]
			self.oRedE.setText(str(r))
			self.oGreenE.setText(str(g))
			self.oBlueE.setText(str(b))
			self.oAlphaE.setText(str(a))
			self.setColor()
			
			# SpecularColor
			[ r, g, b, a ] = [ self.sliderSCR.value(), self.sliderSCG.value(), self.sliderSCB.value(), 255 ]
			self.gColorTarget = "SpecularColor"
			self.gColorToSet[self.gColorTarget] = [ r, g, b, a ]
			self.oRedE.setText(str(r))
			self.oGreenE.setText(str(g))
			self.oBlueE.setText(str(b))
			self.oAlphaE.setText(str(a))
			self.setColor()
			
			# Shininess
			self.gColorTarget = "Shininess"
			self.gColorToSet[self.gColorTarget] = self.sliderShCR.value()
			self.oShineE.setText(str( self.gColorToSet[self.gColorTarget] ))
			self.setColor()
			
			# Transparency
			self.gColorTarget = "Transparency"
			self.gColorToSet[self.gColorTarget] = self.sliderTrCR.value()
			self.oTransE.setText(str( self.gColorToSet[self.gColorTarget] ))
			self.setColor()
			
			# restore from backup
			self.gColorToSet = backupColorToSet
			self.gColorTarget = backupColorTarget
			self.oRedE.setText(str( backupR ))
			self.oGreenE.setText(str( backupG ))
			self.oBlueE.setText(str( backupB ))
			self.oAlphaE.setText(str( backupA ))
			self.oShineE.setText(str( backupSh ))
			self.oTransE.setText(str( backupTr ))
			
		# ############################################################################
		def setShineSlide(self, value):
			self.oShineE.setText(str(value))
			self.setColor()
		
		# ############################################################################
		def setTransSlide(self, value):
			self.oTransE.setText(str(value))
			self.setColor()
		
		# ############################################################################
		def setChooserColor(self, iColor):

			try:
			
				[ r, g, b, a ] = iColor
				self.rtcc.setCurrentColor(QtGui.QColor(r, g, b, a))
			
			# skip for transparency and shininess
			except:
				skip = 1
		
		# ############################################################################
		def getColorFromChooser(self, iColor):
	
			self.oRedE.setText(str( int(iColor.red()) ))
			self.oGreenE.setText(str( int(iColor.green()) ))
			self.oBlueE.setText(str( int(iColor.blue()) ))
			self.oAlphaE.setText(str( int(iColor.alpha()) ))
			
			self.oShineE.setText(str( int(iColor.valueF() * 100) ))
			self.oShineSlide.setValue( int(iColor.valueF() * 100) )
			
			self.oTransE.setText(str( int(iColor.valueF() * 100) ))
			self.oTransSlide.setValue( int(iColor.valueF() * 100) )
			
			self.setColor()

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
			
				# ############################################################################
				# get color
				# ############################################################################
				if self.gMode == "Face":
					self.gColorToSet[self.gColorTarget] = MagicPanels.getColor(self.gObj, self.gFaceIndex, self.gColorTarget, "RGBA")

				if self.gMode == "Object":
					self.gColorToSet[self.gColorTarget] = MagicPanels.getColor(self.gObj, 0, self.gColorTarget, "RGBA")

				if self.gMode == "Multi":

					# first face selected
					if self.gFace == "":
						self.gColorToSet[self.gColorTarget] = MagicPanels.getColor(self.gObj, self.gFaceIndex, self.gColorTarget, "RGBA")

					# first object selected, no face
					else:
						self.gColorToSet[self.gColorTarget] = MagicPanels.getColor(self.gObj, 0, self.gColorTarget, "RGBA")
				
				# ############################################################################
				# set color to GUI
				# ############################################################################
				if self.gColorTarget == "Shininess":
					
					if self.gColorToSet[self.gColorTarget] == "":
						self.gColorToSet[self.gColorTarget] = 90
					
					self.oShineE.setText(str(self.gColorToSet[self.gColorTarget]))
					self.oShineSlide.setValue(int(self.gColorToSet[self.gColorTarget]))
					
				elif self.gColorTarget == "Transparency":
					
					if self.gColorToSet[self.gColorTarget] == "":
						self.gColorToSet[self.gColorTarget] = 0

					self.oTransE.setText(str(self.gColorToSet[self.gColorTarget]))
					self.oTransSlide.setValue(int(self.gColorToSet[self.gColorTarget]))
					
				else:
					color = self.gColorToSet[self.gColorTarget]
					if self.gColorToSet[self.gColorTarget] != "":
						
						[ r, g, b, a ] = [ 
							self.gColorToSet[self.gColorTarget][0], 
							self.gColorToSet[self.gColorTarget][1], 
							self.gColorToSet[self.gColorTarget][2], 
							self.gColorToSet[self.gColorTarget][3] ]

						self.oRedE.setText(str(r))
						self.oGreenE.setText(str(g))
						self.oBlueE.setText(str(b))
						self.oAlphaE.setText(str(a))
						
						if self.gColorTarget == "all-in-one":
							self.setAllSliders()
							
						if self.rb2.isChecked() == True:
							self.setChooserColor(self.gColorToSet[self.gColorTarget])
				
			except:
				self.s1S.setText(translate('magicColors', 'please select objects or faces'))
				return -1
				
		# ############################################################################
		def setColor(self):

			try:
			
				# ############################################################################
				# get color to set
				# ############################################################################
				if self.gColorTarget == "Shininess":
					self.gColorToSet[self.gColorTarget] = int( self.oShineE.text() )
				
				elif self.gColorTarget == "Transparency":
					self.gColorToSet[self.gColorTarget] = int( self.oTransE.text() )

				else:
					r = int( self.oRedE.text() )
					g = int( self.oGreenE.text() )
					b = int( self.oBlueE.text() )
					a = int( self.oAlphaE.text() )
					
					self.gColorToSet[self.gColorTarget] = [ r, g, b, a ]
				
				# ############################################################################
				# set color
				# ############################################################################
				if self.gMode == "Face":
					MagicPanels.setColor(self.gObj, self.gFaceIndex, self.gColorToSet[self.gColorTarget], self.gColorTarget, "RGBA")

				if self.gMode == "Object":
					MagicPanels.setColor(self.gObj, 0, self.gColorToSet[self.gColorTarget], self.gColorTarget, "RGBA")

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
							MagicPanels.setColor(self.gObj, 0, self.gColorToSet[self.gColorTarget], self.gColorTarget, "RGBA")

						# faces selected for object
						else:

							i = 0
							for f in self.gFaceArr[o]:

								# set current face for other functions
								self.gFace = self.gFaceArr[o][i]
								self.gFaceIndex = MagicPanels.getFaceIndex(self.gObj, self.gFace)
							
								MagicPanels.setColor(self.gObj, self.gFaceIndex, self.gColorToSet[self.gColorTarget], self.gColorTarget, "RGBA")

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
				
				self.sColors.setCurrentIndex(0)
			
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
			value = int(self.oAlphaE.text())
			step = int(self.oStepE.text())
			
			if value - step <= 0:
				value = 255
			else:
				value = value - step

			self.oAlphaE.setText(str(value))
			self.setColor()
		
		def setColorAlphaB2(self):
			value = int(self.oAlphaE.text())
			step = int(self.oStepE.text())
			
			if value + step >= 255:
				value = 0
			else:
				value = value + step

			self.oAlphaE.setText(str(value))
			self.setColor()
		
		def setColorShineB1(self):
			value = int(self.oShineE.text())
			step = int(self.oStepSingleE.text())
			
			if value - step <= 0:
				value = 100
			else:
				value = value - step

			self.oShineE.setText(str(value))
			self.oShineSlide.setValue(int(value))
			self.setColor()
		
		def setColorShineB2(self):
			value = int(self.oShineE.text())
			step = int(self.oStepSingleE.text())
			
			if value + step >= 100:
				value = 0
			else:
				value = value + step

			self.oShineE.setText(str(value)) 
			self.oShineSlide.setValue(int(value))
			self.setColor()

		def setColorTransB1(self):
			value = int(self.oTransE.text())
			step = int(self.oStepSingleE.text())
			
			if value - step <= 0:
				value = 100
			else:
				value = value - step

			self.oTransE.setText(str(value))
			self.oTransSlide.setValue(int(value))
			self.setColor()
		
		def setColorTransB2(self):
			value = int(self.oTransE.text())
			step = int(self.oStepSingleE.text())
			
			if value + step >= 100:
				value = 0
			else:
				value = value + step

			self.oTransE.setText(str(value))
			self.oTransSlide.setValue(int(value))
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
			self.oStepE.hide()
			
			self.oStepSingleL.hide()
			self.oStepSingleE.hide()
			self.oShineSlide.hide()
			self.oTransSlide.hide()
			
			self.oCustomB.hide()
			
			self.sheetInfo.hide()
			self.sheetB1.hide()
			
			self.groupDiffuseColor.hide()
			self.groupAmbientColor.hide()
			self.groupEmissiveColor.hide()
			self.groupSpecularColor.hide()
			self.groupShininess.hide()
			self.groupTransparency.hide()

		# ############################################################################
		def showGUI(self, iType="color"):
			
			# if real-time chooser is selected not switch GUI
			if self.rb2.isChecked() == True:
				return ""
			
			self.hideGUI()
			
			self.rb1.show()
			self.rb2.show()
			
			if iType == "Shininess":
				
				self.oShineL.show()
				self.oShineB1.show()
				self.oShineE.show()
				self.oShineB2.show()

				self.oStepSingleL.show()
				self.oStepSingleE.show()
				self.oShineSlide.show()
				
				self.oCustomB.show()

			elif iType == "Transparency":
				
				self.oTransL.show()
				self.oTransB1.show()
				self.oTransE.show()
				self.oTransB2.show()
				
				self.oStepSingleL.show()
				self.oStepSingleE.show()
				self.oTransSlide.show()
				
				self.oCustomB.show()
		
			elif iType == "Sheet":
				
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
				self.oStepE.hide()

				self.oStepSingleL.hide()
				self.oStepSingleE.hide()

				self.oCustomB.hide()

				self.sheetInfo.show()
				self.sheetB1.show()
		
			elif iType == "all-in-one":
				
				self.rb1.hide()
				self.rb2.hide()
			
				self.groupDiffuseColor.show()
				self.groupAmbientColor.show()
				self.groupEmissiveColor.show()
				self.groupSpecularColor.show()
				self.groupShininess.show()
				self.groupTransparency.show()

			else:
			
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
				self.oStepE.show()
				
				self.oStepSingleL.hide()
				self.oStepSingleE.hide()
				
				self.oShineSlide.hide()
				self.oTransSlide.hide()

				self.oCustomB.show()
				
				self.sheetInfo.hide()
				self.sheetB1.hide()

		# ############################################################################
		def setTargetProperty(self, selectedText):
			
			# get current index
			selectedIndex = getMenuIndex1[selectedText]
			
			# set predefined schema to default state
			self.sColors.setCurrentIndex(0)
			
			# set color target, do not get it from translation
			if selectedIndex == 0:
				self.gColorTarget = "DiffuseColor"
			
			if selectedIndex == 1:
				self.gColorTarget = "DiffuseColor"
				
			if selectedIndex == 2:
				self.gColorTarget = "Transparency"
				
			if selectedIndex == 3:
				self.gColorTarget = "AmbientColor"
				
			if selectedIndex == 4:
				self.gColorTarget = "EmissiveColor"
				
			if selectedIndex == 5:
				self.gColorTarget = "Shininess"
				
			if selectedIndex == 6:
				self.gColorTarget = "SpecularColor"

			if selectedIndex == 7:
				self.gColorTarget = "all-in-one"

			if self.rb2.isChecked() == False:
				
				self.showGUI(self.gColorTarget)

				if selectedIndex == 7:
					self.setGeometry(self.gPW, self.gPH, self.toolSW, 720)
					self.setAllSliders()
				else:
					self.setGeometry(self.gPW, self.gPH, self.toolSW, self.toolSH)
					self.getColor()

		# ############################################################################
		def setPredefinedColors(self, selectedText):
			
			# get selection index and set screen size
			selectedIndex = getMenuIndex2[selectedText]
			
			# skip if reset selection
			if selectedIndex == 0:
				return ""
			
			self.showGUI(self.gColorTarget)
			
			# set default color structure, [ RGB int, alpha float ]
			Material = { 
				"DiffuseColor": [ 204, 204, 204, 255 ], 
				"AmbientColor": [ 85, 85, 85, 255 ], 
				"SpecularColor": [ 136, 136, 136, 255 ], 
				"EmissiveColor": [ 0, 0, 0, 255 ], 
				"Shininess": 90, 
				"Transparency": 0 # no comma
			}

			if selectedIndex == 2:
				Material["DiffuseColor"] = [ 255, 255, 255, 255 ]

			if selectedIndex == 3:
				Material["DiffuseColor"] = [ 0, 0, 0, 255 ]
			
			if selectedIndex == 4:
				Material["DiffuseColor"] = [ 255, 0, 255, 255 ]

			if selectedIndex == 5:
				Material["DiffuseColor"] = [ 222, 184, 135, 255 ]
		
			if selectedIndex == 6:
				Material["DiffuseColor"] = [ 247, 185, 108, 255 ]

			if selectedIndex == 7:
				Material["DiffuseColor"] = [ 174, 138, 105, 255 ]

			if selectedIndex == 8:
				Material["DiffuseColor"] = [ 175, 91, 76, 255 ]

			if selectedIndex == 9:
				Material["DiffuseColor"] = [ 205, 170, 125, 255 ]
		
			if selectedIndex == 10:
				Material["DiffuseColor"] = [ 207, 141, 91, 255 ]
		
			if selectedIndex == 11:
				Material["DiffuseColor"] = [ 163, 104, 70, 255 ]

			if selectedIndex == 12:
				Material["DiffuseColor"] = [ 125, 83, 62, 255 ]
		
			if selectedIndex == 13:
				Material["DiffuseColor"] = [ 68, 48, 40, 255 ]
		
			if selectedIndex == 14:
				Material["DiffuseColor"] = [ 63, 25, 17, 255 ]
			
			# setting colors from spreadsheet
			if selectedIndex == 15:
				self.showGUI("Sheet")

			if selectedIndex == 16:
				Material["DiffuseColor"] = [ 255, 0, 0, 255 ]
			
			if selectedIndex == 17:
				Material["DiffuseColor"] = [ 0, 255, 0, 255 ]
			
			if selectedIndex == 18:
				Material["DiffuseColor"] = [ 0, 0, 255, 255 ]
			
			if selectedIndex == 19:
				Material["DiffuseColor"] = MagicPanels.convertColor(MagicPanels.gDefaultColor, "RGBA")
				
			# update color
			if selectedIndex != 0 and selectedIndex != 15:
				
				# update text fields
				if self.gColorTarget == "Shininess":
					self.oShineE.setText(str( Material["Shininess"] ))

				elif self.gColorTarget == "Transparency":
					self.oTransE.setText(str( Material["Transparency"] ))
				
				elif self.gColorTarget == "all-in-one":
						self.gColorToSet = Material
						self.setAllSliders()

				else:
					color = Material[self.gColorTarget]
					[ r, g, b, a ] = [ int(color[0]), int(color[1]), int(color[2]), int(color[3]) ]

					# set GUI form with RGB color values
					self.oRedE.setText(str(r))
					self.oGreenE.setText(str(g))
					self.oBlueE.setText(str(b))
					self.oAlphaE.setText(str(a))

					if self.rb2.isChecked() == True:
						self.setChooserColor(color)

				# update color for selected target
				self.setColor()
				self.getColor()
			
		# ############################################################################
		def selectRadioButton1(self):
			self.rtcc.hide()
			self.setGeometry(self.gPW, self.gPH, self.toolSW, self.toolSH)
			self.showGUI(self.gColorTarget)
			self.sColors.setCurrentIndex(0)
			self.getColor()
			
		def selectRadioButton2(self):
			self.hideGUI()
			self.resize(540, 650)
			self.rtcc.open()
			self.sColors.setCurrentIndex(0)
			self.getColor()

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

