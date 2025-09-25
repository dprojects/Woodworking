import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate

# ###################################################################################################################
# global variables
# ###################################################################################################################

gGUI = "" # do not reset this ;-)
gP1 = ""
gP2 = ""
gObj1 = ""
gObj2 = ""
gSub1 = ""
gSub2 = ""
gPreselectionMode = True
gMeasures = []
gMeasureType = 8

# add new items only at the end and change self.sModeList
getMenuIndex1 = {
	translate('magicMeasure', 'PartDesign - system'): 0, 
	translate('magicMeasure', 'Draft - green'): 1,
	translate('magicMeasure', 'Draft - yellow'): 2,
	translate('magicMeasure', 'Draft - black'): 3,
	translate('magicMeasure', 'Draft - red'): 4, 
	translate('magicMeasure', 'Draft - handwrite green'): 5,
	translate('magicMeasure', 'Draft - handwrite yellow'): 6,
	translate('magicMeasure', 'Draft - handwrite black'): 7,
	translate('magicMeasure', 'Draft - handwrite red'): 8
}

# ###################################################################################################################
# global functions
# ###################################################################################################################

# ###################################################################################################################
def resetGlobals():

	global gP1, gP2, gObj1, gObj2, gSub1, gSub2, gMeasures

	gP1 = ""
	gP2 = ""
	gObj1 = ""
	gObj2 = ""
	gSub1 = ""
	gSub2 = ""
	gMeasures = []

# ###################################################################################################################
def removeMeasures():
	
	if len(gMeasures) != 0:
		for m in gMeasures:
			try:
				if str(m.Name) == "":
					raise
				else:
					FreeCAD.ActiveDocument.removeObject(str(m.Name))
			except:
				skip = 1

# ###################################################################################################################
def clearInfoScreens():
	
	try:
		if gGUI != "":
			gGUI.moi.setPlainText("")
			gGUI.mos.setPlainText("")
	except:
		skip = 1

# ###################################################################################################################
#
# Observer class - main code logic
#
# ###################################################################################################################


