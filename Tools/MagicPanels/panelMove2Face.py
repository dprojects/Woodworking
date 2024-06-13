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
	
	objects = selectedObjects[1:]

	for o in objects:
		
		oRef = MagicPanels.getReference(o)
		toMove = MagicPanels.getObjectToMove(oRef)

		[ X, Y, Z, R ] = MagicPanels.getContainerPlacement(toMove, "clean")
		[ gX, gY, gZ, gR ] = MagicPanels.getContainerPlacement(oRef, "offset")
	
		if basePlane == "XY":
			d = MagicPanels.getVertexAxisCross(gZ, v1[2])
			if gZ < v1[2]:
				Z = Z + d
			else:
				Z = Z - d

		if basePlane == "XZ":
			d = MagicPanels.getVertexAxisCross(gY, v1[1])
			if gY < v1[1]:
				Y = Y + d
			else:
				Y = Y - d

		if basePlane == "YZ":
			d = MagicPanels.getVertexAxisCross(gX, v1[0])
			if gX < v1[0]:
				X = X + d
			else:
				X = X - d

		MagicPanels.setContainerPlacement(toMove, X, Y, Z, 0, "clean")
		FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""

	info += translate('panelMove2Face', '<b>First select face, and next object that should be aligned to the face position. </b><br><br><b>Note:</b> This tool allows to align panels or any other objects to face position. You can select objects at objects Tree window holding left CTRL key. This tool allows to avoid thickness step problem, if you want to move panel to the other edge but the way is not a multiple of the panel thickness. For rotated containers use panelMove2Anchor.')
	
	MagicPanels.showInfo("panelMove2Face", info)

