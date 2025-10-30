# ###################################################################################################################
'''

# MagicPanels

	This is MagicPanels library for Woodworking workbench.
	Darek L (github.com/dprojects)

### Usage:

	import MagicPanels
	returned_value = MagicPanels.function(args)

### Functions at this library:

* Should not have error handling and pop-ups, so you can call it from GUI tools in loops.
* Should return value, if further processing needed.

'''
# ###################################################################################################################


__doc__ = "This is MagicPanels library for Woodworking workbench."
__author__ = "Darek L (github.com/dprojects)"


# ###################################################################################################################
'''

'''
# ###################################################################################################################


import FreeCAD, FreeCADGui
from PySide import QtGui
from PySide import QtCore
from FreeCAD import Units

translate = FreeCAD.Qt.translate

def QT_TRANSLATE_NOOP(context, text): #
	return text


# ###################################################################################################################
'''
# Globals
'''
# ###################################################################################################################


gSettingsPref = 'User parameter:BaseApp/Preferences/Woodworking'                     # settings path <br>
gDefaultColor = (0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 1.0)   # default color [247, 185, 108, 255] <br>
gRoundPrecision = 2                        # should be set according to the user FreeCAD GUI settings <br>
gSearchDepth = 200                         # recursive search depth <br>
gKernelVersion = 0                         # FreeCAD version to add support for new kernel changes <br>
gTheme = "default"                         # no theme by default <br>
gWoodThickness = 18                        # main construction wood thickness <br>
gWoodSizeX = 600                           # default panel long size <br>
gWoodSizeY = 300                           # default panel short size <br>
gWindowStaysOnTop = True                   # to keep window on top <br> 
gCurrentSelection = False                  # to skip refresh selection button <br>
gFrontInsideThickness = 18                 # front inside wood thickness <br>
gFrontInsideOffsetL = 2                    # gap left <br>
gFrontInsideOffsetR = 2                    # gap right <br>
gFrontInsideOffsetB = 2                    # gap bottom <br>
gFrontInsideOffsetT = 2                    # gap top <br>
gFrontOutsideThickness = 18                # front outside wood thickness <br>
gFrontOutsideOffsetL = 9                   # overlap left <br>
gFrontOutsideOffsetR = 9                   # overlap right <br>
gFrontOutsideOffsetB = 7                   # overlap bottom <br>
gFrontOutsideOffsetT = 7                   # overlap top <br>
gShelfThickness = 18                       # shelf wood thickness, usually full wood but can be plywood 6 mm <br>
gBackInsideThickness = 18                  # back inside thickness, usually full wood <br>
gBackOutsideThickness = 3                  # back outside thickness, usually HDF <br>
gEdgebandThickness = 0                     # edgeband thickness <br>
gEdgebandApply = "visible"                 # edgeband apply way "everywhere" or "visible"<br>
gEdgebandColor = (1.0, 1.0, 1.0, 1.0)      # white <br>


# > [!CAUTION]
# > Globals are updated from user settings via updateGlobals function at the end of the library.

# Globals (end section for API generator)


# ###################################################################################################################
'''
# Functions for general purpose
'''
# ###################################################################################################################


# ###################################################################################################################
def getSelectedSubs(iConvert="no"):
	'''
	Description:
	
		This function returns object for selected sub-object (face, edge, vertex) and 
		solves the problem you have sub-object and you do not know what is the object. 

		# > [!NOTE]
		# > This function not keep the subs selection order in return because it is driven 
		# > by objects selection order.
		
	Args:
	
		iConvert: if Part::Box should be converted into PartDesign::Pad
			* "no" (default): not convert, just return selection as it is
			* "yes": converts and return subs and objects after conversion

	Usage:
	
		[ boxSubs, boxObjects ] = MagicPanels.getSelectedSubs()
		[ padSubs, padObjects ] = MagicPanels.getSelectedSubs("yes")

	Result:
	
		return array with two arrays or int to raise error:
			* array with two arrays with objects [ subs, objects ]:
				* subs - for subs[i] it is selected sub
				* objects - for objects[i] it is object for subs[i] selected sub
			* or 0 if there are no selection or other error, so this should raise tool error

	'''
	
	selection = FreeCADGui.Selection.getSelection()
	if len(selection) == 0:
		return 0
	
	index = 0
	subs = []
	objects = []

	# create structure with object reference
	for o in selection:
		osubs = FreeCADGui.Selection.getSelectionEx()[index].SubObjects
		for s in osubs:
			subs.append(s)
			objects.append(o)
		
		index = index + 1
	
	# convert each box and create new arrays
	if iConvert == "yes":
		
		[ boxSubs, boxObjects ] = [ subs, objects ]
		subs = []
		objects = []
		converted = {}
		
		index = 0
		for s in boxSubs:
			if s.ShapeType != "Face" and s.ShapeType != "Edge":
				continue
			
			o = boxObjects[index]
			if o.isDerivedFrom("Part::Box"):
				
				# not convert twice the same object
				if str(o.Name) in converted:
					subs.append(s)
					objects.append(converted[str(o.Name)])

				# convert if is not vonverted yet
				else:
					key = s.BoundBox
					
					[ part, body, sketch, pad ] = makePad(o, o.Label)
					
					if s.ShapeType == "Face":
						subIndex = getFaceIndexByKey(pad, key)
						subs.append(pad.Shape.Faces[subIndex-1])
					
					if s.ShapeType == "Edge":
						subIndex = getEdgeIndexByKey(pad, key)
						subs.append(pad.Shape.Edges[subIndex-1])
					
					objects.append(pad)
					converted[str(o.Name)] = pad # save as object
			else:
			
				subs.append(s)
				objects.append(o)
			
			index = index + 1
		
		# remove object but after all subs conversion 
		# because second sub might be also from the same box panel
		for o in boxObjects:
			if o.isDerivedFrom("Part::Box"):
				try:
					FreeCAD.ActiveDocument.removeObject(o.Name)
				except:
					skip = 1
		
		FreeCAD.ActiveDocument.recompute()

	return [ subs, objects ]


# ###################################################################################################################
def isType(iObj, iType="Clone"):
	'''
	Description:
	
		This function checks if the given object iObj is iType. 
		It has been created mostly for Clones. The Clones are "Part::FeaturePython" type. 
		But the problem is that many other FreeCAD objects are "Part::FeaturePython" type as well, 
		for example Array. So, you can't recognize the Clones only with .isDerivedFrom() function or 
		even .TypeId. To simplify the code look you can hide the ckecks behind the function.
	
	Args:
	
		iObj: object
		iType: string for type:
			"Clone" - for clones
			"Array" - for BIM or Draft Array

	Usage:
	
		if MagicPanels.isType(o, "Clone"):
			do something ...

	Result:
	
		return True or False, so you can use it directly in if statement

	'''
	
	if iType == "Clone":
		
		if iObj.isDerivedFrom("Part::FeaturePython") and iObj.Name.startswith("Clone"):
			return True
	
		if iObj.isDerivedFrom("Part::Part2DObjectPython") and iObj.Name.startswith("Clone"):
			return True

	if iType == "Array":
		
		if iObj.isDerivedFrom("Part::FeaturePython") and iObj.Name.startswith("Array"):
			return True
		
	return False
	

# ###################################################################################################################
def equal(iA, iB):
	'''
	Description:
	
		At FreeCAD there are many values like 1.000006, especially for PartDesign objects. 
		So if you want to compare such values this sometimes might be True and sometimes False. 
		So, finally I decided to write my own function for comparison.
	
	Args:
	
		iA: float value
		iB: float value

	Usage:
	
		if MagicPanels.equal(1.0006, 1):
			do something ...

	Result:
	
		return True if equal or False if not

	'''
	
	return round(iA, gRoundPrecision) == round(iB, gRoundPrecision)


# ###################################################################################################################
def touchTypo(iObj):
	'''
	Description:
	
		Touch the typo so that the typo-snake does not notice it ;-) LOL
	
	Args:
	
		iObj: object to touch

	Usage:
	
		vs = MagicPanels.touchTypo(o)

	Result:
	
		return Vertex + es for object o

	'''
	
	return getattr(iObj, "Vertex"+"es")


# ###################################################################################################################
def normalizeBoundBox(iBoundBox):
	'''
	Description:
	
		Return normalized version of BoundBox. All values 0.01 will be rounded 
		allowing comparison, and searches for the same face or edge.
	
	Args:
	
		iBoundBox: directly pass BoundBox object

	Usage:
	
		e1 = obj1.Shape.Edges[0]
		e2 = obj2.Shape.Edges[0]

		b1 = MagicPanels.normalizeBoundBox(e1.BoundBox)
		b2 = MagicPanels.normalizeBoundBox(e2.BoundBox)

	Result:
	
		return normalized version for comparison if b1 == b2: you can set your own precision here

	'''

	b = "BoundBox ("
	b += str(int(round(iBoundBox.XMin, 0))) + ", "
	b += str(int(round(iBoundBox.YMin, 0))) + ", "
	b += str(int(round(iBoundBox.ZMin, 0))) + ", "
	b += str(int(round(iBoundBox.XMax, 0))) + ", "
	b += str(int(round(iBoundBox.YMax, 0))) + ", "
	b += str(int(round(iBoundBox.ZMax, 0)))
	b += ")"
	
	return b


# ###################################################################################################################
'''
# References
'''
# ###################################################################################################################


# ###################################################################################################################
def getReference(iObj="none"):
	'''
	Description:
	
		Gets reference to the selected or given object.
	
	Args:
	
		iObj (optional): object to get reference (to return base object)
	
	Usage:
	
		gObj = MagicPanels.getReference()
		gObj = MagicPanels.getReference(obj)
		
	Result:
	
		gObj - reference to the base object

	'''

	obj = ""
	
	# #####################################
	# selection
	# #####################################
	
	if iObj == "none":
		obj = FreeCADGui.Selection.getSelection()[0]
	else:
		obj = iObj

	# #####################################
	# object types 
	# #####################################
	
	# Cube
	if obj.isDerivedFrom("Part::Box"):
		return obj
	
	# normal Pad
	if obj.isDerivedFrom("PartDesign::Pad") and obj.BaseFeature == None:
		return obj
	
	# not search for Sketch reference
	if obj.isDerivedFrom("Sketcher::SketchObject"):
		return obj

	# try to find the base in Part::Cut
	if obj.isDerivedFrom("Part::Cut"):
		
		try:
			i = 0
			while i < gSearchDepth:
				obj = obj.Base
				
				if obj.isDerivedFrom("Part::Box"):
					return obj
				
				i = i + 1
		except:
			skip = 1
		
		return obj

	# try to unpack base object for other objects
	try:
		depth = len(obj.OutListRecursive)
		
		if  depth == 0:
			return obj
		
		else:
			i = 0
			while i < depth and i < gSearchDepth:
				
				if obj.isDerivedFrom("Part::Cut"):
					index = i
				else:
					index = depth - 1 - i

				base = obj.OutListRecursive[index]
				
				if (
					base.isDerivedFrom("Part::Box") or 
					(base.isDerivedFrom("PartDesign::Pad") and str(base.Name).find("Tenon") == -1)
					):
					return base
				else:
					i = i + 1
	except:
		skip = 1

	# not recognized
	if obj != "":
		return obj
	
	return -1


# ###################################################################################################################
def getBody(iObj):
	'''
	Description:
	
		Return Body for given object.
	
	Args:
	
		iObj: object to get Body

	Usage:
	
		body = MagicPanels.getBody(sketch)

	Result:
	
		Return body object or empty string if there is no Body

	'''


	try:
		return iObj._Body
	except:
		skip = 1
	
	containers = getContainers(iObj)
	 
	if len(containers) > 0:
		o = containers[0]
		if o.isDerivedFrom("PartDesign::Body"):
			return o

	return ""


# ###################################################################################################################
'''
# Sizes
'''
# ###################################################################################################################



# ###################################################################################################################
def getSizesFromVertices(iObj):
	'''
	Description:
	
		Gets occupied space by the object from vertices.
	
	Args:
	
		iObj: object
	
	Usage:
	
		[ sx, sy, sz ] = MagicPanels.getSizesFromVertices(obj)

	Result:
	
		Returns array with [ mX, mY, mZ ] where: 
		mX - occupied space along X axis
		mY - occupied space along Y axis
		mZ - occupied space along Z axis

	'''

	init = 0
	
	minX = 0
	minY = 0
	minZ = 0

	maxX = 0
	maxY = 0
	maxZ = 0

	vs = getattr(iObj.Shape, "Vertex"+"es")

	for v in vs:
		
		[ x, y, z ] = [ v.X, v.Y, v.Z ]
		
		if init == 0:
			[ minX, minY, minZ ] = [ x, y, z ]
			[ maxX, maxY, maxZ ] = [ x, y, z ]
			init = 1
		
		if x > maxX:
			maxX = x
		
		if y > maxY:
			maxY = y

		if z > maxZ:
			maxZ = z

		if x < minX:
			minX = x

		if y < minY:
			minY = y

		if z < minZ:
			minZ = z
		
	s1 = getVertexAxisCross(minX, maxX)
	s2 = getVertexAxisCross(minY, maxY)
	s3 = getVertexAxisCross(minZ, maxZ)

	mX = round(s1, gRoundPrecision)
	mY = round(s2, gRoundPrecision)
	mZ = round(s3, gRoundPrecision)
	
	return [ mX, mY, mZ ]


# ###################################################################################################################
def getSizesFromBoundBox(iObj):
	'''
	Description:
	
		Gets occupied space by the object from BoundBox. This can be useful for round shapes, 
		where is no vertices at object edges, e.g. cylinders, circle at Sketch.
	
	Args:
	
		iObj: object
	
	Usage:
	
		[ sx, sy, sz ] = MagicPanels.getSizesFromBoundBox(obj)

	Result:
	
		Returns array with [ mX, mY, mZ ] where: 
		mX - occupied space along X axis
		mY - occupied space along Y axis
		mZ - occupied space along Z axis

	'''


	mX = round(iObj.Shape.BoundBox.XLength, gRoundPrecision)
	mY = round(iObj.Shape.BoundBox.YLength, gRoundPrecision)
	mZ = round(iObj.Shape.BoundBox.ZLength, gRoundPrecision)
	
	return [ mX, mY, mZ ]



# ###################################################################################################################
def getOccupiedSpace(iObjects):
	'''
	Description:
	
		Function to get occupied space by many objects. 
	
	Args:
	
		iObjects: array with objects
	
	Usage:
	
		[ minX, minY, minZ, maxX, maxY, maxZ, [ cx, cy, cz ]] = MagicPanels.getOccupiedSpace(objects)

	Result:
	
		Returns array: 
		minX - minimum value of the X-axis coordinates for the occupied space
		minY - minimum value of the Y-axis coordinates for the occupied space
		minZ - minimum value of the Z-axis coordinates for the occupied space
		maxX - maximum value of the X-axis coordinates for the occupied space
		maxY - maximum value of the Y-axis coordinates for the occupied space
		maxZ - maximum value of the Z-axis coordinates for the occupied space
		center - array with:
			cx - X float of the occupied space by all objects
			cy - Y float of the occupied space by all objects
			cz - Z float of the occupied space by all objects

	'''

	
	init = 0

	minX = 0
	minY = 0
	minZ = 0

	maxX = 0
	maxY = 0
	maxZ = 0

	mX = 0
	mY = 0
	mZ = 0

	for o in iObjects:
		
		try:
			
			vs = getattr(o.Shape, "Vertex"+"es")
			
			for v in vs:
				
				[ x, y, z ] = [ v.X, v.Y, v.Z ]
		
				if init == 0:
					[ minX, minY, minZ ] = [ x, y, z ]
					[ maxX, maxY, maxZ ] = [ x, y, z ]
					init = 1
				
				if x > maxX:
					maxX = x
				
				if y > maxY:
					maxY = y

				if z > maxZ:
					maxZ = z

				if x < minX:
					minX = x

				if y < minY:
					minY = y

				if z < minZ:
					minZ = z

		except:
			skip = 1

	cx = minX + ( abs(maxX - minX) / 2 )
	cy = minY + ( abs(maxY - minY) / 2 )
	cz = minZ + ( abs(maxZ - minZ) / 2 )
	
	return [ minX, minY, minZ, maxX, maxY, maxZ, [ cx, cy, cz ]]


# ###################################################################################################################
def getSizesFromSketch(iSketch):
	'''
	Description:
	
		Allows to get sizes for Sketch. If the iSketch object has defined SizeX and SizeY constraints the 
		array with those values will be returned. If there is no SizeX and SizeY constraints this function will try 
		to get iSketch size in other way.
	
	Args:
	
		iSketch: sketch object to get sizes

	Usage:
	
		[ SizeX, SizeY ] = MagicPanels.getSizesFromSketch(sketch)

	Result:
	
		Returns array with floats [ SizeX, SizeY ]

	'''
	
	
	# define as string first, not as 0
	SizeX = ""
	SizeY = ""
	
	# try get values from named constraints
	try:
		constraints = iSketch.Constraints
		for c in constraints:
			if c.Name == "SizeX":
				SizeX = c.Value
			if c.Name == "SizeY":
				SizeY = c.Value
	except:
		skip = 1
	
	# get first dimensions (this may not work for non-rectangle shapes)
	if SizeX == "" or SizeY == "":
		try:
			if len(iSketch.Shape.OrderedEdges) == 4:
				SizeX = iSketch.Shape.OrderedEdges[0].Length
				SizeY = iSketch.Shape.OrderedEdges[1].Length
		except:
			skip = 1

	# try to get dimensions from sketch BoundBox
	# vertices not works in case of rounded edges so prefer this way first
	if SizeX == "" or SizeY == "":
		try:
			sizes = getSizesFromBoundBox(iSketch)
			sizes.sort()
			SizeX = sizes[1]
			SizeY = sizes[2]
		except:
			skip = 1

	# try to get shape size from vertices
	# however in case of rounded edges this will not be fine
	if SizeX == "" or SizeY == "":
		try:
			sizes = getSizesFromVertices(iSketch)
			sizes.sort()
			SizeX = sizes[1]
			SizeY = sizes[2]
		except:
			skip = 1
	
	# prevent tools error and return 0 if there is no size
	if SizeX == "" or SizeY == "":
		return [ 0, 0 ]
	else:
		return [ SizeX, SizeY ]


# ###################################################################################################################
def getSizes(iObj):
	'''
	Description:
	
		Allows to get sizes for object (iObj), according to the object type. 
		The values are not sorted.
	
	Args:
	
		iObj: object to get sizes

	Usage:
	
		[ size1, size2, size3 ] = MagicPanels.getSizes(obj)

	Result:
	
		Returns [ Length, Width, Height ] for Cube.

	'''


	if iObj.isDerivedFrom("Part::Box"):
		return [ iObj.Length.Value, iObj.Width.Value, iObj.Height.Value ]

	if iObj.isDerivedFrom("PartDesign::Pad"):
		[ sizeX, sizeY ] = getSizesFromSketch(iObj.Profile[0])
		return [ sizeX, sizeY, iObj.Length.Value ]

	if iObj.isDerivedFrom("Part::Extrusion"):
		[ sizeX, sizeY ] = getSizesFromSketch(iObj.Base)
		
		length = abs(iObj.LengthFwd.Value)
		if equal(length, 0):
			length = abs(iObj.LengthRev.Value)

		return [ sizeX, sizeY, length ]
		
	if iObj.isDerivedFrom("Part::Cylinder"):
		return [ 1, 1, 1 ]

	if iObj.isDerivedFrom("Part::Cone"):
		return [ 1, 1, 1 ]
	
	if iObj.isDerivedFrom("PartDesign::Thickness"):
		[ sizeX, sizeY ] = getSizesFromSketch(iObj.Base[0].Profile[0])
		return [ sizeX, sizeY, iObj.Base[0].Length.Value ]

	if iObj.isDerivedFrom("Sketcher::SketchObject"):
		[ sizeX, sizeY ] = getSizesFromSketch(iObj)
		return [ sizeX, sizeY, 0 ]
	
	# for custom objects
	try:
		return [ iObj.Base_Width.Value, iObj.Base_Height.Value, iObj.Base_Length.Value ]
	except:
		skip = 1
	
	# try to get sizes from vertices
	try:
		[ sx, sy, sz ] = getSizesFromVertices(iObj)
		return [ sx, sy, sz ]
	except:
		skip = 1
	
	# if nothing was successful, return 100 to move all furniture quickly
	return [ 100, 100, 100 ]


# ###################################################################################################################
'''
# Copy
'''
# ###################################################################################################################


# ###################################################################################################################
def copyPanel(iObjects, iType="auto"):
	'''
	Description:
	
		This function has been created for magicMove tool to copy any object type.

	Args:
	
		iObjects: array with objects to copy
		iType (optional): copy type:
			* "auto" - if the object is Cube it will be copyObject, otherwise Clone will be used to copy
			* "copyObject" - force copyObject copy type, however not use at LinkGroup because it will be visible as single object if you remove the copy the base LinkGroup will be removed as well, and the copy will not be visible at cut-list report
			* "Clone" - force Clone copy type, if you make Clone from Pad and the Pad has Sketch.AttachmentOffset the Clone has Placement set to XYZ (0,0,0) but is not in the zero position so you have to remove Sketch offset from the Clone, I guess the BoundBox is the correct solution here
			* "Link" - force Link copy type, it is faster than Clone but sometimes might be broken

	Usage:
	
		copies = MagicPanels.copyPanel([ o ])
		copies = MagicPanels.copyPanel([ o ], "auto")
		copies = MagicPanels.copyPanel([ o ], "copyObject")
		copies = MagicPanels.copyPanel([ o ], "Clone")
		copies = MagicPanels.copyPanel([ o ], "Link")
		copy = MagicPanels.copyPanel([ o ], "auto")[0]
		copy = MagicPanels.copyPanel([ o ])[0]

	Result:
	
		return array with copies
	'''

	
	copies = []
	copy = ""
	
	for o in iObjects:
		
		if iType == "auto":
			
			if o.isDerivedFrom("Part::Box"):
				copy = FreeCAD.ActiveDocument.copyObject(o)
				copy.Label = getNestingLabel(o, "Copy")
			else:
				import Draft
				copy = Draft.make_clone(o)
				copy.Label = getNestingLabel(o, "Clone")
		
		if iType == "copyObject":
			copy = FreeCAD.ActiveDocument.copyObject(o)
			copy.Label = getNestingLabel(o, "Copy")
		
		if iType == "Clone":
			import Draft
			copy = Draft.make_clone(o)
			copy.Label = getNestingLabel(o, "Clone")
		
		if iType == "Link":
			copy = FreeCAD.ActiveDocument.addObject('App::Link', "Link")
			copy.setLink(o)
			copy.Label = str(o.Label)
			copy.Label = getNestingLabel(o, "Link")
		
		if iType == "Array":
			import Draft
			vx = FreeCAD.Vector(800.0, 0.0, 0.0)
			vy = FreeCAD.Vector(0.0, 100.0, 0.0)
			vz = FreeCAD.Vector(0.0, 0.0, 100.0)
			copy = Draft.make_ortho_array(o, vx, vy, vz, 5, 1, 1, True)
			copy.Fuse = False
			Draft.autogroup(copy)
			copy.Label = getNestingLabel(o, "Array")
		
		# if copy was successful
		try:
			copy.recompute()
		except:
			skip = 1
	
		# if copy was successful
		try:
			copies.append(copy)
		except:
			skip = 1
		
	return copies


# ###################################################################################################################
def getObjectToCopy(iObj):
	'''
	Description:
	
		This function returns object to copy.
	
	Args:
	
		iObj: object to get reference to copy

	Usage:
	
		toCopy = MagicPanels.getObjectToCopy(o)

	Result:
	
		For example: 

		for Cube: always returns Cube
		for Pad: always returns Body
		for PartDesign objects: try to return Body
		for Body returns Body
		for LinkGroup: returns LinkGroup
		for Cut: returns Cut
		for Clones: returns Clone
		for Links: returns Link
		for any other object: returns object

	'''


	if (
		iObj.isDerivedFrom("Part::Box") or 
		iObj.isDerivedFrom("App::LinkGroup") or 
		iObj.isDerivedFrom("PartDesign::Body") or 
		iObj.isDerivedFrom("Part::Cut") 
		):
		return iObj

	elif iObj.isDerivedFrom("PartDesign::Pad"):
		return iObj._Body

	elif isType(iObj, "Clone") or iObj.isDerivedFrom("App::Link"):
		return iObj
		
		# currently will be the same Clone or Link
		# to avoid global position problem and 
		# multi loop reference
		'''
		oRef = getReference(iObj)
		
		if oRef.isDerivedFrom("Part::Box"):
			return oRef
		else:
			try:
				toCopy = iObj._Body
				return toCopy
			except:
				skip = 1
		'''
		
	else:
		
		try:
			iObj = iObj._Body
		except:
			skip = 1

	return iObj


# ###################################################################################################################
'''
# Edges
'''
# ###################################################################################################################


# ###################################################################################################################
def getEdgeVertices(iEdge):
	'''
	Description:
	
		Gets all vertices values for edge.
	
	Args:
	
		iEdge: edge object

	Usage:
	
		[ v1, v2 ] = MagicPanels.getEdgeVertices(gEdge)

	Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 1, 1, 1 ] ].

	'''
	
	vertexArr = touchTypo(iEdge)

	v1 = [ vertexArr[0].X, vertexArr[0].Y, vertexArr[0].Z ]
	v2 = [ vertexArr[1].X, vertexArr[1].Y, vertexArr[1].Z ]

	return [ v1, v2 ]


# ###################################################################################################################
def getEdgeVectors(iEdge):
	'''
	Description:
	
		Gets all vertices values for edge as FreeCAD.Vector array.
	
	Args:
	
		iEdge: edge object

	Usage:
	
		[ v1, v2 ] = MagicPanels.getEdgeVectors(edge)

	Result:
	
		Return vertices array like [ FreeCAD.Vector, FreeCAD.Vector ].

	'''
	
	vertexArr = touchTypo(iEdge)

	v1 = FreeCAD.Vector( vertexArr[0].X, vertexArr[0].Y, vertexArr[0].Z )
	v2 = FreeCAD.Vector( vertexArr[1].X, vertexArr[1].Y, vertexArr[1].Z )

	return [ v1, v2 ]


# ###################################################################################################################
def getEdgeNormalized(iV1, iV2):
	'''
	Description:
	
		Returns vertices with exact sorted order V1 > V2, mostly used 
		to normalize Pad vertices.
	
	Args:
	
		iV1: array with vertices e.g. [ 1, 1, 1 ]
		iV2: array with vertices e.g. [ 2, 2, 2 ]
	
	Usage:
	
		[ v1, v2 ] = MagicPanels.getEdgeNormalized(v1, v2)
		
	Result:
	
		for vertices [ 2, 2, 2 ], [ 1, 1, 1 ] return [ 1, 1, 1 ], [ 2, 2, 2 ]

	'''

	# edge along X
	if not equal(iV1[0], iV2[0]):
		if iV1[0] > iV2[0]:
			return [ iV1, iV2 ]
		else:
			return [ iV2, iV1 ]
			
	# edge along Y
	if not equal(iV1[1], iV2[1]):
		if iV1[1] > iV2[1]:
			return [ iV1, iV2 ]
		else:
			return [ iV2, iV1 ]
			
	# edge along Z
	if not equal(iV1[2], iV2[2]):
		if iV1[2] > iV2[2]:
			return [ iV1, iV2 ]
		else:
			return [ iV2, iV1 ]
		
	return [ iV1, iV2 ]


# ###################################################################################################################
def getEdgeIndex(iObj, iEdge):
	'''
	Description:
	
		Returns edge index for given object and edge.
	
	Args:
	
		iObj: object of the edge
		iEdge: edge object

	Usage:
	
		edgeIndex = MagicPanels.getEdgeIndex(gObj, gEdge)

	Result:
	
		return int value for edge

	'''

	index = 1
	for e in iObj.Shape.Edges:
		if str(e.BoundBox) == str(iEdge.BoundBox):
			return index

		index = index + 1
	
	return -1


# ###################################################################################################################
def getEdgeIndexByKey(iObj, iBoundBox):
	'''
	Description:
	
		Returns edge index for given edge BoundBox.
	
	Args:
	
		iObj: object of the edge
		iBoundBox: edge BoundBox as key

	Usage:
	
		edgeIndex = MagicPanels.getEdgeIndex(o, key)

	Result:
	
		return int value for edge

	'''

	index = 1
	for e in iObj.Shape.Edges:
		
		if normalizeBoundBox(e.BoundBox) == normalizeBoundBox(iBoundBox):
			return index

		index = index + 1
	
	return -1


# ###################################################################################################################
def getEdgePlane(iObj, iEdge, iType="auto"):
	'''
	Description:
	
		Returns orientation for the edge, changed axis, as "X", "Y" or "Z".
	
	Args:
	
		iObj: object with the edge
		iEdge: edge object
		iType:
			* "auto" - check if panel is rotated and get edge plane from its base not rotated position
			* "clean" - return plane for current edge position

	Usage:
	
		plane = MagicPanels.getEdgePlane(o, edge)

	Result:
	
		return string "X", "Y" or "Z".

	'''

	o = getReference(iObj)
	
	if iType == "auto":
		
		rotated = False
		if isRotated(o):
			
			import Part, math
		
			rotated = True
			w = Part.Wire(iEdge)
			wire = Part.show(w)
			wire.Label = "wire"
			
			offset = ""
			
			if o.isDerivedFrom("PartDesign::Pad"):
				
				ref = o.Profile[0].Placement
				try:
					support = o.Profile[0].Support[0][0]
				except:
					support = o.Profile[0].AttachmentSupport[0][0]
				
				if support.Label.startswith("XZ"):
					offset = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 90)
					
				if support.Label.startswith("YZ"):
					offset = FreeCAD.Rotation(FreeCAD.Vector(0.58, 0.58, 0.58), 120)

			else:
				ref = o.Placement

			wire.Placement.Rotation = ref.Rotation
			wire.Placement.Rotation.Angle = - wire.Placement.Rotation.Angle
			FreeCAD.ActiveDocument.recompute()

			[ v1, v2 ] = getEdgeVertices(wire.Shape)
		
		else:

			[ v1, v2 ] = getEdgeVertices(iEdge)
	
	if iType == "clean":
		[ v1, v2 ] = getEdgeVertices(iEdge)
	
	plane = ""
	if not equal(v1[0], v2[0]):
		plane = "X"

	if not equal(v1[1], v2[1]):
		plane = "Y"

	if not equal(v1[2], v2[2]):
		plane = "Z"

	if iType == "auto" and rotated == True:
		FreeCAD.ActiveDocument.removeObject(wire.Name)
		FreeCAD.ActiveDocument.recompute()

	return plane


