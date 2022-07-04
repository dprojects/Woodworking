# ###################################################################################################################

__doc__ = "This is FreeCAD library for Magic Panels at Woodworking workbench."
__author__ = "Darek L (github.com/dprojects)"

# ###################################################################################################################

import FreeCAD, FreeCADGui
from PySide import QtGui
from PySide import QtCore


# ###################################################################################################################
# Functions - internal for this library purposes, no error handling
# ###################################################################################################################


# ############################################################################
def touchTypo(iObj):
	'''
	touchTypo(iObj) - touch the typo so that the typo-snake does not notice it ;-) LOL
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object to touch

	Usage:
	
		vs = touchTypo(o)
		
	Result:
	
		return Vertex + es for object o

	'''
	
	return getattr(iObj, "Vertex"+"es")


# ############################################################################
def getFaceIndex(iObj, iFace):
	'''
	getFaceIndex(iObj, iFace) - returns face index for given object and face.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object of the face
		iFace: face object
	
	Usage:
	
		faceIndex = getFaceIndex(gObj, gFace)
		
	Result:
	
		return int value for face

	'''

	index = 1
	for f in iObj.Shape.Faces:
		if str(f.BoundBox) == str(iFace.BoundBox):
			return index

		index = index + 1
	
	return -1


# ############################################################################
def getEdgeIndex(iObj, iEdge):
	'''
	getEdgeIndex(iObj, iEdge) - returns edge index for given object and edge.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object of the edge
		iEdge: edge object
	
	Usage:
	
		edgeIndex = getEdgeIndex(gObj, gEdge)
		
	Result:
	
		return int value for edge

	'''

	index = 1
	for e in iObj.Shape.Edges:
		if str(e.BoundBox) == str(iEdge.BoundBox):
			return index

		index = index + 1
	
	return -1


# ############################################################################
def getEdgeIndexByKey(iObj, iBoundBox):
	'''
	getEdgeIndexByKey(iObj, iBoundBox) - returns edge index for given edge BoundBox.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object of the edge
		iBoundBox: edge BoundBox
	
	Usage:
	
		edgeIndex = getEdgeIndex(o, key)
		
	Result:
	
		return int value for edge

	'''

	index = 1
	for e in iObj.Shape.Edges:
		
		c = "BoundBox ("
		c += str(int(round(e.BoundBox.XMin, 0))) + ", "
		c += str(int(round(e.BoundBox.YMin, 0))) + ", "
		c += str(int(round(e.BoundBox.ZMin, 0))) + ", "
		c += str(int(round(e.BoundBox.XMax, 0))) + ", "
		c += str(int(round(e.BoundBox.YMax, 0))) + ", "
		c += str(int(round(e.BoundBox.ZMax, 0)))
		c += ")"
		
		if c == str(iBoundBox):
			return index

		index = index + 1
	
	return -1


# ###################################################################################################################
def getFaceVertices(iFace):
	'''
	getFaceVertices(iFace) - get all vertices values for face.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iFace: face object
		
	Usage:
	
		[ v1, v2, v3, v4 ] = getFaceVertices(gFace)
		
	Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 2, 2, 2 ], [ 3, 3, 3 ], [ 4, 4, 4 ] ]
	'''
	
	vertexArr = touchTypo(iFace)

	v1 = [ vertexArr[0].X, vertexArr[0].Y, vertexArr[0].Z ]
	v2 = [ vertexArr[1].X, vertexArr[1].Y, vertexArr[1].Z ]
	v3 = [ vertexArr[2].X, vertexArr[2].Y, vertexArr[2].Z ]
	v4 = [ vertexArr[3].X, vertexArr[3].Y, vertexArr[3].Z ]
	
	return [ v1, v2, v3, v4 ]


# ###################################################################################################################
def getFaceEdges(iObj, iFace):
	'''
	getFaceEdges(iObj, iFace) - get all edges for given face grouped by sizes.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object where is the face
		iFace: face object

	Usage:
	
		[ faceType, arrAll, arrThick, arrShort, arrLong ] = getFaceEdges(gObj, gFace)
		
	Result:
	
		Return arrays like [ faceType, arrAll, arrThick, arrShort, arrLong ] with edges objects, 
		
		faceType - string "surface" or "edge"
		arrAll - array with all edges
		arrThick - array with the thickness edges
		arrShort - array with the short edges (if type is edge this will be the same as arrThick)
		arrLong - array with the long edges

	'''
	
	[ faceAxis, faceType ] = getDirectionFace(iObj, iFace)

	sizes = []
	sizes = getSizes(iObj)
	sizes.sort()
	
	t = int(sizes[0])
	s = int(sizes[1])
	l = int(sizes[2])
	
	e1 = iFace.Edges[0]
	e2 = iFace.Edges[1]
	e3 = iFace.Edges[2]
	e4 = iFace.Edges[3]

	arrAll = [ e1, e2, e3, e4 ]
	arrThick = []
	arrShort = []
	arrLong = []
	
	if int(e1.Length) == t:
		arrThick.append(e1)
	if int(e1.Length) == s:
		arrShort.append(e1)
	if int(e1.Length) == l:
		arrLong.append(e1)
	
	if int(e2.Length) == t:
		arrThick.append(e2)
	if int(e2.Length) == s:
		arrShort.append(e2)
	if int(e2.Length) == l:
		arrLong.append(e2)
		
	if int(e3.Length) == t:
		arrThick.append(e3)
	if int(e3.Length) == s:
		arrShort.append(e3)
	if int(e3.Length) == l:
		arrLong.append(e3)
	
	if int(e4.Length) == t:
		arrThick.append(e4)
	if int(e4.Length) == s:
		arrShort.append(e4)
	if int(e4.Length) == l:
		arrLong.append(e4)
	
	return [ faceType, arrAll, arrThick, arrShort, arrLong ]
	

