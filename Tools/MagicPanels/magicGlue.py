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
		
		gCrossCorner = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
		gCrossCenter = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()
		gCrossCornerOrig = FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize()
		gCrossCenterOrig = FreeCADGui.ActiveDocument.ActiveView.hasAxisCross()
		
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
			toolSW = 250
			toolSH = 400
			
			rside = toolSW - 20
			
			# active screen size (FreeCAD main window)
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			gPW = int( gSW - toolSW )
			gPH = 10

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(gPW, gPH, toolSW, toolSH)
			self.setWindowTitle(translate('magicGlue', 'magicGlue'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# GUI for common selection part (visible by default)
			# ############################################################################

			row = 10
			
			# not write here, copy text from getMenuIndex1 to avoid typo
			self.sModeList = (
				translate('magicGlue', 'Glue position'), 
				translate('magicGlue', 'Glue size'), 
				translate('magicGlue', 'Clean glue')
				)
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(0) # default
			self.sMode.activated[str].connect(self.setModeType)
			self.sMode.setFixedWidth(rside)
			self.sMode.move(10, row)
			
			row += 50

			# ############################################################################
			# settigns for custom GUI
			# ############################################################################
			
			rows = row
			rowc = row
			
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
			self.gp1B.setFixedHeight(20)
			self.gp1B.move(10, row)
			
			self.gp1L = QtGui.QLabel(self.gNoGPSO, self)
			self.gp1L.setFixedWidth(rside - 80)
			self.gp1L.move(80, row+3)

			row += 30
			
			self.gp2B = QtGui.QPushButton(translate('magicGlue', 'set'), self)
			self.gp2B.clicked.connect(self.setGPTO)
			self.gp2B.setFixedWidth(60)
			self.gp2B.setFixedHeight(20)
			self.gp2B.move(10, row)
			
			self.gp2L = QtGui.QLabel(self.gNoGPTO, self)
			self.gp2L.setFixedWidth(rside - 80)
			self.gp2L.move(80, row+3)
			
			row += 30
			
			self.gp3B = QtGui.QPushButton(translate('magicGlue', 'refresh all selection'), self)
			self.gp3B.clicked.connect(self.setGPAll)
			self.gp3B.setFixedWidth(rside)
			self.gp3B.setFixedHeight(40)
			self.gp3B.move(10, row)
			
			row += 80
			
			# label
			self.gp4L = QtGui.QLabel(self.gInfoPositionX, self)
			self.gp4L.move(10, row+3)

			# button
			self.gp4B = QtGui.QPushButton(translate('magicGlue', 'add glue'), self)
			self.gp4B.clicked.connect(self.gluePositionX)
			self.gp4B.setFixedWidth(2 * btsize + 10)
			self.gp4B.move(cbt1, row)
			self.gp4B.setAutoRepeat(False)

			row += 30

			# label
			self.gp5L = QtGui.QLabel(self.gInfoPositionY, self)
			self.gp5L.move(10, row+3)

			# button
			self.gp5B = QtGui.QPushButton(translate('magicGlue', 'add glue'), self)
			self.gp5B.clicked.connect(self.gluePositionY)
			self.gp5B.setFixedWidth(2 * btsize + 10)
			self.gp5B.move(cbt1, row)
			self.gp5B.setAutoRepeat(False)

			row += 30
			
			# label
			self.gp6L = QtGui.QLabel(self.gInfoPositionZ, self)
			self.gp6L.move(10, row+3)

			# button
			self.gp6B = QtGui.QPushButton(translate('magicGlue', 'add glue'), self)
			self.gp6B.clicked.connect(self.gluePositionZ)
			self.gp6B.setFixedWidth(2 * btsize + 10)
			self.gp6B.move(cbt1, row)
			self.gp6B.setAutoRepeat(False)

			# ############################################################################
			# GUI for glue size (hidden by default)
			# ############################################################################
			
			self.gs1B = QtGui.QPushButton(translate('magicGlue', 'set'), self)
			self.gs1B.clicked.connect(self.setGSSO)
			self.gs1B.setFixedWidth(60)
			self.gs1B.setFixedHeight(20)
			self.gs1B.move(10, rows)
			
			self.gs1L = QtGui.QLabel(self.gNoGSSO, self)
			self.gs1L.setFixedWidth(rside - 80)
			self.gs1L.move(80, rows+3)

			rows += 30
			
			self.gs2B = QtGui.QPushButton(translate('magicGlue', 'set'), self)
			self.gs2B.clicked.connect(self.setGSTO)
			self.gs2B.setFixedWidth(60)
			self.gs2B.setFixedHeight(20)
			self.gs2B.move(10, rows)
			
			self.gs2L = QtGui.QLabel(self.gNoGSTO, self)
			self.gs2L.setFixedWidth(rside - 80)
			self.gs2L.move(80, rows+3)
			
			rows += 30
			
			self.gs3B = QtGui.QPushButton(translate('magicGlue', 'refresh all selection'), self)
			self.gs3B.clicked.connect(self.setGSAll)
			self.gs3B.setFixedWidth(rside)
			self.gs3B.setFixedHeight(40)
			self.gs3B.move(10, rows)
			
			rows += 120
		
			# button
			self.gs4B = QtGui.QPushButton(translate('magicGlue', 'add glue size'), self)
			self.gs4B.clicked.connect(self.glueSize)
			self.gs4B.setFixedWidth(rside)
			self.gs4B.setFixedHeight(40)
			self.gs4B.move(10, rows)
			self.gs4B.setAutoRepeat(False)

			# hide by default
			self.gs1L.hide()
			self.gs1B.hide()
			self.gs2L.hide()
			self.gs2B.hide()
			self.gs3B.hide()
			self.gs4B.hide()

			# ############################################################################
			# GUI for glue clean (hidden by default)
			# ############################################################################
			
			self.gc1L = QtGui.QLabel(self.gNoGCO, self)
			self.gc1L.setFixedWidth(rside)
			self.gc1L.move(10, rowc+3)
			
			rowc += 30
			
			self.gc2B = QtGui.QPushButton(translate('magicGlue', 'refresh all selection'), self)
			self.gc2B.clicked.connect(self.setGCO)
			self.gc2B.setFixedWidth(rside)
			self.gc2B.setFixedHeight(40)
			self.gc2B.move(10, rowc)
			
			rowc += 90
		
			# button
			self.gc3B = QtGui.QPushButton(translate('magicGlue', 'clean glue position'), self)
			self.gc3B.clicked.connect(self.glueCleanPosition)
			self.gc3B.setFixedWidth(rside)
			self.gc3B.setFixedHeight(40)
			self.gc3B.move(10, rowc)
			self.gc3B.setAutoRepeat(False)
			
			rowc += 60
			
			# button
			self.gc4B = QtGui.QPushButton(translate('magicGlue', 'clean glue size'), self)
			self.gc4B.clicked.connect(self.glueCleanSize)
			self.gc4B.setFixedWidth(rside)
			self.gc4B.setFixedHeight(40)
			self.gc4B.move(10, rowc)
			self.gc4B.setAutoRepeat(False)
			
			# hide by default
			self.gc1L.hide()
			self.gc2B.hide()
			self.gc3B.hide()
			self.gc4B.hide()

			# ############################################################################
			# GUI for common foot (visible by default)
			# ############################################################################
			
			row = toolSH - 90
			
			# label
			self.o0L = QtGui.QLabel(translate('magicMove', 'Corner cross:'), self)
			self.o0L.move(10, row+3)

			# button
			self.o0B1 = QtGui.QPushButton("-", self)
			self.o0B1.clicked.connect(self.setCornerM)
			self.o0B1.setFixedWidth(btsize)
			self.o0B1.move(cbt1, row)
			self.o0B1.setAutoRepeat(True)
			
			# button
			self.o0B2 = QtGui.QPushButton("+", self)
			self.o0B2.clicked.connect(self.setCornerP)
			self.o0B2.setFixedWidth(btsize)
			self.o0B2.move(cbt2, row)
			self.o0B2.setAutoRepeat(True)

			row += 30
			
			# label
			self.o0L = QtGui.QLabel(translate('magicMove', 'Center cross:'), self)
			self.o0L.move(10, row+3)

			# button
			self.o0B1 = QtGui.QPushButton(translate('magicMove', 'on'), self)
			self.o0B1.clicked.connect(self.setCenterOn)
			self.o0B1.setFixedWidth(btsize)
			self.o0B1.move(cbt1, row)
			self.o0B1.setAutoRepeat(True)
			
			# button
			self.o0B2 = QtGui.QPushButton(translate('magicMove', 'off'), self)
			self.o0B2.clicked.connect(self.setCenterOff)
			self.o0B2.setFixedWidth(btsize)
			self.o0B2.move(cbt2, row)
			self.o0B2.setAutoRepeat(True)

			row += 25
			
			self.kccscb = QtGui.QCheckBox(translate('magicDowels', ' - keep custom cross settings'), self)
			self.kccscb.setCheckState(QtCore.Qt.Unchecked)
			self.kccscb.move(10, row+3)
		
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()
			
			# init
			FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(40)
			self.setGPAll()
		
		# ############################################################################
		# actions - menu selections
		# ############################################################################

		# ############################################################################	
		def setModeType(self, selectedText):
			
			selectedIndex = getMenuIndex1[selectedText]
			self.gModeType = selectedIndex

			# first hide all
			
			self.gp1L.hide()
			self.gp1B.hide()
			self.gp2L.hide()
			self.gp2B.hide()
			self.gp3B.hide()
			self.gp4L.hide()
			self.gp4B.hide()
			self.gp5L.hide()
			self.gp5B.hide()
			self.gp6L.hide()
			self.gp6B.hide()
			
			self.gs1L.hide()
			self.gs1B.hide()
			self.gs2L.hide()
			self.gs2B.hide()
			self.gs3B.hide()
			self.gs4B.hide()
			
			self.gc1L.hide()
			self.gc2B.hide()
			self.gc3B.hide()
			self.gc4B.hide()

			# position
			if selectedIndex == 0:
				
				self.gp1L.show()
				self.gp1B.show()
				self.gp2L.show()
				self.gp2B.show()
				self.gp3B.show()
				self.gp4L.show()
				self.gp4B.show()
				self.gp5L.show()
				self.gp5B.show()
				self.gp6L.show()
				self.gp6B.show()
				
				self.gp4L.setText(self.gInfoPositionX)
				self.gp5L.setText(self.gInfoPositionY)
				self.gp6L.setText(self.gInfoPositionZ)

			# size
			if selectedIndex == 1:
				
				self.gs1L.show()
				self.gs1B.show()
				self.gs2L.show()
				self.gs2B.show()
				self.gs3B.show()
				self.gs4B.show()
				
			# clean
			if selectedIndex == 2:
				
				self.gc1L.show()
				self.gc2B.show()
				self.gc3B.show()
				self.gc4B.show()

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
		def gluePositionX(self):
			self.gluePosition("X")

		def gluePositionY(self):
			self.gluePosition("Y")

		def gluePositionZ(self):
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

			s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
			if s - 1 < 0:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(0)
			else:
				FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s-1)
				self.gCrossCorner = s-1
		
		# ############################################################################
		def setCornerP(self):
			
			s = int(FreeCADGui.ActiveDocument.ActiveView.getCornerCrossSize())
			FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(s+1)
			self.gCrossCorner = s+1
		
		# ############################################################################
		def setCenterOn(self):
			
			FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
			self.gCrossCenter = True
		
		# ############################################################################
		def setCenterOff(self):
			
			FreeCADGui.ActiveDocument.ActiveView.setAxisCross(False)
			self.gCrossCenter = False
		
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:

		if not form.kccscb.isChecked():
			FreeCADGui.ActiveDocument.ActiveView.setAxisCross(form.gCrossCenterOrig)
			FreeCADGui.ActiveDocument.ActiveView.setCornerCrossSize(form.gCrossCornerOrig)

		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################

