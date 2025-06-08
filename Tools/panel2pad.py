import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	
	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 1:
		raise

	for o in objects:
		
		FreeCAD.ActiveDocument.openTransaction("panel2pad "+str(o.Label))
		
		objRef = MagicPanels.getReference(o)
		[ part, body, sketch, pad ] = MagicPanels.makePad(objRef, "panel2pad")
		FreeCAD.ActiveDocument.removeObject(objRef.Name)
		FreeCAD.ActiveDocument.recompute()
		
		FreeCAD.ActiveDocument.commitTransaction()
		
except:
	
	info = ""
	
	info += translate('panel2pad', '<b>Please select Cube panels (Part::Box objects) to convert to Pads (PartDesign::Pad objects). </b><br><br><b>Note:</b> This tool allows to replace Cube panel with Pad panel. The new created Pad panel will get the same dimensions, placement and rotation as the selected Cube panel. You can transform many Cube panels into Pad at once. To select more Cubes hold left CTRL key during selection. This tool is mostly dedicated to add decoration that is not supported for Cube objects by FreeCAD PartDesign workbench. You can also change shape by changing the Sketch.')

	MagicPanels.showInfo("panel2pad", info)