# ###################################################################################################################
def getEdgeVertices(iEdge):
	'''
	getEdgeVertices(iEdge) - get all vertices values for edge.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iEdge: edge object
		
	Usage:
	
		[ v1, v2 ] = getEdgeVertices(gEdge)
		
	Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 1, 1, 1 ] ].
	'''
	
	vertexArr = touchTypo(iEdge)

	v1 = [ vertexArr[0].X, vertexArr[0].Y, vertexArr[0].Z ]
	v2 = [ vertexArr[1].X, vertexArr[1].Y, vertexArr[1].Z ]

	return [ v1, v2 ]


# ###################################################################################################################
def getVertex(iFace, iEdge, iVertex):
	'''
	getVertex(iFace, iEdge, iVertex) - get vertex values for face, edge and vertex index.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iFace: face object
		iEdge: edge array index
		iVertex: vertex array index (0 or 1)
	
	Usage:
	
		[ x, y, z ] = getVertex(gFace, 0, 1)
		
	Result:
	
		Return vertex position.
	'''
	
	vertexArr = touchTypo(iFace.Edges[iEdge])

	return [ vertexArr[iVertex].X, vertexArr[iVertex].Y, vertexArr[iVertex].Z ]


# ###################################################################################################################
def getReference():
	'''
	getReference() - get reference to the selected object.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		none
	
	Usage:
	
		gObj = getReference()
		
	Result:
	
		obj - reference to the base panel object

	'''

	obj = FreeCADGui.Selection.getSelection()[0]

	if ( 
		obj.isDerivedFrom("PartDesign::Thickness") or 
		obj.isDerivedFrom("PartDesign::Chamfer")
		):
		return obj.Base[0]
	else:
		return obj
	
	return -1


# ###################################################################################################################
def getPlacement(iObj):
	'''
	getPlacement(iObj) - get placement with rotation info for given object.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object to get placement

	Usage:
	
		[ x, y, z, r ] = getPlacement(gObj)
		
	Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

	'''

	if iObj.isDerivedFrom("PartDesign::Pad"):
		ref = iObj.Profile[0].AttachmentOffset
	else:
		ref = iObj.Placement
		
	x = ref.Base.x
	y = ref.Base.y
	z = ref.Base.z
	r = ref.Rotation

	return [ x, y, z, r ]


# ###################################################################################################################
def setPlacement(iObj, iX, iY, iZ, iR):
	'''
	setPlacement(iObj, iX, iY, iZ, iR) - set placement with rotation for given object.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object to set custom placement and rotation
		iX: X Axis object position
		iX: Y Axis object position
		iZ: Z Axis object position
		iR: Rotation object

	Usage:
	
		setPlacement(gObj, 100, 100, 200, r)
		
	Result:
	
		Object gObj should be moved into 100, 100, 200 position without rotation.

	'''

	if iObj.isDerivedFrom("PartDesign::Pad"):
		iObj.Profile[0].AttachmentOffset.Base = FreeCAD.Vector(iX, iY, iZ)
		iObj.Profile[0].AttachmentOffset.Rotation = iR
	else:
		iObj.Placement.Base = FreeCAD.Vector(iX, iY, iZ)
		iObj.Placement.Rotation = iR
	

