import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selectedObjects = FreeCADGui.Selection.getSelection()

	if len(selectedObjects) < 1:
		raise

	for o in selectedObjects:

		[ X, Y, Z, R ] = MagicPanels.getContainerPlacement(o, "clean")
		[[ X, Y, Z ]] = MagicPanels.getVerticesPosition([[ X, Y, Z ]], o)
		MagicPanels.setContainerPlacement(o, X, Y, Z, 0, "clean")

		# the highest container is last
		containers = MagicPanels.getContainers(o)
		
		# for calculation the highest container is first
		for c in reversed(containers):
			try:
				coR = c.Placement.Rotation
			except:
				continue

			o.Placement.Rotation = o.Placement.Rotation * coR

		container = o.InList[0]
		container.ViewObject.dragObject(o)
		
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('selected2Outside', '<b>Please select objects to move them outside all containers to the root folder. </b><br><br><b>Note:</b> This tool allows you to get out the selected objects from containers. Normally, if you get out object from the container manually, the object will change place and rotation. This tool allows you to move the objects and keep the same position and rotation. This feature might be very useful if automatic movement to container is not what you want. For example you want single element to no longer be mirrored or further processed with other objects inside the container. To select more objects hold left CTRL key during selection.')

	MagicPanels.showInfo("selected2Outside", info)
