

# MagicPanels

	This is MagicPanels library for Woodworking workbench.
	Darek L (github.com/dprojects)

### Usage:

	import MagicPanels
	returned_value = MagicPanels.function(args)

### Functions at this library:

* Should not have error handling and pop-ups, so you can call it from GUI tools in loops.
* Should return value, if further processing needed.






# Globals

* `gRoundPrecision = 2 `: should be set according to the user FreeCAD GUI settings <br>
* `gSearchDepth = 200 `: recursive search depth <br>
* `gKernelVersion = 0 `: FreeCAD version to add support for new kernel changes <br>
* `gSettingsPref = 'User parameter:BaseApp/Preferences/Woodworking'`: settings path <br>
* `gTheme = "default" `: no theme by default <br>
* `gDefaultColor = (0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 1.0)`: default color [247, 185, 108, 255] <br>
* `gWoodThickness = 18`: wood thickness <br>
* `gWindowStaysOnTop = True `: to keep window on top <br> 
* `gCurrentSelection = False`: to skip refresh selection button <br>

> [!CAUTION]
> Globals are updated from user settings via updateGlobals function at the end of the library.

# Functions for general purpose

### isType(iObj, iType="Clone"):
	
##### Description:
	
		This function checks if the given object iObj is iType. 
		It has been created mostly for Clones. The Clones are "Part::FeaturePython" type. 
		But the problem is that many other FreeCAD objects are "Part::FeaturePython" type as well, 
		for example Array. So, you can't recognize the Clones only with .isDerivedFrom() function or 
		even .TypeId. To simplify the code look you can hide the ckecks behind the function.
	
##### Args:
	
		iObj: object
		iType: string for type:
			"Clone" - for clones
			"Array" - for BIM or Draft Array

##### Usage:
	
		if MagicPanels.isType(o, "Clone"):
			do something ...

##### Result:
	
		return True or False, so you can use it directly in if statement

### equal(iA, iB):
	
##### Description:
	
		At FreeCAD there are many values like 1.000006, especially for PartDesign objects. 
		So if you want to compare such values this sometimes might be True and sometimes False. 
		So, finally I decided to write my own function for comparison.
	
##### Args:
	
		iA: float value
		iB: float value

##### Usage:
	
		if MagicPanels.equal(1.0006, 1):
			do something ...

##### Result:
	
		return True if equal or False if not

### touchTypo(iObj):
	
##### Description:
	
		Touch the typo so that the typo-snake does not notice it ;-) LOL
	
##### Args:
	
		iObj: object to touch

##### Usage:
	
		vs = MagicPanels.touchTypo(o)

##### Result:
	
		return Vertex + es for object o

### normalizeBoundBox(iBoundBox):
	
##### Description:
	
		Return normalized version of BoundBox. All values 0.01 will be rounded 
		allowing comparison, and searches for the same face or edge.
	
##### Args:
	
		iBoundBox: directly pass BoundBox object

##### Usage:
	
		e1 = obj1.Shape.Edges[0]
		e2 = obj2.Shape.Edges[0]

		b1 = MagicPanels.normalizeBoundBox(e1.BoundBox)
		b2 = MagicPanels.normalizeBoundBox(e2.BoundBox)

##### Result:
	
		return normalized version for comparison if b1 == b2: you can set your own precision here


# References

### getReference(iObj="none"):
	
##### Description:
	
		Gets reference to the selected or given object.
	
##### Args:
	
		iObj (optional): object to get reference (to return base object)
	
##### Usage:
	
		gObj = MagicPanels.getReference()
		gObj = MagicPanels.getReference(obj)
		
##### Result:
	
		gObj - reference to the base object

### getBody(iObj):
	
##### Description:
	
		Return Body for given object.
	
##### Args:
	
		iObj: object to get Body

##### Usage:
	
		body = MagicPanels.getBody(sketch)

##### Result:
	
		Return body object or empty string if there is no Body


# Sizes

### getSizesFromVertices(iObj):
	
##### Description:
	
		Gets occupied space by the object from vertices.
	
##### Args:
	
		iObj: object
	
##### Usage:
	
		[ sx, sy, sz ] = MagicPanels.getSizesFromVertices(obj)

##### Result:
	
		Returns array with [ mX, mY, mZ ] where: 
		mX - occupied space along X axis
		mY - occupied space along Y axis
		mZ - occupied space along Z axis

### getSizesFromBoundBox(iObj):
	
##### Description:
	
		Gets occupied space by the object from BoundBox. This can be useful for round shapes, 
		where is no vertices at object edges, e.g. cylinders, circle at Sketch.
	
##### Args:
	
		iObj: object
	
##### Usage:
	
		[ sx, sy, sz ] = MagicPanels.getSizesFromBoundBox(obj)

##### Result:
	
		Returns array with [ mX, mY, mZ ] where: 
		mX - occupied space along X axis
		mY - occupied space along Y axis
		mZ - occupied space along Z axis

### getOccupiedSpace(iObjects):
	
##### Description:
	
		Function to get occupied space by many objects. 
	
##### Args:
	
		iObjects: array with objects
	
##### Usage:
	
		[ minX, minY, minZ, maxX, maxY, maxZ, [ cx, cy, cz ]] = MagicPanels.getOccupiedSpace(objects)

##### Result:
	
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

### getSizesFromSketch(iSketch):
	
##### Description:
	
		Allows to get sizes for Sketch. If the iSketch object has defined SizeX and SizeY constraints the 
		array with those values will be returned. If there is no SizeX and SizeY constraints this function will try 
		to get iSketch size in other way.
	
##### Args:
	
		iSketch: sketch object to get sizes

##### Usage:
	
		[ SizeX, SizeY ] = MagicPanels.getSizesFromSketch(sketch)

##### Result:
	
		Returns array with floats [ SizeX, SizeY ]

### getSizes(iObj):
	
##### Description:
	
		Allows to get sizes for object (iObj), according to the object type. 
		The values are not sorted.
	
##### Args:
	
		iObj: object to get sizes

##### Usage:
	
		[ size1, size2, size3 ] = MagicPanels.getSizes(obj)

##### Result:
	
		Returns [ Length, Width, Height ] for Cube.


# Copy

### copyPanel(iObjects, iType="auto"):
	
##### Description:
	
		This function has been created for magicMove tool to copy any object type.

