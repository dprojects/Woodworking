
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


gRoundPrecision = 2 # should be set according to the user FreeCAD GUI settings


# Functions for general purpose
### equal(iA, iB):

	equal(iA, iB) - At FreeCAD there are many values like 1.000006, especially for PartDesign objects. 
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

	touchTypo(iObj) - touch the typo so that the typo-snake does not notice it ;-) LOL
	
##### Args:
	
		iObj: object to touch

##### Usage:
	
		vs = MagicPanels.touchTypo(o)

##### Result:
	
		return Vertex + es for object o

### normalizeBoundBox(iBoundBox):

	normalizeBoundBox(iBoundBox) - return normalized version of BoundBox. All values 0.01 will be rounded 
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

# Vertices
### showVertex(iVertex, iRadius):

	showVertex(iVertex) - create sphere at given vertex, to show where is the point for debug purposes.
	
##### Args:
	
		iVertex: vertex object
		iRadius: ball Radius

##### Usage:
	
		MagicPanels.showVertex(obj.Shape.CenterOfMass, 20)

##### Result:
	
		show vertex
### getVertex(iFace, iEdge, iVertex):

	getVertex(iFace, iEdge, iVertex) - get vertex values for face, edge and vertex index.
	
##### Args:
	
		iFace: face object
		iEdge: edge array index
		iVertex: vertex array index (0 or 1)

##### Usage:
	
		[ x, y, z ] = MagicPanels.getVertex(gFace, 0, 1)

##### Result:

		Return vertex position.

### getVertexAxisCross(iA, iB):

	getVertexAxisCross(iA, iB) - get (iB - iA) value.
	
##### Args:
	
		iA: vertex float value
		iB: vertex float value
	
##### Usage:
	
		edgeSize = MagicPanels.getVertexAxisCross(v0[0], v1[0])
		
##### Result:
	
		Return diff for vertices values.

### getVerticesPlane(iV1, iV2):

	getVerticesPlane(iV1, iV2) - get axes with the same values
	
##### Args:
	
		iV1: vertex object
		iV2: vertex object
	
##### Usage:
	
		plane = MagicPanels.getVerticesPlane(v1, v2)
		
##### Result:
	
		Return plane as "XY", "XZ", "YZ".

### setVertexPadding(iObj, iVertex, iPadding, iAxis):

	setVertexPadding(iObj, iVertex, iPadding, iAxis) - set padding offset from given vertex to inside the object.
	Do not use it at getPlacement for Pads. Use 0 vertex instead.
	
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

# Edges
### getEdgeVertices(iEdge):

	getEdgeVertices(iEdge) - get all vertices values for edge.
	
##### Args:
	
		iEdge: edge object

##### Usage:
	
		[ v1, v2 ] = MagicPanels.getEdgeVertices(gEdge)

##### Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 1, 1, 1 ] ].

### getEdgeNormalized(iV1, iV2):

	getEdgeNormalized(iV1, iV2) - returns vertices with exact sorted order V1 > V2, mostly used 
	to normalize Pad vertices
	
##### Args:
	
		iV1: array with vertices e.g. [ 1, 1, 1 ]
		iV2: array with vertices e.g. [ 2, 2, 2 ]
	
##### Usage:
	
		[ v1, v2 ] = MagicPanels.getEdgeNormalized(v1, v2)
		
##### Result:
	
		for vertices [ 2, 2, 2 ], [ 1, 1, 1 ] return [ 1, 1, 1 ], [ 2, 2, 2 ]

### getEdgeIndex(iObj, iEdge):

	getEdgeIndex(iObj, iEdge) - returns edge index for given object and edge.
	
##### Args:
	
		iObj: object of the edge
		iEdge: edge object

##### Usage:
	
		edgeIndex = MagicPanels.getEdgeIndex(gObj, gEdge)

##### Result:
	
		return int value for edge

### getEdgeIndexByKey(iObj, iBoundBox):

	getEdgeIndexByKey(iObj, iBoundBox) - returns edge index for given edge BoundBox.
	
##### Args:
	
		iObj: object of the edge
		iBoundBox: edge BoundBox as key

##### Usage:
	
		edgeIndex = MagicPanels.getEdgeIndex(o, key)

##### Result:
	
		return int value for edge

### getEdgePlane(iEdge):

	getEdgePlane(iEdge) - returns orientation for the edge, changed axis, as "X", "Y" or "Z".
	
##### Args:
	
		iEdge: edge object

##### Usage:
	
		plane = MagicPanels.getEdgePlane(edge)

##### Result:
	
		return string "X", "Y" or "Z".

