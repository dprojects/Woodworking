import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	# ###################################################################################################################
	# init database
	# ###################################################################################################################

	selection = FreeCADGui.Selection.getSelection()

	if len(selection) == 0:
		raise

	objects = []
	faces = dict()

	k = 0
	while k < len(selection):
		
		objects.insert(k, FreeCADGui.Selection.getSelection()[k])
		faces[objects[k]] = FreeCADGui.Selection.getSelectionEx()[k].SubObjects
		
		k = k + 1

	# ###################################################################################################################
	# main loop
	# ###################################################################################################################

	for o in objects:

		sizes = MagicPanels.getSizes(o)
		sizes.sort()
		
		edgesCut = []
		
		f = faces[o][0]
		selectionFacePlane = MagicPanels.getFacePlane(f)
		
		faceSizes = [ f.Edges[0].Length, f.Edges[1].Length, f.Edges[2].Length, f.Edges[3].Length ]
		faceSizes.sort()
		sizeCut = faceSizes[0]
		
		index = 0 
		for e in o.Shape.Edges:
			if MagicPanels.equal(e.Length, float(o.Value.Value)):

				plane = MagicPanels.getEdgePlane(o, e)
				
				if selectionFacePlane.find(plane) == -1:
					edgesCut.append("Edge"+str(index+1))
				
			index = index + 1

		cut = o._Body.newObject('PartDesign::Chamfer','Angle45Cut')
		cut.Base = (o, edgesCut)
		cut.Size = sizeCut - 0.01
		o.Visibility = False
			
		FreeCAD.ActiveDocument.recompute()
		
		try:
			
			if len(cut.Shape.Faces) == 10:
				
				colors = [ (0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 1.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 1.0, 0.0, 0.0) ]
			
			if len(cut.Shape.Faces) == 14:
			
				colors = [ (0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 1.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 1.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 1.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0),
						(0.0, 0.0, 0.0, 0.0) ]
				
			cut.ViewObject.DiffuseColor = colors
			FreeCAD.ActiveDocument.recompute()
			
		except:
			skip = 1

except:
	
	info = ""
	
	info += translate('panel2angle45cut', '<b>Please select valid face at construction angle to create 45 cut at edges. </b><br><br><b>Note:</b> This tool allows to cut construction angle with 45 cut. You can select many construction angles at once but only single face can be selected for each construction angle. If the construction angle is C-shape you can select face inside profile and two sides will be cut. If the construction angle is L-shape you select single face inside profile and only single side will be cut. Because to create frame with L-shape profiles you have to cut only single side. To create frame with C-shape profiles you have to cut both sides. The face should be selected inside profile to set exact cut size without profile thickness. To select more faces hold left CTRL key during faces selection. You can remove last operation and try again. If you have all construction created with construction angles you can cut all of them at once.')

	MagicPanels.showInfo("panel2angle45cut", info)

