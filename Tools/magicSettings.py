import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate


# ############################################################################
# Global definitions
# ############################################################################

# add new items only at the end and change self.sPageList
getMenuIndex1 = {
	translate('magicSettings', 'Settings - page 1'): 0, 
	translate('magicSettings', 'Settings - page 2'): 1, 
	translate('magicSettings', 'Settings - page 3'): 2, 
	translate('magicSettings', 'Settings - page 4'): 3, 
	translate('magicSettings', 'Settings - page 5'): 4, 
	translate('magicSettings', 'Settings - page 6'): 5 # no comma 
}

# add new items only at the end and change self.oWoodWeightCalculationList
getWoodWeightCalculation = {
	translate('magicSettings', 'kg per area in m^2'): 'kg/m^2',
	translate('magicSettings', 'kg per volume in m^3'): 'kg/m^3',
	translate('magicSettings', 'kg per wood piece'): 'kg/piece',
	translate('magicSettings', 'pounds per area in ft^2'): 'lb/ft^2',
	translate('magicSettings', 'pounds per cubic foot'): 'lb/ft^3',
	translate('magicSettings', 'pounds per cubic inch'): 'lb/in^3',
	translate('magicSettings', 'pounds per board foot'): 'lb/boardfoot',
	translate('magicSettings', 'pounds per wood piece'): 'lb/piece' # no comma
}

# add new items only at the end and change self.oWoodPriceCalculationList
getWoodPriceCalculation = {
	translate('magicSettings', 'price per area in m^2'): 'm^2',
	translate('magicSettings', 'price per volume in m^3'): 'm^3',
	translate('magicSettings', 'price per wood piece'): 'piece',
	translate('magicSettings', 'price per area in ft^2'): 'ft^2',
	translate('magicSettings', 'price per cubic foot'): 'ft^3',
	translate('magicSettings', 'price per cubic inch'): 'in^3',
	translate('magicSettings', 'price per board foot'): 'boardfoot' # no comma
}

# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):

		# ############################################################################
		# globals
		# ############################################################################
		
		toolSW = 450
		toolSH = 600
		gTheme = MagicPanels.gTheme
		gWoodWeightCalculation = MagicPanels.gWoodWeightCalculation
		gWoodPriceCalculation = MagicPanels.gWoodPriceCalculation
		gPage = 0
		
		# ############################################################################
		# init
		# ############################################################################

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('magicSettings', 'magicSettings'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			
			self.setMinimumSize(self.toolSW, self.toolSH)
			
			# ############################################################################
			# pages
			# ############################################################################

			# not write here, copy text from getMenuIndex1 to avoid typo
			self.sPageList = (
				translate('magicSettings', 'Settings - page 1'), 
				translate('magicSettings', 'Settings - page 2'), 
				translate('magicSettings', 'Settings - page 3'), 
				translate('magicSettings', 'Settings - page 4'), 
				translate('magicSettings', 'Settings - page 5'),
				translate('magicSettings', 'Settings - page 6') # no comma 
			)
			
			self.sPage = QtGui.QComboBox(self)
			self.sPage.addItems(self.sPageList)
			self.sPage.setCurrentIndex(self.gPage)
			self.sPage.textActivated[str].connect(self.showPage)
			self.sPage.setMinimumWidth(150)
			
			# ############################################################################
			# page 1
			# ############################################################################

			# theme
			self.oThemeL = QtGui.QLabel(translate('magicSettings', 'Theme:'), self)
			self.oThemeList = MagicPanels.getTheme("config")
			self.oTheme = QtGui.QComboBox(self)
			self.oTheme.addItems(self.oThemeList)
			self.oTheme.setCurrentIndex(0) # default
			self.oTheme.textActivated[str].connect(self.setThemeType)
			self.oTheme.setMinimumWidth(150)
			
			# main window theme
			self.oMainWindowThemeL = QtGui.QLabel(translate('magicSettings', 'Main window theme:'), self)
			
			self.oMainWindowThemeRB1 = QtGui.QRadioButton(self)
			self.oMainWindowThemeRB1.setText(translate('magicSettings', 'yes'))
			self.oMainWindowThemeRB1.toggled.connect(self.doNothing)

			self.oMainWindowThemeRB2 = QtGui.QRadioButton(self)
			self.oMainWindowThemeRB2.setText(translate('magicSettings', 'no'))
			self.oMainWindowThemeRB2.toggled.connect(self.doNothing)

			self.oMainWindowThemeGRP = QtGui.QButtonGroup(self)
			self.oMainWindowThemeGRP.addButton(self.oMainWindowThemeRB1)
			self.oMainWindowThemeGRP.addButton(self.oMainWindowThemeRB2)

			# wood thickness
			self.oWoodThicknessL = QtGui.QLabel(translate('magicSettings', 'Wood thickness:'), self)
			self.oWoodThicknessE = QtGui.QLineEdit(self)
			self.oWoodThicknessE.setText(MagicPanels.unit2gui(0))
			
			# wood long size
			self.oWoodSizeXL = QtGui.QLabel(translate('magicSettings', 'Wood size X (long):'), self)
			self.oWoodSizeXE = QtGui.QLineEdit(self)
			self.oWoodSizeXE.setText(MagicPanels.unit2gui(0))
			
			# wood short size
			self.oWoodSizeYL = QtGui.QLabel(translate('magicSettings', 'Wood size Y (short):'), self)
			self.oWoodSizeYE = QtGui.QLineEdit(self)
			self.oWoodSizeYE.setText(MagicPanels.unit2gui(0))
			
			# wood description
			self.oWoodDescriptionL = QtGui.QLabel(translate('magicSettings', 'Wood description:'), self)
			self.oWoodDescriptionE = QtGui.QLineEdit(self)
			self.oWoodDescriptionE.setText("0")
			
			# wood weight
			self.oWoodWeightL = QtGui.QLabel(translate('magicSettings', 'Wood weight:'), self)
			self.oWoodWeightE = QtGui.QLineEdit(self)
			self.oWoodWeightE.setText("0")
			
			# wood price calculation
			self.oWoodWeightCalculationL = QtGui.QLabel(translate('magicSettings', 'Wood weight calculation:'), self)
			self.oWoodWeightCalculationList = (
				translate('magicSettings', 'kg per area in m^2'),
				translate('magicSettings', 'kg per volume in m^3'),
				translate('magicSettings', 'kg per wood piece'),
				translate('magicSettings', 'pounds per area in ft^2'),
				translate('magicSettings', 'pounds per cubic foot'),
				translate('magicSettings', 'pounds per cubic inch'),
				translate('magicSettings', 'pounds per board foot'),
				translate('magicSettings', 'pounds per wood piece') # no comma
			)
			self.oWoodWeightCalculationE = QtGui.QComboBox(self)
			self.oWoodWeightCalculationE.addItems(self.oWoodWeightCalculationList)
			self.oWoodWeightCalculationE.setCurrentIndex(0) # default
			self.oWoodWeightCalculationE.textActivated[str].connect(self.setWoodWeightCalculation)
			
			# wood price
			self.oWoodPriceL = QtGui.QLabel(translate('magicSettings', 'Wood price:'), self)
			self.oWoodPriceE = QtGui.QLineEdit(self)
			self.oWoodPriceE.setText("0")
			
			# wood price symbol
			self.oWoodPriceSymbolL = QtGui.QLabel(translate('magicSettings', 'Wood price symbol:'), self)
			self.oWoodPriceSymbolE = QtGui.QLineEdit(self)
			self.oWoodPriceSymbolE.setText("0")
			
			# wood price calculation
			self.oWoodPriceCalculationL = QtGui.QLabel(translate('magicSettings', 'Wood price calculation:'), self)
			self.oWoodPriceCalculationList = (
				translate('magicSettings', 'price per area in m^2'),
				translate('magicSettings', 'price per volume in m^3'),
				translate('magicSettings', 'price per wood piece'),
				translate('magicSettings', 'price per area in ft^2'),
				translate('magicSettings', 'price per cubic foot'),
				translate('magicSettings', 'price per cubic inch'),
				translate('magicSettings', 'price per board foot') # no comma
			)
			self.oWoodPriceCalculationE = QtGui.QComboBox(self)
			self.oWoodPriceCalculationE.addItems(self.oWoodPriceCalculationList)
			self.oWoodPriceCalculationE.setCurrentIndex(0) # default
			self.oWoodPriceCalculationE.textActivated[str].connect(self.setWoodPriceCalculation)
			
			# wood color
			self.oWoodColorRL = QtGui.QLabel(translate('magicSettings', 'Wood color (red):'), self)
			self.oWoodColorRE = QtGui.QLineEdit(self)
			self.oWoodColorRE.setText("0")
			
			self.oWoodColorGL = QtGui.QLabel(translate('magicSettings', 'Wood color (green):'), self)
			self.oWoodColorGE = QtGui.QLineEdit(self)
			self.oWoodColorGE.setText("0")
			
			self.oWoodColorBL = QtGui.QLabel(translate('magicSettings', 'Wood color (blue):'), self)
			self.oWoodColorBE = QtGui.QLineEdit(self)
			self.oWoodColorBE.setText("0")
			
			self.oWoodColorAL = QtGui.QLabel(translate('magicSettings', 'Wood color (alpha channel):'), self)
			self.oWoodColorAE = QtGui.QLineEdit(self)
			self.oWoodColorAE.setText("0")
			
			# window stays on top
			self.oWindowL = QtGui.QLabel(translate('magicSettings', 'Window stays on top:'), self)
			
			self.oWindowRB1 = QtGui.QRadioButton(self)
			self.oWindowRB1.setText(translate('magicSettings', 'yes'))
			self.oWindowRB1.toggled.connect(self.doNothing)

			self.oWindowRB2 = QtGui.QRadioButton(self)
			self.oWindowRB2.setText(translate('magicSettings', 'no'))
			self.oWindowRB2.toggled.connect(self.doNothing)

			self.oWindowGRP = QtGui.QButtonGroup(self)
			self.oWindowGRP.addButton(self.oWindowRB1)
			self.oWindowGRP.addButton(self.oWindowRB2)
			
			# current selection
			self.oCurrentSelectionL = QtGui.QLabel(translate('magicSettings', 'Current selection:'), self)
			
			self.oCurrentSelectionRB1 = QtGui.QRadioButton(self)
			self.oCurrentSelectionRB1.setText(translate('magicSettings', 'yes'))
			self.oCurrentSelectionRB1.toggled.connect(self.doNothing)

			self.oCurrentSelectionRB2 = QtGui.QRadioButton(self)
			self.oCurrentSelectionRB2.setText(translate('magicSettings', 'no'))
			self.oCurrentSelectionRB2.toggled.connect(self.doNothing)
			
			self.oCurrentSelectionGRP = QtGui.QButtonGroup(self)
			self.oCurrentSelectionGRP.addButton(self.oCurrentSelectionRB1)
			self.oCurrentSelectionGRP.addButton(self.oCurrentSelectionRB2)
			
			# ############################################################################
			# page 2
			# ############################################################################

			# front inside wood thickness
			self.oFrontInsideThicknessL = QtGui.QLabel(translate('magicSettings', 'Front inside thickness:'), self)
			self.oFrontInsideThicknessE = QtGui.QLineEdit(self)
			self.oFrontInsideThicknessE.setText(MagicPanels.unit2gui(0))
			
			# front inside offset left
			self.oFrontInsideOffsetLL = QtGui.QLabel(translate('magicSettings', 'Front inside offset left:'), self)
			self.oFrontInsideOffsetLE = QtGui.QLineEdit(self)
			self.oFrontInsideOffsetLE.setText(MagicPanels.unit2gui(0))
			
			# front inside offset right
			self.oFrontInsideOffsetRL = QtGui.QLabel(translate('magicSettings', 'Front inside offset right:'), self)
			self.oFrontInsideOffsetRE = QtGui.QLineEdit(self)
			self.oFrontInsideOffsetRE.setText(MagicPanels.unit2gui(0))
			
			# front inside offset bottom
			self.oFrontInsideOffsetBL = QtGui.QLabel(translate('magicSettings', 'Front inside offset bottom:'), self)
			self.oFrontInsideOffsetBE = QtGui.QLineEdit(self)
			self.oFrontInsideOffsetBE.setText(MagicPanels.unit2gui(0))
			
			# front inside offset top
			self.oFrontInsideOffsetTL = QtGui.QLabel(translate('magicSettings', 'Front inside offset top:'), self)
			self.oFrontInsideOffsetTE = QtGui.QLineEdit(self)
			self.oFrontInsideOffsetTE.setText(MagicPanels.unit2gui(0))
			
			# front outside wood thickness
			self.oFrontOutsideThicknessL = QtGui.QLabel(translate('magicSettings', 'Front outside thickness:'), self)
			self.oFrontOutsideThicknessE = QtGui.QLineEdit(self)
			self.oFrontOutsideThicknessE.setText(MagicPanels.unit2gui(0))
			
			# front outside overlap left
			self.oFrontOutsideOffsetLL = QtGui.QLabel(translate('magicSettings', 'Front outside overlap left:'), self)
			self.oFrontOutsideOffsetLE = QtGui.QLineEdit(self)
			self.oFrontOutsideOffsetLE.setText(MagicPanels.unit2gui(0))
			
			# front outside overlap right
			self.oFrontOutsideOffsetRL = QtGui.QLabel(translate('magicSettings', 'Front outside overlap right:'), self)
			self.oFrontOutsideOffsetRE = QtGui.QLineEdit(self)
			self.oFrontOutsideOffsetRE.setText(MagicPanels.unit2gui(0))
			
			# front outside overlap bottom
			self.oFrontOutsideOffsetBL = QtGui.QLabel(translate('magicSettings', 'Front outside overlap bottom:'), self)
			self.oFrontOutsideOffsetBE = QtGui.QLineEdit(self)
			self.oFrontOutsideOffsetBE.setText(MagicPanels.unit2gui(0))
			
			# front outside overlap top
			self.oFrontOutsideOffsetTL = QtGui.QLabel(translate('magicSettings', 'Front outside overlap top:'), self)
			self.oFrontOutsideOffsetTE = QtGui.QLineEdit(self)
			self.oFrontOutsideOffsetTE.setText(MagicPanels.unit2gui(0))

			# shelf wood thickness
			self.oShelfThicknessL = QtGui.QLabel(translate('magicSettings', 'Shelf thickness:'), self)
			self.oShelfThicknessE = QtGui.QLineEdit(self)
			self.oShelfThicknessE.setText(MagicPanels.unit2gui(0))
			
			# shelf offset sides
			self.oShelfOffsetSidesL = QtGui.QLabel(translate('magicSettings', 'Shelf sides offset:'), self)
			self.oShelfOffsetSidesE = QtGui.QLineEdit(self)
			self.oShelfOffsetSidesE.setText(MagicPanels.unit2gui(0))
			
			# back inside wood thickness
			self.oBackIThicknessL = QtGui.QLabel(translate('magicSettings', 'Back inside thickness:'), self)
			self.oBackIThicknessE = QtGui.QLineEdit(self)
			self.oBackIThicknessE.setText(MagicPanels.unit2gui(0))
			
			# back outside wood thickness
			self.oBackOThicknessL = QtGui.QLabel(translate('magicSettings', 'Back outside thickness:'), self)
			self.oBackOThicknessE = QtGui.QLineEdit(self)
			self.oBackOThicknessE.setText(MagicPanels.unit2gui(0))
			
			# ############################################################################
			# page 3
			# ############################################################################

			# edgeband thickness
			self.oEdgebandThickL = QtGui.QLabel(translate('magicSettings', 'Veneer thickness:'), self)
			self.oEdgebandThickE = QtGui.QLineEdit(self)
			self.oEdgebandThickE.setText("0")
			
			# edgeband apply way
			self.oEdgebandApplyL = QtGui.QLabel(translate('magicSettings', 'Veneer apply:'), self)
			
			self.oEdgebandApplyRB1 = QtGui.QRadioButton(self)
			self.oEdgebandApplyRB1.setText(translate('magicSettings', 'everywhere'))
			self.oEdgebandApplyRB1.toggled.connect(self.doNothing)

			self.oEdgebandApplyRB2 = QtGui.QRadioButton(self)
			self.oEdgebandApplyRB2.setText(translate('magicSettings', 'visible'))
			self.oEdgebandApplyRB2.toggled.connect(self.doNothing)

			self.oEdgebandApplyGRP = QtGui.QButtonGroup(self)
			self.oEdgebandApplyGRP.addButton(self.oEdgebandApplyRB1)
			self.oEdgebandApplyGRP.addButton(self.oEdgebandApplyRB2)
			
			# edgeband color
			self.oEdgebandColorRL = QtGui.QLabel(translate('magicSettings', 'Veneer color (red):'), self)
			self.oEdgebandColorRE = QtGui.QLineEdit(self)
			self.oEdgebandColorRE.setText("0")
			
			self.oEdgebandColorGL = QtGui.QLabel(translate('magicSettings', 'Veneer color (green):'), self)
			self.oEdgebandColorGE = QtGui.QLineEdit(self)
			self.oEdgebandColorGE.setText("0")
			
			self.oEdgebandColorBL = QtGui.QLabel(translate('magicSettings', 'Veneer color (blue):'), self)
			self.oEdgebandColorBE = QtGui.QLineEdit(self)
			self.oEdgebandColorBE.setText("0")
			
			self.oEdgebandColorAL = QtGui.QLabel(translate('magicSettings', 'Veneer color (alpha channel):'), self)
			self.oEdgebandColorAE = QtGui.QLineEdit(self)
			self.oEdgebandColorAE.setText("0")
			
			# ############################################################################
			# page 4
			# ############################################################################

			# gPreferCustomSettings
			self.oPreferCustomSettingsL = QtGui.QLabel(translate('magicSettings', 'Prefer magicSettings defaults:'), self)
			
			self.oPreferCustomSettingsRB1 = QtGui.QRadioButton(self)
			self.oPreferCustomSettingsRB1.setText(translate('magicSettings', 'yes'))
			self.oPreferCustomSettingsRB1.toggled.connect(self.doNothing)

			self.oPreferCustomSettingsRB2 = QtGui.QRadioButton(self)
			self.oPreferCustomSettingsRB2.setText(translate('magicSettings', 'no'))
			self.oPreferCustomSettingsRB2.toggled.connect(self.doNothing)
			
			self.oPreferCustomSettingsGRP = QtGui.QButtonGroup(self)
			self.oPreferCustomSettingsGRP.addButton(self.oPreferCustomSettingsRB1)
			self.oPreferCustomSettingsGRP.addButton(self.oPreferCustomSettingsRB2)

			# gOffsetSides
			self.oOffsetSidesL = QtGui.QLabel(translate('magicSettings', 'Sides:'), self)
			self.oOffsetSidesE = QtGui.QLineEdit(self)
			self.oOffsetSidesE.setText("0")
			
			# gOffsetItemsPerSide
			self.oOffsetItemsPerSideL = QtGui.QLabel(translate('magicSettings', 'Items per side:'), self)
			self.oOffsetItemsPerSideE = QtGui.QLineEdit(self)
			self.oOffsetItemsPerSideE.setText("0")
			
			# gOffsetFromCorner
			self.oOffsetFromCornerL = QtGui.QLabel(translate('magicSettings', 'Offset from corner:'), self)
			self.oOffsetFromCornerE = QtGui.QLineEdit(self)
			self.oOffsetFromCornerE.setText("0")
			
			# gOffsetBetween
			self.oOffsetBetweenL = QtGui.QLabel(translate('magicSettings', 'Offset between items:'), self)
			self.oOffsetBetweenE = QtGui.QLineEdit(self)
			self.oOffsetBetweenE.setText("0")
			
			# gOffsetFromEdge
			self.oOffsetFromEdgeL = QtGui.QLabel(translate('magicSettings', 'Offset from edge:'), self)
			self.oOffsetFromEdgeE = QtGui.QLineEdit(self)
			self.oOffsetFromEdgeE.setText("0")
			
			# ############################################################################
			# page 5
			# ############################################################################

			# gDowelDiameter
			self.oDowelDiameterL = QtGui.QLabel(translate('magicSettings', 'Dowel diameter:'), self)
			self.oDowelDiameterE = QtGui.QLineEdit(self)
			self.oDowelDiameterE.setText("0")
			
			# gDowelSize
			self.oDowelSizeL = QtGui.QLabel(translate('magicSettings', 'Dowel size:'), self)
			self.oDowelSizeE = QtGui.QLineEdit(self)
			self.oDowelSizeE.setText("0")
			
			# gDowelSink
			self.oDowelSinkL = QtGui.QLabel(translate('magicSettings', 'Dowel sink:'), self)
			self.oDowelSinkE = QtGui.QLineEdit(self)
			self.oDowelSinkE.setText("0")
			
			# gHoleDiameter
			self.oHoleDiameterL = QtGui.QLabel(translate('magicSettings', 'Hole diameter:'), self)
			self.oHoleDiameterE = QtGui.QLineEdit(self)
			self.oHoleDiameterE.setText("0")
			
			# gHoleCountersinkDiameter
			self.oHoleCountersinkDiameterL = QtGui.QLabel(translate('magicSettings', 'Hole countersink diameter:'), self)
			self.oHoleCountersinkDiameterE = QtGui.QLineEdit(self)
			self.oHoleCountersinkDiameterE.setText("0")
			
			# gHoleSize
			self.oHoleSizeL = QtGui.QLabel(translate('magicSettings', 'Hole size:'), self)
			self.oHoleSizeE = QtGui.QLineEdit(self)
			self.oHoleSizeE.setText("0")
			
			# gDrillSpike
			self.oDrillSpikeL = QtGui.QLabel(translate('magicSettings', 'Hole spike:'), self)
			self.oDrillSpikeE = QtGui.QLineEdit(self)
			self.oDrillSpikeE.setText("")
			
			# gPocketDiameter
			self.oPocketDiameterL = QtGui.QLabel(translate('magicSettings', 'Pocket diameter:'), self)
			self.oPocketDiameterE = QtGui.QLineEdit(self)
			self.oPocketDiameterE.setText("0")
			
			# gPocketCountersinkDiameter
			self.oPocketCountersinkDiameterL = QtGui.QLabel(translate('magicSettings', 'Pocket countersink:'), self)
			self.oPocketCountersinkDiameterE = QtGui.QLineEdit(self)
			self.oPocketCountersinkDiameterE.setText("0")
			
			# gPocketSize
			self.oPocketSizeL = QtGui.QLabel(translate('magicSettings', 'Pocket size:'), self)
			self.oPocketSizeE = QtGui.QLineEdit(self)
			self.oPocketSizeE.setText("0")
		
			# gPocketOffsetFromEdge
			self.oPocketOffsetFromEdgeL = QtGui.QLabel(translate('magicSettings', 'Pocket offset from edge:'), self)
			self.oPocketOffsetFromEdgeE = QtGui.QLineEdit(self)
			self.oPocketOffsetFromEdgeE.setText("0")
			
			# gPocketRotation
			self.oPocketRotationL = QtGui.QLabel(translate('magicSettings', 'Pocket rotation:'), self)
			self.oPocketRotationE = QtGui.QLineEdit(self)
			self.oPocketRotationE.setText("0")
			
			# gPocketSink
			self.oPocketSinkL = QtGui.QLabel(translate('magicSettings', 'Pocket sink:'), self)
			self.oPocketSinkE = QtGui.QLineEdit(self)
			self.oPocketSinkE.setText("0")

			# ############################################################################
			# save settings
			# ############################################################################
			
			# status
			self.oStatusL = QtGui.QLabel("", self)
			
			# button
			self.oSaveB = QtGui.QPushButton(translate('magicSettings', 'save settings'), self)
			self.oSaveB.clicked.connect(self.saveSettings)
			self.oSaveB.setFixedHeight(40)
			
			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.PageSelection = QtGui.QVBoxLayout()
			self.PageSelection.addWidget(self.sPage)
			
			self.Page11 = QtGui.QGridLayout()
			self.Page11.addWidget(self.oThemeL, 0, 0)
			self.Page11.addWidget(self.oTheme, 0, 1)
			self.Page11mw = QtGui.QGridLayout()
			self.Page11mw.addWidget(self.oMainWindowThemeL, 0, 0)
			self.Page11mw.addWidget(self.oMainWindowThemeRB1, 0, 1)
			self.Page11mw.addWidget(self.oMainWindowThemeRB2, 0, 2)
			self.layTheme = QtGui.QVBoxLayout()
			self.layTheme.addLayout(self.Page11)
			self.layTheme.addLayout(self.Page11mw)
			self.groupPage11 = QtGui.QGroupBox(None, self)
			self.groupPage11.setLayout(self.layTheme)
			
			self.Page12 = QtGui.QGridLayout()
			self.Page12.addWidget(self.oWoodThicknessL, 0, 0)
			self.Page12.addWidget(self.oWoodThicknessE, 0, 1)
			self.Page12.addWidget(self.oWoodSizeXL, 1, 0)
			self.Page12.addWidget(self.oWoodSizeXE, 1, 1)
			self.Page12.addWidget(self.oWoodSizeYL, 2, 0)
			self.Page12.addWidget(self.oWoodSizeYE, 2, 1)
			self.Page12.addWidget(self.oWoodDescriptionL, 3, 0)
			self.Page12.addWidget(self.oWoodDescriptionE, 3, 1)
			self.groupPage12 = QtGui.QGroupBox(None, self)
			self.groupPage12.setLayout(self.Page12)
			
			self.Page13 = QtGui.QGridLayout()
			self.Page13.addWidget(self.oWoodWeightL, 0, 0)
			self.Page13.addWidget(self.oWoodWeightE, 0, 1)
			self.Page13.addWidget(self.oWoodWeightCalculationL, 1, 0)
			self.Page13.addWidget(self.oWoodWeightCalculationE, 1, 1)
			self.groupPage13 = QtGui.QGroupBox(None, self)
			self.groupPage13.setLayout(self.Page13)
			
			self.Page14 = QtGui.QGridLayout()
			self.Page14.addWidget(self.oWoodPriceL, 0, 0)
			self.Page14.addWidget(self.oWoodPriceE, 0, 1)
			self.Page14.addWidget(self.oWoodPriceSymbolL, 1, 0)
			self.Page14.addWidget(self.oWoodPriceSymbolE, 1, 1)
			self.Page14.addWidget(self.oWoodPriceCalculationL, 2, 0)
			self.Page14.addWidget(self.oWoodPriceCalculationE, 2, 1)
			self.groupPage14 = QtGui.QGroupBox(None, self)
			self.groupPage14.setLayout(self.Page14)
		
			self.Page15 = QtGui.QGridLayout()
			self.Page15.addWidget(self.oWoodColorRL, 0, 0)
			self.Page15.addWidget(self.oWoodColorRE, 0, 1)
			self.Page15.addWidget(self.oWoodColorGL, 1, 0)
			self.Page15.addWidget(self.oWoodColorGE, 1, 1)
			self.Page15.addWidget(self.oWoodColorBL, 2, 0)
			self.Page15.addWidget(self.oWoodColorBE, 2, 1)
			self.Page15.addWidget(self.oWoodColorAL, 3, 0)
			self.Page15.addWidget(self.oWoodColorAE, 3, 1)
			self.groupPage15 = QtGui.QGroupBox(None, self)
			self.groupPage15.setLayout(self.Page15)

			self.Page16 = QtGui.QGridLayout()
			self.Page16.addWidget(self.oWindowL, 0, 0)
			self.Page16.addWidget(self.oWindowRB1, 0, 1)
			self.Page16.addWidget(self.oWindowRB2, 0, 2)
			self.Page16.addWidget(self.oCurrentSelectionL, 1, 0)
			self.Page16.addWidget(self.oCurrentSelectionRB1, 1, 1)
			self.Page16.addWidget(self.oCurrentSelectionRB2, 1, 2)
			self.groupPage16 = QtGui.QGroupBox(None, self)
			self.groupPage16.setLayout(self.Page16)

			self.Page21 = QtGui.QGridLayout()
			self.Page21.addWidget(self.oFrontInsideThicknessL, 0, 0)
			self.Page21.addWidget(self.oFrontInsideThicknessE, 0, 1)
			self.Page21.addWidget(self.oFrontInsideOffsetLL, 1, 0)
			self.Page21.addWidget(self.oFrontInsideOffsetLE, 1, 1)
			self.Page21.addWidget(self.oFrontInsideOffsetRL, 2, 0)
			self.Page21.addWidget(self.oFrontInsideOffsetRE, 2, 1)
			self.Page21.addWidget(self.oFrontInsideOffsetBL, 3, 0)
			self.Page21.addWidget(self.oFrontInsideOffsetBE, 3, 1)
			self.Page21.addWidget(self.oFrontInsideOffsetTL, 4, 0)
			self.Page21.addWidget(self.oFrontInsideOffsetTE, 4, 1)
			self.groupPage21 = QtGui.QGroupBox(None, self)
			self.groupPage21.setLayout(self.Page21)

			self.Page22 = QtGui.QGridLayout()
			self.Page22.addWidget(self.oFrontOutsideThicknessL, 0, 0)
			self.Page22.addWidget(self.oFrontOutsideThicknessE, 0, 1)
			self.Page22.addWidget(self.oFrontOutsideOffsetLL, 1, 0)
			self.Page22.addWidget(self.oFrontOutsideOffsetLE, 1, 1)
			self.Page22.addWidget(self.oFrontOutsideOffsetRL, 2, 0)
			self.Page22.addWidget(self.oFrontOutsideOffsetRE, 2, 1)
			self.Page22.addWidget(self.oFrontOutsideOffsetBL, 3, 0)
			self.Page22.addWidget(self.oFrontOutsideOffsetBE, 3, 1)
			self.Page22.addWidget(self.oFrontOutsideOffsetTL, 4, 0)
			self.Page22.addWidget(self.oFrontOutsideOffsetTE, 4, 1)
			self.groupPage22 = QtGui.QGroupBox(None, self)
			self.groupPage22.setLayout(self.Page22)

			self.Page23 = QtGui.QGridLayout()
			self.Page23.addWidget(self.oShelfThicknessL, 0, 0)
			self.Page23.addWidget(self.oShelfThicknessE, 0, 1)
			self.Page23.addWidget(self.oShelfOffsetSidesL, 1, 0)
			self.Page23.addWidget(self.oShelfOffsetSidesE, 1, 1)
			self.Page23.addWidget(self.oBackIThicknessL, 2, 0)
			self.Page23.addWidget(self.oBackIThicknessE, 2, 1)
			self.Page23.addWidget(self.oBackOThicknessL, 3, 0)
			self.Page23.addWidget(self.oBackOThicknessE, 3, 1)
			self.groupPage23 = QtGui.QGroupBox(None, self)
			self.groupPage23.setLayout(self.Page23)
			
			self.Page31 = QtGui.QGridLayout()
			self.Page31.addWidget(self.oEdgebandThickL, 0, 0)
			self.Page31.addWidget(self.oEdgebandThickE, 0, 1)
			self.Page31.addWidget(self.oEdgebandApplyL, 1, 0)
			self.Page31.addWidget(self.oEdgebandApplyRB1, 1, 1)
			self.Page31.addWidget(self.oEdgebandApplyRB2, 1, 2)
			self.groupPage31 = QtGui.QGroupBox(None, self)
			self.groupPage31.setLayout(self.Page31)

			self.Page32 = QtGui.QGridLayout()
			self.Page32.addWidget(self.oEdgebandColorRL, 0, 0)
			self.Page32.addWidget(self.oEdgebandColorRE, 0, 1)
			self.Page32.addWidget(self.oEdgebandColorGL, 1, 0)
			self.Page32.addWidget(self.oEdgebandColorGE, 1, 1)
			self.Page32.addWidget(self.oEdgebandColorBL, 2, 0)
			self.Page32.addWidget(self.oEdgebandColorBE, 2, 1)
			self.Page32.addWidget(self.oEdgebandColorAL, 3, 0)
			self.Page32.addWidget(self.oEdgebandColorAE, 3, 1)
			self.groupPage32 = QtGui.QGroupBox(None, self)
			self.groupPage32.setLayout(self.Page32)

			self.Page41 = QtGui.QGridLayout()
			self.Page41.addWidget(self.oPreferCustomSettingsL, 0, 0)
			self.Page41.addWidget(self.oPreferCustomSettingsRB1, 0, 1)
			self.Page41.addWidget(self.oPreferCustomSettingsRB2, 0, 2)
			self.groupPage41 = QtGui.QGroupBox(None, self)
			self.groupPage41.setLayout(self.Page41)
	
			self.Page42 = QtGui.QGridLayout()
			self.Page42.addWidget(self.oOffsetSidesL, 0, 0)
			self.Page42.addWidget(self.oOffsetSidesE, 0, 1)
			self.Page42.addWidget(self.oOffsetItemsPerSideL, 1, 0)
			self.Page42.addWidget(self.oOffsetItemsPerSideE, 1, 1)
			self.Page42.addWidget(self.oOffsetFromCornerL, 2, 0)
			self.Page42.addWidget(self.oOffsetFromCornerE, 2, 1)
			self.Page42.addWidget(self.oOffsetBetweenL, 3, 0)
			self.Page42.addWidget(self.oOffsetBetweenE, 3, 1)
			self.Page42.addWidget(self.oOffsetFromEdgeL, 4, 0)
			self.Page42.addWidget(self.oOffsetFromEdgeE, 4, 1)
			self.groupPage42 = QtGui.QGroupBox(None, self)
			self.groupPage42.setLayout(self.Page42)

			self.Page51 = QtGui.QGridLayout()
			self.Page51.addWidget(self.oDowelDiameterL, 0, 0)
			self.Page51.addWidget(self.oDowelDiameterE, 0, 1)
			self.Page51.addWidget(self.oDowelSizeL, 1, 0)
			self.Page51.addWidget(self.oDowelSizeE, 1, 1)
			self.Page51.addWidget(self.oDowelSinkL, 2, 0)
			self.Page51.addWidget(self.oDowelSinkE, 2, 1)
			self.groupPage51 = QtGui.QGroupBox(None, self)
			self.groupPage51.setLayout(self.Page51)

			self.Page52 = QtGui.QGridLayout()
			self.Page52.addWidget(self.oHoleDiameterL, 0, 0)
			self.Page52.addWidget(self.oHoleDiameterE, 0, 1)
			self.Page52.addWidget(self.oHoleCountersinkDiameterL, 1, 0)
			self.Page52.addWidget(self.oHoleCountersinkDiameterE, 1, 1)
			self.Page52.addWidget(self.oHoleSizeL, 2, 0)
			self.Page52.addWidget(self.oHoleSizeE, 2, 1)
			self.Page52.addWidget(self.oDrillSpikeL, 3, 0)
			self.Page52.addWidget(self.oDrillSpikeE, 3, 1)
			self.groupPage52 = QtGui.QGroupBox(None, self)
			self.groupPage52.setLayout(self.Page52)

			self.Page53 = QtGui.QGridLayout()
			self.Page53.addWidget(self.oPocketDiameterL, 0, 0)
			self.Page53.addWidget(self.oPocketDiameterE, 0, 1)
			self.Page53.addWidget(self.oPocketCountersinkDiameterL, 1, 0)
			self.Page53.addWidget(self.oPocketCountersinkDiameterE, 1, 1)
			self.Page53.addWidget(self.oPocketSizeL, 2, 0)
			self.Page53.addWidget(self.oPocketSizeE, 2, 1)
			self.Page53.addWidget(self.oPocketOffsetFromEdgeL, 3, 0)
			self.Page53.addWidget(self.oPocketOffsetFromEdgeE, 3, 1)
			self.Page53.addWidget(self.oPocketRotationL, 4, 0)
			self.Page53.addWidget(self.oPocketRotationE, 4, 1)
			self.Page53.addWidget(self.oPocketSinkL, 5, 0)
			self.Page53.addWidget(self.oPocketSinkE, 5, 1)
			self.groupPage53 = QtGui.QGroupBox(None, self)
			self.groupPage53.setLayout(self.Page53)

			self.Save = QtGui.QVBoxLayout()
			self.Save.addWidget(self.oStatusL)
			self.Save.addWidget(self.oSaveB)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			self.layout.addLayout(self.PageSelection)
			self.layout.addStretch()
			self.layout.addWidget(self.groupPage11)
			self.layout.addWidget(self.groupPage12)
			self.layout.addWidget(self.groupPage13)
			self.layout.addWidget(self.groupPage14)
			self.layout.addWidget(self.groupPage15)
			self.layout.addWidget(self.groupPage16)
			self.layout.addWidget(self.groupPage21)
			self.layout.addWidget(self.groupPage22)
			self.layout.addWidget(self.groupPage23)
			self.layout.addWidget(self.groupPage31)
			self.layout.addWidget(self.groupPage32)
			self.layout.addWidget(self.groupPage41)
			self.layout.addWidget(self.groupPage42)
			self.layout.addWidget(self.groupPage51)
			self.layout.addWidget(self.groupPage52)
			self.layout.addWidget(self.groupPage53)
			self.layout.addStretch()
			self.layout.addLayout(self.Save)
			self.setLayout(self.layout)
			
			# init
			self.groupPage11.show()
			self.groupPage12.show()
			self.groupPage13.hide()
			self.groupPage14.hide()
			self.groupPage15.show()
			self.groupPage16.show()
			self.groupPage21.hide()
			self.groupPage22.hide()
			self.groupPage23.hide()
			self.groupPage31.hide()
			self.groupPage32.hide()
			self.groupPage41.hide()
			self.groupPage42.hide()
			self.groupPage51.hide()
			self.groupPage52.hide()
			self.groupPage53.hide()
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)
			
			# show window
			self.show()

			MagicPanels.adjustGUI(self, "center")
			
			# init
			self.getSettings()
			
		# ############################################################################
		# functions
		# ############################################################################
		
		# ############################################################################
		def doNothing(self):
			skip = 1

		def setWoodWeightCalculation(self, selectedText):
			self.gWoodWeightCalculation = getWoodWeightCalculation[selectedText]
			
		def setWoodPriceCalculation(self, selectedText):
			self.gWoodPriceCalculation = getWoodPriceCalculation[selectedText]

		def showPage(self, selectedText):
			selectedIndex = getMenuIndex1[selectedText]
			self.gPage = selectedIndex
			
			if self.gPage == 0:
				self.groupPage11.show()
				self.groupPage12.show()
				self.groupPage13.hide()
				self.groupPage14.hide()
				self.groupPage15.show()
				self.groupPage16.show()
				self.groupPage21.hide()
				self.groupPage22.hide()
				self.groupPage23.hide()
				self.groupPage31.hide()
				self.groupPage32.hide()
				self.groupPage41.hide()
				self.groupPage42.hide()
				self.groupPage51.hide()
				self.groupPage52.hide()
				self.groupPage53.hide()
			
			if self.gPage == 1:
				self.groupPage11.hide()
				self.groupPage12.hide()
				self.groupPage13.show()
				self.groupPage14.show()
				self.groupPage15.hide()
				self.groupPage16.hide()
				self.groupPage21.hide()
				self.groupPage22.hide()
				self.groupPage23.hide()
				self.groupPage31.hide()
				self.groupPage32.hide()
				self.groupPage41.hide()
				self.groupPage42.hide()
				self.groupPage51.hide()
				self.groupPage52.hide()
				self.groupPage53.hide()
			
			if self.gPage == 2:
				self.groupPage11.hide()
				self.groupPage12.hide()
				self.groupPage13.hide()
				self.groupPage14.hide()
				self.groupPage15.hide()
				self.groupPage16.hide()
				self.groupPage21.show()
				self.groupPage22.show()
				self.groupPage23.show()
				self.groupPage31.hide()
				self.groupPage32.hide()
				self.groupPage41.hide()
				self.groupPage42.hide()
				self.groupPage51.hide()
				self.groupPage52.hide()
				self.groupPage53.hide()

			if self.gPage == 3:
				self.groupPage11.hide()
				self.groupPage12.hide()
				self.groupPage13.hide()
				self.groupPage14.hide()
				self.groupPage15.hide()
				self.groupPage16.hide()
				self.groupPage21.hide()
				self.groupPage22.hide()
				self.groupPage23.hide()
				self.groupPage31.show()
				self.groupPage32.show()
				self.groupPage41.hide()
				self.groupPage42.hide()
				self.groupPage51.hide()
				self.groupPage52.hide()
				self.groupPage53.hide()

			if self.gPage == 4:
				self.groupPage11.hide()
				self.groupPage12.hide()
				self.groupPage13.hide()
				self.groupPage14.hide()
				self.groupPage15.hide()
				self.groupPage16.hide()
				self.groupPage21.hide()
				self.groupPage22.hide()
				self.groupPage23.hide()
				self.groupPage31.hide()
				self.groupPage32.hide()
				self.groupPage41.show()
				self.groupPage42.show()
				self.groupPage51.hide()
				self.groupPage52.hide()
				self.groupPage53.hide()
			
			if self.gPage == 5:
				self.groupPage11.hide()
				self.groupPage12.hide()
				self.groupPage13.hide()
				self.groupPage14.hide()
				self.groupPage15.hide()
				self.groupPage16.hide()
				self.groupPage21.hide()
				self.groupPage22.hide()
				self.groupPage23.hide()
				self.groupPage31.hide()
				self.groupPage32.hide()
				self.groupPage41.hide()
				self.groupPage42.hide()
				self.groupPage51.show()
				self.groupPage52.show()
				self.groupPage53.show()
				
		# ############################################################################
		def getSettings(self):
			
			# ################################################################
			# page 1
			# ################################################################
			
			try:
				self.oTheme.setCurrentText(MagicPanels.gTheme)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gMainWindowTheme
				if val == True:
					self.oMainWindowThemeRB1.setChecked(True)
				else:
					self.oMainWindowThemeRB2.setChecked(True)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gWoodThickness
				val = MagicPanels.unit2gui(val)
				self.oWoodThicknessE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gWoodSizeX
				val = MagicPanels.unit2gui(val)
				self.oWoodSizeXE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gWoodSizeY
				val = MagicPanels.unit2gui(val)
				self.oWoodSizeYE.setText(val)
			except:
				skip = 1

			try:
				val = MagicPanels.gWoodDescription
				val = str(val)
				self.oWoodDescriptionE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gWoodWeight
				val = str(float(val))
				self.oWoodWeightE.setText(val)
			except:
				skip = 1
			
			try:
				k = [ key for key, val in getWoodWeightCalculation.items() if val == MagicPanels.gWoodWeightCalculation ][0]
				self.oWoodWeightCalculationE.setCurrentText(k)
			except:
				skip = 1

			try:
				val = MagicPanels.gWoodPrice
				val = str(float(val))
				self.oWoodPriceE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gWoodPriceSymbol
				val = str(val)
				self.oWoodPriceSymbolE.setText(val)
			except:
				skip = 1
			
			try:
				k = [ key for key, val in getWoodPriceCalculation.items() if val == MagicPanels.gWoodPriceCalculation ][0]
				self.oWoodPriceCalculationE.setCurrentText(k)
			except:
				skip = 1

			try:
				color = MagicPanels.gDefaultColor
				color = MagicPanels.convertColor(color, "RGBA")
				[ r, g, b, a ] = [ str(color[0]), str(color[1]), str(color[2]), str(color[3]) ]
				
				self.oWoodColorRE.setText(r)
				self.oWoodColorGE.setText(g)
				self.oWoodColorBE.setText(b)
				self.oWoodColorAE.setText(a)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gWindowStaysOnTop
				if val == True:
					self.oWindowRB1.setChecked(True)
				else:
					self.oWindowRB2.setChecked(True)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gCurrentSelection
				if val == True:
					self.oCurrentSelectionRB1.setChecked(True)
				else:
					self.oCurrentSelectionRB2.setChecked(True)
			except:
				skip = 1

			# ################################################################
			# page 2
			# ################################################################
			
			try:
				val = MagicPanels.gFrontInsideThickness
				val = MagicPanels.unit2gui(val)
				self.oFrontInsideThicknessE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gFrontInsideOffsetL
				val = MagicPanels.unit2gui(val)
				self.oFrontInsideOffsetLE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gFrontInsideOffsetR
				val = MagicPanels.unit2gui(val)
				self.oFrontInsideOffsetRE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gFrontInsideOffsetB
				val = MagicPanels.unit2gui(val)
				self.oFrontInsideOffsetBE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gFrontInsideOffsetT
				val = MagicPanels.unit2gui(val)
				self.oFrontInsideOffsetTE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gFrontOutsideThickness
				val = MagicPanels.unit2gui(val)
				self.oFrontOutsideThicknessE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gFrontOutsideOffsetL
				val = MagicPanels.unit2gui(val)
				self.oFrontOutsideOffsetLE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gFrontOutsideOffsetR
				val = MagicPanels.unit2gui(val)
				self.oFrontOutsideOffsetRE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gFrontOutsideOffsetB
				val = MagicPanels.unit2gui(val)
				self.oFrontOutsideOffsetBE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gFrontOutsideOffsetT
				val = MagicPanels.unit2gui(val)
				self.oFrontOutsideOffsetTE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gShelfThickness
				val = MagicPanels.unit2gui(val)
				self.oShelfThicknessE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gShelfOffsetSides
				val = MagicPanels.unit2gui(val)
				self.oShelfOffsetSidesE.setText(val)
			except:
				skip = 1

			try:
				val = MagicPanels.gBackInsideThickness
				val = MagicPanels.unit2gui(val)
				self.oBackIThicknessE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gBackOutsideThickness
				val = MagicPanels.unit2gui(val)
				self.oBackOThicknessE.setText(val)
			except:
				skip = 1
			
			# ################################################################
			# page 3
			# ################################################################
			
			try:
				edgebandThick = MagicPanels.gEdgebandThickness
				edgebandThick = MagicPanels.unit2gui(edgebandThick)
				self.oEdgebandThickE.setText(edgebandThick)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gEdgebandApply
				if val == "everywhere":
					self.oEdgebandApplyRB1.setChecked(True)
				else:
					self.oEdgebandApplyRB2.setChecked(True)
			except:
				skip = 1

			try:
				color = MagicPanels.gEdgebandColor
				color = MagicPanels.convertColor(color, "RGBA")
				[ r, g, b, a ] = [ str(color[0]), str(color[1]), str(color[2]), str(color[3]) ]
				
				self.oEdgebandColorRE.setText(r)
				self.oEdgebandColorGE.setText(g)
				self.oEdgebandColorBE.setText(b)
				self.oEdgebandColorAE.setText(a)
			except:
				skip = 1
			
			# ################################################################
			# page 4
			# ################################################################
			
			try:
				val = MagicPanels.gPreferCustomSettings
				if val == True:
					self.oPreferCustomSettingsRB1.setChecked(True)
				else:
					self.oPreferCustomSettingsRB2.setChecked(True)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gOffsetSides
				val = int(val)
				self.oOffsetSidesE.setText(str(val))
			except:
				skip = 1
			
			try:
				val = MagicPanels.gOffsetItemsPerSide
				val = int(val)
				self.oOffsetItemsPerSideE.setText(str(val))
			except:
				skip = 1
			
			try:
				val = MagicPanels.gOffsetFromCorner
				val = MagicPanels.unit2gui(val)
				self.oOffsetFromCornerE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gOffsetBetween
				val = MagicPanels.unit2gui(val)
				self.oOffsetBetweenE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gOffsetFromEdge
				val = MagicPanels.unit2gui(val)
				self.oOffsetFromEdgeE.setText(val)
			except:
				skip = 1
				
			# ################################################################
			# page 5
			# ################################################################
			
			try:
				val = MagicPanels.gDowelDiameter
				val = MagicPanels.unit2gui(val)
				self.oDowelDiameterE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gDowelSize
				val = MagicPanels.unit2gui(val)
				self.oDowelSizeE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gDowelSink
				val = MagicPanels.unit2gui(val)
				self.oDowelSinkE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gHoleDiameter
				val = MagicPanels.unit2gui(val)
				self.oHoleDiameterE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gHoleCountersinkDiameter
				val = MagicPanels.unit2gui(val)
				self.oHoleCountersinkDiameterE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gHoleSize
				val = MagicPanels.unit2gui(val)
				self.oHoleSizeE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gDrillSpike
				self.oDrillSpikeE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gPocketDiameter
				val = MagicPanels.unit2gui(val)
				self.oPocketDiameterE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gPocketCountersinkDiameter
				val = MagicPanels.unit2gui(val)
				self.oPocketCountersinkDiameterE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gPocketSize
				val = MagicPanels.unit2gui(val)
				self.oPocketSizeE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gPocketOffsetFromEdge
				val = MagicPanels.unit2gui(val)
				self.oPocketOffsetFromEdgeE.setText(val)
			except:
				skip = 1
			
			try:
				val = MagicPanels.gPocketRotation
				val = float(val)
				self.oPocketRotationE.setText(str(val))
			except:
				skip = 1
			
			try:
				val = MagicPanels.gPocketSink
				val = MagicPanels.unit2gui(val)
				self.oPocketSinkE.setText(val)
			except:
				skip = 1
			
		# ############################################################################
		def setThemeType(self, selectedText):
			
			self.gTheme = selectedText
			
			# set theme
			QtCSS = MagicPanels.getTheme(self.gTheme)
			self.setStyleSheet(QtCSS)
			
			if MagicPanels.gMainWindowTheme == True:
				FreeCADGui.getMainWindow().setStyleSheet(QtCSS)

		# ############################################################################
		def saveSettings(self):
			
			try:
				wus = FreeCAD.ParamGet(MagicPanels.gSettingsPref)
				
				# ################################################################
				# page 1
				# ################################################################
				
				wus.SetString('wTheme', str(self.gTheme))
				
				wus.SetBool('wMainWindowTheme', self.oMainWindowThemeRB1.isChecked())
				
				val = self.oWoodThicknessE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wWoodThickness', str(val))
				
				val = self.oWoodSizeXE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wWoodSizeX', str(val))
				
				val = self.oWoodSizeYE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wWoodSizeY', str(val))

				val = self.oWoodDescriptionE.text()
				wus.SetString('wWoodDescription', str(val))
				
				val = self.oWoodWeightE.text()
				val = float(val)
				wus.SetString('wWoodWeight', str(val))
				
				wus.SetString('wWoodWeightCalculation', str(self.gWoodWeightCalculation))
				
				val = self.oWoodPriceE.text()
				val = float(val)
				wus.SetString('wWoodPrice', str(val))
				
				val = self.oWoodPriceSymbolE.text()
				wus.SetString('wWoodPriceSymbol', str(val))
				
				wus.SetString('wWoodPriceCalculation', str(self.gWoodPriceCalculation))
				
				# color
				cR = self.oWoodColorRE.text()
				cG = self.oWoodColorGE.text()
				cB = self.oWoodColorBE.text()
				cA = self.oWoodColorAE.text()
				
				if cR == "" and cG == "" and cB == "" and cA == "":
					[ cR, cG, cB, cA ] = [ "247", "185", "108", "255" ]

				wus.SetString('wWoodColorR', cR)
				wus.SetString('wWoodColorG', cG)
				wus.SetString('wWoodColorB', cB)
				wus.SetString('wWoodColorA', cA)
				
				# window stays on top
				wus.SetBool('wWindowStaysOnTop', self.oWindowRB1.isChecked())
				
				# current selection
				wus.SetBool('wCurrentSelection', self.oCurrentSelectionRB1.isChecked())
				
				# ################################################################
				# page 2
				# ################################################################
				
				val = self.oFrontInsideThicknessE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wFrontInsideThickness', str(val))
				
				val = self.oFrontInsideOffsetLE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wFrontInsideOffsetL', str(val))
				
				val = self.oFrontInsideOffsetRE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wFrontInsideOffsetR', str(val))
				
				val = self.oFrontInsideOffsetBE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wFrontInsideOffsetB', str(val))
				
				val = self.oFrontInsideOffsetTE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wFrontInsideOffsetT', str(val))
				
				val = self.oFrontOutsideThicknessE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wFrontOutsideThickness', str(val))
				
				val = self.oFrontOutsideOffsetLE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wFrontOutsideOffsetL', str(val))
				
				val = self.oFrontOutsideOffsetRE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wFrontOutsideOffsetR', str(val))
				
				val = self.oFrontOutsideOffsetBE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wFrontOutsideOffsetB', str(val))
				
				val = self.oFrontOutsideOffsetTE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wFrontOutsideOffsetT', str(val))
				
				val = self.oShelfThicknessE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wShelfThickness', str(val))
				
				val = self.oShelfOffsetSidesE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wShelfOffsetSides', str(val))
				
				val = self.oBackIThicknessE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wBackInsideThickness', str(val))
				
				val = self.oBackOThicknessE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wBackOutsideThickness', str(val))
				
				# ################################################################
				# page 3
				# ################################################################
				
				# edgeband thickness
				edgebandThick = self.oEdgebandThickE.text()
				edgebandThick = MagicPanels.unit2value(edgebandThick)
				wus.SetString('wEdgebandThickness', str(edgebandThick))
				
				# edgeband apply
				if self.oEdgebandApplyRB1.isChecked():
					edgebandApply = "everywhere"
				else:
					edgebandApply = "visible"
				wus.SetString('wEdgebandApply', str(edgebandApply))
				
				# color
				cR = self.oEdgebandColorRE.text()
				cG = self.oEdgebandColorGE.text()
				cB = self.oEdgebandColorBE.text()
				cA = self.oEdgebandColorAE.text()
				
				if cR == "" and cG == "" and cB == "" and cA == "":
					[ cR, cG, cB, cA ] = [ "255", "255", "255", "255" ]

				wus.SetString('wEdgebandColorR', cR)
				wus.SetString('wEdgebandColorG', cG)
				wus.SetString('wEdgebandColorB', cB)
				wus.SetString('wEdgebandColorA', cA)
				
				# ################################################################
				# page 4
				# ################################################################
				
				wus.SetBool('wPreferCustomSettings', self.oPreferCustomSettingsRB1.isChecked())
				
				val = self.oOffsetSidesE.text()
				val = int(val)
				wus.SetString('wOffsetSides', str(val))
				
				val = self.oOffsetItemsPerSideE.text()
				val = int(val)
				wus.SetString('wOffsetItemsPerSide', str(val))
				
				val = self.oOffsetFromCornerE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wOffsetFromCorner', str(val))
			
				val = self.oOffsetBetweenE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wOffsetBetween', str(val))
				
				val = self.oOffsetFromEdgeE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wOffsetFromEdge', str(val))
				
				# ################################################################
				# page 5
				# ################################################################
				
				val = self.oDowelDiameterE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wDowelDiameter', str(val))
				
				val = self.oDowelSizeE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wDowelSize', str(val))
				
				val = self.oDowelSinkE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wDowelSink', str(val))
				
				val = self.oHoleDiameterE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wHoleDiameter', str(val))
				
				val = self.oHoleCountersinkDiameterE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wHoleCountersinkDiameter', str(val))
				
				val = self.oHoleSizeE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wHoleSize', str(val))
				
				val = self.oDrillSpikeE.text()
				wus.SetString('wDrillSpike', str(val))
				
				val = self.oPocketDiameterE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wPocketDiameter', str(val))
				
				val = self.oPocketCountersinkDiameterE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wPocketCountersinkDiameter', str(val))
				
				val = self.oPocketSizeE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wPocketSize', str(val))
				
				val = self.oPocketOffsetFromEdgeE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wPocketOffsetFromEdge', str(val))
				
				val = self.oPocketRotationE.text()
				val = float(val)
				wus.SetString('wPocketRotation', str(val))
				
				val = self.oPocketSinkE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wPocketSink', str(val))
		
				# ################################################################
				# update settings
				# ################################################################
				
				MagicPanels.updateGlobals()
				self.oStatusL.setText(translate('magicSettings', 'Settings have been updated.'))
				
			except:
				self.oStatusL.setText(translate('magicSettings', 'Error during save settings.'))
		
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

