import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	[ subs, objects ] = MagicPanels.getSelectedSubs()

	index = 0
	for sub in subs:
		
		if sub.ShapeType != "Face":
			continue
		
		o = objects[index]
		sizes = MagicPanels.getSizes(o)
		sizes.sort()
		depth = sizes[0]
		offset = - sizes[0] / 4
		
		joint = FreeCAD.ActiveDocument.addObject("Part::Box","tenon")
		[ joint.Length, joint.Width, joint.Height ] = MagicPanels.getFaceToCube(sub, depth, offset)

		anchorJoint = joint.Shape.CenterOfMass
		anchorJoint = [ float(anchorJoint.x), float(anchorJoint.y), float(anchorJoint.z) ]
		[ anchorJoint ] = MagicPanels.getVerticesPosition([ anchorJoint ], joint, "array")

		anchorFace = sub.CenterOfMass
		anchorFace = [ float(anchorFace.x), float(anchorFace.y), float(anchorFace.z) ]
		[ anchorFace ] = MagicPanels.getVerticesPosition([ anchorFace ], o, "array")

		MagicPanels.setAnchors(joint, anchorJoint, anchorFace)
		MagicPanels.moveToFirst([ joint ], o)

		if not hasattr(joint, "BOM"):
			info = translate("jointTenonDowel", "Allows to skip tenon at BOM, cut-list report.")
			joint.addProperty("App::PropertyBool", "BOM", "Woodworking", info)
			
			joint.BOM = False

		MagicPanels.copyColors(o, joint)
		index = index + 1
		
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('jointTenonDowel', '<b>Please select at least one face to create tenon dowel joint at the selected face. </b><br><br><b>Note:</b> This tool allows to create quick tenon as dowel joint at selected face. This tool support any object type because the tenon dowel is additional Part::Box object only positioned at the face. This tool supports multi face selection. To select more faces hold left control button CTRL during faces selection. The tenon as dowel joint offset is 1/4 of the object thickness. The tenon dowel joint is hidden inside the object equally to the visible part, thickness up and thickness down. So, you can cut the tenon dowel also at the object and create removable joint similar to the dowels using cutTenonDowels tool. Created tenon dowels have special attribute, so they are not listed at cut-list report.')

	MagicPanels.showInfo("jointTenonDowel", info)
