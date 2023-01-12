
# MagicPanels

	This is MagicPanels library for Woodworking workbench.
	Darek L (github.com/dprojects)

Usage:

	import MagicPanels
	returned_value = MagicPanels.function(args)

Functions at this library:

* Should not have error handling and pop-ups, so you can call it from GUI tools in loops.
* Should return value, if further processing needed.

# Globals


gRoundPrecision = 2      # should be set according to the user FreeCAD GUI settings
gSearchDepth = 200       # recursive search depth

# Functions for general purpose
### equal(iA, iB):

	Description:
	
		At FreeCAD there are many values like 1.000006, especially for PartDesign objects. 
		So if you want to compare such values this sometimes might be True and sometimes False. 
		So, finally I decided to write my own function for comparison.
	
##### Description:
	
		iA: float value
		iB: float value

##### Usage:
	
		if MagicPanels.equal(1.0006, 1):
			do something ...

##### Result:
	
		return True if equal or False if not

### touchTypo(iObj):

	Description:
	
		Touch the typo so that the typo-snake does not notice it ;-) LOL
	
##### Description:
	
		iObj: object to touch

##### Usage:
	
		vs = MagicPanels.touchTypo(o)

##### Result:
	
		return Vertex + es for object o

### normalizeBoundBox(iBoundBox):

	Description:
	
		Return normalized version of BoundBox. All values 0.01 will be rounded 
		allowing comparison, and searches for the same face or edge.
	
##### Description:
	
		iBoundBox: directly pass BoundBox object

##### Usage:
	
		e1 = obj1.Shape.Edges[0]
		e2 = obj2.Shape.Edges[0]

		b1 = MagicPanels.normalizeBoundBox(e1.BoundBox)
		b2 = MagicPanels.normalizeBoundBox(e2.BoundBox)

##### Result:
	
		return normalized version for comparison if b1 == b2: you can set your own precision here

# Vertices
### showVertex(iVertices, iRadius=5):

	Description:
	
		Create sphere at given vertices, to show where are the points for debug purposes.
	
##### Description:
	
		iVertices: array with Vertex or floats objects
		iRadius (optional): ball Radius

##### Usage:
	
		MagicPanels.showVertex([ obj.Shape.CenterOfMass ], 20)

##### Result:
	
		remove old vertices and show new ones, return array of objects, spheres
### getVertex(iFace, iEdge, iVertex):

	Description:
	
		Get vertex values for face, edge and vertex index.
	
##### Description:
	
		iFace: face object
		iEdge: edge array index
		iVertex: vertex array index (0 or 1)

##### Usage:
	
		[ x, y, z ] = MagicPanels.getVertex(gFace, 0, 1)

##### Result:

		Return vertex position.

### getVertexAxisCross(iA, iB):

	Description:
	
		Return difference between iB and iA values with respect of coordinate axes.
	
##### Description:
	
		iA: vertex float value
		iB: vertex float value
	
##### Usage:
	
		edgeSize = MagicPanels.getVertexAxisCross(v0[0], v1[0])
		
##### Result:
	
		Return diff for vertices values.

### getVerticesPlane(iV1, iV2):

	Description:
	
		Gets axes with the same values.
	
##### Description:
	
		iV1: vertex object
		iV2: vertex object
	
##### Usage:
	
		plane = MagicPanels.getVerticesPlane(v1, v2)
		
##### Result:
	
		Return plane as "XY", "XZ", "YZ".

### setVertexPadding(iObj, iVertex, iPadding, iAxis):

	Description:
	
		Sets padding offset from given vertex to inside the object.
		Do not use it at getPlacement for Pads. Use 0 vertex instead.
		
		Note: This need to be improved.
	
##### Description:
	
		iObj: object
		iVertex: vertex object FreeCAD.Vector(x, y, z)
		iPadding: value > 0 for making offset
		iAxis: string: "X" or "Y" or "Z"
		
##### Usage:
	
		v = getattr(obj.Shape, "Vertex"+"es")[0]
		offsetX = MagicPanels.setVertexPadding(obj, v, 15, "X")
		
##### Result:
	
		Return return new position value for given axis.

# Edges
### getEdgeVertices(iEdge):

	Description:
	
		Gets all vertices values for edge.
	