# ###################################################################################################################
def getSizeByEdge(iObj, iEdge):
	'''
	Description:
	
		Returns iObj property (objects field name) to change for iEdge. 
	
	Args:
	
		iObj: object with the edge
		iEdge: edge object

	Usage:
	
		name = MagicPanels.getSizeByEdge(o, edge)

	Result:
	
		For Cube (Part::Box) object returns string "Length", "Width" or "Height".

	'''

	#oplane = getDirection(iObj)
	eplane = getEdgePlane(iObj, iEdge)
	
	if eplane == "X":
		return "Length"
		
	if eplane == "Y":
		return "Width"
	
	if eplane == "Z":
		return "Height"


# ###################################################################################################################
'''
# Faces
'''
# ###################################################################################################################


# ###################################################################################################################
def getFaceIndex(iObj, iFace):
	'''
	Description:
	
		Returns face index for given object and face.
	
	Args:
	
		iObj: object of the face
		iFace: face object

	Usage:
	
		faceIndex = MagicPanels.getFaceIndex(gObj, gFace)

	Result:
	
		return int value for face

	'''

	index = 1
	for f in iObj.Shape.Faces:
		if str(f.BoundBox) == str(iFace.BoundBox):
			return index

		index = index + 1
	
	return -1


# ###################################################################################################################
def getFaceIndexByKey(iObj, iBoundBox):
	'''
	Description:
	
		Returns face index for given face BoundBox.
	
	Args:
	
		iObj: object of the face
		iBoundBox: face BoundBox as key

	Usage:
	
		faceIndex = MagicPanels.getFaceIndexByKey(o, key)

	Result:
	
		return int value for face

	'''

	index = 1
	for f in iObj.Shape.Faces:
		
		if normalizeBoundBox(f.BoundBox) == normalizeBoundBox(iBoundBox):
			return index

		index = index + 1
	
	return -1


# ###################################################################################################################
def getFaceVertices(iFace, iType="4"):
	'''
	Description:
	
		Gets all vertices values for face.
	
	Args:
	
		iFace: face object
		iType (optional): 
			* "4" - 4 vertices for normal Cube
			* "all" - get all vertices, for example for Cut object
			* "vector" - get all vertices as FreeCAD.Vector objects

	Usage:
	
		[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(gFace)
		vertices = MagicPanels.getFaceVertices(gFace, "all")
		vectors = MagicPanels.getFaceVertices(face, "vector")

	Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 2, 2, 2 ], [ 3, 3, 3 ], [ 4, 4, 4 ] ]

	'''
	
	
	vertexArr = touchTypo(iFace)

	if iType == "4":
		
		v1 = [ vertexArr[0].X, vertexArr[0].Y, vertexArr[0].Z ]
		v2 = [ vertexArr[1].X, vertexArr[1].Y, vertexArr[1].Z ]
		v3 = [ vertexArr[2].X, vertexArr[2].Y, vertexArr[2].Z ]
		v4 = [ vertexArr[3].X, vertexArr[3].Y, vertexArr[3].Z ]
		
		return [ v1, v2, v3, v4 ]
	
	if iType == "all":
		
		vertices = []
		for v in vertexArr:
			vertices.append([ v.X, v.Y, v.Z ])
		
		return vertices
	
	if iType == "vector":
		
		vertices = []
		for v in vertexArr:
			vertices.append(FreeCAD.Vector(v.X, v.Y, v.Z))
		
		return vertices
	
	return ""


# ###################################################################################################################
def getFaceType(iObj, iFace):
	'''
	Description:
	
		Gets face type, if this is "edge" or "surface".
	
	Args:
	
		iObj: object where is the face
		iFace: face object

	Usage:
	
		faceType = MagicPanels.getFaceType(gObj, gFace)

	Result:
	
		Return string "surface" or "edge".

	'''
	
	sizes = []
	sizes = getSizes(iObj)
	sizes.sort()
	
	t = int(sizes[0])
	
	for e in iFace.Edges:
		if int(e.Length) == t:
			return "edge"
			
	return "surface"
	

# ###################################################################################################################
def getFaceEdges(iObj, iFace):
	'''
	Description:
	
		Gets all edges for given face grouped by sizes.
	
	Args:
	
		iObj: object where is the face
		iFace: face object

	Usage:
	
		[ faceType, arrAll, arrThick, arrShort, arrLong ] = MagicPanels.getFaceEdges(gObj, gFace)

	Result:
	
		Return arrays like [ faceType, arrAll, arrThick, arrShort, arrLong ] with edges objects, 
		
		faceType - string "surface" or "edge"
		arrAll - array with all edges
		arrThick - array with the thickness edges
		arrShort - array with the short edges (if type is edge this will be the same as arrThick)
		arrLong - array with the long edges

	'''
	
	sizes = []
	sizes = getSizesFromVertices(iObj)
	sizes.sort()
	
	t = int(sizes[0])
	s = int(sizes[1])
	l = int(sizes[2])
	
	arrAll = [ ]
	arrThick = []
	arrShort = []
	arrLong = []
	
	for e in iFace.Edges:
		
		if not e.Curve.isDerivedFrom("Part::GeomLine"):
			continue
		
		arrAll.append(e)
		
		if int(e.Length) == t:
			arrThick.append(e)
			
		if int(e.Length) != t and int(e.Length) <= s:
			arrShort.append(e)
			
		if int(e.Length) != t and int(e.Length) > s:
			arrLong.append(e)
	
	if len(arrThick) == len(arrAll) / 2:
		faceType = "edge"
	else:
		faceType = "surface"
	
	return [ faceType, arrAll, arrThick, arrShort, arrLong ]


# ###################################################################################################################
def getFacePlane(iFace):
	'''
	Description:
	
		Gets face plane in notation "XY", "XZ", "YZ". 

	Args:
	
		iFace: face object

	Usage:
	
		plane = MagicPanels.getFacePlane(face)

	Result:
	
		string "XY", "XZ", or "YZ".
		
	'''

	[ v1, v2, v3, v4 ] = getFaceVertices(iFace)

	# if Z axis not change
	if equal(v1[2] + v2[2] + v3[2] + v4[2], 4 * v1[2]):
		return "XY"
	
	# if Y axis not change
	if equal(v1[1] + v2[1] + v3[1] + v4[1], 4 * v1[1]):
		return "XZ"
	
	# if X axis not change
	if equal(v1[0] + v2[0] + v3[0] + v4[0], 4 * v1[0]):
		return "YZ"

	return ""


# ###################################################################################################################
def getFaceSink(iObj, iFace):
	'''
	Description:
	
		Gets face sink axis direction in notation "+", or "-".

	Args:
	
		iObj: object with the face
		iFace: face object

	Usage:
	
		sink = MagicPanels.getFaceSink(obj, face)

	Result:
	
		string "+" if the object at face should go along axis forward, 
		or "-" if the object at face should go along axis backward

	'''

	inside = True

	plane = getFacePlane(iFace)
	[ x, y, z ] = iFace.CenterOfMass
	
	if plane == "XY":
		v = FreeCAD.Vector(x, y, z + 1)
		inside = iObj.Shape.BoundBox.isInside(v)
		
	if plane == "XZ":
		v = FreeCAD.Vector(x, y + 1, z)
		inside = iObj.Shape.BoundBox.isInside(v)
		
	if plane == "YZ":
		v = FreeCAD.Vector(x + 1, y, z)
		inside = iObj.Shape.BoundBox.isInside(v)
	
	if inside == True:
		return "+"
	else:
		return "-"


# ###################################################################################################################
def getFaceObjectRotation(iObj, iFace):
	'''
	Description:
	
		Gets face object rotation to apply to the new created object at face. 
		Object created at face with this rotation should be up from the face.

	Args:
	
		iObj: object with the face
		iFace: face object

	Usage:
	
		r = MagicPanels.getFaceObjectRotation(obj, face)

	Result:
	
		FreeCAD.Rotation object that can be directly pass to the setPlacement or object.Placement

	'''

	plane = getFacePlane(iFace)
	sink = getFaceSink(iObj, iFace)
	
	if sink == "+":
				
		if plane == "XY":
			r = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 180)
			
		if plane == "XZ":
			r = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 90)

		if plane == "YZ":
			r = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), 270)

	else:
	
		if plane == "XY":
			r = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 0)
			
		if plane == "XZ":
			r = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 270)

		if plane == "YZ":
			r = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), 90)
	
	return r


# ###################################################################################################################
def getFaceDetails(iObj, iFace):
	'''
	Description:
	
		Allows to get detailed information for face direction.
	
	Args:
	
		iObj: selected object
		iFace: selected face object

	Usage:
	
		[ plane, type ] = MagicPanels.getFaceDetails(gObj, gFace)

	Result:
	
		[ "XY", "surface" ] - if the direction is XY and it is surface, no thickness edge
		[ "XY", "edge" ] - if the direction is XY and it is edge, there is thickness edge
		[ "XY", "equal" ] - if the direction is XY and both edges are equal
		
		# > [!NOTE]
		# > The first argument can be "XY", "YX", "XZ", "ZX", "YZ", "ZY". 
		# > This is related to face not to object. The object direction will be different.
		
	'''

	[ v1, v2, v3, v4 ] = getFaceVertices(iFace)

	direction = ""
	
	if int(v1[2] + v2[2] + v3[2] + v4[2]) == int(4 * v1[2]):
		direction = "XY"
	
	if int(v1[1] + v2[1] + v3[1] + v4[1]) == int(4 * v1[1]):
		direction = "XZ"
	
	if int(v1[0] + v2[0] + v3[0] + v4[0]) == int(4 * v1[0]):
		direction = "YZ"

	s = getSizes(iObj)
	s.sort()
	thick = int(s[0])
	
	e1 = int(iFace.Edges[0].Length)
	e2 = int(iFace.Edges[1].Length)
	e3 = int(iFace.Edges[2].Length)
	e4 = int(iFace.Edges[3].Length)
	
	ed = int(iFace.Edges[0].Length + iFace.Edges[1].Length + iFace.Edges[2].Length + iFace.Edges[3].Length)
	
	if ed == int(4 * e1):
		return [ direction, "equal" ]
	
	if iObj.isDerivedFrom("Part::Box"):
		
		if direction == "XY" and e1 < e2:
			if e1 == thick or e2 == thick:
				return [ "XY", "edge" ]
			else:
				return [ "XY", "surface" ]

		if direction == "XY" and e1 > e2:
			if e1 == thick or e2 == thick:
				return [ "YX", "edge" ]
			else:
				return [ "YX", "surface" ]

		if direction == "XZ" and e1 > e2:
			if e1 == thick or e2 == thick:
				return [ "XZ", "edge" ]
			else:
				return [ "XZ", "surface" ]

		if direction == "XZ" and e1 < e2:
			if e1 == thick or e2 == thick:
				return [ "ZX", "edge" ]
			else:
				return [ "ZX", "surface" ]

		if direction == "YZ" and e1 < e2:
			if e1 == thick or e2 == thick:
				return [ "YZ", "edge" ]
			else:
				return [ "YZ", "surface" ]

		if direction == "YZ" and e1 > e2:
			if e1 == thick or e2 == thick:
				return [ "ZY", "edge" ]
			else:
				return [ "ZY", "surface" ]

	else:
		
		return [ "not supported", "not supported" ]


# ###################################################################################################################
def getFaceToCube(iFace, iDepth, iOffset=0):
	'''
	Description:
	
		Create dimensions for simple cube Part::Box object which cover the face with offset.
		
		# > [!NOTE]
		# > The dimensions are for XY panel without rotation. So if you want to replace 
		# > such object later you need correct rotation in base object.
		
	Args:
	
		iFace: face object
		iDepth: size into face direction
		iOffset: additional offset:
			* if > 0: the cube will be bigger with the offset from each side
			* if < 0: the cube will be smaller with the offset from each side
			* if == 0: the cube will be same size as face

	Usage:
	
		objThick = 100
		tenonOffset = - objThick / 4
		tenonDepth = 2 * objThick
		[ Length, Width, Height ] = MagicPanels.getFaceToCube(face, tenonDepth, tenonOffset)

	Result:
	
		return array with the dimensions as face with iOffset and iDepth in order:
		[ Length, Width, Height ] so it can be directly assigned to XY panel

	'''


	plane = getFacePlane(iFace)
	
	if plane == "XY":
		SizeX = iFace.BoundBox.XLength + (2 * iOffset)
		SizeY = iFace.BoundBox.YLength + (2 * iOffset)
		SizeZ = iDepth
	
	if plane == "XZ":
		SizeX = iFace.BoundBox.XLength + (2 * iOffset)
		SizeY = iDepth
		SizeZ = iFace.BoundBox.ZLength + (2 * iOffset)
		
	if plane == "YZ":
		SizeX = iDepth
		SizeY = iFace.BoundBox.YLength + (2 * iOffset)
		SizeZ = iFace.BoundBox.ZLength + (2 * iOffset)
	
	return [ SizeX, SizeY, SizeZ ]


# ###################################################################################################################
'''
# Vertices
'''
# ###################################################################################################################


# ###################################################################################################################
def vertices2vectors(iVertices):
	'''
	Description:
	
		Converts vertices into vector objects.
	
	Args:
	
		iVertices: array with vertices

	Usage:
	
		vertices = MagicPanels.touchTypo(obj.Shape)
		vectors = MagicPanels.vertices2vectors(vertices)

	Result:
	
		return array with vectors
	'''
	
	
	vectors = []
	for v in iVertices:
		vectors.append( FreeCAD.Vector(float(v.X), float(v.Y), float(v.Z)) )
	
	return vectors


# ###################################################################################################################
def showVertex(iVertices, iRadius=20, iColor="red"):
	'''
	Description:
	
		Create sphere at given vertices, to show where are the points for debug purposes.
	
	Args:
	
		iVertices: array with Vertex or floats objects
		iRadius (optional): ball Radius
		iColor: string "red", "green", "blue", or color tuple like (1.0, 1.0, 1.0, 1.0)

	Usage:
	
		MagicPanels.showVertex([ obj.Shape.CenterOfMass ])
		MagicPanels.showVertex([ obj.Shape.CenterOfMass ], 30, "green")
		MagicPanels.showVertex([ obj.Shape.CenterOfMass ], 30, (1.0, 1.0, 1.0, 1.0))
		
	Result:
	
		remove old vertices and show new ones, return array of objects, spheres
	'''
	
	try:
		for o in FreeCAD.ActiveDocument.Objects:
			if str(o.Label).startswith("showVertex"):
				FreeCAD.ActiveDocument.removeObject(o.Name)
	except:
		skip = 1
	
	vertices = []
	
	for v in iVertices:
		
		if hasattr(v, "X"):
			fv = FreeCAD.Vector(v.X, v.Y, v.Z)
		elif hasattr(v, "x"):
			fv = v
		else:
			fv = FreeCAD.Vector(v[0], v[1], v[2])
		
		FreeCAD.Console.PrintMessage("\n")
		FreeCAD.Console.PrintMessage(fv)
		
		s1 = FreeCAD.ActiveDocument.addObject("Part::Sphere","showVertex")
		s1.Placement = FreeCAD.Placement(FreeCAD.Vector(fv), FreeCAD.Rotation(0, 0, 0))
		s1.Radius = iRadius
		
		if iColor == "red":
			color = (1.0, 0.0, 0.0, 1.0)
		elif iColor == "green":
			color = (0.0, 1.0, 0.0, 1.0)
		elif iColor == "blue":
			color = (0.0, 0.0, 1.0, 1.0)
		else:
			color = iColor
		
		setColor(s1, 0, color, "color")
		
		vertices.append(s1)
		
	FreeCAD.ActiveDocument.recompute()

	return vertices


# ###################################################################################################################
def getVertex(iFace, iEdge, iVertex):
	'''
	Description:
	
		Get vertex values for face, edge and vertex index.
	
	Args:
	
		iFace: face object
		iEdge: edge array index
		iVertex: vertex array index (0 or 1)

	Usage:
	
		[ x, y, z ] = MagicPanels.getVertex(gFace, 0, 1)

	Result:

		Return vertex position.

	'''
	
	vertexArr = touchTypo(iFace.Edges[iEdge])

	return [ vertexArr[iVertex].X, vertexArr[iVertex].Y, vertexArr[iVertex].Z ]


# ###################################################################################################################
def getVertexIndex(iObj, iVertex):
	'''
	Description:
	
		Returns vertex index for given object and vertex object.
	
	Args:
	
		iObj: object of the vertex
		iVertex: vertex object

	Usage:
	
		vertexIndex = MagicPanels.getVertexIndex(o, v)

	Result:
	
		return int value for vertex name, so you can create string Vertex + vertexIndex, 
		or get vertex from vertices array

	'''

	index = 1
	ves = touchTypo(iObj.Shape)
	for v in ves:
		if (
			equal(v.X, iVertex.X) and 
			equal(v.Y, iVertex.Y) and 
			equal(v.Z, iVertex.Z) 
			):
			return index

		index = index + 1
	
	return -1


# ###################################################################################################################
def getVertexAxisCross(iA, iB):
	'''
	Description:
	
		Return difference between iB and iA values with respect of coordinate axes.
	
	Args:
	
		iA: vertex float value
		iB: vertex float value
	
	Usage:
	
		edgeSize = MagicPanels.getVertexAxisCross(v0[0], v1[0])
		
	Result:
	
		Return diff for vertices values.

	'''
	
	if iA >= 0 and iB >= 0 and iB > iA:
		return iB - iA
	if iB >= 0 and iA >= 0 and iA > iB:
		return iA - iB
		
	if iA < 0 and iB >= 0 and iB > iA:
		return abs(iA) + iB
	if iB < 0 and iA >= 0 and iA > iB:
		return abs(iB) + iA

	if iA < 0 and iB <= 0 and iB > iA:
		return abs(iA) - abs(iB)
	if iB < 0 and iA <= 0 and iA > iB:
		return abs(iB) - abs(iA)

	return 0


# ###################################################################################################################
def getVerticesPlane(iV1, iV2):
	'''
	Description:
	
		Gets axes with the same values.
	
	Args:
	
		iV1: array or vector object
		iV2: array or vector object
	
	Usage:
	
		plane = MagicPanels.getVerticesPlane(v1, v2)
		
	Result:
	
		Return plane as "XY", "XZ", "YZ".

	'''

	if equal(iV1[0], iV2[0]) and equal(iV1[1], iV2[1]):
		return "XY"

	if equal(iV1[0], iV2[0]) and equal(iV1[2], iV2[2]):
		return "XZ"
		
	if equal(iV1[1], iV2[1]) and equal(iV1[2], iV2[2]):
		return "YZ"

	return ""


# ###################################################################################################################
def getVectorsPlane(iV1, iV2):
	'''
	Description:
	
		Gets axes with the same values. Same as getEdgePlane but for vectors only.
	
	Args:
	
		iV1: vector object
		iV2: vector object
	
	Usage:
	
		plane = MagicPanels.getVectorsPlane(v1, v2)
		
	Result:
	
		Return plane as "X", "Y", "Z".

	'''


	plane = ""
	if not equal(iV1.x, iV2.x):
		plane += "X"

	if not equal(iV1.y, iV2.y):
		plane += "Y"

	if not equal(iV1.z, iV2.z):
		plane += "Z"

	return plane


# ###################################################################################################################
def setVertexPadding(iObj, iVertex, iPadding, iAxis):
	'''
	Description:
	
		Sets padding offset from given vertex to inside the object.
		Do not use it at getPlacement for Pads. Use 0 vertex instead.
		
		# > [!NOTE]
		# > This need to be improved.
	
	Args:
	
		iObj: object
		iVertex: vertex object FreeCAD.Vector(x, y, z)
		iPadding: value > 0 for making offset
		iAxis: string: "X" or "Y" or "Z"
		
	Usage:
	
		v = getattr(obj.Shape, "Vertex"+"es")[0]
		offsetX = MagicPanels.setVertexPadding(obj, v, 15, "X")
		
	Result:
	
		Return return new position value for given axis.

	'''
	
	if iAxis == "X":
		
		v = FreeCAD.Vector(iVertex.X + iPadding, iVertex.Y, iVertex.Z)
		inside = iObj.Shape.BoundBox.isInside(v)
		
		if inside:
			return iVertex.X + iPadding
		else: 
			return iVertex.X - iPadding
			
	if iAxis == "Y":
		
		v = FreeCAD.Vector(iVertex.X, iVertex.Y + iPadding, iVertex.Z)
		inside = iObj.Shape.BoundBox.isInside(v)
		
		if inside:
			return iVertex.Y + iPadding
		else: 
			return iVertex.Y - iPadding
			
	if iAxis == "Z":
		
		v = FreeCAD.Vector(iVertex.X, iVertex.Y, iVertex.Z + iPadding)
		inside = iObj.Shape.BoundBox.isInside(v)
		
		if inside:
			return iVertex.Z + iPadding
		else: 
			return iVertex.Z - iPadding

	return ""


# ###################################################################################################################
def getOnCurve(iPoint, iCurve):
	'''
	Description:
	
		This function has been created to replace python .index() function. 
		FreeCAD has not rounded float values at Vectors, so if you call 
		iCurve.Shape.getPoints(1)[0].index(vector_of_iPoint) this may not find the index 
		of vector_of_iPoint at the iCurve not because it is not there, but because there is 
		small not rounded difference, for example 0.0000006. So, this function scan the iCurve vectors 
		and compare rounded values to return the index.
	
	Args:
	
		iPoint: Part.Vertex object or FreeCAD.Vector or array of floats like [ x, y, z ]
		iCurve: object that has .getPoints() function, for example Wire, Sketch, Helix, Edge

	Usage:
	
		index = MagicPanels.getOnCurve(v, Sketch)
		
	Result:
	
		Return int value index for iPoint on iCurve.

	'''

	curvePoints = iCurve.Shape.getPoints(1)[0]
	
	skip = 0
	if skip == 0:
		try:
			targetVector = FreeCAD.Vector(iPoint.X, iPoint.Y, iPoint.Z)
			skip = 1
		except:
			skip = 0

	if skip == 0:
		try:
			targetVector = FreeCAD.Vector(iPoint.x, iPoint.x, iPoint.x)
			skip = 1
		except:
			skip = 0
	
	if skip == 0:
		try:
			targetVector = FreeCAD.Vector(iPoint[0], iPoint[1], iPoint[2])
			skip = 1
		except:
			skip = 0

	index = 0
	for v in curvePoints:
		if (
			equal(v.x, targetVector.x) and 
			equal(v.y, targetVector.y) and 
			equal(v.z, targetVector.z) 
			):
			return index
		
		index = index + 1
	
	return -1


# ###################################################################################################################
def getVerticesOffset(iVertices, iObj, iType="array"):
	'''
	Gets iObj offset of all supported containers for vertices iVertices.
	
	Args:
	
		iObj: object to get containers offset
		iVertices: vertices array
		iType:
			"array" - array with floats [ 1, 2, 3 ]
			"vector" - array with FreeCAD.Vector types
		
	Usage:
	
		vertices = MagicPanels.getVerticesOffset(vertices, o, "array")

	Result:
	
		return vertices array with correct container offset

	'''

	vertices = []
	
	[ coX, coY, coZ, coR ] = getContainersOffset(iObj)
	
	for v in iVertices:
		if iType == "array":
			n = [ v[0] + coX, v[1] + coY, v[2] + coZ ]
		else:
			n = FreeCAD.Vector(v.x + coX, v.y + coY, v.z + coZ)
		
		vertices.append(n)
	
	return vertices


# ###################################################################################################################
def getVerticesPosition(iVertices, iObj, iType="auto"):
	'''
	Description:
	
		Gets iVertices 3D position. This function should be used to show or select iVertices with rotation. 
		It calculates all offsets with rotation. But this function should not be used for calculation. 
		Because the vertices at FreeCAD are raw, without containers offset. The vertices at FreeCAD have only 
		AttachmentOffset applied. If you start calculation with rotation, you need to calculate plane correctly.
	
	Args:
	
		iVertices: vertices array
		iObj: object to get containers offset
		iType:
			"auto" - recognize the iVertices elements type
			"array" - each element of iVertices is array with floats [ 1, 2, 3 ]
			"vector" - each element of iVertices is array with FreeCAD.Vector
			"vertex" - each element of iVertices is array with Part.Vertex

	Usage:
	
		[[ x, y, z ]] = MagicPanels.getVerticesPosition([[ x, y, z ]], o, "array")
		vertices = MagicPanels.getVerticesPosition(vertices, o, "vector")
		vertices = MagicPanels.getVerticesPosition(vertices, o)
		
		MagicPanels.showVertex(vertices, 10)

	Result:
	
		return vertices array with correct container offset, with the same type

	'''

	# not unpack mirroring
	if iObj.isDerivedFrom("Part::Mirroring"):
		return iVertices

	# recognize iVertices type
	if iType == "auto":
		
		skip = 0
		
		if skip == 0:
			try:
				test = iVertices[0].X
				iType = "vertex"
				skip = 1
			except:
				skip = 0

		if skip == 0:
			try:
				test = iVertices[0].x
				iType = "vector"
				skip = 1
			except:
				skip = 0
		
		if skip == 0:
			try:
				test = iVertices[0][0]
				iType = "array"
				skip = 1
			except:
				skip = 0

	# convert iVertices to Vector for calculation
	vertices = []
	for v in iVertices:
		
		if iType == "array":
			n = FreeCAD.Vector(v[0], v[1], v[2])
		
		elif iType == "vertex":
			import Part
			n = FreeCAD.Vector(v.X, v.Y, v.Z)

		else:
			n = v
			
		vertices.append(n)
	
	# calculate position
	containers = getContainers(iObj)
	for o in containers:
		
		if (
			o.isDerivedFrom("App::Part") or 
			o.isDerivedFrom("PartDesign::Body") or 
			o.isDerivedFrom("App::LinkGroup") or 
			o.isDerivedFrom("Part::Cut") 
			):
			
			try:
				p = o.Placement
			except:
				continue
			
			i = 0
			for v in vertices:

				n = p.multVec(v)
				vertices[i] = n
				
				i = i + 1

	# convert to the same type as iVertices
	i = 0
	for v in vertices:
		if iType == "array":
			vertices[i] = [ v.x, v.y, v.z ]
				
		elif iType == "vertex":
			vertices[i] = Part.Vertex(v.x, v.y, v.z)
				
		else:
			vertices[i] = v
		
		i = i + 1

	return vertices


# ###################################################################################################################
def removeVerticesPosition(iVertices, iObj, iType="auto"):
	'''
	Description:
	
		Remove iVertices 3D position. This function removes offset calculated with getVerticesPosition.
	
	Args:
	
		iVertices: vertices array
		iObj: object to remove containers offset
		iType:
			"auto" - recognize the iVertices elements type
			"array" - each element of iVertices is array with floats [ 1, 2, 3 ]
			"vector" - each element of iVertices is array with FreeCAD.Vector
			"vertex" - each element of iVertices is array with Part.Vertex

	Usage:
	
		[[ x, y, z ]] = MagicPanels.removeVerticesPosition([[ x, y, z ]], o, "array")
		vertices = MagicPanels.removeVerticesPosition(vertices, o, "vector")
		vertices = MagicPanels.removeVerticesPosition(vertices, o)
		
		MagicPanels.showVertex(vertices, 10)

	Result:
	
		return vertices array without container offset, with the same type

	'''

	# not unpack mirroring
	if iObj.isDerivedFrom("Part::Mirroring"):
		return iVertices

	# recognize iVertices type
	if iType == "auto":
		
		skip = 0
		
		if skip == 0:
			try:
				test = iVertices[0].X
				iType = "vertex"
				skip = 1
			except:
				skip = 0

		if skip == 0:
			try:
				test = iVertices[0].x
				iType = "vector"
				skip = 1
			except:
				skip = 0
		
		if skip == 0:
			try:
				test = iVertices[0][0]
				iType = "array"
				skip = 1
			except:
				skip = 0

	# convert iVertices to Vector for calculation
	vertices = []
	for v in iVertices:
		
		if iType == "array":
			n = FreeCAD.Vector(v[0], v[1], v[2])
		
		elif iType == "vertex":
			import Part
			n = FreeCAD.Vector(v.X, v.Y, v.Z)

		else:
			n = v
			
		vertices.append(n)
	
	# calculate position
	containers = getContainers(iObj)
	for o in containers:
		
		if (
			o.isDerivedFrom("App::Part") or 
			o.isDerivedFrom("PartDesign::Body") or 
			o.isDerivedFrom("App::LinkGroup") or 
			o.isDerivedFrom("Part::Cut") 
			):
			
			try:
				p = o.Placement.inverse()
			except:
				continue
			
			i = 0
			for v in vertices:

				n = p.multVec(v)
				vertices[i] = n
				
				i = i + 1

	# convert to the same type as iVertices
	i = 0
	for v in vertices:
		if iType == "array":
			vertices[i] = [ v.x, v.y, v.z ]
				
		elif iType == "vertex":
			vertices[i] = Part.Vertex(v.x, v.y, v.z)
				
		else:
			vertices[i] = v
		
		i = i + 1

	return vertices


# ###################################################################################################################
'''
# Direction, Plane, Orientation, Axis
'''
# ###################################################################################################################


