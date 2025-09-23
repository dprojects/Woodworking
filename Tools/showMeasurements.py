import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCAD.ActiveDocument.Objects

	# first remove all old measurements
	removed = 0
	for o in objects:
		if hasattr(o, "Woodworking_Type"):
			if o.Woodworking_Type == "Measurement":
				if o.Woodworking_Remove == True:
					FreeCAD.ActiveDocument.removeObject(str(o.Name))
					removed = removed + 1

	if len(objects) < 1:
		raise

	# refresh objects list if there was no measurements
	if removed == 0:
		
		objects = FreeCAD.ActiveDocument.Objects
		
		# make sure there are objects to parse
		if len(objects) < 1:
			raise

	# or if there was remove do nothing
	else:
		objects = []

	# create new measurements
	for o in objects:
		
		# skip complex objects
		if not o.isDerivedFrom("Part::Box") and not o.isDerivedFrom("PartDesign::Pad"):
			continue
			
		notSame = dict()
		for e in o.Shape.Edges:
			
			# skip not regular edges
			if not e.Curve.isDerivedFrom("Part::GeomLine"):
				continue
			
			# show only new unique edges per object
			key = str(e.Length)
			if not key in notSame.keys():
				
				# get data
				[ v1, v2 ] = MagicPanels.getEdgeVertices(e)
				[ v1, v2 ] = MagicPanels.getVerticesPosition([ v1, v2 ], o, "array")
				edgeIndex = MagicPanels.getEdgeIndex(o, e)
				edgeName = "Edge"+str(edgeIndex)
				index = edgeIndex - 1
				
				# show
				m = MagicPanels.showMeasure(v1, v2, o, o, edgeName, edgeName, 4)
				
				# add remove attribute for next click
				if not hasattr(m, "Woodworking_Remove"):
					info = translate("showMeasurements", "Allows to remove this measurement after next tool icon press.")
					m.addProperty("App::PropertyBool", "Woodworking_Remove", "Woodworking", info)
					m.Woodworking_Remove = True

				# add expressions and make it parametric
				toMove = MagicPanels.getObjectToMove(o)
				
				exprSX = "<<" + str(toMove.Label) + ">>.Shape.Edges[" + str(index) + "].Vertex"+"es[0].X"
				exprSY = "<<" + str(toMove.Label) + ">>.Shape.Edges[" + str(index) + "].Vertex"+"es[0].Y"
				exprSZ = "<<" + str(toMove.Label) + ">>.Shape.Edges[" + str(index) + "].Vertex"+"es[0].Z"
				
				exprEX = "<<" + str(toMove.Label) + ">>.Shape.Edges[" + str(index) + "].Vertex"+"es[1].X"
				exprEY = "<<" + str(toMove.Label) + ">>.Shape.Edges[" + str(index) + "].Vertex"+"es[1].Y"
				exprEZ = "<<" + str(toMove.Label) + ">>.Shape.Edges[" + str(index) + "].Vertex"+"es[1].Z"
				
				try:
					m.setExpression('.Start.x', exprSX)
					m.setExpression('.Start.y', exprSY)
					m.setExpression('.Start.z', exprSZ)
					m.setExpression('.End.x', exprEX)
					m.setExpression('.End.y', exprEY)
					m.setExpression('.End.z', exprEZ)
					
					offsetX = m.Dimline.x - m.Start.x
					offsetY = m.Dimline.y - m.Start.y
					offsetZ = m.Dimline.z - m.Start.z
					m.setExpression('.Dimline.x', '.Start.x + (' + str(offsetX) + ' mm )')
					m.setExpression('.Dimline.y', '.Start.y + (' + str(offsetY) + ' mm )')
					m.setExpression('.Dimline.z', '.Start.z + (' + str(offsetZ) + ' mm )')
					
				except:
					skip = 1
		
				# mark already show
				notSame[key] = 1
			

	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('showMeasurements', '<b>Please create at least one object to show measurements.</b><br><br><b>Note:</b> This tool allows you to quickly create or remove measurements for all simple objects. The objects that will be dimensioned are Part::Box and PartDesign::Pad. For each such object, the list of edges will be searched and all linear edges of various dimensions will be described with a measurement. The text size depends on the distance, so small dimensions like 18 mm thick may not be visible from a distance. This tool is a typical "quick shot" that allows you to quickly enable or disable measurements for objects. Because there are so many dimensions, it should be used primarily with magicView and primarily for X, Y, Z, or explode views. For each such measurement object there is special attribute named "Remove" set by default to True. So if you click the icon again such measurement will be removed. If you want to keep such measurement, just set this "Remove" attribute to False. Also the measurements created via this tool are parametric. So you can change views in magicView and the measurements will follow the changes.')

	MagicPanels.showInfo("showMeasurements", info)