##### Args:
	
		iObjects: array with objects to copy
		iType (optional): copy type:
			* "auto" - if the object is Cube it will be copyObject, otherwise Clone will be used to copy
			* "copyObject" - force copyObject copy type, however not use at LinkGroup because it will be visible as single object if you remove the copy the base LinkGroup will be removed as well, and the copy will not be visible at cut-list report
			* "Clone" - force Clone copy type, if you make Clone from Pad and the Pad has Sketch.AttachmentOffset the Clone has Placement set to XYZ (0,0,0) but is not in the zero position so you have to remove Sketch offset from the Clone, I guess the BoundBox is the correct solution here
			* "Link" - force Link copy type, it is faster than Clone but sometimes might be broken

##### Usage:
	
		copies = MagicPanels.copyPanel([ o ])
		copies = MagicPanels.copyPanel([ o ], "auto")
		copies = MagicPanels.copyPanel([ o ], "copyObject")
		copies = MagicPanels.copyPanel([ o ], "Clone")
		copies = MagicPanels.copyPanel([ o ], "Link")
		copy = MagicPanels.copyPanel([ o ], "auto")[0]
		copy = MagicPanels.copyPanel([ o ])[0]

##### Result:
	
		return array with copies
### getObjectToCopy(iObj):
	
##### Description:
	
		This function returns object to copy.
	
##### Args:
	
		iObj: object to get reference to copy

##### Usage:
	
		toCopy = MagicPanels.getObjectToCopy(o)

##### Result:
	
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


# Edges

### getEdgeVertices(iEdge):
	
##### Description:
	
		Gets all vertices values for edge.
	
##### Args:
	
		iEdge: edge object

##### Usage:
	
		[ v1, v2 ] = MagicPanels.getEdgeVertices(gEdge)

##### Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 1, 1, 1 ] ].

### getEdgeVectors(iEdge):
	
##### Description:
	
		Gets all vertices values for edge as FreeCAD.Vector array.
	
##### Args:
	
		iEdge: edge object

##### Usage:
	
		[ v1, v2 ] = MagicPanels.getEdgeVectors(edge)

##### Result:
	
		Return vertices array like [ FreeCAD.Vector, FreeCAD.Vector ].

### getEdgeNormalized(iV1, iV2):
	
##### Description:
	
		Returns vertices with exact sorted order V1 > V2, mostly used 
		to normalize Pad vertices.
	
##### Args:
	
		iV1: array with vertices e.g. [ 1, 1, 1 ]
		iV2: array with vertices e.g. [ 2, 2, 2 ]
	
##### Usage:
	
		[ v1, v2 ] = MagicPanels.getEdgeNormalized(v1, v2)
		
##### Result:
	
		for vertices [ 2, 2, 2 ], [ 1, 1, 1 ] return [ 1, 1, 1 ], [ 2, 2, 2 ]

### getEdgeIndex(iObj, iEdge):
	
##### Description:
	
		Returns edge index for given object and edge.
	
##### Args:
	
		iObj: object of the edge
		iEdge: edge object

##### Usage:
	
		edgeIndex = MagicPanels.getEdgeIndex(gObj, gEdge)

##### Result:
	
		return int value for edge

### getEdgeIndexByKey(iObj, iBoundBox):
	
##### Description:
	
		Returns edge index for given edge BoundBox.
	
##### Args:
	
		iObj: object of the edge
		iBoundBox: edge BoundBox as key

##### Usage:
	
		edgeIndex = MagicPanels.getEdgeIndex(o, key)

##### Result:
	
		return int value for edge

### getEdgePlane(iObj, iEdge, iType="auto"):
	
##### Description:
	
		Returns orientation for the edge, changed axis, as "X", "Y" or "Z".
	
##### Args:
	
		iObj: object with the edge
		iEdge: edge object
		iType:
			* "auto" - check if panel is rotated and get edge plane from its base not rotated position
			* "clean" - return plane for current edge position

##### Usage:
	
		plane = MagicPanels.getEdgePlane(o, edge)

##### Result:
	
		return string "X", "Y" or "Z".

### getSizeByEdge(iObj, iEdge):
	
##### Description:
	
		Returns iObj property (objects field name) to change for iEdge. 
	
##### Args:
	
		iObj: object with the edge
		iEdge: edge object

##### Usage:
	
		name = MagicPanels.getSizeByEdge(o, edge)

##### Result:
	
		For Cube (Part::Box) object returns string "Length", "Width" or "Height".


# Faces

### getFaceIndex(iObj, iFace):
	
##### Description:
	
		Returns face index for given object and face.
	
##### Args:
	
		iObj: object of the face
		iFace: face object

##### Usage:
	
		faceIndex = MagicPanels.getFaceIndex(gObj, gFace)

##### Result:
	
		return int value for face

### getFaceIndexByKey(iObj, iBoundBox):
	
##### Description:
	
		Returns face index for given face BoundBox.
	
##### Args:
	
		iObj: object of the face
		iBoundBox: face BoundBox as key

##### Usage:
	
		faceIndex = MagicPanels.getFaceIndexByKey(o, key)

##### Result:
	
		return int value for face

### getFaceVertices(iFace, iType="4"):
	
##### Description:
	
		Gets all vertices values for face.
	
##### Args:
	
		iFace: face object
		iType (optional): 
			* "4" - 4 vertices for normal Cube
			* "all" - get all vertices, for example for Cut object
			* "vector" - get all vertices as FreeCAD.Vector objects

##### Usage:
	
		[ v1, v2, v3, v4 ] = MagicPanels.getFaceVertices(gFace)
		vertices = MagicPanels.getFaceVertices(gFace, "all")
		vectors = MagicPanels.getFaceVertices(face, "vector")

##### Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 2, 2, 2 ], [ 3, 3, 3 ], [ 4, 4, 4 ] ]

### getFaceType(iObj, iFace):
	
##### Description:
	
		Gets face type, if this is "edge" or "surface".
	
##### Args:
	
		iObj: object where is the face
		iFace: face object

##### Usage:
	
		faceType = MagicPanels.getFaceType(gObj, gFace)

##### Result:
	
		Return string "surface" or "edge".

### getFaceEdges(iObj, iFace):
	
##### Description:
	
		Gets all edges for given face grouped by sizes.
	
##### Args:
	
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
	
##### Description:
	
		Gets face plane in notation "XY", "XZ", "YZ". 

##### Args:
	
		iFace: face object

##### Usage:
	
		plane = MagicPanels.getFacePlane(face)

##### Result:
	
		string "XY", "XZ", or "YZ".
		
### getFaceSink(iObj, iFace):
	
