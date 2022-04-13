import FreeCAD

panel = FreeCAD.activeDocument().addObject("Part::Box", "panelXZ")

panel.Length = 600
panel.Width = 18
panel.Height = 300

FreeCAD.activeDocument().recompute()