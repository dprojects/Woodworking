import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# Global definitions
# ############################################################################

# add new items only at the end and change self.sModeList
getMenuIndex1 = {
	translate('magicGlue', 'Glue position'): 0, 
	translate('magicGlue', 'Glue size'): 1, 
	translate('magicGlue', 'Clean glue'): 2
}

# ############################################################################
# Qt Main
# ############################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals
		# ############################################################################
		
		gModeType = getMenuIndex1[translate('magicGlue', 'Glue position')]
		
		gInfoPositionX = translate('magicGlue', 'Position along X:')
		gInfoPositionY = translate('magicGlue', 'Position along Y:')
		gInfoPositionZ = translate('magicGlue', 'Position along Z:')
		
		gNoGPSO = translate('magicGlue', 'vertex or face as source')
		gNoGPTO = translate('magicGlue', 'objects as target')
		gNoGSSO = translate('magicGlue', 'edge as source')
		gNoGSTO = translate('magicGlue', 'edges as target')
		gNoGCO = translate('magicGlue', 'select objects to clean glue')
		
		gGPSO = [] # glue position source object [ obj, face ]
		gGPTO = [] # glue position target objects [ obj1, obj2, ... ]
		gGSSO = [] # glue size source object [ obj, edge ]
		gGSTO = [] # glue size target objects [ edge1, edge2, ... ]
		gGCO = [] # glue clean objects [ obj1, obj2, ... ]
		
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
			toolSW = 310
			toolSH = 520
			
			rside = toolSW - 20
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('magicGlue', 'magicGlue'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			self.setMinimumWidth(toolSW)
			self.setMinimumHeight(toolSH)
			
			# ############################################################################
			# GUI for common selection part (visible by default)
			# ############################################################################

			# not write here, copy text from getMenuIndex1 to avoid typo
			self.sModeList = (
				translate('magicGlue', 'Glue position'), 
				translate('magicGlue', 'Glue size'), 
				translate('magicGlue', 'Clean glue')
				)
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(0) # default
			self.sMode.textActivated[str].connect(self.setModeType)

			# ############################################################################
			# settigns for custom GUI
			# ############################################################################

			btsize = 50
			btoffset = 5
			cbt1 = rside - (2 * btsize) - btoffset + 5
			cbt2 = rside - btsize + btoffset + 5
	
			# ############################################################################
			# GUI for glue position (visible by default)
			# ############################################################################

			self.gp1B = QtGui.QPushButton(translate('magicGlue', 'set'), self)
			self.gp1B.clicked.connect(self.setGPSO)
			self.gp1B.setFixedWidth(60)
			
			self.gp1L = QtGui.QLabel(self.gNoGPSO, self)
			self.gp1L.setFixedWidth(rside - 80)
			
			self.gp2B = QtGui.QPushButton(translate('magicGlue', 'set'), self)
			self.gp2B.clicked.connect(self.setGPTO)
			self.gp2B.setFixedWidth(60)
			
			self.gp2L = QtGui.QLabel(self.gNoGPTO, self)
			self.gp2L.setFixedWidth(rside - 80)
			
			self.gp3B = QtGui.QPushButton(translate('magicGlue', 'refresh all selection'), self)
			self.gp3B.clicked.connect(self.setGPAll)
			self.gp3B.setFixedHeight(40)
			
			# label
			self.gp4L = QtGui.QLabel(self.gInfoPositionX, self)

			# button
			self.gp4B = QtGui.QPushButton(translate('magicGlue', 'add glue'), self)
			self.gp4B.clicked.connect(self.gluePositionX)
			self.gp4B.setFixedWidth(2 * btsize + 10)
			self.gp4B.setAutoRepeat(False)

			# label
			self.gp5L = QtGui.QLabel(self.gInfoPositionY, self)

			# button
			self.gp5B = QtGui.QPushButton(translate('magicGlue', 'add glue'), self)
			self.gp5B.clicked.connect(self.gluePositionY)
			self.gp5B.setFixedWidth(2 * btsize + 10)
			self.gp5B.setAutoRepeat(False)

			# label
			self.gp6L = QtGui.QLabel(self.gInfoPositionZ, self)

			# button
			self.gp6B = QtGui.QPushButton(translate('magicGlue', 'add glue'), self)
			self.gp6B.clicked.connect(self.gluePositionZ)
			self.gp6B.setFixedWidth(2 * btsize + 10)
			self.gp6B.setAutoRepeat(False)

			# ############################################################################
			# GUI for glue size (hidden by default)
			# ############################################################################
			
			self.gs1B = QtGui.QPushButton(translate('magicGlue', 'set'), self)
			self.gs1B.clicked.connect(self.setGSSO)
			self.gs1B.setFixedWidth(60)
			
			self.gs1L = QtGui.QLabel(self.gNoGSSO, self)
			self.gs1L.setFixedWidth(rside - 80)
			
			self.gs2B = QtGui.QPushButton(translate('magicGlue', 'set'), self)
			self.gs2B.clicked.connect(self.setGSTO)
			self.gs2B.setFixedWidth(60)
			
			self.gs2L = QtGui.QLabel(self.gNoGSTO, self)
			self.gs2L.setFixedWidth(rside - 80)
			
			self.gs3B = QtGui.QPushButton(translate('magicGlue', 'refresh all selection'), self)
			self.gs3B.clicked.connect(self.setGSAll)
			self.gs3B.setFixedHeight(40)
		
			# button
			self.gs4B = QtGui.QPushButton(translate('magicGlue', 'add glue size'), self)
			self.gs4B.clicked.connect(self.glueSize)
			self.gs4B.setFixedHeight(40)
			self.gs4B.setAutoRepeat(False)

			# ############################################################################
			# GUI for glue clean (hidden by default)
			# ############################################################################
			
			self.gc1L = QtGui.QLabel(self.gNoGCO, self)
			self.gc1L.setFixedWidth(rside - 20)
			
			self.gc2B = QtGui.QPushButton(translate('magicGlue', 'refresh all selection'), self)
			self.gc2B.clicked.connect(self.setGCO)
			self.gc2B.setFixedHeight(40)
		
			# button
			self.gc3B = QtGui.QPushButton(translate('magicGlue', 'clean glue position'), self)
			self.gc3B.clicked.connect(self.glueCleanPosition)
			self.gc3B.setFixedHeight(40)
			self.gc3B.setAutoRepeat(False)
			
			# button
			self.gc4B = QtGui.QPushButton(translate('magicGlue', 'clean glue size'), self)
			self.gc4B.clicked.connect(self.glueCleanSize)
			self.gc4B.setFixedHeight(40)
			self.gc4B.setAutoRepeat(False)

			self.oVarSetCB = QtGui.QCheckBox(translate('magicGlue', ' - use VarSet'), self)
			self.oVarSetCB.setCheckState(QtCore.Qt.Unchecked)
			
			# ############################################################################
			# GUI for common foot
			# ############################################################################
			
			if self.gCornerCrossSupport == True:
			
				# label
				self.cocL = QtGui.QLabel(translate('magicGlue', 'Corner cross:'), self)

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
				self.cecL = QtGui.QLabel(translate('magicGlue', 'Center cross:'), self)

				# button
				self.cecB1 = QtGui.QPushButton(translate('magicGlue', 'on'), self)
				self.cecB1.clicked.connect(self.setCenterOn)
				self.cecB1.setFixedWidth(btsize)
				self.cecB1.setAutoRepeat(True)
				
				# button
				self.cecB2 = QtGui.QPushButton(translate('magicGlue', 'off'), self)
				self.cecB2.clicked.connect(self.setCenterOff)
				self.cecB2.setFixedWidth(btsize)
				self.cecB2.setAutoRepeat(True)

			if self.gCornerCrossSupport == True or self.gAxisCrossSupport == True:

				self.kccscb = QtGui.QCheckBox(translate('magicGlue', ' - keep custom cross settings'), self)
				self.kccscb.setCheckState(QtCore.Qt.Unchecked)
		
			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.rowH = QtGui.QVBoxLayout()
			self.rowH.addWidget(self.sMode)
			
			# create body - position
			self.rowB1P1 = QtGui.QHBoxLayout()
			self.rowB1P1.addWidget(self.gp1B)
			self.rowB1P1.addWidget(self.gp1L)
			self.rowB1P2 = QtGui.QHBoxLayout()
			self.rowB1P2.addWidget(self.gp2B)
			self.rowB1P2.addWidget(self.gp2L)
			self.rowB1P3 = QtGui.QHBoxLayout()
			self.rowB1P3.addWidget(self.gp3B)
			self.rowBP1 = QtGui.QVBoxLayout()
			self.rowBP1.addLayout(self.rowB1P1)
			self.rowBP1.addLayout(self.rowB1P2)
			self.rowBP1.addLayout(self.rowB1P3)
			self.groupBodyPosition1 = QtGui.QGroupBox(None, self)
			self.groupBodyPosition1.setLayout(self.rowBP1)

			self.rowB2P1 = QtGui.QHBoxLayout()
			self.rowB2P1.addWidget(self.gp4L)
			self.rowB2P1.addWidget(self.gp4B)
			self.rowB2P2 = QtGui.QHBoxLayout()
			self.rowB2P2.addWidget(self.gp5L)
			self.rowB2P2.addWidget(self.gp5B)
			self.rowB2P3 = QtGui.QHBoxLayout()
			self.rowB2P3.addWidget(self.gp6L)
			self.rowB2P3.addWidget(self.gp6B)
			self.rowBP2 = QtGui.QVBoxLayout()
			self.rowBP2.addLayout(self.rowB2P1)
			self.rowBP2.addLayout(self.rowB2P2)
			self.rowBP2.addLayout(self.rowB2P3)
			self.groupBodyPosition2 = QtGui.QGroupBox(None, self)
			self.groupBodyPosition2.setLayout(self.rowBP2)

			# create body - size
			self.rowB1S1 = QtGui.QHBoxLayout()
			self.rowB1S1.addWidget(self.gs1B)
			self.rowB1S1.addWidget(self.gs1L)
			self.rowB1S2 = QtGui.QHBoxLayout()
			self.rowB1S2.addWidget(self.gs2B)
			self.rowB1S2.addWidget(self.gs2L)
			self.rowB1S3 = QtGui.QHBoxLayout()
			self.rowB1S3.addWidget(self.gs3B)
			self.rowBS1 = QtGui.QVBoxLayout()
			self.rowBS1.addLayout(self.rowB1S1)
			self.rowBS1.addLayout(self.rowB1S2)
			self.rowBS1.addLayout(self.rowB1S3)
			self.groupBodySize1 = QtGui.QGroupBox(None, self)
			self.groupBodySize1.setLayout(self.rowBS1)

			self.rowB2S2 = QtGui.QHBoxLayout()
			self.rowB2S2.addWidget(self.gs4B)
			self.rowBS2 = QtGui.QVBoxLayout()
			self.rowBS2.addLayout(self.rowB2S2)
			self.groupBodySize2 = QtGui.QGroupBox(None, self)
			self.groupBodySize2.setLayout(self.rowBS2)

			# create body - clean
			self.rowB1C1 = QtGui.QVBoxLayout()
			self.rowB1C1.addWidget(self.gc1L)
			self.rowB1C1.addWidget(self.gc2B)
			self.groupBodyClean1 = QtGui.QGroupBox(None, self)
			self.groupBodyClean1.setLayout(self.rowB1C1)

			self.rowB1C2 = QtGui.QVBoxLayout()
			self.rowB1C2.addWidget(self.gc3B)
			self.rowB1C2.addWidget(self.gc4B)
			self.groupBodyClean2 = QtGui.QGroupBox(None, self)
			self.groupBodyClean2.setLayout(self.rowB1C2)
			
			self.layVarSet = QtGui.QVBoxLayout()
			self.layVarSet.addWidget(self.oVarSetCB)
			
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
			
			self.layout.addLayout(self.rowH)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBodyPosition1)
			self.layout.addWidget(self.groupBodyPosition2)
			self.layout.addWidget(self.groupBodySize1)
			self.layout.addWidget(self.groupBodySize2)
			self.layout.addWidget(self.groupBodyClean1)
			self.layout.addWidget(self.groupBodyClean2)
			self.layout.addStretch()
			self.layout.addLayout(self.layVarSet)
			self.layout.addStretch()
			self.layout.addLayout(self.layoutFoot)
			self.setLayout(self.layout)
		
			self.groupBodySize1.hide()
			self.groupBodySize2.hide()
			self.groupBodyClean1.hide()
			self.groupBodyClean2.hide()

			if MagicPanels.gKernelVersion < 1.0:
				self.oVarSetCB.hide()

			# ############################################################################
			# show & init defaults
			# ############################################################################

			# init
			self.show()
			
			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)

			if self.gAxisCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			
			if self.gCornerCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(50)
			
			# set window position
			sw = self.width()
			sh = self.height()
			pw = int( FreeCADGui.getMainWindow().width() - sw ) - 5
			ph = 55
			self.setGeometry(pw, ph, sw, sh)

			self.setGPAll()
		
		# ############################################################################
		# actions - menu selections
		# ############################################################################

		# ############################################################################	
		def setModeType(self, selectedText):
			
			selectedIndex = getMenuIndex1[selectedText]
			self.gModeType = selectedIndex

			# first hide all
			self.groupBodyPosition1.hide()
			self.groupBodyPosition2.hide()
			self.groupBodySize1.hide()
			self.groupBodySize2.hide()
			self.groupBodyClean1.hide()
			self.groupBodyClean2.hide()
		
			# position
			if selectedIndex == 0:
				
				self.groupBodyPosition1.show()
				self.groupBodyPosition2.show()
				self.oVarSetCB.show()
				
				self.gp4L.setText(self.gInfoPositionX)
				self.gp5L.setText(self.gInfoPositionY)
				self.gp6L.setText(self.gInfoPositionZ)

			# size
			if selectedIndex == 1:
				
				self.groupBodySize1.show()
				self.groupBodySize2.show()
				self.oVarSetCB.show()

			# clean
			if selectedIndex == 2:
				
				self.groupBodyClean1.show()
				self.groupBodyClean2.show()
				self.oVarSetCB.hide()

			if MagicPanels.gKernelVersion < 1.0:
				self.oVarSetCB.hide()

		# ############################################################################
		# actions - glue positions
		# ############################################################################
		
		# ############################################################################
		def setGPAll(self):
			
			try:
			
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				obs = FreeCADGui.Selection.getSelection()[1:]

				if sub.ShapeType != "Face" and sub.ShapeType != "Vertex":
					raise
				
				self.gGPSO = [ obj, sub ]
				
				self.gGPTO = []
				for o in obs:
					toMove = MagicPanels.getObjectToMove(o)
					self.gGPTO.append(toMove)
				
				if sub.ShapeType == "Face":
					index = MagicPanels.getFaceIndex(self.gGPSO[0], self.gGPSO[1])
					info1 = self.gGPSO[0].Label + ", Face" + str(index)
				
				if sub.ShapeType == "Vertex":
					index = MagicPanels.getVertexIndex(self.gGPSO[0], self.gGPSO[1])
					info1 = self.gGPSO[0].Label + ", Vertex" + str(index)
				
				if len(self.gGPTO) > 1:
					info2 = "Multi, "+str(self.gGPTO[0].Label)
				else:
					info2 = str(self.gGPTO[0].Label)
				
				self.gp1L.setText(info1)
				self.gp2L.setText(info2)
				FreeCADGui.Selection.clearSelection()

			except:
			
				self.gp1L.setText(self.gNoGPSO)
				self.gp2L.setText(self.gNoGPTO)
		
		# ############################################################################
		def setGPSO(self):
			
			try:
			
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

				if sub.ShapeType != "Face" and sub.ShapeType != "Vertex":
					raise
				
				self.gGPSO = [ obj, sub ]
				
				if sub.ShapeType == "Face":
					index = MagicPanels.getFaceIndex(self.gGPSO[0], self.gGPSO[1])
					info1 = self.gGPSO[0].Label + ", Face" + str(index)
				
				if sub.ShapeType == "Vertex":
					index = MagicPanels.getVertexIndex(self.gGPSO[0], self.gGPSO[1])
					info1 = self.gGPSO[0].Label + ", Vertex" + str(index)
				
				self.gp1L.setText(info1)
				FreeCADGui.Selection.clearSelection()
			
			except:
			
				self.gp1L.setText(self.gNoGPSO)

		# ############################################################################
		def setGPTO(self):
			
			try:
			
				obs = FreeCADGui.Selection.getSelection()

				self.gGPTO = []
				for o in obs:
					toMove = MagicPanels.getObjectToMove(o)
					self.gGPTO.append(toMove)
				
				if len(self.gGPTO) > 1:
					info2 = "Multi, "+str(self.gGPTO[0].Label)
				else:
					info2 = str(self.gGPTO[0].Label)
				
				self.gp2L.setText(info2)
				FreeCADGui.Selection.clearSelection()
				
			except:
			
				self.gp2L.setText(self.gNoGPTO)

		# ############################################################################
		def gluePosition(self, iType):
			
			sub = self.gGPSO[1]
			
			if sub.ShapeType == "Face":
				
				subObjName = str(self.gGPSO[0].Name)
				subArrIndex = MagicPanels.getFaceIndex(self.gGPSO[0], self.gGPSO[1]) - 1
				
				sX = float(sub.CenterOfMass.x)
				sY = float(sub.CenterOfMass.y)
				sZ = float(sub.CenterOfMass.z)
			
			if sub.ShapeType == "Vertex":
				
				subObjName = str(self.gGPSO[0].Name)
				subArrIndex = MagicPanels.getVertexIndex(self.gGPSO[0], self.gGPSO[1]) - 1
				
				sX = float(sub.X)
				sY = float(sub.Y)
				sZ = float(sub.Z)
				
			obs = self.gGPTO

			for o in obs:
			
				if iType == "X":
					
					opx = float(o.Placement.Base.x)
					offset = abs(opx - sX)
					
					expr = "<<" + subObjName + ">>"
					
					if sub.ShapeType == "Face":
						expr += ".Shape.Faces[" + str(subArrIndex) + "].CenterOfMass.x"
					
					if sub.ShapeType == "Vertex":
						expr += ".Shape.Vertex"+"es[" + str(subArrIndex) + "].X"
					
					if opx > sX:
						expr += " + " + str(offset)
					else:
						expr += " - " + str(offset)
					
					o.setExpression('.Placement.Base.x', expr)
				
				if iType == "Y":
					
					opy = float(o.Placement.Base.y)
					offset = abs(opy - sY)
					
					expr = "<<" + subObjName + ">>"
					
					if sub.ShapeType == "Face":
						expr += ".Shape.Faces[" + str(subArrIndex) + "].CenterOfMass.y"
					
					if sub.ShapeType == "Vertex":
						expr += ".Shape.Vertex"+"es[" + str(subArrIndex) + "].Y"
					
					if opy > sY:
						expr += " + " + str(offset)
					else:
						expr += " - " + str(offset)
					
					o.setExpression('.Placement.Base.y', expr)
					
				if iType == "Z":
					
					opz = float(o.Placement.Base.z)
					offset = abs(opz - sZ)
					
					expr = "<<" + subObjName + ">>"
					
					if sub.ShapeType == "Face":
						expr += ".Shape.Faces[" + str(subArrIndex) + "].CenterOfMass.z"
					
					if sub.ShapeType == "Vertex":
						expr += ".Shape.Vertex"+"es[" + str(subArrIndex) + "].Z"
					
					if opz > sZ:
						expr += " + " + str(offset)
					else:
						expr += " - " + str(offset)
					
					o.setExpression('.Placement.Base.z', expr)
				
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def gluePositionVarSet(self, iType):
			
			sub = self.gGPSO[1]
			pgroup = translate('magicGlue', 'Glue position')

			if sub.ShapeType == "Face":
				
				sX = float(sub.CenterOfMass.x)
				sY = float(sub.CenterOfMass.y)
				sZ = float(sub.CenterOfMass.z)
				
				subIndex = MagicPanels.getFaceIndex(self.gGPSO[0], self.gGPSO[1])
				
				if iType == "X":
					pname = str(self.gGPSO[0].Name) + "_" + "Face"+str(subIndex) + "_x"
					pvalue = sX
				if iType == "Y":
					pvalue = sY
					pname = str(self.gGPSO[0].Name) + "_" + "Face"+str(subIndex) + "_y"
				if iType == "Z":
					pvalue = sZ
					pname = str(self.gGPSO[0].Name) + "_" + "Face"+str(subIndex) + "_z"
					
			if sub.ShapeType == "Vertex":
				
				pname =  str(self.gGPSO[0].Name) + "_" + "Vertex"+str(subIndex)
				
				sX = float(sub.X)
				sY = float(sub.Y)
				sZ = float(sub.Z)
				
				subIndex = MagicPanels.getVertexIndex(self.gGPSO[0], self.gGPSO[1])

				if iType == "X":
					pname =  str(self.gGPSO[0].Name) + "_" + "Vertex"+str(subIndex) + "_X"
					pvalue = sX
				if iType == "Y":
					pvalue = sY
					pname =  str(self.gGPSO[0].Name) + "_" + "Vertex"+str(subIndex) + "_Y"
				if iType == "Z":
					pvalue = sZ
					pname =  str(self.gGPSO[0].Name) + "_" + "Vertex"+str(subIndex) + "_Z"
			
			# create VarSet by Label to allow rename file and keep multi files
			try:
				varset = FreeCAD.ActiveDocument.getObjectsByLabel('magicGlueVarSet')[0]
			except:
				varset = FreeCAD.ActiveDocument.addObject('App::VarSet','magicGlueVarSet')
			
			# create property in VarSet
			if not hasattr(varset, pname):
				varset.addProperty("App::PropertyFloat", pname, pgroup, "", 0)
			
			# set property value in VarSet
			setattr(varset, pname, pvalue)
			
			# set target objects to Varset
			# self.gGPTO is array with targes objects only
			# the self.gGPSO is [ obj, sub ]
			obs = self.gGPTO
			obs.append(self.gGPSO[0])
			
			for o in obs:
			
				if iType == "X":
					
					opx = float(o.Placement.Base.x)
					offset = abs(opx - sX)
					
					expr = "<<" + varset.Name + ">>" + "." + pname
					
					if opx > sX:
						expr += " + " + str(offset)
					else:
						expr += " - " + str(offset)
					
					o.setExpression('.Placement.Base.x', expr)
				
				if iType == "Y":
					
					opy = float(o.Placement.Base.y)
					offset = abs(opy - sY)
					
					expr = "<<" + varset.Name + ">>" + "." + pname
					
					if opy > sY:
						expr += " + " + str(offset)
					else:
						expr += " - " + str(offset)
					
					o.setExpression('.Placement.Base.y', expr)
					
				if iType == "Z":
					
					opz = float(o.Placement.Base.z)
					offset = abs(opz - sZ)
					
					expr = "<<" + varset.Name + ">>" + "." + pname
					
					if opz > sZ:
						expr += " + " + str(offset)
					else:
						expr += " - " + str(offset)
					
					o.setExpression('.Placement.Base.z', expr)
				
				o.recompute()
				
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def gluePositionX(self):
			if self.oVarSetCB.isChecked():
				self.gluePositionVarSet("X")
			else:
				self.gluePosition("X")

		def gluePositionY(self):
			if self.oVarSetCB.isChecked():
				self.gluePositionVarSet("Y")
			else:
				self.gluePosition("Y")

		def gluePositionZ(self):
			if self.oVarSetCB.isChecked():
				self.gluePositionVarSet("Z")
			else:
				self.gluePosition("Z")

		# ############################################################################
		# actions - glue sizes
		# ############################################################################
		
		# ############################################################################
		def setGSAll(self):
			
			try:
			
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				obs = FreeCADGui.Selection.getSelection()[1:]
				
				if sub.ShapeType != "Edge":
					raise
				
				self.gGSSO = [ obj, sub ]
				
				self.gGSTO = []
				for i in range(1, len(obs)+1):
					o = FreeCADGui.Selection.getSelection()[i]
					e = FreeCADGui.Selection.getSelectionEx()[i].SubObjects[0]
					self.gGSTO.append([ o, e ])

				index = MagicPanels.getEdgeIndex(self.gGSSO[0], self.gGSSO[1])
				info1 = self.gGSSO[0].Label + ", Edge" + str(index)
				
				if len(self.gGSTO) > 1:
					info2 = "Multi, "+str(self.gGSTO[0][0].Label)
				else:
					info2 = str(self.gGSTO[0][0].Label)
				
				self.gs1L.setText(info1)
				self.gs2L.setText(info2)
				FreeCADGui.Selection.clearSelection()

			except:
			
				self.gs1L.setText(self.gNoGSSO)
				self.gs2L.setText(self.gNoGSTO)
		
		# ############################################################################
		def setGSSO(self):
			
			try:
			
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

				if sub.ShapeType != "Edge":
					raise
				
				self.gGSSO = [ obj, sub ]
				
				index = MagicPanels.getEdgeIndex(self.gGSSO[0], self.gGSSO[1])
				info1 = self.gGSSO[0].Label + ", Edge" + str(index)
				
				self.gs1L.setText(info1)
				FreeCADGui.Selection.clearSelection()
				
			except:
			
				self.gs1L.setText(self.gNoGSSO)

		# ############################################################################
		def setGSTO(self):
			
			try:

				obs = FreeCADGui.Selection.getSelection()
				
				self.gGSTO = []
				for i in range(0, len(obs)):
					o = FreeCADGui.Selection.getSelection()[i]
					e = FreeCADGui.Selection.getSelectionEx()[i].SubObjects[0]
					self.gGSTO.append([ o, e ])

				if len(self.gGSTO) > 1:
					info2 = "Multi, "+str(self.gGSTO[0][0].Label)
				else:
					info2 = str(self.gGSTO[0][0].Label)
				
				self.gs2L.setText(info2)
				FreeCADGui.Selection.clearSelection()
			
			except:
			
				self.gs2L.setText(self.gNoGSTO)

		# ############################################################################
		def glueSize(self):
			
			if self.oVarSetCB.isChecked():
				self.glueSizeVarSet()
			else:
				self.glueSizeDirect()
				
		# ############################################################################
		def glueSizeDirect(self):
			
			eS = self.gGSSO[1]
			eSSize = float(eS.Length)
			
			eSObjName = str(self.gGSSO[0].Name)
			eSArrIndex = MagicPanels.getEdgeIndex(self.gGSSO[0], self.gGSSO[1]) - 1
			
			obs = self.gGSTO

			for arr in obs:
				
				o = arr[0]
				eT = arr[1]
				eTSize = float(eT.Length)
				name = MagicPanels.getSizeByEdge(o, eT)
				offset = abs(eTSize - eSSize)
				
				exprValue = "<<" + eSObjName + ">>"
				exprValue += ".Shape.Edges[" + str(eSArrIndex) + "].Length"
				if eSSize < eTSize:
					exprValue += " + " + str(offset)
				else:
					exprValue += " - " + str(offset)
				
				if o.isDerivedFrom("Part::Box"):
					o.setExpression(str(name), exprValue)
				
				elif (
					o.isDerivedFrom("PartDesign::Pad") or 
					o.isDerivedFrom("PartDesign::Thickness") or 
					o.isDerivedFrom("PartDesign::Chamfer")
					):
					
					# search in objects properties
					if o.isDerivedFrom("PartDesign::Pad"):
						if MagicPanels.equal(eTSize, float(o.Length.Value)):
							o.setExpression("Length", str(exprValue))
							continue

					if o.isDerivedFrom("PartDesign::Thickness"):
						if MagicPanels.equal(eTSize, float(o.Value.Value)):
							o.setExpression("Value", str(exprValue))
							continue
						
					if o.isDerivedFrom("PartDesign::Chamfer"):
						if MagicPanels.equal(eTSize, float(o.Size.Value)):
							o.setExpression("Size", str(exprValue))
							continue
						
					# if not found search in Constraints
					for sketch in o.OutListRecursive:
						if sketch.isDerivedFrom("Sketcher::SketchObject"):
							for i in range(0, len(sketch.Constraints)):
								
								c = sketch.Constraints[i]
								if MagicPanels.equal(eTSize, c.Value):
									
									exprName = ".Constraints[" + str(i) + "]"
									sketch.setExpression(str(exprName), str(exprValue))

				else:
				
					FreeCAD.Console.PrintMessage("\n")
					FreeCAD.Console.PrintMessage("Object "+str(o.Label)+" skipped. Not supported type.")

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def glueSizeVarSet(self):
			
			eS = self.gGSSO[1]
			eSSize = float(eS.Length)
			
			eSObjName = str(self.gGSSO[0].Name)
			eSIndex = MagicPanels.getEdgeIndex(self.gGSSO[0], self.gGSSO[1])
			
			# create VarSet property to be added
			pgroup = translate('magicGlue', 'Glue size')
			pname = str(self.gGSSO[0].Name) + "_" + "Edge" + str(eSIndex)
			pvalue = eSSize
			
			# create VarSet by Label to allow rename file and keep multi files
			try:
				varset = FreeCAD.ActiveDocument.getObjectsByLabel('magicGlueVarSet')[0]
			except:
				varset = FreeCAD.ActiveDocument.addObject('App::VarSet','magicGlueVarSet')
			
			# create property in VarSet
			if not hasattr(varset, pname):
				varset.addProperty("App::PropertyFloat", pname, pgroup, "", 0)
				
			# set property value in VarSet
			setattr(varset, pname, pvalue)
			
			# for size both the source self.gGSSO and target self.gGSTO is [ obj, edge ]
			obs = self.gGSTO
			obs.append(self.gGSSO)

			for arr in obs:
				
				o = arr[0]
				eT = arr[1]
				eTSize = float(eT.Length)
				name = MagicPanels.getSizeByEdge(o, eT)
				offset = abs(eTSize - eSSize)
				
				exprValue = "<<" + varset.Name + ">>" + "." + pname
				if eSSize < eTSize:
					exprValue += " + " + str(offset)
				else:
					exprValue += " - " + str(offset)
				
				if o.isDerivedFrom("Part::Box"):
					o.setExpression(str(name), exprValue)
				
				elif (
					o.isDerivedFrom("PartDesign::Pad") or 
					o.isDerivedFrom("PartDesign::Thickness") or 
					o.isDerivedFrom("PartDesign::Chamfer")
					):
					
					# search in objects properties
					if o.isDerivedFrom("PartDesign::Pad"):
						if MagicPanels.equal(eTSize, float(o.Length.Value)):
							o.setExpression("Length", str(exprValue))
							continue

					if o.isDerivedFrom("PartDesign::Thickness"):
						if MagicPanels.equal(eTSize, float(o.Value.Value)):
							o.setExpression("Value", str(exprValue))
							continue
						
					if o.isDerivedFrom("PartDesign::Chamfer"):
						if MagicPanels.equal(eTSize, float(o.Size.Value)):
							o.setExpression("Size", str(exprValue))
							continue
						
					# if not found search in Constraints
					for sketch in o.OutListRecursive:
						if sketch.isDerivedFrom("Sketcher::SketchObject"):
							for i in range(0, len(sketch.Constraints)):
								
								c = sketch.Constraints[i]
								if MagicPanels.equal(eTSize, c.Value):
									
									exprName = ".Constraints[" + str(i) + "]"
									sketch.setExpression(str(exprName), str(exprValue))

				else:
				
					FreeCAD.Console.PrintMessage("\n")
					FreeCAD.Console.PrintMessage("Object "+str(o.Label)+" skipped. Not supported type.")
				
				o.recompute()
				
			# recompute
			FreeCAD.ActiveDocument.recompute()
			
		# ############################################################################
		# actions - clean glue
		# ############################################################################

		# ############################################################################
		def setGCO(self):
			
			try:
				
				obs = FreeCADGui.Selection.getSelection()
				FreeCADGui.Selection.clearSelection()
				
				self.gGCO = obs

				if len(self.gGCO) > 1:
					info = "Multi, "+str(self.gGCO[0].Label)
				else:
					info = str(self.gGCO[0].Label)
				
				self.gc1L.setText(info)
			
			except:
			
				self.gc1L.setText(self.gNoGCO)
			
		# ############################################################################
		def glueCleanPosition(self):
			
			for c in self.gGCO:
				
				o = MagicPanels.getObjectToMove(c)
				
				o.setExpression('.Placement.Base.x', None)
				o.setExpression('.Placement.Base.y', None)
				o.setExpression('.Placement.Base.z', None)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def glueCleanSize(self):
			
			for o in self.gGCO:
				
				if o.isDerivedFrom("Part::Box"):

					try:
						o.setExpression('Length', None)
						o.setExpression('Width', None)
						o.setExpression('Height', None)
					
						o.setExpression('.Length', None)
						o.setExpression('.Width', None)
						o.setExpression('.Height', None)
					
					except:
						skip = 1
				
				elif (
						o.isDerivedFrom("PartDesign::Pad") or 
						o.isDerivedFrom("PartDesign::Thickness") or 
						o.isDerivedFrom("PartDesign::Chamfer")
						):
						
					if o.isDerivedFrom("PartDesign::Pad"):
						try:
							o.setExpression("Length", None)
						except:
							try:
								o.setExpression(".Length", None)
							except:
								skip = 1

					if o.isDerivedFrom("PartDesign::Thickness"):
						try:
							o.setExpression("Value", None)
						except:
							try:
								o.setExpression(".Value", None)
							except:
								skip = 1
						
					if o.isDerivedFrom("PartDesign::Chamfer"):
						try:
							o.setExpression("Size", None)
						except:
							try:
								o.setExpression(".Size", None)
							except:
								skip = 1
						
					for sketch in o.OutListRecursive:
						if sketch.isDerivedFrom("Sketcher::SketchObject"):
							for i in range(0, len(sketch.Constraints)):
								
								try:
									exprName = ".Constraints[" + str(i) + "]"
									sketch.setExpression(str(exprName), None)
								except:
									try:
										c = sketch.Constraints[i]
										exprName = ".Constraints." + str(c.Name)
										sketch.setExpression(str(exprName), None)
									except:
										skip = 1
				else:
				
					FreeCAD.Console.PrintMessage("\n")
					FreeCAD.Console.PrintMessage("Object "+str(o.Label)+" skipped. Not supported type.")

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		# Cross functions
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
				skip = 1
			
		def setCornerP(self):

			try:
				s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s+1)
				self.gCornerCross = s+1
			except:
				skip = 1
		
		def setCenterOn(self):
			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
				self.gAxisCross = True
			except:
				skip = 1
			
		def setCenterOff(self):

			try:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(False)
				self.gAxisCross = False
			except:
				skip = 1
	
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:

		if not form.kccscb.isChecked():

			if form.gAxisCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setAxisCross(form.gAxisCrossOrig)
				
			if form.gCornerCrossSupport == True:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(form.gCornerCrossOrig)

		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################

