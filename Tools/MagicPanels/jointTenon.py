import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	base = MagicPanels.getReference()
	face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
	
	joint = FreeCAD.ActiveDocument.addObject("Part::Box","jointtenon")
	joint.Label = str(base.Label) + ", joint - Tenon "
	
	size = 6.35
	joint.Width, joint.Height, joint.Length = 1 * size, 3 * size, 5 * size
	
	[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(face)
	x, y, z = v1[0], v1[1], v1[2]
		
	r = MagicPanels.getFaceObjectRotation(base, face)
	
	[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(base)
	x = x + coX
	y = y + coY
	z = z + coZ

	MagicPanels.setPlacement(joint, x, y, z, r)
	MagicPanels.moveToFirst([ joint ], base)
	
except:
	
	info = ""
	
	info += translate('jointTenon', '<b>Please select face to create Tenon joint at the selected face. </b><br><br><b>Note:</b> This is simple Cube object and will be created in the corner of the selected face (0 vertex), allowing you to move the joint precisely to any place at the face. It has predefined size but you can resize and move the joint to fit to your elements and needs. For example if you set all Tenons at the element, you can quickly cut all Mortises for the Tenons with magicCut.')

	MagicPanels.showInfo("jointTenon", info)

