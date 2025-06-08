import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()
	
	if len(objects) < 1:
		raise

	# prepere cylinders to avoid double count of copies in Cut
	cylinders = []
	for d in FreeCAD.ActiveDocument.Objects:
		if d.isDerivedFrom("Part::Cylinder"):
			if d.Visibility == True:
				cylinders.append(d)

	for o in objects:
		
		tocut = [ o ]
		for d in cylinders:

			v1 = d.Shape.Faces[0].CenterOfMass
			v2 = d.Shape.Faces[1].CenterOfMass
			v3 = d.Shape.Faces[2].CenterOfMass

			if (
				o.Shape.BoundBox.isInside(v1) or 
				o.Shape.BoundBox.isInside(v2) or 
				o.Shape.BoundBox.isInside(v3)
				):
				tocut.append(d)
		
		if len(tocut) > 1:
			cuts = MagicPanels.makeCuts(tocut)
		
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('cutDowels', '<b>Please select panels to cut dowels. </b><br><br><b>Note:</b> This tool is designed to allow drilling for designing approach based on Cut holes using Cylinders without creating PartDesign objects. This tool allows you to automatically cut all dowels from selected panel. You do not have to select and search exact dowels that belongs to the selected panel. If you select panel, this tool search for all dowels that belongs to the selected panel and apply Boolean Cut on the panel. You can select many panels at once to cut dowels. To select more panels hold left CTRL key during selection. During this process only the copies will be used to cut, so the original Cylinders will not be moved at the objects Tree and will be visible at cut-list report. This feature is sensitive for visibility of Cylinders. So, you can hide Cylinders you do not want to be cut out from the panel.')

	MagicPanels.showInfo("cutDowels", info)
