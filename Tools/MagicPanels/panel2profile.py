import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()
	
	if len(objects) == 0:
		raise

	# ###################################################################################################################
	# main loop
	# ###################################################################################################################

	for obj in objects:
	
		sizes = MagicPanels.getSizes(obj)
		sizes.sort()
		
		# need to be equal to cut ends
		if not MagicPanels.equal(sizes[0], sizes[1]):
			raise
		
		if obj.isDerivedFrom("Part::Box"):
	
			[ part, body, sketch, pad ] = MagicPanels.makePad(obj, "Construction")
			FreeCAD.ActiveDocument.removeObject(obj.Name)
			FreeCAD.ActiveDocument.recompute()

		else:
	
			body = obj._Body
			pad = obj
		
		profile = body.newObject('PartDesign::Thickness','Profile')
		
		faces = []
		i = 0
		for f in pad.Shape.Faces:
			if MagicPanels.equal(pad.Shape.Faces[i].Length, 4 * sizes[0]):
				faces.append("Face"+str(i+1))

			i = i + 1
			
		profile.Base = (pad, faces)
		profile.Value = 1
		profile.Reversed = 1
		profile.Mode = 0
		profile.Intersection = 0
		profile.Join = 0

		pad.Visibility = False

		FreeCAD.ActiveDocument.recompute()
		
		colors = [ (0.0, 0.0, 0.0, 0.0),
			(0.0, 0.0, 0.0, 0.0),
			(0.0, 0.0, 0.0, 0.0),
			(0.0, 0.0, 0.0, 0.0),
			(0.0, 0.0, 0.0, 0.0),
			(0.0, 1.0, 0.0, 0.0),
			(0.0, 0.0, 0.0, 0.0),
			(0.0, 1.0, 0.0, 0.0),
			(0.0, 1.0, 0.0, 0.0),
			(0.0, 1.0, 0.0, 0.0) ]

		profile.ViewObject.DiffuseColor = colors

		FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('panel2profile', '<b>Please select valid Cube or Pad object imitating profile. The selected Cube or Pad objects need to have two equal sizes e.g. 20 mm x 20 mm x 300 mm to replace it with construction profile. </b><br><br><b>Note:</b> This tool allows to replace panel with construction profile. You can replace more than one panel at once. To select more panels hold left CTRL key during selection. The new created construction profile will get the same dimensions, placement and rotation as the selected panel. If you have all construction created with simple panel objects that imitating profiles, you can replace all of them with realistic looking construction profiles with single click.')

	MagicPanels.showInfo("panel2profile", info)


