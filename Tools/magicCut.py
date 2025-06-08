import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 2:
		raise

	cuts = MagicPanels.makeCuts(objects)
	FreeCADGui.Selection.clearSelection()

except:
	
	info = ""
	
	info += translate('magicCut', '<b>Please select the base object to cut and next the objects that will cut the base element. </b><br><br><b>Note:</b> This tool make multi boolean cut operation at selected objects. First object should be the base object to cut. All other selected objects will cut the base 1st selected object. To select more objects hold left CTRL key during selection. During this process only the copies will be used to cut, so the original objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. If you are looking for parametric Boolean Cut operation you may consider magicCutLinks instead.')

	MagicPanels.showInfo("magicCut", info)
