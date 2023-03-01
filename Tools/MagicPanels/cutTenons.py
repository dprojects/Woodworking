import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 1:
		raise

	# prepere tenons to avoid double count of copies in Cut
	tenons = []
	for tenon in FreeCAD.ActiveDocument.Objects:
		if tenon.isDerivedFrom("Part::Box") and tenon.Name.startswith("tenon"):
			if tenon.Visibility == True:
				tenons.append(tenon)

	for o in objects:
		
		tocut = [ o ]
		for tenon in tenons:

			v1 = tenon.Shape.Faces[0].CenterOfMass
			v2 = tenon.Shape.Faces[1].CenterOfMass
			v3 = tenon.Shape.Faces[2].CenterOfMass
			v4 = tenon.Shape.Faces[3].CenterOfMass
			v5 = tenon.Shape.Faces[4].CenterOfMass
			v6 = tenon.Shape.Faces[5].CenterOfMass

			if (
				o.Shape.BoundBox.isInside(v1) or 
				o.Shape.BoundBox.isInside(v2) or 
				o.Shape.BoundBox.isInside(v3) or 
				o.Shape.BoundBox.isInside(v4) or 
				o.Shape.BoundBox.isInside(v5) or 
				o.Shape.BoundBox.isInside(v6) 
				):
				tocut.append(tenon)
		
		if len(tocut) > 1:
			cuts = MagicPanels.makeCuts(tocut)
		
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('cutTenonsInfo', '<b>Please select panels to cut all tenons. </b><br><br><b>Note:</b> This tool allows to create mortises using tenons. This tool cut all tenons automatically for selected panel. You do not have to select and search exact tenons that belongs to the selected panel. If you select panel, this tool search for all tenons that belongs to the selected panel and apply Boolean Cut on the panel. You can select multiply panels at once to cut tenons. To select more panels hold left CTRL key during selection. During this process only the copies will be used to cut, so the original tenon will not be moved at the objects Tree. This feature is sensitive for visibility of tenons. So, you can hide tenons you do not want to be cut out from the panel.')

	MagicPanels.showInfo("cutTenons", info)