##### Description:
	
		Gets face sink axis direction in notation "+", or "-".

##### Args:
	
		iObj: object with the face
		iFace: face object

##### Usage:
	
		sink = MagicPanels.getFaceSink(obj, face)

##### Result:
	
		string "+" if the object at face should go along axis forward, 
		or "-" if the object at face should go along axis backward

### getFaceObjectRotation(iObj, iFace):
	
##### Description:
	
		Gets face object rotation to apply to the new created object at face. 
		Object created at face with this rotation should be up from the face.

##### Args:
	
		iObj: object with the face
		iFace: face object

##### Usage:
	
		r = MagicPanels.getFaceObjectRotation(obj, face)

##### Result:
	
		FreeCAD.Rotation object that can be directly pass to the setPlacement or object.Placement

### getFaceDetails(iObj, iFace):
	
##### Description:
	
		Allows to get detailed information for face direction.
	
##### Args:
	
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
		

# Vertices

### vertices2vectors(iVertices):
	
##### Description:
	
		Converts vertices into vector objects.
	
##### Args:
	
		iVertices: array with vertices

##### Usage:
	
		vertices = MagicPanels.touchTypo(obj.Shape)
		vectors = MagicPanels.vertices2vectors(vertices)

##### Result:
	
		return array with vectors
### showVertex(iVertices, iRadius=20, iColor="red"):
	
##### Description:
	
		Create sphere at given vertices, to show where are the points for debug purposes.
	
##### Args:
	
		iVertices: array with Vertex or floats objects
		iRadius (optional): ball Radius
		iColor: string "red", "green", "blue", or color tuple like (1.0, 0.0, 0.0, 0.0)

##### Usage:
	
		MagicPanels.showVertex([ obj.Shape.CenterOfMass ], 20)

##### Result:
	
		remove old vertices and show new ones, return array of objects, spheres
### getVertex(iFace, iEdge, iVertex):
	
##### Description:
	
		Get vertex values for face, edge and vertex index.
	
##### Args:
	
		iFace: face object
		iEdge: edge array index
		iVertex: vertex array index (0 or 1)

##### Usage:
	
		[ x, y, z ] = MagicPanels.getVertex(gFace, 0, 1)

##### Result:

		Return vertex position.

### getVertexIndex(iObj, iVertex):
	
##### Description:
	
		Returns vertex index for given object and vertex object.
	
##### Args:
	
		iObj: object of the vertex
		iVertex: vertex object

##### Usage:
	
		vertexIndex = MagicPanels.getVertexIndex(o, v)

##### Result:
	
		return int value for vertex name, so you can create string Vertex + vertexIndex, 
		or get vertex from vertices array

### getVertexAxisCross(iA, iB):
	
##### Description:
	
		Return difference between iB and iA values with respect of coordinate axes.
	
##### Args:
	
		iA: vertex float value
		iB: vertex float value
	
##### Usage:
	
		edgeSize = MagicPanels.getVertexAxisCross(v0[0], v1[0])
		
##### Result:
	
		Return diff for vertices values.

### getVerticesPlane(iV1, iV2):
	
##### Description:
	
		Gets axes with the same values.
	
##### Args:
	
		iV1: vertex object
		iV2: vertex object
	
##### Usage:
	
		plane = MagicPanels.getVerticesPlane(v1, v2)
		
##### Result:
	
		Return plane as "XY", "XZ", "YZ".

### setVertexPadding(iObj, iVertex, iPadding, iAxis):
	
##### Description:
	
		Sets padding offset from given vertex to inside the object.
		Do not use it at getPlacement for Pads. Use 0 vertex instead.
		
		Note: This need to be improved.
	
##### Args:
	
		iObj: object
		iVertex: vertex object FreeCAD.Vector(x, y, z)
		iPadding: value > 0 for making offset
		iAxis: string: "X" or "Y" or "Z"
		
##### Usage:
	
		v = getattr(obj.Shape, "Vertex"+"es")[0]
		offsetX = MagicPanels.setVertexPadding(obj, v, 15, "X")
		
##### Result:
	
		Return return new position value for given axis.

### getOnCurve(iPoint, iCurve):
	
##### Description:
	
		This function has been created to replace python .index() function. 
		FreeCAD has not rounded float values at Vectors, so if you call 
		iCurve.Shape.getPoints(1)[0].index(vector_of_iPoint) this may not find the index 
		of vector_of_iPoint at the iCurve not because it is not there, but because there is 
		small not rounded difference, for example 0.0000006. So, this function scan the iCurve vectors 
		and compare rounded values to return the index.
	
##### Args:
	
		iPoint: Part.Vertex object or FreeCAD.Vector or array of floats like [ x, y, z ]
		iCurve: object that has .getPoints() function, for example Wire, Sketch, Helix, Edge

##### Usage:
	
		index = MagicPanels.getOnCurve(v, Sketch)
		
##### Result:
	
		Return int value index for iPoint on iCurve.

### getVerticesOffset(iVertices, iObj, iType="array"):
	
	Gets iObj offset of all supported containers for vertices iVertices.
	
##### Args:
	
		iObj: object to get containers offset
		iVertices: vertices array
		iType:
			"array" - array with floats [ 1, 2, 3 ]
			"vector" - array with FreeCAD.Vector types
		
##### Usage:
	
		vertices = MagicPanels.getVerticesOffset(vertices, o, "array")

##### Result:
	
		return vertices array with correct container offset

### getVerticesPosition(iVertices, iObj, iType="auto"):
	
##### Description:
	
		Gets iVertices 3D position. This function should be used to show or select iVertices with rotation. 
		It calculates all offsets with rotation. But this function should not be used for calculation. 
		Because the vertices at FreeCAD are raw, without containers offset. The vertices at FreeCAD have only 
		AttachmentOffset applied. If you start calculation with rotation, you need to calculate plane correctly.
	
##### Args:
	
		iVertices: vertices array
		iObj: object to get containers offset
		iType:
			"auto" - recognize the iVertices elements type
			"array" - each element of iVertices is array with floats [ 1, 2, 3 ]
			"vector" - each element of iVertices is array with FreeCAD.Vector
			"vertex" - each element of iVertices is array with Part.Vertex

##### Usage:
	
		[[ x, y, z ]] = MagicPanels.getVerticesPosition([[ x, y, z ]], o, "array")
		vertices = MagicPanels.getVerticesPosition(vertices, o, "vector")
		vertices = MagicPanels.getVerticesPosition(vertices, o)
		
		MagicPanels.showVertex(vertices, 10)

