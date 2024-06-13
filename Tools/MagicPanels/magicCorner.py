import FreeCAD, FreeCADGui
import Part, JoinFeatures, BOPTools.JoinFeatures
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 2:
		raise

	base = objects[0]
	baseLabel = str(base.Label)
	objects = objects[1:]

	i = 0
	for o in objects:

		corner = BOPTools.JoinFeatures.makeEmbed(name='Corner')
		corner.Base = base
		corner.Tool = o
		corner.Proxy.execute(corner)
		corner.purgeTouched()
		
		for obj in corner.ViewObject.Proxy.claimChildren():
			obj.ViewObject.hide()

		corner.Label = baseLabel
		corner.Label = MagicPanels.getNestingLabel(corner, "Corner")

		FreeCAD.ActiveDocument.recompute()
		base = corner
		baseLabel = corner.Label

		i = i + 1

	try:
		MagicPanels.copyColors(objects[0], corner)
	except:
		skip = 1

	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:

	info = ""

	info += translate('magicCorner', '<b>First select base object and later all panels you want to fit to the base object. </b><br><br><b>Note:</b> This tool allows to create corner connection via Part :: Embed object FreeCAD feature. To fit corners, first select base object that will be cut, next panels that should be fited to the base object. To select multiple panels hold left CTRL key during selection.')

	MagicPanels.showInfo("magicCorner", info)
