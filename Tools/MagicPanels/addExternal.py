import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	selection = FreeCADGui.Selection.getSelection()

	# you have to select at least 2 objects, first sketch or plane and single sub-object
	if len(selection) < 2:
		raise

	# init data
	sketch = selection[0]
	selection = selection[1:]

	if sketch.isDerivedFrom("Sketcher::SketchObject"):
		body = sketch.InList[0]

	else:
		part = FreeCAD.ActiveDocument.addObject('App::Part', 'Part')
		part.Label = translate('addExternal', 'Part, addExternal ')

		body = FreeCAD.ActiveDocument.addObject('PartDesign::Body', 'Body')
		body.Label = translate('addExternal', 'Body, addExternal ')
		part.addObject(body)

		sketch = body.newObject('Sketcher::SketchObject', 'Sketch')
		sketch.Label = translate('addExternal', 'Pattern, addExternal ')
		
		sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		plane = MagicPanels.getFacePlane(sub)
		
		# support for FreeCAD 1.0+
		if MagicPanels.gKernelVersion >= 1.0:
		
			if plane == "XY":
				sketch.AttachmentSupport = (body.Origin.OriginFeatures[3])
			if plane == "XZ":
				sketch.AttachmentSupport = (body.Origin.OriginFeatures[4])
			if plane == "YZ":
				sketch.AttachmentSupport = (body.Origin.OriginFeatures[5])
		
		# support for FreeCAD 0.21.2
		else:
			if plane == "XY":
				sketch.Support = (body.Origin.OriginFeatures[3])
			if plane == "XZ":
				sketch.Support = (body.Origin.OriginFeatures[4])
			if plane == "YZ":
				sketch.Support = (body.Origin.OriginFeatures[5])
		
		sketch.MapMode = 'FlatFace'
		FreeCAD.ActiveDocument.recompute()

	# build sub-objects structure with objects reference
	itemsO = [] # items objects
	itemsS = [] # items sub-objects

	i = 1 # skip first removed sketch or plane object
	for o in selection:
		subs = FreeCADGui.Selection.getSelectionEx()[i].SubObjects
		for s in subs:
			itemsO.append(o)
			itemsS.append(s)

		i = i + 1

	# create binder object
	binder = body.newObject('PartDesign::SubShapeBinder','Binder')
	binder.Label = translate('addExternal', 'addExternal')

	# create object with all sub-objects to add to binder
	toAdd = []
	i = 0

	for sub in itemsS:
		
		o = itemsO[i]
		
		if sub.ShapeType == "Edge":
			subIndex = MagicPanels.getEdgeIndex(o, sub)
			item = (o, 'Edge'+str(subIndex))
		
		if sub.ShapeType == "Face":
			subIndex = MagicPanels.getFaceIndex(o, sub)
			item = (o, 'Face'+str(subIndex))

		toAdd.append(item)
		i = i + 1

	# add to binder
	binder.Support = toAdd

	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

	# create external geometry based on binder inside selected sketch
	for i in range(1, len(binder.Shape.Edges)+1):
		sketch.addExternal( str(binder.Name), 'Edge'+str(i) )

	FreeCAD.ActiveDocument.recompute()

except:

	info = ""
	info += translate('addExternal', "Possible selections methods: <ul><li><b>Face as Plane + Edges and Faces</b> - in this case new Sketch with external geometry will be created. The new sketch plane will be taken from first selected face. I recommend this method, because in this case the sketch will be created in the root directory and all drawn wires can be converted to Pads in-place, using for example tool wires2pad or magicManager panel from vertices option.</li><li><b>Sketch + Edges and Faces</b> - in this case the external geometry will be created inside the selected Sketch. If the Sketch is inside containers with offsets you can adjust position of the converted Pads using for example tool panelMove2Anchor and selecting two edges.</li></ul><br><br><b>Note:</b> This tool allows you to quickly create external geometry visible in a sketch from selected edges and faces. Edges or faces can belong to any objects. If you select face all edges will be added as external geometry, if you select edge only single edge will be added. This tool uses the PartDesign::SubShapeBinder function but in a slightly more advanced form. To select more objects, hold down CTRL-left while selecting them.")

	MagicPanels.showInfo("addExternal", info)