# ###################################################################################################################
def getModelRotation(iX, iY, iZ):
	'''
	getModelRotation() - transform given iX, iY, iZ values to the correct vector, if the user rotated 3D model.

	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iX: X value to transform
		iY: Y value to transform
		iY: Z value to transform
	
	Usage:
	
		[x, y, z ] = getModelRotation(x, y, z)
		
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
def getSizes(iObj):
	'''
	getSizes(iObj) - allow to get sizes for object (iObj), according to the object type. The values are not sorted.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object to get sizes
	
	Usage:
	
		[ size1, size2, size3 ] = getSizes(obj)
		
	Result:
	
		Returns [ Length, Width, Height ] for Cube.
	'''

	if iObj.isDerivedFrom("Part::Box"):

		return [ iObj.Length.Value, iObj.Width.Value, iObj.Height.Value ]
			
	if iObj.isDerivedFrom("PartDesign::Pad"):

		for c in iObj.Profile[0].Constraints:
			if c.Name == "SizeX":
				sizeX = c.Value
			if c.Name == "SizeY":
				sizeY = c.Value
				
		return [ sizeX, sizeY, iObj.Length.Value ]

	try:
		
		return [ iObj.Base_Width.Value, iObj.Base_Height.Value, iObj.Base_Length.Value ]
		
	except:
		
		return [ 1, 1, 1 ]


# ###################################################################################################################
def getDirection(iObj):
	'''
	getDirection(iObj) - allow to get Cube object direction (iType).
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: selected object
	
	Usage:
	
		getDirection(obj)
		
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
def getDirectionFace(iObj, iFace):
	'''
	getDirectionFace(iObj, iFace) - allow to get Face direction.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: selected object
		iFace: selected face
	
	Usage:
	
		getDirectionFace(gObj, gFace)
		
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


# ###################################################################################################################
def convertPosition(iObj, iX, iY, iZ):
	'''
	convertPosition(iObj, iX, iY, iZ) - convert given position vector to correct position values according 
	to the object direction.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object
		iX: x position
		iY: y position
		iZ: z position
	
	Usage:
	
		convertPosition(obj, 0, 400, 0)
		
	Result:
	
		For Pad object in XZ direction return the AttachmentOffset order [ 0, 0, -400 ]
	'''
	
	if iObj.isDerivedFrom("PartDesign::Pad"):
		
		direction = getDirection(iObj)
		
		if direction == "XY" or direction == "YX":
			return [ iX, iY, iZ ]
		
		if direction == "XZ" or direction == "ZX":
			return [ iX, iZ, -iY ]

		if direction == "YZ" or direction == "ZY":
			return [ iY, iZ, iX ]
	
	else:
		
		return [ iX, iY, iZ ]


# ###################################################################################################################
def sizesToCubePanel(iObj, iType):
	'''
	sizesToCubePanel(iObj, iType) - converts selected object (iObj) sizes to Cube panel sizes into given direction (iType). 
	So, the returned values can be directly assigned to Cube object in order to create 
	panel in exact direction.

	Note: This is internal function, so there is no error pop-up or any error handling.

	Args:

		iObj: selected object
		iType direction: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

	Usage:

		[ Length, Width, Height ] = sizesToCubePanel(obj, "YZ")
		
	Result:

		Returns [ Length, Width, Height ] for YZ object placement".
	'''

	if iObj.isDerivedFrom("Part::Box"):

		sizes = [ iObj.Length.Value, iObj.Width.Value, iObj.Height.Value ]
		
	elif iObj.isDerivedFrom("PartDesign::Pad"):
		
		for c in iObj.Profile[0].Constraints:
			if c.Name == "SizeX":
				sizeX = c.Value
			if c.Name == "SizeY":
				sizeY = c.Value
		
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
def makePad(iSize1, iSize2, iSize3, iX, iY, iZ, iRotation, iType, iPadName="Pad"):
	'''
	makePad(iSize1, iSize2, iSize3, iX, iY, iZ, iType, iPadName="Pad") - allows to create 
	Part, Plane, Body, Pad, Sketch objects.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iSize1: SizeX
		iSize2: SizeY
		iSize3: Pad Length
		
		iX: Sketch AttachmentOffset X
		iY: Sketch AttachmentOffset Y
		iZ: Sketch AttachmentOffset Z
		iRotation: rotation object
		
		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"
		iPadName="Pad": Label for created Pad and other parts
	
	Usage:
	
		import MagicPanels
		
		r = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
		MagicPanels.makePad("600", "300", "18", 0, 0, 0, r, "XY", iPadName="Pad"):
		
	Result:
	
		Created Pad with correct placement, rotation and return [ part, body, sketch, pad ].
	'''

	import Part, PartDesign
	import Sketcher
	import PartDesignGui

	doc = FreeCAD.ActiveDocument
	part = doc.addObject('App::Part', 'Part')
	part.Label = "Part, "+iPadName
	body = doc.addObject('PartDesign::Body', 'Body')
	body.Label = "Body, "+iPadName
	part.addObject(body)
	sketch = body.newObject('Sketcher::SketchObject', 'Sketch')
	sketch.Label = "Pattern, "+iPadName
	
	if iType == "XY" or iType == "YX":
		sketch.Support = (body.Origin.OriginFeatures[3])
	if iType == "XZ" or iType == "ZX":
		sketch.Support = (body.Origin.OriginFeatures[4])
	if iType == "YZ" or iType == "ZY":
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
	sketch.setDatum(9,FreeCAD.Units.Quantity(iSize1))
	sketch.renameConstraint(9, u'SizeX')
	sketch.addConstraint(Sketcher.Constraint('DistanceY',3,1,3,2,159.435455))
	sketch.setDatum(10,FreeCAD.Units.Quantity(iSize2))
	sketch.renameConstraint(10, u'SizeY')

	position = FreeCAD.Vector(iX, iY, iZ)
	sketch.AttachmentOffset = FreeCAD.Placement(position, iRotation)

	pad = body.newObject('PartDesign::Pad', iPadName)
	pad.Profile = sketch
	pad.Length = FreeCAD.Units.Quantity(iSize3)
	sketch.Visibility = False

	doc.recompute()

	return [ part, body, sketch, pad ]


# ###################################################################################################################
def showInfo(iCaller, iInfo, iNote="none"):
	'''
	showInfo(iCaller, iInfo) - allow to show Gui info box for all available function and multiple calls.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iCaller: window title
		iInfo: HTML text to show
	
	Usage:
	
		showInfo("panel"+iType, info)
		
	Result:
	
		Show info Gui.
	'''

	info = iInfo

	if iNote == "replace":
		info += '<br><br>'
		info += 'The replace features are considered for final stage of furniture designing. '
		info += 'Some kind of detailed preview stage. '
		info += 'Do not use the replace feature at the beginning because the Magic Panels may stop working '
		info += 'and the furniture designing process will be much longer and more complicated. '
	

	info += '<br><br><br><br>'
	info += 'To keep furniture designing process quick and simple, '
	info += 'the furniture designing process should follow steps: '
	info += '<ol>'
	info += '<li>Create simple model with simple Cube panels.</li>'
	info += '<li>Add mounting points.</li>'
	info += '<li>Replace desired elements with more detailed elements.</li>'
	info += '<li>Add decoration if needed.</li>'
	info += '<li>Add colors or textures and preview furniture.</li>'
	info += '<li>Generate cut-list.</li>'
	info += '<li>Create furniture in real-life.</li>'
	info += '<li>Have fun with your new furniture in real-life !</li>'
	info += '</ol>'
		
	info += 'For more details please see:' + ' '
	info += '<a href="https://github.com/dprojects/Woodworking">Woodworking workbench documentation.</a>'
	
	msg = QtGui.QMessageBox()
	msg.setWindowTitle(iCaller)
	msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
	msg.setText(info)
	msg.exec_()


# ###################################################################################################################
# Functions - for external usage, should be error handling and pop-up.
# ###################################################################################################################


# ###################################################################################################################
def panelDefault(iType):
	'''
	panelDefault(iType) - allows to create default panel 600 x 300 x 18 into exact direction (iType).

	Note: This function displays pop-up info in case of error.

	Args:

		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

	Usage:

		import MagicPanels
		
		MagicPanels.panelDefault("XY")
		
	Result:

		Created panel 600 x 300 x 18 with correct direction XY.
	'''

	try:

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panel"+iType)

		if iType == "XY":
			panel.Length = 600
			panel.Width = 300
			panel.Height = 18

		if iType == "YX":
			panel.Length = 300
			panel.Width = 600
			panel.Height = 18

		if iType == "XZ":
			panel.Length = 600
			panel.Width = 18
			panel.Height = 300

		if iType == "ZX":
			panel.Length = 300
			panel.Width = 18
			panel.Height = 600

		if iType == "YZ":
			panel.Length = 18
			panel.Width = 600
			panel.Height = 300

		if iType == "ZY":
			panel.Length = 18
			panel.Width = 300
			panel.Height = 600

		FreeCAD.activeDocument().recompute()
	
	except:
	
		info = ""
		
		info += '<b>Please create active document to create default panel 600 mm x 300 mm and thickness of 18 mm.</b>' + ' '
		info += '<br>'
		
		showInfo("panelDefault"+iType, info)


# ###################################################################################################################
def panelCopy(iType):
	'''
	panelCopy(iType) - allows to copy selected panel into exact direction (iType).

	Note: This function displays pop-up info in case of error.

	Args:

		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

	Usage:

		import MagicPanels
		
		MagicPanels.panelCopy("XY")
		
	Result:

		Created panel with correct direction XY.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panel"+iType)
		[ panel.Length, panel.Width, panel.Height ] = sizesToCubePanel(gObj, iType)

		FreeCAD.activeDocument().recompute()

	except:

		info = ""
		
		info += '<b>If you have active document, please select correct panel you want to copy to exact direction.</b>' + ' '
		info += '<br><br>'
		
		info += '<ul>'
		info += '<li>By default you can copy any panel based on FreeCAD Cube object. </li>'
		info += '<li>If you want to copy Pad, you need to have Constraints named "SizeX" and "SizeY" at the Sketch. </li>' 
		info += '<li>For other object types you need to have Length, Width, Height properties at object. '
		info += 'Group: "Base", Type: "App::PropertyLength". </li>'
		info += '</ul>'
	
		showInfo("panelCopy"+iType, info)


