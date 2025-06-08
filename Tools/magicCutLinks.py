import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 2:
		raise

	cuts = MagicPanels.makeCutsLinks(objects)
	FreeCADGui.Selection.clearSelection()

except:
	
	info = ""
	
	info += translate('magicCutLinks', '<b>Please select the base object to cut and next the objects that will cut the base element. </b><br><br><b>Note:</b> This tool make multi boolean cut operation at selected objects. First object should be the base object to cut. All other selected objects will cut the base 1st selected object. To select more objects hold left CTRL key during selection. During this process only the links will be used to cut, so the original objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. This tool works with the same way as magicCut tool but creates LinkGroup container for cut panels, knives, and uses container links for cut operation. Thanks to this approach you can change Cube to Pad or even add new element to the LinkGroup container and the cut will be updated with new content. So, if you are looking for parametric cut, you should rather use this version.')

	MagicPanels.showInfo("magicCutLinks", info)