##### Result:
	
		return vertices array with correct container offset, with the same type

### removeVerticesPosition(iVertices, iObj, iType="auto"):
	
##### Description:
	
		Remove iVertices 3D position. This function removes offset calculated with getVerticesPosition.
	
##### Args:
	
		iVertices: vertices array
		iObj: object to remove containers offset
		iType:
			"auto" - recognize the iVertices elements type
			"array" - each element of iVertices is array with floats [ 1, 2, 3 ]
			"vector" - each element of iVertices is array with FreeCAD.Vector
			"vertex" - each element of iVertices is array with Part.Vertex

##### Usage:
	
		[[ x, y, z ]] = MagicPanels.removeVerticesPosition([[ x, y, z ]], o, "array")
		vertices = MagicPanels.removeVerticesPosition(vertices, o, "vector")
		vertices = MagicPanels.removeVerticesPosition(vertices, o)
		
		MagicPanels.showVertex(vertices, 10)

##### Result:
	
		return vertices array without container offset, with the same type


# Direction, Plane, Orientation, Axis

### isRotated(iObj):
	
##### Description:
	
		Function to check if object iObj is rotated or not.

##### Args:
	
		iObj: object to check rotation

##### Usage:
	
		if MagicPanels.isRotated(o):

##### Result:
	
		Return True if the object is rotated or False otherwise.

### addRotation(iObj, iTarget):
	
##### Description:
	
		This function checks if the iObj is rotated and add the rotation to the iTarget objects.

##### Args:
	
		iObj: object to check rotation
		iTarget: array with objects to set rotation

##### Usage:
	
		MagicPanels.addRotation(base, [ o ]):

##### Result:
	
		If the iObj is rotated, set the same rotation to iTarget

### getModelRotation(iX, iY, iZ):
	
##### Description:
	
		Transform given iX, iY, iZ values to the correct vector, if the user rotated 3D model.

##### Args:
	
		iX: X value to transform
		iY: Y value to transform
		iY: Z value to transform

##### Usage:
	
		[x, y, z ] = MagicPanels.getModelRotation(x, y, z)

##### Result:
	
		[ X, Y, Z ] - transformed vector of given values

### getDirection(iObj):
	
##### Description:
	
		Allows to get Cube object direction (iType).
	
##### Args:
	
		iObj: selected object

##### Usage:
	
		direction = MagicPanels.getDirection(obj)

##### Result:
	
		Returns iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"


# Position, Placement, Move

### getOffset(iObj, iDestination, iType="array"):
	
##### Description:
	
		This function returns offset for setPosition function.
	
##### Args:
	
		iObj: object to get offset
		iDestination: global destination point
		iType (optional): iDestination type
			* "array": the iDestination will be [ float, float, float ]
			* "vector": the iDestination will be FreeCAD.Vector type [ .x, .y, .z ]
			* "vertex": the iDestination will be Vertex type [ .X, .Y, .Z ]

##### Usage:
	
		[ offetX, offetY, offetZ ] = MagicPanels.getOffset(o, [ 100, 200, 0 ], "array")
		[ offetX, offetY, offetZ ] = MagicPanels.getOffset(o, edge.CenterOfMass, "vector")

##### Result:
	
		return array with offsets [ offetX, offetY, offetZ ]

### getPosition(iObj, iType="global"):
	
##### Description:
	
		This function returns placement for the object to move or copy without rotation.
	
##### Args:
	
		iObj: object to get placement
		iType (optional): 
			"global": trying to calculate global position of the object, make sure the object is currently supported
			"local": return iObj.Placement

##### Usage:
	
		[ x, y, z ] = MagicPanels.getPosition(o, "global")
		[ x, y, z ] = MagicPanels.getPosition(o, "local")

