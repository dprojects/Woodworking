import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 2:
		raise

	base = objects[0]
	knife = objects[0]
	knifeName = str(knife.Name)
	knifeLabel = str(knife.Label)

	if not knife.isDerivedFrom("App::LinkGroup"):
		knife = MagicPanels.createContainer([knife])

	objects = objects[1:]

	for o in objects:
		
		knifeLink = FreeCAD.ActiveDocument.addObject('App::Link', "Link")
		knifeLink.setLink(knife)
		knifeLink.Label = MagicPanels.getNestingLabel(knife, "Knife")

		if not hasattr(knifeLink, "BOM"):
			info = translate("magicKnifeLinks", "Allows to skip this duplicated copy in BOM, cut-list report.")
			knifeLink.addProperty("App::PropertyBool", "BOM", "Woodworking", info)

		knifeLink.BOM = False

		cut = FreeCAD.ActiveDocument.addObject("Part::Cut", "Cut")
		cut.Base = o
		cut.Tool = knifeLink
		cut.Label = MagicPanels.getNestingLabel(o, "Cut")
		o.Visibility = False
		
		FreeCAD.ActiveDocument.recompute()
		
		try:
			MagicPanels.copyColors(base, cut)
		except:
			skip = 1

	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:

	info = ""

	info += translate('magicKnifeLinks', '<b>First select knife (object) and later all panels (objects) you want to cut with this knife. </b><br><br><b>Note:</b> This tool allows to use single knife to cut many panels. First selected object should be knife, and all other selected objects will be cut with the knife. The knife can be any object. So, you can create your own shape of the knife and cut many panels at once. Also you can cut all legs of the table using floor or top of the table as knife. To select more objects hold left CTRL key during selection. During this process the links of knife are used, so the original knife objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. This tool works with the same way as magicKnife tool but creates LinkGroup container for Knife and uses container links for cut operation. Thanks to this approach you can change Knife Cube to Pad or even add new Knife to the LinkGroup container and the cut will be updated with new Knife content. So, if you are looking for parametric cut, you should rather use this version.')

	MagicPanels.showInfo("magicKnifeLinks", info)