# ###################################################################################################################
def isRotated(iObj):
	'''
	Description:
	
		Function to check if object iObj is rotated or not.

	Args:
	
		iObj: object to check rotation

	Usage:
	
		if MagicPanels.isRotated(o):

	Result:
	
		Return True if the object is rotated or False otherwise.

	'''

	import math
	
	if iObj.isDerivedFrom("PartDesign::Pad"):

		ref = iObj.Profile[0]
		angle = math.degrees(ref.Placement.Rotation.Angle)
		
		if equal(angle, 0) or equal(angle, 120) or equal(angle, 90):
			return False
		else:
			return True
	
	else:
		
		ref = iObj
		angle = math.degrees(ref.Placement.Rotation.Angle)
		
		if equal(angle, 0):
			return False
		else:
			return True


# ###################################################################################################################
def addRotation(iObj, iTarget):
	'''
	Description:
	
		This function checks if the iObj is rotated and add the rotation to the iTarget objects.

	Args:
	
		iObj: object to check rotation
		iTarget: array with objects to set rotation

	Usage:
	
		MagicPanels.addRotation(base, [ o ]):

	Result:
	
		If the iObj is rotated, set the same rotation to iTarget

	'''

	o = getReference(iObj)
	
	if not isRotated(o):
		return

	if o.isDerivedFrom("PartDesign::Pad"):
		ref = o.Profile[0]
	else:
		ref = o

	for t in iTarget:

		pos = t.Placement.Base
		rot = ref.Placement.Rotation * t.Placement.Rotation

		t.Placement = FreeCAD.Placement(pos, rot)


# ###################################################################################################################
def getModelRotation(iX, iY, iZ):
	'''
	Description:
	
		Transform given iX, iY, iZ values to the correct vector, if the user rotated 3D model.

	Args:
	
		iX: X value to transform
		iY: Y value to transform
		iY: Z value to transform

	Usage:
	
		[x, y, z ] = MagicPanels.getModelRotation(x, y, z)

	Result:
	
		[ X, Y, Z ] - transformed vector of given values

	'''

	[ x, y, z ] = FreeCADGui.ActiveDocument.ActiveView.getViewDirection()
	[ px, py, pz ] = FreeCADGui.ActiveDocument.ActiveView.viewPosition().Rotation.getYawPitchRoll()
	
	# init 0 key
	X = iX
	Y = iY
	Z = iZ

	# X axis invert
	if x > 0:
		X = -iX
	
	# Y axis invert
	if y < 0:
		Y = -iY
		
	# Z axis invert
	if z > 0:
		Z = -iZ

	# did I say rotation? ;-) they see me rolling ;-)

	# ##################################################
	# Z up, X rotation
	# ##################################################

	# Z up, X rotate 0
	# is base state

	# Z up, X rotate 1
	if x < 0 and y < 0 and z < 0 and py < 0 and pz > 0:
		X = -iY
		Y = iX
		Z = iZ
		
	# Z up, X rotate 2
	if x > 0 and y < 0 and z < 0 and py < 0 and pz > 0:
		X = -iX
		Y = -iY
		Z = iZ

	# Z up, X rotate 3
	if x > 0 and y > 0 and z < 0 and py < 0 and pz > 0:
		X = iY
		Y = -iX
		Z = iZ

	# ##################################################
	# Z down, X rotation
	# ##################################################

	# Z down, X rotate 0
	if x < 0 and y < 0 and z > 0 and py > 0 and pz < 0:
		X = iX
		Y = -iY
		Z = -iZ

	# Z down, X rotate 1
	if x < 0 and y > 0 and z > 0 and py > 0 and pz < 0:
		X = -iY
		Y = -iX
		Z = -iZ

	# Z down, X rotate 2
	if x > 0 and y > 0 and z > 0 and py > 0 and pz < 0:
		X = -iX
		Y = iY
		Z = -iZ

	# Z down, X rotate 3
	if x > 0 and y < 0 and z > 0 and py > 0 and pz < 0:
		X = iY
		Y = iX
		Z = -iZ

	# ##################################################
	# X up, Y rotation
	# ##################################################

	# X up, Y rotate 0
	if x < 0 and y > 0 and z > 0 and py > 0 and pz > 0:
		X = iZ
		Y = iY
		Z = -iX
	
	# X up, Y rotate 1
	if x < 0 and y < 0 and z > 0 and py < 0 and pz > 0:
		X = iZ
		Y = iX
		Z = iY
		
	# X up, Y rotate 2
	if x < 0 and y < 0 and z < 0 and py < 0 and pz < 0:
		X = iZ
		Y = -iY
		Z = iX

	# X up, Y rotate 3
	if x < 0 and y > 0 and z < 0 and py > 0 and pz < 0:
		X = iZ
		Y = -iX
		Z = -iY

	# ##################################################
	# X down, Y rotation
	# ##################################################

	# X down, Y rotate 0
	if x > 0 and y > 0 and z < 0 and py < 0 and pz < 0:
		X = -iZ
		Y = iY
		Z = iX
	
	# X down, Y rotate 1
	if x > 0 and y < 0 and z < 0 and py > 0 and pz < 0:
		X = -iZ
		Y = iX
		Z = -iY
	
	# X down, Y rotate 2
	if x > 0 and y < 0 and z > 0 and py > 0 and pz > 0:
		X = -iZ
		Y = -iY
		Z = -iX
	
	# X down, Y rotate 3
	if x > 0 and y > 0 and z > 0 and py < 0 and pz > 0:
		X = -iZ
		Y = -iX
		Z = iY

	# ##################################################
	# Y up, X rotation
	# ##################################################

	# Y up, X rotate 0
	if x < 0 and y < 0 and z < 0 and py > 0 and pz < 0:
		X = iX
		Y = iZ
		Z = -iY
	
	# Y up, X rotate 1
	if x < 0 and y < 0 and z > 0 and py > 0 and pz > 0:
		X = -iY
		Y = iZ
		Z = -iX

	# Y up, X rotate 2
	if x > 0 and y < 0 and z > 0 and py < 0 and pz > 0:
		X = -iX
		Y = iZ
		Z = iY
	
	# Y up, X rotate 3
	if x > 0 and y < 0 and z < 0 and py < 0 and pz < 0:
		X = iY
		Y = iZ
		Z = iX
	
	# ##################################################
	# Y down, X rotation
	# ##################################################

	# Y down, X rotate 0
	if x < 0 and y > 0 and z > 0 and py < 0 and pz > 0:
		X = iX
		Y = -iZ
		Z = iY

	# Y down, X rotate 1
	if x < 0 and y > 0 and z < 0 and py < 0 and pz < 0:
		X = -iY
		Y = -iZ
		Z = iX
	
	# Y down, X rotate 2
	if x > 0 and y > 0 and z < 0 and py > 0 and pz < 0:
		X = -iX
		Y = -iZ
		Z = -iY
	
	# Y down, X rotate 3
	if x > 0 and y > 0 and z > 0 and py > 0 and pz > 0:
		X = iY
		Y = -iZ
		Z = -iX
	
	return [ X, Y, Z ]


# ###################################################################################################################
def getDirection(iObj):
	'''
	Description:
	
		Allows to get Cube object direction (iType).
	
	Args:
	
		iObj: selected object

	Usage:
	
		direction = MagicPanels.getDirection(obj)

	Result:
	
		Returns iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

	'''

	if iObj.isDerivedFrom("Part::Box"):
		
		if (
			iObj.Height.Value < iObj.Width.Value and iObj.Height.Value < iObj.Length.Value and 
			iObj.Width.Value <= iObj.Length.Value
			):
			return "XY"
		
		if (
			iObj.Height.Value < iObj.Width.Value and iObj.Height.Value < iObj.Length.Value and 
			iObj.Width.Value > iObj.Length.Value
			):
			return "YX"
		
		if (
			iObj.Width.Value < iObj.Height.Value and iObj.Width.Value < iObj.Length.Value and 
			iObj.Height.Value <= iObj.Length.Value
			):
			return "XZ"
			
		if (
			iObj.Width.Value < iObj.Height.Value and iObj.Width.Value < iObj.Length.Value and 
			iObj.Height.Value > iObj.Length.Value
			):
			return "ZX"
			
		if (
			iObj.Length.Value < iObj.Height.Value and iObj.Length.Value < iObj.Width.Value and 
			iObj.Height.Value <= iObj.Width.Value
			):
			return "YZ"
			
		if (
			iObj.Length.Value < iObj.Height.Value and iObj.Length.Value < iObj.Width.Value and 
			iObj.Height.Value > iObj.Width.Value
			):
			return "ZY"

		# for profiles with 2 equal sizes
		
		if iObj.Height.Value == iObj.Width.Value and iObj.Length.Value >= iObj.Height.Value:
			return "XY"
			
		if iObj.Length.Value == iObj.Height.Value and iObj.Width.Value > iObj.Height.Value:
			return "YX"
			
		if iObj.Length.Value == iObj.Width.Value and iObj.Height.Value > iObj.Width.Value:
			return "ZX"

	else:
		
		try:
			ref = iObj.Profile[0].Support[0][0]
		except:
			ref = iObj.Profile[0].AttachmentSupport[0][0]
			
		[ sX, sY, thick ] = getSizes(iObj)
		
		if ref.Label.startswith("XY"):
			
			if sX >= sY:
				return "XY"
			
			if sX < sY:
				return "YX"
			
		if ref.Label.startswith("XZ"):
			
			if sX >= sY:
				return "XZ"
			
			if sX < sY:
				return "ZX"
			
		if ref.Label.startswith("YZ"):
			
			if sX >= sY:
				return "YZ"
			
			if sX < sY:
				return "ZY"


# ###################################################################################################################
'''
# Position, Placement, Move
'''
# ###################################################################################################################


# ###################################################################################################################
def resetPlacement(iObj):
	'''
	Description:
	
		Reset placement for given object. Needed to set rotation for object at face.
	
	Args:
	
		iObj: object to reset placement

	Usage:
	
		MagicPanels.resetPlacement(obj)

	Result:
	
		Object obj return to base position.

	'''

	zero = FreeCAD.Vector(0, 0, 0)
	r = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
	
	if iObj.isDerivedFrom("PartDesign::Pad"):
		iObj.Profile[0].AttachmentOffset.Base = zero
		iObj.Profile[0].AttachmentOffset.Rotation = r
		
	elif iObj.isDerivedFrom("Sketcher::SketchObject"):
		iObj.Placement.Base = zero
		iObj.Placement.Rotation = r
		
	else:
		iObj.Placement.Base = zero
		iObj.Placement.Rotation = r


# ###################################################################################################################
def getOffset(iObj, iDestination, iType="array"):
	'''
	Description:
	
		This function returns offset for setPosition function.
	
	Args:
	
		iObj: object to get offset
		iDestination: global destination point
		iType (optional): iDestination type
			* "array": the iDestination will be [ float, float, float ]
			* "vector": the iDestination will be FreeCAD.Vector type [ .x, .y, .z ]
			* "vertex": the iDestination will be Vertex type [ .X, .Y, .Z ]

	Usage:
	
		[ offetX, offetY, offetZ ] = MagicPanels.getOffset(o, [ 100, 200, 0 ], "array")
		[ offetX, offetY, offetZ ] = MagicPanels.getOffset(o, edge.CenterOfMass, "vector")

	Result:
	
		return array with offsets [ offetX, offetY, offetZ ]

	'''


	[ dX, dY, dZ ] = [ 0, 0, 0 ]
	
	if iType == "array":
		[ dX, dY, dZ ] = [ iDestination[0], iDestination[1], iDestination[2] ]
	
	if iType == "vector":
		[ dX, dY, dZ ] = [ iDestination.x, iDestination.y, iDestination.z ]
		
	if iType == "vertex":
		[ dX, dY, dZ ] = [ iDestination.X, iDestination.Y, iDestination.Z ]

	# make sure the object position data has been updated
	try:
		iObj.recompute()
	except:
		skip = 1
	
	[ X, Y, Z ] = getPosition(iObj, "global")
	
	diffX = abs(dX - X)
	diffY = abs(dY - Y)
	diffZ = abs(dZ - Z)

	if X > dX:
		diffX = -diffX

	if Y > dY:
		diffY = -diffY

	if Z > dZ:
		diffZ = -diffZ
	
	return [ diffX, diffY, diffZ ]
	

# ###################################################################################################################
def searchGlobalPosition(iObj):
	'''
	Description:
	
		This function search simple objects for global placement. 
		This can be used in loop for recursive search for more complex objects like LinkGroup or Link.
	
	Args:
	
		iObj: object to search for global placement

	Usage:
	
		[ x, y, z ] = MagicPanels.searchGlobalPosition(o)

	Result:
	
		return [ x, y, z ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position

	'''


	# #######################################################
	# init
	# #######################################################
	
	[ x, y, z ] = [ 0, 0, 0 ]
	
	try:
		x = iObj.Placement.Base.x
		y = iObj.Placement.Base.y
		z = iObj.Placement.Base.z
	except:
		skip = 1

	# #######################################################
	# just make the magic
	# #######################################################
	
	if iObj.isDerivedFrom("Sketcher::SketchObject"):
		import Draft
		copy = Draft.make_clone(iObj)
		containers = getContainers(iObj)
		moveToContainer([ copy ], containers[0])
		copy.recompute()
		x = copy.Shape.BoundBox.XMin
		y = copy.Shape.BoundBox.YMin
		z = copy.Shape.BoundBox.ZMin
		FreeCAD.ActiveDocument.removeObject(str(copy.Name))

	if iObj.isDerivedFrom("PartDesign::Body"):
		try:
			x = iObj.Shape.BoundBox.XMin
			y = iObj.Shape.BoundBox.YMin
			z = iObj.Shape.BoundBox.ZMin
		except:
			iObj = iObj.VisibleFeature
			
	if iObj.isDerivedFrom("Part::Cut"):
		try:
			x = iObj.Shape.BoundBox.XMin
			y = iObj.Shape.BoundBox.YMin
			z = iObj.Shape.BoundBox.ZMin
		except:
			skip = 1
		
	try:
		test = iObj._Body
		x = iObj.Shape.BoundBox.XMin
		y = iObj.Shape.BoundBox.YMin
		z = iObj.Shape.BoundBox.ZMin

	except:
		skip = 1

	if isType(iObj, "Clone"):
		x = iObj.Shape.BoundBox.XMin
		y = iObj.Shape.BoundBox.YMin
		z = iObj.Shape.BoundBox.ZMin
	
	if iObj.isDerivedFrom("PartDesign::SubShapeBinder"):
		x = iObj.Shape.BoundBox.XMin
		y = iObj.Shape.BoundBox.YMin
		z = iObj.Shape.BoundBox.ZMin
	
	# #######################################################
	# recalculate with containers
	# #######################################################
	
	baseV = FreeCAD.Vector(x, y, z)
	containers = getContainers(iObj)
	globalV = baseV
	
	for o in containers:
	
		if (
			o.isDerivedFrom("App::Part") or 
			o.isDerivedFrom("PartDesign::Body") or 
			o.isDerivedFrom("App::LinkGroup") or 
			o.isDerivedFrom("Part::Cut") 
			):

			try:
				p = o.Placement
			except:
				continue
			
			n = p.multVec(globalV)
			globalV = n

	# #######################################################
	# return final result
	# #######################################################
	
	return [ globalV.x, globalV.y, globalV.z ]


# ###################################################################################################################
def getPosition(iObj, iType="global"):
	'''
	Description:
	
		This function returns placement for the object to move or copy without rotation.
	
	Args:
	
		iObj: object to get placement
		iType (optional): 
			"global": trying to calculate global position of the object, make sure the object is currently supported
			"local": return iObj.Placement

	Usage:
	
		[ x, y, z ] = MagicPanels.getPosition(o, "global")
		[ x, y, z ] = MagicPanels.getPosition(o, "local")

	Result:
	
		return [ x, y, z ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		
		if there is error or placement cannot be calculated there 
		will be returned empty string for easier error handling

	'''

	# #######################################################
	# make sure the object position data has been updated
	# #######################################################
	
	try:
		iObj.recompute()
	except:
		return ""

	# #######################################################
	# init
	# #######################################################
	
	[ x, y, z ] = [ 0, 0, 0 ]

	# #######################################################
	# local
	# #######################################################
	
	if iType == "local":
		
		try:
			x = iObj.Placement.Base.x
			y = iObj.Placement.Base.y
			z = iObj.Placement.Base.z
		
			return [ x, y, z ]
		
		except:
			return ""
	
	# #######################################################
	# global
	# #######################################################
	
	elif iType == "global":
		
		# #######################################################
		# for: LinkGroup, Link or Part
		# #######################################################
		
		if (
			iObj.isDerivedFrom("App::LinkGroup") or 
			iObj.isDerivedFrom("App::Link") or
			iObj.isDerivedFrom("App::Part")
			):
			
			# you have better idea to solve this recursive 
			# problem without globals? open issue if so...
			global gx, gy, gz, init
			init = True
			
			# define recursive search
			def searchElements(io):
				global gx, gy, gz, init
				
				if io.isDerivedFrom("App::LinkGroup"):
					target = io.ElementList
				elif io.isDerivedFrom("App::Link"):
					target = [ io.LinkedObject ]
				elif io.isDerivedFrom("App::Part"):
					target = io.Group
				else:
					return
				
				# go deeper
				for o in target:
		
					if (
						o.isDerivedFrom("App::LinkGroup") or 
						o.isDerivedFrom("App::Link") or
						o.isDerivedFrom("App::Part")
						):
						
						# call it again
						searchElements(o)

					else:
						[ ox, oy, oz ] = searchGlobalPosition(o)
						
						# init with first element in container
						if init == True:
							[ gx, gy, gz ] = [ ox, oy, oz ]
							init = False
							
						# try to find minimum values
						# I mean left bottom corner what will be 
						# the placement anchor in this case
						if ox < gx:
							gx = ox
						if oy < gy:
							gy = oy
						if oz < gz:
							gz = oz
			
			# run the recursive search
			searchElements(iObj)
			
			# recalculate Link offset
			if iObj.isDerivedFrom("App::Link"):
				try:
					[ gx, gy, gz ] = iObj.Placement.multVec( FreeCAD.Vector(gx, gy, gz) )
					if iObj.LinkedObject.isDerivedFrom("App::LinkGroup") or iObj.LinkedObject.isDerivedFrom("App::Part"):
						[ gx, gy, gz ] = iObj.LinkedObject.Placement.inverse().multVec( FreeCAD.Vector(gx, gy, gz) )
				except:
					skip = 1
			
			# return the updated minimum via recursive search
			# little crazy way but currently I do not have better idea
			[ x, y, z ] = [ gx, gy, gz ]

		# #######################################################
		# for simple objects
		# #######################################################
		
		else:
			[ x, y, z ] = searchGlobalPosition(iObj)

		# #######################################################
		# return final result
		# #######################################################
	
		return [ x, y, z ]

	else:
		return ""


# ###################################################################################################################
def setPosition(iObj, iX, iY, iZ, iType="offset"):
	'''
	Description:
	
		This function set object position to move or copy without rotation.
		
	Args:

		iObj: object to add position offset, for example already created Clone or Link
		iX: X axis offset to add or position to set
		iY: Y axis offset to add or position to set
		iZ: Z axis offset to add or position to set
		iType (optional):
			* "offset": copy like Clone or Link is created in the same place as base object so you can add only 
							offset to the current copy placement instead of searching for base object global position. So here the iX, iY, iZ is offset for placement.
			* "local": set directly to object Placement attribute, so here the iX, iY, iZ is local object XYZ. However, if the object 
							is not in the container or the containers don't have offsets this might be global.
			* "global": setting object position via global coordinates, here the iX, iY, iZ is global XYZ. The offset to the 
							global iX, iY, iZ will calculated here automatically.
		
	Usage:
	
		MagicPanels.setPosition(copy, 100, 0, 0, "offset")
		MagicPanels.setPosition(copy, 100, 0, 0, "local")
		MagicPanels.setPosition(copy, 100, 0, 0, "global")

	Result:
	
		return empty string if everything was fine or string with error info

	'''

	
	if iType == "offset":
		FreeCAD.ActiveDocument.openTransaction("setPositionOffset "+str(iObj.Label))

		x = iObj.Placement.Base.x
		y = iObj.Placement.Base.y
		z = iObj.Placement.Base.z
		iObj.Placement.Base = FreeCAD.Vector(x + iX, y + iY, z + iZ)

		FreeCAD.ActiveDocument.commitTransaction()
		return ""
	
	if iType == "local":
		FreeCAD.ActiveDocument.openTransaction("setPositionLocal "+str(iObj.Label))

		iObj.Placement.Base = FreeCAD.Vector(iX, iY, iZ)

		FreeCAD.ActiveDocument.commitTransaction()
		return ""
	
	if iType == "global":
		FreeCAD.ActiveDocument.openTransaction("setPositionGlobal "+str(iObj.Label))
		
		[ offsetX, offsetY, offsetZ ] = getOffset(iObj, [ iX, iY, iZ ], "array")
		
		x = iObj.Placement.Base.x
		y = iObj.Placement.Base.y
		z = iObj.Placement.Base.z
		iObj.Placement.Base = FreeCAD.Vector(x + offsetX, y + offsetY, z + offsetZ)
		
		FreeCAD.ActiveDocument.commitTransaction()
		return ""
	
	return "wrong iType"


# ###################################################################################################################
def getObjectToMove(iObj):
	'''
	Description:
	
		This function returns object to move.
	
	Args:
	
		iObj: object to get reference to move

	Usage:
	
		toMove = MagicPanels.getObjectToMove(o)

	Result:
	
		For example: 

		for Cube: always returns Cube
		for Pad: always returns Body
		for PartDesign objects: try to return Body
		for LinkGroup: returns LinkGroup
		for Cut: returns Cut
		for any other object: returns object

	'''

	if (
		iObj.isDerivedFrom("Part::Box") or 
		iObj.isDerivedFrom("Part::Cut") or 
		iObj.isDerivedFrom("PartDesign::Body") or 
		iObj.isDerivedFrom("App::LinkGroup") 
		):
		return iObj

	elif iObj.isDerivedFrom("PartDesign::Pad"):
		return iObj._Body

	else:
		
		try:
			iObj = iObj._Body
		except:
			skip = 1

	return iObj


# ###################################################################################################################
def getObjectCenter(iObj):
	'''
	Description:
	
		Returns center of the object.
	
		# > [!NOTE]
		# > This function will be updated later with more reliable 
		# > way of getting center of the object, also for LinkGroup and other containers. 
		# > Now it returns Shape.CenterOfMass for the object and it is not the same 
		# > as center of the object.
	
	Args:
	
		iObj: object

	Usage:
	
		[ cx, cy, cz ] = MagicPanels.getObjectCenter(obj)

	Result:
	
		Returns array with [ cx, cy, cz ] values for center point.

	'''

	try:
		
		v = iObj.Shape.CenterOfMass
		return [ v[0], v[1], v[2] ]
		
	except:
		
		noCenterOfMass = True
	
	if noCenterOfMass:
		
		[ sx, sy, sz ] = getSizesFromVertices(iObj)
		
		v = getattr(iObj.Shape, "Vertex"+"es")[0]
		x, y, z = v.X, v.Y, v.Z
		
		cx = setVertexPadding(iObj, v, sx / 2, "X")
		cy = setVertexPadding(iObj, v, sy / 2, "Y")
		cz = setVertexPadding(iObj, v, sy / 2, "Z")

		return [ cx, cy, cz ]
		
	return ""


# ###################################################################################################################
def setAnchors(iSourceObj, iSourceAnchor, iTarget):
	'''
	Description:
	
		Set iSourceObj into iTargetObj but using custom anchors.
	
	Args:
	
		iSourceObj: object to move
		iSourceAnchor: array [ X, Y, Z ] as anchor for source object
		iTarget: array [ X, Y, Z ] as destination to move
		
	Usage:
	
		MagicPanels.setAnchors(tenon, tenonCenter, faceCenter)

	Result:
	
		for the sample the tenon will be moved into the center of the face but 
		the center of the face will be equal the center of the tenon object

	'''


	FreeCAD.ActiveDocument.openTransaction("setAnchors "+str(iSourceObj.Label))
	
	[ offetX, offetY, offetZ ] = getOffset(iSourceObj, iSourceAnchor, "array")
	setPosition(iSourceObj, iTarget[0], iTarget[1], iTarget[2], "global")
	setPosition(iSourceObj, -offetX, -offetY, -offetZ, "offset")

	FreeCAD.ActiveDocument.commitTransaction()


# ###################################################################################################################
'''
# Containers
'''
# ###################################################################################################################


# ###################################################################################################################
def createContainer(iObjects, iLabel="Container", iNesting=True):
	'''
	Description:
	
		This function creates container for given iObjects. The label for new container will be get from 
		first element of iObjects (iObjects[0]).
	
	Args:
	
		iObjects: array of object to create container for them
		iLabel: string, container label
		iNesting: boolean, add nesting label prefix (True) or set given label (False)

	Usage:
	
		container = MagicPanels.createContainer([c1, c2])
		container = MagicPanels.createContainer([c1, c2], "LinkGroup")
		container = MagicPanels.createContainer([o1, o2, o3, o4, o5, o6, o7], "Furniture, Module", False)

	Result:
	
		Created container and objects inside the container, return container object.

	'''

	try:
		for o in iObjects:
			oldcontainer = o.InList[0]
			oldcontainer.ViewObject.dragObject(o)
	except:
		skip = 1

	base = iObjects[0]
	container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','LinkGroup')
	container.setLink(iObjects)
	
	if iNesting == True:
		container.Label = getNestingLabel(base, iLabel)
	else:
		container.Label = iLabel + " "
	
	try:
		copyColors(base, container)
	except:
		skip = 1
	
	try:
		objects = oldcontainer.ElementList
		objects.append(container)
		oldcontainer.setLink(objects)
	except:
		skip = 1
	
	FreeCAD.ActiveDocument.recompute()
	
	return container


# ###################################################################################################################
def getContainersPath(iObj):
	'''
	Description:
	
		This function returns string with path to object in this way: LinkGroup.Part.Body.Pad
		
	
	Args:
	
		iObj: object to get path

	Usage:
	
		path = MagicPanels.getContainersPath(o)

	Result:
	
		return string

	'''


	try:
		parents = iObj.Parents
	except:
		return str(iObj.Name)
	
	if len(parents) == 0:
		return str(iObj.Name)
	
	root = str(iObj.Parents[0][0].Name)
	path = str(iObj.Parents[0][1])[:-1]
	
	return str(root + "." + path)


# ###################################################################################################################
def getContainers(iObj):
	'''
	Description:
	
		This function get list of containers for given iObj.
		
	
	Args:
	
		iObj: object to get list of containers

	Usage:
	
		containers = MagicPanels.getContainers(o)

	Result:
	
		return array with objects

	'''


	containers = []
	path = getContainersPath(iObj)
	
	if path == str(iObj.Name):
		return containers
	
	pathArr = path.split(".")[:-1]
	
	for c in reversed(pathArr):
		
		o = FreeCAD.ActiveDocument.getObject(c)
		
		if (
			o.isDerivedFrom("App::Part") or 
			o.isDerivedFrom("PartDesign::Body") or 
			o.isDerivedFrom("App::LinkGroup") or 
			o.isDerivedFrom("Part::Cut") 
		):
			containers.append(o)

	return containers


# ###################################################################################################################
def moveToContainer(iObjects, iContainer, iType="object"):
	'''
	Description:

		Move objects iObjects to iContainer.

	Args:
	
		iObjects: list of objects to move to iContainer, for example new created Cube
		iContainer: container object or string describing destination level, possible:
			iContainer: object for example LinkGroup or Pad to search
			"object": move all iObjects directly to given iContainer object
			"parent": move all iObjects to first container above Body, for example Part for given iContainer
			"LinkGroup": move all iObjects to first LinkGroup container above given iContainer

	Usage:

		For Pad structure: "LinkGroup2 -> LinkGroup1 -> Part -> Body -> Pad"
		and copy object is in root folder. 
		
		MagicPanels.moveToContainer([ copy ], LinkGroup2)            # to move copy object to LinkGroup2
		MagicPanels.moveToContainer([ copy ], LinkGroup2, "object")  # to move copy object to LinkGroup2
		MagicPanels.moveToContainer([ copy ], Pad, "parent")         # to move copy object to Part
		MagicPanels.moveToContainer([ copy ], Pad, "LinkGroup")      # to move copy object to LinkGroup1

	Result:

		No return, move object.

	'''
	
	
	for o in iObjects:
		
		destination = iContainer
		
		if iType != "object":

			containers = getContainers(iContainer)
			
			if len(containers) < 1:
				return
			
			for c in containers:
				
				if iType == "parent":
					if (
						c.isDerivedFrom("App::LinkGroup") or 
						c.isDerivedFrom("App::DocumentObjectGroup") or 
						c.isDerivedFrom("App::Part")
					):
						destination = c
						break
				
				if iType == "LinkGroup":
					if c.isDerivedFrom("App::LinkGroup"):
						destination = c
						break
		
		# move the object to this container
		# in try to avoid dependency loop
		# caused by incorrect containers list
		try:
			FreeCADGui.Selection.addSelection(o)
			o.adjustRelativeLinks(destination)
			destination.ViewObject.dropObject(o, None, '', [])
			FreeCADGui.Selection.clearSelection()
		except:
			skip = 1

	FreeCAD.ActiveDocument.recompute()


