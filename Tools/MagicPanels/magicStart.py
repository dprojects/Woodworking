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
			toolSH = 550
			
			# active screen size - FreeCAD main window
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = 0 + 50
			gPH = int( gSH - toolSH ) - 30

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
				translate('magicStart', 'Bookcase ( import parametric )'), 
				translate('magicStart', 'Simple drawer ( import parametric )'), 
				translate('magicStart', 'Simple chair ( import parametric )'), 
				translate('magicStart', 'Picture frame ( import parametric )'), 
				translate('magicStart', 'Simple table ( import parametric )'), 
				translate('magicStart', 'Storage box ( import parametric )'), 
				translate('magicStart', 'Dowel 8x35 mm ( import parametric )'), 
				translate('magicStart', 'Screw 4x40 mm ( import parametric )'), 
				translate('magicStart', 'Modular storage'), 
				translate('magicStart', 'Screw 3x20 mm for HDF ( import parametric )'), 
				translate('magicStart', 'Screw 5x50 mm ( import parametric )'), 
				translate('magicStart', 'Counterbore 2x 5x60 mm ( import parametric )'), 
				translate('magicStart', 'Shelf Pin 5x16 mm ( import parametric )'), 
				translate('magicStart', 'Angle 40x40x100 mm ( import parametric )'), 
				translate('magicStart', 'Foot ( good for cleaning )'), 
				translate('magicStart', 'Foot ( standard )'), 
				translate('magicStart', 'Foot ( more stable )'), 
				translate('magicStart', 'Foot ( decorated )'), 
				translate('magicStart', 'Foot ( chair style )'), 
				translate('magicStart', 'Drawer with front outside ( fit into the shelf gap )'), 
				translate('magicStart', 'Drawer with front inside ( fit into the shelf gap )'), 
				translate('magicStart', 'Front outside ( fit into gap )'), 
				translate('magicStart', 'Front inside ( fit into gap )'), 
				translate('magicStart', 'Shelf ( fit into gap )')
				)
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(0)
			self.sMode.activated[int].connect(self.selectedOption)
			self.sMode.setFixedWidth(toolSW - 20)
			self.sMode.move(10, row)

			row += 50
			rowgap = row
			rowfoot = row
			rowfront = row
			rowshelf = row

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
			# GUI for merge (hidden by default)
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
			# GUI for furniture (visible by default)
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

			row += 60

			# button
			self.s1B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.s1B1.clicked.connect(self.createObject)
			self.s1B1.setFixedWidth(200)
			self.s1B1.setFixedHeight(40)
			self.s1B1.move(10, row)

			# ############################################################################
			# GUI for foot (hidden by default)
			# ############################################################################
			
			# label
			self.of1L = QtGui.QLabel(translate('magicStart', 'Furniture width:'), self)
			self.of1L.move(10, rowfoot+3)
			
			# text input
			self.of1E = QtGui.QLineEdit(self)
			self.of1E.setText(str(self.gFSX))
			self.of1E.setFixedWidth(90)
			self.of1E.move(120, rowfoot)

			rowfoot += 30

			# label
			self.of2L = QtGui.QLabel(translate('magicStart', 'Furniture depth:'), self)
			self.of2L.move(10, rowfoot+3)

			# text input
			self.of2E = QtGui.QLineEdit(self)
			self.of2E.setText(str(self.gFSY))
			self.of2E.setFixedWidth(90)
			self.of2E.move(120, rowfoot)

			rowfoot += 60

			# label
			self.of3L = QtGui.QLabel(translate('magicStart', 'Foot height:'), self)
			self.of3L.move(10, rowfoot+3)

			# text input
			self.of3E = QtGui.QLineEdit(self)
			self.of3E.setText("100")
			self.of3E.setFixedWidth(90)
			self.of3E.move(120, rowfoot)

			rowfoot += 30

			# label
			self.of4L = QtGui.QLabel(translate('magicStart', 'Foot thickness:'), self)
			self.of4L.move(10, rowfoot+3)

			# text input
			self.of4E = QtGui.QLineEdit(self)
			self.of4E.setText(str(self.gThick))
			self.of4E.setFixedWidth(90)
			self.of4E.move(120, rowfoot)

			rowfoot += 30

			# label
			self.of5L = QtGui.QLabel(translate('magicStart', 'Front offset:'), self)
			self.of5L.move(10, rowfoot+3)

			# text input
			self.of5E = QtGui.QLineEdit(self)
			self.of5E.setText(str(self.gThick))
			self.of5E.setFixedWidth(90)
			self.of5E.move(120, rowfoot)
			
			rowfoot += 60

			# button
			self.of6B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.of6B1.clicked.connect(self.createObject)
			self.of6B1.setFixedWidth(200)
			self.of6B1.setFixedHeight(40)
			self.of6B1.move(10, rowfoot)
			
			# hide by default
			self.of1L.hide()
			self.of1E.hide()
			self.of2L.hide()
			self.of2E.hide()
			self.of3L.hide()
			self.of3E.hide()
			self.of4L.hide()
			self.of4E.hide()
			self.of5L.hide()
			self.of5E.hide()
			self.of6B1.hide()

			# ############################################################################
			# GUI for drawer GAP (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 2 edges and face to calculate gap for drawer. First edge is starting Z axis position. Second selected edge is Z axis end position. Face is to calculate depth. If only one edge is selected, the starting Z axis point will be 0. If no face is selected, depth will be calculated from shortest shelf.')
			self.og1i = QtGui.QLabel(info, self)
			self.og1i.move(10, rowgap+3)
			self.og1i.setFixedWidth(200)
			self.og1i.setWordWrap(True)
			self.og1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowgap += 150
			
			# button
			self.og4B1 = QtGui.QPushButton(translate('magicStart', 'calculate gap'), self)
			self.og4B1.clicked.connect(self.calculateGapForDrawer)
			self.og4B1.setFixedWidth(200)
			self.og4B1.setFixedHeight(40)
			self.og4B1.move(10, rowgap)
			
			rowgap += 60
			
			# label
			self.og2L = QtGui.QLabel(translate('magicStart', 'Gap start XYZ:'), self)
			self.og2L.move(10, rowgap+3)
			
			# text input
			self.og2E = QtGui.QLineEdit(self)
			self.og2E.setText("0")
			self.og2E.setFixedWidth(80)
			self.og2E.move(120, rowgap)
			
			# text input
			self.og3E = QtGui.QLineEdit(self)
			self.og3E.setText("0")
			self.og3E.setFixedWidth(80)
			self.og3E.move(210, rowgap)
			
			# text input
			self.og4E = QtGui.QLineEdit(self)
			self.og4E.setText("0")
			self.og4E.setFixedWidth(80)
			self.og4E.move(300, rowgap)
			
			rowgap += 30

			# label
			self.og5L = QtGui.QLabel(translate('magicStart', 'Gap width:'), self)
			self.og5L.move(10, rowgap+3)
			
			# text input
			self.og5E = QtGui.QLineEdit(self)
			self.og5E.setText("400")
			self.og5E.setFixedWidth(90)
			self.og5E.move(120, rowgap)
			
			rowgap += 30
			
			# label
			self.og6L = QtGui.QLabel(translate('magicStart', 'Gap height:'), self)
			self.og6L.move(10, rowgap+3)

			# text input
			self.og6E = QtGui.QLineEdit(self)
			self.og6E.setText("150")
			self.og6E.setFixedWidth(90)
			self.og6E.move(120, rowgap)
			
			rowgap += 30
			
			# label
			self.og7L = QtGui.QLabel(translate('magicStart', 'Gap depth:'), self)
			self.og7L.move(10, rowgap+3)

			# text input
			self.og7E = QtGui.QLineEdit(self)
			self.og7E.setText("350")
			self.og7E.setFixedWidth(90)
			self.og7E.move(120, rowgap)
			
			rowgap += 30
			
			# label
			self.og8L = QtGui.QLabel(translate('magicStart', 'Wood thickness:'), self)
			self.og8L.move(10, rowgap+3)

			# text input
			self.og8E = QtGui.QLineEdit(self)
			self.og8E.setText(str(self.gThick))
			self.og8E.setFixedWidth(90)
			self.og8E.move(120, rowgap)
			
			rowgap += 30
			
			# label
			self.og9L = QtGui.QLabel(translate('magicStart', 'Drawer system offsets:'), self)
			self.og9L.move(10, rowgap+3)

			rowgap += 20
			
			# label
			self.og91L = QtGui.QLabel(translate('magicStart', 'Sides:'), self)
			self.og91L.move(10, rowgap+3)
			
			# label
			self.og92L = QtGui.QLabel(translate('magicStart', 'Back:'), self)
			self.og92L.move(110, rowgap+3)
			
			# label
			self.og93L = QtGui.QLabel(translate('magicStart', 'Top:'), self)
			self.og93L.move(210, rowgap+3)
			
			# label
			self.og94L = QtGui.QLabel(translate('magicStart', 'Bottom:'), self)
			self.og94L.move(310, rowgap+3)

			rowgap += 20
			
			# text input
			self.og91E = QtGui.QLineEdit(self)
			self.og91E.setText("26")
			self.og91E.setFixedWidth(50)
			self.og91E.move(10, rowgap)
			
			# text input
			self.og92E = QtGui.QLineEdit(self)
			self.og92E.setText("20")
			self.og92E.setFixedWidth(50)
			self.og92E.move(110, rowgap)
			
			# text input
			self.og93E = QtGui.QLineEdit(self)
			self.og93E.setText("30")
			self.og93E.setFixedWidth(50)
			self.og93E.move(210, rowgap)
			
			# text input
			self.og94E = QtGui.QLineEdit(self)
			self.og94E.setText("10")
			self.og94E.setFixedWidth(50)
			self.og94E.move(310, rowgap)

			rowgap += 40

			# button
			self.og9B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.og9B1.clicked.connect(self.createObject)
			self.og9B1.setFixedWidth(toolSW - 20)
			self.og9B1.setFixedHeight(40)
			self.og9B1.move(10, rowgap)

			# hide by default
			self.og1i.hide()
			self.og2L.hide()
			self.og2E.hide()
			self.og3E.hide()
			self.og4E.hide()
			self.og4B1.hide()
			self.og5L.hide()
			self.og5E.hide()
			self.og6L.hide()
			self.og6E.hide()
			self.og7L.hide()
			self.og7E.hide()
			self.og8L.hide()
			self.og8E.hide()
			self.og9L.hide()
			self.og91L.hide()
			self.og92L.hide()
			self.og93L.hide()
			self.og94L.hide()
			self.og91E.hide()
			self.og92E.hide()
			self.og93E.hide()
			self.og94E.hide()
			self.og9B1.hide()
			
			# ############################################################################
			# GUI for Front from GAP (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap to calculate front size in this order: <br><br> 1. selection - bottom edge <br> 2. selection - top edge <br> 3. selection - left edge <br> 4. selection - right edge')
			self.ofr1i = QtGui.QLabel(info, self)
			self.ofr1i.move(10, rowfront+3)
			self.ofr1i.setFixedWidth(200)
			self.ofr1i.setWordWrap(True)
			self.ofr1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowfront += 130
			
			# label
			self.ofr7L = QtGui.QLabel(translate('magicStart', 'Front thickness:'), self)
			self.ofr7L.move(10, rowfront+3)

			# text input
			self.ofr7E = QtGui.QLineEdit(self)
			self.ofr7E.setText("18")
			self.ofr7E.setFixedWidth(90)
			self.ofr7E.move(120, rowfront)
		
			rowfront += 40
			
			# label
			self.ofr8L = QtGui.QLabel(translate('magicStart', 'Front offsets:'), self)
			self.ofr8L.move(10, rowfront+3)

			rowfront += 20
			
			# label
			self.ofr81L = QtGui.QLabel(translate('magicStart', 'Left side:'), self)
			self.ofr81L.move(10, rowfront+3)
			
			# label
			self.ofr82L = QtGui.QLabel(translate('magicStart', 'Right side:'), self)
			self.ofr82L.move(110, rowfront+3)
			
			# label
			self.ofr83L = QtGui.QLabel(translate('magicStart', 'Top:'), self)
			self.ofr83L.move(210, rowfront+3)
			
			# label
			self.ofr84L = QtGui.QLabel(translate('magicStart', 'Bottom:'), self)
			self.ofr84L.move(310, rowfront+3)

			rowfront += 20
			
			# text input
			self.ofr81E = QtGui.QLineEdit(self)
			self.ofr81E.setText("0")
			self.ofr81E.setFixedWidth(50)
			self.ofr81E.move(10, rowfront)
			
			# text input
			self.ofr82E = QtGui.QLineEdit(self)
			self.ofr82E.setText("0")
			self.ofr82E.setFixedWidth(50)
			self.ofr82E.move(110, rowfront)
			
			# text input
			self.ofr83E = QtGui.QLineEdit(self)
			self.ofr83E.setText("0")
			self.ofr83E.setFixedWidth(50)
			self.ofr83E.move(210, rowfront)
			
			# text input
			self.ofr84E = QtGui.QLineEdit(self)
			self.ofr84E.setText("0")
			self.ofr84E.setFixedWidth(50)
			self.ofr84E.move(310, rowfront)

			rowfront += 40
			
			# button
			self.ofr4B1 = QtGui.QPushButton(translate('magicStart', 'calculate front'), self)
			self.ofr4B1.clicked.connect(self.calculateFrontFromGap)
			self.ofr4B1.setFixedWidth(200)
			self.ofr4B1.setFixedHeight(40)
			self.ofr4B1.move(10, rowfront)
			
			rowfront += 80
			
			# label
			self.ofr2L = QtGui.QLabel(translate('magicStart', 'Front start XYZ:'), self)
			self.ofr2L.move(10, rowfront+3)
			
			# text input
			self.ofr2E = QtGui.QLineEdit(self)
			self.ofr2E.setText("0")
			self.ofr2E.setFixedWidth(90)
			self.ofr2E.move(120, rowfront)
			
			# text input
			self.ofr3E = QtGui.QLineEdit(self)
			self.ofr3E.setText("0")
			self.ofr3E.setFixedWidth(90)
			self.ofr3E.move(220, rowfront)
			
			# text input
			self.ofr4E = QtGui.QLineEdit(self)
			self.ofr4E.setText("0")
			self.ofr4E.setFixedWidth(90)
			self.ofr4E.move(320, rowfront)
			
			rowfront += 30

			# label
			self.ofr5L = QtGui.QLabel(translate('magicStart', 'Front width:'), self)
			self.ofr5L.move(10, rowfront+3)
			
			# text input
			self.ofr5E = QtGui.QLineEdit(self)
			self.ofr5E.setText("0")
			self.ofr5E.setFixedWidth(90)
			self.ofr5E.move(120, rowfront)
			
			rowfront += 30
			
			# label
			self.ofr6L = QtGui.QLabel(translate('magicStart', 'Front height:'), self)
			self.ofr6L.move(10, rowfront+3)

			# text input
			self.ofr6E = QtGui.QLineEdit(self)
			self.ofr6E.setText("0")
			self.ofr6E.setFixedWidth(90)
			self.ofr6E.move(120, rowfront)
			
			rowfront += 40

			# button
			self.ofr8B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.ofr8B1.clicked.connect(self.createObject)
			self.ofr8B1.setFixedWidth(toolSW - 20)
			self.ofr8B1.setFixedHeight(40)
			self.ofr8B1.move(10, rowfront)

			# hide by default
			self.ofr1i.hide()
			self.ofr2L.hide()
			self.ofr2E.hide()
			self.ofr3E.hide()
			self.ofr4E.hide()
			self.ofr4B1.hide()
			self.ofr5L.hide()
			self.ofr5E.hide()
			self.ofr6L.hide()
			self.ofr6E.hide()
			self.ofr7L.hide()
			self.ofr7E.hide()
			self.ofr8L.hide()
			self.ofr81L.hide()
			self.ofr82L.hide()
			self.ofr83L.hide()
			self.ofr84L.hide()
			self.ofr81E.hide()
			self.ofr82E.hide()
			self.ofr83E.hide()
			self.ofr84E.hide()
			self.ofr8B1.hide()
			
			# ############################################################################
			# GUI for Shelf from GAP (hidden by default)
			# ############################################################################
			
			rowshelf -= 20
			
			# label
			info = translate('magicStart', 'Please select 2 edges and face to calculate shelf: <br><br> 1. selection - left edge <br> 2. selection - right edge <br> 3. selection - back face <br><br> Please add "Shelf by depth" or "Shelf by offsets", if you do not want full depth.')
			self.osh1i = QtGui.QLabel(info, self)
			self.osh1i.move(10, rowshelf+3)
			self.osh1i.setFixedWidth(200)
			self.osh1i.setWordWrap(True)
			self.osh1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowshelf += 150
			
			# label
			self.osh1L = QtGui.QLabel(translate('magicStart', 'Shelf thickness:'), self)
			self.osh1L.move(10, rowshelf+3)

			# text input
			self.osh1E = QtGui.QLineEdit(self)
			self.osh1E.setText("18")
			self.osh1E.setFixedWidth(90)
			self.osh1E.move(120, rowshelf)
		
			rowshelf += 30
			
			# label
			self.osh2L = QtGui.QLabel(translate('magicStart', 'Shelf by depth:'), self)
			self.osh2L.move(10, rowshelf+3)

			# text input
			self.osh2E = QtGui.QLineEdit(self)
			self.osh2E.setText("0")
			self.osh2E.setFixedWidth(90)
			self.osh2E.move(120, rowshelf)
			
			rowshelf += 30
			
			# label
			self.osh3L = QtGui.QLabel(translate('magicStart', 'Shelf by offsets:'), self)
			self.osh3L.move(10, rowshelf+3)

			rowshelf += 20
			
			# label
			self.osh31L = QtGui.QLabel(translate('magicStart', 'Left side:'), self)
			self.osh31L.move(10, rowshelf+3)
			
			# label
			self.osh32L = QtGui.QLabel(translate('magicStart', 'Right side:'), self)
			self.osh32L.move(110, rowshelf+3)
			
			# label
			self.osh33L = QtGui.QLabel(translate('magicStart', 'Front:'), self)
			self.osh33L.move(210, rowshelf+3)
			
			# label
			self.osh34L = QtGui.QLabel(translate('magicStart', 'Back:'), self)
			self.osh34L.move(310, rowshelf+3)

			rowshelf += 20
			
			# text input
			self.osh31E = QtGui.QLineEdit(self)
			self.osh31E.setText("0")
			self.osh31E.setFixedWidth(50)
			self.osh31E.move(10, rowshelf)
			
			# text input
			self.osh32E = QtGui.QLineEdit(self)
			self.osh32E.setText("0")
			self.osh32E.setFixedWidth(50)
			self.osh32E.move(110, rowshelf)
			
			# text input
			self.osh33E = QtGui.QLineEdit(self)
			self.osh33E.setText("0")
			self.osh33E.setFixedWidth(50)
			self.osh33E.move(210, rowshelf)
			
			# text input
			self.osh34E = QtGui.QLineEdit(self)
			self.osh34E.setText("0")
			self.osh34E.setFixedWidth(50)
			self.osh34E.move(310, rowshelf)

			rowshelf += 40
			
			# button
			self.osh4B1 = QtGui.QPushButton(translate('magicStart', 'calculate shelf'), self)
			self.osh4B1.clicked.connect(self.calculateShelfFromGap)
			self.osh4B1.setFixedWidth(200)
			self.osh4B1.setFixedHeight(40)
			self.osh4B1.move(10, rowshelf)
			
			rowshelf += 70
			
			# label
			self.osh5L = QtGui.QLabel(translate('magicStart', 'Shelf start XYZ:'), self)
			self.osh5L.move(10, rowshelf+3)
			
			# text input
			self.osh51E = QtGui.QLineEdit(self)
			self.osh51E.setText("0")
			self.osh51E.setFixedWidth(90)
			self.osh51E.move(120, rowshelf)
			
			# text input
			self.osh52E = QtGui.QLineEdit(self)
			self.osh52E.setText("0")
			self.osh52E.setFixedWidth(90)
			self.osh52E.move(220, rowshelf)
			
			# text input
			self.osh53E = QtGui.QLineEdit(self)
			self.osh53E.setText("0")
			self.osh53E.setFixedWidth(90)
			self.osh53E.move(320, rowshelf)
			
			rowshelf += 30

			# label
			self.osh6L = QtGui.QLabel(translate('magicStart', 'Calculated shelf width:'), self)
			self.osh6L.move(10, rowshelf+3)
			
			# text input
			self.osh6E = QtGui.QLineEdit(self)
			self.osh6E.setText("0")
			self.osh6E.setFixedWidth(90)
			self.osh6E.move(220, rowshelf)
			
			rowshelf += 30
			
			# label
			self.osh7L = QtGui.QLabel(translate('magicStart', 'Calculated shelf depth:'), self)
			self.osh7L.move(10, rowshelf+3)

			# text input
			self.osh7E = QtGui.QLineEdit(self)
			self.osh7E.setText("0")
			self.osh7E.setFixedWidth(90)
			self.osh7E.move(220, rowshelf)
			
			rowshelf += 40

			# button
			self.osh8B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.osh8B1.clicked.connect(self.createObject)
			self.osh8B1.setFixedWidth(toolSW - 20)
			self.osh8B1.setFixedHeight(40)
			self.osh8B1.move(10, rowshelf)

			# hide by default
			self.osh1i.hide()
			self.osh1L.hide()
			self.osh1E.hide()
			self.osh2L.hide()
			self.osh2E.hide()
			self.osh3L.hide()
			self.osh31L.hide()
			self.osh32L.hide()
			self.osh33L.hide()
			self.osh34L.hide()
			self.osh31E.hide()
			self.osh32E.hide()
			self.osh33E.hide()
			self.osh34E.hide()
			self.osh4B1.hide()
			self.osh5L.hide()
			self.osh51E.hide()
			self.osh52E.hide()
			self.osh53E.hide()
			self.osh6L.hide()
			self.osh6E.hide()
			self.osh7L.hide()
			self.osh7E.hide()
			self.osh8B1.hide()
			
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
			
			depth = self.gFSY - self.gThick
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(0, self.gThick, 0)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ - (2 * self.gThick)
			o2.Width = depth
			pl = FreeCAD.Vector(0, self.gThick, self.gThick)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ - (2 * self.gThick)
			o3.Width = depth
			pl = FreeCAD.Vector(self.gFSX - self.gThick, self.gThick, self.gThick)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.DiffuseColor = self.gColor
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX - (2 * self.gThick)
			o4.Height = self.gFSZ - (2 * self.gThick)
			o4.Width = self.gThick
			pl = FreeCAD.Vector(self.gThick, depth, self.gThick)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.DiffuseColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(0, self.gThick, self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.DiffuseColor = self.gColor
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = self.gFSX - self.gThick
			o6.Height = self.gFSZ - self.gThick - 4
			o6.Width = self.gThick
			pl = FreeCAD.Vector(self.gThick / 2, 0, (self.gThick / 2) + 2)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.DiffuseColor = self.gColor
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = self.gFSX - (2 * self.gThick)
			o7.Height = self.gThick
			o7.Width = depth - (3 * self.gThick)
			pl = FreeCAD.Vector(self.gThick, 3 * self.gThick, (self.gFSZ / 2) - (self.gThick / 2))
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			o7.ViewObject.DiffuseColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF1(self):
			
			depth = self.gFSY - 3
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX - (2 * self.gThick)
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(self.gThick, 0, self.gFSZ / 10)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ
			o2.Width = depth
			pl = FreeCAD.Vector(0, 0, 0)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ
			o3.Width = depth
			pl = FreeCAD.Vector(self.gFSX - self.gThick, 0, 0)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.DiffuseColor = self.gColor
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ - (self.gFSZ / 10)
			o4.Width = 3
			pl = FreeCAD.Vector(0, depth, self.gFSZ / 10)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.DiffuseColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX - (2 * self.gThick)
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(self.gThick, 0, self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.DiffuseColor = self.gColor

			# Shelf
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o6.Label = translate('magicStart', 'Shelf')
			o6.Length = self.gFSX - (2 * self.gThick)
			o6.Height = self.gThick
			o6.Width = depth
			pl = FreeCAD.Vector(self.gThick, 0, (self.gFSZ / 2) - (self.gThick / 2))
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.DiffuseColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF10(self):
			
			# calculation
			mNum = 3
			sideZ = ((self.gFSZ - self.gThick - (mNum * self.gThick)) / mNum)
			depth = self.gFSY - self.gThick
			
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
				o1.Width = depth
				pl = FreeCAD.Vector(0, self.gThick, posZ)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				o1.ViewObject.DiffuseColor = self.gColor
				
				# Left Side
				o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
				o2.Label = translate('magicStart', 'Left M'+str(i))
				o2.Length = self.gThick
				o2.Height = sideZ
				o2.Width = depth
				pl = FreeCAD.Vector(0, self.gThick, posZ + self.gThick)
				o2.Placement = FreeCAD.Placement(pl, self.gR)
				o2.ViewObject.DiffuseColor = self.gColor
				
				# Right Side
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
				o3.Label = translate('magicStart', 'Right M'+str(i))
				o3.Length = self.gThick
				o3.Height = sideZ
				o3.Width = depth
				pl = FreeCAD.Vector(self.gFSX - self.gThick, self.gThick, posZ + self.gThick)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				o3.ViewObject.DiffuseColor = self.gColor
				
				# Back
				o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
				o4.Label = translate('magicStart', 'Back M'+str(i))
				o4.Length = self.gFSX - (2 * self.gThick)
				o4.Height = sideZ
				o4.Width = self.gThick
				pl = FreeCAD.Vector(self.gThick, depth, posZ + self.gThick)
				o4.Placement = FreeCAD.Placement(pl, self.gR)
				o4.ViewObject.DiffuseColor = self.gColor
				
				# Front
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
				o5.Label = translate('magicStart', 'Front M'+str(i))
				o5.Length = self.gFSX - self.gThick
				o5.Height = sideZ + self.gThick - 4
				o5.Width = self.gThick
				pl = FreeCAD.Vector(self.gThick / 2, 0, posZ + (self.gThick / 2) + 2)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				o5.ViewObject.DiffuseColor = self.gColor
				
				# Shelf
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
				o6.Label = translate('magicStart', 'Shelf M'+str(i))
				o6.Length = self.gFSX - (2 * self.gThick)
				o6.Height = self.gThick
				o6.Width = depth - (3 * self.gThick)
				pZ = ((2 * i) + 1) * ((self.gThick + sideZ) / 2)
				pl = FreeCAD.Vector(self.gThick, 3 * self.gThick, pZ)
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
			t1.Width = depth
			pZ = mNum * (self.gThick + sideZ)
			pl = FreeCAD.Vector(0, self.gThick, pZ)
			t1.Placement = FreeCAD.Placement(pl, self.gR)
			t1.ViewObject.DiffuseColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF16(self):
			
			FSX = float(self.of1E.text())
			FSY = float(self.of2E.text())
			height = float(self.of3E.text())
			thick = float(self.of4E.text())
			frontOF = float(self.of5E.text())
			depth = self.gFSY - frontOF
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(0, frontOF, -height)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(FSX - thick, frontOF, -height)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFoot')
			container.setLink([o1, o2])
			container.Label = "Container, Foot"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF17(self):
			
			FSX = float(self.of1E.text())
			FSY = float(self.of2E.text())
			height = float(self.of3E.text())
			thick = float(self.of4E.text())
			frontOF = float(self.of5E.text())
			depth = FSY - frontOF
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(0, frontOF, -height)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(FSX - thick, frontOF, -height)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootBack")
			o3.Label = translate('magicStart', 'Foot Back')
			o3.Length = FSX - (2 * thick)
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(thick, frontOF + depth - thick, -height)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.DiffuseColor = self.gColor
			
			# Front
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootFront")
			o4.Label = translate('magicStart', 'Foot Front')
			o4.Length = FSX - (2 * thick)
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(thick, frontOF, -height)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.DiffuseColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFoot')
			container.setLink([o1, o2, o3, o4])
			container.Label = "Container, Foot"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF18(self):
			
			FSX = float(self.of1E.text())
			FSY = float(self.of2E.text())
			height = float(self.of3E.text())
			thick = float(self.of4E.text())
			frontOF = float(self.of5E.text())
			depth = FSY - frontOF

			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(0, frontOF, -height)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(FSX - thick, frontOF, -height)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootBack")
			o3.Label = translate('magicStart', 'Foot Back')
			o3.Length = FSX - (2 * thick)
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(thick, frontOF + depth - thick, -height)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.DiffuseColor = self.gColor
			
			# Front
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootFront")
			o4.Label = translate('magicStart', 'Foot Front')
			o4.Length = FSX - (2 * thick)
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(thick, frontOF, -height)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.DiffuseColor = self.gColor
			
			# Center
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootCenter")
			o5.Label = translate('magicStart', 'Foot Center')
			o5.Length = FSX - (2 * thick)
			o5.Height = height
			o5.Width = thick
			py = frontOF + (depth / 2) - (thick / 2)
			pl = FreeCAD.Vector(thick, py, -height)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.DiffuseColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFoot')
			container.setLink([o1, o2, o3, o4, o5])
			container.Label = "Container, Foot"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF19(self):
			
			FSX = float(self.of1E.text())
			FSY = float(self.of2E.text())
			height = float(self.of3E.text())
			thick = float(self.of4E.text())
			frontOF = float(self.of5E.text())
			depth = FSY - frontOF

			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(0, frontOF, -height)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(FSX - thick, frontOF, -height)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootBack")
			o3.Label = translate('magicStart', 'Foot Back')
			o3.Length = FSX - (2 * thick)
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(thick, frontOF + depth - thick, -height)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.DiffuseColor = self.gColor
			
			# Front
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootFront")
			o4.Label = translate('magicStart', 'Foot Front')
			o4.Length = FSX - (2 * thick)
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(thick, frontOF + thick, -height)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.DiffuseColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFoot')
			container.setLink([o1, o2, o3, o4])
			container.Label = "Container, Foot"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF20(self):
			
			FSX = float(self.of1E.text())
			FSY = float(self.of2E.text())
			height = float(self.of3E.text())
			thick = float(self.of4E.text())
			frontOF = float(self.of5E.text())
			depth = FSY - frontOF
			
			# Left Front
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeftFront")
			o1.Label = translate('magicStart', 'Foot Left Front')
			o1.Length = thick
			o1.Height = height
			o1.Width = thick
			pl = FreeCAD.Vector(0, frontOF, -height)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Left Back
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeftBack")
			o2.Label = translate('magicStart', 'Foot Left Back')
			o2.Length = thick
			o2.Height = height
			o2.Width = thick
			pl = FreeCAD.Vector(0, frontOF + depth - thick, -height)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			# Right Front
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRightFront")
			o3.Label = translate('magicStart', 'Foot Right Front')
			o3.Length = thick
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(FSX - thick, frontOF, -height)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.DiffuseColor = self.gColor
			
			# Right Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRightBack")
			o4.Label = translate('magicStart', 'Foot Right Back')
			o4.Length = thick
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(FSX - thick, frontOF + depth - thick, -height)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.DiffuseColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFoot')
			container.setLink([o1, o2, o3, o4])
			container.Label = "Container, Foot"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def calculateGapForDrawer(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			
			edge1 = False
			edge2 = False
			face1 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
			
			except:
				skip = 1
				
			try:
				obj2 = FreeCADGui.Selection.getSelection()[1]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
			except:
				skip = 1
			
			try:
				obj3 = FreeCADGui.Selection.getSelection()[1]
				face1 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
			
			except:
				skip = 1
				
			FreeCADGui.Selection.clearSelection()

			startX = 0
			startY = 0
			startZ = 0
			width = 0
			height = 0
			depth = 0
				
			if edge1 != False and edge2 != False:
				
				height = float(MagicPanels.touchTypo(edge2)[1].Z) - float(MagicPanels.touchTypo(edge1)[1].Z)
				
				# first short shelf and second long top
				if float(edge1.Length) < float(edge2.Length):
					width = float(edge1.Length)
					startX = float(MagicPanels.touchTypo(edge1)[1].X)
					startY = float(MagicPanels.touchTypo(edge2)[1].Y) # but shelf might be inside
					startZ = float(MagicPanels.touchTypo(edge1)[1].Z) # Z start should always be first selected
				
				# first long bottom floor and second short shelf
				else:
					width = float(edge2.Length)
					startX = float(MagicPanels.touchTypo(edge2)[1].X)
					startY = float(MagicPanels.touchTypo(edge1)[1].Y) # but shelf might be inside
					startZ = float(MagicPanels.touchTypo(edge1)[1].Z) # Z start should always be first selected
				
				# first short shelf and second long top
				if float(obj1.Width.Value) < float(obj2.Width.Value):
					depth = float(obj1.Width.Value)
				
				# first long bottom floor and second short shelf
				else:
					depth = float(obj2.Width.Value)

			if edge1 != False and edge2 == False:
				
				width = float(edge1.Length)
				height = float(MagicPanels.touchTypo(edge1)[1].Z)
				depth = float(obj1.Width.Value)
				startX = float(MagicPanels.touchTypo(edge1)[1].X)
				startY = float(MagicPanels.touchTypo(edge1)[1].Y)
				startZ = 0
			
			# try to fix depth if face selected
			if face1 != False:
				depth = float(face1.CenterOfMass.y) - startY
			
			# set values to text fields
			self.og2E.setText(str(startX))
			self.og3E.setText(str(startY))
			self.og4E.setText(str(startZ))
			self.og5E.setText(str(width))
			self.og6E.setText(str(height))
			self.og7E.setText(str(depth))

		# ############################################################################
		def createF21(self):
			
			p0X = float(self.og2E.text())
			p0Y = float(self.og3E.text())
			p0Z = float(self.og4E.text())
			
			gapX = float(self.og5E.text())
			gapZ = float(self.og6E.text())
			gapY = float(self.og7E.text())
			
			thick = float(self.og8E.text())
			
			sidesOF = float(self.og91E.text())
			sideOF = sidesOF / 2
			backOF = float(self.og92E.text())
			topOF = float(self.og93E.text())
			bottomOF = float(self.og94E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
			o1.Label = translate('magicStart', 'Drawer Left')
			o1.Length = thick
			o1.Height = gapZ - bottomOF - topOF - 3
			o1.Width = gapY - backOF
			pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z + bottomOF + 3)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
			o2.Label = translate('magicStart', 'Drawer Right')
			o2.Length = thick
			o2.Height = gapZ - bottomOF - topOF - 3
			o2.Width = gapY - backOF
			pl = FreeCAD.Vector(p0X + gapX - thick - sideOF, p0Y, p0Z + bottomOF + 3)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
			o3.Label = translate('magicStart', 'Drawer Back')
			o3.Length = gapX - (2 * thick) - sidesOF
			o3.Height = gapZ - bottomOF - topOF - 3
			o3.Width = thick
			pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y + gapY - thick - backOF, p0Z + bottomOF + 3)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.DiffuseColor = self.gColor
			
			# Front inside
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
			o4.Label = translate('magicStart', 'Drawer Front Inside')
			o4.Length = gapX - (2 * thick) - sidesOF
			o4.Height = gapZ - bottomOF - topOF - 3
			o4.Width = thick
			pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y, p0Z + bottomOF + 3)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.DiffuseColor = self.gColor

			# HDF bottom
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
			o5.Label = translate('magicStart', 'Drawer Bottom HDF')
			o5.Length = gapX - sidesOF
			o5.Height = 3
			o5.Width = gapY - backOF
			pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z  + bottomOF)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.DiffuseColor = self.gColor

			# Front outside
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
			o6.Label = translate('magicStart', 'Drawer Front Outside')
			o6.Length = gapX + thick
			o6.Height = gapZ + thick - 4
			o6.Width = thick
			pl = FreeCAD.Vector(p0X - (thick / 2), p0Y - thick, p0Z - (thick / 2) + 2)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.DiffuseColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDrawer')
			container.setLink([o1, o2, o3, o4, o5, o6])
			container.Label = "Container, Drawer"
		
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF22(self):
			
			p0X = float(self.og2E.text())
			p0Y = float(self.og3E.text())
			p0Z = float(self.og4E.text())
			
			gapX = float(self.og5E.text())
			gapZ = float(self.og6E.text())
			gapY = float(self.og7E.text())
			
			thick = float(self.og8E.text())
			
			sidesOF = float(self.og91E.text())
			sideOF = sidesOF / 2
			backOF = float(self.og92E.text())
			topOF = float(self.og93E.text())
			bottomOF = float(self.og94E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
			o1.Label = translate('magicStart', 'Drawer Left')
			o1.Length = thick
			o1.Height = gapZ - bottomOF - topOF - 3
			o1.Width = gapY - backOF - thick
			pl = FreeCAD.Vector(p0X + sideOF, p0Y + thick, p0Z + bottomOF + 3)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
			o2.Label = translate('magicStart', 'Drawer Right')
			o2.Length = thick
			o2.Height = gapZ - bottomOF - topOF - 3
			o2.Width = gapY - backOF - thick
			pl = FreeCAD.Vector(p0X + gapX - thick - sideOF, p0Y + thick, p0Z + bottomOF + 3)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.DiffuseColor = self.gColor
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
			o3.Label = translate('magicStart', 'Drawer Back')
			o3.Length = gapX - (2 * thick) - sidesOF
			o3.Height = gapZ - bottomOF - topOF - 3
			o3.Width = thick
			pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y + gapY - thick - backOF, p0Z + bottomOF + 3)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.DiffuseColor = self.gColor
			
			# Front inside
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
			o4.Label = translate('magicStart', 'Drawer Front Inside')
			o4.Length = gapX - (2 * thick) - sidesOF
			o4.Height = gapZ - bottomOF - topOF - 3
			o4.Width = thick
			pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y + thick, p0Z + bottomOF + 3)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.DiffuseColor = self.gColor

			# HDF bottom
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
			o5.Label = translate('magicStart', 'Drawer Bottom HDF')
			o5.Length = gapX - sidesOF
			o5.Height = 3
			o5.Width = gapY - backOF - thick
			pl = FreeCAD.Vector(p0X + sideOF, p0Y + thick, p0Z  + bottomOF)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.DiffuseColor = self.gColor

			# Front outside make inside as well
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
			o6.Label = translate('magicStart', 'Drawer Front Outside')
			o6.Length = gapX - 4
			o6.Height = gapZ - 4
			o6.Width = thick
			pl = FreeCAD.Vector(p0X + 2, p0Y, p0Z + 2)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.DiffuseColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDrawer')
			container.setLink([o1, o2, o3, o4, o5, o6])
			container.Label = "Container, Drawer"
		
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def calculateFrontFromGap(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			obj4 = False
			
			edge1 = False
			edge2 = False
			edge3 = False
			edge4 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				obj2 = FreeCADGui.Selection.getSelection()[0]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				obj3 = FreeCADGui.Selection.getSelection()[0]
				edge3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
				obj4 = FreeCADGui.Selection.getSelection()[0]
				edge4 = FreeCADGui.Selection.getSelectionEx()[3].SubObjects[0]
				
			except:
				return
				
			FreeCADGui.Selection.clearSelection()

			gh = float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z)
			gw = float(edge4.CenterOfMass.x) - float(edge3.CenterOfMass.x)
			
			sx = float(MagicPanels.touchTypo(edge1)[1].X)
			sy = float(MagicPanels.touchTypo(edge1)[1].Y)
			sz = float(MagicPanels.touchTypo(edge1)[1].Z)
			
			thick = float(self.ofr7E.text())
			
			offsetL = float(self.ofr81E.text())
			offsetR = float(self.ofr82E.text())
			offsetT = float(self.ofr83E.text())
			offsetB = float(self.ofr84E.text())
			
			# outside
			if self.gSelectedFurniture == "F23":
				width = offsetL + gw + offsetR
				height = offsetB + gh + offsetT
				startX = sx - offsetL
				startY = sy - thick
				startZ = sz - offsetB

			# inside
			if self.gSelectedFurniture == "F24":
				width = gw - offsetL - offsetR
				height = gh - offsetB - offsetT
				startX = sx + offsetL
				startY = sy
				startZ = sz + offsetB
	
			# set values to text fields
			self.ofr2E.setText(str(startX))
			self.ofr3E.setText(str(startY))
			self.ofr4E.setText(str(startZ))
			self.ofr5E.setText(str(width))
			self.ofr6E.setText(str(height))

		# ############################################################################
		def createF23(self):
			
			p0X = float(self.ofr2E.text())
			p0Y = float(self.ofr3E.text())
			p0Z = float(self.ofr4E.text())
			
			width = float(self.ofr5E.text())
			height = float(self.ofr6E.text())
			thick = float(self.ofr7E.text())
			
			# Front outside
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FrontOutside")
			o1.Label = translate('magicStart', 'Front outside')
			o1.Length = width
			o1.Height = height
			o1.Width = thick
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF24(self):

			p0X = float(self.ofr2E.text())
			p0Y = float(self.ofr3E.text())
			p0Z = float(self.ofr4E.text())
			
			width = float(self.ofr5E.text())
			height = float(self.ofr6E.text())
			thick = float(self.ofr7E.text())
			
			# Front outside
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FrontInside")
			o1.Label = translate('magicStart', 'Front inside')
			o1.Length = width
			o1.Height = height
			o1.Width = thick
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def calculateShelfFromGap(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			
			edge1 = False
			edge2 = False
			face1 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				obj2 = FreeCADGui.Selection.getSelection()[0]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				obj3 = FreeCADGui.Selection.getSelection()[0]
				face1 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
			except:
				return
				
			FreeCADGui.Selection.clearSelection()

			gdepth = float(face1.CenterOfMass.y) - float(edge1.CenterOfMass.y)
			gwidth = float(edge2.CenterOfMass.x) - float(edge1.CenterOfMass.x)
			
			sx = float(edge1.CenterOfMass.x)
			sy = float(edge1.CenterOfMass.y)
			sz = float(edge1.CenterOfMass.z)
			
			thick = float(self.osh1E.text())
			udepth = float(self.osh2E.text())
			
			offsetL = float(self.osh31E.text())
			offsetR = float(self.osh32E.text())
			offsetF = float(self.osh33E.text())
			offsetB = float(self.osh34E.text())
			
			width = gwidth - offsetL - offsetR
			
			if udepth == 0:
				depth = gdepth - offsetF - offsetB
			else:
				depth = udepth
				offsetB = 0
				offsetF = gdepth - depth
			
			startX = sx + offsetL
			startY = sy + offsetF
			startZ = sz

			# set values to text fields
			self.osh2E.setText(str(depth))
			self.osh31E.setText(str(offsetL))
			self.osh32E.setText(str(offsetR))
			self.osh33E.setText(str(offsetF))
			self.osh34E.setText(str(offsetB))
			
			self.osh51E.setText(str(startX))
			self.osh52E.setText(str(startY))
			self.osh53E.setText(str(startZ))
			
			self.osh6E.setText(str(width))
			self.osh7E.setText(str(depth))

		# ############################################################################
		def createF25(self):
	
			p0X = float(self.osh51E.text())
			p0Y = float(self.osh52E.text())
			p0Z = float(self.osh53E.text())
			
			width = float(self.osh6E.text())
			depth = float(self.osh7E.text())
			thick = float(self.osh1E.text())
			
			# Front outside
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o1.Label = translate('magicStart', 'Shelf')
			o1.Length = width
			o1.Height = thick
			o1.Width = depth
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.DiffuseColor = self.gColor
			
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
			
			if iType == "angles":
				path = FreeCADGui.activeWorkbench().path
				path = str(os.path.join(path, "Examples"))
				path = str(os.path.join(path, "Fixture"))
				path = str(os.path.join(path, "Angles"))
				path = str(os.path.join(path, iName))
				
			return path

		# ############################################################################
		def mergeF(self, iName, iType="F"):
		
			# merge
			FreeCAD.ActiveDocument.mergeProject(self.getPathToMerge(iName, iType))
		
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def setGUIInfo(self, iType="furniture"):

			# ##############################################
			# hide everything first
			# ##############################################
			
			# shelf
			self.osh1i.hide()
			self.osh1L.hide()
			self.osh1E.hide()
			self.osh2L.hide()
			self.osh2E.hide()
			self.osh3L.hide()
			self.osh31L.hide()
			self.osh32L.hide()
			self.osh33L.hide()
			self.osh34L.hide()
			self.osh31E.hide()
			self.osh32E.hide()
			self.osh33E.hide()
			self.osh34E.hide()
			self.osh4B1.hide()
			self.osh5L.hide()
			self.osh51E.hide()
			self.osh52E.hide()
			self.osh53E.hide()
			self.osh6L.hide()
			self.osh6E.hide()
			self.osh7L.hide()
			self.osh7E.hide()
			self.osh8B1.hide()

			# front
			self.ofr1i.hide()
			self.ofr2L.hide()
			self.ofr2E.hide()
			self.ofr3E.hide()
			self.ofr4E.hide()
			self.ofr4B1.hide()
			self.ofr5L.hide()
			self.ofr5E.hide()
			self.ofr6L.hide()
			self.ofr6E.hide()
			self.ofr7L.hide()
			self.ofr7E.hide()
			self.ofr8L.hide()
			self.ofr81L.hide()
			self.ofr82L.hide()
			self.ofr83L.hide()
			self.ofr84L.hide()
			self.ofr81E.hide()
			self.ofr82E.hide()
			self.ofr83E.hide()
			self.ofr84E.hide()
			self.ofr8B1.hide()
		
			# gap
			self.og1i.hide()
			self.og2L.hide()
			self.og2E.hide()
			self.og3E.hide()
			self.og4E.hide()
			self.og4B1.hide()
			self.og5L.hide()
			self.og5E.hide()
			self.og6L.hide()
			self.og6E.hide()
			self.og7L.hide()
			self.og7E.hide()
			self.og8L.hide()
			self.og8E.hide()
			self.og9L.hide()
			self.og91L.hide()
			self.og92L.hide()
			self.og93L.hide()
			self.og94L.hide()
			self.og91E.hide()
			self.og92E.hide()
			self.og93E.hide()
			self.og94E.hide()
			self.og9B1.hide()
		
			# foot
			self.of1L.hide()
			self.of1E.hide()
			self.of2L.hide()
			self.of2E.hide()
			self.of3L.hide()
			self.of3E.hide()
			self.of4L.hide()
			self.of4E.hide()
			self.of5L.hide()
			self.of5E.hide()
			self.of6B1.hide()
			
			# merge
			self.minfo.hide()
			
			# furniture (default)
			self.o1L.hide()
			self.o1E.hide()
			self.o2L.hide()
			self.o2E.hide()
			self.o3L.hide()
			self.o3E.hide()
			self.o4L.hide()
			self.o4E.hide()
			self.s1B1.hide()
			
			# ##############################################
			# show only needed
			# ##############################################
			
			if iType == "furniture":
				self.o1L.show()
				self.o1E.show()
				self.o2L.show()
				self.o2E.show()
				self.o3L.show()
				self.o3E.show()
				self.o4L.show()
				self.o4E.show()
				self.s1B1.show()

			if iType == "shelf":
				self.osh1i.show()
				self.osh1L.show()
				self.osh1E.show()
				self.osh2L.show()
				self.osh2E.show()
				self.osh3L.show()
				self.osh31L.show()
				self.osh32L.show()
				self.osh33L.show()
				self.osh34L.show()
				self.osh31E.show()
				self.osh32E.show()
				self.osh33E.show()
				self.osh34E.show()
				self.osh4B1.show()
				self.osh5L.show()
				self.osh51E.show()
				self.osh52E.show()
				self.osh53E.show()
				self.osh6L.show()
				self.osh6E.show()
				self.osh7L.show()
				self.osh7E.show()
				self.osh8B1.show()

			if iType == "front":
				self.ofr1i.show()
				self.ofr2L.show()
				self.ofr2E.show()
				self.ofr3E.show()
				self.ofr4E.show()
				self.ofr4B1.show()
				self.ofr5L.show()
				self.ofr5E.show()
				self.ofr6L.show()
				self.ofr6E.show()
				self.ofr7L.show()
				self.ofr7E.show()
				self.ofr8L.show()
				self.ofr81L.show()
				self.ofr82L.show()
				self.ofr83L.show()
				self.ofr84L.show()
				self.ofr81E.show()
				self.ofr82E.show()
				self.ofr83E.show()
				self.ofr84E.show()
				self.ofr8B1.show()
				
			if iType == "gap":
				self.og1i.show()
				self.og2L.show()
				self.og2E.show()
				self.og3E.show()
				self.og4E.show()
				self.og4B1.show()
				self.og5L.show()
				self.og5E.show()
				self.og6L.show()
				self.og6E.show()
				self.og7L.show()
				self.og7E.show()
				self.og8L.show()
				self.og8E.show()
				self.og9L.show()
				self.og91L.show()
				self.og92L.show()
				self.og93L.show()
				self.og94L.show()
				self.og91E.show()
				self.og92E.show()
				self.og93E.show()
				self.og94E.show()
				self.og9B1.show()

			if iType == "foot":
				self.of1L.show()
				self.of1E.show()
				self.of2L.show()
				self.of2E.show()
				self.of3L.show()
				self.of3E.show()
				self.of4L.show()
				self.of4E.show()
				self.of5L.show()
				self.of5E.show()
				self.of6B1.show()
			
			if iType == "merge":
				self.minfo.show()

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
				self.createF10()
			
			if self.gSelectedFurniture == "F11":
				self.mergeF("Screw_3_x_20_mm.FCStd", "mount")
				
			if self.gSelectedFurniture == "F12":
				self.mergeF("Screw_5_x_50_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F13":
				self.mergeF("Counterbore2x_5_x_60_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F14":
				self.mergeF("Shelf_Pin_5_x_16.FCStd", "mount")
			
			if self.gSelectedFurniture == "F15":
				self.mergeF("Angle_40_x_40_x_100_mm.FCStd", "angles")
			
			if self.gSelectedFurniture == "F16":
				self.createF16()
			
			if self.gSelectedFurniture == "F17":
				self.createF17()
				
			if self.gSelectedFurniture == "F18":
				self.createF18()
				
			if self.gSelectedFurniture == "F19":
				self.createF19()
				
			if self.gSelectedFurniture == "F20":
				self.createF20()
			
			if self.gSelectedFurniture == "F21":
				self.createF21()
			
			if self.gSelectedFurniture == "F22":
				self.createF22()
			
			if self.gSelectedFurniture == "F23":
				self.createF23()
			
			if self.gSelectedFurniture == "F24":
				self.createF24()
			
			if self.gSelectedFurniture == "F25":
				self.createF25()
				
		# ############################################################################	
		def selectedOption(self, selectedIndex):
			
			global gSelectedFurniture
			
			self.gSelectedFurniture = "F"+str(selectedIndex)
			
			if selectedIndex < 10:
				self.setIcon("msf00"+str(selectedIndex))
			if selectedIndex >= 10 and selectedIndex < 100:
				self.setIcon("msf0"+str(selectedIndex))
			if selectedIndex >= 100:
				self.setIcon("msf"+str(selectedIndex))
				
			if (
				selectedIndex == 2 or 
				selectedIndex == 3 or 
				selectedIndex == 4 or 
				selectedIndex == 5 or 
				selectedIndex == 6 or 
				selectedIndex == 7 or 
				selectedIndex == 8 or 
				selectedIndex == 9 or 
				selectedIndex == 11 or 
				selectedIndex == 12 or 
				selectedIndex == 13 or 
				selectedIndex == 14 or 
				selectedIndex == 15
				):
				self.setGUIInfo("merge")
				
			if (
				selectedIndex == 0 or 
				selectedIndex == 1 or 
				selectedIndex == 10
				):
				self.setGUIInfo()
			
			if (
				selectedIndex == 16 or 
				selectedIndex == 17 or 
				selectedIndex == 18 or 
				selectedIndex == 19 or 
				selectedIndex == 20
				):
				self.setGUIInfo("foot")
			
			if selectedIndex == 21 or selectedIndex == 22:
				self.setGUIInfo("gap")
			
			if selectedIndex == 23:
				self.setGUIInfo("front")
				self.ofr7E.setText("18")
				self.ofr81E.setText("9")
				self.ofr82E.setText("9")
				self.ofr83E.setText("7")
				self.ofr84E.setText("7")
			
			if selectedIndex == 24:
				self.setGUIInfo("front")
				self.ofr7E.setText("18")
				self.ofr81E.setText("2")
				self.ofr82E.setText("2")
				self.ofr83E.setText("2")
				self.ofr84E.setText("2")
			
			if selectedIndex == 25:
				self.setGUIInfo("shelf")
				
			if selectedIndex == 10:
				self.o2E.setText("2300")
			else:
				self.o2E.setText("760")
				
			if selectedIndex == 20:
				self.of4E.setText("80")
			else:
				self.of4E.setText("18")
			
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

