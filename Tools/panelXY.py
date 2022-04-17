import FreeCAD, FreeCADGui

panel = FreeCAD.activeDocument().addObject("Part::Box", "panelXY")

try:

	obj = FreeCADGui.Selection.getSelection()[0]
	sizes = [ obj.Length.Value, obj.Width.Value, obj.Height.Value ]
	sizes.sort()

	panel.Length = sizes[2]
	panel.Width = sizes[1]
	panel.Height = sizes[0]
	
except:

	panel.Length = 600
	panel.Width = 300
	panel.Height = 18

FreeCAD.activeDocument().recompute()
