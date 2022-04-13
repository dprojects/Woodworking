import FreeCAD

panel = FreeCAD.activeDocument().addObject("Part::Box", "panelYZ")

panel.Length = 18
panel.Width = 600
panel.Height = 300

FreeCAD.activeDocument().recompute()