# ###################################################################################################################
def panelMove(iType):
	'''
	panelMove(iType) - allows to move panel in given direction.

	Note: This function displays pop-up info in case of error.

	Args:
	
		iType: "Xp", "Xm", "Yp", "Ym", "Zp", "Zm"
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelMove("Xp")
		
	Result:
	
		Panel will be moved into X+ direction for 0 key view position. 
		If user rotated 3D model this should adjust to the model position.
		
	'''

	try:

		gObj = getReference()

		sizes = []
		sizes = getSizes(gObj)
		sizes.sort()

		x = 0
		y = 0
		z = 0
		
		if iType == "Xp":
			x = sizes[0]
		
		if iType == "Xm":
			x = - sizes[0]

		if iType == "Yp":
			y = sizes[0]

		if iType == "Ym":
			y = - sizes[0]

		if iType == "Zp":
			z = sizes[0]

		if iType == "Zm":
			z = - sizes[0]

		[ x, y, z ] = convertPosition(gObj, x, y, z)
		[ x, y, z ] = getModelRotation(x, y, z)

		[ px, py, pz, r ] = getPlacement(gObj)
		setPlacement(gObj, px+x, py+y, pz+z, r)

		FreeCAD.activeDocument().recompute()
	
	except:
		
		info = ""
		
		info += '<b>If you have active document, please select correct panel to move.</b>' + ' '
		info += '<br><br>'
		
		info += '<b>Note:</b>' + ' '
		info += 'Panel is moved into direction described by the icon. However, in some cases the panel may move '
		info += 'into opposite direction, if the panel type is not supported.'
		
		showInfo("panelMove"+iType, info)


