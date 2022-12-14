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
	[ oX, oY, oZ, oR ] = MagicPanels.getContainersOffset(base)

	objects = selectedObjects[1:]

	for o in objects:
		
		obj = MagicPanels.getReference(o)
		
		[ x, y, z, r ] = MagicPanels.getGlobalPlacement(obj)
		
		if basePlane == "XY":
			X = x
			Y = y
			Z = v1[2] + oZ
			R = r
			
		if basePlane == "XZ":
			X = x
			Y = v1[1] + oY
			Z = z
			R = r
		
		if basePlane == "YZ":
			X = v1[0] + oX
			Y = y
			Z = z
			R = r
		
		MagicPanels.setPlacement(obj, X, Y, Z, R)
		FreeCAD.ActiveDocument.recompute()
	
except:
	
	info = ""

	info += translate('panelMove2FaceInfo', '<b>First select face, and next object that should be aligned to the face position. </b><br><br><b>Note:</b> This tool allows to align panels or any other objects to face position. You can select objects at objects Tree window holding left CTRL key. This tool allows to avoid thickness step problem, if you want to move panel to the other edge but the way is not a multiple of the panel thickness.')
	
	MagicPanels.showInfo("panelMove2Face", info)

