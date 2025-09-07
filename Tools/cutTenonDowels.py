import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 1:
		raise

	# prepere tenons to avoid double count of copies in Cut
	tenons = []
	for o in FreeCAD.ActiveDocument.Objects:
		if hasattr(o, "Tenon"):
			if o.Visibility == True and o.Tenon == True:
				tenons.append(o)

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
	
	info += translate('cutTenonDowels', '<b>Please select at least one panel to cut all tenon dowels. </b><br><br><b>Note:</b> This tool allows to create mortises using tenon dowels created via jointTenonDowel or jointTenonDowelP tool. You do not have to select and search exact tenon dowels that belongs to the selected panel, this tool cut all tenon dowels automatically for selected panel. If you select panel, this tool search for all tenon dowels that belongs to the selected panel and apply Part Boolean Cut operation on the panel. The selected panel should rather be Part::Box type to not mix Part::Box objects with PartDesign::Pad design line too much. You can select multiply panels at once to cut tenon dowels. To select more panels hold left control key CTRL during objects selection. During this process only the copies will be used to cut, so the original tenon dowels will not be moved at the objects Tree. This feature is sensitive for visibility of tenon dowels and also for Tenon attribute. If the tenon dowel is hidden or Tenon attribute is set to False, such tenon dowel will be skipped during cut.')

	MagicPanels.showInfo("cutTenonDowels", info)