##### Description:
	
		iEdge: edge object

##### Usage:
	
		[ v1, v2 ] = MagicPanels.getEdgeVertices(gEdge)

##### Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 1, 1, 1 ] ].

### getEdgeNormalized(iV1, iV2):

	Description:
	
		Returns vertices with exact sorted order V1 > V2, mostly used 
		to normalize Pad vertices.
	
##### Description:
	
		iV1: array with vertices e.g. [ 1, 1, 1 ]
		iV2: array with vertices e.g. [ 2, 2, 2 ]
	
##### Usage:
	
		[ v1, v2 ] = MagicPanels.getEdgeNormalized(v1, v2)
		
##### Result:
	
		for vertices [ 2, 2, 2 ], [ 1, 1, 1 ] return [ 1, 1, 1 ], [ 2, 2, 2 ]

### getEdgeIndex(iObj, iEdge):

	Description:
	
		Returns edge index for given object and edge.
	
##### Description:
	
		iObj: object of the edge
		iEdge: edge object

##### Usage:
	
		edgeIndex = MagicPanels.getEdgeIndex(gObj, gEdge)

##### Result:
	
		return int value for edge

### getEdgeIndexByKey(iObj, iBoundBox):

	Description:
	
		Returns edge index for given edge BoundBox.
	
##### Description:
	
		iObj: object of the edge
		iBoundBox: edge BoundBox as key

##### Usage:
	
		edgeIndex = MagicPanels.getEdgeIndex(o, key)

##### Result:
	
		return int value for edge

### getEdgePlane(iEdge):

	Description:
	
		Returns orientation for the edge, changed axis, as "X", "Y" or "Z".
	
##### Description:
	
		iEdge: edge object

##### Usage:
	
		plane = MagicPanels.getEdgePlane(edge)

##### Result:
	
		return string "X", "Y" or "Z".

# Router
### getSubByKey(iObj, iKey, iType, iSubType):

	Description:
	
		This is extended version of getEdgeIndexByKey function. 
		This function has been created to solve resized edge problem. If you cut the edge the next 
		edge will change the Length. So, also the BoundBox will be changed. With this function you 
		can customize reference key to solve the Topology Naming Problem.
	
##### Description:
	
		iObj: object for the sub-object
		iKey: array with keys
		iType: type of comparison
		iSubType: type of sub-object to return, "edge" or "face"

##### Usage:
	
		key = [ e.CenterOfMass, plane ]
		[ edge, edgeName, edgeIndex ] = MagicPanels.getSubByKey(o, key, "CenterOfMass", "edge")

##### Result:
	
		return edge object, name like Edge1 and also index starting from 0 (for iObj.Shape.Edges[index])

### getSketchPatternRotation(iObj, iSub):

	Description:
	
		Returns Rotation object which can be passed directly to setSketchPlacement 
		functions. The Sketch will be perpendicular to the iSub object, so it can be used as 
		router bit to cut the edge or face.
	
##### Description:
	
		iObj: object for sub-object
		iSub: selected sub-object, edge or face

##### Usage:
	
		r = MagicPanels.getSketchPatternRotation(o, edge)
		r = MagicPanels.getSketchPatternRotation(o, face)

##### Result:
	
		return FreeCAD.Rotation object.

### edgeRouter(iPad, iSub, iSketch, iLength, iLabel, iType):

	Description:
	
		This function is router for the edge. It cut the 
		iSub with iSketch pattern. The new object will get iLabel label.
	
##### Description:
	
		iPad: Pad object of the sub-object, for routing
		iSub: sub-object, edge or face
		iSketch: sketch object will be used as pattern to cut, the sketch should be around XYZ center cross.
		iLength: length to cut, float or int value, 0 means ThroughAll
		iLabel: label for new object
		iType: type of routing

##### Usage:
	
		router = MagicPanels.edgeRouter(pad, edge, sketch, 0, "routerCove", "simple")

##### Result:
	
		return router object, the result of cut

### makePockets(iObjects, iLength):

	Description:
	
		This function is multi Pocket. First object from iObjects will be base
		object to Pocket, all others should be Sketches. The Length is depth for Pocket. 
		If the Length is 0 the Pocket will be ThroughAll.
	
