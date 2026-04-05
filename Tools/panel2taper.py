import FreeCAD, FreeCADGui, Draft
import MagicPanels

MagicPanels.initConfig()
translate = FreeCAD.Qt.translate

try:

	[ subs, objects ] = MagicPanels.getSelectedSubs()

	oIndex = 0
	for sub in subs:
		o = objects[oIndex]
		oIndex = oIndex + 1
		
		if sub.ShapeType == "Face":
			faceIndex = MagicPanels.getFaceIndex(o, sub)
			facePlane = MagicPanels.getFacePlane(sub)
			
			for f in o.Shape.Faces:
				index = MagicPanels.getFaceIndex(o, f)
				plane = MagicPanels.getFacePlane(f)
				
				if plane == facePlane and index != faceIndex:
					face = f
					break

			part = FreeCAD.ActiveDocument.addObject('App::Part', 'Part')
			part.Label = translate('panel2taper', 'Part, panel2taper ')
			body = FreeCAD.ActiveDocument.addObject('PartDesign::Body', 'Body')
			body.Label = translate('panel2taper', 'Body, panel2taper ')
			part.addObject(body)
			
			draftSketch = Draft.make_sketch(face.Wires[0], autoconstraints = True)
			draftSketch.Label = translate('panel2taper', 'Pattern, panel2taper ')
			
			draftSketch.adjustRelativeLinks(body)
			body.ViewObject.dropObject(draftSketch, None, '', [])
			FreeCAD.ActiveDocument.recompute()
			
			pad = body.newObject('PartDesign::Pad', "panel2taper")
			pad.Label = translate('panel2taper', 'panel2taper ')
			pad.Profile = draftSketch
			
			[ Length, Width, Height ] = MagicPanels.getSizes(o)
			
			plane = MagicPanels.getFacePlane(face)
			if plane == "XY":
				pad.Length = Height
			if plane == "XZ":
				pad.Length = Width
			if plane == "YZ":
				pad.Length = Length
			
			pad.Reversed = True
			pad.TaperAngle = "-2 deg"
			draftSketch.Visibility = False
			
			MagicPanels.copyColors(o, body)
			MagicPanels.copyColors(o, pad)
			MagicPanels.moveToFirst([ part ], o)
			
			try:
				if o.isDerivedFrom("Part::Box"):
					FreeCAD.ActiveDocument.removeObject(o.Name)
			except:
				skip = 1
			
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:

	info = translate('panel2taper', "Please select at least one surface to create a tapered panel.</b><br><br><b>Note:</b> This tool allows you to create tapered panel. You can use this tool to create tapered legs of wooden table by selecting the bottom surfaces of each leg. The default taper angle is -2 degrees because the new object is created from other side of the selected surface to keep correct position and taper angle direction. You can change the taper angle by edit the panel2taper object properties. This tool supports multi surface selection, to select more surfaces hold left CTRL key during selection.")

	MagicPanels.showInfo("panel2taper", info)
