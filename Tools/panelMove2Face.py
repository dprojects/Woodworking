import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selectedObjects = FreeCADGui.Selection.getSelection()
	allObjects = FreeCAD.ActiveDocument.Objects

	if len(selectedObjects) < 2:
		raise

	base = selectedObjects[0]
	baseFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
	basePlane = MagicPanels.getFacePlane(baseFace)
	[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(baseFace)
	[ v1, v2, v3, v4 ] = MagicPanels.getVerticesPosition([ v1, v2, v3, v4 ], base, "array")
	
	bx = v1[0]
	by = v1[1]
	bz = v1[2]

	fcx = float(baseFace.CenterOfMass.x)
	fcy = float(baseFace.CenterOfMass.y)
	fcz = float(baseFace.CenterOfMass.z)
	
	bcx = float(base.Shape.CenterOfMass.x)
	bcy = float(base.Shape.CenterOfMass.y)
	bcz = float(base.Shape.CenterOfMass.z)

	objects = selectedObjects[1:]

	for o in objects:
		
		oRef = MagicPanels.getReference(o)
		toMove = MagicPanels.getObjectToMove(oRef)

		[ X, Y, Z, R ] = MagicPanels.getContainerPlacement(toMove, "clean")
		[ refX, refY, refZ, refR ] = MagicPanels.getContainerPlacement(oRef, "offset")
		[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)
		
		if basePlane == "XY":
			
			d = MagicPanels.getVertexAxisCross(refZ, bz)
			
			if refZ < bz:
				Z = Z + d
			else:
				Z = Z - d

			if fcz < bcz:
				Z = Z - sizeZ

		if basePlane == "XZ":

			d = MagicPanels.getVertexAxisCross(refY, by)

			if refY < by:
				Y = Y + d
			else:
				Y = Y - d

			if fcy < bcy:
				Y = Y - sizeY

		if basePlane == "YZ":

			d = MagicPanels.getVertexAxisCross(refX, bx)

			if refX < bx:
				X = X + d
			else:
				X = X - d

			if fcx < bcx:
				X = X - sizeX

		MagicPanels.setContainerPlacement(toMove, X, Y, Z, 0, "clean")
	
	# clean selection and recompute
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""

	info += translate('panelMove2Face', '<b>Please first select face, next select objects to move.</b><br><br><b>Note:</b> This tool allows to move panels to the selected face position. You can select more objects holding left CTRL key. This tool allows you to avoid thickness step problem, if you want to move panel to the other edge but the way is not a multiple of the panel thickness. Also you can move shelves to the back or to the sides of the furniture. For rotated containers use panelMove2Anchor.')
	
	MagicPanels.showInfo("panelMove2Face", info)