# ###################################################################################################################
def panelResize(iType):
	'''
	panelResize(iType) - allows to resize panel in given direction.
	
	Note: This function displays pop-up info in case of error.
	
	Args:
	
		iType 1: make bigger long side of panel
		iType 2: make smaller long side of panel
		iType 3: make bigger short side of panel
		iType 4: make smaller short side of panel
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelResize("1")
		
	Result:
	
		Make bigger long side of panel.
	'''

	try:

		gObj = getReference()

		sizes = []
		sizes = getSizes(gObj)
		sizes.sort()
		thick = sizes[0]

		if gObj.isDerivedFrom("Part::Box"):

			if iType == "1":
				if gObj.Length.Value == sizes[2]:
					gObj.Length = gObj.Length.Value + thick
					return
					
				if gObj.Width.Value == sizes[2]:
					gObj.Width = gObj.Width.Value + thick
					return
					
				if gObj.Height.Value == sizes[2]:
					gObj.Height = gObj.Height.Value + thick
					return

			if iType == "2":
				if gObj.Length.Value == sizes[2]:
					if gObj.Length.Value - thick > 0:
						gObj.Length = gObj.Length.Value - thick
					return
					
				if gObj.Width.Value == sizes[2]:
					if gObj.Width.Value - thick > 0:
						gObj.Width = gObj.Width.Value - thick
					return
					
				if gObj.Height.Value == sizes[2]:
					if gObj.Height.Value - thick > 0:
						gObj.Height = gObj.Height.Value - thick
					return

			if iType == "3":
				if gObj.Length.Value == sizes[1]:
					gObj.Length = gObj.Length.Value + thick
					return
					
				if gObj.Width.Value == sizes[1]:
					gObj.Width = gObj.Width.Value + thick
					return
					
				if gObj.Height.Value == sizes[1]:
					gObj.Height = gObj.Height.Value + thick
					return

			if iType == "4":
				if gObj.Length.Value == sizes[1]:
					if gObj.Length.Value - thick > 0:
						gObj.Length = gObj.Length.Value - thick
					return
					
				if gObj.Width.Value == sizes[1]:
					if gObj.Width.Value - thick > 0:
						gObj.Width = gObj.Width.Value - thick
					return
					
				if gObj.Height.Value == sizes[1]:
					if gObj.Height.Value - thick > 0:
						gObj.Height = gObj.Height.Value - thick
					return

		else:
		
			direction = getDirection(gObj)
		
			if iType == "1":
				
				if direction == "XY" or direction == "XZ" or direction == "YZ":
					gObj.Profile[0].setDatum(9, FreeCAD.Units.Quantity(sizes[2] + thick))
				else:
					gObj.Profile[0].setDatum(10, FreeCAD.Units.Quantity(sizes[2] + thick))
		
			if sizes[2] - thick > 0:

				if iType == "2":
				
					if direction == "XY" or direction == "XZ" or direction == "YZ":
						gObj.Profile[0].setDatum(9, FreeCAD.Units.Quantity(sizes[2] - thick))
					else:
						gObj.Profile[0].setDatum(10, FreeCAD.Units.Quantity(sizes[2] - thick))

			if iType == "3":
				
				if direction == "XY" or direction == "XZ" or direction == "YZ":
					gObj.Profile[0].setDatum(10, FreeCAD.Units.Quantity(sizes[1] + thick))
				else:
					gObj.Profile[0].setDatum(9, FreeCAD.Units.Quantity(sizes[1] + thick))

			if sizes[1] - thick > 0:
				
				if iType == "4":
				
					if direction == "XY" or direction == "XZ" or direction == "YZ":
						gObj.Profile[0].setDatum(10, FreeCAD.Units.Quantity(sizes[1] - thick))
					else:
						gObj.Profile[0].setDatum(9, FreeCAD.Units.Quantity(sizes[1] - thick))

		FreeCAD.activeDocument().recompute()

	except:
		
		info = ""
		
		info += '<b>If you have active document, please select correct panel to resize.</b>' + ' '
		info += '<br><br>'
		
		info += '<b>Note:</b>' + ' '
		info += 'Panel is resized into direction described by the icon for XY panel. However, in some cases the '
		info += 'panel may be resized into opposite direction, if the panel is not supported or the sides are equal.'
	
		showInfo("panelResize"+iType, info)


