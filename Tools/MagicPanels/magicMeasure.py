import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate


# ###################################################################################################################
#
# Globals are good as pizza ;-)
#
# ###################################################################################################################


gGUI = "" # do not reset this ;-)
gP1 = ""
gP2 = ""
gRef = ""
gHoverMode = True
gHoverMeasure = []

def resetGlobals():

	global gP1, gP2, gRef, gHoverMeasure

	gP1 = ""
	gP2 = ""
	gRef = ""
	gHoverMeasure = []

def removeHoverMeasure():
	
	if len(gHoverMeasure) != 0:
		for h in gHoverMeasure:
			try:
				FreeCAD.ActiveDocument.removeObject(str(h.Name))
			except:
				skip = 1

def clearInfoScreens():
	
	try:
		if gGUI != "":
			gGUI.hoverIS.setPlainText("")
			gGUI.sizeIS.setPlainText("")
	except:
		skip = 1


# ###################################################################################################################
#
# Observer class - main code logic
#
# ###################################################################################################################


class SelectionObserver:
	
	# ############################################################################
	# preselect - hover mode, use locals here
	# ############################################################################

	# ############################################################################
	def edgePreselect(self, doc, obj, sub):
		
		removeHoverMeasure()
		clearInfoScreens()
		
		o = FreeCAD.ActiveDocument.getObject(obj)
		label = obj
		
		try:
			label = o.Label
		except:
			skip = 1
		
		index = int(sub.replace("Edge",""))
		edge = o.Shape.Edges[index-1]
		
		# normal edge
		if edge.Curve.isDerivedFrom("Part::GeomLine"):
			
			[ v1, v2 ] = MagicPanels.getEdgeVertices(edge)
			[ v1, v2 ] = MagicPanels.getVerticesPosition([ v1, v2 ], o, "array")

			p1 = FreeCAD.Vector(v1)
			p2 = FreeCAD.Vector(v2)
			
			# show measure
			size = round(p1.distanceToPoint(p2), MagicPanels.gRoundPrecision)
			
			gGUI.hoverIS.setText(str(label) + ", " + str(sub))
			gGUI.hoverIS.setText(str(obj) + ", " + str(sub))
			gGUI.sizeIS.setPlainText("Size:" + " " + str(size))
			
			if gHoverMode == True:
				m = MagicPanels.showMeasure(p1, p2, str(o.Label) + ", " + str(sub))
				gHoverMeasure.append(m)
			
		# hole edge
		if edge.Curve.isDerivedFrom("Part::GeomCircle"):
		
			p1 = FreeCAD.Vector(edge.Curve.Location.x, edge.Curve.Location.y, edge.Curve.Location.z)
			p2 = FreeCAD.Vector(edge.SubShapes[1].X, edge.SubShapes[1].Y, edge.SubShapes[1].Z)
			[ p1, p2 ] = MagicPanels.getVerticesPosition([ p1, p2 ], o, "vector")
			
			# show measure
			size = round(p1.distanceToPoint(p2), MagicPanels.gRoundPrecision)
			
			gGUI.hoverIS.setText(str(label) + ", " + str(sub))
			gGUI.hoverIS.setText(str(obj) + ", " + str(sub))
			gGUI.sizeIS.setPlainText("Size:" + " " + str(size))
			
			if gHoverMode == True:
				m = MagicPanels.showMeasure(p1, p2, str(o.Label) + ", " + str(sub))
				gHoverMeasure.append(m)
		
		# ellipse edge
		if edge.Curve.isDerivedFrom("Part::GeomEllipse"):
			
			import math
			
			# 1st measure
			p1 = FreeCAD.Vector(edge.Curve.Location.x, edge.Curve.Location.y, edge.Curve.Location.z)

			v = edge.Curve.value(0)
			p2 = FreeCAD.Vector(v[0], v[1], v[2])
			[ p1, p2 ] = MagicPanels.getVerticesPosition([ p1, p2 ], o, "vector")
			
			s1 = round(p1.distanceToPoint(p2), MagicPanels.gRoundPrecision)
			
			if gHoverMode == True:
				m = MagicPanels.showMeasure(p1, p2, str(o.Label) + ", " + str(sub))
				gHoverMeasure.append(m)
	
			# 2nd measure
			p1 = FreeCAD.Vector(edge.Curve.Location.x, edge.Curve.Location.y, edge.Curve.Location.z)
			
			v = edge.Curve.value(math.pi / 2)
			p2 = FreeCAD.Vector(v[0], v[1], v[2])
			[ p1, p2 ] = MagicPanels.getVerticesPosition([ p1, p2 ], o, "vector")
			
			s2 = round(p1.distanceToPoint(p2), MagicPanels.gRoundPrecision)
			
			if gHoverMode == True:
				m = MagicPanels.showMeasure(p1, p2, str(o.Label) + ", " + str(sub))
				gHoverMeasure.append(m)
				
			# screen update
			
			size = str(s1) + ", " + str(s2)
	
			gGUI.hoverIS.setText(str(label) + ", " + str(sub))
			gGUI.hoverIS.setText(str(obj) + ", " + str(sub))
			gGUI.sizeIS.setPlainText("Size:" + " " + str(size))

	# ############################################################################
	def facePreselect(self, doc, obj, sub):
		
		removeHoverMeasure()
		clearInfoScreens()
		
		o = FreeCAD.ActiveDocument.getObject(obj)
		label = obj
		
		try:
			label = o.Label
		except:
			skip = 1
		
		index = int(sub.replace("Face",""))
		face = o.Shape.Faces[index-1]
		
		edges = face.Edges
		
		size = ""
		hover = dict()
		
		i = 0
		for e in edges:
			
			if not e.Curve.isDerivedFrom("Part::GeomLine"):
				continue
			
			i = i + 1
			
			[ v1, v2 ] = MagicPanels.getEdgeVertices(e)
			[ v1, v2 ] = MagicPanels.getVerticesPosition([ v1, v2 ], o, "array")
			p1 = FreeCAD.Vector(v1)
			p2 = FreeCAD.Vector(v2)
			val = round(p1.distanceToPoint(p2), MagicPanels.gRoundPrecision)
			s = str(val)
			
			if i != 1:
				size += " x "
			
			size += s
			
			if gHoverMode == True:
				if not s in hover.keys():
					m = MagicPanels.showMeasure(p1, p2, str(o.Label) + ", " + str(sub))
					gHoverMeasure.append(m)
					hover[s] = 1
		
		gGUI.hoverIS.setText(str(label) + ", " + str(sub))
		gGUI.hoverIS.setText(str(obj) + ", " + str(sub))
		gGUI.sizeIS.setPlainText("Size:" + " " + str(size))
	
	# ############################################################################
	# select - selection mode, use globals here, to store first selection
	# ############################################################################

	# ############################################################################
	def edgeSelect(self, doc, obj, sub, pos):
		
		global gP1, gP2, gRef
		
		removeHoverMeasure()
		clearInfoScreens()
		
		o = FreeCAD.ActiveDocument.getObject(obj)
		label = obj
		
		try:
			label = o.Label
		except:
			skip = 1
		
		index = int(sub.replace("Edge",""))
		edge = o.Shape.Edges[index-1]
		
		skip = 1
		
		# normal edge
		if edge.Curve.isDerivedFrom("Part::GeomLine"):
			
			skip = 0

			# if already selected vertex, get from edge only one vertex
			if gP1 != "":
				
				[ v1, v2 ] = MagicPanels.getEdgeVertices(edge)
				[ v1, v2 ] = MagicPanels.getVerticesPosition([ v1, v2 ], o, "array")
				axis = MagicPanels.getEdgePlane(o, edge)
				
				if axis == "X":
					gP2 = FreeCAD.Vector(gP1[0], v1[1], v1[2])
				if axis == "Y":
					gP2 = FreeCAD.Vector(v1[0], gP1[1], v1[2])
				if axis == "Z":
					gP2 = FreeCAD.Vector(v1[0], v1[1], gP1[2])
		
			# get both vertices from edge, and draw measure for entire edge
			else:
				[ v1, v2 ] = MagicPanels.getEdgeVertices(edge)
				[ v1, v2 ] = MagicPanels.getVerticesPosition([ v1, v2 ], o, "array")
				gP1 = FreeCAD.Vector(v1)
				gP2 = FreeCAD.Vector(v2)
		
		# hole ellipse edge
		if edge.Curve.isDerivedFrom("Part::GeomCircle") or edge.Curve.isDerivedFrom("Part::GeomEllipse"):
		
			skip = 0
			
			if gP1 == "":
				gP1 = FreeCAD.Vector(edge.Curve.Location.x, edge.Curve.Location.y, edge.Curve.Location.z)
				[ gP1 ] = MagicPanels.getVerticesPosition([ gP1 ], o, "vector")
			else:
				gP2 = FreeCAD.Vector(edge.Curve.Location.x, edge.Curve.Location.y, edge.Curve.Location.z)
				[ gP2 ] = MagicPanels.getVerticesPosition([ gP2 ], o, "vector")
		
		# skip if there is no data to show measurement
		if skip == 1 or gP1 == "" or gP2 == "":
			return
		
		size = round(gP1.distanceToPoint(gP2), MagicPanels.gRoundPrecision)
		
		gGUI.hoverIS.setText(str(label) + ", " + str(sub))
		gGUI.hoverIS.setText(str(obj) + ", " + str(sub))
		gGUI.sizeIS.setPlainText("Size:" + " " + str(size))
		
		m = MagicPanels.showMeasure(gP1, gP2, str(o.Label) + ", " + str(sub))
		resetGlobals()

	# ############################################################################
	def faceSelect(self, doc, obj, sub, pos):
		
		global gP1, gP2, gRef
		
		removeHoverMeasure()
		clearInfoScreens()
		
		skip = 0
		
		o = FreeCAD.ActiveDocument.getObject(obj)
		label = obj
		
		try:
			label = o.Label
		except:
			skip = 1
		
		face = o.getSubObject(sub)
		
		# if already selected vertex, get second vertex from face
		if gP1 != "":
			
			[ v1, v2 ] = MagicPanels.getEdgeVertices(face.Edges[0])
			[ v1, v2 ] = MagicPanels.getVerticesPosition([ v1, v2 ], o, "array")
			axis = MagicPanels.getFacePlane(face)
			
			if axis == "YZ":
				gP2 = FreeCAD.Vector(v1[0], gP1[1], gP1[2])
			if axis == "XZ":
				gP2 = FreeCAD.Vector(gP1[0], v1[1], gP1[2])
			if axis == "XY":
				gP2 = FreeCAD.Vector(gP1[0], gP1[1], v1[2])
	
		# not supported
		else:
			skip = 1
	
		# skip if there is no data to show measurement
		if skip == 1 or gP1 == "" or gP2 == "":
			return
		
		size = round(gP1.distanceToPoint(gP2), MagicPanels.gRoundPrecision)
		
		gGUI.hoverIS.setText(str(label) + ", " + str(sub))
		gGUI.hoverIS.setText(str(obj) + ", " + str(sub))
		gGUI.sizeIS.setPlainText("Size:" + " " + str(size))
		
		m = MagicPanels.showMeasure(gP1, gP2, str(o.Label) + ", " + str(sub))
		resetGlobals()
		
	# ############################################################################
	def vertexSelect(self, doc, obj, sub, pos):
		
		global gP1, gP2, gRef
		
		removeHoverMeasure()
		clearInfoScreens()
	
		o = FreeCAD.ActiveDocument.getObject(obj)
		label = obj
		
		try:
			label = o.Label
		except:
			skip = 1
	
		if gP1 == "":
			gP1 = FreeCAD.Vector(pos[0], pos[1], pos[2])
		else:
			gP2 = FreeCAD.Vector(pos[0], pos[1], pos[2])
		
		if gP1 != "" and gP2 != "":
			
			# you can use gRef to store reference for both vertices
			MagicPanels.showMeasure(gP1, gP2, str(o.Label) + ", " + str(sub))
			resetGlobals()
		
	# ############################################################################
	# Controllers 
	#
	# Note: Not code here, because this will be one big jumbo, "register" only 
	# new objects types here, if needed and implement the logic in dedicated 
	# function. This will be easier to extend and control globals. 
	# ############################################################################
	
	def addSelection(self, doc, obj, sub, pos):
		
		if gHoverMode == True:
			resetGlobals()
			return
		
		if sub.find("Edge") != -1:
			self.edgeSelect(doc, obj, sub, pos)
		
		if sub.find("Face") != -1:
			self.faceSelect(doc, obj, sub, pos)
			
		if sub.find("Vertex") != -1:
			self.vertexSelect(doc, obj, sub, pos)
			
	def setPreselection(self, doc, obj, sub):
		
		# debug for new types
		#FreeCAD.Console.PrintMessage("\n")
		#FreeCAD.Console.PrintMessage(sub)
		
		if sub.find("Edge") != -1:
			self.edgePreselect(doc, obj, sub)
		
		if sub.find("Face") != -1:
			self.facePreselect(doc, obj, sub)


