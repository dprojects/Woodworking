import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selectedObjects = FreeCADGui.Selection.getSelection()
	allObjects = FreeCAD.ActiveDocument.Objects

	if len(selectedObjects) < 2:
		raise
		
	base = selectedObjects[0]
	objects = selectedObjects[1:]
	baseRef = MagicPanels.getReference(base)
	[ baseX, baseY, baseZ, baseR ] = MagicPanels.getContainerPlacement(baseRef, "clean")
	[[ baseX, baseY, baseZ ]] = MagicPanels.getVerticesPosition([[ baseX, baseY, baseZ ]], baseRef, "array")

	# sub-object selection
	sx, sy, sz = "", "", ""
	try:
		sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

		if sub.ShapeType == "Edge":

			if sub.Curve.isDerivedFrom("Part::GeomLine"):
				sx = sub.CenterOfMass.x
				sy = sub.CenterOfMass.y
				sz = sub.CenterOfMass.z

			elif sub.Curve.isDerivedFrom("Part::GeomCircle"):
				sx = sub.Curve.Center.x
				sy = sub.Curve.Center.y
				sz = sub.Curve.Center.z

		if sub.ShapeType == "Face":
			sx = sub.CenterOfMass.x
			sy = sub.CenterOfMass.y
			sz = sub.CenterOfMass.z

		if sub.ShapeType == "Vertex":
			sx = sub.X
			sy = sub.Y
			sz = sub.Z

	except:
		skip = 1

	# objects to move
	for o in objects:

		if o.isDerivedFrom("Sketcher::SketchObject"):
			
			[ oX, oY, oZ, oR ] = MagicPanels.getSketchPlacement(o, "global")
			
			try:
				plane = o.Support[0][0].Label
				if plane.startswith("XY") or plane.startswith("XZ") or plane.startswith("YZ"):
					t = "attach"
				else:
					raise
			except:
				t = "global"
			
			if sx != "" and sy != "" and sz != "":
				MagicPanels.setSketchPlacement(o, sx, sy, sz, oR, t)
			else:
				MagicPanels.setSketchPlacement(o, x, y, z, oR, t)
				
		elif o.isDerivedFrom("Part::Cylinder"):
			
			[ oX, oY, oZ, oR ] = MagicPanels.getPlacement(o)

			if sx != "" and sy != "" and sz != "":
				MagicPanels.setPlacement(o, sx, sy, sz, oR)
			else:
				MagicPanels.setPlacement(o, x, y, z, oR)

		else:
			
			objRef = MagicPanels.getReference(o)
			objMove = MagicPanels.getObjectToMove(objRef)
			[ gX, gY, gZ, gR ] = MagicPanels.getContainerPlacement(objRef, "offset")
			[ X, Y, Z, R ] = MagicPanels.getContainerPlacement(objMove, "clean")

			dX = MagicPanels.getVertexAxisCross(gX, baseX)
			dY = MagicPanels.getVertexAxisCross(gY, baseY)
			dZ = MagicPanels.getVertexAxisCross(gZ, baseZ)
			
			if gX < baseX:
				X = X + dX
			else:
				X = X - dX

			if gY < baseY:
				Y = Y + dY
			else:
				Y = Y - dY

			if gZ < baseZ:
				Z = Z + dZ
			else:
				Z = Z - dZ

			MagicPanels.setContainerPlacement(objMove, X, Y, Z, 0, "clean")
			FreeCAD.ActiveDocument.recompute()

	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""

	info += translate('mapPosition', '<b>First select object to copy position, next select objects to move. </b><br><br><b>Note:</b> This tool allows to move objects to the same position as first selected object. The objects will be moved without rotation. Only the placement will change. If the first selected object is rotated the objects may not match exactly the starting point. This tool is very useful if you want to redesign furniture and you want to create new element. Using this tool you can quickly move the new element to the same position of old element and remove the old element. To select more objects hold left CTRL key during selection. With this tool you can also move Cylinders and Sketches more precisely. If first you select Edge or Face the Cylinders or Sketches will be moved to the CenterOfMass. If first you select Vertex the Cylinders or Sketches will be moved to the selected Vertex position.')
	
	MagicPanels.showInfo("mapPosition", info)
