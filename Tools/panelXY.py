import FreeCAD

panel = FreeCAD.activeDocument().addObject("Part::Box", "panelXY")

panel.Length = 600
panel.Width = 300
panel.Height = 18

FreeCAD.activeDocument().recompute()