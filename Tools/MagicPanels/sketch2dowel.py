import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 2:
		raise

	face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
	objRef = FreeCADGui.Selection.getSelection()[0]

	i = 0
	for o in objects:

		i = i + 1
		
		if i == 1:
			base = o
			continue

		sketch = o

		if not sketch.isDerivedFrom("Sketcher::SketchObject"):
			raise
			
		hole = ""
			
		if sketch.InList[0].isDerivedFrom("PartDesign::Hole"):
			hole = sketch.InList[0]
			htype = "hole"
			
		if sketch.InList[1].isDerivedFrom("PartDesign::Hole"):
			hole = sketch.InList[1]
			htype = "hole"
		
		if sketch.InList[0].isDerivedFrom("PartDesign::Pocket"):
			hole = sketch.InList[0]
			htype = "pocket"
			
		if sketch.InList[1].isDerivedFrom("PartDesign::Pocket"):
			hole = sketch.InList[1]
			htype = "pocket"
		
		if hole == "":
			raise
		
		[ x, y, z, r ] = MagicPanels.getSketchPlacement(sketch, "global")
		r = MagicPanels.getFaceObjectRotation(hole, face)
		
		d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DowelSketch")
		d.Label = "Dowel - " + str(sketch.Label)

		if htype == "hole":
			d.Radius = hole.Diameter / 2
			d.Height = hole.Depth
		
		if htype == "pocket":
			d.Radius = hole.Profile[0].Geometry[0].Radius
			loc = hole.Profile[0].Geometry[0].Location
			x = x + loc[0]
			y = y + loc[1]
			z = z + loc[2]
			
			if hole.Midplane == 1:
				d.Height = hole.Length / 2
			else:
				d.Height = hole.Length
			
		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(objRef)
		x = x + coX
		y = y + coY
		z = z + coZ
		MagicPanels.setContainerPlacement(d, x, y, z, r, "clean")
		MagicPanels.moveToFirst([ d ], objRef)

except:
	
	info = ""
	
	info += translate('sketch2dowel', '<b>Please first select face, next Sketches of the holes to create dowels. </b><br><br> <b>Note:</b> This tool allows to create dowel from Sketch of the hole. The first selected face refers to the side the dowel will be raised, exact orientation for the dowel. Dowel position will be get from the Sketch. The dowel Radius and Height will be get from hole object. If the hole is throughAll the dowel height will be very big, so make sure you use dimensions for hole. To select more Sketches hold left CTRL key during selection.')

	MagicPanels.showInfo("sketch2dowel", info)
