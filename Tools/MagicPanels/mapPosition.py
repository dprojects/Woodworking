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
			
			if o.isDerivedFrom("PartDesign::Pad"):
				
				ref = o.Profile[0].Placement
				x = ref.Base.x
				y = ref.Base.y
				z = ref.Base.z
				r = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
				
			else:
				[ x, y, z, r ] = MagicPanels.getPlacement(o)

			continue

		MagicPanels.setPlacement(o, x, y, z, r)


	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""

	info += translate('mapPosition', '<b>First select object to copy position, next select objects to move. </b><br><br><b>Note:</b> This tool allows to move objects to the same position as first selected object. The objects will be moved without rotation. Only the placement will change. If the first selected object is rotated they objects may not match exactly the starting point. This tool is very useful if you want to redesign furniture and you want to create new element. Using this tool you can quickly move the new element to the same position of old element and remove the old element. To select more objects hold left CTRL key during selection. ')
	
	MagicPanels.showInfo("mapPosition", info)

