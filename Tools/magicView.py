import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore
import time

import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# Global definitions
# ############################################################################

# add new items only at the end and change self.sModeList
getMenuIndex1 = {
	translate('magicView', 'restore'): 0, 
	translate('magicView', 'explode'): 1, 
	translate('magicView', 'along X'): 2, 
	translate('magicView', 'along Y'): 3, 
	translate('magicView', 'along Z'): 4, 
	translate('magicView', 'along XYZ'): 5, 
	translate('magicView', 'Assembly'): 6, 
	translate('magicView', 'custom'): 7 # no comma 
}

# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals
		# ############################################################################
		
		gObjects = []
		
		gCustomView = {} # syntax: sheet.Label: sheet.Name
		
		gCurrentViewText = translate('magicView', 'restore')
		gCurrentViewIndex = getMenuIndex1[gCurrentViewText]
		
		gCornerCrossSupport = True
		gAxisCrossSupport = True
		
		try:
			gCornerCross = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
			gCornerCrossOrig = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
		except:
			gCornerCrossSupport = False
			
		try:
			gAxisCross = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()
			gAxisCrossOrig = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()
		except:
			gAxisCrossSupport = False
		
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
			toolSH = 440
			
			area = toolSW - 20          # full gui area
			rside = toolSW - 10         # right side of the GUI
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 230
			gPH = int( gSH - toolSH ) - 40

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicView', 'magicView'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# settings
			# ############################################################################

			row = 10
			btsize = 50                                    # button size
			btoffset = 5                                   # button offset
			bc1 = area - (2 * btsize) - btoffset + 5       # button column 1
			bc2 = area - btsize + btoffset + 5             # button column 2
			
			# ############################################################################
			# GUI - selection
			# ############################################################################

			# not write here, copy text from getMenuIndex1 to avoid typo
			self.sModeList = (
				translate('magicView', 'custom'), 
				translate('magicView', 'restore'), 
				translate('magicView', 'explode'), 
				translate('magicView', 'along X'), 
				translate('magicView', 'along Y'), 
				translate('magicView', 'along Z'), 
				translate('magicView', 'along XYZ'), 
				translate('magicView', 'Assembly') # no comma
			)
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(0) # default
			self.sMode.textActivated[str].connect(self.setViewType)
		
			# ############################################################################
			# GUI - normal view
			# ############################################################################

			self.oImportB1 = QtGui.QPushButton(translate('magicView', 'read from spreadsheet'), self)
			self.oImportB1.clicked.connect(self.setReadView)
			self.oImportB1.setFixedHeight(40)
			
			self.oSaveB1 = QtGui.QPushButton(translate('magicView', 'save to spreadsheet'), self)
			self.oSaveB1.clicked.connect(self.setSaveView)
			self.oSaveB1.setFixedHeight(40)
			
			# radio buttons
			
			self.rb1 = QtGui.QRadioButton(self)
			self.rb1.setText(translate('magicView', 'screenshoot'))
			self.rb1.toggled.connect(self.selectRadioButton1)
			self.rb1.setChecked(True)
			
			self.rb2 = QtGui.QRadioButton(self)
			self.rb2.setText(translate('magicView', 'objects'))
			self.rb2.toggled.connect(self.selectRadioButton2)

			self.oSetTechDrawB1 = QtGui.QPushButton(translate('magicView', 'export to TechDraw'), self)
			self.oSetTechDrawB1.clicked.connect(self.setTechDraw)
			self.oSetTechDrawB1.setFixedHeight(40)

			# ############################################################################
			# GUI for common foot
			# ############################################################################
			
			if self.gCornerCrossSupport == True:
			
				# label
				self.cocL = QtGui.QLabel(translate('magicView', 'Corner cross:'), self)

				# button
				self.cocB1 = QtGui.QPushButton("-", self)
				self.cocB1.clicked.connect(self.setCornerM)
				self.cocB1.setFixedWidth(btsize)
				self.cocB1.setAutoRepeat(True)
				
				# button
				self.cocB2 = QtGui.QPushButton("+", self)
				self.cocB2.clicked.connect(self.setCornerP)
				self.cocB2.setFixedWidth(btsize)
				self.cocB2.setAutoRepeat(True)

			if self.gAxisCrossSupport == True:
				
				# label
				self.cecL = QtGui.QLabel(translate('magicView', 'Center cross:'), self)

				# button
				self.cecB1 = QtGui.QPushButton(translate('magicView', 'on'), self)
				self.cecB1.clicked.connect(self.setCenterOn)
				self.cecB1.setFixedWidth(btsize)
				self.cecB1.setAutoRepeat(True)
				
				# button
				self.cecB2 = QtGui.QPushButton(translate('magicView', 'off'), self)
				self.cecB2.clicked.connect(self.setCenterOff)
				self.cecB2.setFixedWidth(btsize)
				self.cecB2.setAutoRepeat(True)

			if self.gCornerCrossSupport == True or self.gAxisCrossSupport == True:

				self.kccscb = QtGui.QCheckBox(translate('magicView', ' - keep custom cross settings'), self)
				self.kccscb.setCheckState(QtCore.Qt.Unchecked)

			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.row1 = QtGui.QVBoxLayout()
			self.row1.addWidget(self.sMode)
			self.row1.addSpacing(10)
			self.row1.addWidget(self.oImportB1)
			self.row1.addWidget(self.oSaveB1)
			self.groupBody1 = QtGui.QGroupBox(None, self)
			self.groupBody1.setLayout(self.row1)

			self.row2 = QtGui.QHBoxLayout()
			self.row2.addWidget(self.rb1)
			self.row2.addWidget(self.rb2)
			
			self.row3 = QtGui.QVBoxLayout()
			self.row3.addLayout(self.row2)
			self.row3.addSpacing(10)
			self.row3.addWidget(self.oSetTechDrawB1)
			self.groupBody2 = QtGui.QGroupBox(None, self)
			self.groupBody2.setLayout(self.row3)

			# create foot
			self.layoutFoot = QtGui.QVBoxLayout()
			
			self.rowFoot1 = QtGui.QHBoxLayout()
			self.rowFoot1.addWidget(self.cocL)
			self.rowFoot1.addWidget(self.cocB1)
			self.rowFoot1.addWidget(self.cocB2)
			self.layoutFoot.addLayout(self.rowFoot1)

			self.rowFoot2 = QtGui.QHBoxLayout()
			self.rowFoot2.addWidget(self.cecL)
			self.rowFoot2.addWidget(self.cecB1)
			self.rowFoot2.addWidget(self.cecB2)
			self.layoutFoot.addLayout(self.rowFoot2)
			
			self.rowFoot3 = QtGui.QHBoxLayout()
			self.rowFoot3.addWidget(self.kccscb)
			self.layoutFoot.addLayout(self.rowFoot3)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			
			self.layout.addWidget(self.groupBody1)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody2)
			self.layout.addStretch()
			self.layout.addLayout(self.layoutFoot)
			self.setLayout(self.layout)
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()
			
			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)

			# init
			self.initSettings()
			
			# not active by default maybe
			'''
			if self.gAxisCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			
			if self.gCornerCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(50)
			'''
			
		# ############################################################################
		# functions
		# ############################################################################
		
		# ############################################################################
		def isSafe(self, iObj):
		
			if (
				iObj.isDerivedFrom("Part::Box") or 
				iObj.isDerivedFrom("PartDesign::Body")
			):
				return True
			
			return False
		
		# ############################################################################
		def initGlobals(self):
			
			objects = []
			
			try:
				objects = FreeCAD.ActiveDocument.Objects
			except:
				skip = 1
				
			if len(objects) > 0:
				
				self.gObjects = []
				
				for o in objects:
					try:
						test = o.Placement
						self.gObjects.append(o)
					except:
						skip = 1

		# ############################################################################
		def initSheet(self):
			
			# search all objects because Spreadsheet not have Placement
			for o in FreeCAD.ActiveDocument.Objects:
				if o.isDerivedFrom("Spreadsheet::Sheet") and str(o.Name).startswith("magicview"):
					if str(o.Name) != "magicviewrestore":
						self.sMode.addItems( tuple([ str(o.Label) ]) )
						self.gCustomView[str(o.Label)] = str(o.Name)
			
			# create restore file
			sheet = FreeCAD.ActiveDocument.getObject("magicviewrestore")
			if sheet != None:
				return	
			
			sheet = FreeCAD.ActiveDocument.addObject("Spreadsheet::Sheet","magicviewrestore")
			sheet.Label = translate('magicView', 'magicView - restore view')

			sheet.set( "A2", str("Settings:") )
			sheet.set( "B1", str("Rows") )
			sheet.set( "B2", str(len(self.gObjects)) )
			
			sheet.set( "A4", str("Name") )
			sheet.set( "B4", str("Label") )
			sheet.set( "C4", str("Placement X") )
			sheet.set( "D4", str("Placement Y") )
			sheet.set( "E4", str("Placement Z") )
			sheet.set( "F4", str("Rotation Angle") )
			sheet.set( "G4", str("Rotation X") )
			sheet.set( "H4", str("Rotation Y") )
			sheet.set( "I4", str("Rotation Z") )
			
			# store all objects with Placement maybe
			# to allow custom move but auto explode only safe objects
			row = 5
			for o in self.gObjects:
				
				try:
					sheet.set( "A"+str(row), str(o.Name) )
					sheet.set( "B"+str(row), str(o.Label) )
					sheet.set( "C"+str(row), str(o.Placement.Base.x) )
					sheet.set( "D"+str(row), str(o.Placement.Base.y) )
					sheet.set( "E"+str(row), str(o.Placement.Base.z) )
					sheet.set( "F"+str(row), str(o.Placement.Rotation.Angle) )
					sheet.set( "G"+str(row), str(o.Placement.Rotation.Axis.x) )
					sheet.set( "H"+str(row), str(o.Placement.Rotation.Axis.y) )
					sheet.set( "I"+str(row), str(o.Placement.Rotation.Axis.z) )
				except:
					continue

				row = row + 1
			
			# decoration
			sheet.setStyle('A1:I1', 'bold')
			sheet.setBackground('A1:I1', (1.000000,0.000000,0.000000,1.000000))
			sheet.setStyle('A2:A2', 'bold')
			sheet.setBackground('A2:A2', (1.000000,0.000000,0.000000,1.000000))
			sheet.setStyle('A4:I4', 'bold')
			sheet.setBackground('A4:I4', (1.000000,0.000000,0.000000,1.000000))
			sheet.setStyle('A5:A'+str(row-1), 'bold')
			sheet.setBackground('A5:A'+str(row-1), (1.000000,0.000000,0.000000,1.000000))
			
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def initSettings(self):
			
			self.initGlobals()
			self.initSheet()
			
		# ############################################################################
		# possible view
		# ############################################################################
	
		# ############################################################################
		def setView0(self):
			
			sheet = FreeCAD.ActiveDocument.getObject("magicviewrestore")
			if sheet == None:
				return
		
			num = int(sheet.get("B2"))

			row = 5
			for i in range(0, num):

				name = str(sheet.get( "A"+str(row) ))
				px = float(sheet.get( "C"+str(row) ))
				py = float(sheet.get( "D"+str(row) ))
				pz = float(sheet.get( "E"+str(row) ))
				angle = float(sheet.get( "F"+str(row) ))
				rx = float(sheet.get( "G"+str(row) ))
				ry = float(sheet.get( "H"+str(row) ))
				rz = float(sheet.get( "I"+str(row) ))
			
				o = FreeCAD.ActiveDocument.getObject(str(name))
				MagicPanels.setPosition(o, px, py, pz, "local")
				o.Placement.Rotation.Angle = angle
				o.Placement.Rotation.Axis.x = rx
				o.Placement.Rotation.Axis.y = ry
				o.Placement.Rotation.Axis.z = rz

				row = row + 1
			
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def setView1(self):

			[ minX, minY, minZ, 
				maxX, maxY, maxZ, 
				[ cx, cy, cz ] ] = MagicPanels.getOccupiedSpace(self.gObjects)
			
			for o in self.gObjects:
				if self.isSafe(o):
				
					try:
						test = o.Shape.CenterOfMass
					except:
						continue
					
					[ px, px, pz ] = [ 0, 0, 0 ]
					[ ocx, ocy, ocz ] = [ o.Shape.CenterOfMass.x, o.Shape.CenterOfMass.y, o.Shape.CenterOfMass.z ]
					
					offsetX = abs(cx - ocx)
					offsetY = abs(cy - ocy)
					offsetZ = abs(cz - ocz)
					
					if ocx > cx:
						px = offsetX
					else:
						px = - offsetX
					
					if ocy > cy:
						py = offsetY
					else:
						py = - offsetY
					
					if ocz > cz:
						pz = offsetZ
					else:
						pz = - offsetZ
					
					MagicPanels.setPosition(o, px, py, pz, "offset")
			
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def setView2(self):

			vx = 0 
			for o in self.gObjects:
				if self.isSafe(o):
				
					[ x, y, z ] = MagicPanels.getPosition(o, "local")
					MagicPanels.setPosition(o, vx, y, z, "local")
					[ sx, sy, sz ] = MagicPanels.getSizes(o)
					vx = vx + sx + 50
				
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def setView3(self):

			vy = 0 
			for o in self.gObjects:
				if self.isSafe(o):
				
					[ x, y, z ] = MagicPanels.getPosition(o, "local")
					MagicPanels.setPosition(o, x, vy, z, "local")
					[ sx, sy, sz ] = MagicPanels.getSizes(o)
					vy = vy + sy + 50
				
			FreeCAD.ActiveDocument.recompute()
			
		# ############################################################################
		def setView4(self):

			vz = 0 
			for o in self.gObjects:
				if self.isSafe(o):
				
					[ x, y, z ] = MagicPanels.getPosition(o, "local")
					MagicPanels.setPosition(o, x, y, vz, "local")
					[ sx, sy, sz ] = MagicPanels.getSizes(o)
					vz = vz + sz + 50
				
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def setView5(self):

			[ vx, vy, vz ] = [ 0, 0, 0 ]
			for o in self.gObjects:
				if self.isSafe(o):
				
					[ x, y, z ] = MagicPanels.getPosition(o, "local")
					MagicPanels.setPosition(o, vx, vy, vz, "local")
					[ sx, sy, sz ] = MagicPanels.getSizes(o)
					vx = vx + sx + 50
					vy = vy + sy + 50
					vz = vz + sz + 50
				
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def setView6(self):

			for o in self.gObjects:
				if self.isSafe(o):
					
					[ x, y, z ] = MagicPanels.getPosition(o, "local")
					MagicPanels.setPosition(o, 0, 0, 0, "local")
				
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		# action functions
		# ############################################################################
	
		# ############################################################################
		def setSelectedView(self):
		
			# reset first for all except custom view
			if self.gCurrentViewIndex != 7:
				self.setView0()
			
			# explode
			if self.gCurrentViewIndex == 1:
				self.setView1()
				
			# along X
			if self.gCurrentViewIndex == 2:
				self.setView2()
			
			# along Y
			if self.gCurrentViewIndex == 3:
				self.setView3()
			
			# along Z
			if self.gCurrentViewIndex == 4:
				self.setView4()
			
			# along XYZ
			if self.gCurrentViewIndex == 5:
				self.setView5()
			
			# Assembly
			if self.gCurrentViewIndex == 6:
				self.setView6()
			
		# ############################################################################
		def setViewType(self, selectedText):
			
			self.gCurrentViewText = selectedText
			
			custom = False
			try:
				self.gCurrentViewIndex = getMenuIndex1[selectedText]
				self.setSelectedView()
			except:
				custom = True
			
			if custom == True:
				
				try:
					sheet = self.gCustomView[self.gCurrentViewText]
					self.gCurrentViewIndex = -1
					self.setReadView(sheet)
				except:
					skip = 1

		# ############################################################################
		def setReadView(self, iSheet):

			if iSheet == False:

				try:
					sheet = FreeCADGui.Selection.getSelection()[0]
					num = int(sheet.get("B2"))

				except:
					return

			else:

				try:
					sheet = FreeCAD.ActiveDocument.getObject(iSheet)
					num = int(sheet.get("B2"))
				except:
					return

			row = 5
			for i in range(0, num):

				name = str(sheet.get( "A"+str(row) ))
				px = float(sheet.get( "C"+str(row) ))
				py = float(sheet.get( "D"+str(row) ))
				pz = float(sheet.get( "E"+str(row) ))
				angle = float(sheet.get( "F"+str(row) ))
				rx = float(sheet.get( "G"+str(row) ))
				ry = float(sheet.get( "H"+str(row) ))
				rz = float(sheet.get( "I"+str(row) ))
			
				o = FreeCAD.ActiveDocument.getObject(str(name))

				MagicPanels.setPosition(o, px, py, pz, "local")
				o.Placement.Rotation.Angle = angle
				o.Placement.Rotation.Axis.x = rx
				o.Placement.Rotation.Axis.y = ry
				o.Placement.Rotation.Axis.z = rz

				row = row + 1
			
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def setSaveView(self):

			sheet = FreeCAD.ActiveDocument.addObject("Spreadsheet::Sheet","magicview")
			sheet.Label = translate('magicView', 'magicView ')

			sheet.set( "A2", str("Settings:") )
			sheet.set( "B1", str("Rows") )
			sheet.set( "B2", str(len(self.gObjects)) )
			
			sheet.set( "A4", str("Name") )
			sheet.set( "B4", str("Label") )
			sheet.set( "C4", str("Placement X") )
			sheet.set( "D4", str("Placement Y") )
			sheet.set( "E4", str("Placement Z") )
			sheet.set( "F4", str("Rotation Angle") )
			sheet.set( "G4", str("Rotation X") )
			sheet.set( "H4", str("Rotation Y") )
			sheet.set( "I4", str("Rotation Z") )
			
			row = 5
			for o in self.gObjects:
				
				sheet.set( "A"+str(row), str(o.Name) )
				sheet.set( "B"+str(row), str(o.Label) )
				sheet.set( "C"+str(row), str(o.Placement.Base.x) )
				sheet.set( "D"+str(row), str(o.Placement.Base.y) )
				sheet.set( "E"+str(row), str(o.Placement.Base.z) )
				sheet.set( "F"+str(row), str(o.Placement.Rotation.Angle) )
				sheet.set( "G"+str(row), str(o.Placement.Rotation.Axis.x) )
				sheet.set( "H"+str(row), str(o.Placement.Rotation.Axis.y) )
				sheet.set( "I"+str(row), str(o.Placement.Rotation.Axis.z) )
				
				row = row + 1
			
			# decoration
			sheet.setStyle('A1:I1', 'bold')
			sheet.setBackground('A1:I1', (0.666667,0.333333,1.000000,1.000000))
			sheet.setStyle('A2:A2', 'bold')
			sheet.setBackground('A2:A2', (0.666667,0.333333,1.000000,1.000000))
			sheet.setStyle('A4:I4', 'bold')
			sheet.setBackground('A4:I4', (0.666667,0.333333,1.000000,1.000000))
			sheet.setStyle('A5:A'+str(row-1), 'bold')
			sheet.setBackground('A5:A'+str(row-1), (0.666667,0.333333,1.000000,1.000000))
			
			FreeCAD.ActiveDocument.recompute()
			self.sMode.addItems( tuple([ str(sheet.Label) ]) )
			self.gCustomView[str(sheet.Label)] = str(sheet.Name)

		# ############################################################################
		def setTechDraw(self):
			
			page = FreeCAD.ActiveDocument.addObject("TechDraw::DrawPage","page")
			page.Label = 'TechDraw' + " - " + self.gCurrentViewText
			
			template = FreeCAD.ActiveDocument.addObject("TechDraw::DrawSVGTemplate","Template")
			template.Template = FreeCAD.getResourceDir() + "Mod/TechDraw/Templates/A4_Portrait_blank.svg"
			
			templateWidth = float(template.Width)
			templateHeight = float(template.Height)

			if templateWidth == 0 or templateHeight == 0:
				templateWidth = float(210)
				templateHeight = float(297)
	
			page.Template = template
			FreeCAD.ActiveDocument.recompute()
			
			if self.rb1.isChecked() == True:
				
				view = FreeCAD.ActiveDocument.addObject('TechDraw::DrawViewImage','ActiveView')
				page.addView(view)
				FreeCADGui.ActiveDocument.ActiveView.saveImage("magicView.png", 500, 500, "Transparent")
				view.ImageFile = "magicView.png"
				view.ScaleType = "Custom"
				view.Scale = 4
				view.X = 120
				view.Y = 150
			
			if self.rb2.isChecked() == True:
			
				view = FreeCAD.ActiveDocument.addObject('TechDraw::DrawViewPart', 'View')
				page.addView(view)
				view.Direction = FreeCAD.Vector(0.552501000000, -0.686953000000, 0.472057000000)
				view.XDirection = FreeCAD.Vector(0.775825697655, 0.630867700455, 0.010024182780)
				
				objects = []
				selection = []
				
				try:
					selection = FreeCADGui.Selection.getSelection()
				except:
					skip = 1
					
				if len(selection) == 0:
					selection = self.gObjects
					
				for o in selection:
					if MagicPanels.isVisible(o) == True:
						objects.append(o)

				view.Source = objects
				view.ScaleType = "Custom"
				view.Scale = 0.10
				view.X = 100
				view.Y = 150

			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def selectRadioButton1(self, selected):
			skip = 1
		
		def selectRadioButton2(self, selected):
			skip = 1
				
		# ############################################################################
		# cross functions
		# ############################################################################

		# ############################################################################
		def setCornerM(self):

			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				if s - 1 < 0:
					FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(0)
				else:
					FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s-1)
					self.gCornerCross = s-1
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setCornerP(self):

			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s+1)
				self.gCornerCross = s+1
			except:
				self.s1S.setText(self.gNoSelection)
		
		# ############################################################################
		def setCenterOn(self):
			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
				self.gAxisCross = True
			except:
				self.s1S.setText(self.gNoSelection)
			
		def setCenterOff(self):

			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(False)
				self.gAxisCross = False
			except:
				self.s1S.setText(self.gNoSelection)

	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		
		if not form.kccscb.isChecked():

			try:
				if form.gAxisCrossSupport == True:
					FreeCADGui.ActiveDocument.ActiveView.setAxisCross(form.gAxisCrossOrig)
			except:
				skip = 1
				
			try:
				if form.gCornerCrossSupport == True:
					FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(form.gCornerCrossOrig)
			except:
				skip = 1
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################

