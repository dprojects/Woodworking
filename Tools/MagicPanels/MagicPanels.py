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


gRoundPrecision = 2      # should be set according to the user FreeCAD GUI settings
gSearchDepth = 200       # recursive search depth

# end globals (for API generator)


# ###################################################################################################################
'''
# Functions for general purpose
'''
# ###################################################################################################################


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
# Vertices
'''
# ###################################################################################################################


# ###################################################################################################################
def showVertex(iVertices, iRadius=5):
	'''
	Description:
	
		Create sphere at given vertices, to show where are the points for debug purposes.
	
	Args:
	
		iVertices: array with Vertex or floats objects
		iRadius (optional): ball Radius

	Usage:
	
		MagicPanels.showVertex([ obj.Shape.CenterOfMass ], 20)

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
		else:
			fv = FreeCAD.Vector(v[0], v[1], v[2])
		
		FreeCAD.Console.PrintMessage("\n")
		FreeCAD.Console.PrintMessage(fv)
		
		s1 = FreeCAD.ActiveDocument.addObject("Part::Sphere","showVertex")
		s1.Placement = FreeCAD.Placement(FreeCAD.Vector(fv), FreeCAD.Rotation(0, 0, 0))
		s1.ViewObject.ShapeColor = (1.0, 0.0, 0.0, 0.0)
		s1.Radius = iRadius
		
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
	Description:
	
		Sets padding offset from given vertex to inside the object.
		Do not use it at getPlacement for Pads. Use 0 vertex instead.
		
		Note: This need to be improved.
	
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
def getEdgePlane(iEdge):
	'''
	Description:
	
		Returns orientation for the edge, changed axis, as "X", "Y" or "Z".
	
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
# Router
'''
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
				
				p = getEdgePlane(e)
				
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
	
		plane = getEdgePlane(iSub)

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
			subPlane = getEdgePlane(arrLong[0])
		elif len(arrShort) > 0:
			subPlane = getEdgePlane(arrShort[0])
		elif len(arrAll) > 0:
			subPlane = getEdgePlane(arrAll[0])
		
		if subPlane == "X":
			r = FreeCAD.Rotation(FreeCAD.Vector(0.00, 1.00, 0.00), 90.00)

		if subPlane == "Y":
			r = FreeCAD.Rotation(FreeCAD.Vector(1.00, 0.00, 0.00), 90.00)

		if subPlane == "Z":
			r = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 00.00)
	
	# This can be updated later for rotated edges with additional rotation angle (offset from axis)
	return r


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
'''
# Sizes
'''
# ###################################################################################################################


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
	Description:
	
		Creates measurements object, I mean draw it. Now it use FreeCAD function 
		to create and draw object. But in the future this can be changed to 
		more beautiful drawing without changing tools. 
	
	Args:
	
		iP1: starting point vertex object
		iP2: ending point vertex object
		iRef (optional): string for future TechDraw import or any other use, other tools

	Usage:
	
		m = MagicPanels.showMeasure(gP1, gP2, "Pad")

	Result:
	
		Create measure object, draw it and return measure object for further processing. 

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
	
	if str(iObj1.Name) != str(iObj2.Name):
		
		[ o1X, o1Y, o1Z, o1R ] = getContainersOffset(iObj1)
		[ o2X, o2Y, o2Z, o2R ] = getContainersOffset(iObj2)

		x1 = x1 + o1X
		y1 = y1 + o1Y
		z1 = z1 + o1Z
		
		x2 = x2 + o2X
		y2 = y2 + o2Y
		z2 = z2 + o2Z
	
	else:
		
		[ o1X, o1Y, o1Z, o1R ] = getContainersOffset(iObj1)
		x1 = x1 + o1X
		y1 = y1 + o1Y
		z1 = z1 + o1Z

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
def getPlacement(iObj):
	'''
	Description:
	
		Gets placement with rotation info for given object.
		Note: This is useful if you not use containers. 
	
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
def getGlobalPlacement(iObj):
	'''
	Description:
	
		Calls FreeCAD getGlobalPlacement at base object, and return useful form of placement.
	
	Args:
	
		iObj: object to get placement

	Usage:
	
		[ x, y, z, r ] = MagicPanels.getGlobalPlacement(o)

	Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

	'''

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


# ###################################################################################################################
def setPlacement(iObj, iX, iY, iZ, iR, iAnchor=""):
	'''
	Description:
	
		Sets placement with rotation for given object.
	
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
def getSketchPlacement(iSketch, iType):
	'''
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
	Description:
	
		Set placement with rotation dedicated to move and copy Sketch directly.
	
	Args:

		iSketch: Sketch object to set custom placement and rotation
		iX: X Axis object position
		iX: Y Axis object position
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

	if iType == "auto":
		
		iType = "global"
		try:
			plane = iSketch.Support[0][0].Label
			if plane.startswith("XY") or plane.startswith("XZ") or plane.startswith("YZ"):
				iType = "attach"
		except:
			skip = 1

	if iType == "attach":

		plane = iSketch.Support[0][0].Label

		rX = iR.Axis.x
		rY = iR.Axis.y
		rZ = iR.Axis.z
		rAngle = iR.Angle

		# the Sketch AttachmentOffset position is rocket science for me ;-)
		# it has been invented by time travelers or what? ;-)

		if plane.startswith("XY"):
			x, y, z = iX, iY, iZ
			r = FreeCAD.Rotation(FreeCAD.Vector(rX, rY, rZ), rAngle)
			
		if plane.startswith("XZ"):
			x, y, z = iX, iZ, -iY
			r = FreeCAD.Rotation(FreeCAD.Vector(rX, rZ, -rY), rAngle)
			
		if plane.startswith("YZ"):
			x, y, z = iY, iZ, iX
			r = FreeCAD.Rotation(FreeCAD.Vector(rY, rZ, rX), rAngle)

		iSketch.AttachmentOffset.Base = FreeCAD.Vector(x, y, z)
		iSketch.AttachmentOffset.Rotation = r
		
	if iType == "global":
		
		iSketch.Placement.Base = FreeCAD.Vector(iX, iY, iZ)
		iSketch.Placement.Rotation = iR


# ###################################################################################################################
def getObjectCenter(iObj):
	'''
	Description:
	
		Returns center of the object.
	
		Note: This function will be updated later with more reliable 
		way of getting center of the object, also for LinkGroup and other containers. 
		Now it returns Shape.CenterOfMass for the object and it is not the same 
		as center of the object.
	
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
'''
# Containers
'''
# ###################################################################################################################


