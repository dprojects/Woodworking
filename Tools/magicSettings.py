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
	translate('magicSettings', 'Settings - page 3'): 2 # no comma 
}

# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):

		# ############################################################################
		# globals
		# ############################################################################
		
		gTheme = MagicPanels.gTheme
		gPage = 0
		
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
			toolSW = 400
			toolSH = 600
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('magicSettings', 'magicSettings'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			
			self.setMinimumWidth(toolSW)
			self.setMinimumHeight(toolSH)

			# ############################################################################
			# pages
			# ############################################################################

			# not write here, copy text from getMenuIndex1 to avoid typo
			self.sPageList = (
				translate('magicSettings', 'Settings - page 1'), 
				translate('magicSettings', 'Settings - page 2'), 
				translate('magicSettings', 'Settings - page 3') # no comma 
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
			# save settings
			# ############################################################################
			
			# status
			self.oStatusL = QtGui.QLabel("", self)
			
			# button
			self.oSaveB = QtGui.QPushButton(translate('magicSettings', 'save settigns'), self)
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
			self.groupPage11 = QtGui.QGroupBox(None, self)
			self.groupPage11.setLayout(self.Page11)
			
			self.Page12 = QtGui.QGridLayout()
			self.Page12.addWidget(self.oWoodThicknessL, 0, 0)
			self.Page12.addWidget(self.oWoodThicknessE, 0, 1)
			self.Page12.addWidget(self.oWoodSizeXL, 1, 0)
			self.Page12.addWidget(self.oWoodSizeXE, 1, 1)
			self.Page12.addWidget(self.oWoodSizeYL, 2, 0)
			self.Page12.addWidget(self.oWoodSizeYE, 2, 1)
			self.groupPage12 = QtGui.QGroupBox(None, self)
			self.groupPage12.setLayout(self.Page12)
		
			self.Page13 = QtGui.QGridLayout()
			self.Page13.addWidget(self.oWoodColorRL, 0, 0)
			self.Page13.addWidget(self.oWoodColorRE, 0, 1)
			self.Page13.addWidget(self.oWoodColorGL, 1, 0)
			self.Page13.addWidget(self.oWoodColorGE, 1, 1)
			self.Page13.addWidget(self.oWoodColorBL, 2, 0)
			self.Page13.addWidget(self.oWoodColorBE, 2, 1)
			self.Page13.addWidget(self.oWoodColorAL, 3, 0)
			self.Page13.addWidget(self.oWoodColorAE, 3, 1)
			self.groupPage13 = QtGui.QGroupBox(None, self)
			self.groupPage13.setLayout(self.Page13)

			self.Page14 = QtGui.QGridLayout()
			self.Page14.addWidget(self.oWindowL, 1, 0)
			self.Page14.addWidget(self.oWindowRB1, 1, 1)
			self.Page14.addWidget(self.oWindowRB2, 1, 2)
			self.Page14.addWidget(self.oCurrentSelectionL, 2, 0)
			self.Page14.addWidget(self.oCurrentSelectionRB1, 2, 1)
			self.Page14.addWidget(self.oCurrentSelectionRB2, 2, 2)
			self.groupPage14 = QtGui.QGroupBox(None, self)
			self.groupPage14.setLayout(self.Page14)

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
			self.Page23.addWidget(self.oBackIThicknessL, 1, 0)
			self.Page23.addWidget(self.oBackIThicknessE, 1, 1)
			self.Page23.addWidget(self.oBackOThicknessL, 2, 0)
			self.Page23.addWidget(self.oBackOThicknessE, 2, 1)
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
			self.layout.addWidget(self.groupPage21)
			self.layout.addWidget(self.groupPage22)
			self.layout.addWidget(self.groupPage23)
			self.layout.addWidget(self.groupPage31)
			self.layout.addWidget(self.groupPage32)
			self.layout.addStretch()
			self.layout.addLayout(self.Save)
			self.setLayout(self.layout)
			
			# init
			self.groupPage11.show()
			self.groupPage12.show()
			self.groupPage13.show()
			self.groupPage14.show()
			self.groupPage21.hide()
			self.groupPage22.hide()
			self.groupPage23.hide()
			self.groupPage31.hide()
			self.groupPage32.hide()
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()

			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)

			# set window position
			sw = self.width()
			sh = self.height()
			pw = int( (FreeCADGui.getMainWindow().width() / 2) - ( sw / 2 ) )
			ph = int( (FreeCADGui.getMainWindow().height() / 2) - ( sh / 2 ) )
			self.setGeometry(pw, ph, sw, sh)
			
			# init
			self.getSettings()
			
		# ############################################################################
		# functions
		# ############################################################################
		
		# ############################################################################
		def doNothing(self):
			skip = 1

		def showPage(self, selectedText):
			selectedIndex = getMenuIndex1[selectedText]
			self.gPage = selectedIndex
			
			if self.gPage == 0:
				self.groupPage11.show()
				self.groupPage12.show()
				self.groupPage13.show()
				self.groupPage14.show()
				self.groupPage21.hide()
				self.groupPage22.hide()
				self.groupPage23.hide()
				self.groupPage31.hide()
				self.groupPage32.hide()
			
			if self.gPage == 1:
				self.groupPage11.hide()
				self.groupPage12.hide()
				self.groupPage13.hide()
				self.groupPage14.hide()
				self.groupPage21.show()
				self.groupPage22.show()
				self.groupPage23.show()
				self.groupPage31.hide()
				self.groupPage32.hide()

			if self.gPage == 2:
				self.groupPage11.hide()
				self.groupPage12.hide()
				self.groupPage13.hide()
				self.groupPage14.hide()
				self.groupPage21.hide()
				self.groupPage22.hide()
				self.groupPage23.hide()
				self.groupPage31.show()
				self.groupPage32.show()

		# ############################################################################
		def getSettings(self):
			
			# page 1
			
			try:
				self.oTheme.setCurrentText(MagicPanels.gTheme)
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

			# page 2
			
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
			
			# page 3
			
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
			
		# ############################################################################
		def setThemeType(self, selectedText):
			
			self.gTheme = selectedText
			
			# set theme
			QtCSS = MagicPanels.getTheme(self.gTheme)
			self.setStyleSheet(QtCSS)

		# ############################################################################
		def saveSettings(self):
			
			try:
				wus = FreeCAD.ParamGet(MagicPanels.gSettingsPref)
				
				# #######################################################
				# page 1
				# #######################################################
				
				wus.SetString('wTheme', str(self.gTheme))
				
				val = self.oWoodThicknessE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wWoodThickness', str(val))
				
				val = self.oWoodSizeXE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wWoodSizeX', str(val))
				
				val = self.oWoodSizeYE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wWoodSizeY', str(val))

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
				
				# #######################################################
				# page 2
				# #######################################################
				
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
				
				val = self.oBackIThicknessE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wBackInsideThickness', str(val))
				
				val = self.oBackOThicknessE.text()
				val = MagicPanels.unit2value(val)
				wus.SetString('wBackOutsideThickness', str(val))
				
				# #######################################################
				# page 3
				# #######################################################
				
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
				
				# #######################################################
				# update settings
				# #######################################################
				
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

