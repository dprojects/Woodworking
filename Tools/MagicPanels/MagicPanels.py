# ###################################################################################################################
'''

# MagicPanels

	This is MagicPanels library for Woodworking workbench.
	Darek L (github.com/dprojects)

Usage:

	import MagicPanels
	returned_value = MagicPanels.function(args)

Functions at this library:

* Should not have error handling and pop-ups, so you can call it from GUI tools in loops.
* Should return value, if further processing needed.

'''
# ###################################################################################################################
__doc__ = "This is MagicPanels library for Woodworking workbench."
__author__ = "Darek L (github.com/dprojects)"


# ###################################################################################################################
#
# Imports
#
# ###################################################################################################################


import FreeCAD, FreeCADGui
from PySide import QtGui
from PySide import QtCore

translate = FreeCAD.Qt.translate

def QT_TRANSLATE_NOOP(context, text): #
	return text


# ###################################################################################################################
'''
# Globals
'''
# ###################################################################################################################


gRoundPrecision = 2 # should be set according to the user FreeCAD GUI settings


# end globals (for API generator)


# ###################################################################################################################
'''
# Functions for general purpose
'''
# ###################################################################################################################


# ###################################################################################################################
def equal(iA, iB):
	'''
	equal(iA, iB) - At FreeCAD there are many values like 1.000006, especially for PartDesign objects. 
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
	touchTypo(iObj) - touch the typo so that the typo-snake does not notice it ;-) LOL
	
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
	normalizeBoundBox(iBoundBox) - return normalized version of BoundBox. All values 0.01 will be rounded 
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
# Vertices
'''
# ###################################################################################################################


# ###################################################################################################################
def showVertex(iVertex, iRadius):
	'''
	showVertex(iVertex) - create sphere at given vertex, to show where is the point for debug purposes.
	
	Args:
	
		iVertex: vertex object
		iRadius: ball Radius

	Usage:
	
		MagicPanels.showVertex(obj.Shape.CenterOfMass, 20)

	Result:
	
		show vertex
	'''
	
	try:
		FreeCAD.ActiveDocument.removeObject("showVertex")
	except:
		skip = 1
	
	s1 = FreeCAD.ActiveDocument.addObject("Part::Sphere","showVertex")
	s1.Placement = FreeCAD.Placement(iVertex, FreeCAD.Rotation(0, 0, 0))
	s1.ViewObject.ShapeColor = (1.0, 0.0, 0.0, 0.0)
	s1.Radius = iRadius
	
	FreeCAD.ActiveDocument.recompute()
		

