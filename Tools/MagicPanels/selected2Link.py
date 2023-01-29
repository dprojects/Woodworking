import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selectedObjects = FreeCADGui.Selection.getSelection()

	if len(selectedObjects) < 1:
		raise

	for o in selectedObjects:
		[ x, y, z, r ] = MagicPanels.getContainerPlacement(o, "clean")
		link = FreeCAD.ActiveDocument.addObject('App::Link','Link')
		link.setLink(o)
		MagicPanels.setContainerPlacement(link, x, y, z, 0, "clean")
		FreeCAD.ActiveDocument.recompute()
		
		link.Label = str(o.Label)
		link.Label = MagicPanels.getNestingLabel(o, "Link")
	
		try:
			MagicPanels.copyColors(o, link)
		except:
			skip = 1

	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('selected2LinkInfo', '<b>Please select objects to create Link. </b><br><br><b>Note:</b> This tool call FreeCAD simple Link command and set color for new Link objects from first selected object. To select more objects hold left CTRL key during selection.')

	MagicPanels.showInfo("selected2Link", info)
