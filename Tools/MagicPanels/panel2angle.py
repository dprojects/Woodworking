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
		
		if len(faces[o]) == 0:
			raise
		
		FreeCAD.ActiveDocument.openTransaction("panel2angle "+str(o.Label))
		
		# store selected faces keys
		facesKeys = []
		for f in faces[o]:
			facesKeys.append(f.BoundBox)
		
		# get size before remove
		sizes = MagicPanels.getSizes(o)
		sizes.sort()
		
		if o.isDerivedFrom("Part::Box"):
		
			[ part, body, sketch, pad ] = MagicPanels.makePad(o, "Construction")
			FreeCAD.ActiveDocument.removeObject(o.Name)
			FreeCAD.ActiveDocument.recompute()
		
		else:
		
			body = o._Body
			pad = o
		
		angle = body.newObject('PartDesign::Thickness','Angle')
		
		facesCut = []
		
		# add smallest faces (profile edges)
		i = 0
		for f in pad.Shape.Faces:
			if MagicPanels.equal(pad.Shape.Faces[i].Length, 4 * sizes[0]):
				facesCut.append("Face"+str(i+1))

			i = i + 1
		
		# add selected faces at new object 
		for key in facesKeys:
			faceIndex = MagicPanels.getFaceIndexByKey(pad, key)
			facesCut.append("Face"+str(faceIndex))
		
		# cut faces
		angle.Base = (pad, facesCut)
		angle.Value = 1
		angle.Reversed = 1
		angle.Mode = 0
		angle.Intersection = 0
		angle.Join = 0

		pad.Visibility = False

		FreeCAD.ActiveDocument.recompute()
		
		# add colors
		
		if MagicPanels.equal(sizes[0], sizes[1]):
		
			if len(faces[o]) == 1:
				colors = [ (0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0) ]

			if len(faces[o]) == 2:
				colors = [ (0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0) ]

		else:
		
			if len(faces[o]) == 1:
				colors = [ (0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0) ]

			if len(faces[o]) == 2:
				colors = [ (0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0) ]
			
			if len(faces[o]) == 3:
				colors = [ (0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0) ]

			if len(faces[o]) >= 4:
				colors = [ (0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 0.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0),
					(0.0, 1.0, 0.0, 1.0) ]

		try:
			MagicPanels.setColor(angle, 0, colors, "color")
			FreeCAD.ActiveDocument.recompute()
			
		except:
			skip = 1
		
		FreeCAD.ActiveDocument.commitTransaction()
except:
	
	info = ""
	
	info += translate('panel2angle', '<b>Please select valid faces at any amount of Cubes or Pads to cut the faces and create construction angle profiles. </b><br><br><b>Note:</b> This tool allows to replace panel with construction angle. You can replace more than one panel at once. To select more faces hold left CTRL key during faces selection. The new created construction angle will get the same dimensions, placement and rotation as the selected panel. You can cut any faces at panel. However, if the panel has two equal sizes e.g. 20 mm x 20 mm x 600 mm, the ends will be cut as well, so you do not have to select them. If you do not have same sizes you have have to select ends too, if you want to cut them. If the selected faces are not valid, e.g. opposite faces, the final object may disappear and be broken. You can remove last operation and try again. If you have all construction created with simple panels that imitating angles, you can replace all of them with realistic looking construction angles with single click and they will be rotated according to the selected faces.')

	MagicPanels.showInfo("panel2angle", info)

