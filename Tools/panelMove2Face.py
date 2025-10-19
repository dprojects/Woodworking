import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selectedObjects = FreeCADGui.Selection.getSelection()
	allObjects = FreeCAD.ActiveDocument.Objects

	if len(selectedObjects) < 2:
		raise

	targetObj = selectedObjects[0]
	targetFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
	targetPlane = MagicPanels.getFacePlane(targetFace)
	
	centerFace = targetFace.CenterOfMass
	centerObj = targetObj.Shape.CenterOfMass
	[ centerFace, centerObj ] = MagicPanels.getVerticesPosition([ centerFace, centerObj ], targetObj, "vector")

	objects = selectedObjects[1:]

	for o in objects:
		
		toMove = MagicPanels.getObjectToMove(o)
		[ X, Y, Z ] = MagicPanels.getPosition(toMove, "global")
		[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)
		
		if targetPlane == "XY":
			
			d = abs(Z - centerFace.z)
			
			if Z < centerFace.z:
				Z = Z + d
			else:
				Z = Z - d

			if centerFace.z < centerObj.z:
				Z = Z - sizeZ

		if targetPlane == "XZ":

			d = abs(Y - centerFace.y)

			if Y < centerFace.y:
				Y = Y + d
			else:
				Y = Y - d

			if centerFace.y < centerObj.y:
				Y = Y - sizeY

		if targetPlane == "YZ":

			d = abs(X - centerFace.x)

			if X < centerFace.x:
				X = X + d
			else:
				X = X - d

			if centerFace.x < centerObj.x:
				X = X - sizeX

		MagicPanels.setPosition(toMove, X, Y, Z, "global")
	
	# clean selection and recompute
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""

	info += translate('panelMove2Face', '<b>Please first select face, next select objects to move.</b><br><br><b>Note:</b> This tool allows to move panels to the selected face position. You can select more objects holding left CTRL key. This tool allows you to avoid thickness step problem, if you want to move panel to the other edge but the way is not a multiple of the panel thickness. Also you can move shelves to the back or to the sides of the furniture. For rotated containers use panelMove2Anchor.')
	
	MagicPanels.showInfo("panelMove2Face", info)