# ###################################################################################################################
def getVertex(iFace, iEdge, iVertex):
	'''
	getVertex(iFace, iEdge, iVertex) - get vertex values for face, edge and vertex index.
	
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
def getVertexAxisCross(iA, iB):
	'''
	getVertexAxisCross(iA, iB) - get (iB - iA) value.
	
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
	getVerticesPlane(iV1, iV2) - get axes with the same values
	
	Args:
	
		iV1: vertex object
		iV2: vertex object
	
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
def setVertexPadding(iObj, iVertex, iPadding, iAxis):
	'''
	setVertexPadding(iObj, iVertex, iPadding, iAxis) - set padding offset from given vertex to inside the object.
	Do not use it at getPlacement for Pads. Use 0 vertex instead.
	
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
'''
# Edges
'''
# ###################################################################################################################


# ###################################################################################################################
def getEdgeVertices(iEdge):
	'''
	getEdgeVertices(iEdge) - get all vertices values for edge.
	
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
def getEdgeNormalized(iV1, iV2):
	'''
	getEdgeNormalized(iV1, iV2) - returns vertices with exact sorted order V1 > V2, mostly used 
	to normalize Pad vertices
	
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
	getEdgeIndex(iObj, iEdge) - returns edge index for given object and edge.
	
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
	getEdgeIndexByKey(iObj, iBoundBox) - returns edge index for given edge BoundBox.
	
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
def getEdgePlane(iEdge):
	'''
	getEdgePlane(iEdge) - returns orientation for the edge, changed axis, as "X", "Y" or "Z".
	
	Args:
	
		iEdge: edge object

	Usage:
	
		plane = MagicPanels.getEdgePlane(edge)

	Result:
	
		return string "X", "Y" or "Z".

	'''

	[ v1, v2 ] = getEdgeVertices(iEdge)
	
	if not equal(v1[0], v2[0]):
		return "X"

	if not equal(v1[1], v2[1]):
		return "Y"

	if not equal(v1[2], v2[2]):
		return "Z"
		
	return ""


# ###################################################################################################################
'''
# Faces
'''
# ###################################################################################################################


# ###################################################################################################################
def getFaceIndex(iObj, iFace):
	'''
	getFaceIndex(iObj, iFace) - returns face index for given object and face.
	
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
	getFaceIndexByKey(iObj, iBoundBox) - returns face index for given face BoundBox.
	
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
	getFaceVertices(iFace, iType="4") - get all vertices values for face.
	
	Args:
	
		iFace: face object
		iType (optional): 
			* "4" - 4 vertices for normal Cube
			* "all" - get all vertices, for example for Cut object

	Usage:
	
		[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(gFace)
		vertices = MagicPanels.getFaceVertices(gFace, "all")

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
	
	return ""


# ###################################################################################################################
def getFaceType(iObj, iFace):
	'''
	getFaceType(iObj, iFace) - get face type, if this is "edge" or "surface".
	
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
	getFaceEdges(iObj, iFace) - get all edges for given face grouped by sizes.
	
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
	sizes = getSizes(iObj)
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
	getFacePlane(iFace) - get face plane in notation "XY", "XZ", "YZ". 

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
	getFaceSink(iObj, iFace) - get face sink axis direction in notation "+", or "-".

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
	getFaceObjectRotation(iObj, iFace) - get face object rotation to apply to the new created object at face. 
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
	getFaceDetails(iObj, iFace) - allow to get detailed information for face direction.
	
	Args:
	
		iObj: selected object
		iFace: selected face object

	Usage:
	
		[ plane, type ] = MagicPanels.getFaceDetails(gObj, gFace)

	Result:
	
		[ "XY", "surface" ] - if the direction is XY and it is surface, no thickness edge
		[ "XY", "edge" ] - if the direction is XY and it is edge, there is thickness edge
		[ "XY", "equal" ] - if the direction is XY and both edges are equal
		
		Note: The first argument can be "XY", "YX", "XZ", "ZX", "YZ", "ZY". 
		This is related to face not to object. The object direction will be different.
		
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
'''
# References
'''
# ###################################################################################################################


# ###################################################################################################################
def getReference(iObj="none"):
	'''
	getReference(iObj="none") - get reference to the selected or given object.
	
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
	
	# Mortise and Tenon
	if (
		( obj.isDerivedFrom("PartDesign::Pocket") and obj.BaseFeature != None ) or
		( obj.isDerivedFrom("PartDesign::Pad") and obj.BaseFeature != None )
		):
		
		i = 0
		base = obj
		while True:
			
			if base.BaseFeature == None:
				return base
			
			else:
			
				if (
					obj.isDerivedFrom("PartDesign::Pad") or 
					obj.isDerivedFrom("PartDesign::Pocket")
					):
					base = base.BaseFeature
			
			# search depth level
			if i > 200:
				break
			else:
				i = i + 1
	
	# construction Profiles and Frames
	if ( 
		obj.isDerivedFrom("PartDesign::Thickness") or 
		obj.isDerivedFrom("PartDesign::Chamfer")
		):
		return obj.Base[0]

	# boolean Cut and Holes
	if (
		obj.isDerivedFrom("Part::Cut") or 
		obj.isDerivedFrom("PartDesign::Hole")
		):
		
		i = 0
		base = obj
		while True:
			
			if base.isDerivedFrom("Part::Box") or base.isDerivedFrom("PartDesign::Pad"):
				return base
			
			else:
			
				if obj.isDerivedFrom("Part::Cut"):
					base = base.Base
					
				if obj.isDerivedFrom("PartDesign::Hole"):
					base = base.BaseFeature
			
			# search depth level
			if i > 200:
				break
			else:
				i = i + 1
	
	# not recognized
	if obj != "":
		return obj
	
	return -1


# ###################################################################################################################
'''
# Sizes
'''
# ###################################################################################################################


# ###################################################################################################################
def getSizes(iObj):
	'''
	getSizes(iObj) - allow to get sizes for object (iObj), according to the object type. The values are not sorted.
	
	Args:
	
		iObj: object to get sizes

	Usage:
	
		[ size1, size2, size3 ] = MagicPanels.getSizes(obj)

	Result:
	
		Returns [ Length, Width, Height ] for Cube.

	'''

	# for Cube panels
	if iObj.isDerivedFrom("Part::Box"):

		return [ iObj.Length.Value, iObj.Width.Value, iObj.Height.Value ]

	# for Pad panels
	if iObj.isDerivedFrom("PartDesign::Pad"):
		
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
			return sizes
			
		else:
			return [ sizeX, sizeY, iObj.Length.Value ]

	# to move drill bits more precisely
	if iObj.isDerivedFrom("Part::Cylinder"):
		return [ 1, 1, 1 ]

	if iObj.isDerivedFrom("Part::Cone"):
		return [ 1, 1, 1 ]
	
	if iObj.isDerivedFrom("PartDesign::Thickness"):
		
		sizeX = ""
		sizeY = ""

		for c in iObj.Base[0].Profile[0].Constraints:
			if c.Name == "SizeX":
				sizeX = c.Value
			if c.Name == "SizeY":
				sizeY = c.Value
			
		if sizeX == "" or sizeY == "":
			sizes = getSizesFromVertices(iObj.Base[0].Profile[0])
			sizes.sort()
			sizes.pop(0)
			sizes.insert(0, iObj.Base[0].Length.Value)
			return sizes
			
		else:
			return [ sizeX, sizeY, iObj.Base[0].Length.Value ]
	
	# for custom objects
	try:
		
		return [ iObj.Base_Width.Value, iObj.Base_Height.Value, iObj.Base_Length.Value ]
		
	except:
		
		# to move all furniture more quickly
		return [ 100, 100, 100 ]


# ###################################################################################################################
def getSizesFromVertices(iObj):
	'''
	getSizesFromVertices(iObj) - get occupied space by the object from vertices.
	
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
	getSizesFromBoundBox(iObj) - get occupied space by the object from BoundBox. This can be useful for round shapes, 
	where is no vertices at object edges, e.g. cylinders, circle at Sketch.
	
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


	mX = round(iObj.Shape.BoundBox.XLength, gRoundPrecision)
	mY = round(iObj.Shape.BoundBox.YLength, gRoundPrecision)
	mZ = round(iObj.Shape.BoundBox.ZLength, gRoundPrecision)
	
	return [ mX, mY, mZ ]


# ###################################################################################################################
'''
# Measurements
'''
# ###################################################################################################################


# ###################################################################################################################
def showMeasure(iP1, iP2, iRef=""):
	'''
	showMeasure(iP1, iP2, iRef="") - create measurements object, I mean draw it. Now it use FreeCAD function 
	to create and draw object. But in the future this can be changed to more beautiful drawing without changing
	tools. 
	
	Args:
	
		iP1: starting point vertex object
		iP2: ending point vertex object
		iRef (optional): string for future TechDraw import or any other use, other tools

	Usage:
	
		m = MagicPanels.showMeasure(gP1, gP2, "Pad")

	Result:
	
		Create measure object, draw it and return measure object for further proccessing. 

	'''

	m = FreeCAD.ActiveDocument.addObject('App::MeasureDistance', "measure")
	m.P1 = iP1
	m.P2 = iP2
	
	if iRef != "":
		m.Label = "Measure "
		m.Label2 = str(iRef)
	else:
		m.Label = "Measure "
	
	m.ViewObject.LineColor = (1.0, 0.0, 0.0, 0.0)
	m.ViewObject.TextColor = (1.0, 0.0, 0.0, 0.0)
	m.ViewObject.FontSize = 24
	m.ViewObject.DistFactor = 0.25
	
	FreeCAD.ActiveDocument.recompute()
	
	return m


# ###################################################################################################################
def getDistanceBetweenFaces(iFace1, iFace2):
	'''
	getDistanceBetweenFaces(iFace1, iFace2) - get distance between iFace1 and iFace2
	
	Args:
	
		iFace1: face object
		iFace2: face object

	Usage:
	
		size = MagicPanels.getDistanceBetweenFaces(face1, face2)

	Result:

		return distance between face1 object and face2 object

	'''

	plane1 = getFacePlane(iFace1)
	plane2 = getFacePlane(iFace2)
	[ x1, y1, z1 ] = getVertex(iFace1, 0, 0)
	[ x2, y2, z2 ] = getVertex(iFace2, 0, 0)
	
	if plane1 == "XY" and plane2 == "XY":
		return round(abs(z1-z2), gRoundPrecision)

	if plane1 == "XZ" and plane2 == "XZ":
		return round(abs(y1-y2), gRoundPrecision)
		
	if plane1 == "YZ" and plane2 == "YZ":
		return round(abs(x1-x2), gRoundPrecision)

	return ""


# ###################################################################################################################
'''
# Direction, Plane, Orientation, Axis
'''
# ###################################################################################################################


# ###################################################################################################################
def getModelRotation(iX, iY, iZ):
	'''
	getModelRotation() - transform given iX, iY, iZ values to the correct vector, if the user rotated 3D model.

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
	getDirection(iObj) - allow to get Cube object direction (iType).
	
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
		
		ref = iObj.Profile[0].Support[0][0]
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
def getPlacement(iObj):
	'''
	getPlacement(iObj) - get placement with rotation info for given object.
	
	Args:
	
		iObj: object to get placement

	Usage:
	
		[ x, y, z, r ] = MagicPanels.getPlacement(gObj)

	Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

	'''

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
def setPlacement(iObj, iX, iY, iZ, iR, iAnchor=""):
	'''
	setPlacement(iObj, iX, iY, iZ, iR, iAnchor="") - set placement with rotation for given object.
	
	Args:

		iObj: object to set custom placement and rotation
		iX: X Axis object position
		iX: Y Axis object position
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
	

# ###################################################################################################################
def resetPlacement(iObj):
	'''
	resetPlacement(iObj) - reset placement for given object. Needed to set rotation for object at face.
	
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
def getSketchPlacement(iSketch, iType):
	'''
	getSketchPlacement(iSketch, iType) - get placement dedicated to move and copy Sketch directly.
	
	Args:
	
		iSketch: Sketch object
		iType: 
			"global" - global Sketch position
			"attach" - AttachmentOffset position

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
	setSketchPlacement(iSketch, iX, iY, iZ, iR, iType) - set placement with rotation dedicated to move and copy Sketch directly.
	
	Args:

		iSketch: Sketch object to set custom placement and rotation
		iX: X Axis object position
		iX: Y Axis object position
		iZ: Z Axis object position
		iR: Rotation object
		iType: 
			"global" - global Sketch position
			"attach" - AttachmentOffset position

	Usage:
	
		MagicPanels.setSketchPlacement(sketch, 100, 100, 200, r, "attach")

	Result:
	
		Object Sketch should be moved.

	'''

	if iType == "attach":
		
		iSketch.AttachmentOffset.Base = FreeCAD.Vector(iX, iY, iZ)
		iSketch.AttachmentOffset.Rotation = iR
		
	if iType == "global":
		
		iSketch.Placement.Base = FreeCAD.Vector(iX, iY, iZ)
		iSketch.Placement.Rotation = iR


# ###################################################################################################################
def convertPosition(iObj, iX, iY, iZ):
	'''
	convertPosition(iObj, iX, iY, iZ) - convert given position vector to correct position values according 
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
		
		obj = iObj.Support[0][0]
		faceName = str(iObj.Support[0][1]).replace("'","").replace(",","").replace("(","").replace(")","")
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
def getObjectCenter(iObj):
	'''
	getObjectCenter(iObj) - return Shape.CenterOfMass for the object or calculates center from vertices. 
	However, for Cone the CenterOfMass is not the center of object. More reliable is calculation 
	from vertices but some objects do not have all vertices to calculation. So, for now to handle 
	simple Pad objects and LinkGroups the CenterOfMass will be returned first.
	
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
def sizesToCubePanel(iObj, iType):
	'''
	sizesToCubePanel(iObj, iType) - converts selected object (iObj) sizes to Cube panel sizes into given direction (iType). 
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
	
	else:
		
		sizes = [ iObj.Base_Length.Value, iObj.Base_Width.Value, iObj.Base_Height.Value ]

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
	makePad(iObj, iPadLabel="Pad") - allows to create Part, Plane, Body, Pad, Sketch objects.
	
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

	[ X, Y, Z, r ] = getPlacement(iObj)
	
	if direction == "XY" or direction == "YX":
		[ x, y, z ] = [ X, Y, Z ]
	
	if direction == "XZ" or direction == "ZX":
		[ x, y, z ] = [ X, Z, -(Y+sizes[0]) ]

	if direction == "YZ" or direction == "ZY":
		[ x, y, z ] = [ Y, Z, X ]
	
	import Part, PartDesign
	import Sketcher
	import PartDesignGui

	doc = FreeCAD.ActiveDocument
	
	part = doc.addObject('App::Part', 'Part')
	part.Label = "Part, "+iPadLabel
	
	body = doc.addObject('PartDesign::Body', 'Body')
	body.Label = "Body, "+iPadLabel
	part.addObject(body)
	
	sketch = body.newObject('Sketcher::SketchObject', 'Sketch')
	sketch.Label = "Pattern, "+iPadLabel
	
	if direction == "XY" or direction == "YX":
		sketch.Support = (body.Origin.OriginFeatures[3])
	if direction == "XZ" or direction == "ZX":
		sketch.Support = (body.Origin.OriginFeatures[4])
	if direction == "YZ" or direction == "ZY":
		sketch.Support = (body.Origin.OriginFeatures[5])

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

	position = FreeCAD.Vector(x, y, z)
	sketch.AttachmentOffset = FreeCAD.Placement(position, r)

	pad = body.newObject('PartDesign::Pad', "Pad")
	pad.Label = iPadLabel
	pad.Profile = sketch
	pad.Length = FreeCAD.Units.Quantity(s[2])
	sketch.Visibility = False

	try:
		copyColors(iObj, pad)
	except:
		skip = 1

	doc.recompute()

	return [ part, body, sketch, pad ]


# ###################################################################################################################
'''
# Holes
'''
# ###################################################################################################################


# ###################################################################################################################
def makeHoles(iObj, iFace, iCylinders):
	'''
	makeHoles(iObj, iFace, iCylinders) - make holes

	Args:

		iObj: base object to make hole
		iFace: face of base object to make hole
		iCylinders: list of cylinders to make holes below each one

	Usage:

		holes = MagicPanels.makeHoles(obj, face, cylinders)
		
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
	
	else:
		
		body = base._Body

	# loop in drill bits and drill holes
	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = o.Placement.Rotation.Axis
		circleGeo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, o.Radius)
		holeSketch.addGeometry(circleGeo, False)
		
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1)) 
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 0, 2 * o.Radius)) 
		s = str(float(2 * o.Radius))+" mm"
		holeSketch.setDatum(1, FreeCAD.Units.Quantity(s))
		holeSketch.renameConstraint(1, u'Hole00Diameter')
		
		FreeCAD.ActiveDocument.recompute()
		
		# set position to hole Sketch
		[ x, y, z, r ] = getPlacement(o)
		setPlacement(holeSketch, x, y, z, r)
		
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
def makeCountersinks(iObj, iFace, iCones):
	'''
	makeCountersinks(iObj, iFace, iCones) - make countersinks

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
	
	else:
		
		body = base._Body
	
	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = o.Placement.Rotation.Axis
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
		[ x, y, z, r ] = getPlacement(o)
		setPlacement(holeSketch, x, y, z, r)
		
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
	makeCounterbores(iObj, iFace, iCones) - make counterbores

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
	
	else:
		
		body = base._Body

	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = o.Placement.Rotation.Axis
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
		[ x, y, z, r ] = getPlacement(o)
		setPlacement(holeSketch, x, y, z, r)
		
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
	makePocketHoles(iObj, iFace, iCones) - make pocket holes for invisible connections

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
	
	else:
		
		body = base._Body

	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = o.Placement.Rotation.Axis
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
		[ x, y, z, r ] = getPlacement(o)
		setPlacement(holeSketch, x, y, z, r)
		
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
	makeCounterbores2x(iObj, iFace, iCones) - make counterbores from both sides

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
	
	else:
		
		body = base._Body

	for o in objects:
		
		# create hole Sketch
		holeSketch1 = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch1.MapMode = 'FlatFace'

		axis = o.Placement.Rotation.Axis
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
		[ xs1, ys1, zs1, rs1 ] = getPlacement(o)
		setPlacement(holeSketch1, xs1, ys1, zs1, rs1)

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

		axis = o.Placement.Rotation.Axis
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
		setPlacement(o, xs2, ys2, zs2, rs2)
		Draft.rotate(o, 180, center, axis, False)
		
		# move & rotate sketch for hole
		[ xs3, ys3, zs3, rs3 ] = getPlacement(o)
		setPlacement(holeSketch2, xs3, ys3, zs3, rs3)
		
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
		setPlacement(o, xs1, ys1, zs1, rs1)
		
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
	makeCuts(iObjects) - allows to create multi bool cut operation at given objects. First objects 
	from iObjects is the base element and all other will cut the base. The copies will be created for cut. 
	
	Args:
	
		iObjects: objects to parse by multi bool cut

	Usage:
	
		cuts = MagicPanels.makeCuts(objects)

	Result:
	
		Array of cut objects will be returned.

	'''
	
	cuts = []
	
	i = 0
	for o in iObjects:
		
		i = i + 1
		
		if i == 1:
			base = o
			baseName = str(base.Name)
			baseLabel = str(base.Label)
			continue

		copy = FreeCAD.ActiveDocument.copyObject(o)
		copy.Label = "copy, " + o.Label
		
		if not hasattr(copy, "BOM"):
			info = QT_TRANSLATE_NOOP("App::Property", "Allows to skip this duplicated copy in BOM, cut-list report.")
			copy.addProperty("App::PropertyBool", "BOM", "Woodworking", info)
		
		copy.BOM = False
		
		cutName = baseName + str(i-1)
		cut = FreeCAD.ActiveDocument.addObject("Part::Cut", cutName)
		cut.Base = base
		cut.Tool = copy
		cut.Label = "Cut " + str(i-1) + ", " + baseLabel
		
		FreeCAD.ActiveDocument.recompute()
		
		base = cut
		cuts.append(cut)
		
	cut.Label = "Cut, " + baseLabel

	return cuts


