import FreeCAD

panel = FreeCAD.activeDocument().addObject("Part::Box", "panelYZ")

try:

	obj = FreeCADGui.Selection.getSelection()[0]
	sizes = [ obj.Length.Value, obj.Width.Value, obj.Height.Value ]
	sizes.sort()

	panel.Length = sizes[0]
	panel.Width = sizes[2]
	panel.Height = sizes[1]
	
except:

	panel.Length = 18
	panel.Width = 600
	panel.Height = 300

FreeCAD.activeDocument().recompute()