import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	
	objects = FreeCADGui.Selection.getSelectionEx()[0].SubObjects

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
		
		d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DrillBitHole")
		d.Label = "Drill Bit - simple hole "

		d.Radius = edgeRadius
		d.Height = 16

		MagicPanels.setPlacement(d, x, y, z, r)
		
		# default drill bit colors (middle, bottom, top)
		colors = [ (1.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0) ]
		d.ViewObject.DiffuseColor = colors
		
except:
	
	info = ""
	
	info += translate('edge2drillbit', '<b>Please select valid edge to create drill bit. This feature can be used to create drill bits above holes at hinges, angles or other fixture type. </b><br><br><b>Note:</b> This tool allows to create drill bits for making simple hole. The drill bits will be created above the selected hole edges. To create drill bits select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The drill bit Height will be 16. The drill bits radius will be get from the selected edge hole radius but will be little smaller, 1 mm, than the hole to make pilot hole. To select more objects hold left CTRL key during selection.')

	MagicPanels.showInfo("edge2drillbit", info)
