import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):

		# ############################################################################
		# globals
		# ############################################################################
		
		gTheme = MagicPanels.gTheme
		
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
			toolSW = 300
			toolSH = 400
			
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
			# body
			# ############################################################################

			# theme
			self.oThemeL = QtGui.QLabel(translate('magicSettings', 'Theme:'), self)

			self.oThemeList = MagicPanels.getTheme("config")
			self.oTheme = QtGui.QComboBox(self)
			self.oTheme.addItems(self.oThemeList)
			self.oTheme.setCurrentIndex(0) # default
			self.oTheme.textActivated[str].connect(self.setThemeType)

			# wood color
			self.oWoodColorRL = QtGui.QLabel(translate('magicSettings', 'Red color:'), self)
			self.oWoodColorRE = QtGui.QLineEdit(self)
			self.oWoodColorRE.setText("247")
			
			self.oWoodColorGL = QtGui.QLabel(translate('magicSettings', 'Green color:'), self)
			self.oWoodColorGE = QtGui.QLineEdit(self)
			self.oWoodColorGE.setText("185")
			
			self.oWoodColorBL = QtGui.QLabel(translate('magicSettings', 'Blue color:'), self)
			self.oWoodColorBE = QtGui.QLineEdit(self)
			self.oWoodColorBE.setText("108")
			
			self.oWoodColorAL = QtGui.QLabel(translate('magicSettings', 'Alpha channel:'), self)
			self.oWoodColorAE = QtGui.QLineEdit(self)
			self.oWoodColorAE.setText("255")
			
			# wood thickness
			self.oWoodThickL = QtGui.QLabel(translate('magicSettings', 'Wood thickness:'), self)
			self.oWoodThickE = QtGui.QLineEdit(self)
			self.oWoodThickE.setText(MagicPanels.unit2gui(18))
			
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
			self.Body1 = QtGui.QGridLayout()
			self.Body1.addWidget(self.oThemeL, 0, 0)
			self.Body1.addWidget(self.oTheme, 0, 1)
			self.Body1.addWidget(self.oWoodThickL, 2, 0)
			self.Body1.addWidget(self.oWoodThickE, 2, 1)
			self.groupBody1 = QtGui.QGroupBox(None, self)
			self.groupBody1.setLayout(self.Body1)

			self.Body2 = QtGui.QGridLayout()
			self.Body2.addWidget(self.oWoodColorRL, 0, 0)
			self.Body2.addWidget(self.oWoodColorRE, 0, 1)
			self.Body2.addWidget(self.oWoodColorGL, 1, 0)
			self.Body2.addWidget(self.oWoodColorGE, 1, 1)
			self.Body2.addWidget(self.oWoodColorBL, 2, 0)
			self.Body2.addWidget(self.oWoodColorBE, 2, 1)
			self.Body2.addWidget(self.oWoodColorAL, 3, 0)
			self.Body2.addWidget(self.oWoodColorAE, 3, 1)
			self.groupBody2 = QtGui.QGroupBox(translate('magicSettings', 'Wood color'), self)
			self.groupBody2.setLayout(self.Body2)

			self.Body3 = QtGui.QGridLayout()
			self.Body3.addWidget(self.oWindowL, 0, 0)
			self.Body3.addWidget(self.oWindowRB1, 0, 1)
			self.Body3.addWidget(self.oWindowRB2, 0, 2)
			self.Body3.addWidget(self.oCurrentSelectionL, 1, 0)
			self.Body3.addWidget(self.oCurrentSelectionRB1, 1, 1)
			self.Body3.addWidget(self.oCurrentSelectionRB2, 1, 2)
			self.groupBody3 = QtGui.QGroupBox(translate('magicSettings', ''), self)
			self.groupBody3.setLayout(self.Body3)
			
			self.Save = QtGui.QVBoxLayout()
			self.Save.addWidget(self.oStatusL)
			self.Save.addWidget(self.oSaveB)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			self.layout.addWidget(self.groupBody1)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody2)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody3)
			self.layout.addStretch()
			self.layout.addLayout(self.Save)
			self.setLayout(self.layout)
			
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

		# ############################################################################
		def getSettings(self):
			
			try:
				self.oTheme.setCurrentText(MagicPanels.gTheme)
			except:
				skip = 1
				
			try:
				thick = MagicPanels.gWoodThickness
				thick = MagicPanels.unit2gui(thick)
				self.oWoodThickE.setText(thick)
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
				
				# theme
				wus.SetString('wTheme', str(self.gTheme))
				
				
				# thickness
				thick = self.oWoodThickE.text()
				thick = MagicPanels.unit2value(thick)
				wus.SetString('wWoodThickness', str(thick))

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
				
				# update globals
				MagicPanels.updateGlobals()
				
				# status
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