# ###################################################################################################################
def panelFace(iType):
	'''
	panelFace(iType) - allows to create simple panel based on selected face and object.

	Note: This function displays pop-up info in case of error.
	
	Args:
	
		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelFace("XY")
		
	Result:
	
		Created panel at selected face with correct placement.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]
		gFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelFace"+iType)
		[ panel.Length, panel.Width, panel.Height ] = sizesToCubePanel(gObj, iType)

		if gObj.isDerivedFrom("Part::Box"):
			[ x, y, z ] = getVertex(gFace, 0, 1)
		else:
			[ x, y, z ] = getVertex(gFace, 1, 0)

		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
		FreeCAD.activeDocument().recompute()
		
	except:
		
		info = ""
		
		info += '<b>If you have active document, please select face at panel to create new panel at this selected face.</b>' + ' '
		info += '<br><br>'
		
		info += '<b>Note:</b>' + ' '
		info += 'Usually for the opposite direction to the coordinate axes there is thickness offset for the panel. '
		info += 'However, to move the panel quickly to the correct place, you can: '
		info += '<ul>'
		info += '<li>use dedicated Magic Panels to move panels,</li>'
		info += '<li>use dedicated Magic Panels for left furniture side creation.</li>'
		info += '</ul>'
		
		showInfo("panelFace"+iType, info)


# ###################################################################################################################
def panelBetween(iType):
	'''
	panelBetween(iType) - allows to create simple panel between 2 selected faces.
	
	Note: This function displays pop-up info in case of error.
	
	Args:
	
		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelBetween("XY")
		
	Result:
	
		Created panel between 2 selected faces with correct placement.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]
		gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
	
		[ x1, y1, z1 ] = getVertex(gFace1, 0, 1)
		[ x2, y2, z2 ] = getVertex(gFace2, 0, 1)

		x = abs(x2 - x1)
		y = abs(y2 - y1)
		z = abs(z2 - z1)

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelBetween"+iType)
		[ panel.Length, panel.Width, panel.Height ] = sizesToCubePanel(gObj, iType)

		z1 = z1 + gObj.Height.Value - panel.Height.Value
		
		if x > 0:
			panel.Length = x
		
		if y > 0:
			panel.Width = y
			
		if z > 0:
			panel.Height = z

		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z1), FreeCAD.Rotation(0, 0, 0))
		FreeCAD.activeDocument().recompute()

	except:
		
		info = ""
		
		info += '<b>If you have active document, please select 2 faces at 2 different panels to create new panel between these '
		info += '2 selected faces.</b>' + ' '
		info += '<br><br>'
		
		info += '<b>Note:</b>' + ' '
		info += 'To use the feature you have to keep exact face selection order. If you change selection order the '
		info += 'result will be different. You can also experiment with outside faces, move and resize panels. To select '
		info += 'more than 1 face you have to hold CTRL key.'

		showInfo("panelBetween"+iType, info)


