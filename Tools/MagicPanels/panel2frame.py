import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	# ###################################################################################################################
	# init database for call
	# ###################################################################################################################

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) == 0:
		raise

	faces = dict()

	i = 0
	for o in objects:
		faces[o] = FreeCADGui.Selection.getSelectionEx()[i].SubObjects
		i = i + 1

	# ###################################################################################################################
	# main call
	# ###################################################################################################################
	
	frames = MagicPanels.makeFrame45cut(objects, faces)

except:
	
	info = ""
	
	info += translate('panel2frameInfo', '<b>Please select single face for each Cube object to make 45 cut at both sides. </b><br><br><b>Note:</b> This tool allows to replace Cube panel with frame 45 cut at both sides. You can replace more than one Cube panel at once. To replace Cube objects with frames you have to select exact face at each Cube object. To select more objects hold left CTRL key during selection. The new created frame will get the same dimensions, placement and rotation as the selected Cube panel but will be cut at the selected face. If you have all construction created with simple Cube objects that imitating picture frame or window, you can replace all of them with realistic looking frame with single click.')

	MagicPanels.showInfo("panel2frame", info)