# ###################################################################################################################
def getContainersOffset(iObj):
	'''
	Description:
	
		If the object is in the container like Part, Body, LingGroup the vertices are 
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

	for o in iObj.InListRecursive:
		
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
def getVerticesPosition(iVertices, iObj, iType="array"):
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
			"array" - array with floats [ 1, 2, 3 ]
			"vector" - array with FreeCAD.Vector types
			"vertex" - array with Part.Vertex types

	Usage:
	
		vertices = MagicPanels.getVerticesPosition(vertices, o, "array")
		MagicPanels.showVertex(iVertices, 10)

	Result:
	
		return vertices array with correct container offset

	'''

	# not unpack mirroring
	if iObj.isDerivedFrom("Part::Mirroring"):
		return iVertices

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
	
	for o in iObj.InListRecursive:
		
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
def removeVerticesOffset(iVertices, iObj, iType="array"):
	'''
	Description:
	
		Remove iObj container offset for vertices iVertices.
	
	Args:
	
		iVertices: vertices array
		iObj: object to remove containers offset
		iType:
			"array" - array with floats [ 1, 2, 3 ]
			"vector" - array with FreeCAD.Vector types

	Usage:
	
		vertices = MagicPanels.removeVerticesOffset(vertices, o, "array")

	Result:
	
		return vertices array without container offset

	'''

	objRef = getReference(iObj)
	
	if objRef.isDerivedFrom("PartDesign::Pad"):
	
		[ x, y, z, r ] = getContainerPlacement(objRef, "clean")
		
		vertices = []
		for v in iVertices:
			
			if iType == "array":
				n = FreeCAD.Vector(v[0]-x, v[1]-y, v[2]-z)
			else:
				n = FreeCAD.Vector(v.x-x, v.y-y, v.z-z)
				
			vertices.append(n)
	
		return vertices
		
	else: 
		
		return iVertices

	return ""