# ###################################################################################################################
def panelSide(iType):
	'''
	panelSide(iType) - allows to create back of the furniture with 3 selected faces.
	
	Note: This function displays pop-up info in case of error.
	
	Args:
	
		"1": Left side of the furniture
		"2": Left side of the furniture but raised up
		"3": Right side of the furniture
		"4": Right side of the furniture but raised up
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelSide("1")
		
	Result:
	
		Created side of the furniture.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]
		gFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

		[ Length, Width, Height ] = sizesToCubePanel(gObj, "ZY")

		if gObj.isDerivedFrom("Part::Box"):
			[ x, y, z ] = getVertex(gFace, 0, 1)

		else:

			if iType == "1" or iType == "2":
				[ x, y, z ] = getVertex(gFace, 0, 0)

			if iType == "3" or iType == "4":
				[ x, y, z ] = getVertex(gFace, 1, 0)

		if iType == "1":
			x = x - Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideLeft")
		
		if iType == "2":
			z = z + Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideLeftUP")
		
		if iType == "3":
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideRight")
		
		if iType == "4":
			x = x - Length
			z = z + Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideRightUP")

		panel.Length = Length
		panel.Width = Width
		panel.Height = Height
		
		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
		FreeCAD.activeDocument().recompute()

	except:
		
		info = ""
		
		info += '<b>If you have active document, please select 1 face to create side of the furniture.</b>'
		info += '<br><br>'
		
		info += '<b>Note:</b>' + ' '
		info += 'The face should be selected at edge of the side you want to create new panel. '
		info += 'This feature is mostly designed to this specific situation. In other cases the result may be '
		info += 'different than expected. '

		showInfo("panelSide"+iType, info)


# ###################################################################################################################
def panelBackOut():
	'''
	panelCover(iType) - allows to create back of the furniture with 3 selected faces.
	
	Note: This function displays pop-up info in case of error.
	
	Args:
	
		no args
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelBackOut()
		
	Result:
	
		Created back of the furniture.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]

		gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
		gFace3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]

		[ x, y, z ] = sizesToCubePanel(gObj, "ZX")

		[ x1, y1, z1 ] = getVertex(gFace1, 0, 1)
		[ x2, y2, z2 ] = getVertex(gFace2, 0, 0)
		[ x3, y3, z3 ] = getVertex(gFace3, 0, 1)

		x = abs(x2 - x1)
		z = z - z3

		if x > 0 and y > 0 and z > 0:

			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelBackOut")
			panel.Length = x
			panel.Width = y
			panel.Height = z

			panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z3), FreeCAD.Rotation(0, 0, 0))
			FreeCAD.activeDocument().recompute()
			
		else:
		
			raise
			
	except:
			
		info = ""
		
		info += '<b>If you have active document, please select 3 faces at 3 different panels to create back of the furniture.</b>'
		info += '<br><br>'
		
		info += '<b>Note:</b>' + ' '
		info += 'The 3rd selected face panel should be the bottom shelf of the furniture to resize the back panel to this place. '
		info += 'This feature is mostly designed to this specific situation. In other cases the result may be different than '
		info += 'expected. To use the feature you have to keep exact face selection order. If you change selection order the '
		info += 'result will be different. To select more than 1 face you have to hold CTRL key.'

		showInfo("panelBackOut", info)


# ###################################################################################################################
def panelCover(iType):
	'''
	panelCover(iType) - allows to create simple panel on top of 3 selected faces.
	
	Note: This function displays pop-up info in case of error.
	
	Args:
	
		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelCover("XY")
		
	Result:
	
		Created panel on top of 3 selected faces with correct placement.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]
		
		gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
		gFace3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]

		[ x, y, z ] = sizesToCubePanel(gObj, iType)

		[ x1, y1, z1 ] = getVertex(gFace1, 0, 1)
		[ x2, y2, z2 ] = getVertex(gFace2, 2, 1)
		[ x3, y3, z3 ] = getVertex(gFace3, 0, 1)

		x = abs(x2 - x1)
		y = y + z

		if x > 0 and y > 0 and z > 0:
		
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelCover"+iType)
			panel.Length = x
			panel.Width = y
			panel.Height = z

			panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z3), FreeCAD.Rotation(0, 0, 0))
			FreeCAD.activeDocument().recompute()

	except:
		
		info = ""
		
		info += '<b>If you have active document, please select 3 faces at 3 different panels to create new panel on top of these '
		info += '3 selected faces.</b>' + ' '
		info += '<br><br>'
		
		info += '<b>Note:</b>' + ' '
		info += 'The 3rd selected object should be the back of the furniture to resize the new cover panel with the thickness. '
		info += 'This feature is mostly designed to this specific situation. In other cases the result may be different than '
		info += 'expected. To use the feature you have to keep exact face selection order. If you change selection order the '
		info += 'result will be different. To select more than 1 face you have to hold CTRL key.'

		showInfo("panelCover"+iType, info)


# ###################################################################################################################
def panelReplacePad(iLabel="rpanelPad"):
	'''
	panelReplacePad() - allows to replace Cube panel with the same panel but Pad.

	Note: This function displays pop-up info in case of error.
	
	Args:

		iLabel (optional): name all parts with given string

	Usage:

		import MagicPanels
		
		MagicPanels.panelReplacePad()
		
	Result:

		Selected Cube panel will be replaced with Pad and return [ part, body, sketch, pad ] references 
		that can be used for further transformations.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]

		sizes = getSizes(gObj)
		sizes.sort()
		
		direction = getDirection(gObj)
		
		if direction == "XY" or direction == "XZ" or direction == "YZ":
			s = [ sizes[2], sizes[1], sizes[0] ]
		
		if direction == "YX" or direction == "ZX" or direction == "ZY":
			s = [ sizes[1], sizes[2], sizes[0] ]

		[ X, Y, Z, r ] = getPlacement(gObj)
		
		if direction == "XY" or direction == "YX":
			[ x, y, z ] = [ X, Y, Z ]
		
		if direction == "XZ" or direction == "ZX":
			[ x, y, z ] = [ X, Z, -(Y+sizes[0]) ]

		if direction == "YZ" or direction == "ZY":
			[ x, y, z ] = [ Y, Z, X ]
			
		[ part, body, sketch, pad ] = makePad(s[0], s[1], s[2], x, y, z, r, direction, iLabel)
		
		FreeCAD.ActiveDocument.removeObject(gObj.Name)
		FreeCAD.activeDocument().recompute()
		
		return [ part, body, sketch, pad ]

	except:
		
		info = ""
		
		info += '<b>If you have active document, please select Cube panel you want to replace with the same Pad panel. </b>'
		info += 'You can select only one Cube panel at once. This replace panel is mostly for manual changes and decorations. '
		info += '<br><br>'
	
		showInfo("rpanelPad", info, "replace")
	