# ###################################################################################################################
def moveToFirst(iObjects, iSelection):
	'''
	Description:

		Move objects iObjects to first LinkGroup container for iSelection object.
		
		# > [!NOTE]
		# > This function removes the offset that should have been added earlier. Why not just copy without offset?
		# > If you have 2 objects in separate containers and the second object is only moved via the container Placement, 
		# > then from FreeCAD point the objects are in the same place. So you won't be able to compute space between 
		# > objects in these containers. FreeCAD uses local positions. It's good because you can calculate many things 
		# > without using advanced formulas. Adding an offset and removing it later is a trick for easier calculations.
		# > 
		# > You can convert all vertices to global, but in this case you won't be able to determine the plane correctly 
		# > in an easy way, for example the vertices on an edge would no longer be along the same coordinate axis, 
		# > and thus you'd have to use advanced formulas. It can be done with a trick, but maybe something like 
		# > that will come along later if need be.

	Args:
	
		iObjects: list of objects to move to container, for example [ copy1, copy2 ]
		iSelection: selected object, for example "PartDesign::Pad" with structure "LinkGroup2 -> LinkGroup1 -> Part -> Body -> Pad" or "Part::Box" in structure "LinkGroup2 -> LinkGroup1 -> panelXY", to move the object to LinkGroup1

	Usage:

		MagicPanels.moveToFirst([ copy ], pad)
		MagicPanels.moveToFirst([ copy ], panel)

	Result:

		No return, move copy object to LinkGroup1 container.

	'''
	
	# if no container, do nothing
	containers = getContainers(iSelection)
	rsize = len(containers)
	if rsize == 0:
		return

	# check containers
	boX, boY, boZ = 0, 0, 0
	boR = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
	i = 0
	while i < rsize and i < gSearchDepth:
		
		c = containers[i]
		
		# if there is supported container
		if (
			c.isDerivedFrom("App::LinkGroup") or 
			c.isDerivedFrom("App::DocumentObjectGroup") 
			):
		
			for o in iObjects:
			
				# remove Body offset
				[ x, y, z, r ] = getContainerPlacement(o, "clean")
				[ coX, coY, coZ, coR ] = getContainersOffset(iSelection)
				
				# calculate new offset without Body
				x = x - coX + boX
				y = y - coY + boY
				z = z - coZ + boZ
				
				# set new placement
				setContainerPlacement(o, x, y, z, 0, "clean")

				# move the object to this container
				FreeCADGui.Selection.addSelection(o)
				o.adjustRelativeLinks(c)
				c.ViewObject.dropObject(o, None, '', [])
				FreeCADGui.Selection.clearSelection()

			FreeCAD.ActiveDocument.recompute()
			return

		# if there is other container with placement
		elif (
			c.isDerivedFrom("App::Part") or 
			c.isDerivedFrom("PartDesign::Body") 
			):

			# check if there is placement, that can impact the placement
			try:
				boX = boX + c.Placement.Base.x
				boY = boY + c.Placement.Base.y
				boZ = boZ + c.Placement.Base.z
			except:
				skip = 1

		# skip other objects with placements, like Sketches, Plane
		else:
			skip = 1

		i = i + 1


# ###################################################################################################################
def getNestingLabel(iObj, iPrefix):
	'''
	Description:
	
		This function set label for nesting objects, containers, copied, to not repeat 
		the prefix and not make the label too long. 
	
	Args:
	
		iObj: object for the label check
		iPrefix: string, preferred prefix for the label

	Usage:
	
		o.Label = MagicPanels.getNestingLabel(o, "Container")

	Result:
	
		return string for the new label

	'''

	label = str(iObj.Label)

	if label.find(", ") == -1:
		newLabel = iPrefix + ", " + label + " "

	else:
		prefix = label.split(", ")[0]
		newLabel = label.replace(prefix, iPrefix)

	return newLabel


# ###################################################################################################################
def getContainersOffset(iObj):
	'''
	Description:
	
		If the object is in the container like Part, Body, LinkGroup the vertices are 
		not updated by FreeCAD. From FreeCAD perspective the object is still in the 
		same place. This function is trying to solve this problem and calculates 
		all offsets of all containers.
	
	Args:
	
		iObj: object to get containers offset

	Usage:
	
		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(o)

	Result:
	
		return [ coX, coY, coZ, coR ] array with offsets for placement:
		
		coX: X Axis object position
		coY: Y Axis object position
		coZ: Z Axis object position
		coR: Rotation object

	'''

	coX, coY, coZ = 0, 0, 0
	coR = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)

	# not unpack mirroring
	if iObj.isDerivedFrom("Part::Mirroring"):
		return [ coX, coY, coZ, coR ]

	containers = getContainers(iObj)
	for o in containers:
		
		if (
			o.isDerivedFrom("App::Part") or 
			o.isDerivedFrom("PartDesign::Body") or 
			o.isDerivedFrom("App::LinkGroup") or 
			o.isDerivedFrom("Part::Cut") 
			):
			
			try:
				x = o.Placement.Base.x
				y = o.Placement.Base.y
				z = o.Placement.Base.z
				r = o.Placement.Rotation
			except:
				continue

			coX = coX + x
			coY = coY + y
			coZ = coZ + z
			coR = coR * r

	return [ coX, coY, coZ, coR ]


# ###################################################################################################################
def getPlacementDiff(iStart, iDestination):
	'''
	Description:
	
		Return diff that should be added to iStart to move object from iStart to iDestination position. 
		If you want to move back you can minus the diff from iDestination.
		
	Args:
	
		iStart: start vertex float value
		iDestination: destination vertex float value
	
	Usage:
		
		[ moveX, moveY, moveZ ] = MagicPanels.getPlacementDiff(v1, v2)
		
	Result:
	
		Return [ moveX, moveY, moveZ ] array with X, Y, Z floats to move object.

	'''

	diffX = getVertexAxisCross(iStart[0], iDestination[0])
	if iStart[0] < iDestination[0]:
		moveX = diffX
	else:
		moveX = - diffX
	
	diffY = getVertexAxisCross(iStart[1], iDestination[1])
	if iStart[1] < iDestination[1]:
		moveY = diffY
	else:
		moveY = - diffY
	
	diffZ = getVertexAxisCross(iStart[2], iDestination[2])
	if iStart[2] < iDestination[2]:
		moveZ = diffZ
	else:
		moveZ = - diffZ

	return [ moveX, moveY, moveZ ]


# ###################################################################################################################
def isVisible(iObj):
	'''
	Description:
	
		Returns object visibility, even if object is visible but inside the hidden LinkGroup container.
		
	Args:
	
		iObj: object to search visibility

	Usage:
		
		visible = MagicPanels.isVisible(iObj)
		
	Result:
	
		Return boolean True or False
	'''
	
	current = iObj

	while True:
	
		if current.Visibility == False:
			return False
	
		try:
			visible = current.Parents[0][0].isElementVisible(current.Parents[0][1]+str(current.Name))
			if visible == 0:
				return False
		except:
			return True

		try:
			current = current.Parents[0][0]
		except:
			return True

	return True


# ###################################################################################################################
def toggleVisibility(iObj):
	'''
	Description:
	
		Toggle object visibility.
		
	Args:
	
		iObj: object to toggle visibility

	Usage:
		
		MagicPanels.toggleVisibility(old)
		
	Result:
	
		no return
	'''


	try:
		FreeCADGui.Selection.clearSelection()
		FreeCADGui.Selection.addSelection(iObj)
		FreeCADGui.runCommand('Std_ToggleVisibility', 0)
		FreeCADGui.Selection.clearSelection()

	except:
		skip = 1


# ###################################################################################################################
'''
# Conversion
'''
# ###################################################################################################################


# ###################################################################################################################
def convertPosition(iObj, iX, iY, iZ):
	'''
	Description:
	
		Convert given position vector to correct position values according 
		to the object direction.
	
	Args:
	
		iObj: object
		iX: x position
		iY: y position
		iZ: z position

	Usage:
	
		[ x, y, z ] = MagicPanels.convertPosition(obj, 0, 400, 0)

	Result:
	
		For Pad object in XZ direction return the AttachmentOffset order [ 0, 0, -400 ]

	'''
	
	# it is better to use Sketch.getGlobalPlacement()
	if iObj.isDerivedFrom("Sketcher::SketchObject"):
		
		try:
			obj = iObj.Support[0][0]
			faceName = str(iObj.Support[0][1]).replace("'","").replace(",","").replace("(","").replace(")","")
		except:
			obj = iObj.AttachmentSupport[0][0]
			faceName = str(iObj.AttachmentSupport[0][1]).replace("'","").replace(",","").replace("(","").replace(")","")
			
		face = obj.getSubObject(faceName)
		axis = getFacePlane(face)
		
		if axis == "XY":
			return [ iX, iY, iZ ]
		
		if axis == "XZ":
			return [ iX, iZ, -iY ]

		if axis == "YZ":
			return [ iY, iZ, iX ]

	if iObj.isDerivedFrom("PartDesign::Pad"):
		
		direction = getDirection(iObj)
		
		if direction == "XY" or direction == "YX":
			return [ iX, iY, iZ ]
		
		if direction == "XZ" or direction == "ZX":
			return [ iX, iZ, -iY ]

		if direction == "YZ" or direction == "ZY":
			return [ iY, iZ, iX ]
	
	return [ iX, iY, iZ ]


# ###################################################################################################################
def sizesToCubePanel(iObj, iType):
	'''
	Description:
	
		Converts selected object (iObj) sizes to Cube panel sizes into given direction (iType). 
		So, the returned values can be directly assigned to Cube object in order to create 
		panel in exact direction.

	Args:

		iObj: selected object
		iType direction: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

	Usage:

		[ Length, Width, Height ] = MagicPanels.sizesToCubePanel(obj, "YZ")

	Result:

		Returns [ Length, Width, Height ] for YZ object placement.

	'''

	if iObj.isDerivedFrom("Part::Box"):

		sizes = [ iObj.Length.Value, iObj.Width.Value, iObj.Height.Value ]
		
	elif iObj.isDerivedFrom("PartDesign::Pad"):
		
		sizeX = ""
		sizeY = ""
		
		for c in iObj.Profile[0].Constraints:
			if c.Name == "SizeX":
				sizeX = c.Value
			if c.Name == "SizeY":
				sizeY = c.Value
		
		if sizeX == "" or sizeY == "":
			sizes = getSizesFromVertices(iObj.Profile[0])
			sizes.sort()
			sizes.pop(0)
			sizes.insert(0, iObj.Length.Value)
			
		else:
			sizes = [ iObj.Length.Value, sizeX, sizeY ]
	
	elif hasattr(iObj, "Base_Length"):

		sizes = [ iObj.Base_Length.Value, iObj.Base_Width.Value, iObj.Base_Height.Value ]

	else:
		sizes = getSizesFromVertices(iObj)

	sizes.sort()

	if iType == "XY":
		Length = sizes[2]
		Width = sizes[1]
		Height = sizes[0]

	if iType == "YX":
		Length = sizes[1]
		Width = sizes[2]
		Height = sizes[0]

	if iType == "XZ":
		Length = sizes[2]
		Width = sizes[0]
		Height = sizes[1]

	if iType == "ZX":
		Length = sizes[1]
		Width = sizes[0]
		Height = sizes[2]

	if iType == "YZ":
		Length = sizes[0]
		Width = sizes[2]
		Height = sizes[1]

	if iType == "ZY":
		Length = sizes[0]
		Width = sizes[1]
		Height = sizes[2]

	return [ Length, Width, Height ]


# ###################################################################################################################
'''
# Replace
'''
# ###################################################################################################################


# ###################################################################################################################
def makePad(iObj, iPadLabel="Pad"):
	'''
	Description:
	
		Allows to create Part, Plane, Body, Pad, Sketch objects.
	
	Args:
	
		iObj: object Cube to change into Pad
		iPadLabel: Label for the new created Pad, the Name will be Pad

	Usage:

		[ part, body, sketch, pad ] = MagicPanels.makePad(obj, "myPanel")

	Result:
	
		Created Pad with correct placement, rotation and return [ part, body, sketch, pad ].

	'''

	sizes = getSizes(iObj)
	sizes.sort()

	direction = getDirection(iObj)
	
	if direction == "XY" or direction == "XZ" or direction == "YZ":
		s = [ sizes[2], sizes[1], sizes[0] ]
	
	if direction == "YX" or direction == "ZX" or direction == "ZY":
		s = [ sizes[1], sizes[2], sizes[0] ]

	[ X, Y, Z, R ] = getContainerPlacement(iObj, "clean")
	
	if direction == "XY" or direction == "YX":
		[ x, y, z ] = [ X, Y, Z ]
	
	if direction == "XZ" or direction == "ZX":
		[ x, y, z ] = [ X, Y, Z ]

	if direction == "YZ" or direction == "ZY":
		[ x, y, z ] = [ Y, Z, X ]
	
	import Part, PartDesign
	import Sketcher
	import PartDesignGui
	import math

	doc = FreeCAD.ActiveDocument
	
	part = doc.addObject('App::Part', 'Part')
	part.Label = translate('makePad', 'Part') + ", "+iPadLabel
	
	body = doc.addObject('PartDesign::Body', 'Body')
	body.Label = translate('makePad', 'Body') + ", "+iPadLabel
	part.addObject(body)
	
	sketch = body.newObject('Sketcher::SketchObject', 'Sketch')
	sketch.Label = translate('makePad', 'Pattern') + ", "+iPadLabel
	
	try:
		if direction == "XY" or direction == "YX":
			sketch.Support = (body.Origin.OriginFeatures[3])
		if direction == "XZ" or direction == "ZX":
			sketch.Support = (body.Origin.OriginFeatures[4])
		if direction == "YZ" or direction == "ZY":
			sketch.Support = (body.Origin.OriginFeatures[5])
	except:
		if direction == "XY" or direction == "YX":
			sketch.AttachmentSupport = (body.Origin.OriginFeatures[3])
		if direction == "XZ" or direction == "ZX":
			sketch.AttachmentSupport = (body.Origin.OriginFeatures[4])
		if direction == "YZ" or direction == "ZY":
			sketch.AttachmentSupport = (body.Origin.OriginFeatures[5])

	sketch.MapMode = 'FlatFace'

	geoList = []
	geoList.append(Part.LineSegment(FreeCAD.Vector(115.695488,159.435455,0),FreeCAD.Vector(274.784485,159.435455,0)))
	geoList.append(Part.LineSegment(FreeCAD.Vector(274.784485,159.435455,0),FreeCAD.Vector(274.784485,53.166523,0)))
	geoList.append(Part.LineSegment(FreeCAD.Vector(274.784485,53.166523,0),FreeCAD.Vector(115.695488,53.166523,0)))
	geoList.append(Part.LineSegment(FreeCAD.Vector(115.695488,53.166523,0),FreeCAD.Vector(115.695488,159.435455,0)))
	sketch.addGeometry(geoList,False)
	
	conList = []
	conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
	conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
	conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
	conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
	conList.append(Sketcher.Constraint('Horizontal',0))
	conList.append(Sketcher.Constraint('Horizontal',2))
	conList.append(Sketcher.Constraint('Vertical',1))
	conList.append(Sketcher.Constraint('Vertical',3))
	sketch.addConstraint(conList)
	del geoList, conList

	sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,-1,1))
	sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,274.784485))
	sketch.setDatum(9,FreeCAD.Units.Quantity(s[0]))
	sketch.renameConstraint(9, u'SizeX')
	sketch.addConstraint(Sketcher.Constraint('DistanceY',3,1,3,2,159.435455))
	sketch.setDatum(10,FreeCAD.Units.Quantity(s[1]))
	sketch.renameConstraint(10, u'SizeY')

	if isRotated(iObj):

		if direction == "XZ" or direction == "ZX":
			sketch.Placement.Rotation.Angle = sketch.Placement.Rotation.Angle - math.radians(90)
		if direction == "YZ" or direction == "ZY":
			sketch.Placement.Rotation.Angle = sketch.Placement.Rotation.Angle - math.radians(120)

		rotation = R * sketch.Placement.Rotation

	else:
		rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0)

	setSketchPlacement(sketch, x, y, z, rotation, "attach")

	pad = body.newObject('PartDesign::Pad', "Pad")
	pad.Label = iPadLabel
	pad.Profile = sketch
	pad.Length = FreeCAD.Units.Quantity(s[2])
	sketch.Visibility = False

	if direction == "XZ" or direction == "ZX":
		pad.Reversed = True

	# try copy expressions from Cube to Pad
	if iObj.ExpressionEngine != []:
		
		doc.recompute()
		
		for ex in iObj.ExpressionEngine:
			
			ev = iObj.evalExpression(str(ex[1]))
			
			# this might be integer without units, so there is no .Value for int
			try:
				ev = ev.Value
			except:
				skip = 1
			
			if equal(ev, s[0]):
				sketch.setExpression('.Constraints.SizeX', str(ex[1]))
				
			elif equal(ev, s[1]):
				sketch.setExpression('.Constraints.SizeY', str(ex[1]))
				
			elif equal(ev, s[2]):
				pad.setExpression('Length', str(ex[1]))

			else:
				skip = 1

	try:
		copyColors(iObj, body)
	except:
		skip = 1

	try:
		copyColors(iObj, pad)
	except:
		skip = 1

	doc.recompute()
	
	# trick to avoid Topology Naming Problem with containers
	# if the Cube is replaced by Pad and you move the Pad directly
	# the BoundBox will be different than Cube ;-)
	# so move it via Body container so the BoundBox will not change ;-) LOL
	[ coX, coY, coZ, coR ] = getContainersOffset(iObj)
	body.Placement.Base.x = body.Placement.Base.x + coX
	body.Placement.Base.y = body.Placement.Base.y + coY
	body.Placement.Base.z = body.Placement.Base.z + coZ
	moveToFirst([ part ], iObj)

	doc.recompute()

	return [ part, body, sketch, pad ]


# ###################################################################################################################
'''
# Measurements
'''
# ###################################################################################################################


# ###################################################################################################################
def createMeasureExpression(iP1, iP2, iObject1, iObject2, iSubName1, iSubName2):
	'''
	Description:
	
		This function creates measurement expression. It is used by showMeasure function.
	
	Args:
	
		iP1: FreeCAD.Vector(x, y, z), Vertex object, or array with floats, for start
		iP2: FreeCAD.Vector(x, y, z), Vertex object, or array with floats, for end
		iObject1: object for start
		iObject2: object for end
		iSubName1: string with sub-object name for start, for example "Vertex1", "Edge1", "Face1"
		iSubName2: string with sub-object name for end, for example "Vertex1", "Edge1", "Face1"
		
	Usage:
	
		[ exprSX, exprSY, exprSZ, 
		exprEX, exprEY, exprEZ ] = MagicPanels.createMeasureExpression(iP1, iP2, obj1, obj2, "Vertex1", "Face2")

	Result:
	
		Create measure expressions for iSubName1 and iSubName2. 

	'''

	sub1Type = ""
	sub1Index = ""
	sub1Owner = iObject1
	sub1Object = sub1Owner.getSubObject(iSubName1)
	[ sub1OffsetX, sub1OffsetY, sub1OffsetZ, r1 ] = getContainersOffset(sub1Owner)
	
	sub2Type = ""
	sub2Index = ""
	sub2Owner = iObject2
	sub2Object = sub2Owner.getSubObject(iSubName2)
	[ sub2OffsetX, sub2OffsetY, sub2OffsetZ, r2 ] = getContainersOffset(sub2Owner)
	
	# ########################################################################################
	# set iSubName1
	# ########################################################################################
	
	if iSubName1.startswith("Edge"):
		sub1Type = "Edge"
		sub1Index = int(iSubName1.replace("Edge",""))-1
	
		if hasattr(sub1Object, "Curve"):
			
			if sub1Object.Curve.isDerivedFrom("Part::GeomLine"):
				exprSX = "<<" + str(sub1Owner.Label) + ">>.Shape.Edges[" + str(sub1Index) + "].Vertex"+"es[0].X + " + str(sub1OffsetX)
				exprSY = "<<" + str(sub1Owner.Label) + ">>.Shape.Edges[" + str(sub1Index) + "].Vertex"+"es[0].Y + " + str(sub1OffsetY)
				exprSZ = "<<" + str(sub1Owner.Label) + ">>.Shape.Edges[" + str(sub1Index) + "].Vertex"+"es[0].Z + " + str(sub1OffsetZ)
		
			if sub1Object.Curve.isDerivedFrom("Part::GeomCircle") or sub1Object.Curve.isDerivedFrom("Part::GeomEllipse"):
				exprSX = "<<" + str(sub1Owner.Label) + ">>.Shape.Edges[" + str(sub1Index) + "].Curve.Location.x + " + str(sub1OffsetX)
				exprSY = "<<" + str(sub1Owner.Label) + ">>.Shape.Edges[" + str(sub1Index) + "].Curve.Location.y + " + str(sub1OffsetY)
				exprSZ = "<<" + str(sub1Owner.Label) + ">>.Shape.Edges[" + str(sub1Index) + "].Curve.Location.z + " + str(sub1OffsetZ)


	if iSubName1.startswith("Vertex"):
		sub1Type = "Vertex"
		sub1Index = int(iSubName1.replace("Vertex",""))-1
	
		exprSX = "<<" + str(sub1Owner.Label) + ">>.Shape.Vertex"+"es[" + str(sub1Index) + "].X + " + str(sub1OffsetX)
		exprSY = "<<" + str(sub1Owner.Label) + ">>.Shape.Vertex"+"es[" + str(sub1Index) + "].Y + " + str(sub1OffsetY)
		exprSZ = "<<" + str(sub1Owner.Label) + ">>.Shape.Vertex"+"es[" + str(sub1Index) + "].Z + " + str(sub1OffsetZ)
	
	# ########################################################################################
	# set iSubName2
	# ########################################################################################
	
	if iSubName2.startswith("Edge"):
		sub2Type = "Edge"
		sub2Index = int(iSubName2.replace("Edge",""))-1
		
		if hasattr(sub2Object, "Curve"):
			
			if sub2Object.Curve.isDerivedFrom("Part::GeomLine"):
				
				# for single line edge
				if iSubName1.startswith("Edge") and sub1Object.Curve.isDerivedFrom("Part::GeomLine"):
					exprEX = "<<" + str(sub2Owner.Label) + ">>.Shape.Edges[" + str(sub2Index) + "].Vertex"+"es[1].X + " + str(sub2OffsetX)
					exprEY = "<<" + str(sub2Owner.Label) + ">>.Shape.Edges[" + str(sub2Index) + "].Vertex"+"es[1].Y + " + str(sub2OffsetY)
					exprEZ = "<<" + str(sub2Owner.Label) + ">>.Shape.Edges[" + str(sub2Index) + "].Vertex"+"es[1].Z + " + str(sub2OffsetZ)
				
				# from vertex or hole to edge
				else:
					
					exprEX = exprSX
					exprEY = exprSY
					exprEZ = exprSZ
					
					axis = getVectorsPlane(iP1, iP2)
					
					if axis == "X":
						exprEX = "<<" + str(sub2Owner.Label) + ">>.Shape.Edges[" + str(sub2Index) + "].CenterOfMass.x + " + str(sub2OffsetX)

					if axis == "Y":
						exprEY = "<<" + str(sub2Owner.Label) + ">>.Shape.Edges[" + str(sub2Index) + "].CenterOfMass.y + " + str(sub2OffsetY)
					
					if axis == "Z":
						exprEZ = "<<" + str(sub2Owner.Label) + ">>.Shape.Edges[" + str(sub2Index) + "].CenterOfMass.z + " + str(sub2OffsetZ)

			if sub2Object.Curve.isDerivedFrom("Part::GeomCircle") or sub2Object.Curve.isDerivedFrom("Part::GeomEllipse"):
				exprEX = "<<" + str(sub2Owner.Label) + ">>.Shape.Edges[" + str(sub2Index) + "].Curve.Location.x + " + str(sub2OffsetX)
				exprEY = "<<" + str(sub2Owner.Label) + ">>.Shape.Edges[" + str(sub2Index) + "].Curve.Location.y + " + str(sub2OffsetY)
				exprEZ = "<<" + str(sub2Owner.Label) + ">>.Shape.Edges[" + str(sub2Index) + "].Curve.Location.z + " + str(sub2OffsetZ)
	
	if iSubName2.startswith("Vertex"):
		sub2Type = "Vertex"
		sub2Index = int(iSubName2.replace("Vertex",""))-1
	
		exprEX = "<<" + str(sub2Owner.Label) + ">>.Shape.Vertex"+"es[" + str(sub2Index) + "].X + " + str(sub2OffsetX)
		exprEY = "<<" + str(sub2Owner.Label) + ">>.Shape.Vertex"+"es[" + str(sub2Index) + "].Y + " + str(sub2OffsetY)
		exprEZ = "<<" + str(sub2Owner.Label) + ">>.Shape.Vertex"+"es[" + str(sub2Index) + "].Z + " + str(sub2OffsetZ)
	
	if iSubName2.startswith("Face"):
		sub2Type = "Face"
		sub2Index = int(iSubName2.replace("Face",""))-1
	
		exprEX = exprSX
		exprEY = exprSY
		exprEZ = exprSZ
		
		plane = getFacePlane(sub2Object)
		
		if plane == "YZ":
			exprEX = "<<" + str(sub2Owner.Label) + ">>.Shape.Faces[" + str(sub2Index) + "].CenterOfMass.x + " + str(sub2OffsetX)
		if plane == "XZ":
			exprEY = "<<" + str(sub2Owner.Label) + ">>.Shape.Faces[" + str(sub2Index) + "].CenterOfMass.y + " + str(sub2OffsetY)
		if plane == "XY":
			exprEZ = "<<" + str(sub2Owner.Label) + ">>.Shape.Faces[" + str(sub2Index) + "].CenterOfMass.z + " + str(sub2OffsetZ)
	
	# ########################################################################################
	# return
	# ########################################################################################
	
	return [ exprSX, exprSY, exprSZ, exprEX, exprEY, exprEZ ]


