import FreeCAD, FreeCADGui, Part, Draft
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	# get selection
	[ subs, objects ] = MagicPanels.getSelectedSubs("yes")

	sizes = MagicPanels.getSizes(objects[0])
	sizes.sort()

	sizeOffset = sizes[0] / 4
	sizePocket = sizes[0]

	baseSub = subs[0]
	baseObj = objects[0]

	# create Sketch Pattern in separate container
	doc = FreeCAD.ActiveDocument

	partPattern = doc.addObject('App::Part', 'Part')
	partPattern.Label = translate("jointTenonCut", "Part, jointTenonCut")

	bodyPattern = doc.addObject('PartDesign::Body', 'Body')
	bodyPattern.Label = translate("jointTenonCut", "Body, jointTenonCut")
	partPattern.addObject(bodyPattern)

	wires = baseSub.Wires

	for w in baseSub.Wires:
		ow = w.makeOffset2D(-sizeOffset, join=0, fill=False, openResult=False, intersection=True)
		wires.append(ow)

	sketchPattern = Draft.make_sketch(wires, autoconstraints=True)
	sketchPattern.Label = translate('jointTenonCut', 'Pattern, jointTenonCut')

	# reset pattern to 0 position 
	sketchPatternPosition = sketchPattern.Placement
	MagicPanels.resetPlacement(sketchPattern)

	# create clones
	index = 0
	for sub in subs:
		
		if sub.ShapeType != "Face":
			continue

		o = objects[index]
		body = o._Body
		
		# create clone for object pocket
		sketchClone = Draft.make_clone(sketchPattern)
		sketchClone.Label = "Clone, jointTenonCut"
		sketchClone.recompute()
		
		# move clone to object
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
		
		# move clone to center of the face
		centerSub = [ sub.CenterOfMass.x, sub.CenterOfMass.y, sub.CenterOfMass.z ]
		[ centerSub ] = MagicPanels.getVerticesPosition([ centerSub ], o, "array")
		MagicPanels.setPosition(sketchClone, centerSub[0], centerSub[1], centerSub[2], "global")
		sketchClone.recompute()
		
		# move clone to center offset
		cg = sketchClone.Shape.CenterOfGravity
		centerClone = [ cg.x, cg.y, cg.z ]
		[ offetX, offetY, offetZ ] = MagicPanels.getOffset(sketchClone, centerClone, "array")
		MagicPanels.setPosition(sketchClone, -offetX, -offetY, -offetZ, "offset")

		# make pocket via clone
		pocket = body.newObject('PartDesign::Pocket','jointTenonCut')
		pocket.Label = translate('jointTenonCut', 'jointTenonCut ')
		pocket.Profile = sketchClone
		pocket.Midplane = 1
		pocket.Length = sizePocket
		sketchClone.Visibility = False
		o.Visibility = False

		# set colors
		MagicPanels.copyColors(o, pocket)
		
		# go to next selected sub-object
		index = index + 1
		sketchClone.recompute()
		pocket.recompute()

	FreeCAD.ActiveDocument.recompute()

	# restore pattern position
	sketchPattern.Placement = sketchPatternPosition

	# move pattern to object folder
	sketchPattern.adjustRelativeLinks(bodyPattern)
	bodyPattern.ViewObject.dropObject(sketchPattern, None, '', [])
	sketchPattern.Visibility = False

	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('jointTenonCut', '<b>Please select at least one face to cut tenon joint at the selected face. </b><br><br><b>Note:</b> This tool cut tenon at the selected face in the parametric way. The pocket is created using Clones to the Sketch pattern. The Sketch pattern for pocket operation will be the same for all selected faces and is based from first selected face. So if the faces have different sizes it is recommended to use this tool twice with different selection to have two Sketch patterns for pockets. This tool supports multi face selection. To select more faces hold left control button CTRL during faces selection. The objects can be type of PartDesign::Pad or Part::Box. If the object is Part::Box it will be automatically converted into PartDesign::Pad object and the cut will be done on such Pad. The dimensions is taken from not-cut Pad objects, SizeX and SizeY constraints.')

	MagicPanels.showInfo("jointTenonCut", info)
