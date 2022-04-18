import FreeCAD, FreeCADGui

panel = FreeCAD.activeDocument().addObject("Part::Box", "panelZX")

try:

	obj = FreeCADGui.Selection.getSelection()[0]
	sizes = [ obj.Length.Value, obj.Width.Value, obj.Height.Value ]
	sizes.sort()

	panel.Length = sizes[1]
	panel.Width = sizes[0]
	panel.Height = sizes[2]
	
except: 

	panel.Length = 300
	panel.Width = 18
	panel.Height = 600

FreeCAD.activeDocument().recompute()