# ###################################################################################################################
def showMeasure(iP1, iP2, iObject1="", iObject2="", iSubName1="", iSubName2="", iType=0, iParametric="no"):
	'''
	Description:
	
		This function creates measurement object and return it.
	
	Args:
	
		iP1: FreeCAD.Vector(x, y, z), Vertex object, or array with floats, for start
		iP2: FreeCAD.Vector(x, y, z), Vertex object, or array with floats, for end
		iObject1 (optional): object for iP1
		iObject2 (optional): object for iP2
		iSubName1 (optional): string with sub-object name for iP1, for example "Vertex1", "Edge1", "Face1"
		iSubName2 (optional): string with sub-object name for iP2, for example "Vertex1", "Edge1", "Face1"
		iType (optional): integer:
			* 0: to show measurement as PartDesign object
			* 1: to show measurement as Draft object (green color)
			* 2: to show measurement as Draft object (yellow color)
			* 3: to show measurement as Draft object (black color)
			* 4: to show measurement as Draft object (red color)
			* 5: to show measurement as Draft object (art handwrite green color)
			* 6: to show measurement as Draft object (art handwrite yellow color)
			* 7: to show measurement as Draft object (art handwrite black color)
			* 8: to show measurement as Draft object (art handwrite red color)
		iParametric (optional): string:
			* "no" (default): you have to add iP1 and iP2 and the measurement will not be parametric
			* "yes": you have to add iObject1, iObject2, iSubName1, iSubName2, and the measurement will be parametric

		# > [!NOTE]
		# > The iP1, iP2 should be global and are mandatory, because I do not want to overload this function
		# > with global position calculation from SubNames for each sub-type.
		# > If you want to have dimline position you have to add iObject1 and iSubName1 as well.
		# > The iObject2, iSubName2 is needed only for parametric version and reference info. 
		
	Usage:
	
		p1 = [0, 0, 0]
		p2 = [100, 0, 0]

		# for non-parametric simple PartDesign style
		m = MagicPanels.showMeasure(p1, p2)
		
		# for parametric Draft auto-position dimline style
		m = MagicPanels.showMeasure(p1, p2, obj1, obj2, "Vertex1", "Face2", 4, "yes")

	Result:
	
		Create measure object, draw it and return measure object for further processing. 

	'''


	# #############################################################################
	# convert input to Vectors
	# #############################################################################
	
	vectorStart = ""
	vectorEnd = ""
	
	try:
		if hasattr(iP1, "X"):
			vectorStart = FreeCAD.Vector(iP1.X, iP1.Y, iP1.Z)
		if hasattr(iP2, "X"):
			vectorEnd = FreeCAD.Vector(iP2.X, iP2.Y, iP2.Z)
	except:
		skip = 1

	if vectorStart == "":
		try:
			vectorStart = FreeCAD.Vector(iP1[0], iP1[1], iP1[2])
		except:
			skip = 1
	
	if vectorEnd == "":
		try:
			vectorEnd = FreeCAD.Vector(iP2[0], iP2[1], iP2[2])
		except:
			skip = 1
	
	if vectorStart == "" or vectorEnd == "":
		return "you have to add correct iP1 and iP2"
		
	# #############################################################################
	# to show measurement as PartDesign object
	# #############################################################################
	if iType == 0:

		# support for FreeCAD 1.0+
		if gKernelVersion >= 1.0:
			
			try:
				m = FreeCAD.ActiveDocument.addObject('Measure::MeasureDistanceDetached', "measure")
				
				m.Position1 = vectorStart
				m.Position2 = vectorEnd
				
				m.ViewObject.LineColor = (1.0, 0.0, 0.0, 0.0)
				m.ViewObject.TextColor = (1.0, 0.0, 0.0, 0.0)
				m.ViewObject.FontSize = 24

				# avoid FreeCAD automatic labeling bug and crash
				label = str(m.Name)
				if str(m.Name) == "measure":
					label = translate("showMeasure", "Measure")
				else:
					label = translate("showMeasure", "Measure") + " " + str(m.Name)[7:]
					
				m.Label = label
		
			except:
				skip = 1

		# support for FreeCAD 0.21.2
		else:
			
			try:
				m = FreeCAD.ActiveDocument.addObject('App::MeasureDistance', "measure")
				
				m.P1 = vectorStart
				m.P2 = vectorEnd
				
				m.ViewObject.LineColor = (1.0, 0.0, 0.0, 0.0)
				m.ViewObject.TextColor = (1.0, 0.0, 0.0, 0.0)
				m.ViewObject.FontSize = 24
				m.ViewObject.DistFactor = 0.25

				m.Label = translate("showMeasure", "Measure") + " "

			except:
				skip = 1
		
	# #############################################################################
	# to show measurement as Draft object (more detailed)
	# #############################################################################
	if iType >= 1 and iType <= 8:
		
		import Draft
		
		# create measurement object
		distance = round(vectorStart.distanceToPoint(vectorEnd), gRoundPrecision)
		m = Draft.make_linear_dimension(vectorStart, vectorEnd)
		
		try:
			prefix = translate("showMeasure", "Measure") + ", "
			m.Label = prefix + str(distance) + ", " + str(iObject1.Label) + " "
		except:
			skip = 1
		
		m.recompute()
		
		# set dimline offset from object
		dimlineOffset = distance / 9
		dimlineOffsetX = 0
		dimlineOffsetY = 0
		dimlineOffsetZ = 0
		
		# try to set iObject1
		o1Center = ""
		if hasattr(iObject1.Shape, "CenterOfMass"):
			o1Center = iObject1.Shape.CenterOfMass
		else:
			if hasattr(iObject1.Shape, "CenterOfGravity"):
				o1Center = iObject1.Shape.CenterOfGravity
		
		# try to position text only if there is access to center of the first selected object
		if o1Center != "":
			
			[ o1Center ] = getVerticesPosition([ o1Center ], iObject1, "vector")
			plane = getVectorsPlane(vectorStart, vectorEnd)
			
			if plane == "X":
				
				if o1Center.z > vectorStart.z:
					dimlineOffsetZ = - dimlineOffset
				else:
					dimlineOffsetZ = dimlineOffset

				m.Dimline = (vectorStart.x, vectorStart.y, vectorStart.z + dimlineOffsetZ)
				m.Normal = FreeCAD.Vector(1, -1, 0)
			
				if vectorStart.x < vectorEnd.x:
					m.ViewObject.FlipText = False
				else:
					m.ViewObject.FlipText = True
					
			if plane == "Y":
				
				if o1Center.z > vectorStart.z:
					dimlineOffsetZ = - dimlineOffset
				else:
					dimlineOffsetZ = dimlineOffset

				m.Dimline = (vectorStart.x, vectorStart.y, vectorStart.z + dimlineOffsetZ)
				m.Normal = FreeCAD.Vector(1, 0, 0)

			if plane == "Z":
				
				if o1Center.x > vectorStart.x:
					dimlineOffsetX = - dimlineOffset
				else:
					dimlineOffsetX = dimlineOffset

				m.Dimline = (vectorStart.x + dimlineOffsetX, vectorStart.y, vectorStart.z)
				m.Normal = FreeCAD.Vector(0, -1, 1)
				
				if vectorStart.z < vectorEnd.z:
					if o1Center.x < vectorStart.x + dimlineOffsetX:
						m.ViewObject.FlipText = True
					else:
						m.ViewObject.FlipText = False
				else:
					if o1Center.x < vectorStart.x + dimlineOffsetX:
						m.ViewObject.FlipText = False
					else:
						m.ViewObject.FlipText = True

		# set decoration
		m.ViewObject.FontSize = '3.5 mm'
		m.ViewObject.ShowLine = True
		m.ViewObject.LineWidth = 2
		m.ViewObject.FlipArrows = False
		m.ViewObject.ExtOvershoot = '2 mm'
		m.ViewObject.ExtLines = '13.5 mm'
		m.ViewObject.DimOvershoot = '0 mm'
		m.ViewObject.TextSpacing = '0.5 mm'
		
		# settings for FreeCAD 1.1
		if hasattr(m.ViewObject, "ArrowTypeStart"):
			m.ViewObject.ArrowTypeStart = u"Arrow"
		if hasattr(m.ViewObject, "ArrowTypeEnd"):
			m.ViewObject.ArrowTypeEnd = u"Arrow"
		
		if hasattr(m.ViewObject, "ArrowSizeStart"):
			m.ViewObject.ArrowSizeStart = '0.5 mm'
		if hasattr(m.ViewObject, "ArrowSizeEnd"):
			m.ViewObject.ArrowSizeEnd = '0.5 mm'
		
		# backward compatibility
		if hasattr(m.ViewObject, "ArrowType"):
			m.ViewObject.ArrowType = u"Arrow"
		if hasattr(m.ViewObject, "ArrowSize"):
			m.ViewObject.ArrowSize = '0.5 mm'
		
		m.ViewObject.ScaleMultiplier = float(distance / 30)
		
		m.ViewObject.Visibility = True
		m.ViewObject.ShowInTree = True
		
		# custom drawing style settings
		if iType == 1:
			m.ViewObject.LineColor = (0, 255, 0)
			m.ViewObject.TextColor = (0, 255, 0)
			m.ViewObject.DisplayMode = u"World"
		if iType == 2:
			m.ViewObject.LineColor = (255, 255, 0)
			m.ViewObject.TextColor = (255, 255, 0)
			m.ViewObject.DisplayMode = u"World"
		if iType == 3:
			m.ViewObject.LineColor = (0, 0, 0)
			m.ViewObject.TextColor = (0, 0, 0)
			m.ViewObject.DisplayMode = u"World"
		if iType == 4:
			m.ViewObject.LineColor = (255, 0, 0)
			m.ViewObject.TextColor = (255, 0, 0)
			m.ViewObject.DisplayMode = u"World"
		if iType == 5:
			m.ViewObject.LineColor = (0, 255, 0)
			m.ViewObject.TextColor = (0, 255, 0)
			m.ViewObject.DisplayMode = u"World"
			m.ViewObject.FontName = "Chilanka"
		if iType == 6:
			m.ViewObject.LineColor = (255, 255, 0)
			m.ViewObject.TextColor = (255, 255, 0)
			m.ViewObject.DisplayMode = u"World"
			m.ViewObject.FontName = "Chilanka"
		if iType == 7:
			m.ViewObject.LineColor = (0, 0, 0)
			m.ViewObject.TextColor = (0, 0, 0)
			m.ViewObject.DisplayMode = u"World"
			m.ViewObject.FontName = "Chilanka"
		if iType == 8:
			m.ViewObject.LineColor = (255, 0, 0)
			m.ViewObject.TextColor = (255, 0, 0)
			m.ViewObject.DisplayMode = u"World"
			m.ViewObject.FontName = "Chilanka"
	
	# #############################################################################
	# set references and Label2 cut-list description
	# #############################################################################
	
	ref1 = ""
	ref2 = ""
	
	if iObject1 != "" and iSubName1 != "":
		ref1 = str(iObject1.Name) + ", " + str(iSubName1)
	
	if iObject2 != "" and iSubName2 != "":
		ref2 = str(iObject2.Name) + ", " + str(iSubName2)
	
	if ref1 != "" or ref2 != "":
		m.Label2 = ref1 + " ---> " + ref2
		
	# #############################################################################
	# set attributes
	# #############################################################################
	
	# set show attribute for cut-list
	if not hasattr(m, "Woodworking_BOM"):
		info = translate("showMeasure", "Allows to skip measurement at BOM, cut-list report.")
		m.addProperty("App::PropertyBool", "Woodworking_BOM", "Woodworking", info)
		m.Woodworking_BOM = True

	# set correct object type
	if not hasattr(m, "Woodworking_Type"):
		info = translate("showMeasure", "Measurement object type.")
		m.addProperty("App::PropertyString", "Woodworking_Type", "Woodworking", info)
		m.Woodworking_Type = "Measurement"

	# set reference for selection 1
	if not hasattr(m, "Woodworking_Ref1"):
		info = translate("showMeasure", "Reference for selection 1.")
		m.addProperty("App::PropertyString", "Woodworking_Ref1", "Woodworking", info)
		m.Woodworking_Ref1 = ref1
	
	# set reference for selection 2
	if not hasattr(m, "Woodworking_Ref2"):
		info = translate("showMeasure", "Reference for selection 2.")
		m.addProperty("App::PropertyString", "Woodworking_Ref2", "Woodworking", info)
		m.Woodworking_Ref2 = ref2
	
	# add remove attribute for auto-remove purposes
	if not hasattr(m, "Woodworking_Remove"):
		info = translate("showMeasurements", "Allows to remove this measurement via script.")
		m.addProperty("App::PropertyBool", "Woodworking_Remove", "Woodworking", info)
		m.Woodworking_Remove = False

	# #############################################################################
	# set measurements parametric
	# #############################################################################
	
	if iParametric == "yes":
		
		[ exprSX, exprSY, exprSZ, 
		exprEX, exprEY, exprEZ ] = createMeasureExpression(iP1, iP2, iObject1, iObject2, iSubName1, iSubName2)
		
		if iType == 0:
			
			m.setExpression('.Position1.x', exprSX)
			m.setExpression('.Position1.y', exprSY)
			m.setExpression('.Position1.z', exprSZ)
			m.setExpression('.Position2.x', exprEX)
			m.setExpression('.Position2.y', exprEY)
			m.setExpression('.Position2.z', exprEZ)
		
		if iType >= 1 and iType <= 8:
			
			m.setExpression('.Start.x', exprSX)
			m.setExpression('.Start.y', exprSY)
			m.setExpression('.Start.z', exprSZ)
			m.setExpression('.End.x', exprEX)
			m.setExpression('.End.y', exprEY)
			m.setExpression('.End.z', exprEZ)
			
			m.setExpression('.Dimline.x', '.Start.x + ' + str(dimlineOffsetX) + ' mm')
			m.setExpression('.Dimline.y', '.Start.y + ' + str(dimlineOffsetY) + ' mm')
			m.setExpression('.Dimline.z', '.Start.z + ' + str(dimlineOffsetZ) + ' mm')

	# #############################################################################
	# recompute & return
	# #############################################################################
	m.recompute()
	FreeCAD.ActiveDocument.recompute()
	FreeCADGui.Selection.clearSelection()

	return m
	
	
# ###################################################################################################################
def getDistanceBetweenFaces(iObj1, iObj2, iFace1, iFace2):
	'''
	Description:
	
		Gets distance between iFace1 and iFace2.
	
	Args:
	
		iObj1: object of iFace1
		iObj2: object of iFace2
		iFace1: face object
		iFace2: face object

	Usage:
	
		size = MagicPanels.getDistanceBetweenFaces(o1, o2, face1, face2)

	Result:

		return distance between face1 object and face2 object

	'''

	plane1 = getFacePlane(iFace1)
	plane2 = getFacePlane(iFace2)
	[ x1, y1, z1 ] = getVertex(iFace1, 0, 0)
	[ x2, y2, z2 ] = getVertex(iFace2, 0, 0)

	# if you switch to global be sure the planes are not rotated
	[[ x1, y1, z1 ]] = getVerticesPosition([[ x1, y1, z1 ]], iObj1)
	[[ x2, y2, z2 ]] = getVerticesPosition([[ x2, y2, z2 ]], iObj2)
	
	if plane1 == "XY" and plane2 == "XY":
		return round(abs(z1-z2), gRoundPrecision)

	if plane1 == "XZ" and plane2 == "XZ":
		return round(abs(y1-y2), gRoundPrecision)
		
	if plane1 == "YZ" and plane2 == "YZ":
		return round(abs(x1-x2), gRoundPrecision)

	return ""


# ###################################################################################################################
'''
# Units
'''
# ###################################################################################################################


# ###################################################################################################################
def unit2gui(iValue):
	'''
	Description:
	
		Allows to convert unit from value (mm float FreeCAD format) into gui user settings.

	Args:

		iValue: float from FreeCAD or from calculations
		
	Usage:

		unitForUser = MagicPanels.unit2gui(300.55)
		
		# > [!NOTE]
		# > if user has set inches units the unitForUser should contains recalculation to inches 
		
	Result:

		string

	'''


	# fix FreeCAD 1.1 bug
	userSettings = 0
	try:
		userSettings = Units.getSchema()
		if userSettings > len(Units.listSchemas()) - 1:
			userSettings = 0
	except:
		skip = 1

	value = Units.Quantity( str(iValue) + " mm" )
	forUser = Units.schemaTranslate(value, userSettings)[0]

	# fix for FreeCAD bug with "Building US", 
	# only "0 mm" is translated to "0" value without units
	# see: https://github.com/dprojects/Woodworking/issues/57#issuecomment-2841510545
	if userSettings == 5:
		try:
			float(forUser)
			forUser = str(forUser) + " in"
		except:
			skip = 1

	return str(forUser)


# ###################################################################################################################
def unit2value(iString):
	'''
	Description:
	
		Allows to convert user unit string into float for calculation. 

	Args:

		iString: units string in user settings notation, for example "5 mm", "5 in", "5 ft", 
		but also accept quick value notation like "500" for all units schemas.
		
	Usage:
		
		forCalculation = MagicPanels.unit2value("18 mm")
		forCalculation = MagicPanels.unit2value("0.06 ft") # forCalculation will be 18.288
		forCalculation = MagicPanels.unit2value("18")
		forCalculation = MagicPanels.unit2value("0")

	Result:

		float for calculation

	'''


	unitString = str(iString)

	# fix FreeCAD 1.1 bug
	userSettings = 0
	try:
		userSettings = Units.getSchema()
		if userSettings > len(Units.listSchemas()) - 1:
			userSettings = 0
	except:
		skip = 1

	# fix FreeCAD Building US units schema conversion syntax bug 
	# https://github.com/dprojects/Woodworking/issues/63
	try:
		if userSettings == 5:
			unitString = unitString.replace("+","--")

	except:
		skip = 1
	
	# quick value notation
	try:
		value = unitString.replace(",",".")
		float(value)
		
		unit = Units.schemaTranslate( Units.Quantity("1.0 mm"), userSettings )[2]
		unitString = str(value) + " " + str(unit)

	except:
		skip = 1

	forCalculation = Units.Quantity(str(unitString)).getValueAs("mm")

	return float(forCalculation)


# ###################################################################################################################
def unitArea2gui(iValue):
	'''
	Description:
	
		Allows to convert area value (mm float FreeCAD format) into gui user settings.

	Args:

		iValue: float from FreeCAD or from calculations
		
	Usage:

		areaString = MagicPanels.unitArea2gui(180000)

	Result:

		string, for example "180000 mm^2"

	'''


	# fix FreeCAD 1.1 bug
	userSettings = 0
	try:
		userSettings = Units.getSchema()
		if userSettings > len(Units.listSchemas()) - 1:
			userSettings = 0
	except:
		skip = 1

	value = Units.Quantity( str(iValue) + " mm^2" )
	forUser = Units.schemaTranslate(value, userSettings)[0]

	# fix for FreeCAD bug with "Building US", 
	# only "0 mm" is translated to "0" value without units
	# see: https://github.com/dprojects/Woodworking/issues/57#issuecomment-2841510545
	if userSettings == 5:
		try:
			float(forUser)
			forUser = str(forUser) + " in^2"
		except:
			skip = 1

	return str(forUser)


# ###################################################################################################################
def unit2fractions(iValue, iPrecision=0, iReduction="no", iPrefix=""):
	'''
	Description:
	
		Allows to convert unit from value (mm float FreeCAD format) into fractions string X' Y n/d" or X' Y-n/d". 
		X' represents a whole number of feet. Y represents a whole number of inches and n/d" represents 
		a fraction of an inch, where n is the numerator and d is the denominator.
		
		# > [!NOTE]
		# > This function not reduce fraction part by default (keeps the denominator the same as given iPrecision).

	Args:

		iValue: float from FreeCAD or from calculations
		iPrecision: integer value
			0: read from user settings: "User parameter:BaseApp/Preferences/Units/FracInch"
			value: denominator in fraction part, for example 128, if there will be bug the default will be set to 32
		iReduction: string
			"system": the fraction part will by reduced by system
			"no" (default): not reduce the fraction part
			"python": reduce the fraction part via python fractions module, but in this case the denominator might be changed also
		iPrefix: string
			"": means single space between Y inches part and n/d fraction part
			"-": means minus between Y inches part and n/d fraction part, however this notation can be considered by human ad subtraction operation, 11-5/8" might be interpreted by human as 10 3/8"
		
	Usage:

		unitForUser = MagicPanels.unit2fractions(464, 128, "system", "")
		result: 1' 6 1/4"

		unitForUser = MagicPanels.unit2fractions(464, 128, "system", "-")
		result: 1' 6-1/4"

		unitForUser = MagicPanels.unit2fractions(464, 128, "no", "")
		result: 1' 6 34/128"

		unitForUser = MagicPanels.unit2fractions(464, 128, "no", "-")
		result: 1' 6-34/128"

		unitForUser = MagicPanels.unit2fractions(464, 128, "python", "")
		result: 1' 6 34/127"

		unitForUser = MagicPanels.unit2fractions(464, 128, "python", "-")
		result: 1' 6-34/127"

		unitForUser = MagicPanels.unit2fractions(464, 8, "no", "")
		result: 1' 6 2/8"

		unitForUser = MagicPanels.unit2fractions(464, 8, "system", "")
		result: 1' 6 1/4"

	Result:

		string for GUI

	'''


	if iReduction == "system":

		if iPrefix == "":
			forUser = unit2gui(iValue)
			forUser = forUser.replace("\" + "," ")
			
		if iPrefix == "-":
			forUser = unit2gui(iValue)
			forUser = forUser.replace("\" + ","-")
			
		return forUser

	import math
	
	# defaults
	inch = float(0.0393700787)    # 1 mm in inches
	foot = int(12)                # 1 foot in inches

	# set default precision
	precision = iPrecision
	if precision == 0:
		try:
			us = FreeCAD.ParamGet('User parameter:BaseApp/Preferences/Units')
			precision = us.GetInt('FracInch') # if not defined return 0
		except:
			precision = 0

	# set default in case of bug
	if precision == 0:
		precision = 32

	# convert float in mm to inches
	inches = iValue * inch
	
	# calculate X (whole feet)
	X = math.floor(inches / foot)
	
	# calculate remaining inches
	rinches = inches - (X * foot)
	
	# calculate Y (whole inches)
	Y = math.floor(rinches)

	# calculate n / d (fractional part)
	finches = rinches - Y
	
	# by default not reduce
	if iReduction == "no":
	
		t = finches * precision
		tC = math.ceil(t)
		tF = math.floor(t)
		
		diffC = abs(t - tC)
		diffF = abs(t - tF)
		
		if diffC < diffF:
			n = tC
		else:
			n = tF
		
		d = precision
	
	# makes denominator 127 not 128, Python library bug?
	if iReduction == "python":
		from fractions import Fraction
		
		if precision != 0:
			fr = Fraction(str(finches)).limit_denominator(precision)
		else:
			fr = Fraction.from_float(finches)
		
		n = fr.numerator
		d = fr.denominator
	
	# create string for user
	forUser = ""
	if X != 0:
		forUser += str(X) + "' "

	if Y != 0:
		if iPrefix == "-":
			forUser += str(Y) + "-"
		else:
			forUser += str(Y) + " "

	if n != 0:
		forUser += str(n) + "/" + str(d) + '"'

	return forUser
	

# ###################################################################################################################
'''
# Colors
'''
# ###################################################################################################################


# ###################################################################################################################
def convertColor(iColor, iTarget):
	'''
	Description:
	
		Converts colors.

	Args:

		iColor: 
		
			possible formats from FreeCAD to RGBA:
			* tuple with floats: ( 0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 1.0 )
			* array with floats: [ 0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 1.0 ]
			* array with tuples: [ (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0) ]
			* array with arrays: [ [1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0] ]
			
			possible formats from RGBA to FreeCAD:
			* array with RGBA ints: [ 255, 0, 0, 255 ]
			* array with RGBA arrays: [ [255, 0, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255] ]
			
		iTarget: string:
			* "kernel": converts RGBA to FreeCAD tuple with floats (for array as well)
			* "RGBA": converts FreeCAD floats to RGBA array

	Usage:

		color = MagicPanels.convertColor([ 247, 185, 108, 255 ], "kernel")
		
		colorTuple = (0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 1.0)
		color = MagicPanels.convertColor(colorTuple, "RGBA")
		
		colorArray = [ 0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 1.0 ]
		color = MagicPanels.convertColor(colorArray, "RGBA")
		
		color = MagicPanels.convertColor(obj.ViewObject.DiffuseColor, "RGBA")

	Result:

		returns converted color

	'''


	if iTarget == "kernel":
		
		# array
		if type(iColor) is list:
			
			# array with arrays
			if type(iColor[0]) is list:

				colorToSet = []
				for c in iColor:
					r = float(c[0] / 255)
					g = float(c[1] / 255)
					b = float(c[2] / 255)
					a = float(c[3] / 255)
					colorToSet.append( tuple( [ r, g, b, a ] ) )
			
			# single array
			else:
				r = float(iColor[0] / 255)
				g = float(iColor[1] / 255)
				b = float(iColor[2] / 255)
				a = float(iColor[3] / 255)
				colorToSet = tuple( [ r, g, b, a ] )
		
		return colorToSet

	if iTarget == "RGBA":
		
		# single tuple
		if type(iColor) is tuple:
			r = int(iColor[0] * 255)
			g = int(iColor[1] * 255)
			b = int(iColor[2] * 255)
			a = int(iColor[3] * 255)
			colorToSet = [ r, g, b, a ]
		
		# array
		elif type(iColor) is list:
			
			# array with arrays or tuples
			if type(iColor[0]) is list or type(iColor[0]) is tuple:
				
				colorToSet = []
				
				for c in iColor:
					r = int(c[0] * 255)
					g = int(c[1] * 255)
					b = int(c[2] * 255)
					a = int(c[3] * 255)
					colorToSet.append([ r, g, b, a ])
			
			# array with floats
			else:
				r = int(iColor[0] * 255)
				g = int(iColor[1] * 255)
				b = int(iColor[2] * 255)
				a = int(iColor[3] * 255)
				colorToSet = [ r, g, b, a ]
		
		# only array or tuple is supported
		else:
			return ""
		
		return colorToSet

	return ""


# ###################################################################################################################
def getColor(iObj, iFaceIndex, iAttribute="color", iType="kernel"):
	'''
	Description:
	
		Allows to get color for object or face.

	Args:

		iObj: object
		iFaceIndex: index to get color for face or 0 to get color for object
		iAttribute: string, attribute name from FreeCAD.Material structure, e.g.:
			* "color": to get color from DiffuseColor attribute
			* "trans": to get color from Transparency attribute
			* "DiffuseColor": to get color from DiffuseColor attribute
			* "AmbientColor": to get color from AmbientColor attribute
			* "SpecularColor": to get color from SpecularColor attribute
			* "EmissiveColor": to get color from EmissiveColor attribute
			* "Shininess": to get color from Shininess attribute
			* "Transparency": to get color from Transparency attribute
		iType (optional): string to describe the color type
			* "kernel" (default): return tuple with floats
			* "RGBA": return RGBA array with integers [ r, g, b, a ] 

	Usage:

		colorTuple = MagicPanels.getColor(o, 0, "color") # to get object color
		colorTuple = MagicPanels.getColor(o, 5, "color") # to get face5 color
		
		[ r, g, b, a ] = MagicPanels.getColor(o, 0, "color", "RGBA") # to get object color
		[ r, g, b, a ] = MagicPanels.getColor(o, 5, "color", "RGBA") # to get face5 color

	Result:

		Returns color in desired format or empty string.
		
		For FreeCAD 0.21.2 returns color for object from .ViewObject.ShapeColor or 
		color for face from .ViewObject.DiffuseColor.
		
		Since FreeCAD 1.0+ there is no .ViewObject.ShapeColor for object. Color for object 
		and faces are stored only at .ViewObject.ShapeAppearance behind FreeCAD.Material 
		structure. If all the faces have the same color there is only one Material object. 
		But for example if only single face have different color, there are Material objects 
		for all faces, but there is no color for object. So in this case the color for 
		object cannot be determined, so will be returned as empty string "". 

	'''


	# init return color
	returnColor = ""
	
	# ############################################################################
	# support for FreeCAD 1.0+
	# ############################################################################
	if gKernelVersion >= 1.0:
	
		# set target attribute
		if iAttribute == "color":
			attribute = "DiffuseColor"
		
		elif iAttribute == "trans":
			attribute = "Transparency"
		
		else:
			attribute = iAttribute
		
		# for example LinkGroup
		if returnColor == "":
			if not hasattr(iObj.ViewObject, "ShapeAppearance"):
				if hasattr(iObj.ViewObject, "ShapeMaterial"):
					if hasattr(iObj.ViewObject.ShapeMaterial, attribute):
						returnColor = getattr(iObj.ViewObject.ShapeMaterial, attribute)
		
		# continue for other objects
		if returnColor == "":
			try:
				num = len(iObj.ViewObject.ShapeAppearance)
			except:
				return ""
		
		# get color for object, all color faces the same
		if returnColor == "":
			if iFaceIndex == 0 and num == 1:
				m = iObj.ViewObject.ShapeAppearance[0]
				if hasattr(m, attribute):
					returnColor = getattr(m, attribute)
		
		# get color for face, all color faces the same
		if returnColor == "":
			if iFaceIndex != 0 and num == 1:
				m = iObj.ViewObject.ShapeAppearance[0]
				if hasattr(m, attribute):
					returnColor = getattr(m, attribute)
		
		# get color for face, already multi color faces
		if returnColor == "":
			if iFaceIndex != 0 and num != 1:
				m = iObj.ViewObject.ShapeAppearance[iFaceIndex-1]
				if hasattr(m, attribute):
					returnColor = getattr(m, attribute)

	# ############################################################################
	# support for FreeCAD 0.21.2 and below
	# ############################################################################
	else:
		
		# set target attribute
		if iAttribute == "color" or iAttribute == "DiffuseColor":
			attribute = "DiffuseColor"
		
		elif iAttribute == "trans" or iAttribute == "Transparency":
			attribute = "Transparency"
		
		else:
			return "not supported attribute in this version"
		
		# for example LinkGroup
		if returnColor == "":
			if not hasattr(iObj.ViewObject, "DiffuseColor"):
				if hasattr(iObj.ViewObject, "ShapeMaterial"):
					if hasattr(iObj.ViewObject.ShapeMaterial, attribute):
						returnColor = getattr(iObj.ViewObject.ShapeMaterial, attribute)
		
		# transparent will be from 1.0 schema in float
		if returnColor == "":
			if attribute == "Transparency":
				returnColor = float( int(iObj.ViewObject.Transparency) / 100 )
		
		# for object
		if returnColor == "":
			if iFaceIndex == 0:
				returnColor = iObj.ViewObject.ShapeColor
		
		# continue for other objects
		if returnColor == "":
			try:
				num = len(iObj.ViewObject.DiffuseColor)
			except:
				return ""
		
		# for face
		if returnColor == "":
			
			# if all faces are the same
			if num == 1:
				returnColor = iObj.ViewObject.DiffuseColor[0]
			
			# if multi color faces
			else:
				returnColor = iObj.ViewObject.DiffuseColor[iFaceIndex-1]

		# fix wrong alpha meaning
		if returnColor != "" and attribute != "Transparency":
			[ r, g, b, a ] = returnColor
			returnColor = tuple([ r, g, b, round( float(1 - a), 2 ) ])
			
	# ############################################################################
	# convert color & return final color
	# ############################################################################
	if returnColor != "":
		
		if iType == "RGBA":
			
			if attribute == "Shininess" or attribute == "Transparency":
				return int( round(returnColor * 100, 0) )
			else:
				return convertColor(returnColor, "RGBA")
		
		else:
			return returnColor
	else:
		return ""