# Router
### getSubByKey(iObj, iKey, iType, iSubType):

	getSubByKey(iObj, iKey, iType, iSubType) - this is extended version of getEdgeIndexByKey function. 
	This function has been created to solve resized edge problem. If you cut the edge the next edge will 
	change the Length. So, also the BoundBox will be changed. With this function you can customize 
	reference key to solve the Topology Naming Problem.
	
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

	getSketchPatternRotation(iObj, iSub) - returns Rotation object which can be passed directly to setSketchPlacement 
	functions. The Sketch will be perpendicular to the iSub object, so it can be used as router bit to cut the 
	edge or face.
	
##### Args:
	
		iObj: object for sub-object
		iSub: selected sub-object, edge or face

##### Usage:
	
		r = MagicPanels.getSketchPatternRotation(o, edge)
		r = MagicPanels.getSketchPatternRotation(o, face)

##### Result:
	
		return FreeCAD.Rotation object.

### edgeRouter(iPad, iSub, iSketch, iLength, iLabel, iType):

	edgeRouter(iPad, iSub, iSketch, iLength, iLabel, iType) - this function is router for the edge. It cut the 
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

	makePockets(iObjects, iLength) - this function is multi Pocket. First object from iObjects will be base
	object to Pocket, all others should be Sketches. The Length is depth for Pocket. If the Length is 0 
	the Pocket will be ThroughAll.
	
##### Args:
	
		iObjects: First base objects, next sketches
		iLength: length to cut, float or int value, 0 means ThroughAll
		
##### Usage:
	
		pocket = MagicPanels.makePockets(selectedObjects, 0)

##### Result:
	
		return last pocket object, the result of cut

# Faces
### getFaceIndex(iObj, iFace):

	getFaceIndex(iObj, iFace) - returns face index for given object and face.
	
##### Args:
	
		iObj: object of the face
		iFace: face object

##### Usage:
	
		faceIndex = MagicPanels.getFaceIndex(gObj, gFace)

##### Result:
	
		return int value for face

### getFaceIndexByKey(iObj, iBoundBox):

	getFaceIndexByKey(iObj, iBoundBox) - returns face index for given face BoundBox.
	
##### Args:
	
		iObj: object of the face
		iBoundBox: face BoundBox as key

##### Usage:
	
		faceIndex = MagicPanels.getFaceIndexByKey(o, key)

##### Result:
	
		return int value for face

### getFaceVertices(iFace, iType="4"):

	getFaceVertices(iFace, iType="4") - get all vertices values for face.
	
##### Args:
	
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

	getFaceType(iObj, iFace) - get face type, if this is "edge" or "surface".
	
##### Args:
	
		iObj: object where is the face
		iFace: face object

##### Usage:
	
		faceType = MagicPanels.getFaceType(gObj, gFace)

##### Result:
	
		Return string "surface" or "edge".

### getFaceEdges(iObj, iFace):

	getFaceEdges(iObj, iFace) - get all edges for given face grouped by sizes.
	
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

	getFacePlane(iFace) - get face plane in notation "XY", "XZ", "YZ". 

##### Args:
	
		iFace: face object

##### Usage:
	
		plane = MagicPanels.getFacePlane(face)

##### Result:
	
		string "XY", "XZ", or "YZ".
		
### getFaceSink(iObj, iFace):

	getFaceSink(iObj, iFace) - get face sink axis direction in notation "+", or "-".

##### Args:
	
		iObj: object with the face
		iFace: face object

##### Usage:
	
		sink = MagicPanels.getFaceSink(obj, face)

##### Result:
	
		string "+" if the object at face should go along axis forward, 
		or "-" if the object at face should go along axis backward

### getFaceObjectRotation(iObj, iFace):

	getFaceObjectRotation(iObj, iFace) - get face object rotation to apply to the new created object at face. 
	Object created at face with this rotation should be up from the face.

##### Args:
	
		iObj: object with the face
		iFace: face object

##### Usage:
	
		r = MagicPanels.getFaceObjectRotation(obj, face)

##### Result:
	
		FreeCAD.Rotation object that can be directly pass to the setPlacement or object.Placement

### getFaceDetails(iObj, iFace):

	getFaceDetails(iObj, iFace) - allow to get detailed information for face direction.
	
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
		
# References
### getReference(iObj="none"):

	getReference(iObj="none") - get reference to the selected or given object.
	
##### Args:
	
		iObj (optional): object to get reference (to return base object)
	
##### Usage:
	
		gObj = MagicPanels.getReference()
		gObj = MagicPanels.getReference(obj)
		
##### Result:
	
		gObj - reference to the base object