##### Description:
	
		iObjects: First base objects, next sketches
		iLength: length to cut, float or int value, 0 means ThroughAll
		
##### Usage:
	
		pocket = MagicPanels.makePockets(selectedObjects, 0)

##### Result:
	
		return last pocket object, the result of cut

# Faces
### getFaceIndex(iObj, iFace):

	Description:
	
		Returns face index for given object and face.
	
##### Description:
	
		iObj: object of the face
		iFace: face object

##### Usage:
	
		faceIndex = MagicPanels.getFaceIndex(gObj, gFace)

##### Result:
	
		return int value for face

### getFaceIndexByKey(iObj, iBoundBox):

	Description:
	
		Returns face index for given face BoundBox.
	
##### Description:
	
		iObj: object of the face
		iBoundBox: face BoundBox as key

##### Usage:
	
		faceIndex = MagicPanels.getFaceIndexByKey(o, key)

##### Result:
	
		return int value for face

### getFaceVertices(iFace, iType="4"):

	Description:
	
		Gets all vertices values for face.
	
##### Description:
	
		iFace: face object
		iType (optional): 
			* "4" - 4 vertices for normal Cube
			* "all" - get all vertices, for example for Cut object

##### Usage:
	
		[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(gFace)
		vertices = MagicPanels.getFaceVertices(gFace, "all")

##### Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 2, 2, 2 ], [ 3, 3, 3 ], [ 4, 4, 4 ] ]

### getFaceType(iObj, iFace):

	Description:
	
		Gets face type, if this is "edge" or "surface".
	
##### Description:
	
		iObj: object where is the face
		iFace: face object

##### Usage:
	
		faceType = MagicPanels.getFaceType(gObj, gFace)

##### Result:
	
		Return string "surface" or "edge".

### getFaceEdges(iObj, iFace):

	Description:
	
		Gets all edges for given face grouped by sizes.
	
##### Description:
	
		iObj: object where is the face
		iFace: face object

##### Usage:
	
		[ faceType, arrAll, arrThick, arrShort, arrLong ] = MagicPanels.getFaceEdges(gObj, gFace)

##### Result:
	
		Return arrays like [ faceType, arrAll, arrThick, arrShort, arrLong ] with edges objects, 
		
		faceType - string "surface" or "edge"
		arrAll - array with all edges
		arrThick - array with the thickness edges
		arrShort - array with the short edges (if type is edge this will be the same as arrThick)
		arrLong - array with the long edges

### getFacePlane(iFace):

	Description:
	
		Gets face plane in notation "XY", "XZ", "YZ". 

##### Description:
	
		iFace: face object

##### Usage:
	
		plane = MagicPanels.getFacePlane(face)

##### Result:
	
		string "XY", "XZ", or "YZ".
		
### getFaceSink(iObj, iFace):

	Description:
	
		Gets face sink axis direction in notation "+", or "-".

##### Description:
	
		iObj: object with the face
		iFace: face object

##### Usage:
	
		sink = MagicPanels.getFaceSink(obj, face)

##### Result:
	
		string "+" if the object at face should go along axis forward, 
		or "-" if the object at face should go along axis backward

### getFaceObjectRotation(iObj, iFace):

	Description:
	
		Gets face object rotation to apply to the new created object at face. 
		Object created at face with this rotation should be up from the face.

##### Description:
	
		iObj: object with the face
		iFace: face object

##### Usage:
	
		r = MagicPanels.getFaceObjectRotation(obj, face)

##### Result:
	
		FreeCAD.Rotation object that can be directly pass to the setPlacement or object.Placement

### getFaceDetails(iObj, iFace):

	Description:
	
		Allows to get detailed information for face direction.
	
##### Description:
	
		iObj: selected object
		iFace: selected face object

##### Usage:
	
		[ plane, type ] = MagicPanels.getFaceDetails(gObj, gFace)

##### Result:
	
		[ "XY", "surface" ] - if the direction is XY and it is surface, no thickness edge
		[ "XY", "edge" ] - if the direction is XY and it is edge, there is thickness edge
		[ "XY", "equal" ] - if the direction is XY and both edges are equal
		
		Note: The first argument can be "XY", "YX", "XZ", "ZX", "YZ", "ZY". 
		This is related to face not to object. The object direction will be different.
		
# References
### getReference(iObj="none"):

	Description:
	
		Gets reference to the selected or given object.
	
##### Description:
	
		iObj (optional): object to get reference (to return base object)
	
##### Usage:
	
		gObj = MagicPanels.getReference()
		gObj = MagicPanels.getReference(obj)
		
##### Result:
	
		gObj - reference to the base object

# Sizes
### getSizes(iObj):

	Description:
	
		Allows to get sizes for object (iObj), according to the object type. 
		The values are not sorted.
	
##### Description:
	
		iObj: object to get sizes

##### Usage:
	
		[ size1, size2, size3 ] = MagicPanels.getSizes(obj)

##### Result:
	
		Returns [ Length, Width, Height ] for Cube.

### getSizesFromVertices(iObj):

	Description:
	
		Gets occupied space by the object from vertices.
	
##### Description:
	
		iObj: object
	
##### Usage:
	
		[ sx, sy, sz ] = MagicPanels.getSizesFromVertices(obj)

##### Result:
	
		Returns array with [ mX, mY, mZ ] where: 
		mX - occupied space along X axis
		mY - occupied space along Y axis
		mZ - occupied space along Z axis

### getSizesFromBoundBox(iObj):

	Description:
	
		Gets occupied space by the object from BoundBox. This can be useful for round shapes, 
		where is no vertices at object edges, e.g. cylinders, circle at Sketch.
	
##### Description:
	
		iObj: object
	
##### Usage:
	
		[ sx, sy, sz ] = MagicPanels.getSizesFromVertices(obj)

##### Result:
	
		Returns array with [ mX, mY, mZ ] where: 
		mX - occupied space along X axis
		mY - occupied space along Y axis
		mZ - occupied space along Z axis

# Measurements
### showMeasure(iP1, iP2, iRef=""):

	Description:
	
		Creates measurements object, I mean draw it. Now it use FreeCAD function 
		to create and draw object. But in the future this can be changed to 
		more beautiful drawing without changing tools. 
	
##### Description:
	
		iP1: starting point vertex object
		iP2: ending point vertex object
		iRef (optional): string for future TechDraw import or any other use, other tools

##### Usage:
	
		m = MagicPanels.showMeasure(gP1, gP2, "Pad")

##### Result:
	
		Create measure object, draw it and return measure object for further processing. 

### getDistanceBetweenFaces(iObj1, iObj2, iFace1, iFace2):

	Description:
	
		Gets distance between iFace1 and iFace2.
	
##### Description:
	
		iObj1: object of iFace1
		iObj2: object of iFace2
		iFace1: face object
		iFace2: face object

##### Usage:
	
		size = MagicPanels.getDistanceBetweenFaces(o1, o2, face1, face2)

##### Result:

		return distance between face1 object and face2 object

# Direction, Plane, Orientation, Axis
### getModelRotation(iX, iY, iZ):

	Description:
	
		Transform given iX, iY, iZ values to the correct vector, if the user rotated 3D model.

##### Description:
	
		iX: X value to transform
		iY: Y value to transform
		iY: Z value to transform

##### Usage:
	
		[x, y, z ] = MagicPanels.getModelRotation(x, y, z)

##### Result:
	
		[ X, Y, Z ] - transformed vector of given values

### getDirection(iObj):

	Description:
	
		Allows to get Cube object direction (iType).
	
##### Description:
	
		iObj: selected object

##### Usage:
	
		direction = MagicPanels.getDirection(obj)

##### Result:
	
		Returns iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

# Position, Placement, Move
### resetPlacement(iObj):

	Description:
	
		Reset placement for given object. Needed to set rotation for object at face.
	
##### Description:
	
		iObj: object to reset placement

##### Usage:
	
		MagicPanels.resetPlacement(obj)

##### Result:
	
		Object obj return to base position.

### getPlacement(iObj):

	Description:
	
		Gets placement with rotation info for given object.
		Note: This is useful if you not use containers. 
	
##### Description:
	
		iObj: object to get placement

##### Usage:
	
		[ x, y, z, r ] = MagicPanels.getPlacement(gObj)

##### Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

### getGlobalPlacement(iObj):

	Description:
	
		Calls FreeCAD getGlobalPlacement at base object, and return useful form of placement.
	
##### Description:
	
		iObj: object to get placement

##### Usage:
	
		[ x, y, z, r ] = MagicPanels.getGlobalPlacement(o)

##### Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

### setPlacement(iObj, iX, iY, iZ, iR, iAnchor=""):

	Description:
	
		Sets placement with rotation for given object.
	
##### Description:

		iObj: object to set custom placement and rotation
		iX: X Axis object position
		iX: Y Axis object position
		iZ: Z Axis object position
		iR: Rotation object
		iAnchor="" (optional): anchor for placement instead of 0 vertex, FreeCAD.Vector(x, y, z)

##### Usage:
	
		MagicPanels.setPlacement(gObj, 100, 100, 200, r)

##### Result:
	
		Object gObj should be moved into 100, 100, 200 position without rotation.

### getSketchPlacement(iSketch, iType):

	Description:
	
		Gets placement dedicated to move and copy Sketch directly.
	
##### Description:
	
		iSketch: Sketch object
		iType: 
			"attach" - AttachmentOffset position, need to be converted later
			"clean" - directly from Placement, so the AttachmentOffset don't need to be converted
			"global" - global Sketch position, can be directly set to object

##### Usage:
	
		[ x, y, z, r ] = MagicPanels.getSketchPlacement(sketch, "global")

##### Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

### setSketchPlacement(iSketch, iX, iY, iZ, iR, iType):

	Description:
	
		Set placement with rotation dedicated to move and copy Sketch directly.
	
##### Description:

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

##### Usage:
	
		MagicPanels.setSketchPlacement(sketch, 100, 100, 200, r, "global")

##### Result:
	
		Object Sketch should be moved.

### getObjectCenter(iObj):

	Description:
	
		Returns center of the object.
	
		Note: This function will be updated later with more reliable 
		way of getting center of the object, also for LinkGroup and other containers. 
		Now it returns Shape.CenterOfMass for the object and it is not the same 
		as center of the object.
	
##### Description:
	
		iObj: object

##### Usage:
	
		[ cx, cy, cz ] = MagicPanels.getObjectCenter(obj)

##### Result:
	
		Returns array with [ cx, cy, cz ] values for center point.

# Containers
### getContainersOffset(iObj):

	Description:
	
		If the object is in the container like Part, Body, LingGroup the vertices are 
		not updated by FreeCAD. From FreeCAD perspective the object is still in the 
		same place. This function is trying to solve this problem and calculates 
		all offsets of all containers.
	
##### Description:
	
		iObj: object to get containers offset

##### Usage:
	
		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(o)

##### Result:
	
		return [ coX, coY, coZ, coR ] array with offsets for placement:
		
		coX: X Axis object position
		coY: Y Axis object position
		coZ: Z Axis object position
		coR: Rotation object

### getVerticesOffset(iVertices, iObj, iType="array"):

	Gets iObj offset of all supported containers for vertices iVertices.
	
##### Description:
	
		iObj: object to get containers offset
		iVertices: vertices array
		iType:
			"array" - array with floats [ 1, 2, 3 ]
			"vector" - array with FreeCAD.Vector types
		
##### Usage:
	
		vertices = MagicPanels.getVerticesOffset(vertices, o, "array")

##### Result:
	
		return vertices array with correct container offset

### getVerticesPosition(iVertices, iObj, iType="array"):

	Description:
	
		Gets iVertices 3D position. This function should be used to show or select iVertices with rotation. 
		It calculates all offsets with rotation. But this function should not be used for calculation. 
		Because the vertices at FreeCAD are raw, without containers offset. The vertices at FreeCAD have only 
		AttachmentOffset applied. If you start calculation with rotation, you need to calculate plane correctly.
	
##### Description:
	
		iVertices: vertices array
		iObj: object to get containers offset
		iType:
			"array" - array with floats [ 1, 2, 3 ]
			"vector" - array with FreeCAD.Vector types
			"vertex" - array with Part.Vertex types

##### Usage:
	
		vertices = MagicPanels.getVerticesPosition(vertices, o, "array")
		MagicPanels.showVertex(iVertices, 10)

##### Result:
	
		return vertices array with correct container offset

### removeVerticesOffset(iVertices, iObj, iType="array"):

	Description:
	
		Remove iObj container offset for vertices iVertices.
	
##### Description:
	
		iVertices: vertices array
		iObj: object to remove containers offset
		iType:
			"array" - array with floats [ 1, 2, 3 ]
			"vector" - array with FreeCAD.Vector types

##### Usage:
	
		vertices = MagicPanels.removeVerticesOffset(vertices, o, "array")

##### Result:
	
		return vertices array without container offset

### moveToContainer(iObjects, iSelection):

	Description:
	
		Move objects iObjects to container for iSelection object. 
		Container need to be in the clean path, no other objects except Group or LinkGroup, 
		for example LinkGroup -> LinkGroup is clean path, only containers, but the 
		Mirror -> LinkGroup is not considered as clean container path here.
	
##### Description:
	
		iObjects: list of objects to move to container, for example new created Cube
		iSelection: selected object, for example Pad

##### Usage:
	
		MagicPanels.moveToContainer([ o ], pad)

##### Result:
	
		No return, move object.

### moveToFirst(iObjects, iSelection):

	Description:
	
		Move objects iObjects to first container above Body for iSelection object.
		This can be used to force object at face to be moved into Mirror -> LinkGroup.
	
##### Description:
	
		iObjects: list of objects to move to container, for example new created Cube
		iSelection: selected object, for example Pad

##### Usage:
	
		MagicPanels.moveToFirst([ o ], pad)

##### Result:
	
		No return, move object.

### moveToFirstWithInverse(iObjects, iSelection):

	Description:
	
		This version remove the placement and rotation offset from iObjects and move the iObjects to first 
		supported container (LinkGroup). 
		
		Note: It is dedicated to move panel created from vertices to the first LinkGroup container. 
		The object created from vertices have applied offset with rotation after creation 
		but is outside the container. So if you move it manually it will be in the wrong place because 
		container apply the placement and rotation again. So, you have to remove the offset and move it. 
		Yea, that's the beauty of FreeCAD ;-)
	
##### Description:
	
		iObjects: list of objects to move to container, for example new created Cube
		iSelection: selected object, for example Pad

##### Usage:
	
		MagicPanels.moveToFirstWithInverse([ o ], pad)

##### Result:
	
		No return, move object.

### moveToParent(iObjects, iSelection):

	Description:
	
		This version move object to parent container without adding or remove offset. This is useful if you copy the 
		Sketch, because SKetch after copy is located outside Body, in Part. But if the Part is inside LinkGroup 
		the copied Sketch will be located outside LinkGroup, in main root folder. This is problematic because 
		the Sketch after copy has offset from containers. The object to move need to be in root folder to avoid 
		duplicated already copied objects, Cube.
	
##### Description:
	
		iObjects: list of objects to move to container, for example new created Sketch
		iSelection: selected object, for example Sketch

##### Usage:
	
		MagicPanels.moveToParent([ copy ], sketch)

##### Result:
	
		No return, move object.

### getObjectToMove(iObj):

	Description:
	
		This function returns object to move.
	
##### Description:
	
		iObj: object to get placement, selected container or base reference object

##### Usage:
	
		toMove = MagicPanels.getObjectToMove(o)

##### Result:
	
		For example: 

		for Cube: always returns Cube
		for Pad: always returns Body
		for LinkGroup: returns LinkGroup
		for Cut: returns Cut
		for other PartDesign objects: try to return Body
		for any other object: returns object

### createContainer(iObjects, iLabel=""):

	Description:
	
		This function creates container for given iObjects. The label for new container will be get from 
		first element of iObjects (iObjects[0]).
	
##### Description:
	
		iObjects: array of object to create container for them
		iLabel: container label

##### Usage:
	
		container = MagicPanels.createContainer([c1, c2])

##### Result:
	
		Created container and objects inside the container, return container object.

### getContainerPlacement(iObj, iType="clean"):

	Description:
	
		This function returns placement for the object with all 
		containers offsets or clean. The given object might be container or 
		selected object, the base Cube or Pad.
	
##### Description:
	
		iObj: object to get placement
		iType (optional): 
			"clean" - to get iObj.Placement, 
			"offset" to get iObj.Placement with containers offset.

##### Usage:
	
		[ x, y, z, r ] = MagicPanels.getContainerPlacement(o, "clean")
		[ x, y, z, r ] = MagicPanels.getContainerPlacement(o, "offset")

##### Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object - not supported yet

### getPlacementDiff(iStart, iDestination):

	Description:
	
		Return diff that should be added to iStart to move object from iStart to iDestination position. 
		If you want to move back you can minus the diff from iDestination.
		
##### Description:
	
		iStart: start vertex float value
		iDestination: destination vertex float value
	
##### Usage:
		
		[ moveX, moveY, moveZ ] = MagicPanels.getPlacementDiff(v1, v2)
		
##### Result:
	
		Return [ moveX, moveY, moveZ ] array with X, Y, Z floats to move object.

### setContainerPlacement(iObj, iX, iY, iZ, iR, iAnchor="auto"):

	Description:
	
		Little more advanced set placement function, especially used with containers.
		Adding offset here not make sense, because object can be moved via container so all the vertices might 
		be equal. Vertices not have containers offsets. They are only impacted by AttachmentOffset. 
		So you need to add all needed offsets and call this function with offsets.
	
##### Description:

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
		
##### Usage:
		
		MagicPanels.setContainerPlacement(cube, 100, 100, 200, 0, "clean")
		MagicPanels.setContainerPlacement(pad, 100, 100, 200, 0, "auto")
		MagicPanels.setContainerPlacement(body, 100, 100, 200, 0, "center")

##### Result:
	
		Object should be moved into 100, 100, 200 position with exact anchor.

# Conversion
### convertPosition(iObj, iX, iY, iZ):

	Description:
	
		Convert given position vector to correct position values according 
		to the object direction.
	
##### Description:
	
		iObj: object
		iX: x position
		iY: y position
		iZ: z position

##### Usage:
	
		[ x, y, z ] = MagicPanels.convertPosition(obj, 0, 400, 0)

##### Result:
	
		For Pad object in XZ direction return the AttachmentOffset order [ 0, 0, -400 ]

### sizesToCubePanel(iObj, iType):

	Description:
	
		Converts selected object (iObj) sizes to Cube panel sizes into given direction (iType). 
		So, the returned values can be directly assigned to Cube object in order to create 
		panel in exact direction.

##### Description:

		iObj: selected object
		iType direction: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

##### Usage:

		[ Length, Width, Height ] = MagicPanels.sizesToCubePanel(obj, "YZ")

##### Result:

		Returns [ Length, Width, Height ] for YZ object placement.

# Replace
### makePad(iObj, iPadLabel="Pad"):

	Description:
	
		Allows to create Part, Plane, Body, Pad, Sketch objects.
	
##### Description:
	
		iObj: object Cube to change into Pad
		iPadLabel: Label for the new created Pad, the Name will be Pad

##### Usage:

		[ part, body, sketch, pad ] = MagicPanels.makePad(obj, "myPanel")

##### Result:
	
		Created Pad with correct placement, rotation and return [ part, body, sketch, pad ].

# Holes
### makeHoles(iObj, iFace, iCylinders):

	Description:
	
		Making holes.

##### Description:

		iObj: base object to make hole
		iFace: face of base object to make hole
		iCylinders: list of cylinders to make holes below each one

##### Usage:

		holes = MagicPanels.makeHoles(obj, face, cylinders)
		
##### Result:

		Make holes and return list of holes.

### makeCountersinks(iObj, iFace, iCones):

	Description:
	
		Making countersinks.

##### Description:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makeCountersinks(obj, face, cones)

##### Result:

		Make holes and return list of holes. 

### makeCounterbores(iObj, iFace, iCones):

	Description:
	
		Making counterbores.

##### Description:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makeCounterbores(obj, face, cones)

##### Result:

		Make holes and return list of holes.

### makePocketHoles(iObj, iFace, iCones):

	Description:
	
		Making pocket holes for invisible connections.

##### Description:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makePocketHoles(obj, face, cones)

##### Result:

		Make holes and return list of holes.

### makeCounterbores2x(iObj, iFace, iCones):

	Description:
	
		Making counterbores from both sides.

##### Description:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makeCounterbores2x(obj, face, cones)

##### Result:

		Make holes and return list of holes.

# Joinery
### makeCuts(iObjects):

	Description:
	
		Allows to create multi bool cut operation at given objects. First objects 
		from iObjects is the base element and all other will cut the base. 
		The copies will be created for cut. 
	
##### Description:
	
		iObjects: objects to parse by multi bool cut

##### Usage:
	
		cuts = MagicPanels.makeCuts(objects)

##### Result:
	
		Array of cut objects will be returned.

### makeFrame45cut(iObjects, iFaces):

	Description:
	
		Makes 45 frame cut with PartDesing Chamfer. For each face the ends will be cut.
	
##### Description:
	
		iObjects: array of objects to cut
		iFaces: dict() of faces for Chamfer cut direction, the key is iObjects value (object), 
				if there are more faces for object, the first one will be get as direction.

##### Usage:
	
		frames = MagicPanels.makeFrame45cut(objects, faces)
		
##### Result:
	
		Created Frames with correct placement, rotation and return array with Chamfer frame objects.

### makeChamferCut(iObjects, iEdges, iSizes, iLabels):

	Description:
	
		Makes PartDesing Chamfer cut for edges array. But you can set different size for each edge. 
		Yes, you give edge objects, and you make chamfer for each edge, one by one, with different 
		size, but the most funny part is that the selected edge not exists because the Cube 
		object not exists ;-)

