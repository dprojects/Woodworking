import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore
import os, sys

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
		
		gFSX = 500   # furniture size X (width)
		gFSY = 400   # furniture size Y (depth)
		gFSZ = 760   # furniture size Z (height)
		gThick = 18  # wood thickness
		
		gSelectedFurniture = "F0"
		gColor = (0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 0.0)
		gR = FreeCAD.Rotation(0, 0, 0)
		
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
			toolSW = 450
			toolSH = 300
			
			# active screen size - FreeCAD main window
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = int( ( gSW - toolSW ) / 2 )
			gPH = int( ( gSH - toolSH ) / 2 )

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicStart', 'magicStart'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection
			# ############################################################################
			
			row = 10
	
			self.sModeList = (
				translate('magicStart', 'Simple storage'), 
				translate('magicStart', 'Simple bookcase'), 
				translate('magicStart', 'Bookcase (import parametric)'), 
				translate('magicStart', 'Simple drawer (import parametric)'), 
				translate('magicStart', 'Simple chair (import parametric)'), 
				translate('magicStart', 'Picture frame (import parametric)'), 
				translate('magicStart', 'Simple table (import parametric)'), 
				translate('magicStart', 'Storage box (import parametric)'), 
				translate('magicStart', 'Dowel 8x35 mm (import parametric)'), 
				translate('magicStart', 'Screw 4x40 mm (import parametric)'), 
				translate('magicStart', 'Modular storage')
				)
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(0)
			self.sMode.activated[int].connect(self.selectedOption)
			self.sMode.setFixedWidth(toolSW - 20)
			self.sMode.move(10, row)

			row += 60
			
			# ############################################################################
			# selection icon
			# ############################################################################
			
			icon = ""
			
			self.si = QtGui.QLabel(icon, self)
			self.si.setFixedWidth(200)
			self.si.setFixedHeight(200)
			self.si.setWordWrap(True)
			self.si.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.si.setOpenExternalLinks(True)
			self.setIcon("msf000")

			# ############################################################################
			# options - merge info
			# ############################################################################

			# label
			
			info = translate('magicStart', 'This object has its own settings in spreadsheet and will be imported from Woodworking workbench Examples folder.')
			self.minfo = QtGui.QLabel(info, self)
			self.minfo.move(10, row+3)
			self.minfo.setFixedWidth(200)
			self.minfo.setWordWrap(True)
			self.minfo.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.minfo.hide()
			
			# ############################################################################
			# options - sizes
			# ############################################################################

			# label
			self.o1L = QtGui.QLabel(translate('magicStart', 'Furniture width:'), self)
			self.o1L.move(10, row+3)
			
			# text input
			self.o1E = QtGui.QLineEdit(self)
			self.o1E.setText(str(self.gFSX))
			self.o1E.setFixedWidth(90)
			self.o1E.move(120, row)

			row += 30

			# label
			self.o2L = QtGui.QLabel(translate('magicStart', 'Furniture height:'), self)
			self.o2L.move(10, row+3)

			# text input
			self.o2E = QtGui.QLineEdit(self)
			self.o2E.setText(str(self.gFSZ))
			self.o2E.setFixedWidth(90)
			self.o2E.move(120, row)

			row += 30

			# label
			self.o3L = QtGui.QLabel(translate('magicStart', 'Furniture depth:'), self)
			self.o3L.move(10, row+3)

			# text input
			self.o3E = QtGui.QLineEdit(self)
			self.o3E.setText(str(self.gFSY))
			self.o3E.setFixedWidth(90)
			self.o3E.move(120, row)
			
			row += 30

			# label
			self.o4L = QtGui.QLabel(translate('magicStart', 'Wood thickness:'), self)
			self.o4L.move(10, row+3)

			# text input
			self.o4E = QtGui.QLineEdit(self)
			self.o4E.setText(str(self.gThick))
			self.o4E.setFixedWidth(90)
			self.o4E.move(120, row)

			# ############################################################################
			# options - create button
			# ############################################################################
			
			row += 60

			# button
			self.s1B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.s1B1.clicked.connect(self.createObject)
			self.s1B1.setFixedWidth(200)
			self.s1B1.setFixedHeight(40)
			self.s1B1.move(10, row)

			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()

		# ############################################################################
		# actions - internal functions
		# ############################################################################

		# ############################################################################
		def createF0(self):
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX
			o1.Height = self.gThick
			o1.Width = self.gFSY
			pl = FreeCAD.Vector(0, 0, 0)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ - (2 * self.gThick)
			o2.Width = self.gFSY
			pl = FreeCAD.Vector(0, 0, self.gThick)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ - (2 * self.gThick)
			o3.Width = self.gFSY
			pl = FreeCAD.Vector(self.gFSX - self.gThick, 0, self.gThick)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.DiffuseColor = self.gColor
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX - (2 * self.gThick)
			o4.Height = self.gFSZ - (2 * self.gThick)
			o4.Width = self.gThick
			pl = FreeCAD.Vector(self.gThick, self.gFSY - self.gThick, self.gThick)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.DiffuseColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX
			o5.Height = self.gThick
			o5.Width = self.gFSY
			pl = FreeCAD.Vector(0, 0, self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.DiffuseColor = self.gColor
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = self.gFSX - self.gThick
			o6.Height = self.gFSZ - self.gThick - 4
			o6.Width = self.gThick
			pl = FreeCAD.Vector(self.gThick / 2, - self.gThick, (self.gThick / 2) + 2)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.DiffuseColor = self.gColor
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = self.gFSX - (2 * self.gThick)
			o7.Height = self.gThick
			o7.Width = self.gFSY - (3 * self.gThick)
			pl = FreeCAD.Vector(self.gThick, 2 * self.gThick, (self.gFSZ / 2) - (self.gThick / 2))
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			o7.ViewObject.DiffuseColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF1(self):
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX - (2 * self.gThick)
			o1.Height = self.gThick
			o1.Width = self.gFSY
			pl = FreeCAD.Vector(self.gThick, 0, self.gFSZ / 10)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ
			o2.Width = self.gFSY
			pl = FreeCAD.Vector(0, 0, 0)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ
			o3.Width = self.gFSY
			pl = FreeCAD.Vector(self.gFSX - self.gThick, 0, 0)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.DiffuseColor = self.gColor
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ - (self.gFSZ / 10)
			o4.Width = 3
			pl = FreeCAD.Vector(0, self.gFSY, self.gFSZ / 10)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.DiffuseColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX - (2 * self.gThick)
			o5.Height = self.gThick
			o5.Width = self.gFSY
			pl = FreeCAD.Vector(self.gThick, 0, self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.DiffuseColor = self.gColor

			# Shelf
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o6.Label = translate('magicStart', 'Shelf')
			o6.Length = self.gFSX - (2 * self.gThick)
			o6.Height = self.gThick
			o6.Width = self.gFSY
			pl = FreeCAD.Vector(self.gThick, 0, (self.gFSZ / 2) - (self.gThick / 2))
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.DiffuseColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF2(self):
			
			# calculation
			mNum = 3
			sideZ = ((self.gFSZ - self.gThick - (mNum * self.gThick)) / mNum)
			
			# #######################
			# Modules
			# #######################
			
			for i in range(mNum):
			
				posZ = (i * sideZ) + (i * self.gThick)
			
				# Floor
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
				o1.Label = translate('magicStart', 'Floor M'+str(i))
				o1.Length = self.gFSX
				o1.Height = self.gThick
				o1.Width = self.gFSY
				pl = FreeCAD.Vector(0, 0, posZ)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				o1.ViewObject.DiffuseColor = self.gColor
				
				# Left Side
				o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
				o2.Label = translate('magicStart', 'Left M'+str(i))
				o2.Length = self.gThick
				o2.Height = sideZ
				o2.Width = self.gFSY
				pl = FreeCAD.Vector(0, 0, posZ + self.gThick)
				o2.Placement = FreeCAD.Placement(pl, self.gR)
				o2.ViewObject.DiffuseColor = self.gColor
				
				# Right Side
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
				o3.Label = translate('magicStart', 'Right M'+str(i))
				o3.Length = self.gThick
				o3.Height = sideZ
				o3.Width = self.gFSY
				pl = FreeCAD.Vector(self.gFSX - self.gThick, 0, posZ + self.gThick)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				o3.ViewObject.DiffuseColor = self.gColor
				
				# Back
				o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
				o4.Label = translate('magicStart', 'Back M'+str(i))
				o4.Length = self.gFSX - (2 * self.gThick)
				o4.Height = sideZ
				o4.Width = self.gThick
				pl = FreeCAD.Vector(self.gThick, self.gFSY - self.gThick, posZ + self.gThick)
				o4.Placement = FreeCAD.Placement(pl, self.gR)
				o4.ViewObject.DiffuseColor = self.gColor
				
				# Front
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
				o5.Label = translate('magicStart', 'Front M'+str(i))
				o5.Length = self.gFSX - self.gThick
				o5.Height = sideZ + self.gThick - 4
				o5.Width = self.gThick
				pl = FreeCAD.Vector(self.gThick / 2, - self.gThick, posZ + (self.gThick / 2) + 2)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				o5.ViewObject.DiffuseColor = self.gColor
				
				# Shelf
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
				o6.Label = translate('magicStart', 'Shelf M'+str(i))
				o6.Length = self.gFSX - (2 * self.gThick)
				o6.Height = self.gThick
				o6.Width = self.gFSY - (3 * self.gThick)
				pZ = ((2 * i) + 1) * ((self.gThick + sideZ) / 2)
				pl = FreeCAD.Vector(self.gThick, 2 * self.gThick, pZ)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				o6.ViewObject.DiffuseColor = self.gColor
				
				# create folder
				group = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroup','Group')
				group.Label = translate('magicStart', 'Module '+str(i))
				group.addObject(o1)
				group.addObject(o2)
				group.addObject(o3)
				group.addObject(o4)
				group.addObject(o5)
				group.addObject(o6)
			
			# #######################
			# Top cover
			# #######################
			
			# final top
			t1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			t1.Label = translate('magicStart', 'Top cover')
			t1.Length = self.gFSX
			t1.Height = self.gThick
			t1.Width = self.gFSY
			pZ = mNum * (self.gThick + sideZ)
			pl = FreeCAD.Vector(0, 0, pZ)
			t1.Placement = FreeCAD.Placement(pl, self.gR)
			t1.ViewObject.DiffuseColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def setIcon(self, iName):
			
			path = FreeCADGui.activeWorkbench().path
			iconPath = str(os.path.join(path, "Icons"))
			f = os.path.join(iconPath, iName+".png")
			
			if os.path.exists(f):
				filename = f
				icon = '<img src="'+ filename + '" width="200" height="200" align="right">'
				self.si.hide()
				self.si = QtGui.QLabel(icon, self)
				self.si.move(250, 50)
				self.si.show()

		# ############################################################################
		def getPathToMerge(self, iName, iType):
			
			if iType == "F":
				path = FreeCADGui.activeWorkbench().path
				path = str(os.path.join(path, "Examples"))
				path = str(os.path.join(path, "Parametric"))
				path = str(os.path.join(path, "Furniture"))
				path = str(os.path.join(path, iName))

			if iType == "box":
				path = FreeCADGui.activeWorkbench().path
				path = str(os.path.join(path, "Examples"))
				path = str(os.path.join(path, "Parametric"))
				path = str(os.path.join(path, "Storage boxes"))
				path = str(os.path.join(path, iName))
			
			if iType == "mount":
				path = FreeCADGui.activeWorkbench().path
				path = str(os.path.join(path, "Examples"))
				path = str(os.path.join(path, "Fixture"))
				path = str(os.path.join(path, "Mount"))
				path = str(os.path.join(path, iName))
				
			return path

		# ############################################################################
		def mergeF(self, iName, iType="F"):
		
			# merge
			FreeCAD.ActiveDocument.mergeProject(self.getPathToMerge(iName, iType))
		
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def setMergeInfo(self, iType):
			
			if iType == "show":
				
				self.o1L.hide()
				self.o2L.hide()
				self.o3L.hide()
				self.o4L.hide()
				
				self.o1E.hide()
				self.o2E.hide()
				self.o3E.hide()
				self.o4E.hide()
				
				self.minfo.show()
				
			else:
				
				self.minfo.hide()
				
				self.o1L.show()
				self.o2L.show()
				self.o3L.show()
				self.o4L.show()
				
				self.o1E.show()
				self.o2E.show()
				self.o3E.show()
				self.o4E.show()

		# ############################################################################
		def createObject(self):

			self.gFSX = float(self.o1E.text())
			self.gFSZ = float(self.o2E.text())
			self.gFSY = float(self.o3E.text())
			self.gThick = float(self.o4E.text())

			if self.gSelectedFurniture == "F0":
				self.createF0()
			
			if self.gSelectedFurniture == "F1":
				self.createF1()
			
			if self.gSelectedFurniture == "F2":
				self.mergeF("Bookcase_002.FCStd")

			if self.gSelectedFurniture == "F3":
				self.mergeF("Drawer_001.FCStd")
			
			if self.gSelectedFurniture == "F4":
				self.mergeF("Chair_001.FCStd")
				
			if self.gSelectedFurniture == "F5":
				self.mergeF("PictureFrame_002.FCStd")
			
			if self.gSelectedFurniture == "F6":
				self.mergeF("Table_001.FCStd")
			
			if self.gSelectedFurniture == "F7":
				self.mergeF("StorageBox_001.FCStd", "box")
			
			if self.gSelectedFurniture == "F8":
				self.mergeF("Dowel_8_x_35_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F9":
				self.mergeF("Screw_4_x_40_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F10":
				self.createF2()
				
		# ############################################################################	
		def selectedOption(self, selectedIndex):
			
			global gSelectedFurniture
			
			if selectedIndex == 0:
				self.gSelectedFurniture = "F0"
				self.setIcon("msf000")
				
			if selectedIndex == 1:
				self.gSelectedFurniture = "F1"
				self.setIcon("msf001")
				
			if selectedIndex == 2:
				self.gSelectedFurniture = "F2"
				self.setIcon("msf002")
			
			if selectedIndex == 3:
				self.gSelectedFurniture = "F3"
				self.setIcon("msf003")
			
			if selectedIndex == 4:
				self.gSelectedFurniture = "F4"
				self.setIcon("msf004")
			
			if selectedIndex == 5:
				self.gSelectedFurniture = "F5"
				self.setIcon("msf005")
			
			if selectedIndex == 6:
				self.gSelectedFurniture = "F6"
				self.setIcon("msf006")
			
			if selectedIndex == 7:
				self.gSelectedFurniture = "F7"
				self.setIcon("msf007")
			
			if selectedIndex == 8:
				self.gSelectedFurniture = "F8"
				self.setIcon("msf008")
			
			if selectedIndex == 9:
				self.gSelectedFurniture = "F9"
				self.setIcon("msf009")
			
			if selectedIndex == 10:
				self.gSelectedFurniture = "F10"
				self.setIcon("msf010")

			if (
				selectedIndex == 2 or  
				selectedIndex == 3 or
				selectedIndex == 4 or 
				selectedIndex == 5 or 
				selectedIndex == 6 or 
				selectedIndex == 7 or 
				selectedIndex == 8 or 
				selectedIndex == 9
				):
				self.setMergeInfo("show")
			else:
				self.setMergeInfo("hide")
			
			if selectedIndex == 10:
				self.o2E.setText("2300")
			else:
				self.o2E.setText("760")
			
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################

