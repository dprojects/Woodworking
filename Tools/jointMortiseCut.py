import FreeCAD, FreeCADGui, Part, Draft
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	# test selection type
	selectionType = 0
	sketchPattern = FreeCADGui.Selection.getSelection()[0]

	# get selection
	[ subs, objects ] = MagicPanels.getSelectedSubs("yes")

	# set object for Mortise
	mortiseSub = subs[0]
	mortiseObj = objects[0]

	# use existing sketch pattern
	if sketchPattern.isDerivedFrom("Sketcher::SketchObject"):
		selectionType = 1
		
	# create new sketch pattern
	else:
		selectionType = 2
		
		# set tenon face for mortise pattern
		baseSub = subs[1]
		baseObj = objects[1]

		# create Sketch Pattern in separate container
		doc = FreeCAD.ActiveDocument

		partPattern = doc.addObject('App::Part', 'Part')
		partPattern.Label = translate("jointMortiseCut", "Part, jointMortiseCut")

		bodyPattern = doc.addObject('PartDesign::Body', 'Body')
		bodyPattern.Label = translate("jointMortiseCut", "Body, jointMortiseCut")
		partPattern.addObject(bodyPattern)

		sketchPattern = Draft.make_sketch(baseSub.Wires, autoconstraints=True)
		sketchPattern.Label = translate('jointMortiseCut', 'Pattern, jointMortiseCut')

	# reset pattern to 0 position 
	sketchPatternPosition = sketchPattern.Placement
	MagicPanels.resetPlacement(sketchPattern)

	# leave only mortises to cut
	subs = subs[1:]
	objects = objects[1:]
	index = 0

	# create clones and mortises
	for sub in subs:
		
		if sub.ShapeType != "Face":
			continue
		
		o = objects[index]        # set object for selected tenon face
		body = mortiseObj._Body   # set body mortise to move clone there
		
		# create pattern clone for mortise
		sketchClone = Draft.make_clone(sketchPattern)
		sketchClone.Label = "Clone, jointMortiseCut"
		sketchClone.recompute()
		
		# move clone to cut object container
		sketchClone.adjustRelativeLinks(body)
		body.ViewObject.dropObject(sketchClone, None, '', [])

		# set correct rotation
		plane = MagicPanels.getFacePlane(sub)
		if plane == "XY":
			rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0)

		if plane == "XZ":
			rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 90) 
		
		if plane == "YZ":
			rotation = FreeCAD.Rotation(FreeCAD.Vector(0, -1, 0), 90) 

		sketchClone.Placement.Rotation = rotation

		# move clone onto tenon face
		centerSub = [ sub.CenterOfMass.x, sub.CenterOfMass.y, sub.CenterOfMass.z ]
		[ centerSub ] = MagicPanels.getVerticesPosition([ centerSub ], o, "array")
		MagicPanels.setPosition(sketchClone, centerSub[0], centerSub[1], centerSub[2], "global")
		sketchClone.recompute()

		# move clone to its center
		cg = sketchClone.Shape.CenterOfGravity
		centerClone = [ cg.x, cg.y, cg.z ]
		[ centerClone ] = MagicPanels.getVerticesPosition([ centerClone ], sketchClone, "array")
		[ offetX, offetY, offetZ ] = MagicPanels.getOffset(sketchClone, centerClone, "array")
		MagicPanels.setPosition(sketchClone, -offetX, -offetY, -offetZ, "offset")
		sketchClone.recompute()
		
		# switch mortise to global
		centerMortise = [ mortiseSub.CenterOfMass.x, mortiseSub.CenterOfMass.y, mortiseSub.CenterOfMass.z ]
		[ centerMortise ] = MagicPanels.getVerticesPosition([ centerMortise ], mortiseObj, "array")
		
		# switch sub to global
		centerSub = [ sub.CenterOfMass.x, sub.CenterOfMass.y, sub.CenterOfMass.z ]
		[ centerSub ] = MagicPanels.getVerticesPosition([ centerSub ], o, "array")
		
		# move clone from tenon face to mortise object face and set size
		[ x, y, z ] = MagicPanels.getPosition(sketchClone, "global")
		plane = MagicPanels.getFacePlane(sub)
		
		if plane == "XY":
			mortiseSize = abs(centerMortise[2] - centerSub[2])
			if centerMortise[2] < centerSub[2]:
				z = z - mortiseSize
			else:
				z = z + mortiseSize
				
		if plane == "XZ":
			mortiseSize = abs(centerMortise[1] - centerSub[1])
			if centerMortise[1] < centerSub[1]:
				y = y - mortiseSize
			else:
				y = y + mortiseSize
				
		if plane == "YZ":
			mortiseSize = abs(centerMortise[0] - centerSub[0])
			if centerMortise[0] < centerSub[0]:
				x = x - mortiseSize
			else:
				x = x + mortiseSize
				
		MagicPanels.setPosition(sketchClone, x, y, z, "global")
		sketchClone.recompute()
		
		# create mortise via clone
		mortise = body.newObject('PartDesign::Pocket','jointMortiseCut')
		mortise.Label = translate('jointMortiseCut', 'jointMortiseCut ')
		mortise.Profile = sketchClone
		mortise.Midplane = 1
		mortise.Length = 2 * mortiseSize
		sketchClone.Visibility = False
		mortiseObj.Visibility = False

		# set colors
		MagicPanels.copyColors(mortiseObj, mortise)
		
		# go to next selected tenon face
		index = index + 1
		sketchClone.recompute()
		mortise.recompute()

	FreeCAD.ActiveDocument.recompute()

	# restore pattern position
	sketchPattern.Placement = sketchPatternPosition

	# move pattern to object folder if was new created
	if selectionType == 2:
		sketchPattern.adjustRelativeLinks(bodyPattern)
		bodyPattern.ViewObject.dropObject(sketchPattern, None, '', [])
		sketchPattern.Visibility = False

	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('jointMortiseCut', '<b>Possible selections:</b><ul><li><b>Face to create Mortise + Tenons faces</b> - in this case you need to first select the face of the object on which you want to create the Mortise, then press the spacebar to hide the object on which the Mortise will be created, to get access to the tenons faces inside the Mortise object, then while holding down the left CTRL key, select all the tenons faces for which you want to cut the Mortises. The Mortise object will appear if the Mortises will be created correctly. In this case, a new common Mortise pattern will be created for all selected Tenons faces.</li><li><b>Sketch Mortise pattern + Face to create Mortise + Tenons faces</b> - this version is the same as the previous one, except that you must first select the Sketch of an existing Mortise connection. This allows you to continue creating a Mortise for the existing connection pattern.</li></ul><b>Note:</b> This tool cut Mortises at the selected face in the parametric way. The pocket is created using Clones to the Sketch pattern. The Sketch pattern for pocket operation will be the same for all selected tenons faces and is based from first selected face or existing Sketch pattern. So if the faces have different sizes it is recommended to use this tool twice with different selection to have two Sketch patterns for pockets. This tool supports multi face selection. To select more faces hold left control button CTRL during faces selection. The objects can be type of PartDesign::Pad or Part::Box. If the object is Part::Box it will be automatically converted into PartDesign::Pad object and the cut will be done on such Pad. The dimensions is taken from not-cut Pad objects, SizeX and SizeY constraints.')

	MagicPanels.showInfo("jointMortiseCut", info)