##### Description:
	
		iObjects: array of objects to cut
		iEdges: dict() of arrays [ edgeObj1, edgeObj2 ], edgeArr = iEdges[iObjects[0]]
		iSizes: dict() of arrays [ 100, 50 ], sizeArr = iSizes[iObjects[0]]
		iLabels: dict() of labels for new object, label = iLabels[iObjects[0]]

##### Usage:
	
		cuts = MagicPanels.makeChamferCut(objects, edges, sizes, labels)
		
##### Result:
	
		return array with chamfer objects

### makeMortise(iSketch, iDepth, iPad, iFace):

	Description:
	
		Make Mortise pocket for given iSketch pattern.

##### Description:

		iSketch: Sketch object as pattern for Mortise
		iDepth: depth of the pocket
		iPad: pad object to get Body
		iFace: face object at the pad where is the iSketch

##### Usage:

		[ obj, face ] = MagicPanels.makeMortise(sketch, 20, obj, face)

##### Result:

		Make Mortise and return new object and face reference for GUI info screen update and further processing

### makeTenon(iSketch, iLength, iPad, iFace):

	Description:
	
		Make Tenon pad for given iSketch pattern.

##### Description:

		iSketch: Sketch object as pattern for Mortise
		iLength: Length for the Tenon pad
		iPad: pad object to get Body
		iFace: face object at the pad where is the iSketch

