import FreeCAD, FreeCADGui, Draft
import MagicPanels

translate = FreeCAD.Qt.translate

woodThick = "18 mm"

try:
	selection = FreeCADGui.Selection.getSelection()

	# you have to select at least single sketch
	if len(selection) < 1:
		raise

	for sketch in selection:
		wires = sketch.Shape.Wires
		for wire in wires:
			
			part = FreeCAD.ActiveDocument.addObject('App::Part', 'Part')
			part.Label = translate('wires2pad', 'Part, wire2pad ')
			body = FreeCAD.ActiveDocument.addObject('PartDesign::Body', 'Body')
			body.Label = translate('wires2pad', 'Body, wire2pad ')
			part.addObject(body)
			
			draftSketch = Draft.make_sketch(wire, autoconstraints = True)
			draftSketch.Label = translate('wires2pad', 'Pattern, wire2pad ')
			
			draftSketch.adjustRelativeLinks(body)
			body.ViewObject.dropObject(draftSketch, None, '', [])
			FreeCAD.ActiveDocument.recompute()
			
			# create Pad with the Sketch
			pad = body.newObject('PartDesign::Pad', "wire2pad")
			pad.Label = translate('wires2pad', 'wire2pad ')
			pad.Profile = draftSketch
			t = MagicPanels.unit2value(woodThick)
			pad.Length = FreeCAD.Units.Quantity(str(t))
			draftSketch.Visibility = False
			
			MagicPanels.setColor(body, 0, MagicPanels.gDefaultColor, "color")
			MagicPanels.setColor(pad, 0, MagicPanels.gDefaultColor, "color")
			
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:

	info = ""
	info += translate('wires2pad', "<b>Please select at least one Sketch to create a Pad from wires.</b><br><br><b>Note:</b> This tool allows you to create panels from wires in Sketch. A Pad with the default size of 18 mm will be created for each wire. If you want to have a different panel size, change the Pad.Length option or use the Panel from vertices option in the magicManager tool, selecting the appropriate edges. To create separate Pads from one Sketch, wires must not touch each other. If the Sketch is placed in containers, for example Part or LinkGroup with set offsets, you need to adjust the panel position, for example using the panelMove2Anchor tool, selecting two edges. You can also consider creating panels from the Sketch in the root directory, see the addExternal tool.")

	MagicPanels.showInfo("wires2pad", info)

