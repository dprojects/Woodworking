import FreeCAD, FreeCADGui
from PySide import QtGui

selected = FreeCADGui.Selection.getSelection()
selectedLen = len(selected)

if selectedLen == 0:
	QtGui.QMessageBox.information(None,"panelSideLeft","Please select face to create side panel adjusted to left and try again.")
	
else: 
	try:
		obj = FreeCADGui.Selection.getSelection()[0]
		face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
	except:
		QtGui.QMessageBox.information(None,"panelSideLeft","Please select face not object and try again.")
		
	vertexes = face.Edges[0].Vertexes
	x = vertexes[1].X - obj.Height.Value
	y = vertexes[1].Y
	z = vertexes[1].Z

	panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideLeft")
	panel.Length = obj.Height
	panel.Width = obj.Width
	panel.Height = obj.Length
	
	panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
	
	FreeCAD.activeDocument().recompute()
