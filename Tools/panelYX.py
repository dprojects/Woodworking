import FreeCAD, FreeCADGui

panel = FreeCAD.activeDocument().addObject("Part::Box", "panelYX")

try:

	obj = FreeCADGui.Selection.getSelection()[0]
	sizes = [ obj.Length.Value, obj.Width.Value, obj.Height.Value ]
	sizes.sort()

	panel.Length = sizes[1]
	panel.Width = sizes[2]
	panel.Height = sizes[0]
	
except:

	panel.Length = 300
	panel.Width = 600
	panel.Height = 18

FreeCAD.activeDocument().recompute()