##### Result:
	
		return [ x, y, z ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position

### setPosition(iObj, iX, iY, iZ, iType="offset"):
	
##### Description:
	
		This function set object position to move or copy without rotation.
		
##### Args:

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
		
##### Usage:
	
		MagicPanels.setPosition(copy, 100, 0, 0, "offset")
		MagicPanels.setPosition(copy, 100, 0, 0, "local")
		MagicPanels.setPosition(copy, 100, 0, 0, "global")

##### Result:
	
		return empty string if everything was fine or string with error info

### getObjectToMove(iObj):
	
##### Description:
	
		This function returns object to move.
	
##### Args:
	
		iObj: object to get reference to move

##### Usage:
	
		toMove = MagicPanels.getObjectToMove(o)

##### Result:
	
		For example: 

		for Cube: always returns Cube
		for Pad: always returns Body
		for PartDesign objects: try to return Body
		for LinkGroup: returns LinkGroup
		for Cut: returns Cut
		for any other object: returns object

### getObjectCenter(iObj):
	
##### Description:
	
		Returns center of the object.
	
		Note: This function will be updated later with more reliable 
		way of getting center of the object, also for LinkGroup and other containers. 
		Now it returns Shape.CenterOfMass for the object and it is not the same 
		as center of the object.
	
##### Args:
	
		iObj: object

##### Usage:
	
		[ cx, cy, cz ] = MagicPanels.getObjectCenter(obj)

##### Result:
	
		Returns array with [ cx, cy, cz ] values for center point.


# Containers

### createContainer(iObjects, iLabel="Container", iNesting=True):
	
##### Description:
	
		This function creates container for given iObjects. The label for new container will be get from 
		first element of iObjects (iObjects[0]).
	
##### Args:
	
		iObjects: array of object to create container for them
		iLabel: string, container label
		iNesting: boolean, add nesting label prefix (True) or set given label (False)

##### Usage:
	
		container = MagicPanels.createContainer([c1, c2])
		container = MagicPanels.createContainer([c1, c2], "LinkGroup")
		container = MagicPanels.createContainer([o1, o2, o3, o4, o5, o6, o7], "Furniture, Module", False)

##### Result:
	
		Created container and objects inside the container, return container object.

### getContainersPath(iObj):
	
##### Description:
	
		This function returns string with path to object in this way: LinkGroup.Part.Body.Pad
		
	
##### Args:
	
		iObj: object to get path

##### Usage:
	
		path = MagicPanels.getContainersPath(o)

##### Result:
	
		return string

### getContainers(iObj):
	
##### Description:
	
		This function get list of containers for given iObj.
		
	
##### Args:
	
		iObj: object to get list of containers

##### Usage:
	
		containers = MagicPanels.getContainers(o)

##### Result:
	
		return array with objects

### moveToContainer(iObjects, iContainer, iType="object"):
	
##### Description:

		Move objects iObjects to iContainer.

##### Args:
	
		iObjects: list of objects to move to iContainer, for example new created Cube
		iContainer: container object or string describing destination level, possible:
			iContainer: object for example LinkGroup or Pad to search
			"object": move all iObjects directly to given iContainer object
			"parent": move all iObjects to first container above Body, for example Part for given iContainer
			"LinkGroup": move all iObjects to first LinkGroup container above given iContainer

##### Usage:

		For Pad structure: "LinkGroup2 -> LinkGroup1 -> Part -> Body -> Pad"
		and copy object is in root folder. 
		
		MagicPanels.moveToContainer([ copy ], LinkGroup2)            # to move copy object to LinkGroup2
		MagicPanels.moveToContainer([ copy ], LinkGroup2, "object")  # to move copy object to LinkGroup2
		MagicPanels.moveToContainer([ copy ], Pad, "parent")         # to move copy object to Part
		MagicPanels.moveToContainer([ copy ], Pad, "LinkGroup")      # to move copy object to LinkGroup1

##### Result:

		No return, move object.

### moveToFirst(iObjects, iSelection):
	
##### Description:

		Move objects iObjects to first LinkGroup container for iSelection object.
		
		Note: This function removes the offset that should have been added earlier. Why not just copy without offset?
		If you have 2 objects in separate containers and the second object is only moved via the container Placement, 
		then from FreeCAD point the objects are in the same place. So you won't be able to compute space between 
		objects in these containers. FreeCAD uses local positions. It's good because you can calculate many things 
		without using advanced formulas. Adding an offset and removing it later is a trick for easier calculations.

		You can convert all vertices to global, but in this case you won't be able to determine the plane correctly 
		in an easy way, for example the vertices on an edge would no longer be along the same coordinate axis, 
		and thus you'd have to use advanced formulas. It can be done with a trick, but maybe something like 
		that will come along later if need be.

##### Args:
	
		iObjects: list of objects to move to container, for example [ copy1, copy2 ]
		iSelection: selected object, for example "PartDesign::Pad" with structure "LinkGroup2 -> LinkGroup1 -> Part -> Body -> Pad" or "Part::Box" in structure "LinkGroup2 -> LinkGroup1 -> panelXY", to move the object to LinkGroup1

##### Usage:

		MagicPanels.moveToFirst([ copy ], pad)
		MagicPanels.moveToFirst([ copy ], panel)

##### Result:

		No return, move copy object to LinkGroup1 container.

### getNestingLabel(iObj, iPrefix):
	
##### Description:
	
		This function set label for nesting objects, containers, copied, to not repeat 
		the prefix and not make the label too long. 
	
##### Args:
	
		iObj: object for the label check
		iPrefix: string, preferred prefix for the label

##### Usage:
	
		o.Label = MagicPanels.getNestingLabel(o, "Container")

##### Result:
	
		return string for the new label

### getContainersOffset(iObj):
	
##### Description:
	
		If the object is in the container like Part, Body, LinkGroup the vertices are 
		not updated by FreeCAD. From FreeCAD perspective the object is still in the 
		same place. This function is trying to solve this problem and calculates 
		all offsets of all containers.
	
##### Args:
	
		iObj: object to get containers offset

##### Usage:
	
		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(o)

##### Result:
	
		return [ coX, coY, coZ, coR ] array with offsets for placement:
		
		coX: X Axis object position
		coY: Y Axis object position
		coZ: Z Axis object position
		coR: Rotation object

### getPlacementDiff(iStart, iDestination):
	
##### Description:
	
		Return diff that should be added to iStart to move object from iStart to iDestination position. 
		If you want to move back you can minus the diff from iDestination.
		
##### Args:
	
		iStart: start vertex float value
		iDestination: destination vertex float value
	
##### Usage:
		
		[ moveX, moveY, moveZ ] = MagicPanels.getPlacementDiff(v1, v2)
		
##### Result:
	
		Return [ moveX, moveY, moveZ ] array with X, Y, Z floats to move object.

### isVisible(iObj):
	
##### Description:
	
		Returns object visibility, even if object is visible but inside the hidden LinkGroup container.
		
##### Args:
	
		iObj: object to search visibility

##### Usage:
		
		visible = MagicPanels.isVisible(iObj)
		
##### Result:
	
		Return boolean True or False
### toggleVisibility(iObj):
	
##### Description:
	
		Toggle object visibility.
		
##### Args:
	
		iObj: object to toggle visibility

##### Usage:
		
		MagicPanels.toggleVisibility(old)
		
##### Result:
	
		no return

# Conversion

### convertPosition(iObj, iX, iY, iZ):
	
##### Description:
	
		Convert given position vector to correct position values according 
		to the object direction.
	
##### Args:
	
		iObj: object
		iX: x position
		iY: y position
		iZ: z position

##### Usage:
	
		[ x, y, z ] = MagicPanels.convertPosition(obj, 0, 400, 0)

##### Result:
	
		For Pad object in XZ direction return the AttachmentOffset order [ 0, 0, -400 ]

### sizesToCubePanel(iObj, iType):
	
##### Description:
	
		Converts selected object (iObj) sizes to Cube panel sizes into given direction (iType). 
		So, the returned values can be directly assigned to Cube object in order to create 
		panel in exact direction.

##### Args:

		iObj: selected object
		iType direction: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

##### Usage:

		[ Length, Width, Height ] = MagicPanels.sizesToCubePanel(obj, "YZ")

##### Result:

		Returns [ Length, Width, Height ] for YZ object placement.


# Replace

### makePad(iObj, iPadLabel="Pad"):
	
##### Description:
	
		Allows to create Part, Plane, Body, Pad, Sketch objects.
	
##### Args:
	
		iObj: object Cube to change into Pad
		iPadLabel: Label for the new created Pad, the Name will be Pad

##### Usage:

		[ part, body, sketch, pad ] = MagicPanels.makePad(obj, "myPanel")

##### Result:
	
		Created Pad with correct placement, rotation and return [ part, body, sketch, pad ].


# Measurements

### showMeasure(iP1, iP2, iRef=""):
	
##### Description:
	
		Creates measurements object, I mean draw it. Now it use FreeCAD function 
		to create and draw object. But in the future this can be changed to 
		more beautiful drawing without changing tools. 
	
##### Args:
	
		iP1: starting point vertex object
		iP2: ending point vertex object
		iRef (optional): string for future TechDraw import or any other use, other tools

##### Usage:
	
		m = MagicPanels.showMeasure(gP1, gP2, "Pad")

##### Result:
	
		Create measure object, draw it and return measure object for further processing. 

### getDistanceBetweenFaces(iObj1, iObj2, iFace1, iFace2):
	
##### Description:
	
		Gets distance between iFace1 and iFace2.
	
##### Args:
	
		iObj1: object of iFace1
		iObj2: object of iFace2
		iFace1: face object
		iFace2: face object

##### Usage:
	
		size = MagicPanels.getDistanceBetweenFaces(o1, o2, face1, face2)

##### Result:

		return distance between face1 object and face2 object


# Units

### unit2gui(iValue):
	
##### Description:
	
		Allows to convert unit from value (mm float FreeCAD format) into gui user settings.

##### Args:

		iValue: float from FreeCAD or from calculations
		
##### Usage:

		unitForUser = MagicPanels.unit2gui(300.55)
		
		# Note: if user has set inches units the unitForUser should contains recalculation to inches 
		
##### Result:

		string

### unit2value(iString):
	
##### Description:
	
		Allows to convert user unit string into float for calculation. 

##### Args:

		iString: units string in user settings notation, for example "5 mm", "5 in", "5 ft", 
		but also accept quick value notation like "500" for all units schemas.
		
##### Usage:
		
		forCalculation = MagicPanels.unit2value("18 mm")
		forCalculation = MagicPanels.unit2value("0.06 ft") # forCalculation will be 18.288
		forCalculation = MagicPanels.unit2value("18")
		forCalculation = MagicPanels.unit2value("0")

##### Result:

		float for calculation

### unitArea2gui(iValue):
	
##### Description:
	
		Allows to convert area value (mm float FreeCAD format) into gui user settings.

##### Args:

		iValue: float from FreeCAD or from calculations
		
##### Usage:

		areaString = MagicPanels.unitArea2gui(180000)

##### Result:

		string, for example "180000 mm^2"

### unit2fractions(iValue, iPrecision=0, iReduction="no", iPrefix=""):
	
##### Description:
	
		Allows to convert unit from value (mm float FreeCAD format) into fractions string X' Y n/d" or X' Y-n/d". 
		X' represents a whole number of feet. Y represents a whole number of inches and n/d" represents 
		a fraction of an inch, where n is the numerator and d is the denominator.
		
		Note: This function not reduce fraction part by default (keeps the denominator the same as given iPrecision).

##### Args:

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
		
##### Usage:

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

##### Result:

		string for GUI


# Colors

### convertColor(iColor, iTarget):
	
##### Description:
	
		Converts colors.

##### Args:

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

##### Usage:

		color = MagicPanels.convertColor([ 247, 185, 108, 255 ], "kernel")
		
		colorTuple = (0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 1.0)
		color = MagicPanels.convertColor(colorTuple, "RGBA")
		
		colorArray = [ 0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 1.0 ]
		color = MagicPanels.convertColor(colorArray, "RGBA")
		
		color = MagicPanels.convertColor(obj.ViewObject.DiffuseColor, "RGBA")

##### Result:

		returns converted color

### getColor(iObj, iFaceIndex, iAttribute="color", iType="kernel"):
	
##### Description:
	
		Allows to get color for object or face.

##### Args:

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

##### Usage:

		colorTuple = MagicPanels.getColor(o, 0, "color") # to get object color
		colorTuple = MagicPanels.getColor(o, 5, "color") # to get face5 color
		
		[ r, g, b, a ] = MagicPanels.getColor(o, 0, "color", "RGBA") # to get object color
		[ r, g, b, a ] = MagicPanels.getColor(o, 5, "color", "RGBA") # to get face5 color

##### Result:

		Returns color in desired format or empty string.
		
		For FreeCAD 0.21.2 returns color for object from .ViewObject.ShapeColor or 
		color for face from .ViewObject.DiffuseColor.
		
		Since FreeCAD 1.0+ there is no .ViewObject.ShapeColor for object. Color for object 
		and faces are stored only at .ViewObject.ShapeAppearance behind FreeCAD.Material 
		structure. If all the faces have the same color there is only one Material object. 
		But for example if only single face have different color, there are Material objects 
		for all faces, but there is no color for object. So in this case the color for 
		object cannot be determined, so will be returned as empty string "". 

### setColor(iObj, iFaceIndex, iColor, iAttribute="color", iType="kernel"):
	
##### Description:
	
		Allows to set color for object or face.

##### Args:

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

##### Usage:

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

##### Result:

		return empty string if everything is fine or string with error info

### copyColors(iSource, iTarget):
	
##### Description:
	
		Allows to copy colors from iSource object to iTarget object.

##### Args:

		iSource: source object
		iTarget: target object

##### Usage:

		MagicPanels.copyColors(panel, copy)

##### Result:

		All colors structure should be copied from source to target.


# Holes

### makeHoles(iObj, iFace, iCylinders, iDrillPoint="Angled"):
	
##### Description:
	
		Making holes.

##### Args:

		iObj: base object to make hole
		iFace: face of base object to make hole
		iCylinders: list of cylinders to make holes below each one
		iDrillPoint (optional): "Angled" for normal conical hole or "Flat" for flat hole
		
##### Usage:

		holes = MagicPanels.makeHoles(obj, face, cylinders)
		holes = MagicPanels.makeHoles(obj, face, cylinders, "Angled")
		holes = MagicPanels.makeHoles(obj, face, cylinders, "Flat")
		
##### Result:

		Make holes and return list of holes.

### makeCountersinks(iObj, iFace, iCones):
	
##### Description:
	
		Making countersinks.

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makeCountersinks(obj, face, cones)

##### Result:

		Make holes and return list of holes. 

### makeCounterbores(iObj, iFace, iCones):
	
##### Description:
	
		Making counterbores.

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makeCounterbores(obj, face, cones)

##### Result:

		Make holes and return list of holes.

### makePocketHoles(iObj, iFace, iCones):
	
##### Description:
	
		Making pocket holes for invisible connections.

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makePocketHoles(obj, face, cones)

##### Result:

		Make holes and return list of holes.

### makeCounterbores2x(iObj, iFace, iCones):
	
##### Description:
	
		Making counterbores from both sides.

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makeCounterbores2x(obj, face, cones)

##### Result:

		Make holes and return list of holes.


# Joinery

### makeCuts(iObjects):
	
##### Description:
	
		Allows to create multi bool cut operation at given objects. First objects 
		from iObjects is the base element and all other will cut the base. 
		The copies will be created for cut. 
	
##### Args:
	
		iObjects: objects to parse by multi bool cut

##### Usage:
	
		cuts = MagicPanels.makeCuts(objects)

##### Result:
	
		Array of cut objects will be returned.

### makeCutsLinks(iObjects):
	
##### Description:
	
		Allows to create multi bool cut operation at given objects. First objects 
		from iObjects is the base element and all other will cut the base. 
		At this function version App::Link is used to create copy.
	
##### Args:
	
		iObjects: objects to parse by multi bool cut

##### Usage:
	
		cuts = MagicPanels.makeCutsLinks(objects)

##### Result:
	
		Array of cut objects will be returned.

### makeFrame45cut(iObjects, iFaces):
	
##### Description:
	
		Makes 45 frame cut with PartDesing Chamfer. For each face the ends will be cut.
	
##### Args:
	
		iObjects: array of objects to cut
		iFaces: dict() of faces for Chamfer cut direction, the key is iObjects value (object), 
				if there are more faces for object, the first one will be get as direction.

##### Usage:
	
		frames = MagicPanels.makeFrame45cut(objects, faces)
		
##### Result:
	
		Created Frames with correct placement, rotation and return array with Chamfer frame objects.

### makeChamferCut(iObjects, iEdges, iSizes, iLabels):
	
##### Description:
	
		Makes PartDesing Chamfer cut for edges array. But you can set different size for each edge. 
		Yes, you give edge objects, and you make chamfer for each edge, one by one, with different 
		size, but the most funny part is that the selected edge not exists because the Cube 
		object not exists ;-)