# ###################################################################################################################
def moveToContainer(iObjects, iSelection):
	'''
	Description:
	
		Move objects iObjects to container for iSelection object. 
		Container need to be in the clean path, no other objects except Group or LinkGroup, 
		for example LinkGroup -> LinkGroup is clean path, only containers, but the 
		Mirror -> LinkGroup is not considered as clean container path here.
	
	Args:
	
		iObjects: list of objects to move to container, for example new created Cube
		iSelection: selected object, for example Pad

	Usage:
	
		MagicPanels.moveToContainer([ o ], pad)

	Result:
	
		No return, move object.

	'''

	rsize = len(iSelection.InListRecursive)
	
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
			c = iSelection.InListRecursive[index]
			
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
					# coR = coR + c.Placement.Rotation # not supported yet
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
			[x, y, z, r ] = getPlacement(o)
			
			x = x + coX
			y = y + coY
			z = z + coZ
			# r = r + coR # not supported yet
			
			setPlacement(o, x, y, z, r)
			
			# move object to saved container
			o.adjustRelativeLinks(toMove)
			toMove.ViewObject.dropObject(o, None, '', [])
			
		FreeCAD.ActiveDocument.recompute()


# ###################################################################################################################
def moveToFirst(iObjects, iSelection):
	'''
	Description:
	
		Move objects iObjects to first container above Body for iSelection object.
		This can be used to force object at face to be moved into Mirror -> LinkGroup.
	
	Args:
	
		iObjects: list of objects to move to container, for example new created Cube
		iSelection: selected object, for example Pad

	Usage:
	
		MagicPanels.moveToFirst([ o ], pad)

	Result:
	
		No return, move object.

	'''

	boX, boY, boZ = 0, 0, 0
	boR = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
	
	rsize = len(iSelection.InListRecursive)
	
	# if no container, do nothing
	if rsize == 0:
		return

	i = 0
	while i < rsize and i < gSearchDepth:
		
		c = iSelection.InListRecursive[i]
		
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
				
				# not disturb, not needed right now
				# coR = o.Placement.inverse().Rotation
				# r = r * coR * boR
				
				# set new placement
				setPlacement(o, x, y, z, r)

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
				
				# not disturb, not needed right now
				# boR = boR * c.Placement.Rotation
				
			except:
				skip = 1

		# skip other objects with placements, like Sketches, Plane
		else:
			skip = 1

		i = i + 1


# ###################################################################################################################
def moveToFirstWithInverse(iObjects, iSelection):
	'''
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

	rsize = len(iSelection.InListRecursive)
	
	# if no container, do nothing
	if rsize == 0:
		return
	
	# calculate offset to remove
	toRemove = ""
	i = 0
	while i < rsize and i < gSearchDepth:

		c = iSelection.InListRecursive[i]

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
		
		c = iSelection.InListRecursive[i]

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
def moveToParent(iObjects, iSelection):
	'''
	Description:
	
		This version move object to parent container without adding or remove offset. This is useful if you copy the 
		Sketch, because SKetch after copy is located outside Body, in Part. But if the Part is inside LinkGroup 
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

	# if Cube and Part are in the root, and Part was created before Cube
	# the InList will return Part as parent, do you believe it?
	if len(iSelection.InList) < 1 or len(iSelection.Parents) < 1:
		return

	parent = iSelection.InList[0]
	
	for o in iObjects:
		
		# skip already copied objects
		if len(o.InList) > 0:
			continue
		
		# move object to the same container
		FreeCADGui.Selection.addSelection(o)
		o.adjustRelativeLinks(parent)
		parent.ViewObject.dropObject(o, None, '', [])
		FreeCADGui.Selection.clearSelection()

	FreeCAD.ActiveDocument.recompute()


