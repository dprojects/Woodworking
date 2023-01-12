import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	sv1 = ""
	sv2 = ""
	obj1Ref = ""
	obj2Ref = ""
	objects = []

	selection = FreeCADGui.Selection.getSelection()

	try:
		sv1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		sv2 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[1]
		obj1Ref = FreeCADGui.Selection.getSelection()[0]
		obj2Ref = FreeCADGui.Selection.getSelection()[0]
		
		objects = FreeCADGui.Selection.getSelection()
		objects.pop(0)
		
	except:
		skip = 1
		
	if sv1 == "" or sv2 == "" or len(objects) < 1:
		
		try:
			sv1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
			sv2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
			obj1Ref = FreeCADGui.Selection.getSelection()[0]
			obj2Ref = FreeCADGui.Selection.getSelection()[1]
		
			objects = FreeCADGui.Selection.getSelection()
			objects.pop(0)
			objects.pop(0)
			
		except:
			skip = 1

	if sv1 == "" or sv2 == "" or len(objects) < 1:
		raise

	for o in objects:
		
		oRef = MagicPanels.getReference(o)
		
		if hasattr(sv1, "Curve"):
			if sv1.Curve.isDerivedFrom("Part::GeomCircle"):
				v1 = sv1.Curve.Location
		else:
			v1 = FreeCAD.Vector(sv1.X, sv1.Y, sv1.Z)

		if hasattr(sv2, "Curve"):
			if sv2.Curve.isDerivedFrom("Part::GeomCircle"):
				v2 = sv2.Curve.Location
		else:
			v2 = FreeCAD.Vector(sv2.X, sv2.Y, sv2.Z)

		[ v1 ] = MagicPanels.getVerticesOffset([ v1 ], obj1Ref, "vector")
		[ v2 ] = MagicPanels.getVerticesOffset([ v2 ], obj2Ref, "vector")
		
		[ cx, cy, cz ] = MagicPanels.getObjectCenter(oRef)
		c = FreeCAD.Vector(cx, cy, cz)
		[ c ] = MagicPanels.getVerticesOffset([ c ], oRef, "vector")
		
		X, Y, Z = v1[0], v1[1], v1[2]
		plane = MagicPanels.getVerticesPlane(v1, v2)
		
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

		toMove = MagicPanels.getObjectToMove(oRef)
		MagicPanels.setContainerPlacement(toMove, X, Y, Z, 0, edgeCenter)
		FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""

	info += translate('panelMove2Center', '<b>To move object to the center please select single edge of two holes and objects to move. Or select two vertices and objects to move. </b><br><br><b>Note:</b> This tool allows to move object to the center of two holes or two vertices. The edge holes or vertices should lie on one of the coordinate axes XYZ. The object can be Cylinder, Cone (dril bit), Cube (panel), Pad or LinkGroup with as many objects you want. If you want to move Pad, select Body. If you want to move many Pads, select Body or pack all Part into LinkGroup and select LinkGroup to move. Make sure you do not have Sketch position set. This tool use .Shape.CenterOfMass but if it is not available for object like it is for LinkGroup the center will be calculated from vertices. You can move to the center many objects at once. Hold left CTRL key during selection. ')
	
	MagicPanels.showInfo("panelMove2Center", info)