# ###################################################################################################################
def makeFrame45cut(iObjects, iFaces):
	'''
	makeFrame45cut(iObjects, iFaces) - makes 45 frame cut with PartDesing Chamfer. 
	For each face the ends will be cut.
	
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
		frames.append(frame)
	
	return frames


# ###################################################################################################################
def makeChamferCut(iObjects, iEdges, iSizes, iLabels):
	'''
	makeChamferCut(iObjects, iEdges, iSizes, iLabels) - makes PartDesing Chamfer cut for edges array. But you can set 
	different size for each edge. Yes, you give edge objects, and you make chamfer for each edge, one by one, 
	with different size, but the most funny part is that the selected edge not exists because the Cube 
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
	makeMortise(iSketch, iDepth, iPad, iFace) - make Mortise pocket for given iSketch pattern

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
	sketch.Support = ""
	
	sketch.adjustRelativeLinks(body)
	body.ViewObject.dropObject(sketch, None, '', [])
	
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
	makeTenon(iSketch, iLength, iPad, iFace) - make Tenon pad for given iSketch pattern

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
	sketch.Support = ""
	
	sketch.adjustRelativeLinks(body)
	body.ViewObject.dropObject(sketch, None, '', [])

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
# Colors
'''
# ###################################################################################################################


# ###################################################################################################################
def copyColors(iSource, iTarget):
	'''
	copyColors(iSource, iTarget) - allows to copy colors from iSource object to iTarget object

	Args:

		iSource: source object
		iTarget: target object

	Usage:

		try:
			MagicPanels.copyColors(panel, copy)
		except:
			skip = 1

	Result:

		All colors structure should be copied from source to target.

	'''

	skip = 0
	
	try:
		iTarget.ViewObject.ShapeColor = iSource.ViewObject.ShapeColor
	except:
		skip = 1
		
	try:
		# copy edge and only for cubes because other objects have different face order
		if len(iTarget.ViewObject.DiffuseColor) == len(iSource.ViewObject.DiffuseColor):
			iTarget.ViewObject.DiffuseColor = iSource.ViewObject.DiffuseColor
		
		if len(iSource.ViewObject.DiffuseColor) > 0 and len(iTarget.ViewObject.DiffuseColor) == 1:
			iTarget.ViewObject.DiffuseColor = iSource.ViewObject.DiffuseColor[0]
	except:
		skip = 1
	
	try:
		iTarget.ViewObject.LineColor = iSource.ViewObject.LineColor
	except:
		skip = 1
	
	if skip == 0:
		return 0
	else:
		return -1


# ###################################################################################################################
'''
# Spreadsheet
'''
# ###################################################################################################################

def sheetGetKey(iC, iR):
	'''
	sheetGetKey(iC, iR) - allow to get key as letters for spreadsheet from given column and row index.

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
# Info screen
'''
# ###################################################################################################################


def showInfo(iCaller, iInfo, iNote="yes"):
	'''
	showInfo(iCaller, iInfo, iNote="yes") - allow to show Gui info box for all available function and multiple calls.

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
	
	filename = ""
	
	f = os.path.join(iconPath, iCaller+".xpm")
	if os.path.exists(f):
		filename = f
		info += '<img src="'+ filename + '" width="200" height="200" align="right"/>'
	
	f = os.path.join(iconPath, iCaller+".svg")
	if os.path.exists(f):
		filename = f
		info += '<svg>'
		info += '<img src="'+ filename + '" width="200" height="200" align="right"/>'
		info += '</svg>'
		
	f = os.path.join(iconPath, iCaller+".png")
	if os.path.exists(f):
		filename = f
		info += '<img src="'+ filename + '" width="200" height="200" align="right">'
	
	info += iInfo

	if iNote == "yes":
		
		info += '<br><br>'
		info += translate('showInfoAll', 'For features description and detailed tutorials please see:')
		info += '<br>' + '<a href="https://github.com/dprojects/Woodworking/tree/master/Docs">'
		info += translate('showInfoAll', 'Woodworking workbench documentation')
		info += '</a>'
		
	msg = QtGui.QMessageBox()
	msg.setWindowTitle(iCaller)
	msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
	msg.setText(info)
	msg.exec_()


# ###################################################################################################################