# ###################################################################################################################
def getObjectToMove(iObj):
	'''
	Description:
	
		This function returns object to move.
	
	Args:
	
		iObj: object to get placement, selected container or base reference object

	Usage:
	
		toMove = MagicPanels.getObjectToMove(o)

	Result:
	
		For example: 

		for Cube: always returns Cube
		for Pad: always returns Body
		for LinkGroup: returns LinkGroup
		for Cut: returns Cut
		for other PartDesign objects: try to return Body
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
def createContainer(iObjects, iLabel=""):
	'''
	Description:
	
		This function creates container for given iObjects. The label for new container will be get from 
		first element of iObjects (iObjects[0]).
	
	Args:
	
		iObjects: array of object to create container for them
		iLabel: container label

	Usage:
	
		container = MagicPanels.createContainer([c1, c2])

	Result:
	
		Created container and objects inside the container, return container object.

	'''

	base = iObjects[0]
	container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','container')
	container.setLink(iObjects)
	
	if iLabel == "":
		container.Label = "Container, " + str(base.Label)
	else:
		container.Label = iLabel
		
	try:
		MagicPanels.copyColors(base, container)
	except:
		skip = 1
		
	FreeCAD.ActiveDocument.recompute()
	
	return container


# ###################################################################################################################
def getContainerPlacement(iObj, iType="clean"):
	'''
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
def setContainerPlacement(iObj, iX, iY, iZ, iR, iAnchor="auto"):
	'''
	Description:
	
		Little more advanced set placement function, especially used with containers.
		Adding offset here not make sense, because object can be moved via container so all the vertices might 
		be equal. Vertices not have containers offsets. They are only impacted by AttachmentOffset. 
		So you need to add all needed offsets and call this function with offsets.
	
	Args:

		iObj: object or container to set placement, for example Body, LinkGroup, Cut, Pad, Cube, Sketch, Cylinder
		iX: X Axis object position
		iX: Y Axis object position
		iZ: Z Axis object position
		iR: 
			0 - means auto rotation value set to iObj.Placement.Rotation
			R - custom FreeCAD.Placement.Rotation object
		iAnchor (optional):
			"clean" - set directly to iObj.Placement, if object is Pad set to Sketch directly
			"auto" - default object anchor with auto adjust to match iX, iY, iZ
			"center" - center of the object with auto adjust to match iX, iY, iZ
			[ iAX, iAY, iAZ ] - custom vertex with auto adjust to match iX, iY, iZ
		
	Usage:
		
		MagicPanels.setContainerPlacement(cube, 100, 100, 200, 0, "clean")
		MagicPanels.setContainerPlacement(pad, 100, 100, 200, 0, "auto")
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
		
		if iObj.isDerivedFrom("PartDesign::Pad"):
			setSketchPlacement(iObj.Profile[0], X, Y, Z, R, "global")
		else:
			iObj.Placement.Base = FreeCAD.Vector(X, Y, Z)
			iObj.Placement.Rotation = R

		return
	
	# ###############################################################################
	# custom set
	# ###############################################################################
	
	# set starting point
	[ oX, oY, oZ, oR ] = getContainerPlacement(iObj, "clean")
	
	# save object placement for later use
	X, Y, Z, R = oX, oY, oZ, oR
	
	# custom anchor = object anchor
	if iAnchor == "auto":
		aX, aY, aZ, aR = oX, oY, oZ, oR

	elif iAnchor == "center":
		[ aX, aY, aZ ] = getObjectCenter(iObj)
	
	else:
		aX, aY, aZ = iAnchor[0], iAnchor[1], iAnchor[2]

	# calculate diff between object anchor and custom anchor
	if iAnchor != "auto":
		[ moveX, moveY, moveZ ] = getPlacementDiff([oX, oY, oZ], [ aX, aY, aZ])
		X = X - moveX
		Y = Y - moveY
		Z = Z - moveZ
	
	# calculate diff between object anchor and new given position iX, iY, iZ
	[ moveX, moveY, moveZ ] = getPlacementDiff([oX, oY, oZ], [ iX, iY, iZ])
	X = X + moveX
	Y = Y + moveY
	Z = Z + moveZ
	
	# set placement
	iObj.Placement.Base = FreeCAD.Vector(X, Y, Z)
	iObj.Placement.Rotation = R


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
# Holes
'''
# ###################################################################################################################