# Sizes
### getSizes(iObj):

	getSizes(iObj) - allow to get sizes for object (iObj), according to the object type. The values are not sorted.
	
##### Args:
	
		iObj: object to get sizes

##### Usage:
	
		[ size1, size2, size3 ] = MagicPanels.getSizes(obj)

##### Result:
	
		Returns [ Length, Width, Height ] for Cube.

### getSizesFromVertices(iObj):

	getSizesFromVertices(iObj) - get occupied space by the object from vertices.
	
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

	getSizesFromBoundBox(iObj) - get occupied space by the object from BoundBox. This can be useful for round shapes, 
	where is no vertices at object edges, e.g. cylinders, circle at Sketch.
	
##### Args:
	
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

	showMeasure(iP1, iP2, iRef="") - create measurements object, I mean draw it. Now it use FreeCAD function 
	to create and draw object. But in the future this can be changed to more beautiful drawing without changing
	tools. 
	
##### Args:
	
		iP1: starting point vertex object
		iP2: ending point vertex object
		iRef (optional): string for future TechDraw import or any other use, other tools

##### Usage:
	
		m = MagicPanels.showMeasure(gP1, gP2, "Pad")

##### Result:
	
		Create measure object, draw it and return measure object for further processing. 

### getDistanceBetweenFaces(iFace1, iFace2):

	getDistanceBetweenFaces(iFace1, iFace2) - get distance between iFace1 and iFace2
	
##### Args:
	
		iFace1: face object
		iFace2: face object

##### Usage:
	
		size = MagicPanels.getDistanceBetweenFaces(face1, face2)

##### Result:

		return distance between face1 object and face2 object

# Direction, Plane, Orientation, Axis
### getModelRotation(iX, iY, iZ):

	getModelRotation() - transform given iX, iY, iZ values to the correct vector, if the user rotated 3D model.

##### Args:
	
		iX: X value to transform
		iY: Y value to transform
		iY: Z value to transform

##### Usage:
	
		[x, y, z ] = MagicPanels.getModelRotation(x, y, z)

##### Result:
	
		[ X, Y, Z ] - transformed vector of given values

### getDirection(iObj):

	getDirection(iObj) - allow to get Cube object direction (iType).
	
##### Args:
	
		iObj: selected object

##### Usage:
	
		direction = MagicPanels.getDirection(obj)

##### Result:
	
		Returns iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

# Position, Placement, Move
### getPlacement(iObj):

	getPlacement(iObj) - get placement with rotation info for given object.
	
##### Args:
	
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

	getGlobalPlacement(iObj) - call FreeCAD getGlobalPlacement at base object, and return useful form of placement
	
##### Args:
	
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

	setPlacement(iObj, iX, iY, iZ, iR, iAnchor="") - set placement with rotation for given object.
	
##### Args:

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

### resetPlacement(iObj):

	resetPlacement(iObj) - reset placement for given object. Needed to set rotation for object at face.
	
##### Args:
	
		iObj: object to reset placement

##### Usage:
	
		MagicPanels.resetPlacement(obj)

##### Result:
	
		Object obj return to base position.

### getSketchPlacement(iSketch, iType):

	getSketchPlacement(iSketch, iType) - get placement dedicated to move and copy Sketch directly.
	
##### Args:
	
		iSketch: Sketch object
		iType: 
			"global" - global Sketch position
			"attach" - AttachmentOffset position

##### Usage:
	
		[ x, y, z, r ] = MagicPanels.getSketchPlacement(sketch, "global")

##### Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

### setSketchPlacement(iSketch, iX, iY, iZ, iR, iType):

	setSketchPlacement(iSketch, iX, iY, iZ, iR, iType) - set placement with rotation dedicated to move and copy Sketch directly.
	
##### Args:

		iSketch: Sketch object to set custom placement and rotation
		iX: X Axis object position
		iX: Y Axis object position
		iZ: Z Axis object position
		iR: Rotation object
		iType: 
			"global" - global Sketch position, good before Pocket or any other operation, Sketch global position is temporary, FreeCAD bug? after Sketch edit the Sketch position will be lost, use "attach" to keep it
			"attach" - AttachmentOffset position, global position will be converted to AttachmentOffset, make sure the Support is set for Sketch, the Clones may not have Support, use global instead

##### Usage:
	
		MagicPanels.setSketchPlacement(sketch, 100, 100, 200, r, "attach")

##### Result:
	
		Object Sketch should be moved.

### convertPosition(iObj, iX, iY, iZ):

	convertPosition(iObj, iX, iY, iZ) - convert given position vector to correct position values according 
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

