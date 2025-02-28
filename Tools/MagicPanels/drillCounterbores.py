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

		d = FreeCAD.ActiveDocument.addObject("Part::Cone","DrillBitCounterbore")
		d.Label = "Drill Bit - counterbore "

		# default drill bit size
		d.Radius1 = 3
		d.Radius2 = 7.5
		d.Height = 50
		
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
		colors = [ (0.0, 0.0, 1.0, 0.0), (0.0, 1.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ]
		d.ViewObject.DiffuseColor = colors
		
		MagicPanels.moveToFirst([ d ], base)

	else:
	
		MagicPanels.makeCounterbores(base, face, objects)

except:
	
	info = ""
	
	info += "<b>" + translate('drillCounterbores', 'Possible selection methods') + ": " + "</b><ul>"
	info += "<li>"
	info += translate('drillCounterbores', 'Select face to create drill bit.')
	info += "</li>"
	info += "<li>"
	info += translate('drillCounterbores', 'Select face and next drill bits to drill holes at selected face.')
	info += "</li></ul>"
	info += "<b>" + translate('drillCounterbores', 'Note') + ": </b>"
	info += translate('drillCounterbores', 'This is drill bit to make counterbore with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of counterbore will be drill bit Radius2. The hole depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad.')

	MagicPanels.showInfo("drillCounterbores", info)

