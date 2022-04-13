import FreeCAD, FreeCADGui
from PySide import QtGui

selected = FreeCADGui.Selection.getSelection()
selectedLen = len(selected)

if selectedLen == 0:
	QtGui.QMessageBox.information(None,"panelYZFace","Please select face to create panel and try again.")
	
else: 
	try:
		obj = FreeCADGui.Selection.getSelection()[0]
		face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
	except:
		QtGui.QMessageBox.information(None,"panelYZFace","Please select face not object and try again.")
		
	vertexes = face.Edges[0].Vertexes
	x = vertexes[1].X
	y = vertexes[1].Y
	z = vertexes[1].Z
	
	if y == 0:
		y = - obj.Height

	panel = FreeCAD.activeDocument().addObject("Part::Box", "panelYZFace")
	panel.Length = obj.Length
	panel.Width = obj.Height
	panel.Height = obj.Width
	
	panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
	
	FreeCAD.activeDocument().recompute()