##### Args:
	
		iObjects: array of objects to cut
		iEdges: dict() of arrays [ edgeObj1, edgeObj2 ], edgeArr = iEdges[iObjects[0]]
		iSizes: dict() of arrays [ 100, 50 ], sizeArr = iSizes[iObjects[0]]
		iLabels: dict() of labels for new object, label = iLabels[iObjects[0]]

##### Usage:
	
		cuts = MagicPanels.makeChamferCut(objects, edges, sizes, labels)
		
##### Result:
	
		return array with chamfer objects

### makeMortise(iSketch, iDepth, iPad, iFace):
	
##### Description:
	
		Make Mortise pocket for given iSketch pattern.

##### Args:

		iSketch: Sketch object as pattern for Mortise
		iDepth: depth of the pocket
		iPad: pad object to get Body
		iFace: face object at the pad where is the iSketch

##### Usage:

		[ obj, face ] = MagicPanels.makeMortise(sketch, 20, obj, face)

##### Result:

		Make Mortise and return new object and face reference for GUI info screen update and further processing

### makeTenon(iSketch, iLength, iPad, iFace):
	
##### Description:
	
		Make Tenon pad for given iSketch pattern.

##### Args:

		iSketch: Sketch object as pattern for Mortise
		iLength: Length for the Tenon pad
		iPad: pad object to get Body
		iFace: face object at the pad where is the iSketch

