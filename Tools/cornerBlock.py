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

	edges = dict()
	sizes = dict()
	labels = dict()

	i = 0
	for o in objects:

		oRef = MagicPanels.getReference(o)
		if MagicPanels.isRotated(oRef):
			s = MagicPanels.getSizes(oRef)
			s.sort()
		else:
			s = MagicPanels.getSizesFromVertices(oRef)
			s.sort()

		edges[o] = [ FreeCADGui.Selection.getSelectionEx()[i].SubObjects[0] ]
		sizes[o] = [ s[0] ]
		labels[o] = "cornerBlock "

		i = i + 1

	# ###################################################################################################################
	# main call
	# ###################################################################################################################

	FreeCAD.ActiveDocument.openTransaction("cornerBlock")
	cuts = MagicPanels.makeChamferCut(objects, edges, sizes, labels)
	FreeCAD.ActiveDocument.commitTransaction()
	
except:
	
	info = ""
	
	info += translate('cornerBlock', '<b>Please select single edge at each panel you want to change into corner block. </b><br><br><b>Note:</b> This tool allows to create corner block from selected edge. The cut size will be the panel thickness. The cut will be at the other side of selected edge, for better access for example if you create Cube 100 mm x 100 mm x 100 mm in the corner of the table to support table leg, and you want to change it into corner block, quickly with single click. You can replace more than one panel at once. Hold left CTRL key during edges selection.')

	MagicPanels.showInfo("cornerBlock", info)