# ###################################################################################################################
def setColor(iObj, iFaceIndex, iColor, iAttribute="color", iType="kernel"):
	'''
	Description:
	
		Allows to set color for object or face.

	Args:

		iObj: object
		iFaceIndex: index to set color for face or 0 to set color for object
		iColor: color according to the FreeCAD.Material structure, e.g.:
			* "DiffuseColor" - (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
			* "AmbientColor" - (0.33333298563957214, 0.33333298563957214, 0.33333298563957214, 1.0)
			* "SpecularColor" - (0.5333330035209656, 0.5333330035209656, 0.5333330035209656, 1.0)
			* "EmissiveColor" - (0.0, 0.0, 0.0, 1.0)
			* "Shininess" - float in range from 0.0 to 1.0, default is: 0.8999999761581421
			* "Transparency" - float in range from 0.0 (no transparent) to 1.0 (full transparent), default is: 0.0
		iAttribute: string, attribute name from FreeCAD.Material structure, e.g.:
			* "color" - to set color for DiffuseColor attribute
			* "trans" - to set color for Transparency attribute
			* "DiffuseColor" - to set color for DiffuseColor attribute
			* "AmbientColor" - to set color for AmbientColor attribute
			* "SpecularColor" - to set color for SpecularColor attribute
			* "EmissiveColor" - to set color for EmissiveColor attribute
			* "Shininess" - to set color for Shininess attribute
			* "Transparency" - to set color for Transparency attribute
		iType (optional): string to describe the color type
			* "kernel" (default): iColor will be tuple with floats
			* "RGBA": iColor will be RGBA array [ r, g, b, a ] 

	Usage:

		MagicPanels.setColor(o, 0, (1.0, 0.0, 0.0, 1.0), "color") # to set object color
		MagicPanels.setColor(o, 5, (1.0, 0.0, 0.0, 1.0), "color") # to set face5 color
		
		# to set colors for all faces, e.g. for dowel with 3 faces
		colors = [ (1.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0) ]
		MagicPanels.setColor(o, 0, colors, "color")
		
		or 
		
		MagicPanels.setColor(o, 0, [ 255, 0, 0, 255 ], "color", "RGBA") # to set object color
		MagicPanels.setColor(o, 5, [ 255, 0, 0, 255 ], "color", "RGBA") # to set face5 color
		
		# to set colors for all faces, e.g. for dowel with 3 faces
		colors = [ [ 255, 0, 0, 255 ], [ 0, 0, 0, 255 ], [ 0, 255, 0, 255 ] ]
		MagicPanels.setColor(o, 0, colors, "color", "RGBA")

	Result:

		return empty string if everything is fine or string with error info

	'''


	# init color to set
	colorToSet = iColor
	
	# ############################################################################
	# convert color
	# ############################################################################
	if iType == "RGBA":
		
		if (
			iAttribute == "Shininess" or 
			iAttribute == "Transparency" or 
			iAttribute == "trans"
		):
			colorToSet = float( int(iColor) / 100 )

		else:
			colorToSet = convertColor(iColor, "kernel")

	# ############################################################################
	# support for FreeCAD 1.0+
	# ############################################################################
	if gKernelVersion >= 1.0:
	
		# set target attribute
		if iAttribute == "color":
			attribute = "DiffuseColor"
		
		elif iAttribute == "trans":
			attribute = "Transparency"
		
		else:
			attribute = iAttribute

		# for example LinkGroup
		if not hasattr(iObj.ViewObject, "ShapeAppearance"):
			if hasattr(iObj.ViewObject, "ShapeMaterial"):
				if hasattr(iObj.ViewObject.ShapeMaterial, attribute):
					setattr(iObj.ViewObject.ShapeMaterial, attribute, colorToSet)
					return ""
		
		# continue for other objects
		try:
			num = len(iObj.ViewObject.ShapeAppearance)
		except:
			return "wrong .ViewObject.ShapeAppearance structure"
		
		# for all faces from array
		if type(colorToSet) is list:
			
			initSA = []
			for i in range(0, len(iObj.Shape.Faces)):
				m = iObj.ViewObject.ShapeAppearance[0]
				if hasattr(m, attribute):
					setattr(m, attribute, colorToSet[i])
					initSA.append(m)
				else:
					return "wrong iAttribute attribute"

			iObj.ViewObject.ShapeAppearance = tuple(initSA)
			
			return ""
		
		# for object, set the same color for all faces
		if iFaceIndex == 0:
			sa = iObj.ViewObject.ShapeAppearance
			m = sa[0]
			if hasattr(m, attribute):
				setattr(m, attribute, colorToSet)
				iObj.ViewObject.ShapeAppearance = ( m, )
			else:
				return "wrong iAttribute attribute"

			return ""

		# for face, if all faces has the same material structure
		if iFaceIndex != 0 and num == 1:
			
			sa = iObj.ViewObject.ShapeAppearance
			m = sa[0]
			
			# skip if there is no attribute to set (for example wrong object type)
			if not hasattr(m, attribute):
				return "wrong iAttribute attribute"
			
			# init new color structure with Material object from first face (object)
			initSA = []
			for f in iObj.Shape.Faces:
				initSA.append(m)
			
			iObj.ViewObject.ShapeAppearance = tuple(initSA)
			
			# replace attribute in Material structure for exact face
			sa = iObj.ViewObject.ShapeAppearance
			m = sa[iFaceIndex-1]
			setattr(m, attribute, colorToSet)
			iObj.ViewObject.ShapeAppearance = sa

			return ""

		# for face, if all faces has its own material structure
		if iFaceIndex != 0 and num != 1:
			sa = iObj.ViewObject.ShapeAppearance
			m = sa[iFaceIndex-1]
			if hasattr(m, attribute):
				setattr(m, attribute, colorToSet)
				iObj.ViewObject.ShapeAppearance = sa
			else:
				return "wrong iAttribute attribute"
			
			return ""
		
		return "not settings found"

	# ############################################################################
	# support for FreeCAD 0.21.2 and below
	# ############################################################################
	else:
		
		# set target attribute
		if iAttribute == "color" or iAttribute == "DiffuseColor":
			attribute = "DiffuseColor"
		
		elif iAttribute == "trans" or iAttribute == "Transparency":
			attribute = "Transparency"
		
		else:
			return "not supported attribute in this version"
		
		# transparent will be from 1.0 schema, to get float better precision
		if attribute == "Transparency":
			iObj.ViewObject.Transparency = int( round(colorToSet * 100, 0) )
			return ""
		
		# for all faces from array
		if type(colorToSet) is list:
			
			initSA = []
			for i in range(0, len(iObj.Shape.Faces)):
				
				# fix for wrong alpha meaning in FreeCAD 0.21.2
				[ r, g, b, a ] = colorToSet[i]
				m = tuple([ r, g, b, round( float(1 - a), 2 ) ])
				initSA.append(m)

			iObj.ViewObject.DiffuseColor = initSA
			return ""

		# for example LinkGroup
		if not hasattr(iObj.ViewObject, "DiffuseColor"):
			if hasattr(iObj.ViewObject, "ShapeMaterial"):
				if hasattr(iObj.ViewObject.ShapeMaterial, attribute):
					setattr(iObj.ViewObject.ShapeMaterial, attribute, colorToSet)
					return ""

		# fix for wrong alpha meaning in FreeCAD 0.21.2, 
		# the ShapeMaterial has good alpha meaning so not move it above
		[ r, g, b, a ] = colorToSet
		colorToSet = tuple([ r, g, b, round( float(1 - a), 2 ) ])

		# for object
		if iFaceIndex == 0:
			iObj.ViewObject.ShapeColor = colorToSet
			iObj.ViewObject.DiffuseColor = colorToSet
			return ""
		
		# continue for other objects
		try:
			num = len(iObj.ViewObject.DiffuseColor)
		except:
			return "wrong .ViewObject.DiffuseColor structure"
		
		# for face, all faces has the same color
		if iFaceIndex != 0 and num == 1:
			
			c = iObj.ViewObject.DiffuseColor[0]
			init = []
			for f in iObj.Shape.Faces:
				init.append(c)
			
			iObj.ViewObject.DiffuseColor = tuple(init)
			
			c = iObj.ViewObject.DiffuseColor
			c[iFaceIndex-1] = colorToSet
			iObj.ViewObject.DiffuseColor = c
			return ""

		# for face, multi color faces
		if iFaceIndex != 0 and num != 1:
			
			c = iObj.ViewObject.DiffuseColor
			c[iFaceIndex-1] = colorToSet
			iObj.ViewObject.DiffuseColor = c
			return ""

		return "not settings found"


# ###################################################################################################################
def copyColors(iSource, iTarget):
	'''
	Description:
	
		Allows to copy colors from iSource object to iTarget object.

	Args:

		iSource: source object
		iTarget: target object

	Usage:

		MagicPanels.copyColors(panel, copy)

	Result:

		All colors structure should be copied from source to target.

	'''


	try:
		color = getColor(iSource, 0, "color")
		if color == "":
			color = getColor(iSource, 1, "color")
		
		setColor(iTarget, 0, color, "color")

		return 0
	except:
		return -1


# ###################################################################################################################
'''
# Holes
'''
# ###################################################################################################################


# ###################################################################################################################
def makeHoles(iObj, iFace, iCylinders, iDrillPoint="Angled"):
	'''
	Description:
	
		Making holes.

	Args:

		iObj: base object to make hole
		iFace: face of base object to make hole
		iCylinders: list of cylinders to make holes below each one
		iDrillPoint (optional): "Angled" for normal conical hole or "Flat" for flat hole
		
	Usage:

		holes = MagicPanels.makeHoles(obj, face, cylinders)
		holes = MagicPanels.makeHoles(obj, face, cylinders, "Angled")
		holes = MagicPanels.makeHoles(obj, face, cylinders, "Flat")
		
	Result:

		Make holes and return list of holes.

	'''

	import Part, Sketcher

	holes = []

	base = iObj
	face = iFace
	objects = iCylinders
	
	# set body for base object
	if base.isDerivedFrom("Part::Box"):
		
		[ part, body, sketch, pad ] = makePad(base, base.Label)
		FreeCAD.ActiveDocument.removeObject(base.Name)
		FreeCAD.ActiveDocument.recompute()
		base = pad
		
	else:
		
		body = base._Body

	# loop in drill bits and drill holes
	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = FreeCAD.Vector(0, 0, 1)
		circleGeo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, o.Radius)
		holeSketch.addGeometry(circleGeo, False)
		
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1)) 
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 0, 2 * o.Radius)) 
		s = str(float(2 * o.Radius))+" mm"
		holeSketch.setDatum(1, FreeCAD.Units.Quantity(s))
		holeSketch.renameConstraint(1, u'Hole00Diameter')
		
		FreeCAD.ActiveDocument.recompute()
		
		# set position to hole Sketch
		[ x, y, z, r ] = getContainerPlacement(o, "clean")
		[[ x, y, z ]] = removeVerticesPosition([[ x, y, z ]], base, "array")
		
		setSketchPlacement(holeSketch, x, y, z, r, "global")
		FreeCAD.ActiveDocument.recompute()
		
		# create hole object
		hole = body.newObject('PartDesign::Hole','Hole')
		hole.Profile = holeSketch
		holeSketch.Visibility = False
		
		hole.Diameter = 2 * o.Radius
		hole.HoleCutDiameter = 2 * o.Radius
		hole.HoleCutDepth = o.Height
		hole.HoleCutCountersinkAngle = 90.000000
		hole.Depth = o.Height
		hole.DrillPointAngle = 118.000000
		hole.TaperedAngle = 90.000000
		hole.Threaded = 0
		hole.ThreadType = 0
		hole.HoleCutType = 0
		hole.DepthType = 0
		hole.DrillForDepth = 1
		hole.Tapered = 0
		hole.DrillPoint = iDrillPoint
		
		try:
			copyColors(hole.BaseFeature, hole)
		except:
			skip = 1
		
		FreeCAD.ActiveDocument.recompute()
		
		base = hole
		holes.append(hole)

	return holes
	

# ###################################################################################################################
def makeCountersinks(iObj, iFace, iCones):
	'''
	Description:
	
		Making countersinks.

	Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

	Usage:

		holes = MagicPanels.makeCountersinks(obj, face, cones)

	Result:

		Make holes and return list of holes. 

	'''

	import Part, Sketcher

	holes = []

	base = iObj
	face = iFace
	objects = iCones
	
	# set body for base object
	if base.isDerivedFrom("Part::Box"):
		
		[ part, body, sketch, pad ] = makePad(base, base.Label)
		FreeCAD.ActiveDocument.removeObject(base.Name)
		FreeCAD.ActiveDocument.recompute()
		base = pad
		
	else:
		
		body = base._Body
	
	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = FreeCAD.Vector(0, 0, 1)
		r1 = float(2 * o.Radius1)
		r2 = float(2 * o.Radius2)
		sr1 = str(r1)+" mm"
		sr2 = str(r2)+" mm"
		
		# set hole
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r1)
		holeSketch.addGeometry(geo, False)
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 0, r1)) 
		holeSketch.setDatum(1, FreeCAD.Units.Quantity(sr1))
		holeSketch.renameConstraint(1, u'Hole00Diameter')
		
		# set countersink
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r2)
		holeSketch.addGeometry(geo, True)
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 1, 3, -1, 1)) 
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 1, r2)) 
		holeSketch.setDatum(3, FreeCAD.Units.Quantity(sr2))
		holeSketch.renameConstraint(3, u'Countersink00Diameter')
		
		FreeCAD.ActiveDocument.recompute()
		
		# set position to hole Sketch
		[ x, y, z, r ] = getContainerPlacement(o, "clean")
		[[ x, y, z ]] = removeVerticesPosition([[ x, y, z ]], base, "array")
		
		setSketchPlacement(holeSketch, x, y, z, r, "global")
		FreeCAD.ActiveDocument.recompute()
		
		# create hole object
		hole = body.newObject('PartDesign::Hole','Countersink')
		hole.Profile = holeSketch
		holeSketch.Visibility = False
		
		hole.Diameter = 2 * o.Radius1
		hole.HoleCutDiameter = 2 * o.Radius2
		hole.HoleCutDepth = 5.000000
		hole.HoleCutCountersinkAngle = 90.000000
		hole.Depth = o.Height
		hole.DrillPointAngle = 118.000000
		hole.TaperedAngle = 90.000000
		hole.Threaded = 0
		hole.ThreadType = 0
		hole.HoleCutType = 2
		hole.DepthType = 0
		hole.DrillPoint = 1
		hole.DrillForDepth = 1
		hole.Tapered = 0
		
		try:
			copyColors(hole.BaseFeature, hole)
		except:
			skip = 1
		
		FreeCAD.ActiveDocument.recompute()
		
		base = hole
		holes.append(hole)
		
	return holes
	

# ###################################################################################################################
def makeCounterbores(iObj, iFace, iCones):
	'''
	Description:
	
		Making counterbores.

	Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

	Usage:

		holes = MagicPanels.makeCounterbores(obj, face, cones)

	Result:

		Make holes and return list of holes.

	'''

	import Part, Sketcher

	holes = []

	base = iObj
	face = iFace
	objects = iCones
	
	# set body for base object
	if base.isDerivedFrom("Part::Box"):
		
		[ part, body, sketch, pad ] = makePad(base, base.Label)
		FreeCAD.ActiveDocument.removeObject(base.Name)
		FreeCAD.ActiveDocument.recompute()
		base = pad
		
	else:
		
		body = base._Body

	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = FreeCAD.Vector(0, 0, 1)
		r1 = float(2 * o.Radius1)
		r2 = float(2 * o.Radius2)
		sr1 = str(r1)+" mm"
		sr2 = str(r2)+" mm"
		
		# set hole
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r1)
		holeSketch.addGeometry(geo, False)
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 0, r1)) 
		holeSketch.setDatum(1, FreeCAD.Units.Quantity(sr1))
		holeSketch.renameConstraint(1, u'Hole00Diameter')
		
		# set counterbore
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r2)
		holeSketch.addGeometry(geo, True)
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 1, 3, -1, 1)) 
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 1, r2)) 
		holeSketch.setDatum(3, FreeCAD.Units.Quantity(sr2))
		holeSketch.renameConstraint(3, u'Counterbore00Diameter')
		
		FreeCAD.ActiveDocument.recompute()
		
		# set position to hole Sketch
		[ x, y, z, r ] = getContainerPlacement(o, "clean")
		[[ x, y, z ]] = removeVerticesPosition([[ x, y, z ]], base, "array")
		
		setSketchPlacement(holeSketch, x, y, z, r, "global")
		FreeCAD.ActiveDocument.recompute()
		
		# create hole object
		hole = body.newObject('PartDesign::Hole','Counterbore')
		hole.Profile = holeSketch
		holeSketch.Visibility = False
		
		hole.Diameter = r1
		hole.HoleCutDiameter = r2
		hole.HoleCutDepth = 5.000000
		hole.HoleCutCountersinkAngle = 90.000000
		hole.Depth = o.Height
		hole.TaperedAngle = 90.000000
		hole.Threaded = 0
		hole.ThreadType = 0
		hole.HoleCutType = 1
		hole.DepthType = 0
		hole.DrillPoint = 0
		hole.Tapered = 0
		
		try:
			copyColors(hole.BaseFeature, hole)
		except:
			skip = 1
		
		FreeCAD.ActiveDocument.recompute()
		
		base = hole
		holes.append(hole)
		
	return holes


# ###################################################################################################################
def makePocketHoles(iObj, iFace, iCones):
	'''
	Description:
	
		Making pocket holes for invisible connections.

	Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

	Usage:

		holes = MagicPanels.makePocketHoles(obj, face, cones)

	Result:

		Make holes and return list of holes.

	'''

	import Part, Sketcher

	holes = []

	base = iObj
	face = iFace
	objects = iCones
	
	# set body for base object
	if base.isDerivedFrom("Part::Box"):
		
		[ part, body, sketch, pad ] = makePad(base, base.Label)
		FreeCAD.ActiveDocument.removeObject(base.Name)
		FreeCAD.ActiveDocument.recompute()
		base = pad
		
	else:
		
		body = base._Body

	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = FreeCAD.Vector(0, 0, 1)
		r1 = float(2 * o.Radius1)
		r2 = float(2 * o.Radius2)
		sr1 = str(r1)+" mm"
		sr2 = str(r2)+" mm"
		
		# set hole
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r1)
		holeSketch.addGeometry(geo, False)
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 0, r1)) 
		holeSketch.setDatum(1, FreeCAD.Units.Quantity(sr1))
		holeSketch.renameConstraint(1, u'Tip0hole00Diameter')
		
		# set counterbore
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r2)
		holeSketch.addGeometry(geo, True)
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 1, 3, -1, 1)) 
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 1, r2)) 
		holeSketch.setDatum(3, FreeCAD.Units.Quantity(sr2))
		holeSketch.renameConstraint(3, u'Pocket0hole00Diameter')
		
		FreeCAD.ActiveDocument.recompute()
		
		# set position to hole Sketch
		[ x, y, z, r ] = getContainerPlacement(o, "clean")
		[[ x, y, z ]] = removeVerticesPosition([[ x, y, z ]], base, "array")
		
		setSketchPlacement(holeSketch, x, y, z, r, "global")
		FreeCAD.ActiveDocument.recompute()
		
		# create hole object
		hole = body.newObject('PartDesign::Hole','PocketHole')
		hole.Profile = holeSketch
		holeSketch.Visibility = False
		
		hole.Diameter = r1
		hole.HoleCutDiameter = r2
		hole.HoleCutDepth = o.Height / 2
		hole.HoleCutCountersinkAngle = 90.000000
		hole.Depth = o.Height
		hole.TaperedAngle = 90.000000
		hole.Threaded = 0
		hole.ThreadType = 0
		hole.HoleCutType = 1
		hole.DepthType = 0
		hole.DrillPoint = 0
		hole.Tapered = 0
		
		try:
			copyColors(hole.BaseFeature, hole)
		except:
			skip = 1
		
		FreeCAD.ActiveDocument.recompute()
		
		base = hole
		holes.append(hole)
		
	return holes


# ###################################################################################################################
def makeCounterbores2x(iObj, iFace, iCones):
	'''
	Description:
	
		Making counterbores from both sides.

	Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

	Usage:

		holes = MagicPanels.makeCounterbores2x(obj, face, cones)

	Result:

		Make holes and return list of holes.

	'''

	import Part, Sketcher, Draft

	holes = []

	base = iObj
	face = iFace
	objects = iCones

	sizes = []
	sizes = getSizes(getReference(base))
	sizes.sort()
	thick = sizes[0]
	
	plane = getFacePlane(face)
	sink = getFaceSink(base, face)
	
	# set body for base object
	if base.isDerivedFrom("Part::Box"):
		
		[ part, body, sketch, pad ] = makePad(base, base.Label)
		FreeCAD.ActiveDocument.removeObject(base.Name)
		FreeCAD.ActiveDocument.recompute()
		base = pad
		
	else:
		
		body = base._Body

	for o in objects:
		
		# create hole Sketch
		holeSketch1 = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch1.MapMode = 'FlatFace'

		axis = FreeCAD.Vector(0, 0, 1)
		r1 = float(2 * o.Radius1)
		r2 = float(2 * o.Radius2)
		sr1 = str(r1)+" mm"
		sr2 = str(r2)+" mm"
		
		# set hole
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r1)
		holeSketch1.addGeometry(geo, False)
		holeSketch1.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
		holeSketch1.addConstraint(Sketcher.Constraint('Diameter', 0, r1)) 
		holeSketch1.setDatum(1, FreeCAD.Units.Quantity(sr1))
		holeSketch1.renameConstraint(1, u'Hole100Diameter')
		
		# set counterbore
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r2)
		holeSketch1.addGeometry(geo, True)
		holeSketch1.addConstraint(Sketcher.Constraint('Coincident', 1, 3, -1, 1)) 
		holeSketch1.addConstraint(Sketcher.Constraint('Diameter', 1, r2)) 
		holeSketch1.setDatum(3, FreeCAD.Units.Quantity(sr2))
		holeSketch1.renameConstraint(3, u'Counterbore100Diameter')
		
		FreeCAD.ActiveDocument.recompute()
		
		# #################################################################
		# First hole
		# #################################################################
		
		# get & store drill bit position and set it to sketch
		[ xs1, ys1, zs1, rs1 ] = getContainerPlacement(o, "clean")
		[ xs0, ys0, zs0, rs0 ] = [ xs1, ys1, zs1, rs1 ]
		[[ xs1, ys1, zs1 ]] = removeVerticesPosition([[ xs1, ys1, zs1 ]], base, "array")
		
		setSketchPlacement(holeSketch1, xs1, ys1, zs1, rs1, "global")
		FreeCAD.ActiveDocument.recompute()
		
		# create hole object
		hole = body.newObject('PartDesign::Hole','Counterbore')
		hole.Profile = holeSketch1
		holeSketch1.Visibility = False
		
		hole.Diameter = r1
		hole.HoleCutDiameter = r2
		hole.HoleCutDepth = o.Height
		hole.HoleCutCountersinkAngle = 90.000000
		hole.Depth = thick
		hole.TaperedAngle = 90.000000
		hole.Threaded = 0
		hole.ThreadType = 0
		hole.HoleCutType = 1
		hole.DepthType = 0
		hole.DrillPoint = 0
		hole.Tapered = 0
		
		try:
			copyColors(hole.BaseFeature, hole)
		except:
			skip = 1
		
		FreeCAD.ActiveDocument.recompute()
		
		base = hole
		holes.append(hole)
		
		# #################################################################
		# Second hole
		# #################################################################
		
		# create hole Sketch
		holeSketch2 = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch2.MapMode = 'FlatFace'

		axis = FreeCAD.Vector(0, 0, 1)
		r1 = float(2 * o.Radius1)
		r2 = float(2 * o.Radius2)
		sr1 = str(r1)+" mm"
		sr2 = str(r2)+" mm"
		
		# set hole
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r1)
		holeSketch2.addGeometry(geo, False)
		holeSketch2.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
		holeSketch2.addConstraint(Sketcher.Constraint('Diameter', 0, r1)) 
		holeSketch2.setDatum(1, FreeCAD.Units.Quantity(sr1))
		holeSketch2.renameConstraint(1, u'Hole200Diameter')
		
		# set counterbore
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r2)
		holeSketch2.addGeometry(geo, True)
		holeSketch2.addConstraint(Sketcher.Constraint('Coincident', 1, 3, -1, 1)) 
		holeSketch2.addConstraint(Sketcher.Constraint('Diameter', 1, r2)) 
		holeSketch2.setDatum(3, FreeCAD.Units.Quantity(sr2))
		holeSketch2.renameConstraint(3, u'Counterbore200Diameter')
		
		xs2, ys2, zs2, rs2 = xs1, ys1, zs1, rs1
		
		if sink == "+":

			if plane == "XY":
				zs2 = zs2 + thick
				axis = FreeCAD.Vector(1, 0, 0)
				
			if plane == "XZ":
				ys2 = ys2 + thick
				axis = FreeCAD.Vector(1, 0, 0)

			if plane == "YZ":
				xs2 = xs2 + thick
				axis = FreeCAD.Vector(0, 1, 0)

		else:

			if plane == "XY":
				zs2 = zs2 - thick
				axis = FreeCAD.Vector(1, 0, 0)
				
			if plane == "XZ":
				ys2 = ys2 - thick
				axis = FreeCAD.Vector(1, 0, 0)

			if plane == "YZ":
				xs2 = xs2 - thick
				axis = FreeCAD.Vector(0, 1, 0)
	
		center = FreeCAD.Vector(xs2, ys2, zs2)

		# move & rotate drill bit
		setContainerPlacement(o, xs2, ys2, zs2, rs2, "clean")
		Draft.rotate(o, 180, center, axis, False)
		
		# move & rotate sketch for hole
		[ xs3, ys3, zs3, rs3 ] = getContainerPlacement(o, "clean")
		setSketchPlacement(holeSketch2, xs3, ys3, zs3, rs3, "global")
		
		FreeCAD.ActiveDocument.recompute()
		
		# create hole object
		hole = body.newObject('PartDesign::Hole','Counterbore')
		hole.Profile = holeSketch2
		holeSketch2.Visibility = False
		
		hole.Diameter = r1
		hole.HoleCutDiameter = r2
		hole.HoleCutDepth = o.Height
		hole.HoleCutCountersinkAngle = 90.000000
		hole.Depth = thick
		hole.TaperedAngle = 90.000000
		hole.Threaded = 0
		hole.ThreadType = 0
		hole.HoleCutType = 1
		hole.DepthType = 0
		hole.DrillPoint = 0
		hole.Tapered = 0
		
		try:
			copyColors(hole.BaseFeature, hole)
		except:
			skip = 1
		
		FreeCAD.ActiveDocument.recompute()
		
		base = hole
		holes.append(hole)
		
		# move & rotate back drill bit
		setContainerPlacement(o, xs0, ys0, zs0, rs0, "clean")
		
		FreeCAD.ActiveDocument.recompute()
	
	FreeCADGui.Selection.clearSelection()
		
	return holes


# ###################################################################################################################
'''
# Joinery
'''
# ###################################################################################################################


# ###################################################################################################################
def makeCuts(iObjects):
	'''
	Description:
	
		Allows to create multi bool cut operation at given objects. First objects 
		from iObjects is the base element and all other will cut the base. 
		The copies will be created for cut. 
	
	Args:
	
		iObjects: objects to parse by multi bool cut

	Usage:
	
		cuts = MagicPanels.makeCuts(objects)

	Result:
	
		Array of cut objects will be returned.

	'''
	
	cuts = []
	
	base = iObjects[0]
	baseName = str(base.Name)
	baseLabel = str(base.Label)
	
	objects = iObjects[1:]
	
	for o in objects:
		
		copy = FreeCAD.ActiveDocument.copyObject(o)
		copy.Label = getNestingLabel(o, "Copy")
		
		if not hasattr(copy, "BOM"):
			info = translate("makeCuts", "Allows to skip this duplicated copy in BOM, cut-list report.")
			copy.addProperty("App::PropertyBool", "BOM", "Woodworking", info)
		
		copy.BOM = False
		
		cut = FreeCAD.ActiveDocument.addObject("Part::Cut", "Cut")
		cut.Base = base
		cut.Tool = copy
		cut.Label = getNestingLabel(base, "Cut")
		
		base = cut
		cuts.append(cut)
		
	cut.Label = getNestingLabel(base, "Cut")
	copyColors(iObjects[0], cut)
	FreeCAD.ActiveDocument.recompute()

	return cuts


# ###################################################################################################################
def makeCutsLinks(iObjects):
	'''
	Description:
	
		Allows to create multi bool cut operation at given objects. First objects 
		from iObjects is the base element and all other will cut the base. 
		At this function version App::Link is used to create copy.
	
	Args:
	
		iObjects: objects to parse by multi bool cut

	Usage:
	
		cuts = MagicPanels.makeCutsLinks(objects)

	Result:
	
		Array of cut objects will be returned.

	'''

	cuts = []

	base = iObjects[0]
	baseName = str(base.Name)
	baseLabel = str(base.Label)
	base.Visibility = False
	
	objects = iObjects[1:]

	for o in objects:

		if not o.isDerivedFrom("App::LinkGroup"):
			o = createContainer([o])

		copy = FreeCAD.ActiveDocument.addObject('App::Link', "Link")
		copy.setLink(o)
		copy.Label = getNestingLabel(o, "Copy")

		if not hasattr(copy, "BOM"):
			info = translate("makeCutsLinks", "Allows to skip this duplicated copy in BOM, cut-list report.")
			copy.addProperty("App::PropertyBool", "BOM", "Woodworking", info)

		copy.BOM = False

		cut = FreeCAD.ActiveDocument.addObject("Part::Cut", "Cut")
		cut.Base = base
		cut.Tool = copy
		cut.Label = getNestingLabel(base, "Cut")
		base.Visibility = False
		
		base = cut
		cuts.append(cut)

	cut.Label = getNestingLabel(base, "Cut")
	copyColors(iObjects[0], cut)
	FreeCAD.ActiveDocument.recompute()
	
	return cuts


# ###################################################################################################################
def makeFrame45cut(iObjects, iFaces):
	'''
	Description:
	
		Makes 45 frame cut with PartDesing Chamfer. For each face the ends will be cut.
	
	Args:
	
		iObjects: array of objects to cut
		iFaces: dict() of faces for Chamfer cut direction, the key is iObjects value (object), 
				if there are more faces for object, the first one will be get as direction.

	Usage:
	
		frames = MagicPanels.makeFrame45cut(objects, faces)
		
	Result:
	
		Created Frames with correct placement, rotation and return array with Chamfer frame objects.

	'''

	frames = []

	for o in iObjects:
	
		FreeCAD.ActiveDocument.openTransaction("makeFrame45cut "+str(o.Label))
	
		face = iFaces[o][0]

		sizes = getSizes(o)
		sizes.sort()
		
		[ faceType, arrAll, arrThick, arrShort, arrLong ] = getFaceEdges(o, face)
		
		if faceType == "edge":
			arr = arrThick
			size = sizes[1]
			
		if faceType == "surface":
			arr = arrShort
			size = sizes[0]

		keys = []
		
		for e in arr:
			keys.append(e.BoundBox)
		
		if o.isDerivedFrom("Part::Box"):
		
			[ part, body, sketch, pad ] = makePad(o, "Frame")
			FreeCAD.ActiveDocument.removeObject(o.Name)
			FreeCAD.ActiveDocument.recompute()
		
		else:
		
			body = o._Body
			pad = o

		edges = []
		for k in keys:
			index = getEdgeIndexByKey(pad, k)
			edges.append("Edge"+str(int(index)))
		
		frame = body.newObject('PartDesign::Chamfer','Frame45Cut')
		frame.Base = (pad, edges)
		frame.Size = size - 0.01
		pad.Visibility = False
		
		FreeCAD.ActiveDocument.recompute()

		try:
			copyColors(pad, frame)
		except:
			skip = 1
		
		frames.append(frame)
	
		FreeCAD.ActiveDocument.commitTransaction()
	
	return frames


# ###################################################################################################################
def makeChamferCut(iObjects, iEdges, iSizes, iLabels):
	'''
	Description:
	
		Makes PartDesing Chamfer cut for edges array. But you can set different size for each edge. 
		Yes, you give edge objects, and you make chamfer for each edge, one by one, with different 
		size, but the most funny part is that the selected edge not exists because the Cube 
		object not exists ;-)

	Args:
	
		iObjects: array of objects to cut
		iEdges: dict() of arrays [ edgeObj1, edgeObj2 ], edgeArr = iEdges[iObjects[0]]
		iSizes: dict() of arrays [ 100, 50 ], sizeArr = iSizes[iObjects[0]]
		iLabels: dict() of labels for new object, label = iLabels[iObjects[0]]

	Usage:
	
		cuts = MagicPanels.makeChamferCut(objects, edges, sizes, labels)
		
	Result:
	
		return array with chamfer objects

	'''

	cuts = []

	for o in iObjects:
	
		edges = iEdges[o]
		sizes = iSizes[o]
		label = iLabels[o]

		# do not watch this, because it is Topology Naming Problem ;-)
		keys = []
		for e in edges:
			keys.append(e.BoundBox)
		
		if o.isDerivedFrom("Part::Box"):
		
			[ part, body, sketch, pad ] = makePad(o, str(o.Label))
			FreeCAD.ActiveDocument.removeObject(o.Name)
			FreeCAD.ActiveDocument.recompute()

		else:
		
			body = o._Body
			pad = o

		# so let's roll, you have also Topology Naming Problem in the fridge? ;-)
		cut = pad
		i = 0
		for k in keys:
			
			index = getEdgeIndexByKey(cut, k)
			edgeName = "Edge"+str(index)

			newCut = body.newObject('PartDesign::Chamfer', "chamferCut")
			newCut.Label = label
			newCut.Base = (cut, edgeName)
			newCut.Size = sizes[i] - (1 / (10 * gRoundPrecision))
			cuts.append(newCut)
			
			cut.Visibility = False
			FreeCAD.ActiveDocument.recompute()

			try:
				copyColors(cut, newCut)
			except:
				skip = 1
		
			FreeCAD.ActiveDocument.recompute()
			
			cut = newCut
			i = i + 1

	return cuts


