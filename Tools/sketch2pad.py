import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	selection = FreeCADGui.Selection.getSelection()
	if len(selection) < 1:
		raise

	for sketch in selection:
			
			body = MagicPanels.getBody(sketch)
			
			pad = body.newObject('PartDesign::Pad', "sketch2pad")
			pad.Label = translate('sketch2pad', 'sketch2pad ')
			pad.Profile = sketch
			pad.Length = MagicPanels.gWoodThickness
			sketch.Visibility = False
			
			MagicPanels.setColor(body, 0, MagicPanels.gDefaultColor, "color")
			MagicPanels.setColor(pad, 0, MagicPanels.gDefaultColor, "color")
			
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:

	info = ""
	info += translate('sketch2pad', "<b>Please select at least one Sketch to create a Pad.</b><br><br><b>Note:</b> This tool allows you to create Pad object from selected Sketch. A Pad with the default size of MagicPanels.gWoodThickness and color from magicSettings tool will be created for each selected Sketch. To change the default wood size or color use magicSettings tool or change the Pad attributes directly. To select more Sketches hold left CTRL key during selection. This tool has been created to quickly create Pad object from Sketch created via addExternal tool to create irregular panels very quickly.")

	MagicPanels.showInfo("sketch2pad", info)
