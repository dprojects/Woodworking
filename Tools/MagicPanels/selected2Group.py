import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selectedObjects = FreeCADGui.Selection.getSelection()

	if len(selectedObjects) < 1:
		raise
		
	group = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroup','Group')
	group.Label = MagicPanels.getNestingLabel(selectedObjects[0], "Group")
	
	for o in selectedObjects:
		group.addObject(o)

	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('selected2GroupInfo', '<b>Please select objects to create Group. </b><br><br><b>Note:</b> This tool call FreeCAD Group command. The group name is from first selected object. To select more objects hold left CTRL key during selection.')

	MagicPanels.showInfo("selected2Group", info)