# ###################################################################################################################
def makeMortise(iSketch, iDepth, iPad, iFace):
	'''
	Description:
	
		Make Mortise pocket for given iSketch pattern.

	Args:

		iSketch: Sketch object as pattern for Mortise
		iDepth: depth of the pocket
		iPad: pad object to get Body
		iFace: face object at the pad where is the iSketch

	Usage:

		[ obj, face ] = MagicPanels.makeMortise(sketch, 20, obj, face)

	Result:

		Make Mortise and return new object and face reference for GUI info screen update and further processing

	'''

	faceKey = iFace.BoundBox
	
	# set body for object
	if iPad.isDerivedFrom("Part::Box"):
		
		[ part, body, sketchPad, pad ] = makePad(iPad, iPad.Label)
		FreeCAD.ActiveDocument.removeObject(iPad.Name)
		FreeCAD.ActiveDocument.recompute()
	
	else:
		
		body = iPad._Body
		pad = iPad

	sketch = FreeCAD.ActiveDocument.copyObject(iSketch)
	try:
		sketch.Support = ""
	except:
		sketch.AttachmentSupport = ""
	
	sketch.adjustRelativeLinks(body)
	body.ViewObject.dropObject(sketch, None, '', [])
	
	[ x, y, z ] = getPosition(iSketch, "global")
	setPosition(sketch, x, y, z, "global")
	
	mortise = body.newObject('PartDesign::Pocket','Mortise')
	mortise.Profile = sketch
	
	mortise.Length = 2 * iDepth
	mortise.Midplane = 1
	mortise.Label = "Mortise "
	
	# not needed
	#plane = getFacePlane(iFace)
	
	#if plane == "XY":
	#	direction = (0, 0, 1)
	#if plane == "XZ":
	#	direction = (0, 1, 0)
	#if plane == "YZ":
	#	direction = (1, 0, 0)

	#mortise.TaperAngle = 0.000000
	#mortise.UseCustomVector = 0
	#mortise.Direction = direction
	#mortise.AlongSketchNormal = 1
	#mortise.Type = 0
	#mortise.UpToFace = None
	#mortise.Reversed = 0
	#mortise.Offset = 0

	sketch.Visibility = False
	pad.Visibility = False
	FreeCAD.ActiveDocument.recompute()
	
	try:
		copyColors(pad, mortise)
	except:
		skip = 1
	
	FreeCAD.ActiveDocument.recompute()
	
	index = getFaceIndexByKey(mortise, faceKey)
	newFace = mortise.Shape.Faces[index-1]

	return [ mortise, newFace ]


# ###################################################################################################################
def makeTenon(iSketch, iLength, iPad, iFace):
	'''
	Description:
	
		Make Tenon pad for given iSketch pattern.

	Args:

		iSketch: Sketch object as pattern for Mortise
		iLength: Length for the Tenon pad
		iPad: pad object to get Body
		iFace: face object at the pad where is the iSketch

	Usage:

		[ obj, face ] = MagicPanels.makeTenon(sketch, 20, obj, face)

	Result:

		Make Tenon and return new object and face reference for GUI info screen update and further processing

	'''

	faceKey = iFace.BoundBox

	# set body for object
	if iPad.isDerivedFrom("Part::Box"):
		
		[ part, body, sketchPad, pad ] = makePad(iPad, iPad.Label)
		FreeCAD.ActiveDocument.removeObject(iPad.Name)
		FreeCAD.ActiveDocument.recompute()
	
	else:
		
		body = iPad._Body
		pad = iPad

	sketch = FreeCAD.ActiveDocument.copyObject(iSketch)
	try:
		sketch.Support = ""
	except:
		sketch.AttachmentSupport = ""
	
	sketch.adjustRelativeLinks(body)
	body.ViewObject.dropObject(sketch, None, '', [])
	
	[ x, y, z ] = getPosition(iSketch, "global")
	setPosition(sketch, x, y, z, "global")

	tenon = body.newObject('PartDesign::Pad', "Tenon")
	tenon.Label = "Tenon "
	tenon.Profile = sketch
	tenon.Length = FreeCAD.Units.Quantity(2 * iLength)
	tenon.Midplane = 1
	
	sketch.Visibility = False
	pad.Visibility = False
	FreeCAD.ActiveDocument.recompute()
	
	try:
		copyColors(pad, tenon)
	except:
		skip = 1
	
	FreeCAD.ActiveDocument.recompute()
	
	index = getFaceIndexByKey(tenon, faceKey)
	newFace = tenon.Shape.Faces[index-1]

	return [ tenon, newFace ]


# ###################################################################################################################
'''
# Router
'''
# ###################################################################################################################


# ###################################################################################################################
def getSubByKey(iObj, iKey, iType, iSubType):
	'''
	Description:
	
		This is extended version of getEdgeIndexByKey function. 
		This function has been created to solve resized edge problem. If you cut the edge the next 
		edge will change the Length. So, also the BoundBox will be changed. With this function you 
		can customize reference key to solve the Topology Naming Problem.
	
	Args:
	
		iObj: object for the sub-object
		iKey: array with keys
		iType: type of comparison
		iSubType: type of sub-object to return, "edge" or "face"

	Usage:
	
		key = [ e.CenterOfMass, plane ]
		[ edge, edgeName, edgeIndex ] = MagicPanels.getSubByKey(o, key, "CenterOfMass", "edge")

	Result:
	
		return edge object, name like Edge1 and also index starting from 0 (for iObj.Shape.Edges[index])

	'''
	
	if iType == "CenterOfMass":
		
		key = iKey[0]
		plane = iKey[1]
		
		edge = ""
		index = 1
		name = "Edge"
		
		if iSubType == "edge":
			
			for e in iObj.Shape.Edges:
				
				p = getEdgePlane(iObj, e)
				
				if p == plane:
					if plane == "X":
						if equal(e.CenterOfMass.y, key.y) and equal(e.CenterOfMass.z, key.z):
							name += str(index)
							return [ e, name, index ]

					if plane == "Y":
						if equal(e.CenterOfMass.x, key.x) and equal(e.CenterOfMass.z, key.z):
							name += str(index)
							return [ e, name, index ]
							
					if plane == "Z":
						if equal(e.CenterOfMass.x, key.x) and equal(e.CenterOfMass.y, key.y):
							name += str(index)
							return [ e, name, index ]
				
				index = index + 1

		# not needed now
		if iSubType == "face":
			
			search = iObj.Shape.Faces
			return [ "not supported", "not supported", "not supported" ]
		
	if iType == "BoundBox":
		
		key = iKey[0]
		index = 1
		
		if iSubType == "edge":
			
			for e in iObj.Shape.Edges:
			
				if normalizeBoundBox(e.BoundBox) == normalizeBoundBox(key):
					edgeName = "Edge"+str(index)
					idx = index - 1
					return [ e, edgeName, idx ]

				index = index + 1

		if iSubType == "face":
			
			for f in iObj.Shape.Faces:
			
				if normalizeBoundBox(f.BoundBox) == normalizeBoundBox(key):
					faceName = "Face"+str(index)
					idx = index - 1
					return [ f, faceName, idx ]

				index = index + 1

	return [ "", "", "" ]


# ###################################################################################################################
def getSketchPatternRotation(iObj, iSub):
	'''
	Description:
	
		Returns Rotation object which can be passed directly to setSketchPlacement 
		functions. The Sketch will be perpendicular to the iSub object, so it can be used as 
		router bit to cut the edge or face.
	
	Args:
	
		iObj: object for sub-object
		iSub: selected sub-object, edge or face

	Usage:
	
		r = MagicPanels.getSketchPatternRotation(o, edge)
		r = MagicPanels.getSketchPatternRotation(o, face)

	Result:
	
		return FreeCAD.Rotation object.

	'''

	r = ""
	
	if iSub.ShapeType == "Edge":
	
		plane = getEdgePlane(iObj, iSub)

		if plane == "X":
			r = FreeCAD.Rotation(FreeCAD.Vector(0.00, 1.00, 0.00), 90.00)

		if plane == "Y":
			r = FreeCAD.Rotation(FreeCAD.Vector(1.00, 0.00, 0.00), 90.00)

		if plane == "Z":
			r = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 00.00)
	
	if iSub.ShapeType == "Face":
		
		plane = getFacePlane(iSub)
		[ faceType, arrAll, arrThick, arrShort, arrLong ] = getFaceEdges(iObj, iSub)
		
		if len(arrLong) > 0:
			subPlane = getEdgePlane(iObj, arrLong[0])
		elif len(arrShort) > 0:
			subPlane = getEdgePlane(iObj, arrShort[0])
		elif len(arrAll) > 0:
			subPlane = getEdgePlane(iObj, arrAll[0])
		
		if subPlane == "X":
			r = FreeCAD.Rotation(FreeCAD.Vector(0.00, 1.00, 0.00), 90.00)

		if subPlane == "Y":
			r = FreeCAD.Rotation(FreeCAD.Vector(1.00, 0.00, 0.00), 90.00)

		if subPlane == "Z":
			r = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 00.00)
	
	# This can be updated later for rotated edges with additional rotation angle (offset from axis)
	return r


# ###################################################################################################################
def edgeRouter(iPad, iSub, iSketch, iLength, iLabel, iType):
	'''
	Description:
	
		This function is router for the edge. It cut the 
		iSub with iSketch pattern. The new object will get iLabel label.
	
	Args:
	
		iPad: Pad object of the sub-object, for routing
		iSub: sub-object, edge or face
		iSketch: sketch object will be used as pattern to cut, the sketch should be around XYZ center cross.
		iLength: length to cut, float or int value, 0 means ThroughAll
		iLabel: label for new object
		iType: type of routing

	Usage:
	
		router = MagicPanels.edgeRouter(pad, edge, sketch, 0, "routerCove", "simple")

	Result:
	
		return router object, the result of cut

	'''

	if iType == "simple":
		
		anchor = iSub.CenterOfMass
		r = getSketchPatternRotation(iPad, iSub)
		setSketchPlacement(iSketch, anchor.x, anchor.y, anchor.z, r, "global")
		
		router = iPad._Body.newObject('PartDesign::Pocket','router')
		router.Profile = iSketch
		router.Midplane = 1
		router.Label = iLabel + " "
		
		if iLength == 0:
			router.Type = 1
		else:
			router.Length = iLength

		iSketch.Visibility = False
		iPad.Visibility = False
		FreeCAD.ActiveDocument.recompute()
		
		try:
			copyColors(iPad, router)
		except:
			skip = 1
		
		FreeCAD.ActiveDocument.recompute()
	
		return router

	return ""


