import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selectedObjects = FreeCADGui.Selection.getSelection()

	if len(selectedObjects) < 1:
		raise
	
	container = MagicPanels.createContainer(selectedObjects)

except:
	
	info = ""
	
	info += translate('selected2LinkGroupInfo', '<b>Please select objects to create LinkGroup. </b><br><br><b>Note:</b> This tool call FreeCAD LinkGroup command and set color for new LinkGroup objects from first selected object. To select more objects hold left CTRL key during selection.')

	MagicPanels.showInfo("selected2LinkGroup", info)
