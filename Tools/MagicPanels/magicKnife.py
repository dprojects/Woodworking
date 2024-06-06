import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

def QT_TRANSLATE_NOOP(context, text):
	return text

try:

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 2:
		raise

	i = 0
	for o in objects:
		
		i = i + 1
		
		if i == 1:
			knife = o
			knifeName = str(knife.Name)
			knifeLabel = str(knife.Label)
			continue

		knifeCopy = FreeCAD.ActiveDocument.copyObject(knife)
		knifeCopy.Label = MagicPanels.getNestingLabel(knife, "Knife")
		
		if not hasattr(knifeCopy, "BOM"):
			info = translate("App::Property", "Allows to skip this duplicated copy in BOM, cut-list report.")
			knifeCopy.addProperty("App::PropertyBool", "BOM", "Woodworking", info)
		
		knifeCopy.BOM = False
		
		cut = FreeCAD.ActiveDocument.addObject("Part::Cut", "Cut")
		cut.Base = o
		cut.Tool = knifeCopy
		cut.Label = MagicPanels.getNestingLabel(o, "Cut")
		
		FreeCAD.ActiveDocument.recompute()
	
	FreeCADGui.Selection.clearSelection()

except:
	
	info = ""
	
	info += translate('magicKnife', '<b>First select knife (object) and later all panels (objects) you want to cut with this knife. </b><br><br><b>Note:</b> This tool is opposite for magicCut tool. This tool allows to use single knife to cut many panels. First selected object should be knife, and all other selected objects will be cut with the knife. The knife can be any object. So, you can create your own shape of the knife and cut many panels at once. Also you can cut all legs of the table using floor or top of the table as knife. To select more objects hold left CTRL key during selection. During this process the copies of knife are used, so the original knife objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. If you are looking for parametric Boolean Cut operation you may consider magicKnifeLinks instead.')

	MagicPanels.showInfo("magicKnife", info)