# ###################################################################################################################
def makePockets(iObjects, iLength):
	'''
	Description:
	
		This function is multi Pocket. First object from iObjects will be base
		object to Pocket, all others should be Sketches. The Length is depth for Pocket. 
		If the Length is 0 the Pocket will be ThroughAll.
	
	Args:
	
		iObjects: First base objects, next sketches
		iLength: length to cut, float or int value, 0 means ThroughAll
		
	Usage:
	
		pocket = MagicPanels.makePockets(selectedObjects, 0)

	Result:
	
		return last pocket object, the result of cut

	'''

	base = iObjects[0]
	sketches = iObjects[1:]

	if base.isDerivedFrom("Part::Box"):

		[ part, body, sketch, pad ] = makePad(base, "panel2pad")
		FreeCAD.ActiveDocument.removeObject(base.Name)
		FreeCAD.ActiveDocument.recompute()
		base = pad

	for s in sketches:
		
		body = base._Body

		# FreeCAD know what is going on here and not blow up, I am surprised ;-)
		try:
			[ x, y, z, r ] = getSketchPlacement(s, "global")
			[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(base)
			x = x - coX
			y = y - coY
			z = z - coZ
			s.adjustRelativeLinks(body)
			body.ViewObject.dropObject(s, None, '', [])
			setSketchPlacement(s, x, y, z, r, "global")
		except:
			skip = 1

		pocket = body.newObject('PartDesign::Pocket','multiPocket')
		pocket.Profile = s
		pocket.Midplane = 1
		pocket.Label = "multiPocket "
		pocket.Midplane = 1

		if iLength == 0:
			pocket.Type = 1
		else:
			pocket.Length = 2 * iLength

		s.Visibility = False
		base.Visibility = False
		FreeCAD.ActiveDocument.recompute()
		
		try:
			copyColors(base, pocket)
		except:
			skip = 1
			
		FreeCAD.ActiveDocument.recompute()
		
		base = pocket


# ###################################################################################################################
'''
# Spreadsheet
'''
# ###################################################################################################################

def sheetGetKey(iC, iR):
	'''
	Description:
	
		Allows to get key as letters for spreadsheet from given column and row index.

	Args:
	
		iC: column index
		iR: row index

	Usage:
	
		key = MagicPanels.sheetGetKey(1, 2)

	Result:
	
		return key string

	'''

	letters = "ZABCDEFGHIJKLMNOPQRSTUVWXYZ" # max 26

	mod = int((iC % 26))
	div = int((iC - 1) / 26) 

	keyC = ""

	if iC < 27:
		keyC = letters[iC]
	else:
		keyC = letters[div] + letters[mod]

	keyR = str(iR)

	key = keyC + keyR

	# for given column and row it returns
	# spreadsheet key for cell like e.g. A5, AG125 etc
	return str(key)


# ###################################################################################################################
'''
# TechDraw
'''
# ###################################################################################################################

def createTechDrawPage(iName="page", iSize="A4", iType="v"):
	'''
	Description:
	
		Create TechDraw page with exact template.

	Args:
	
		iName (optional): string, object name for created page
		iSize (optional): string, size of the page e.g. "A4"
		iType (optional): string, orientation of the page:
			* "v": vertical means Portrait
			* "h": horizontal means Landscape

	Usage:
	
		page = MagicPanels.createTechDrawPage()
		page = MagicPanels.createTechDrawPage("toPrint", "A4", "v")

	Result:
	
		return TechDraw page object

	'''


	import os
	
	page = FreeCAD.ActiveDocument.addObject("TechDraw::DrawPage", iName)
	template = FreeCAD.ActiveDocument.addObject("TechDraw::DrawSVGTemplate","Template")

	templates = []
	if iSize == "A4" and iType == "v":
		
		# support for backward and forward compatibility 
		templates = [ 
			FreeCAD.getResourceDir() + "Mod/TechDraw/Templates/A4_Portrait_blank.svg",
			FreeCAD.getResourceDir() + "Mod/TechDraw/Templates/ISO/A4_Portrait_blank.svg"
		]
	
	if iSize == "A4" and iType == "h":
		
		# support for backward and forward compatibility
		templates = [ 
			FreeCAD.getResourceDir() + "Mod/TechDraw/Templates/A4_Landscape_blank.svg",
			FreeCAD.getResourceDir() + "Mod/TechDraw/Templates/ISO/A4_Landscape_blank.svg"
		]
		
	for t in templates:
		if os.path.exists(t):
			template.Template = t

	page.Template = template
	
	return page
	

# ###################################################################################################################
'''
# Themes
'''
# ###################################################################################################################


def getTheme(iType=""):
	'''
	Description:
	
		Allows to set GUI color theme. 

	Args:
	
		iType: color theme reference name
		
	Usage:

		# to return Qt CSS string
		QtCSS = MagicPanels.getTheme("classic")
		QtCSS = MagicPanels.getTheme("lavender")
		self.setStyleSheet(QtCSS)
		
		# to return list of available themes
		self.sModeList = MagicPanels.getTheme("config")
		self.sMode = QtGui.QComboBox(self)
		self.sMode.addItems(self.sModeList)

	Result:
	
		return Qt CSS string to set via self.setStyleSheet(QtCSS)

	'''
	
	
	# ##############################################################
	# setting themes
	# ##############################################################
	
	themes = (
		"default",
		"classic", 
		"pink",
		"lavender",
		"sky",
		"sun",
		"gray",
		"grass",
		"winter",
		"classic 3D", 
		"pink 3D",
		"lavender 3D",
		"sky 3D",
		"sun 3D",
		"gray 3D",
		"grass 3D",
		"winter 3D",
		"classic 3D v2", 
		"pink 3D v2",
		"lavender 3D v2",
		"sky 3D v2",
		"sun 3D v2",
		"gray 3D v2",
		"grass 3D v2",
		"winter 3D v2" # no comma
	)
	
	if iType == "config":
		return themes
	
	# ##############################################################
	# setting color for themes
	# ##############################################################
	
	if iType == "default" or iType == "":
		return ""
	
	if iType == "classic":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#E4E4E4"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#A1A1A1"   # border around elements

	if iType == "pink":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#FF00EE"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#BB00AA"   # border around elements
	
	if iType == "lavender":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#B57EDC"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#A46DCB"   # border around elements

	if iType == "sky":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#AAAAFF"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#5555AA"   # border around elements
	
	if iType == "sun":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#FFAA00"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#AA5500"   # border around elements

	if iType == "gray":
		color1 = "#D1D1D1"   # background gradient start
		color2 = "#A1A1A1"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#515151"   # border around elements

	if iType == "grass":
		color1 = "#D1D1D1"   # background gradient start
		color2 = "#AAFFAA"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#55AA55"   # border around elements
	
	if iType == "winter":
		color1 = "#D1D1D1"   # background gradient start
		color2 = "#E1E1E1"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#A1A1A1"   # border around elements

	if iType == "classic 3D":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#E4E4E4"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#A1A1A1"   # border around elements

	if iType == "pink 3D":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#FF00EE"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#BB00AA"   # border around elements
	
	if iType == "lavender 3D":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#B57EDC"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#A46DCB"   # border around elements

	if iType == "sky 3D":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#AAAAFF"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#5555AA"   # border around elements
	
	if iType == "sun 3D":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#FFAA00"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#AA5500"   # border around elements

	if iType == "gray 3D":
		color1 = "#D1D1D1"   # background gradient start
		color2 = "#A1A1A1"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#515151"   # border around elements

	if iType == "grass 3D":
		color1 = "#D1D1D1"   # background gradient start
		color2 = "#AAFFAA"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#55AA55"   # border around elements
	
	if iType == "winter 3D":
		color1 = "#D1D1D1"   # background gradient start
		color2 = "#E1E1E1"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#A1A1A1"   # border around elements

	if iType == "classic 3D v2":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#E4E4E4"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#A1A1A1"   # border around elements

	if iType == "pink 3D v2":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#FF00EE"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#BB00AA"   # border around elements
	
	if iType == "lavender 3D v2":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#B57EDC"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#A46DCB"   # border around elements

	if iType == "sky 3D v2":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#AAAAFF"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#5555AA"   # border around elements
	
	if iType == "sun 3D v2":
		color1 = "#FFFFFF"   # background gradient start
		color2 = "#FFAA00"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#AA5500"   # border around elements

	if iType == "gray 3D v2":
		color1 = "#D1D1D1"   # background gradient start
		color2 = "#A1A1A1"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#515151"   # border around elements

	if iType == "grass 3D v2":
		color1 = "#D1D1D1"   # background gradient start
		color2 = "#AAFFAA"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#55AA55"   # border around elements
	
	if iType == "winter 3D v2":
		color1 = "#D1D1D1"   # background gradient start
		color2 = "#E1E1E1"   # background gradient stop
		color3 = "#000000"   # text color
		color4 = "#A1A1A1"   # border around elements

	# ##############################################################
	# QtCSS - 2D
	# ##############################################################

	QtCSS =  '''
	
		QDialog {
			color: '''+color3+''';
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 1, y2: 1,
				stop: 0 '''+color1+''', stop: 1 '''+color2+'''
			);
		}
		
		QPushButton, QPushButton:enabled {
			color: '''+color3+''';
			border: 2px solid '''+color4+''';
			background-color: '''+color2+''';
		}
		QPushButton:pressed {
			background-color: #FF0000;
		}
		QPushButton:disabled {
			background-color: '''+color1+''';
		}
		
		QLineEdit, QTextEdit {
			color: '''+color3+''';
			border: 2px solid '''+color4+''';
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 1, y2: 1,
				stop: 0 '''+color1+''', stop: 1 '''+color2+'''
			);
		}
	
		QScrollBar {
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 2, y2: 2,
				stop: 0 '''+color2+''', stop: 1 '''+color1+'''
			);
		}
		
		QGroupBox, QLabel#qt_msgbox_label {
			color: '''+color3+''';
			border: 2px solid '''+color4+''';
			margin-top: 2.5ex;
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 1, y2: 1,
				stop: 0 '''+color1+''', stop: 1 '''+color2+'''
			);
		}
		QGroupBox:title {
			color: '''+color3+''';
			background-color: transparent;
		}
		
		QLabel {
			color: '''+color3+''';
			background-color: transparent;
		}
		
		QLabel#qt_msgbox_label {
			min-width: 700px;
			padding: 15px;
			margin: 15px 25px 15px 0px;
		}
		QDialogButtonBox#qt_msgbox_buttonbox > QPushButton {
			width: 100%;
		}

	'''

	# ##############################################################
	# QtCSS - 3D
	# ##############################################################

	QtCSS3D =  '''
			
		QDialog {
			color: '''+color3+''';
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 1, y2: 1,
				stop: 0 '''+color1+''', stop: 1 '''+color2+'''
			);
		}
		
		QPushButton, QPushButton:enabled {
			color: '''+color3+''';
			border: 1px outset '''+color4+''';
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 0, y2: 1,
				stop: 0 '''+color1+''', stop: 1 '''+color2+'''
			);
		}
		QPushButton:pressed {
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 0, y2: 1,
				stop: 0 '''+color1+''', stop: 1 #FF0000
			);
		}
		QPushButton:disabled {
			color: '''+color1+''';
			background-color: '''+color2+''';
		}
		
		QLineEdit, QTextEdit {
			color: '''+color3+''';
			border: 1px inset '''+color4+''';
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 1, y2: 1,
				stop: 0 '''+color1+''', stop: 1 '''+color2+'''
			);
		}
		
		QScrollBar {
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 2, y2: 2,
				stop: 0 '''+color2+''', stop: 1 '''+color1+'''
			);
		}
		
		QGroupBox, QLabel#qt_msgbox_label {
			color: '''+color3+''';
			background-color: '''+color2+''';
			border-left: 3px solid '''+color4+''';
			border-top: 3px solid '''+color4+''';
			border-right: 3px solid '''+color1+''';
			border-bottom: 3px solid '''+color1+''';
			margin-top: 2.5ex;
		}
		QGroupBox:title {
			color: '''+color3+''';
			background-color: transparent;
		}
		
		QLabel {
			color: '''+color3+''';
			background-color: transparent;
		}
		
		QLabel#qt_msgbox_label {
			min-width: 700px;
			padding: 15px;
			margin: 15px 25px 15px 0px;
		}
		QDialogButtonBox#qt_msgbox_buttonbox > QPushButton {
			width: 100%;
		}
		
	'''
	# ##############################################################
	# QtCSS - 3D v2
	# ##############################################################

	QtCSS3Dv2 =  '''
			
		QDialog {
			color: '''+color3+''';
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 1, y2: 1,
				stop: 0 '''+color1+''', stop: 1 '''+color2+'''
			);
		}
		
		QPushButton, QPushButton:enabled {
			color: '''+color3+''';
			border: 1px outset '''+color4+''';
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 0, y2: 1,
				stop: 0 '''+color1+''', stop: 1 '''+color2+'''
			);
		}
		QPushButton:pressed {
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 0, y2: 1,
				stop: 0 '''+color1+''', stop: 1 #FF0000
			);
		}
		QPushButton:disabled {
			color: '''+color1+''';
			background-color: '''+color2+''';
		}
		
		QLineEdit, QTextEdit {
			color: '''+color3+''';
			border: 1px inset '''+color4+''';
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 1, y2: 1,
				stop: 0 '''+color2+''', stop: 1 '''+color1+'''
			);
		}
		
		QScrollBar {
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 2, y2: 2,
				stop: 0 '''+color2+''', stop: 1 '''+color1+'''
			);
		}
		
		QGroupBox, QLabel#qt_msgbox_label {
			color: '''+color3+''';
			background-color: qlineargradient( 
				x1: 0, y1: 0, 
				x2: 1, y2: 1,
				stop: 0 '''+color2+''', stop: 1 '''+color1+'''
			);
			border-left: 3px solid '''+color1+''';
			border-top: 3px solid '''+color1+''';
			border-right: 3px solid '''+color4+''';
			border-bottom: 3px solid '''+color4+''';
			margin-top: 2.5ex;
		}
		QGroupBox:title {
			color: '''+color3+''';
			background-color: transparent;
		}
		
		QLabel {
			color: '''+color3+''';
			background-color: transparent;
		}
		
		QLabel#qt_msgbox_label {
			min-width: 700px;
			padding: 15px;
			margin: 15px 25px 15px 0px;
		}
		QDialogButtonBox#qt_msgbox_buttonbox > QPushButton {
			width: 100%;
		}
		
	'''

	# ##############################################################
	# set
	# ##############################################################

	if iType[-3:] == " 3D":
		return QtCSS3D
	elif iType[-6:] == " 3D v2":
		return QtCSS3Dv2
	else:
		return QtCSS


# ###################################################################################################################
'''
# Info screen
'''
# ###################################################################################################################


def showInfo(iCaller, iInfo, iNote="yes"):
	'''
	Description:
	
		Allows to show Gui info box for all available function and multiple calls.

	Args:
	
		iCaller: window title
		iInfo: HTML text to show
		iNote: additional tutorial ("yes" or "no"), by default is "yes".

	Usage:

		info = "text to show"
		iType = "XY"
		
		MagicPanels.showInfo("window title", info)
		MagicPanels.showInfo("window title", info, "no")

	Result:
	
		Show info Gui.

	'''

	info = ""
	
	import os, sys
	import fakemodule
	path = os.path.dirname(fakemodule.__file__)
	iconPath = str(os.path.join(path, "Icons"))
	
	fpng = os.path.join(iconPath, iCaller+".png")
	fsvg = os.path.join(iconPath, iCaller+".svg")
	fxpm = os.path.join(iconPath, iCaller+".xpm")
	
	if os.path.exists(fpng):
		info += '<img src="'+ fpng + '" width="200" height="200" align="right">'

	elif os.path.exists(fsvg):
		info += '<svg>'
		info += '<img src="'+ fsvg + '" width="200" height="200" align="right"/>'
		info += '</svg>'
	
	elif os.path.exists(fxpm):
		info += '<img src="'+ fxpm + '" width="200" height="200" align="right"/>'
	
	else:
		skip = 1
	
	info += iInfo
	
	info += "<br><br>"
	info += "<b>" + translate('showInfoAll','Golden rules:') + "</b>"
	info += "<ul>"
	
	info += "<li>"
	info += translate('showInfoAll','Not rotate objects directly, rotate them via LinkGroup container.')
	info += "</li>"
	info += "<li>"
	info += translate('showInfoAll','Not copy Pad directly. Copy, Clone or Link the Part container.')
	info += "</li>"
	info += "<li>"
	info += translate('showInfoAll','Not mix Cut with PartDesign too much. Keep clear and simple design line based on simple panels.')
	info += "</li>"
	info += "<li>"
	info += translate('showInfoAll','If you want generate cut-list, BOM, dimensions, rather avoid packing objects extremely, for example Array on Array or MultiTransform on MultiTransform.')
	info += "</li>"
	info += "<li>"
	info += translate('showInfoAll','Not move objects via AttachmentOffset, move them via Body or LinkGroup container.')
	info += "</li>"
	info += "<li>"
	info += translate('showInfoAll','Design furniture from simple panels (Part::Box objects). If you want more detailed model convert desired simple panel into Pad and edit the Sketch. Also for irregular or not rectangle shapes.')
	info + "</li>"
	info += "<li>"
	info += translate('showInfoAll','Always make backup of your project. Read documentation, watch videos, learn more or open issue.')
	info += "</li>"
	info += "<li>"
	info += translate('showInfoAll','Break all rules, if you know what you are doing.')
	info += "</li>"
	info += "<ul>"
	
	if iNote == "yes":
		
		info += '<br><br>'
		info += translate('showInfoAll', 'For more details see:') + ' '
		info += '<a href="https://github.com/dprojects/Woodworking/tree/master/Docs">'
		info += translate('showInfoAll', 'Woodworking workbench documentation')
		info += '</a>'
	
	msg = QtGui.QMessageBox()
	msg.setWindowTitle(iCaller)
	msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
	msg.setText(info)
	
	# set theme
	QtCSS = getTheme(gTheme)
	
	if QtCSS == "":
		
		colorR = msg.palette().window().color().red()
		colorG = msg.palette().window().color().green()
		colorB = msg.palette().window().color().blue()
	
		offset1 = 50
		offset2 = 5
		borderColor1 = "rgb(" + str(colorR-offset1) + ", " + str(colorG-offset1) + ", " + str(colorB-offset1) + ")"
		borderColor2 = "rgb(" + str(colorR-offset2) + ", " + str(colorG-offset2) + ", " + str(colorB-offset2) + ")"
	
		css = '''
	
			QLabel { 
				min-width: 700px; 
				padding: 15px;
				margin: 15px 25px 15px 0px;
				border-left: 15px solid ''' + borderColor1 + ''';
				border-top: 15px solid ''' + borderColor1 + ''';
				border-right: 15px solid ''' + borderColor2 + ''';
				border-bottom: 15px solid ''' + borderColor2 + ''';
			}
		
		'''
		QtCSS = css

	msg.setStyleSheet(QtCSS)
	msg.exec_()


# ###################################################################################################################
'''
# DEPRECATED
'''
# ###################################################################################################################


# ###################################################################################################################
def moveToParent(iObjects, iSelection):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		This version move object to parent container without adding or remove offset. This is useful if you copy the 
		Sketch, because Sketch after copy is located outside Body, in Part. But if the Part is inside LinkGroup 
		the copied Sketch will be located outside LinkGroup, in main root folder. This is problematic because 
		the Sketch after copy has offset from containers. The object to move need to be in root folder to avoid 
		duplicated already copied objects, Cube.
	
	Args:
	
		iObjects: list of objects to move to container, for example new created Sketch
		iSelection: selected object, for example Sketch

	Usage:
	
		MagicPanels.moveToParent([ copy ], sketch)

	Result:
	
		No return, move object.

	'''

	# in try to avoid dependency loop
	try:
		
		# skip move to Body container
		if iSelection.isDerivedFrom("PartDesign::Body"):
			return

		# if Cube and Part are in the root, and Part was created before Cube
		# the InList will return Part as parent, do you believe it?
		if len(iSelection.InList) < 1 or len(iSelection.Parents) < 1:
			return

		parent = iSelection.InList[0]

		for o in iObjects:

			# skip move Link of LinkGroup to the same LinkGroup
			if iSelection.isDerivedFrom("App::LinkGroup") or iSelection.isDerivedFrom("App::Link"):
				if o.isDerivedFrom("App::Link"):
					continue

			# move object
			FreeCADGui.Selection.addSelection(o)
			o.adjustRelativeLinks(parent)
			parent.ViewObject.dropObject(o, None, '', [])
			FreeCADGui.Selection.clearSelection()

		FreeCAD.ActiveDocument.recompute()

	except:
		skip = 1


# ###################################################################################################################
def moveToClean(iObjects, iSelection):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		Move objects iObjects to clean container for iSelection object.
		Container need to be in the clean path, no other objects except Group or LinkGroup, 

		For example:

		clean path: LinkGroup -> LinkGroup
		not clean: Mirror -> LinkGroup
	
	Args:
	
		iObjects: list of objects to move to container, for example new created Cube
		iSelection: selected object, for example Pad

	Usage:
	
		MagicPanels.moveToClean([ o ], pad)

	Result:
	
		No return, move object.

	'''

	containers = getContainers(iSelection)
	rsize = len(containers)
	
	# if no container, do nothing
	if rsize == 0:
		return
	
	# if containers
	else:
		
		coX, coY, coZ, coR = 0, 0, 0, 0
		search = True
		toMove = ""
		
		# search for first non container item
		i = 0
		while i < rsize and i < gSearchDepth:
			
			index = rsize - 1 - i
			c = containers[index]
			
			# if there is supported container
			if (
				c.isDerivedFrom("App::LinkGroup") or 
				c.isDerivedFrom("App::DocumentObjectGroup") 
				):
			
				# save last valid container
				toMove = c
			
				# skip group without placement
				try:
					coX = coX + c.Placement.Base.x
					coY = coY + c.Placement.Base.y
					coZ = coZ + c.Placement.Base.z
				except:
					skip = 1
			else:
				break

			i = i + 1

		# after search, check if found
		if toMove == "":
			return

		# move objects
		for o in iObjects:
		
			# add containers offset
			[x, y, z, r ] = getContainerPlacement(o, "clean")
			
			x = x + coX
			y = y + coY
			z = z + coZ
			
			setContainerPlacement(o, x, y, z, 0, "clean")
			
			# move object to saved container
			o.adjustRelativeLinks(toMove)
			toMove.ViewObject.dropObject(o, None, '', [])
			
		FreeCAD.ActiveDocument.recompute()


# ###################################################################################################################
def moveToFirstWithInverse(iObjects, iSelection):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		This version remove the placement and rotation offset from iObjects and move the iObjects to first 
		supported container (LinkGroup). 
		
		Note: It is dedicated to move panel created from vertices to the first LinkGroup container. 
		The object created from vertices have applied offset with rotation after creation 
		but is outside the container. So if you move it manually it will be in the wrong place because 
		container apply the placement and rotation again. So, you have to remove the offset and move it. 
		Yea, that's the beauty of FreeCAD ;-)
	
	Args:
	
		iObjects: list of objects to move to container, for example new created Cube
		iSelection: selected object, for example Pad

	Usage:
	
		MagicPanels.moveToFirstWithInverse([ o ], pad)

	Result:
	
		No return, move object.

	'''

	containers = getContainers(iSelection)
	rsize = len(containers)
	
	# if no container, do nothing
	if rsize == 0:
		return
	
	# calculate offset to remove
	toRemove = ""
	i = 0
	while i < rsize and i < gSearchDepth:

		c = containers[i]

		if c.isDerivedFrom("App::LinkGroup"):
			try:
				p = c.Placement
				if toRemove == "":
					toRemove = p.inverse()
				else:
					toRemove = toRemove * p.inverse()
			except:
				skip = 1
	
		i = i + 1

	# remove offset and move to container
	i = 0
	while i < rsize and i < gSearchDepth:
		
		c = containers[i]

		if c.isDerivedFrom("App::LinkGroup"):
			for o in iObjects:
					
				o.Placement = o.Placement * toRemove

				FreeCADGui.Selection.addSelection(o)
				o.adjustRelativeLinks(c)
				c.ViewObject.dropObject(o, None, '', [])
				FreeCADGui.Selection.clearSelection()

			FreeCAD.ActiveDocument.recompute()
			
			return
			
		i = i + 1


# ###################################################################################################################
def adjustClonePosition(iPad, iX, iY, iZ):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		This function has been created for magicMove tool to adjust Clone position.
		If you make Clone from Pad and the Pad has not zero Sketch.AttachmentOffset, 
		the Clone has Placement set to XYZ (0,0,0) but is not in the zero position. 
		So you have to remove Sketch offset from the Clone position. 
		I guess the BoundBox is the correct solution here.
	
	Args:
	
		iPad: Pad object with not zero Sketch.AttachmentOffset used to create new Clone
		iX: X Axis object position
		iY: Y Axis object position
		iZ: Z Axis object position

	Usage:
	
		[ x, y, z ] = MagicPanels.adjustClonePosition(o, x, y, z)

	Result:
	
		Returns array with new correct [ x, y, z ] values.

	'''

	x = iX - float(iPad.Shape.BoundBox.XMin)
	y = iY - float(iPad.Shape.BoundBox.YMin)
	z = iZ - float(iPad.Shape.BoundBox.ZMin)

	return [ x, y, z ]


# ###################################################################################################################
def getPlacement(iObj, iType="clean"):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		Gets placement with rotation info for given object.
		Note: This is useful if you not use containers. 
	
	Args:
	
		iObj: object to get placement
		iType: 
			* "clean" - old way good for simple objects but it not works if the object has AttachmentOffset set or there are multiple Pads and only the first one has AttachmentOffset set
			* "BoundBox" - return [ XMin, YMin, ZMin ] from object BoundBox, this way solves the problem with AttachmentOffset but you need to be careful, but if the object has containers offset, for example Placement set at Part, Body or LinkGroups additionally you have to add the containers offset, also there will be problem with additional rotation

	Usage:
	
		[ x, y, z, r ] = MagicPanels.getPlacement(o)
		[ x, y, z, r ] = MagicPanels.getPlacement(o, "clean")
		[ x, y, z, r ] = MagicPanels.getPlacement(o, "BoundBox")

	Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

	'''

	if iType == "BoundBox":
		
		x = float(iObj.Shape.BoundBox.XMin)
		y = float(iObj.Shape.BoundBox.YMin)
		z = float(iObj.Shape.BoundBox.ZMin)
		r = iObj.Placement.Rotation

		return [ x, y, z, r ]

	if iType == "clean":
		
		if iObj.isDerivedFrom("PartDesign::Pad"):
			
			skip = 0
			
			try:
				direction = getDirection(iObj)
			except:
				skip = 1
			
			# for normal rectangular Pad
			if skip == 0:
				ref = iObj.Profile[0].AttachmentOffset
				
			# for irregular shapes
			else:
				ref = iObj.Profile[0].Placement
			
		elif iObj.isDerivedFrom("Sketcher::SketchObject"):
			ref = iObj.AttachmentOffset
		else:
			ref = iObj.Placement
			
		x = ref.Base.x
		y = ref.Base.y
		z = ref.Base.z
		r = ref.Rotation

		return [ x, y, z, r ]


# ###################################################################################################################
def getGlobalPlacement(iObj, iType="FreeCAD"):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		Calls FreeCAD getGlobalPlacement at base object, and return useful form of placement.
	
	Args:
	
		iObj: object to get placement
		iType:
			* "FreeCAD" - return getGlobalPlacement for object or for Sketch if iObj is Pad 
			* "BoundBox" - return [ XMin, YMin, ZMin ] from BoundBox
	Usage:
	
		[ x, y, z, r ] = MagicPanels.getGlobalPlacement(o)
		[ x, y, z, r ] = MagicPanels.getGlobalPlacement(o, "BoundBox")

	Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

	'''

	if iType == "FreeCAD":
		
		o = getReference(iObj)

		if o.isDerivedFrom("PartDesign::Pad"):
			ref = o.Profile[0]
		else:
			ref = o

		p = ref.getGlobalPlacement()

		x = p.Base.x
		y = p.Base.y
		z = p.Base.z
		r = p.Rotation

		return [ x, y, z, r ]

	if iType == "BoundBox":
		
		return [ 
			iObj.Shape.BoundBox.XMin, 
			iObj.Shape.BoundBox.YMin, 
			iObj.Shape.BoundBox.ZMin, 
			iObj.Placement.Rotation
			]
		

# ###################################################################################################################
def setPlacement(iObj, iX, iY, iZ, iR, iAnchor=""):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		Sets placement with rotation for given object.
	
	Args:

		iObj: object to set custom placement and rotation
		iX: X Axis object position
		iY: Y Axis object position
		iZ: Z Axis object position
		iR: Rotation object
		iAnchor="" (optional): anchor for placement instead of 0 vertex, FreeCAD.Vector(x, y, z)

	Usage:
	
		MagicPanels.setPlacement(gObj, 100, 100, 200, r)

	Result:
	
		Object gObj should be moved into 100, 100, 200 position without rotation.

	'''

	# recalculate position for custom anchor
	if iAnchor != "":
		
		[ oX, oY, oZ, oR ] = getPlacement(iObj)
		aX, aY, aZ = iAnchor[0], iAnchor[1], iAnchor[2] 
		
		offset = getVertexAxisCross(oX, aX)
		
		if oX < aX:
			iX = iX - offset
		else:
			iX = iX + offset
		
		offset = getVertexAxisCross(oY, aY)
		
		if oY < aY:
			iY = iY - offset
		else:
			iY = iY + offset
			
		offset = getVertexAxisCross(oZ, aZ)
		
		if oZ < aZ:
			iZ = iZ - offset
		else:
			iZ = iZ + offset
	
	# default anchor 0 vertex if not set above
	
	FreeCAD.ActiveDocument.openTransaction("setPlacement "+str(iObj.Label))
	
	if iObj.isDerivedFrom("PartDesign::Pad"):
		
		skip = 0
		
		try:
			direction = getDirection(iObj)
		except:
			skip = 1
		
		# for normal rectangular Pad
		if skip == 0:
			iObj.Profile[0].AttachmentOffset.Base = FreeCAD.Vector(iX, iY, iZ)
			iObj.Profile[0].AttachmentOffset.Rotation = iR
		
		# for irregular shapes
		else:
			iObj.Profile[0].Placement.Base = FreeCAD.Vector(iX, iY, iZ)
			iObj.Profile[0].Placement.Rotation = iR
		
	elif iObj.isDerivedFrom("Sketcher::SketchObject"):
		iObj.Placement.Base = FreeCAD.Vector(iX, iY, iZ)
		iObj.Placement.Rotation = iR
		
	else:
		iObj.Placement.Base = FreeCAD.Vector(iX, iY, iZ)
		iObj.Placement.Rotation = iR
	
	FreeCAD.ActiveDocument.commitTransaction()


# ###################################################################################################################
def getSketchPlacement(iSketch, iType):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		Gets placement dedicated to move and copy Sketch directly.
	
	Args:
	
		iSketch: Sketch object
		iType: 
			"attach" - AttachmentOffset position, need to be converted later
			"clean" - directly from Placement, so the AttachmentOffset don't need to be converted
			"global" - global Sketch position, can be directly set to object

	Usage:
	
		[ x, y, z, r ] = MagicPanels.getSketchPlacement(sketch, "global")

	Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

	'''

	if iType == "attach":
		x = iSketch.AttachmentOffset.Base.x
		y = iSketch.AttachmentOffset.Base.y
		z = iSketch.AttachmentOffset.Base.z
		r = iSketch.AttachmentOffset.Rotation

	if iType == "clean":
		x = iSketch.Placement.Base.x
		y = iSketch.Placement.Base.y
		z = iSketch.Placement.Base.z
		r = iSketch.Placement.Rotation

	if iType == "global":
		gp = iSketch.getGlobalPlacement()
		x = gp.Base.x
		y = gp.Base.y
		z = gp.Base.z
		r = gp.Rotation

	return [ x, y, z, r ]


# ###################################################################################################################
def setSketchPlacement(iSketch, iX, iY, iZ, iR, iType):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		Set placement with rotation dedicated to move and copy Sketch directly.
	
	Args:

		iSketch: Sketch object to set custom placement and rotation
		iX: X Axis object position
		iY: Y Axis object position
		iZ: Z Axis object position
		iR: Rotation object
		iType: 
			"global" - global Sketch position, good before Pocket or any other operation, Sketch global 
						position is temporary, FreeCAD bug? after Sketch edit the Sketch position will 
						be lost, use "attach" to keep it
			"attach" - AttachmentOffset position, global position will be converted to AttachmentOffset, 
						make sure the Support is set for Sketch, the Clones may not have Support, 
						use global instead
			"auto" - recognize if Sketch has Support, if yes this will be "attach", if no Support this 
						will be "global", it is useful to move Pads

	Usage:
	
		MagicPanels.setSketchPlacement(sketch, 100, 100, 200, r, "global")

	Result:
	
		Object Sketch should be moved.

	'''

	FreeCAD.ActiveDocument.openTransaction("setSketchPlacement "+str(iType))

	if iType == "auto":
		
		iType = "global"
		try:
			try:
				plane = iSketch.Support[0][0].Name
			except:
				plane = iSketch.AttachmentSupport[0][0].Name
				
			if plane.startswith("XY") or plane.startswith("XZ") or plane.startswith("YZ"):
				iType = "attach"
		except:
			skip = 1

	if iType == "attach":

		import math
		
		try:
			plane = iSketch.Support[0][0].Name
		except:
			plane = iSketch.AttachmentSupport[0][0].Name

		rX = iR.Axis.x
		rY = iR.Axis.y
		rZ = iR.Axis.z
		rAngle = math.degrees(iR.Angle)
		
		if plane.startswith("XY"):
			x, y, z = iX, iY, iZ
			r = FreeCAD.Rotation(FreeCAD.Vector(rX, rY, rZ), rAngle)

		if plane.startswith("XZ"):
			x, y, z = iX, iZ, -iY
			r = FreeCAD.Rotation(FreeCAD.Vector(rX, rZ, -rY), rAngle)

		if plane.startswith("YZ"):
			x, y, z = iX, iY, iZ
			r = FreeCAD.Rotation(FreeCAD.Vector(rY, rZ, rX), rAngle)
		
		iSketch.AttachmentOffset.Base = FreeCAD.Vector(x, y, z)
		iSketch.AttachmentOffset.Rotation = r

	if iType == "global":

		iSketch.Placement.Base = FreeCAD.Vector(iX, iY, iZ)
		iSketch.Placement.Rotation = iR

	FreeCAD.ActiveDocument.commitTransaction()


# ###################################################################################################################
def getContainerPlacement(iObj, iType="clean"):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		This function returns placement for the object with all 
		containers offsets or clean. The given object might be container or 
		selected object, the base Cube or Pad.
	
	Args:
	
		iObj: object to get placement
		iType (optional): 
			"clean" - to get iObj.Placement, 
			"offset" to get iObj.Placement with containers offset.

	Usage:
	
		[ x, y, z, r ] = MagicPanels.getContainerPlacement(o, "clean")
		[ x, y, z, r ] = MagicPanels.getContainerPlacement(o, "offset")

	Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object - not supported yet

	'''

	# direct placement only for object
	if iType == "clean":
		
		if iObj.isDerivedFrom("PartDesign::Pad"):

			[ x, y, z, r ] = getSketchPlacement(iObj.Profile[0], "clean")
			return [ x, y, z, r ]

		else:

			x = iObj.Placement.Base.x
			y = iObj.Placement.Base.y
			z = iObj.Placement.Base.z
			r = iObj.Placement.Rotation

			return [ x, y, z, r ]
	
	# placement with all needed offsets
	if iType == "offset":
		
		if iObj.isDerivedFrom("Sketcher::SketchObject"):
			[ x, y, z, r ] = getSketchPlacement(iObj, "global")
			return [ x, y, z, r ]
			
		# get base object
		objRef = getReference(iObj)
		
		if objRef.isDerivedFrom("PartDesign::Pad"):
			
			# FreeCAD getGlobalPlacement for Sketch not returns LinkGroup offset
			# so you have to get clean placement and add all offsets on your own
			[ x, y, z, r ] = getSketchPlacement(objRef.Profile[0], "clean")
			
			[ coX, coY, coZ, coR ] = getContainersOffset(objRef)
			x = x + coX
			y = y + coY
			z = z + coZ
			
			return [ x, y, z, r ]

		else:

			# get base object placement, the starting point
			x = objRef.Placement.Base.x
			y = objRef.Placement.Base.y
			z = objRef.Placement.Base.z
			r = objRef.Placement.Rotation
			
			# get offsets of all containers
			[ coX, coY, coZ, coR ] = getContainersOffset(objRef)
			x = x + coX
			y = y + coY
			z = z + coZ

			return [ x, y, z, r ]

	return [ "", "", "", "" ]


# ###################################################################################################################
def setContainerPlacement(iObj, iX, iY, iZ, iR, iAnchor="normal"):
	'''
	
	# > [!CAUTION]
	# > ########################################################################################
	# > THIS FUNCTION IS DEPRECATED !!!
	# > ########################################################################################
	
	Description:
	
		Set placement function, especially used with containers.
	
	Args:

		iObj: object or container to set placement, for example Body, LinkGroup, Cut, Pad, Cube, Sketch, Cylinder
		iX: X Axis object position
		iY: Y Axis object position
		iZ: Z Axis object position
		iR: 
			0 - means rotation value set to iObj.Placement.Rotation
			R - custom FreeCAD.Placement.Rotation object
		iAnchor (optional):
			"clean" - set directly to iObj.Placement, if object is Pad set to Sketch directly
			"normal" - default object anchor with global vertices calculation
			"center" - anchor will be center of the object (CenterOfMass)
			[ iAX, iAY, iAZ ] - custom anchor, this should be global position

	Usage:
		
		MagicPanels.setContainerPlacement(cube, 100, 100, 200, 0, "clean")
		MagicPanels.setContainerPlacement(pad, 100, 100, 200, 0, "normal")
		MagicPanels.setContainerPlacement(body, 100, 100, 200, 0, "center")

	Result:
	
		Object should be moved into 100, 100, 200 position with exact anchor.

	'''
	
	X, Y, Z, R = iX, iY, iZ, iR

	if iR == 0:
		R = iObj.Placement.Rotation

	# ###############################################################################
	# direct set
	# ###############################################################################

	if iAnchor == "clean":
		
		FreeCAD.ActiveDocument.openTransaction("setContainerPlacement "+str(iAnchor))
		
		if iObj.isDerivedFrom("PartDesign::Pad"):
			setSketchPlacement(iObj.Profile[0], X, Y, Z, R, "global")
		else:
			iObj.Placement.Base = FreeCAD.Vector(X, Y, Z)
			iObj.Placement.Rotation = R

		FreeCAD.ActiveDocument.commitTransaction()
		return

	# ###############################################################################
	# custom set
	# ###############################################################################

	# set starting point
	[ oX, oY, oZ, oR ] = getContainerPlacement(iObj, "clean")
	
	# switch from local to global vertices
	[[ goX, goY, goZ ]] = getVerticesPosition([[ oX, oY, oZ ]], iObj)

	# save object placement for later use
	X, Y, Z = goX, goY, goZ

	# custom anchor = object anchor
	if iAnchor == "normal":
		aX, aY, aZ = goX, goY, goZ

	elif iAnchor == "center":
		[ aX, aY, aZ ] = getObjectCenter(iObj)
		[[ aX, aY, aZ ]] = getVerticesPosition([[ aX, aY, aZ ]], iObj)

	else:
		aX, aY, aZ = iAnchor[0], iAnchor[1], iAnchor[2]

	# calculate diff between object anchor and custom anchor
	if iAnchor != "normal":
		[ moveX, moveY, moveZ ] = getPlacementDiff([goX, goY, goZ], [ aX, aY, aZ])
		X = X - moveX
		Y = Y - moveY
		Z = Z - moveZ

	# calculate diff between object anchor and new given position iX, iY, iZ
	[ moveX, moveY, moveZ ] = getPlacementDiff([goX, goY, goZ], [ iX, iY, iZ])
	X = X + moveX
	Y = Y + moveY
	Z = Z + moveZ

	# switch from global to local vertices
	[[ X, Y, Z ]] = removeVerticesPosition([[ X, Y, Z ]], iObj)

	FreeCAD.ActiveDocument.openTransaction("setContainerPlacement "+str(iAnchor))
	# set placement
	iObj.Placement.Base = FreeCAD.Vector(X, Y, Z)
	iObj.Placement.Rotation = R
	FreeCAD.ActiveDocument.commitTransaction()


# ###################################################################################################################
'''
# Functions for MagicPanels library config
'''
# ###################################################################################################################


def updateGlobals():
	'''
	Description:
	
		This function update MagicPanels library globals from user settings.
	
	Args:
		none, user config may not exist, so should not be direct assign
		
	Usage:
	
		MagicPanels.updateGlobals()

	Result:
	
		there is no return, just overwrite all MagicPanels globals from user config

	'''

	# #######################################################
	# settings
	# #######################################################

	# Woodworking User Settings
	wus = FreeCAD.ParamGet(gSettingsPref)
	wusStrings = wus.GetStrings()
	wusBools = wus.GetBools()
	
	# FreeCAD kernel version
	try:
		global gKernelVersion
		gKernelVersion = float( str(FreeCAD.Version()[0]) + "." + str(FreeCAD.Version()[1]) + str(FreeCAD.Version()[2]) )
	except:
		skip = 1

	# #######################################################
	# page 1
	# #######################################################

	# theme
	try:
		if "wTheme" in wusStrings:
			global gTheme
			gTheme = wus.GetString('wTheme')
	except:
		skip = 1

	# wood thickness
	try:
		if "wWoodThickness" in wusStrings:
			global gWoodThickness
			gWoodThickness = float( wus.GetString('wWoodThickness') )
	except:
		skip = 1

	try:
		if "wWoodSizeX" in wusStrings:
			global gWoodSizeX
			gWoodSizeX = float( wus.GetString('wWoodSizeX') )
	except:
		skip = 1
	
	try:
		if "wWoodSizeY" in wusStrings:
			global gWoodSizeY
			gWoodSizeY = float( wus.GetString('wWoodSizeY') )
	except:
		skip = 1

	# color
	try:
		if "wWoodColorR" in wusStrings:
			cR = wus.GetString('wWoodColorR')
			cG = wus.GetString('wWoodColorG')
			cB = wus.GetString('wWoodColorB')
			cA = wus.GetString('wWoodColorA')
			colorArr = [ int(float(cR)), int(float(cG)), int(float(cB)), int(float(cA)) ]
			global gDefaultColor
			gDefaultColor = convertColor(colorArr, "kernel")
	except:
		skip = 1

	# window stays on top
	try:
		if "wWindowStaysOnTop" in wusBools:
			global gWindowStaysOnTop
			gWindowStaysOnTop = wus.GetBool('wWindowStaysOnTop')
	except:
		skip = 1

	# current selection
	try:
		if "wCurrentSelection" in wusBools:
			global gCurrentSelection
			gCurrentSelection = wus.GetBool('wCurrentSelection')
	except:
		skip = 1

	# #######################################################
	# page 2
	# #######################################################

	try:
		if "wFrontInsideThickness" in wusStrings:
			global gFrontInsideThickness
			gFrontInsideThickness = float( wus.GetString('wFrontInsideThickness') )
	except:
		skip = 1

	try:
		if "wFrontInsideOffsetL" in wusStrings:
			global gFrontInsideOffsetL
			gFrontInsideOffsetL = float( wus.GetString('wFrontInsideOffsetL') )
	except:
		skip = 1

	try:
		if "wFrontInsideOffsetR" in wusStrings:
			global gFrontInsideOffsetR
			gFrontInsideOffsetR = float( wus.GetString('wFrontInsideOffsetR') )
	except:
		skip = 1

	try:
		if "wFrontInsideOffsetB" in wusStrings:
			global gFrontInsideOffsetB
			gFrontInsideOffsetB = float( wus.GetString('wFrontInsideOffsetB') )
	except:
		skip = 1

	try:
		if "wFrontInsideOffsetT" in wusStrings:
			global gFrontInsideOffsetT
			gFrontInsideOffsetT = float( wus.GetString('wFrontInsideOffsetT') )
	except:
		skip = 1

	try:
		if "wFrontOutsideThickness" in wusStrings:
			global gFrontOutsideThickness
			gFrontOutsideThickness = float( wus.GetString('wFrontOutsideThickness') )
	except:
		skip = 1

	try:
		if "wFrontOutsideOffsetL" in wusStrings:
			global gFrontOutsideOffsetL
			gFrontOutsideOffsetL = float( wus.GetString('wFrontOutsideOffsetL') )
	except:
		skip = 1

	try:
		if "wFrontOutsideOffsetR" in wusStrings:
			global gFrontOutsideOffsetR
			gFrontOutsideOffsetR = float( wus.GetString('wFrontOutsideOffsetR') )
	except:
		skip = 1

	try:
		if "wFrontOutsideOffsetB" in wusStrings:
			global gFrontOutsideOffsetB
			gFrontOutsideOffsetB = float( wus.GetString('wFrontOutsideOffsetB') )
	except:
		skip = 1

	try:
		if "wFrontOutsideOffsetT" in wusStrings:
			global gFrontOutsideOffsetT
			gFrontOutsideOffsetT = float( wus.GetString('wFrontOutsideOffsetT') )
	except:
		skip = 1

	try:
		if "wShelfThickness" in wusStrings:
			global gShelfThickness
			gShelfThickness = float( wus.GetString('wShelfThickness') )
	except:
		skip = 1

	try:
		if "wBackInsideThickness" in wusStrings:
			global gBackInsideThickness
			gBackInsideThickness = float( wus.GetString('wBackInsideThickness') )
	except:
		skip = 1

	try:
		if "wBackOutsideThickness" in wusStrings:
			global gBackOutsideThickness
			gBackOutsideThickness = float( wus.GetString('wBackOutsideThickness') )
	except:
		skip = 1

	# #######################################################
	# page 3
	# #######################################################

	# edgeband thickness
	try:
		if "wEdgebandThickness" in wusStrings:
			global gEdgebandThickness
			gEdgebandThickness = float( wus.GetString('wEdgebandThickness') )
	except:
		skip = 1

	# edgeband apply way
	try:
		if "wEdgebandApply" in wusStrings:
			global gEdgebandApply
			gEdgebandApply = wus.GetString('wEdgebandApply')
	except:
		skip = 1

	# color
	try:
		if "wEdgebandColorR" in wusStrings:
			cR = wus.GetString('wEdgebandColorR')
			cG = wus.GetString('wEdgebandColorG')
			cB = wus.GetString('wEdgebandColorB')
			cA = wus.GetString('wEdgebandColorA')
			colorArr = [ int(float(cR)), int(float(cG)), int(float(cB)), int(float(cA)) ]
			global gEdgebandColor
			gEdgebandColor = convertColor(colorArr, "kernel")
	except:
		skip = 1


# ###################################################################################################################
# UPDATE GLOBALS HERE AFTER FUNCTIONS LOADED
# ###################################################################################################################


'''
FreeCAD.Console.PrintMessage("\n\n")
FreeCAD.Console.PrintMessage(gKernelVersion)
FreeCAD.Console.PrintMessage("\n")
FreeCAD.Console.PrintMessage(gTheme)
FreeCAD.Console.PrintMessage("\n")
FreeCAD.Console.PrintMessage(gWoodThickness)
FreeCAD.Console.PrintMessage("\n")
FreeCAD.Console.PrintMessage(gDefaultColor)
FreeCAD.Console.PrintMessage("\n")
FreeCAD.Console.PrintMessage(gWindowStaysOnTop)
FreeCAD.Console.PrintMessage("\n")
FreeCAD.Console.PrintMessage(gCurrentSelection)
'''

# not assign directly to values because user config values may not exist yet
# and do not repeat default value inside the update function in return to avoid inconsistency
updateGlobals()


'''
FreeCAD.Console.PrintMessage("\n\n")
FreeCAD.Console.PrintMessage(gKernelVersion)
FreeCAD.Console.PrintMessage("\n")
FreeCAD.Console.PrintMessage(gTheme)
FreeCAD.Console.PrintMessage("\n")
FreeCAD.Console.PrintMessage(gWoodThickness)
FreeCAD.Console.PrintMessage("\n")
FreeCAD.Console.PrintMessage(gDefaultColor)
FreeCAD.Console.PrintMessage("\n")
FreeCAD.Console.PrintMessage(gWindowStaysOnTop)
FreeCAD.Console.PrintMessage("\n")
FreeCAD.Console.PrintMessage(gCurrentSelection)
'''

# ###################################################################################################################
