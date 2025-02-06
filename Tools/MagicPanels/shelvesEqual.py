import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selection = FreeCADGui.Selection.getSelection()
	
	if len(selection) < 3:
		raise

	obj1 = selection[0]
	edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
	
	obj2 = selection[1]
	edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
	
	gapz = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
	startZ = float(edge1.CenterOfMass.z)
	objects = selection[2:]
	num = len(objects)

	thick = 0
	for o in objects:
		
		[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)
		thick = thick + sizeZ

	offset = (gapz - thick) / (num + 1)
	
	i = 0
	for o in objects:
		
		[ sizeX, sizeY, sizeZ ] = MagicPanels.getSizesFromVertices(o)
		
		oRef = MagicPanels.getReference(o)
		toMove = MagicPanels.getObjectToMove(oRef)
		[ X, Y, Z, R ] = MagicPanels.getContainerPlacement(toMove, "clean")

		Z = startZ + ((i + 1) * offset) + (i * sizeZ)
		
		MagicPanels.setContainerPlacement(toMove, X, Y, Z, 0, "clean")
		i = i + 1

	FreeCAD.ActiveDocument.recompute()
	FreeCADGui.Selection.clearSelection()

except:
	
	info = ""

	info += translate('shelvesEqual', 'To set equal space between shelves please select: <br><br>1. selection: <b>X axis edge</b><br>2. selection: <b>X axis edge</b><br>3. selection: <b>shelves to set equal space</b><br><br><b>Note:</b> This tool allows you to set equal space for selected shelves. It works only at Z axis. To select more objects hold left CTRL key during selection.')
	
	MagicPanels.showInfo("shelvesEqual", info)
