import FreeCAD, FreeCADGui
import Draft
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selectedObjects = FreeCADGui.Selection.getSelection()
	allObjects = FreeCAD.ActiveDocument.Objects

	if len(selectedObjects) < 2:
		raise
		
	base = selectedObjects[0]
	sketches = selectedObjects[1:]

	sketchPattern = FreeCAD.ActiveDocument.copyObject(base)
	sketchPattern.Label = "Parametric Pattern "
	
	for sketch in selectedObjects:

		for o in allObjects:
			skip = 0
			try:
				test = o.Profile[0]
			except:
				skip = 1

			if skip == 0:
				if str(o.Profile[0].Name) == str(sketch.Name):

					cloneName = "clone_" + str(sketch.Name)
					clone = Draft.make_clone(sketchPattern)
					clone.Label = "Clone " + str(sketch.Label) + " "

					[ x, y, z, r ] = MagicPanels.getSketchPlacement(sketch, "global")
					MagicPanels.setPlacement(clone, x, y, z, r)

					FreeCAD.ActiveDocument.recompute()

					parent = FreeCAD.ActiveDocument.getObject(o.Name)
					
					body = parent._Body
					clone.adjustRelativeLinks(body)
					body.ViewObject.dropObject(clone, None, '', [])

					parent.Profile = clone
					clone.Visibility = False

		sketch.Visibility = False
		FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('sketch2clone', '<b>Please select valid sketches to make parametric model. </b><br><br><b>Note:</b> This tool allows to replace selected Sketches with Clones and thanks to it, convert static model to parametric. First selected Sketch will be changed into "Parametric Pattern" for all other selected Sketches. After this operation, if you change the "Parametric Pattern" all other Sketches will be automatically updated with new pattern. For example if you have Pad, it will change the shape. Make sure the center of coordinate axes XYZ for each selected Sketch is in the middle of the pattern, this will allow for correct positioning of the Sketches. To select more objects hold left CTRL key during selection. For more complicated objects use panel2link or panel2clone at the whole Part. ')

	MagicPanels.showInfo("sketch2clone", info)