# ###################################################################################################################
def panel2profile():
	'''
	panel2profile() - allows to replace Cube panels with construction profiles made from Thickness.

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		
		profiles = MagicPanels.panel2profile()
		
	Result:

		Selected Cube panels will be changed into Thickness construction profiles. This function 
		returns array with references to the created profiles, so it can be used for further 
		transfomrations.
	'''

	try:

		profiles = []
		objects = FreeCADGui.Selection.getSelection()
		if len(objects) == 0:
			raise
			
		for gObj in objects:
		
			sizes = getSizes(gObj)
			sizes.sort()
			if sizes[0] != sizes[1]:
				raise
			
			[ part, body, sketch, pad ] = panelReplacePad("Construction")
			profile = body.newObject('PartDesign::Thickness','Profile')
			
			faces = []
			i = 0
			for f in pad.Shape.Faces:
				if int(round(pad.Shape.Faces[i].Length)) == int(round(4 * sizes[0])):
					faces.append("Face"+str(i+1))

				i = i + 1
				
			profile.Base = (pad, faces)
			profile.Value = 1
			profile.Reversed = 1
			profile.Mode = 0
			profile.Intersection = 0
			profile.Join = 0

			pad.Visibility = False

			FreeCAD.activeDocument().recompute()
			
			colors = [ (0.0, 0.0, 0.0, 0.0),
				(0.0, 0.0, 0.0, 0.0),
				(0.0, 0.0, 0.0, 0.0),
				(0.0, 0.0, 0.0, 0.0),
				(0.0, 0.0, 0.0, 0.0),
				(0.0, 1.0, 0.0, 0.0),
				(0.0, 0.0, 0.0, 0.0),
				(0.0, 1.0, 0.0, 0.0),
				(0.0, 1.0, 0.0, 0.0),
				(0.0, 1.0, 0.0, 0.0) ]

			profile.ViewObject.DiffuseColor = colors

			FreeCAD.activeDocument().recompute()
			profiles.append(profile)
		
		return profiles
	
	except:
		
		info = ""
		
		info += '<b>If you have active document, please select panels (Cubes) with 2 equal sizes e.g. '
		info += '20 mm x 20 mm x 300 mm to replace it with construction profiles.</b>' + '<br><br>'
		
		showInfo("panel2profile", info, "replace")


# ###################################################################################################################
def panel2frame():
	'''
	panel2frame() - allows to replace Cube panels with frame elements cut with 45 angle. You have to select 
	face at Cube panels to make frame.

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		
		frames = MagicPanels.panel2frame()
		
	Result:

		Selected Cube panels faces will be changed into frame. This function 
		returns array with references to the created frames, so it can be used for further 
		transfomrations.
	'''

	try:

		frames = []
		frame = ""
		objects = FreeCADGui.Selection.getSelection()
		
		if len(objects) == 0:
			raise
		
		faces = dict()
		
		i = 0
		for o in objects:
			faces[o] = FreeCADGui.Selection.getSelectionEx()[i].SubObjects
			i = i + 1

		for o in objects:
			
			face = faces[o][0]
		
			sizes = getSizes(o)
			sizes.sort()
			
			[ faceType, arrAll, arrThick, arrShort, arrLong ] = getFaceEdges(o, face)
			
			keys = []
			
			if faceType == "edge":
				arr = arrThick
				size = sizes[1]
			if faceType == "surface":
				arr = arrShort
				size = sizes[0]
				
			for e in arr:
				keys.append(str(e.BoundBox))
			
			[ part, body, sketch, pad ] = panelReplacePad("Frame")

			edges = []
			for k in keys:
				index = getEdgeIndexByKey(pad, k)
				edges.append("Edge"+str(int(index)))
			
			frame = body.newObject('PartDesign::Chamfer','Frame45Cut')
			frame.Base = (pad, edges)
			frame.Size = size - 0.01
			pad.Visibility = False
			
			FreeCAD.activeDocument().recompute()
			
			color = (0.5098039507865906, 0.3137255012989044, 0.1568627506494522, 0.0)

			frame.ViewObject.ShapeColor = color
			frame.ViewObject.DiffuseColor = color
			FreeCAD.activeDocument().recompute()
			
			frames.append(frame)
		
		return frames
	
	except:
		
		info = ""
		
		info += '<b>If you have active document, please select face of panel (Cube) to change it into '
		info += 'picture frame element. You can select more than one face to change all '
		info += 'elements at once with single click. </b>' + '<br><br>'
		info += 'If the selected face is edge, the 45 cut depth will be according to the short edge of the object. '
		info += 'If the selected face is surface, the 45 cut depth will be according to the thickness of the object. '
				
		showInfo("panel2frame", info, "replace")
	

# ###################################################################################################################
