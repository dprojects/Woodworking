import FreeCAD, FreeCADGui
from PySide import QtGui

selected = FreeCADGui.Selection.getSelection()
selectedLen = len(selected)

if selectedLen != 2:
	QtGui.QMessageBox.information(None,"panelXZBetween","Please select 2 faces to create panel between them and try again.")
	
else: 
	try:
		obj = FreeCADGui.Selection.getSelection()[0]
		face1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		face2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
	except:
		QtGui.QMessageBox.information(None,"panelXZBetween","Please select 2 faces not object and try again.")
		
	vertexes1 = face1.Edges[0].Vertexes
	x1 = vertexes1[1].X
	y1 = vertexes1[1].Y
	z1 = vertexes1[1].Z

	vertexes2 = face2.Edges[0].Vertexes
	x2 = vertexes2[1].X
	y2 = vertexes2[1].Y
	z2 = vertexes2[1].Z

	x = abs(x2 - x1)
	y = abs(y2 - y1)
	z = abs(z2 - z1)
	
	if x > 0:
		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelXZBetween")
		panel.Length = x
		panel.Width = obj.Length
		panel.Height = obj.Height
		
		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z1), FreeCAD.Rotation(0, 0, 0))
		
		FreeCAD.activeDocument().recompute()
	else:
		QtGui.QMessageBox.information(None,"panelXZBetween","Can't create this type of panel between selected faces. Try other type of panel here.")
