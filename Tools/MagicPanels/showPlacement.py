import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = ""

	if len(FreeCADGui.Selection.getSelection()) == 0:
		if len(FreeCAD.ActiveDocument.Objects) == 0:
			raise
		else:
			objects = FreeCAD.ActiveDocument.Objects
	else:
		objects = FreeCADGui.Selection.getSelection()

	vertices = []
	for o in objects:

		if hasattr(o, "Placement"):
			[ x, y, z ] = MagicPanels.getPosition(o, "global")
			vertices.append(FreeCAD.Vector(x, y, z))

		else:
			continue

	MagicPanels.showVertex(vertices, 30)


except:
	
	info = ""

	info += translate('showPlacement', '<b>Please create document and objects to see objects anchor placement. </b><br><br><b>Note:</b> This tool allows to see objects anchor placement for selected objects or for all objects, if nothing was selected. To select more objects hold left CTRL key during selection. This tool creates a ball in the default anchor for an object, which corresponds to the X, Y, Z coordinates for the Placement attribute. This allows you to quickly see where the object is anchored and to which vertex it is positioned by default. Additionally, it allows you to quickly check for possible problems with the function of calculating the global position of the object and to further improve it for more complex objects. Unfortunately, FreeCAD has not solved the basic problem with object position for so many years, which means that more complex objects do not know their position and cannot be managed.')
	
	MagicPanels.showInfo("showPlacement", info)
