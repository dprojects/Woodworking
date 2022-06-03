# -*- coding: utf-8 -*-

# magicManager tool for Magic Panels
# Author: Darek L (github.com/dprojects)

import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore
import MagicPanels


# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals
		# ############################################################################

		gMode = ""
		
		gPanel = ""
		gPanelTypes = []
		gPanelIndex = 0
		
		gEdgeTypes = []
		gEdgeIndex = 0
		
		gVertexTypes = []
		gVertexIndex = 0
		
		gObj = ""
		gFace1 = ""
		gFace2 = ""
		gFace3 = ""
		gColor = ""

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
			toolSH = 200
			
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
			self.setWindowTitle("magicManager")
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options
			# ############################################################################
			
			# screen
			self.oModeL = QtGui.QLabel("                                          ", self)
			self.oModeL.move(10, 10)

			# button - refresh
			self.oModeB1 = QtGui.QPushButton("refresh selection", self)
			self.oModeB1.clicked.connect(self.setMode)
			self.oModeB1.setFixedWidth(240)
			self.oModeB1.move(10, 30)

			# ############################################################################
			# options - panel
			# ############################################################################

			# label
			self.spL = QtGui.QLabel("Select panel:", self)
			self.spL.move(10, 73)

			# button - previous
			self.spBP = QtGui.QPushButton("<", self)
			self.spBP.clicked.connect(self.setPreviousPanel)
			self.spBP.setFixedWidth(50)
			self.spBP.move(100, 70)
			self.spBP.setAutoRepeat(True)

			# button - next
			self.spBN = QtGui.QPushButton(">", self)
			self.spBN.clicked.connect(self.setNextPanel)
			self.spBN.setFixedWidth(50)
			self.spBN.move(170, 70)
			self.spBN.setAutoRepeat(True)

			# ############################################################################
			# options - edge
			# ############################################################################

			# label
			self.seL = QtGui.QLabel("Select edge:", self)
			self.seL.move(10, 103)

			# button - previous
			self.seBP = QtGui.QPushButton("<", self)
			self.seBP.clicked.connect(self.setPreviousEdge)
			self.seBP.setFixedWidth(50)
			self.seBP.move(100, 100)
			self.seBP.setAutoRepeat(True)

			# button - next
			self.seBN = QtGui.QPushButton(">", self)
			self.seBN.clicked.connect(self.setNextEdge)
			self.seBN.setFixedWidth(50)
			self.seBN.move(170, 100)
			self.seBN.setAutoRepeat(True)

			# ############################################################################
			# options - vertex
			# ############################################################################

			# label
			self.svL = QtGui.QLabel("Select vertex:", self)
			self.svL.move(10, 133)

			# button - previous
			self.svBP = QtGui.QPushButton("<", self)
			self.svBP.clicked.connect(self.setPreviousVertex)
			self.svBP.setFixedWidth(50)
			self.svBP.move(100, 130)
			self.svBP.setAutoRepeat(True)

			# button - next
			self.svBN = QtGui.QPushButton(">", self)
			self.svBN.clicked.connect(self.setNextVertex)
			self.svBN.setFixedWidth(50)
			self.svBN.move(170, 130)
			self.svBN.setAutoRepeat(True)

			# ############################################################################
			# options - apply
			# ############################################################################

			# button - apply
			self.oSetB = QtGui.QPushButton("apply panel to this position", self)
			self.oSetB.clicked.connect(self.setPanel)
			self.oSetB.setFixedWidth(240)
			self.oSetB.move(10, 160)

			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()

			# init
			self.resetGlobals()
			self.setMode()

			
		# ############################################################################
		# actions - internal functions
		# ############################################################################

		# ############################################################################
		def projectPanelFace(self, iType):

			self.gPanel = FreeCAD.activeDocument().addObject("Part::Box", "panelFace"+iType)
			[ self.gPanel.Length, self.gPanel.Width, self.gPanel.Height ] = MagicPanels.sizesToCubePanel(self.gObj, iType)

			edge = self.gEdgeTypes[self.gEdgeIndex]
			vertex = self.gVertexTypes[self.gVertexIndex]
			[ x, y, z ] = MagicPanels.getVertex(self.gFace1, edge, vertex)

			self.gPanel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
			self.gPanel.ViewObject.ShapeColor = (0.0, 0.0, 0.0, 0.0)
			self.gPanel.ViewObject.Transparency = 83
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def projectPanelBetween(self, iType):

			[ x1, y1, z1 ] = MagicPanels.getVertex(self.gFace1, 0, 1)
			[ x2, y2, z2 ] = MagicPanels.getVertex(self.gFace2, 0, 1)

			x = abs(x2 - x1)
			y = abs(y2 - y1)
			z = abs(z2 - z1)

			self.gPanel = FreeCAD.activeDocument().addObject("Part::Box", "panelBetween"+iType)
			[ self.gPanel.Length, self.gPanel.Width, self.gPanel.Height ] = MagicPanels.sizesToCubePanel(self.gObj, iType)

			z1 = z1 + self.gObj.Height.Value - self.gPanel.Height.Value
			
			if x > 0:
				self.gPanel.Length = x
			
			if y > 0:
				self.gPanel.Width = y
				
			if z > 0:
				self.gPanel.Height = z

			self.gPanel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z1), FreeCAD.Rotation(0, 0, 0))
			self.gPanel.ViewObject.ShapeColor = (0.0, 0.0, 0.0, 0.0)
			self.gPanel.ViewObject.Transparency = 83
			FreeCAD.activeDocument().recompute()

		# ############################################################################
		def setSelection(self):
			
			self.resetGlobals()
			
			try:
				self.gObj = FreeCADGui.Selection.getSelection()[0]
				self.gColor = self.gObj.ViewObject.ShapeColor
			except:
				skip = 1
				
			try:
				self.gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
			except:
				skip = 1
			
			try:
				self.gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
			except:
				skip = 1

			FreeCADGui.Selection.clearSelection()
			
		# ############################################################################
		def setMode(self):
			
			try:
				FreeCAD.activeDocument().removeObject(str(self.gPanel.Name))
			except:
				skip = 1
				
			self.setSelection()
			
			if self.gFace1 == "":

				self.gMode = ""
				self.oModeL.setText("select 1 or 2 faces")
				
				self.seL.hide()
				self.seBP.hide()
				self.seBN.hide()
				
				self.svL.hide()
				self.svBP.hide()
				self.svBN.hide()
				
				return

			if self.gFace2 == "":

				self.gMode = "Face"
				self.oModeL.setText("Selection: 1 face")
				
				self.seL.show()
				self.seBP.show()
				self.seBN.show()
				
				self.svL.show()
				self.svBP.show()
				self.svBN.show()
				
			else:
				self.gMode = "Between"
				self.oModeL.setText("Selection: 2 faces")
				
				self.seL.hide()
				self.seBP.hide()
				self.seBN.hide()
				
				self.svL.hide()
				self.svBP.hide()
				self.svBN.hide()

		# ############################################################################
		def resetGlobals(self):
			
			self.gMode = ""

			self.gPanel = ""
			self.gPanelTypes = [ "XY", "YX", "XZ", "ZX", "YZ", "ZY" ]
			self.gPanelIndex = 5
			
			self.gObj = ""
			self.gFace1 = ""
			self.gFace2 = ""
			
			self.gEdgeTypes = [ 0, 1, 2, 3 ]
			self.gEdgeIndex = 0
		
			self.gVertexTypes = [ 0, 1 ]
			self.gVertexIndex = 1

		# ############################################################################
		# actions - buttons functions
		# ############################################################################

		# ############################################################################
		def previewPanel(self):
			
			try:
				FreeCAD.activeDocument().removeObject(str(self.gPanel.Name))
			except:
				skip = 1

			if self.gMode == "Face":
				self.projectPanelFace(self.gPanelTypes[self.gPanelIndex])

			if self.gMode == "Between":
				self.projectPanelBetween(self.gPanelTypes[self.gPanelIndex])

		# ############################################################################
		def setPreviousPanel(self):
			if self.gPanelIndex == 0:
				self.gPanelIndex = 5
			else:
				self.gPanelIndex = self.gPanelIndex - 1
			self.previewPanel()
			
		def setNextPanel(self):
			if self.gPanelIndex == 5:
				self.gPanelIndex = 0
			else:
				self.gPanelIndex = self.gPanelIndex + 1
			self.previewPanel()
			
		# ############################################################################
		def setPreviousEdge(self):
			if self.gEdgeIndex == 0:
				self.gEdgeIndex = 3
			else:
				self.gEdgeIndex = self.gEdgeIndex - 1
			self.previewPanel()

		def setNextEdge(self):
			if self.gEdgeIndex == 3:
				self.gEdgeIndex = 0
			else:
				self.gEdgeIndex = self.gEdgeIndex + 1
			self.previewPanel()
			
		# ############################################################################
		def setPreviousVertex(self):
			if self.gVertexIndex == 0:
				self.gVertexIndex = 1
			else:
				self.gVertexIndex = 0
			self.previewPanel()
			
		def setNextVertex(self):
			if self.gVertexIndex == 0:
				self.gVertexIndex = 1
			else:
				self.gVertexIndex = 0
			self.previewPanel()

		# ############################################################################
		def setPanel(self):
			if self.gPanel != "":
				self.gPanel.ViewObject.ShapeColor = self.gColor
				self.gPanel.ViewObject.Transparency = 0
				self.gPanel = ""
		
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		if form.gPanel != "":
			try:
				FreeCAD.activeDocument().removeObject(str(form.gPanel.Name))
			except:
				skip = 1

		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
