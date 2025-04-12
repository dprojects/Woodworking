import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	
	objects = FreeCADGui.Selection.getSelectionEx()[0].SubObjects
	objRef = FreeCADGui.Selection.getSelection()[0]

	if len(objects) == 0:
		raise
	
	for e in objects:
	
		if not e.Curve.isDerivedFrom("Part::GeomCircle"):
			raise
		
		edgeRadius = e.Curve.Radius - 1
		x = e.Curve.Center[0]
		y = e.Curve.Center[1]
		z = e.Curve.Center[2]
		r = e.Curve.Rotation
		
		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(objRef)
		x = x + coX
		y = y + coY
		z = z + coZ
		
		d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DrillBitHole")
		d.Label = "Drill Bit - simple hole "

		d.Radius = edgeRadius
		d.Height = 16

		MagicPanels.setPlacement(d, x, y, z, r)
		
		# default drill bit colors (middle, bottom, top)
		colors = [ (1.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0) ]
		MagicPanels.setColor(d, 0, colors, "color")

except:
	
	info = ""
	
	info += translate('edge2drillbit', '<b>Please select valid hole edges to create drill bits.</b><br><br><b>Note:</b> This tool can be used to create drill bits above holes of the hinges, angles or other fixture type. You to create drill bits precisely above the hole so that you can drill the hole quickly later. The drill bits will be created above the selected hole edges. To create drill bits select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The drill bit Height will be 16. The drill bits radius will be get from the selected edge hole radius but will be little smaller, 1 mm, than the selected hole, to make correct pilot hole for screw. To select more objects hold left CTRL key during selection.')

	MagicPanels.showInfo("edge2drillbit", info)