##### Usage:

		[ obj, face ] = MagicPanels.makeTenon(sketch, 20, obj, face)

##### Result:

		Make Tenon and return new object and face reference for GUI info screen update and further processing


# Router

### getSubByKey(iObj, iKey, iType, iSubType):
	
##### Description:
	
		This is extended version of getEdgeIndexByKey function. 
		This function has been created to solve resized edge problem. If you cut the edge the next 
		edge will change the Length. So, also the BoundBox will be changed. With this function you 
		can customize reference key to solve the Topology Naming Problem.
	
##### Args:
	
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
	
##### Description:
	
		Returns Rotation object which can be passed directly to setSketchPlacement 
		functions. The Sketch will be perpendicular to the iSub object, so it can be used as 
		router bit to cut the edge or face.
	
##### Args:
	
		iObj: object for sub-object
		iSub: selected sub-object, edge or face

##### Usage:
	
		r = MagicPanels.getSketchPatternRotation(o, edge)
		r = MagicPanels.getSketchPatternRotation(o, face)

##### Result:
	
		return FreeCAD.Rotation object.

### edgeRouter(iPad, iSub, iSketch, iLength, iLabel, iType):
	
##### Description:
	
		This function is router for the edge. It cut the 
		iSub with iSketch pattern. The new object will get iLabel label.
	
##### Args:
	
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
	
##### Description:
	
		This function is multi Pocket. First object from iObjects will be base
		object to Pocket, all others should be Sketches. The Length is depth for Pocket. 
		If the Length is 0 the Pocket will be ThroughAll.
	
##### Args:
	
		iObjects: First base objects, next sketches
		iLength: length to cut, float or int value, 0 means ThroughAll
		
##### Usage:
	
		pocket = MagicPanels.makePockets(selectedObjects, 0)

##### Result:
	
		return last pocket object, the result of cut


# Spreadsheet

### sheetGetKey(iC, iR):
	
##### Description:
	
		Allows to get key as letters for spreadsheet from given column and row index.

##### Args:
	
		iC: column index
		iR: row index

##### Usage:
	
		key = MagicPanels.sheetGetKey(1, 2)

##### Result:
	
		return key string


# Themes

### getTheme(iType=""):
	
##### Description:
	
		Allows to set GUI color theme. 

##### Args:
	
		iType: color theme reference name
		
##### Usage:

		# to return Qt CSS string
		QtCSS = MagicPanels.getTheme("classic")
		QtCSS = MagicPanels.getTheme("lavender")
		self.setStyleSheet(QtCSS)
		
		# to return list of available themes
		self.sModeList = MagicPanels.getTheme("config")
		self.sMode = QtGui.QComboBox(self)
		self.sMode.addItems(self.sModeList)

##### Result:
	
		return Qt CSS string to set via self.setStyleSheet(QtCSS)


# Info screen

### showInfo(iCaller, iInfo, iNote="yes"):

# DEPRECATED

### moveToParent(iObjects, iSelection):
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		This version move object to parent container without adding or remove offset. This is useful if you copy the 
		Sketch, because Sketch after copy is located outside Body, in Part. But if the Part is inside LinkGroup 
		the copied Sketch will be located outside LinkGroup, in main root folder. This is problematic because 
		the Sketch after copy has offset from containers. The object to move need to be in root folder to avoid 
		duplicated already copied objects, Cube.
	
