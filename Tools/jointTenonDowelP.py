import FreeCAD, FreeCADGui, Draft
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
		
		if index == 0:
			
			# create base tenon dowel
			joint = FreeCAD.ActiveDocument.addObject("Part::Box","tenon")
			joint.Label = translate("jointTenonDowelP", "Tenon pattern ")
			[ joint.Length, joint.Width, joint.Height ] = MagicPanels.getFaceToCube(sub, depth, offset)

			# create parametric joint as container for Clones
			jointP = MagicPanels.createContainer( [ joint ], iLabel="Tenon dowel patterns ", iNesting=False)
			joint.recompute()
			
			# set joint anchor
			anchorJoint = joint.Shape.CenterOfMass
			anchorJoint = [ float(anchorJoint.x), float(anchorJoint.y), float(anchorJoint.z) ]
			[ anchorJoint ] = MagicPanels.getVerticesPosition([ anchorJoint ], joint, "array")

		else:
			
			# create Clone to tenon dowel pattern
			joint = Draft.make_clone(jointP)
			joint.Label = translate("jointTenonDowelP", "Tenon clone ")
			joint.recompute()
		
			# set joint anchor (LinkGroup not has CenterOfMass)
			anchorJoint = joint.Shape.CenterOfGravity
			anchorJoint = [ float(anchorJoint.x), float(anchorJoint.y), float(anchorJoint.z) ]
			[ anchorJoint ] = MagicPanels.getVerticesPosition([ anchorJoint ], joint, "array")

		# set face anchor
		anchorFace = sub.CenterOfMass
		anchorFace = [ float(anchorFace.x), float(anchorFace.y), float(anchorFace.z) ]
		[ anchorFace ] = MagicPanels.getVerticesPosition([ anchorFace ], o, "array")

		# set tenon dowel into face position
		MagicPanels.setAnchors(joint, anchorJoint, anchorFace)
		
		# not move first pattern
		if index != 0:
			MagicPanels.moveToFirst([ joint ], o)

		# set hide attribute for cut-list
		if not hasattr(joint, "BOM"):
			info = translate("jointTenonDowelP", "Allows to skip tenon at BOM, cut-list report.")
			joint.addProperty("App::PropertyBool", "BOM", "Woodworking", info)
			joint.BOM = False
		
		# set tenon attribute for cut via cutTenonDowels tool
		if not hasattr(joint, "Tenon"):
			info = translate("jointTenonDowelP", "Allows to cut tenon dowel via cutTenonDowels tool.")
			joint.addProperty("App::PropertyBool", "Tenon", "Woodworking", info)
			joint.Tenon = True

		# set colors and go to next face
		MagicPanels.copyColors(o, joint)
		index = index + 1
		
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('jointTenonDowelP', '<b>Please select at least one face to create parametric tenon dowel joint at the selected face. </b><br><br><b>Note:</b> This is parametric version of jointTenonDowel tool. In this case all the tenon dowels are linked via Clones to the simple LinkGroup container. Inside the LinkGroup container is the simple Part::Box object as tenon dowel pattern. This approach allows you to add new objects to the LinkGroup container or change the tenon dowel pattern inside the container and all tenon dowel clones will be updated. This tool works in the same way as jointTenonDowel and allows to create quick tenon as dowel joint at selected face. This tool support any object type because the tenon dowel is additional object only positioned at the face. This tool supports multi face selection. To select more faces hold left control button CTRL during faces selection. The tenon as dowel joint offset is 1/4 of the object thickness but you can change the tenon dowel pattern size and offset here because it is parametric. By default the tenon dowel joint is hidden inside the object equally to the visible part, thickness up and thickness down. So, you can cut all the tenon dowels also at the object and create removable joints similar to the dowels using cutTenonDowels tool. Created tenon dowels have special BOM attribute. By default the BOM attribute is set to False, so all tenon dowels are not listed at cut-list report, but if you set it to True, those tenon dowels will be listed. Also the parametric tenon dowels have special Tenon attribute, set by default to True to notify the cutTenonDowels tool to cut such tenon dowel. But if you set it to False such tenon dowel will be skipped during cut.')

	MagicPanels.showInfo("jointTenonDowelP", info)
