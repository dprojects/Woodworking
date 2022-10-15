import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	base = MagicPanels.getReference()
	face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
	
	joint = FreeCAD.ActiveDocument.addObject("Part::Box","jointcustom")
	joint.Label = str(base.Label) + ", joint - Custom "
	
	size = 6.35
	joint.Length, joint.Width, joint.Height = 5 * size, 3 * size, 1 * size
	
	[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(face)
	x, y, z = v1[0], v1[1], v1[2]
		
	r = MagicPanels.getFaceObjectRotation(base, face)
		
	MagicPanels.setPlacement(joint, x, y, z, r)
	[ part, body, sketch, pad ] = MagicPanels.makePad(joint, joint.Label)
	
	FreeCAD.ActiveDocument.removeObject(joint.Name)
	FreeCAD.ActiveDocument.recompute()
	
except:
	
	info = ""
	
	info += translate('jointCustom', '<b>Please select face to create Custom joint at the selected face. </b><br><br><b>Note:</b> The simple Pad will be created in the corner of the selected face (0 vertex), allowing you to move the joint precisely to any place at the face. It has predefined size but you can resize and move the joint to fit to your elements and needs. Also you can edit the Sketch to create your custom joint shape. For example if you set all joints at the element, you can quickly cut all Mortises for the joints with magicCut.')

	MagicPanels.showInfo("jointCustom", info)