##### Args:
	
		iObjects: list of objects to move to container, for example new created Sketch
		iSelection: selected object, for example Sketch

##### Usage:
	
		MagicPanels.moveToParent([ copy ], sketch)

##### Result:
	
		No return, move object.

### moveToClean(iObjects, iSelection):
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		Move objects iObjects to clean container for iSelection object.
		Container need to be in the clean path, no other objects except Group or LinkGroup, 

		For example:

		clean path: LinkGroup -> LinkGroup
		not clean: Mirror -> LinkGroup
	
##### Args:
	
		iObjects: list of objects to move to container, for example new created Cube
		iSelection: selected object, for example Pad

##### Usage:
	
		MagicPanels.moveToClean([ o ], pad)

##### Result:
	
		No return, move object.

### moveToFirstWithInverse(iObjects, iSelection):
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		This version remove the placement and rotation offset from iObjects and move the iObjects to first 
		supported container (LinkGroup). 
		
		Note: It is dedicated to move panel created from vertices to the first LinkGroup container. 
		The object created from vertices have applied offset with rotation after creation 
		but is outside the container. So if you move it manually it will be in the wrong place because 
		container apply the placement and rotation again. So, you have to remove the offset and move it. 
		Yea, that's the beauty of FreeCAD ;-)
	
##### Args:
	
		iObjects: list of objects to move to container, for example new created Cube
		iSelection: selected object, for example Pad

##### Usage:
	
		MagicPanels.moveToFirstWithInverse([ o ], pad)

##### Result:
	
		No return, move object.

### adjustClonePosition(iPad, iX, iY, iZ):
	
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		This function has been created for magicMove tool to adjust Clone position.
		If you make Clone from Pad and the Pad has not zero Sketch.AttachmentOffset, 
		the Clone has Placement set to XYZ (0,0,0) but is not in the zero position. 
		So you have to remove Sketch offset from the Clone position. 
		I guess the BoundBox is the correct solution here.
	
##### Args:
	
		iPad: Pad object with not zero Sketch.AttachmentOffset used to create new Clone
		iX: X Axis object position
		iY: Y Axis object position
		iZ: Z Axis object position

##### Usage:
	
		[ x, y, z ] = MagicPanels.adjustClonePosition(o, x, y, z)

##### Result:
	
		Returns array with new correct [ x, y, z ] values.

### resetPlacement(iObj):
	
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		Reset placement for given object. Needed to set rotation for object at face.
	
##### Args:
	
		iObj: object to reset placement

##### Usage:
	
		MagicPanels.resetPlacement(obj)

##### Result:
	
		Object obj return to base position.

### getPlacement(iObj, iType="clean"):
	
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		Gets placement with rotation info for given object.
		Note: This is useful if you not use containers. 
	
##### Args:
	
		iObj: object to get placement
		iType: 
			* "clean" - old way good for simple objects but it not works if the object has AttachmentOffset set or there are multiple Pads and only the first one has AttachmentOffset set
			* "BoundBox" - return [ XMin, YMin, ZMin ] from object BoundBox, this way solves the problem with AttachmentOffset but you need to be careful, but if the object has containers offset, for example Placement set at Part, Body or LinkGroups additionally you have to add the containers offset, also there will be problem with additional rotation

##### Usage:
	
		[ x, y, z, r ] = MagicPanels.getPlacement(o)
		[ x, y, z, r ] = MagicPanels.getPlacement(o, "clean")
		[ x, y, z, r ] = MagicPanels.getPlacement(o, "BoundBox")

##### Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

### getGlobalPlacement(iObj, iType="FreeCAD"):
	
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		Calls FreeCAD getGlobalPlacement at base object, and return useful form of placement.
	
##### Args:
	
		iObj: object to get placement
		iType:
			* "FreeCAD" - return getGlobalPlacement for object or for Sketch if iObj is Pad 
			* "BoundBox" - return [ XMin, YMin, ZMin ] from BoundBox
##### Usage:
	
		[ x, y, z, r ] = MagicPanels.getGlobalPlacement(o)
		[ x, y, z, r ] = MagicPanels.getGlobalPlacement(o, "BoundBox")

##### Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

### setPlacement(iObj, iX, iY, iZ, iR, iAnchor=""):
	
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		Sets placement with rotation for given object.
	
##### Args:

		iObj: object to set custom placement and rotation
		iX: X Axis object position
		iY: Y Axis object position
		iZ: Z Axis object position
		iR: Rotation object
		iAnchor="" (optional): anchor for placement instead of 0 vertex, FreeCAD.Vector(x, y, z)

##### Usage:
	
		MagicPanels.setPlacement(gObj, 100, 100, 200, r)

##### Result:
	
		Object gObj should be moved into 100, 100, 200 position without rotation.

### getSketchPlacement(iSketch, iType):
	
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		Gets placement dedicated to move and copy Sketch directly.
	
##### Args:
	
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
	
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		Set placement with rotation dedicated to move and copy Sketch directly.
	
##### Args:

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

##### Usage:
	
		MagicPanels.setSketchPlacement(sketch, 100, 100, 200, r, "global")

##### Result:
	
		Object Sketch should be moved.

### getContainerPlacement(iObj, iType="clean"):
	
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		This function returns placement for the object with all 
		containers offsets or clean. The given object might be container or 
		selected object, the base Cube or Pad.
	
##### Args:
	
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

### setContainerPlacement(iObj, iX, iY, iZ, iR, iAnchor="normal"):
	
	
	# ########################################################################################
	# THIS FUNCTION IS DEPRECATED !!!
	# ########################################################################################
	
##### Description:
	
		Set placement function, especially used with containers.
	
##### Args:

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

##### Usage:
		
		MagicPanels.setContainerPlacement(cube, 100, 100, 200, 0, "clean")
		MagicPanels.setContainerPlacement(pad, 100, 100, 200, 0, "normal")
		MagicPanels.setContainerPlacement(body, 100, 100, 200, 0, "center")

##### Result:
	
		Object should be moved into 100, 100, 200 position with exact anchor.


# Functions for MagicPanels library config

### updateGlobals():
	
##### Description:
	
		This function update MagicPanels library globals from user settings.
	
##### Args:
		none, user config may not exist, so should not be direct assign
		
##### Usage:
	
		MagicPanels.updateGlobals()

##### Result:
	
		there is no return, just overwrite all MagicPanels globals from user config

# UPDATE GLOBALS HERE AFTER FUNCTIONS LOADED