# ###################################################################################################################
#
# Qt Main GUI class
#
# ###################################################################################################################


def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals
		# ############################################################################

		gObserver = ""
		gInfoMeasureON = "Measuring: ON"
		gInfoMeasureOFF = "Measuring: OFF"
		gInfoHoverON = "hover & click to store measurement"
		gInfoHoverOFF = "select to create measurement"
		
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
			toolSH = 250
			
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
			self.setWindowTitle(translate('magicMeasure', 'magicMeasure'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - info screens
			# ############################################################################
			
			info = ""
			info += "                                             "
			info += "                                             "
			info += "                                             "

			row = 10
			
			# mode screen - measure
			self.modeMIS = QtGui.QLabel(info, self)
			self.modeMIS.move(10, row)
			
			row += 20
			
			# mode screen - hover
			self.modeHIS = QtGui.QLabel(info, self)
			self.modeHIS.move(10, row)

			row += 20

			# hover screen - label
			self.hoverIS = QtGui.QLabel(info, self)
			self.hoverIS.move(10, row)

			row += 20

			# hover screen - size
			self.sizeIS = QtGui.QTextEdit(self)
			self.sizeIS.setMinimumSize(toolSW-20, 60)
			self.sizeIS.setMaximumSize(toolSW-20, 60)
			self.sizeIS.move(10, row)
			self.sizeIS.setPlainText("")
			
			# ############################################################################
			# options - modes selection
			# ############################################################################

			row += 80
			
			# button
			self.modeB1 = QtGui.QPushButton(translate('magicMeasure', 'measuring ON'), self)
			self.modeB1.clicked.connect(self.measureStart)
			self.modeB1.setFixedWidth((toolSW/2)-20)
			self.modeB1.setFixedHeight(40)
			self.modeB1.move(10, row)

			# button
			self.modeB2 = QtGui.QPushButton(translate('magicMeasure', 'measuring OFF'), self)
			self.modeB2.clicked.connect(self.measureFinish)
			self.modeB2.setFixedWidth((toolSW/2)-20)
			self.modeB2.setFixedHeight(40)
			self.modeB2.move((toolSW/2)+10, row)

			# ############################################################################
			# options - hover selection
			# ############################################################################

			row += 50
			
			# button
			self.modeHoverB1 = QtGui.QPushButton(translate('magicMeasure', 'hover ON'), self)
			self.modeHoverB1.clicked.connect(self.setHoverOn)
			self.modeHoverB1.setFixedWidth((toolSW/2)-20)
			self.modeHoverB1.setFixedHeight(40)
			self.modeHoverB1.move(10, row)

			# button
			self.modeHoverB2 = QtGui.QPushButton(translate('magicMeasure', 'hover OFF'), self)
			self.modeHoverB2.clicked.connect(self.setHoverOff)
			self.modeHoverB2.setFixedWidth((toolSW/2)-20)
			self.modeHoverB2.setFixedHeight(40)
			self.modeHoverB2.move((toolSW/2)+10, row)


			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()

			# init
			self.setInit()

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def setInit(self):

			try:
				resetGlobals()
				
				self.measureStart()
				self.modeMIS.setText(self.gInfoMeasureON)
				self.modeHIS.setText(self.gInfoHoverON)
				
			except:

				self.modeMIS.setText(self.gInfoMeasureOFF)
				return -1

		# ############################################################################
		def measureStart(self):
			
			global gGUI
			
			try:
				if self.gObserver == "":
					gGUI = self
					self.gObserver = SelectionObserver()
					FreeCADGui.Selection.addObserver(self.gObserver)
					self.modeMIS.setText(self.gInfoMeasureON)
				
			except:
				skip = 1

		def measureFinish(self):
			try:
				FreeCADGui.Selection.removeObserver(self.gObserver)
				self.gObserver = ""
				self.modeMIS.setText(self.gInfoMeasureOFF)
			except:
				skip = 1
		
		# ############################################################################
		def setHoverOn(self):
			
			global gHoverMode
			
			try:
				gHoverMode = True
				self.modeHIS.setText(self.gInfoHoverON)
			except:
				skip = 1

		def setHoverOff(self):
			
			global gHoverMode
			
			try:
				gHoverMode = False
				self.modeHIS.setText(self.gInfoHoverOFF)
				removeHoverMeasure()
				
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
		
		try:
			FreeCADGui.Selection.removeObserver(form.gObserver)
			form.gObserver = ""
			form.modeMIS.setText(self.gInfoMeasureOFF)
		except:
			skip = 1
		
		removeHoverMeasure()
		
		pass


# ###################################################################################################################
#
# Main run
#
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
