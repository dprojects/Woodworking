import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selection = FreeCADGui.Selection.getSelection()

	if len(selection) < 1:
		raise

	i = 0
	for o in selection:

		objRef = MagicPanels.getReference(selection[i])
		subs = FreeCADGui.Selection.getSelectionEx()[i].SubObjects
		i = i + 1

		for objFace in subs:
			
			anchorFace = objFace.CenterOfMass
			anchorFace = [ float(anchorFace.x), float(anchorFace.y), float(anchorFace.z) ]
			[ anchorFace ] = MagicPanels.getVerticesPosition([ anchorFace ], objRef)
			x, y, z = anchorFace[0], anchorFace[1], anchorFace[2]

			[ faceType, eAll, eThick, eShort, eLong ] = MagicPanels.getFaceEdges(objRef, objFace)

			if len(eLong) > 0:
				edge = eLong[0]
			elif len(eShort) > 0:
				edge = eShort[0]
			elif len(eThick) > 0:
				edge = eThick[0]

			sizes = MagicPanels.getSizes(objRef)
			sizes.sort()
			thick = sizes[0]

			offset = thick / 2
			jointSize = thick - offset
			size = edge.Length - offset

			plane = MagicPanels.getEdgePlane(objFace, edge)

			if plane == "X":
				Length = size
				Width = jointSize
				Height = jointSize

			if plane == "Y":
				Length = jointSize
				Width = size
				Height = jointSize

			if plane == "Z":
				Length = jointSize
				Width = jointSize
				Height = size

			joint = FreeCAD.ActiveDocument.addObject("Part::Box","tenon")
			joint.Width, joint.Height, joint.Length = Width, Height, Length

			MagicPanels.setContainerPlacement(joint, x, y, z, 0, "center")
			MagicPanels.moveToFirst([ joint ], objRef)

			if not hasattr(joint, "BOM"):
				info = translate("jointTenon", "Allows to skip tenon at BOM, cut-list report.")
				joint.addProperty("App::PropertyBool", "BOM", "Woodworking", info)
		
			joint.BOM = False

			try:
				MagicPanels.copyColors(objRef, joint)
			except:
				skip = 1

	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('jointTenon', '<b>Please select face to create Tenon joint at the selected face. </b><br><br><b>Note:</b> This tool allows to create quick tenon joint at selected face. You can select multiple faces at single object or multiple faces at multiple objects. The tenon joint offset is 1/4 of the object thickness. The tenon joint is hidden inside the object equally to the visible part. So, you can cut the tenon also at the object and create removable joint similar to the dowels. Tenons have special attribute, so they are not listed at cut-list report.')

	MagicPanels.showInfo("jointTenon", info)

