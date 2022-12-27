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
		
		edgeRadius = e.Curve.Radius
		x = e.Curve.Center[0]
		y = e.Curve.Center[1]
		z = e.Curve.Center[2]
		r = e.Curve.Rotation
		
		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(objRef)
		x = x + coX
		y = y + coY
		z = z + coZ
	
		d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DowelEdge")
		d.Label = "Dowel - edge "

		d.Radius = edgeRadius
		d.Height = 40

		MagicPanels.setPlacement(d, x, y, z, r)
		MagicPanels.moveToFirst([ d ], objRef)

except:
	
	info = ""
	
	info += translate('edge2dowel', '<b>Please select valid edge of the hole to create dowel. </b><br><br><b>Note:</b> This tool allows to create dowels above the selected hole edges. To create dowel select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The dowel Height will be 40. The dowel radius will be get from the selected edge hole radius. To select more objects hold left CTRL key during selection.')

	MagicPanels.showInfo("edge2dowel", info)

