import FreeCAD, FreeCADGui
from PySide import QtGui

selected = FreeCADGui.Selection.getSelection()
selectedLen = len(selected)

if selectedLen != 3:
	QtGui.QMessageBox.information(None,"panelXYCover","Please select 3 faces to create cover panel and try again.")
	
else: 
	try:
		obj1 = FreeCADGui.Selection.getSelection()[0]
		obj2 = FreeCADGui.Selection.getSelection()[1]
		obj3 = FreeCADGui.Selection.getSelection()[2]
		face1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		face2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
		face3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
	except:
		QtGui.QMessageBox.information(None,"panelXYCover","Please select 3 faces not object and try again.")
		
	vertexes1 = face1.Edges[0].Vertexes
	x1 = vertexes1[1].X
	y1 = vertexes1[1].Y
	z1 = vertexes1[1].Z

	s1 = obj3.Length
	s2 = obj1.Width + obj3.Width
	s3 = obj1.Length
	
	if s1 > 0 and s2 > 0 and s3 > 0:
		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelXYCover")
		panel.Length = s1
		panel.Width = s2
		panel.Height = s3
		
		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z1), FreeCAD.Rotation(0, 0, 0))
		
		FreeCAD.activeDocument().recompute()
	else:
		QtGui.QMessageBox.information(None,"panelXYCover","Can't create this type of panel at selected faces. Try other type of panel here.")