class SelectionObserver:
	
	# ############################################################################
	# preselect - preselection mode, use locals here
	# ############################################################################

	# ############################################################################
	def edgePreselect(self, doc, obj, sub):
		
		removeMeasures()
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
			
			gGUI.moi.setText(str(label) + ", " + str(sub))
			gGUI.moi.setText(str(obj) + ", " + str(sub))
			gGUI.mos.setPlainText("Size:" + " " + MagicPanels.unit2gui(size))
			
			if gPreselectionMode == True:
				m = MagicPanels.showMeasure(p1, p2, o, o, sub, sub, gMeasureType, "no")
				gMeasures.append(m)
			
		# hole edge
		if edge.Curve.isDerivedFrom("Part::GeomCircle"):
		
			p1 = FreeCAD.Vector(edge.Curve.Location.x, edge.Curve.Location.y, edge.Curve.Location.z)
			p2 = FreeCAD.Vector(edge.SubShapes[1].X, edge.SubShapes[1].Y, edge.SubShapes[1].Z)
			[ p1, p2 ] = MagicPanels.getVerticesPosition([ p1, p2 ], o, "vector")
			
			# show measure
			size = round(p1.distanceToPoint(p2), MagicPanels.gRoundPrecision)
			
			gGUI.moi.setText(str(label) + ", " + str(sub))
			gGUI.moi.setText(str(obj) + ", " + str(sub))
			gGUI.mos.setPlainText("Size:" + " " + MagicPanels.unit2gui(size))
			
			if gPreselectionMode == True:
				m = MagicPanels.showMeasure(p1, p2, o, o, sub, sub, gMeasureType, "no")
				gMeasures.append(m)
		
		# ellipse edge
		if edge.Curve.isDerivedFrom("Part::GeomEllipse"):
			
			import math
			
			# 1st measure
			p1 = FreeCAD.Vector(edge.Curve.Location.x, edge.Curve.Location.y, edge.Curve.Location.z)

			v = edge.Curve.value(0)
			p2 = FreeCAD.Vector(v[0], v[1], v[2])
			[ p1, p2 ] = MagicPanels.getVerticesPosition([ p1, p2 ], o, "vector")
			
			s1 = round(p1.distanceToPoint(p2), MagicPanels.gRoundPrecision)
			
			if gPreselectionMode == True:
				m = MagicPanels.showMeasure(p1, p2, o, o, sub, sub, gMeasureType, "no")
				gMeasures.append(m)
	
			# 2nd measure
			p1 = FreeCAD.Vector(edge.Curve.Location.x, edge.Curve.Location.y, edge.Curve.Location.z)
			
			v = edge.Curve.value(math.pi / 2)
			p2 = FreeCAD.Vector(v[0], v[1], v[2])
			[ p1, p2 ] = MagicPanels.getVerticesPosition([ p1, p2 ], o, "vector")
			
			s2 = round(p1.distanceToPoint(p2), MagicPanels.gRoundPrecision)
			
			if gPreselectionMode == True:
				m = MagicPanels.showMeasure(p1, p2, o, o, sub, sub, gMeasureType, "no")
				gMeasures.append(m)
				
			# screen update
			
			size = MagicPanels.unit2gui(s1) + ", " + MagicPanels.unit2gui(s2)
	
			gGUI.moi.setText(str(label) + ", " + str(sub))
			gGUI.moi.setText(str(obj) + ", " + str(sub))
			gGUI.mos.setPlainText("Size:" + " " + str(size))

	# ############################################################################
	def facePreselect(self, doc, obj, sub):
		
		removeMeasures()
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
		preselection = dict()
		
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
			
			size += MagicPanels.unit2gui(s)
			
			if gPreselectionMode == True:
				if not s in preselection.keys():
					m = MagicPanels.showMeasure(p1, p2, o, o, sub, sub, gMeasureType, "no")
					gMeasures.append(m)
					preselection[s] = 1
		
		gGUI.moi.setText(str(label) + ", " + str(sub))
		gGUI.moi.setText(str(obj) + ", " + str(sub))
		gGUI.mos.setPlainText("Size:" + " " + str(size))
	
	# ############################################################################
	# select - selection mode, use globals here, to store first selection
	# ############################################################################

	# ############################################################################
	def edgeSelect(self, doc, obj, sub, pos):
		
		global gP1, gP2, gObj1, gObj2, gSub1, gSub2

		removeMeasures()
		clearInfoScreens()
		
		o = FreeCAD.ActiveDocument.getObject(obj)
		label = obj
		
		try:
			label = o.Label
		except:
			skip = 1
		
		index = int(sub.replace("Edge",""))-1
		edge = o.Shape.Edges[index]
		
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
		
				gObj2 = MagicPanels.getObjectToMove(o)
				gSub2 = sub
				
			# get both vertices from edge, and draw measure for entire edge
			else:
				[ v1, v2 ] = MagicPanels.getEdgeVertices(edge)
				[ v1, v2 ] = MagicPanels.getVerticesPosition([ v1, v2 ], o, "array")
				gP1 = FreeCAD.Vector(v1)
				gP2 = FreeCAD.Vector(v2)
				
				gObj1 = MagicPanels.getObjectToMove(o)
				gSub1 = sub
				gObj2 = MagicPanels.getObjectToMove(o)
				gSub2 = sub

		# hole ellipse edge
		if edge.Curve.isDerivedFrom("Part::GeomCircle") or edge.Curve.isDerivedFrom("Part::GeomEllipse"):
		
			skip = 0
			
			if gP1 == "":
				gP1 = FreeCAD.Vector(edge.Curve.Location.x, edge.Curve.Location.y, edge.Curve.Location.z)
				[ gP1 ] = MagicPanels.getVerticesPosition([ gP1 ], o, "vector")
				
				gObj1 = MagicPanels.getObjectToMove(o)
				gSub1 = sub
			else:
				gP2 = FreeCAD.Vector(edge.Curve.Location.x, edge.Curve.Location.y, edge.Curve.Location.z)
				[ gP2 ] = MagicPanels.getVerticesPosition([ gP2 ], o, "vector")
				
				gObj2 = MagicPanels.getObjectToMove(o)
				gSub2 = sub

		# skip if there is no data to show measurement
		if skip == 1 or gP1 == "" or gP2 == "":
			return
		
		size = round(gP1.distanceToPoint(gP2), MagicPanels.gRoundPrecision)
		
		gGUI.moi.setText(str(label) + ", " + str(sub))
		gGUI.moi.setText(str(obj) + ", " + str(sub))
		gGUI.mos.setPlainText("Size:" + " " + MagicPanels.unit2gui(size))
		
		m = MagicPanels.showMeasure(gP1, gP2, gObj1, gObj2, gSub1, gSub2, gMeasureType, "yes")
		resetGlobals()

	# ############################################################################
	def faceSelect(self, doc, obj, sub, pos):
		
		global gP1, gP2, gObj1, gObj2, gSub1, gSub2
		
		removeMeasures()
		clearInfoScreens()
		
		skip = 0
		
		o = FreeCAD.ActiveDocument.getObject(obj)
		label = obj
		
		try:
			label = o.Label
		except:
			skip = 1
		
		index = int(sub.replace("Face",""))-1
		face = o.getSubObject(sub)
		
		# if already selected vertex, get second vertex from face
		if gP1 != "":
			
			v1 = [ face.CenterOfMass.x, face.CenterOfMass.y, face.CenterOfMass.z ]
			[ v1 ] = MagicPanels.getVerticesPosition([ v1 ], o, "array")
			axis = MagicPanels.getFacePlane(face)
			
			gObj2 = MagicPanels.getObjectToMove(o)
			gSub2 = sub

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
		
		gGUI.moi.setText(str(label) + ", " + str(sub))
		gGUI.moi.setText(str(obj) + ", " + str(sub))
		gGUI.mos.setPlainText("Size:" + " " + MagicPanels.unit2gui(size))
		
		m = MagicPanels.showMeasure(gP1, gP2, gObj1, gObj2, gSub1, gSub2, gMeasureType, "yes")
		resetGlobals()
		
	# ############################################################################
	def vertexSelect(self, doc, obj, sub, pos):
		
		global gP1, gP2, gObj1, gObj2, gSub1, gSub2

		removeMeasures()
		clearInfoScreens()
	
		o = FreeCAD.ActiveDocument.getObject(obj)
		label = obj
		
		try:
			label = o.Label
		except:
			skip = 1
		
		if gP1 == "":
			gP1 = FreeCAD.Vector(pos[0], pos[1], pos[2])
			gObj1 = MagicPanels.getObjectToMove(o)
			gSub1 = sub
		else:
			gP2 = FreeCAD.Vector(pos[0], pos[1], pos[2])
			gObj2 = MagicPanels.getObjectToMove(o)
			gSub2 = sub
		
		if gP1 != "" and gP2 != "":
			m = MagicPanels.showMeasure(gP1, gP2, gObj1, gObj2, gSub1, gSub2, gMeasureType, "yes")
			resetGlobals()
		
	# ############################################################################
	# Controllers 
	#
	# Note: Not code here, because this will be one big jumbo, "register" only 
	# new objects types here, if needed and implement the logic in dedicated 
	# function. This will be easier to extend and control globals. 
	# ############################################################################
	
	def addSelection(self, doc, obj, sub, pos):
		
		if gPreselectionMode == True:
			resetGlobals()
			return
		
		if sub.startswith("Edge"):
			self.edgeSelect(doc, obj, sub, pos)
		
		if sub.startswith("Face"):
			self.faceSelect(doc, obj, sub, pos)
			
		if sub.startswith("Vertex"):
			self.vertexSelect(doc, obj, sub, pos)
			
	def setPreselection(self, doc, obj, sub):
		
		# debug for new types
		#FreeCAD.Console.PrintMessage("\n\n")
		#FreeCAD.Console.PrintMessage(obj)
		#FreeCAD.Console.PrintMessage("\n")
		#FreeCAD.Console.PrintMessage(sub)
		
		if sub.startswith("Edge"):
			self.edgePreselect(doc, obj, sub)
		
		if sub.startswith("Face"):
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
		
		# preselection ON - info
		gObserverOff = '<div>'
		gObserverOff += translate('magicMeasure', 'The observer is currently <b>disabled</b>, please click observer <b>start</b> button to start measuring.') + '<br><br>'
		gObserverOff += translate('magicMeasure', 'This tool works in two modes:')
		gObserverOff += '<ul>'
		gObserverOff += '<li><b>' + translate('magicMeasure', 'Preselection mode: ') + '</b>'
		gObserverOff += translate('magicMeasure', 'this mode allows you to measure objects quickly only by moving mouse cursor over the object.') + '</li>'
		gObserverOff += '<li><b>' + translate('magicMeasure', 'Selection mode: ') + '</b>'
		gObserverOff += translate('magicMeasure', 'this mode allows you to measure objects by selecting vertex, face or holes.') + '</li>'
		gObserverOff += '</ul>'
		gObserverOff += '</div>'
		
		# preselection ON - status
		gPsOnS = translate('magicMeasure', 'Preselection mode is: ') + '<b>' + translate('magicMeasure', 'ON') + '</b>'

		# preselection ON - info
		gPsOnI = '<div>'
		gPsOnI += '<ul>'
		gPsOnI += '<li>'
		gPsOnI += translate('magicMeasure', 'In this mode you can measure: ')
		gPsOnI += '<b>' + translate('magicMeasure', 'edge') + ', </b>'
		gPsOnI += '<b>' + translate('magicMeasure', 'face') + ', </b>'
		gPsOnI += '<b>' + translate('magicMeasure', 'hole diameter') + ', </b>'
		gPsOnI += '<b>' + translate('magicMeasure', 'and hole depth') + '. </b>'
		gPsOnI += '</li>'
		gPsOnI += '<li>' + translate('magicMeasure', 'To see measurements, in this preselection mode, you have to move cursor over the object.') + '</li>' 
		gPsOnI += '<li>' + translate('magicMeasure', 'If you click left mouse button the current visible measurements will be stored.') + '</li>'
		gPsOnI += '<li>' + translate('magicMeasure', 'For more detailed measurements turn off preselection mode.') + '</li>'
		gPsOnI += '</ul>'
		gPsOnI += '<br>'
		gPsOnI += '</div>'
		
		# preselection OFF - status
		gPsOffS = translate('magicMeasure', 'Preselection mode is: ') + '<b>' + translate('magicMeasure', 'OFF') + '</b>'
		
		# preselection OFF - info
		gPsOffI = '<div>'
		gPsOffI += translate('magicMeasure', 'In this mode you have possible selections:')
		gPsOffI += '<ul>'
		gPsOffI += '<li>' + translate('magicMeasure', '<b>Edge</b>: to measure edge size,') + '</li>'
		gPsOffI += '<li>' + translate('magicMeasure', '<b>Vertex -> Face</b> or <b>Vertex -> Edge</b> or <b>Vertex -> Hole</b> or <b>Vertex -> Vertex</b>: to measure distance from vertex to the other selected object,') + '</li>'
		gPsOffI += '<li>' + translate('magicMeasure', '<b>Hole -> Hole</b> or <b>Hole -> Edge</b> or <b>Hole -> Face</b> or <b>Hole -> Vertex</b>: to measure distance from hole to the other selected object.') + '</li>'
		gPsOffI += '</ul>'
		gPsOffI += '</div>'
		
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
			toolSW = 320
			toolSH = 650
			
			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setWindowTitle(translate('magicMeasure', 'magicMeasure'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
			self.setFixedWidth(toolSW)
			self.setFixedHeight(toolSH)
			
			# ############################################################################
			# measure type selection
			# ############################################################################
			
			# label
			self.sModeL = QtGui.QLabel(translate('magicMeasure', 'Drawing type:'), self)
			
			# not write here, copy text from getMenuIndex1 to avoid typo
			self.sModeList = (
				translate('magicMeasure', 'PartDesign - system'),
				translate('magicMeasure', 'Draft - green'),
				translate('magicMeasure', 'Draft - yellow'),
				translate('magicMeasure', 'Draft - black'),
				translate('magicMeasure', 'Draft - red'),
				translate('magicMeasure', 'Draft - handwrite green'),
				translate('magicMeasure', 'Draft - handwrite yellow'),
				translate('magicMeasure', 'Draft - handwrite black'),
				translate('magicMeasure', 'Draft - handwrite red') # no comma
			)
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(gMeasureType) # default
			self.sMode.textActivated[str].connect(self.setModeType)
			self.sMode.setMinimumWidth(100)
			
			# ############################################################################
			# measure observer
			# ############################################################################
			
			# measurement observer active status
			self.moas = QtGui.QLabel(translate('magicMeasure', 'Measurement observer:'), self)
			
			# measurement observer active button
			self.moaBON = QtGui.QPushButton(translate('magicMeasure', 'START'), self)
			self.moaBON.clicked.connect(self.measureStart)
			self.moaBON.setFixedWidth(80)
			self.moaBON.setFixedHeight(40)
			
			# measurement observer active button
			self.moaBPAUSE = QtGui.QPushButton(translate('magicMeasure', 'PAUSE'), self)
			self.moaBPAUSE.clicked.connect(self.measureFinish)
			self.moaBPAUSE.setFixedWidth(80)
			self.moaBPAUSE.setFixedHeight(40)
			
			# ############################################################################
			# preselection
			# ############################################################################
			
			# preselection mode label
			self.psmL = QtGui.QLabel(translate('magicMeasure', 'Preselection mode:'), self)
			
			# preselection mode button
			self.psmB1 = QtGui.QPushButton(translate('magicMeasure', 'ON'), self)
			self.psmB1.clicked.connect(self.setPSMOn)
			self.psmB1.setFixedWidth(80)
			self.psmB1.setFixedHeight(40)
			
			# preselection mode button
			self.psmB2 = QtGui.QPushButton(translate('magicMeasure', 'OFF'), self)
			self.psmB2.clicked.connect(self.setPSMOff)
			self.psmB2.setFixedWidth(80)
			self.psmB2.setFixedHeight(40)
			
			# ############################################################################
			# resize vertex
			# ############################################################################
			
			# measurement observer active status
			self.vsL = QtGui.QLabel(translate('magicMeasure', 'Vertices size:'), self)
			
			# measurement observer active button
			self.vsBM = QtGui.QPushButton('- 5', self)
			self.vsBM.clicked.connect(self.vertexSizeM)
			self.vsBM.setFixedHeight(40)
			self.vsBM.setAutoRepeat(True)
			
			# measurement observer active button
			self.vsBP = QtGui.QPushButton('+ 5', self)
			self.vsBP.clicked.connect(self.vertexSizeP)
			self.vsBP.setFixedHeight(40)
			self.vsBP.setAutoRepeat(True)
			
			# ############################################################################
			# selection description info
			# ############################################################################
			
			# preselection mode active status
			self.psmas = QtGui.QLabel("", self)
			
			# mode description
			self.sdi = QtGui.QLabel(self.gObserverOff, self)
			self.sdi.setFixedHeight(230)
			self.sdi.setWordWrap(True)
			self.sdi.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			# ############################################################################
			# # measure data
			# ############################################################################

			# measure object info
			self.moi = QtGui.QLabel("", self)
			self.moi.setWordWrap(True)

			# measure object size
			self.mos = QtGui.QTextEdit(self)
			self.mos.setFixedHeight(60)
			self.mos.setPlainText("")

			# ############################################################################
			# build GUI layout
			# ############################################################################
			
			# create structure
			self.body0 = QtGui.QGridLayout()
			self.body0.addWidget(self.sModeL, 0, 0)
			self.body0.addWidget(self.sMode, 0, 1)
			self.body1 = QtGui.QGridLayout()
			self.body1.addWidget(self.moas, 0, 0)
			self.body1.addWidget(self.moaBON, 0, 1)
			self.body1.addWidget(self.moaBPAUSE, 0, 1)
			self.body1.addWidget(self.psmL, 1, 0)
			self.body1.addWidget(self.psmB1, 1, 1)
			self.body1.addWidget(self.psmB2, 1, 1)
			self.body12 = QtGui.QHBoxLayout()
			self.body12.addWidget(self.vsL)
			self.body12.addWidget(self.vsBM)
			self.body12.addWidget(self.vsBP)
			self.lay1 = QtGui.QVBoxLayout()
			self.lay1.addLayout(self.body0)
			self.lay1.addLayout(self.body1)
			self.lay1.addLayout(self.body12)
			self.groupBody1 = QtGui.QGroupBox(None, self)
			self.groupBody1.setLayout(self.lay1)
			
			self.body2 = QtGui.QVBoxLayout()
			self.body2.addWidget(self.psmas)
			self.body2.addWidget(self.sdi)
			self.groupBody2 = QtGui.QGroupBox(None, self)
			self.groupBody2.setLayout(self.body2)
			
			self.body3 = QtGui.QVBoxLayout()
			self.body3.addWidget(self.moi)
			self.body3.addWidget(self.mos)
			self.groupBody3 = QtGui.QGroupBox(None, self)
			self.groupBody3.setLayout(self.body3)
			
			# set layout to main window
			self.layout = QtGui.QVBoxLayout()
			self.layout.addWidget(self.groupBody1)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody2)
			self.layout.addStretch()
			self.layout.addWidget(self.groupBody3)
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
			pw = int( FreeCADGui.getMainWindow().width() - sw ) - 5
			ph = int( FreeCADGui.getMainWindow().height() - sh ) + 30
			self.setGeometry(pw, ph, sw, sh)

			# init
			self.setInit()

		# ############################################################################
		# actions - functions for actions
		# ############################################################################

		# ############################################################################
		def setInit(self):

			try:
				resetGlobals()
				
				# support for FreeCAD 1.0+
				if MagicPanels.gKernelVersion >= 1.0:
					import Draft
					Viewer = FreeCADGui.ActiveDocument.ActiveView.getViewer()
					UserState = Viewer.getSceneGraph().highlightMode.getValue()
				
				# support for FreeCAD 0.21.2
				else:
					Viewer = FreeCADGui.ActiveDocument.ActiveView.getViewer()
					UserState = Viewer.getSceneGraph().highlightMode.getValue()
				
				# FreeCAD GUI preselection off
				if UserState == 2:
					self.measureStart()
					self.setPSMOff()
					
					self.psmB1.show()
					self.psmB2.hide()
					
					self.psmas.setText(self.gPsOffS)
					self.sdi.setText(self.gPsOffI)
				
				# FreeCAD GUI preselection on
				else:
					self.measureStart()
					
					self.psmB1.hide()
					self.psmB2.show()
					
					self.psmas.setText(self.gPsOnS)
					self.sdi.setText(self.gPsOnI)
					
				self.moaBON.hide()
				self.moaBPAUSE.show()

			except:

				self.moaBON.show()
				self.moaBPAUSE.hide()
				return -1

		# ############################################################################
		def setModeType(self, selectedText):
			global gMeasureType
			selectedIndex = getMenuIndex1[selectedText]
			gMeasureType = selectedIndex

		# ############################################################################
		def setPSMOn(self):
			
			global gPreselectionMode
			
			gPreselectionMode = True
			
			self.psmB1.hide()
			self.psmB2.show()
			
			self.psmas.setText(self.gPsOnS)
			self.sdi.setText(self.gPsOnI)

		def setPSMOff(self):
			
			global gPreselectionMode
			
			gPreselectionMode = False
			removeMeasures()
			
			self.psmB1.show()
			self.psmB2.hide()
			
			self.psmas.setText(self.gPsOffS)
			self.sdi.setText(self.gPsOffI)

		# ############################################################################
		def measureStart(self):
			
			global gGUI
			
			try:
				if self.gObserver == "":
					gGUI = self
					self.gObserver = SelectionObserver()
					FreeCADGui.Selection.addObserver(self.gObserver)
					
					self.moaBON.hide()
					self.moaBPAUSE.show()
					
					if gPreselectionMode == True:
						self.setPSMOn()
					else:
						self.setPSMOff()
			except:
				
				self.moaBON.show()
				self.moaBPAUSE.hide()
				
		def measureFinish(self):
			
			try:
				FreeCADGui.Selection.removeObserver(self.gObserver)
				self.gObserver = ""

				self.moaBON.show()
				self.moaBPAUSE.hide()
				
				self.psmas.setText("")
				self.sdi.setText(self.gObserverOff)

			except:
				
				self.moaBON.hide()
				self.moaBPAUSE.show()
		
		# ############################################################################
		def vertexSizeM(self):
			
			objects = FreeCAD.ActiveDocument.Objects

			for o in objects:
				try:
					o.ViewObject.PointSize = o.ViewObject.PointSize - 5
				except:
					skip = 1

		def vertexSizeP(self):
			
			objects = FreeCAD.ActiveDocument.Objects
			
			for o in objects:
				try:
					o.ViewObject.PointSize = o.ViewObject.PointSize + 5
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
		except:
			skip = 1
		
		removeMeasures()
		
		pass


# ###################################################################################################################
#
# Main run
#
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
