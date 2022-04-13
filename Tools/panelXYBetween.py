import FreeCAD, FreeCADGui
from PySide import QtGui

selected = FreeCADGui.Selection.getSelection()
selectedLen = len(selected)

if selectedLen != 2:
	QtGui.QMessageBox.information(None,"panelXYBetween","Please select 2 faces to create panel between them and try again.")
	
else: 
	try:
		obj = FreeCADGui.Selection.getSelection()[0]
		face1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		face2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
	except:
		QtGui.QMessageBox.information(None,"panelXYBetween","Please select 2 faces not object and try again.")
		
	vertexes1 = face1.Edges[0].Vertexes
	x1 = vertexes1[0].X
	y1 = vertexes1[0].Y
	z1 = vertexes1[0].Z

	vertexes2 = face2.Edges[0].Vertexes
	x2 = vertexes2[0].X
	y2 = vertexes2[0].Y
	z2 = vertexes2[0].Z

	x = abs(x2 - x1)
	y = abs(y2 - y1)
	z = abs(z2 - z1)
	
	z1 = z1 - obj.Length.Value

	if x > 0:
		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelXYBetween")
		panel.Length = x
		panel.Width = obj.Width
		panel.Height = obj.Length
		
		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z1), FreeCAD.Rotation(0, 0, 0))
		
		FreeCAD.activeDocument().recompute()
	else:
		QtGui.QMessageBox.information(None,"panelXYBetween","Can't create this type of panel between selected faces. Try other type of panel here.")
