import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selectedObjects = FreeCADGui.Selection.getSelection()
	allObjects = FreeCAD.ActiveDocument.Objects

	if len(selectedObjects) < 2:
		raise

	baseObj = selectedObjects[0]

	try:
		baseSub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

		if str(baseSub.ShapeType) == "Vertex":
			[ X, Y, Z ] = [ float(baseSub.X), float(baseSub.Y), float(baseSub.Z) ]

		elif str(baseSub.ShapeType) == "Edge" or str(baseSub.ShapeType) == "Face":
			v = baseSub.CenterOfMass
			[ X, Y, Z ] = [ float(v.x), float(v.y), float(v.z) ]

		else:
			skip = 1

	except:
		[ X, Y, Z, R ] = MagicPanels.getContainerPlacement(baseObj, "clean")

	[[ X, Y, Z ]] = MagicPanels.getVerticesPosition([[ X, Y, Z ]], baseObj)
	objects = selectedObjects[1:]

	i = 1
	for o in objects:

		try:
			sub = FreeCADGui.Selection.getSelectionEx()[i].SubObjects[0]

			if str(sub.ShapeType) == "Vertex":
				anchor = [ float(sub.X), float(sub.Y), float(sub.Z) ]
				[ anchor ] = MagicPanels.getVerticesPosition([ anchor ], o)

			elif str(sub.ShapeType) == "Edge" or str(sub.ShapeType) == "Face":
				v = sub.CenterOfMass
				anchor = [ float(v.x), float(v.y), float(v.z) ]
				[ anchor ] = MagicPanels.getVerticesPosition([ anchor ], o)

			else:
				skip = 1

		except:
			anchor = "normal"

		toMove = MagicPanels.getObjectToMove(o)
		
		if toMove.isDerivedFrom("PartDesign::SubShapeBinder"):
			MagicPanels.setPosition(toMove, X, Y, Z, "global")
		else:
			MagicPanels.setContainerPlacement(toMove, X, Y, Z, 0, anchor)
		
		i = i + 1

	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += "<b>" + translate('panelMove2Anchor', 'First select anchor at base object, next select anchor at each object to move.') + "</b>"
	info += "<br><br>"
	info += translate('panelMove2Anchor', 'Possible anchors to select') + ":"
	info += "<ul>"
	info += "<li><b>" + translate('panelMove2Anchor', 'vertex') + "</b> - "
	info += translate('panelMove2Anchor', 'position of selected vertex') + "</li>"
	info += "<li><b>" + translate('panelMove2Anchor', 'edge') + "</b> - "
	info += translate('panelMove2Anchor', 'edge CenterOfMass') + "</li>"
	info += "<li><b>" + translate('panelMove2Anchor', 'face') + "</b> - "
	info += translate('panelMove2Anchor', 'face CenterOfMass') + "</li>"
	info += "<li><b>" + translate('panelMove2Anchor', 'object') + "</b> - "
	info += translate('panelMove2Anchor', 'position of default object Placement') + "</li>"
	info += "</ul>"
	info += "<b>" + translate('panelMove2Anchor', 'Note') + ": </b>"
	info += translate('panelMove2Anchor', 'This tool allows you to align panels more precisely, to connect selected anchors. Hold left CTRL key to select anchors.')
	
	MagicPanels.showInfo("panelMove2Anchor", info)
