import FreeCAD, FreeCADGui

panel = FreeCAD.activeDocument().addObject("Part::Box", "panelZY")

try:

	obj = FreeCADGui.Selection.getSelection()[0]
	sizes = [ obj.Length.Value, obj.Width.Value, obj.Height.Value ]
	sizes.sort()

	panel.Length = sizes[0]
	panel.Width = sizes[1]
	panel.Height = sizes[2]
	
except:

	panel.Length = 18
	panel.Width = 300
	panel.Height = 600

FreeCAD.activeDocument().recompute()
