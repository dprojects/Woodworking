import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	# ###################################################################################################################
	# init database for call
	# ###################################################################################################################

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) == 0:
		raise

	edges = dict()
	sizes = dict()
	labels = dict()

	i = 0
	for o in objects:
		
		edges[o] = []
		sizes[o] = []
		labels[o] = "cornerBrace "
		
		oRef = MagicPanels.getReference(o)
		if MagicPanels.isRotated(oRef):
			s = MagicPanels.getSizes(oRef)
			s.sort()
		else:
			s = MagicPanels.getSizesFromVertices(oRef)
			s.sort()

		thick = s[0]
		
		edgeSelected = FreeCADGui.Selection.getSelectionEx()[i].SubObjects[0]
		[ vb1, vb2 ] = MagicPanels.getEdgeVertices(edgeSelected)
		vbv1 = FreeCAD.Vector(vb1)
		planeB = MagicPanels.getEdgePlane(o, edgeSelected)
		
		for e in o.Shape.Edges:
			
			[ vs1, vs2 ] = MagicPanels.getEdgeVertices(e)
			vsv1 = FreeCAD.Vector(vs1)
			vsv2 = FreeCAD.Vector(vs2)
			distance1 = round(vbv1.distanceToPoint(vsv1), MagicPanels.gRoundPrecision)
			distance2 = round(vbv1.distanceToPoint(vsv2), MagicPanels.gRoundPrecision)
			planeS = MagicPanels.getEdgePlane(o, e)
			
			if planeB == planeS and distance1 > thick and distance2 > thick:
			
				edges[o].append(edgeSelected)
				edges[o].append(e)
			
				sizes[o].append(thick)
				sizes[o].append(thick/2)

		i = i + 1

	# ###################################################################################################################
	# main call
	# ###################################################################################################################

	FreeCAD.ActiveDocument.openTransaction("cornerBrace")
	cuts = MagicPanels.makeChamferCut(objects, edges, sizes, labels)
	FreeCAD.ActiveDocument.commitTransaction()
	
except:
	
	info = ""
	
	info += translate('cornerBrace', '<b>Please select single edge at each panel you want to change into corner brace. </b><br><br><b>Note:</b> This tool allows to create corner brace from selected edge (the single visible edge). The cut size will be the panel thickness for the first edge and for the second edge half of the thickness. So, you get nice looking corner brace with single click. For example you can create Cube 100 mm x 100 mm x 100 mm in the corner of the table to support table leg, and you can change it into corner brace, quickly with single click. You can replace more than one panel at once. Hold left CTRL key during edges selection.')

	MagicPanels.showInfo("cornerBrace", info)