##### Usage:

		[ obj, face ] = MagicPanels.makeTenon(sketch, 20, obj, face)

##### Result:

		Make Tenon and return new object and face reference for GUI info screen update and further processing

# Colors
### copyColors(iSource, iTarget):

	Description:
	
		Allows to copy colors from iSource object to iTarget object.

##### Description:

		iSource: source object
		iTarget: target object

##### Usage:

		try:
			MagicPanels.copyColors(panel, copy)
		except:
			skip = 1

##### Result:

		All colors structure should be copied from source to target.

# Spreadsheet
### sheetGetKey(iC, iR):

	Description:
	
		Allows to get key as letters for spreadsheet from given column and row index.

##### Description:
	
		iC: column index
		iR: row index

##### Usage:
	
		key = MagicPanels.sheetGetKey(1, 2)

##### Result:
	
		return key string

# Info screen
### showInfo(iCaller, iInfo, iNote="yes"):

	Description:
	
		Allows to show Gui info box for all available function and multiple calls.

##### Description:
	
		iCaller: window title
		iInfo: HTML text to show
		iNote: additional tutorial ("yes" or "no"), by default is "yes".

##### Usage:

		info = "text to show"
		iType = "XY"
		
		MagicPanels.showInfo("window title", info)
		MagicPanels.showInfo("window title", info, "no")

##### Result:
	
		Show info Gui.

