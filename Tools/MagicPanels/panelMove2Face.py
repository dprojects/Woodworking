import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()
	
	if len(objects) < 2:
		raise
	
	i = 0
	for o in objects:
		
		i = i + 1
		
		if i == 1:

			gObj = FreeCADGui.Selection.getSelection()[0]
			gFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

			gFPlane = MagicPanels.getFacePlane(gFace)
			[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(gFace)

			continue
		
		obj = MagicPanels.getReference(o)
		
		[ x, y, z, r ] = MagicPanels.getPlacement(obj)
		
		if gFPlane == "XY":
			X = x
			Y = y
			Z = v1[2]
			R = r
			
		if gFPlane == "XZ":
			X = x
			Y = v1[1]
			Z = z
			R = r
		
		if gFPlane == "YZ":
			X = v1[0]
			Y = y
			Z = z
			R = r
		
		MagicPanels.setPlacement(obj, X, Y, Z, R)
		FreeCAD.ActiveDocument.recompute()
		
except:
	
	info = ""

	info += translate('panelMove2FaceInfo', '<b>First select face, and next object that should be aligned to the face position. </b><br><br><b>Note:</b> This tool allows to align panels or any other objects to face position. You can select objects at objects Tree window holding left CTRL key. This tool allows to avoid thickness step problem, if you want to move panel to the other edge but the way is not a multiple of the panel thickness.')
	
	MagicPanels.showInfo("panelMove2Face", info)

