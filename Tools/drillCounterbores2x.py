import FreeCAD, FreeCADGui, Part, Sketcher
import MagicPanels

MagicPanels.initConfig()
translate = FreeCAD.Qt.translate

try:

	base = FreeCADGui.Selection.getSelection()[0]
	face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
	objects = FreeCADGui.Selection.getSelection()
	
	del objects[0]

	# if face is selected create drill bit at face only
	if len(objects) == 0:

		d = FreeCAD.ActiveDocument.addObject("Part::Cone","DrillBitCounterbore2x")
		d.Label = "Drill Bit - 2 sides "

		# default drill bit size
		d.Radius1 = 3
		d.Radius2 = 7.5
		d.Height = 5
		
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
		colors = [ (0.0, 0.0, 1.0, 1.0), (0.0, 1.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0) ]
		MagicPanels.setColor(d, 0, colors, "color")

		MagicPanels.moveToFirst([ d ], base)

	else:
	
		MagicPanels.makeCounterbores2x(base, face, objects)

except:
	
	info = ""
	
	info += "<b>" + translate('drillCounterbores2x', 'Possible selection methods') + ": " + "</b><ul>"
	info += "<li>"
	info += translate('drillCounterbores2x', 'Select face to create drill bit.')
	info += "</li>"
	info += "<li>"
	info += translate('drillCounterbores2x', 'Select face and next drill bits to drill holes at selected face from both sides of the panel.')
	info += "</li></ul>"
	info += "<b>" + translate('drillCounterbores2x', 'Note') + ": </b>"
	info += translate('drillCounterbores2x', 'This is drill bit to make counterbore2x with hole. The hole will be drilled below the bottom part of the drill bit, below the red surface. The radius of the hole will be equal to Radius1 drill bit attribute. The radius of counterbore will be equal to Radius2 drill bit attribute. The hole depth will be equal to panel thickness. The counterbore depth will be equal to Height drill bit attribute. If you select surface only, the drill bit will be created in the corner of the surface (0 vertex), allowing you to move the drill bit precisely to any place at the surface. Do not move the drill bit up, the drill bit should touch the surface. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected object should be surface, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is type of Part::Box (simple panel), it will be replaced with object with type of PartDesign::Pad.')

	MagicPanels.showInfo("drillCounterbores2x", info)

