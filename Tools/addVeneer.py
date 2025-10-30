import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	[ subs, objects ] = MagicPanels.getSelectedSubs(iConvert="no")

	index = 0
	for sub in subs:
		
		if sub.ShapeType != "Face":
			continue
		
		o = objects[index]
		
		if MagicPanels.equal(MagicPanels.gEdgebandThickness, 0):
			thick = 0.01
		else:
			thick = MagicPanels.gEdgebandThickness
			
		veneer = FreeCAD.ActiveDocument.addObject("Part::Box","veneer")
		veneer.Label = translate("addVeneer","Venner ")
		[ veneer.Length, veneer.Width, veneer.Height ] = MagicPanels.getFaceToCube(sub, thick, 0)

		centerFace = sub.CenterOfMass
		centerFace = [ float(centerFace.x), float(centerFace.y), float(centerFace.z) ]
		[ centerFace ] = MagicPanels.getVerticesPosition([ centerFace ], o, "array")

		centerObj = o.Shape.CenterOfMass
		centerObj = [ float(centerObj.x), float(centerObj.y), float(centerObj.z) ]
		[ centerObj ] = MagicPanels.getVerticesPosition([ centerObj ], o, "array")

		plane = MagicPanels.getFacePlane(sub)
		
		if plane == "XY":
			if centerObj[2] < centerFace[2]:
				anchorVeneer = veneer.Shape.Faces[4].CenterOfMass
			else:
				anchorVeneer = veneer.Shape.Faces[5].CenterOfMass

		if plane == "XZ":
			if centerObj[1] < centerFace[1]:
				anchorVeneer = veneer.Shape.Faces[2].CenterOfMass
			else:
				anchorVeneer = veneer.Shape.Faces[3].CenterOfMass
				
		if plane == "YZ":
			if centerObj[0] < centerFace[0]:
				anchorVeneer = veneer.Shape.Faces[0].CenterOfMass
			else:
				anchorVeneer = veneer.Shape.Faces[1].CenterOfMass
		
		anchorVeneer = [ float(anchorVeneer.x), float(anchorVeneer.y), float(anchorVeneer.z) ]
		[ anchorVeneer ] = MagicPanels.getVerticesPosition([ anchorVeneer ], veneer, "array")

		MagicPanels.setAnchors(veneer, anchorVeneer, centerFace)
		MagicPanels.moveToFirst([ veneer ], o)

		# #############################################################################
		# set veneer info
		# #############################################################################
		
		subIndex = MagicPanels.getFaceIndex(o, sub)
		subName = "Face" + str(subIndex)
		
		sizes = MagicPanels.getSizes(veneer)
		sizes.sort()
		[ sizeThick, sizeWidth, sizeLength ] = [ sizes[0], sizes[1], sizes[2] ]
		
		# #############################################################################
		# set attributes
		# #############################################################################
		
		# set show attribute for cut-list
		if not hasattr(veneer, "Woodworking_BOM"):
			info = translate("addVeneer", "Allows to skip this object at BOM, cut-list report.")
			veneer.addProperty("App::PropertyBool", "Woodworking_BOM", "Woodworking", info)
			veneer.Woodworking_BOM = True

		# set correct object type
		if not hasattr(veneer, "Woodworking_Type"):
			info = translate("addVeneer", "Object reference for script parsing.")
			veneer.addProperty("App::PropertyString", "Woodworking_Type", "Woodworking", info)
			veneer.Woodworking_Type = "Veneer"

		# set object label
		if not hasattr(veneer, "Woodworking_ObjectLabel"):
			info = translate("addVeneer", "Object reference label.")
			veneer.addProperty("App::PropertyString", "Woodworking_ObjectLabel", "Woodworking", info)
			veneer.Woodworking_ObjectLabel = str(o.Label)
		
		# set object name
		if not hasattr(veneer, "Woodworking_ObjectName"):
			info = translate("addVeneer", "Object reference name.")
			veneer.addProperty("App::PropertyString", "Woodworking_ObjectName", "Woodworking", info)
			veneer.Woodworking_ObjectName = str(o.Name)
			
		# set face name
		if not hasattr(veneer, "Woodworking_FaceName"):
			info = translate("addVeneer", "Face name reference for script parsing.")
			veneer.addProperty("App::PropertyString", "Woodworking_FaceName", "Woodworking", info)
			veneer.Woodworking_FaceName = subName
		
		# set face index
		if not hasattr(veneer, "Woodworking_FaceIndex"):
			info = translate("addVeneer", "Face reference for script parsing.")
			veneer.addProperty("App::PropertyString", "Woodworking_FaceIndex", "Woodworking", info)
			veneer.Woodworking_FaceIndex = str(subIndex)
			
		# set reference thickness
		if not hasattr(veneer, "Woodworking_Ref_Thickness"):
			info = translate("addVeneer", "Veneer thickness for reference object face. It is not current veneer thickness.")
			veneer.addProperty("App::PropertyLength", "Woodworking_Ref_Thickness", "Woodworking", info)
			veneer.Woodworking_Ref_Thickness = sizeThick
		
		# set reference width
		if not hasattr(veneer, "Woodworking_Ref_Width"):
			info = translate("addVeneer", "Veneer width for reference object face. It is not current veneer width.")
			veneer.addProperty("App::PropertyLength", "Woodworking_Ref_Width", "Woodworking", info)
			veneer.Woodworking_Ref_Width = sizeWidth
		
		# set reference length
		if not hasattr(veneer, "Woodworking_Ref_Length"):
			info = translate("addVeneer", "Veneer length for reference object face. It is not current veneer length.")
			veneer.addProperty("App::PropertyLength", "Woodworking_Ref_Length", "Woodworking", info)
			veneer.Woodworking_Ref_Length = sizeLength
		
		MagicPanels.setColor(veneer, 0, MagicPanels.gEdgebandColor, "color", "kernel")
		index = index + 1
		
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('addVeneer', '<b>Please select at least one face to add veneer. </b><br><br><b>Note:</b> Veneer created from PVC material can be up to 2 mm thick. In such a case, you can use this tool, which allows you to simulate the addition of veneer. A Part::Box object will be created on the selected face, simulating the added veneer. This approach allows the added veneer to be easily modified. You can modify the length, width, thickness, and other parameters of the applied veneer, which means you can more accurately calculate how much veneer is needed and what spacing should be maintained when calculating board sizes. The default size and other parameters of the applied veneer are taken from the settings in the magicSettings tool. By default, the thickness of the applied veneer is set to 0 mm to avoid interfering with the modeling process. However, the object cannot be 0 mm thick, so the default settings set the veneer thickness to 0.01 mm. The default veneer color is white because the default board color is brown. Personally, I often use white veneer heat-sealing tape on plywood shelves, which makes the shelf look much better in white furniture. I use black veneer on white chipboard furniture. This approach allows you also to add texture only to veneer and get more realistic look. Added venner is also supported by cut-list created via getDimensions tool, so you can create detailed description of added veneer. To select more faces hold left control button CTRL during faces selection.')

	MagicPanels.showInfo("addVeneer", info)