# ###################################################################################################################
def makeHoles(iObj, iFace, iCylinders):
	'''
	Description:
	
		Making holes.

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
		setContainerPlacement(o, xs1, ys1, zs1, rs1, "clean")
		
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
	sketch.Support = ""
	
	[ x, y, z, r ] = getPlacement(sketch)
	[ coX, coY, coZ, coR ] = getContainersOffset(pad)
	x = x - coX
	y = y - coY
	z = z - coZ
	setPlacement(sketch, x, y, z, r)

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
	sketch.Support = ""
	
	[ x, y, z, r ] = getPlacement(sketch)
	[ coX, coY, coZ, coR ] = getContainersOffset(pad)
	x = x - coX
	y = y - coY
	z = z - coZ
	setPlacement(sketch, x, y, z, r)

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
	Description:
	
		Allows to copy colors from iSource object to iTarget object.

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
	
	# handling links
	if (
		iSource.isDerivedFrom("App::LinkGroup") or 
		iTarget.isDerivedFrom("App::LinkGroup") or
		iSource.isDerivedFrom("App::Link") or 
		iTarget.isDerivedFrom("App::Link") 
		):
	
		# normal -> link
		try:
			iTarget.ViewObject.ShapeMaterial.DiffuseColor = iSource.ViewObject.ShapeColor
		except:
			skip = 1
		
		try:
			iTarget.ViewObject.ShapeMaterial.DiffuseColor = iSource.ViewObject.DiffuseColor
		except:
			skip = 1

		# link -> normal
		try:
			iTarget.ViewObject.ShapeColor = iSource.ViewObject.ShapeMaterial.DiffuseColor
		except:
			skip = 1
		
		try:
			iTarget.ViewObject.DiffuseColor = iSource.ViewObject.ShapeMaterial.DiffuseColor
		except:
			skip = 1
		
		# link -> link
		try:
			iTarget.ViewObject.ShapeMaterial.DiffuseColor = iSource.ViewObject.ShapeMaterial.DiffuseColor
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


	info += "<br><br>"
	info += "<b>Golden rules:</b>"
	info += "<ul>"
	
	info += "<li>Don't rotate objects directly, rotate them via container LinkGroup.</li>"
	info += "<li>Don't copy Pad directly. Copy, Clone, Link the Part container.</li>"
	info += "<li>Don't mix Cut with PartDesign too much. Keep clear and simple design line.</li>"
	info += "<li>If you want generate cut-list, BOM, dimensions, rather avoid packing objects extremely, for example Array on Array or MultiTransform on MultiTransform.</li>"
	info += "<li>Rather not move objects via AttachmentOffset, move them via container Body, LinkGroup.</li>"
	info += "<li>Design furniture from Cubes. If you want more detailed model convert exact element to Pad and edit the Sketch. Also for irregular or not rectangle shapes.</li>"
	info += "<li>Always make backup of your project.</li>"
	info += "<ul>"
	
	if iNote == "yes":
		
		info += '<br><br>'
		info += translate('showInfoAll', 'For more details see:') + '<br>'
		info += '<a href="https://github.com/dprojects/Woodworking/tree/master/Docs">'
		info += translate('showInfoAll', 'Woodworking workbench documentation')
		info += '</a>'
		
	msg = QtGui.QMessageBox()
	msg.setWindowTitle(iCaller)
	msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
	msg.setText(info)
	msg.exec_()


# ###################################################################################################################
