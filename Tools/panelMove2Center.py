import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	selection = FreeCADGui.Selection.getSelection()

	# at least 2 subs at the same object should be selected 
	# and object to center = 2 objects
	if len(selection) < 2:
		raise

	startIndex = 0
	sub1 = "" 
	sub2 = ""
	sv1 = ""
	sv2 = ""
	obj1Ref = ""
	obj2Ref = ""
	objects = []

	# try selection at single object first
	try:
		sub1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		sub2 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[1]
		
		obj1Ref = FreeCADGui.Selection.getSelection()[0]
		obj2Ref = FreeCADGui.Selection.getSelection()[0]
		
		objects = FreeCADGui.Selection.getSelection()
		startIndex = 1
	except:
		skip = 1

	# if selection is at two different objects
	if sub1 == "" or sub2 == "" or len(objects) < 1:
		try:
			sub1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
			sub2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
			
			obj1Ref = FreeCADGui.Selection.getSelection()[0]
			obj2Ref = FreeCADGui.Selection.getSelection()[1]
		
			objects = FreeCADGui.Selection.getSelection()
			startIndex = 2
		except:
			skip = 1
	
	# set the center reference points
	try:
		if sub1.ShapeType == "Edge" and sub2.ShapeType == "Edge":
			
			sv1 = sub1.CenterOfMass
			if hasattr(sub1, "Curve"):
				if sub1.Curve.isDerivedFrom("Part::GeomCircle"):
					sv1 = sub1.Curve.Location
			
			sv2 = sub2.CenterOfMass
			if hasattr(sub2, "Curve"):
				if sub2.Curve.isDerivedFrom("Part::GeomCircle"):
					sv2 = sub2.Curve.Location

		if sub1.ShapeType == "Face" and sub2.ShapeType == "Face":
			sv1 = sub1.CenterOfMass
			sv2 = sub2.CenterOfMass

		if sub1.ShapeType == "Vertex" and sub2.ShapeType == "Vertex":
			sv1 = FreeCAD.Vector(sub1.X, sub1.Y, sub1.Z)
			sv2 = FreeCAD.Vector(sub2.X, sub2.Y, sub2.Z)
	except:
		skip = 1

	# show error info if there are no center reference points
	if sv1 == "" or sv2 == "":
		raise

	# start center objects
	for i in range(startIndex, len(objects)):
		
		o = objects[i]
		v1 = sv1
		v2 = sv2
		
		[ cx, cy, cz ] = MagicPanels.getObjectCenter(o)
		c = FreeCAD.Vector(cx, cy, cz)
		
		[ globalV1 ] = MagicPanels.getVerticesPosition([ v1 ], obj1Ref)
		[ globalV2 ] = MagicPanels.getVerticesPosition([ v2 ], obj2Ref)

		plane = MagicPanels.getVerticesPlane(globalV1, globalV2)
		
		# I don't like this way but this is working solution to get the plane correctly and calculate position
		# I need to re-think better solution someday with general plane recognition for rotatated containers
		verticesType = ""
		if plane == "":
			plane = MagicPanels.getVerticesPlane(v1, v2)
			verticesType = "local"
		else:
			v1, v2 = globalV1, globalV2
			[ c ] = MagicPanels.getVerticesPosition([ c ], o)
			verticesType = "global"
		
		X, Y, Z = v1[0], v1[1], v1[2]
		
		if plane == "XY":

			edgeCenter = FreeCAD.Vector(v1[0], v1[1], c[2])

			# along Z
			offset = MagicPanels.getVertexAxisCross(v1[2], v2[2]) / 2
			

			if v1[2] < v2[2]:
				Z = Z + offset
			else:
				Z = Z - offset

		if plane == "XZ":

			edgeCenter = FreeCAD.Vector(v1[0], c[1], v1[2])

			# along Y
			offset = MagicPanels.getVertexAxisCross(v1[1], v2[1]) / 2
			
			if v1[1] < v2[1]:
				Y = Y + offset
			else:
				Y = Y - offset
			
		if plane == "YZ":

			edgeCenter = FreeCAD.Vector(c[0], v1[1], v1[2])

			# along X
			offset = MagicPanels.getVertexAxisCross(v1[0], v2[0]) / 2
					
			if v1[0] < v2[0]:
				X = X + offset
			else:
				X = X - offset

		toMove = MagicPanels.getObjectToMove(o)
		
		if verticesType == "global":
			MagicPanels.setContainerPlacement(toMove, X, Y, Z, 0, edgeCenter)
		
		if verticesType == "local":
			MagicPanels.setPlacement(toMove, X, Y, Z, toMove.Placement.Rotation, edgeCenter)
		
		FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""

	info += translate('panelMove2Center', 'This tool allows you to center objects. Possible selection methods') + ": "
	info += "<ul>"
	info += "<li>" + translate('panelMove2Center', '<b>Edge</b> + <b>Edge</b> + <b>Objects</b>') + "</li>"
	info += "<li>" + translate('panelMove2Center', '<b>Face</b> + <b>Face</b> + <b>Objects</b>') + "</li>"
	info += "<li>" + translate('panelMove2Center', '<b>Vertex</b> + <b>Vertex</b> + <b>Objects</b>') + "</li>"
	info += "<li>" + translate('panelMove2Center', '<b>Hole edge</b> + <b>Hole edge</b> + <b>Objects</b>') + "</li>"
	info += "</ul>"
	info += translate('panelMove2Center', 'Tip') + ":"
	info += "<ul>"
	info += "<li>" + translate('panelMove2Center', '<b>Edge, Face, Vertex or Hole edge</b> - can be at the same object or at two different objects but both should lie on one of the coordinate axes XYZ. Because if there would be for example offset at X and Y, this tool would not be able to recognize to which direction center objects.') + "</li>"
	info += "<li>" + translate('panelMove2Center', '<b>Objects</b> - The object can be Cylinder, Cone (dril bit), Cube (panel), Pad or LinkGroup with as many objects you want. If you want to move Pad, select Body. If you want to move many Pads, select Body or pack all Part into LinkGroup and select LinkGroup to move. Make sure you do not have Sketch position set. This tool use .Shape.CenterOfMass but if it is not available for object like it is for LinkGroup the center will be calculated from vertices. You can move to the center many objects at once. Hold left CTRL key during selection. ') + "</li>"
	info += "</ul>"
	
	MagicPanels.showInfo("panelMove2Center", info)

