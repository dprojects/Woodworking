import FreeCAD, FreeCADGui, Part, Sketcher
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	base = FreeCADGui.Selection.getSelection()[0]
	face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
	objects = FreeCADGui.Selection.getSelection()
	
	del objects[0]
		
	# if face is selected create drill bit at face only
	if len(objects) == 0:

		d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DrillBitHole")
		d.Label = "Drill Bit - simple hole "

		# default drill bit size
		d.Radius = 4
		d.Height = 25

		# default drill bit position 0 - vertex
		[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(face)
		x, y, z = v1[0], v1[1], v1[2]

		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(base)
		x = x + coX
		y = y + coY
		z = z + coZ
		r = MagicPanels.getFaceObjectRotation(base, face)
		
		MagicPanels.setContainerPlacement(d, x, y, z, r, "clean")
		
		# default drill bit colors (middle, bottom, top)
		colors = [ (1.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0) ]
		d.ViewObject.DiffuseColor = colors
		
		MagicPanels.moveToFirst([ d ], base)

	else:

		MagicPanels.makeHoles(base, face, objects)

except:
	
	info = ""
	
	info += translate('drillHoles', '<b>Please select face to create drill bit. Or please select face and next drill bits to drill holes at selected face. </b><br><br><b>Note:</b> This is drill bit to make simple hole. The hole will be drilled below the bottom part of the drill bit, below the red face of the cylinder. The radius and depth of the hole will be the same as drill bit radius and height. You can resize the drill bit if you want. If you select face only, the drill bit will be created in the corner of the face (0 vertex). So, you will be able to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face to get exact hole depth. If you select face and than any amount of drill bits, the holes will be drilled below each drill bit. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad.')

	MagicPanels.showInfo("drillHoles", info)