### getObjectCenter(iObj):

	getObjectCenter(iObj) - return Shape.CenterOfMass for the object or calculates center from vertices. 
	However, for Cone the CenterOfMass is not the center of object. More reliable is calculation 
	from vertices but some objects do not have all vertices to calculation. So, for now to handle 
	simple Pad objects and LinkGroups the CenterOfMass will be returned first.
	
##### Args:
	
		iObj: object

##### Usage:
	
		[ cx, cy, cz ] = MagicPanels.getObjectCenter(obj)

##### Result:
	
		Returns array with [ cx, cy, cz ] values for center point.

### sizesToCubePanel(iObj, iType):

	sizesToCubePanel(iObj, iType) - converts selected object (iObj) sizes to Cube panel sizes into given direction (iType). 
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

	makePad(iObj, iPadLabel="Pad") - allows to create Part, Plane, Body, Pad, Sketch objects.
	
##### Args:
	
		iObj: object Cube to change into Pad
		iPadLabel: Label for the new created Pad, the Name will be Pad

##### Usage:

		[ part, body, sketch, pad ] = MagicPanels.makePad(obj, "myPanel")

##### Result:
	
		Created Pad with correct placement, rotation and return [ part, body, sketch, pad ].

# Holes
### makeHoles(iObj, iFace, iCylinders):

	makeHoles(iObj, iFace, iCylinders) - make holes

##### Args:

		iObj: base object to make hole
		iFace: face of base object to make hole
		iCylinders: list of cylinders to make holes below each one

##### Usage:

		holes = MagicPanels.makeHoles(obj, face, cylinders)
		
##### Result:

		Make holes and return list of holes.

### makeCountersinks(iObj, iFace, iCones):

	makeCountersinks(iObj, iFace, iCones) - make countersinks

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makeCountersinks(obj, face, cones)

##### Result:

		Make holes and return list of holes. 

### makeCounterbores(iObj, iFace, iCones):

	makeCounterbores(iObj, iFace, iCones) - make counterbores

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makeCounterbores(obj, face, cones)

##### Result:

		Make holes and return list of holes.

### makePocketHoles(iObj, iFace, iCones):

	makePocketHoles(iObj, iFace, iCones) - make pocket holes for invisible connections

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		holes = MagicPanels.makePocketHoles(obj, face, cones)

##### Result:

		Make holes and return list of holes.

### makeCounterbores2x(iObj, iFace, iCones):

	makeCounterbores2x(iObj, iFace, iCones) - make counterbores from both sides

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

	makeCuts(iObjects) - allows to create multi bool cut operation at given objects. First objects 
	from iObjects is the base element and all other will cut the base. The copies will be created for cut. 
	
##### Args:
	
		iObjects: objects to parse by multi bool cut

##### Usage:
	
		cuts = MagicPanels.makeCuts(objects)

##### Result:
	
		Array of cut objects will be returned.

### makeFrame45cut(iObjects, iFaces):

	makeFrame45cut(iObjects, iFaces) - makes 45 frame cut with PartDesing Chamfer. 
	For each face the ends will be cut.
	
##### Args:
	
		iObjects: array of objects to cut
		iFaces: dict() of faces for Chamfer cut direction, the key is iObjects value (object), 
				if there are more faces for object, the first one will be get as direction.

##### Usage:
	
		frames = MagicPanels.makeFrame45cut(objects, faces)
		
##### Result:
	
		Created Frames with correct placement, rotation and return array with Chamfer frame objects.

### makeChamferCut(iObjects, iEdges, iSizes, iLabels):

	makeChamferCut(iObjects, iEdges, iSizes, iLabels) - makes PartDesing Chamfer cut for edges array. But you can set 
	different size for each edge. Yes, you give edge objects, and you make chamfer for each edge, one by one, 
	with different size, but the most funny part is that the selected edge not exists because the Cube 
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

	makeMortise(iSketch, iDepth, iPad, iFace) - make Mortise pocket for given iSketch pattern

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

	makeTenon(iSketch, iLength, iPad, iFace) - make Tenon pad for given iSketch pattern

##### Args:

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

	copyColors(iSource, iTarget) - allows to copy colors from iSource object to iTarget object

##### Args:

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

	sheetGetKey(iC, iR) - allow to get key as letters for spreadsheet from given column and row index.

##### Args:
	
		iC: column index
		iR: row index

##### Usage:
	
		key = MagicPanels.sheetGetKey(1, 2)

##### Result:
	
		return key string

# Info screen
### showInfo(iCaller, iInfo, iNote="yes"):

	showInfo(iCaller, iInfo, iNote="yes") - allow to show Gui info box for all available function and multiple calls.

##### Args:
	
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

