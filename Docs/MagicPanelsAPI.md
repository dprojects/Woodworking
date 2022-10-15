# equal(iA, iB):

	equal(iA, iB) - At FreeCAD there are many values like 1.000006, especially for PartDesign objects. 
	So if you want to compare such values this sometimes might be True and sometimes False. Some people will 
	tell you it is because of Pi, but I do not have the time or the desire to fight with human stupidity. 
	Recently I spent two hours debugging my code and in the end it turned out to be working fine after 
	rounding the values. So, finally I decided to write my own function for comparison.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iA: float value
		iB: float value

##### Usage:
	
		if equal(1.0006, 1):
			do something ...
		
##### Result:
	
		return True if equal or False if not

# touchTypo(iObj):

	touchTypo(iObj) - touch the typo so that the typo-snake does not notice it ;-) LOL
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object to touch

##### Usage:
	
		vs = touchTypo(o)
		
##### Result:
	
		return Vertex + es for object o

# normalizeBoundBox(iBoundBox):

	normalizeBoundBox(iBoundBox) - return normalized version of BoundBox. All values 0.01 will be rounded 
	allowing comparison, and searches for the same face or edge.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iBoundBox: directly pass BoundBox object

##### Usage:
	
		e1 = obj1.Shape.Edges[0]
		e2 = obj2.Shape.Edges[0]
		
		b1 = normalizeBoundBox(e1.BoundBox)
		b2 = normalizeBoundBox(e2.BoundBox)
		
##### Result:
	
		return normalized version for comparison if b1 == b2: you can set your own precision here

# showVertex(iVertex):

	showVertex(iVertex) - create sphere at given vertex, to show where is the point for debug purposes.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iVertex: vertex object
	
##### Usage:
	
		showVertex(obj.Shape.CenterOfMass)
		
##### Result:
	
		show vertex
# getVertex(iFace, iEdge, iVertex):

	getVertex(iFace, iEdge, iVertex) - get vertex values for face, edge and vertex index.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iFace: face object
		iEdge: edge array index
		iVertex: vertex array index (0 or 1)
	
##### Usage:
	
		[ x, y, z ] = getVertex(gFace, 0, 1)
		
##### Result:
	
		Return vertex position.
# getVertexAxisCross(iA, iB):

	getVertexAxisCross(iA, iB) - get (iB - iA) value.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iA: vertex float value
		iB: vertex float value
	
##### Usage:
	
		edgeSize = getVertexAxisCross(v0[0], v1[0])
		
##### Result:
	
		Return diff for vertices values.
# getVerticesPlane(iV1, iV2):

	getVerticesPlane(iV1, iV2) - get axes with the same values
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iV1: vertex object
		iV2: vertex object
	
##### Usage:
	
		plane = getVerticesPlane(v1, v2)
		
##### Result:
	
		Return plane as "XY", "XZ", "YZ".
# setVertexPadding(iObj, iVertex, iPadding, iAxis):

	setVertexPadding(iObj, iVertex, iPadding, iAxis) - set padding offset from given vertex to inside the object.
	Do not use it at getPlacement for Pads. Use 0 vertex instead.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object
		iVertex: vertex object FreeCAD.Vector(x, y, z)
		iPadding: value > 0 for making offset
		iAxis: string: "X" or "Y" or "Z"
		
##### Usage:
	
		v = getattr(obj.Shape, "Vertex"+"es")[0]
		offsetX = setVertexPadding(obj, v, 15, "X")
		
##### Result:
	
		Return return new position value for given axis.
# getEdgeVertices(iEdge):

	getEdgeVertices(iEdge) - get all vertices values for edge.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iEdge: edge object
		
##### Usage:
	
		[ v1, v2 ] = getEdgeVertices(gEdge)
		
##### Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 1, 1, 1 ] ].
# getEdgeNormalized(iV1, iV2):

	getEdgeNormalized(iV1, iV2) - returns vertices with exact sorted order V1 > V2, mostly used 
	to normalize Pad vertices
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iV1: array with vertices e.g. [ 1, 1, 1 ]
		iV2: array with vertices e.g. [ 2, 2, 2 ]
	
##### Usage:
	
		[ v1, v2 ] = getEdgeNormalized(v1, v2)
		
##### Result:
	
		for vertices [ 2, 2, 2 ], [ 1, 1, 1 ] return [ 1, 1, 1 ], [ 2, 2, 2 ]

# getEdgeIndex(iObj, iEdge):

	getEdgeIndex(iObj, iEdge) - returns edge index for given object and edge.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object of the edge
		iEdge: edge object
	
##### Usage:
	
		edgeIndex = getEdgeIndex(gObj, gEdge)
		
##### Result:
	
		return int value for edge

# getEdgeIndexByKey(iObj, iBoundBox):

	getEdgeIndexByKey(iObj, iBoundBox) - returns edge index for given edge BoundBox.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object of the edge
		iBoundBox: edge BoundBox as key
	
##### Usage:
	
		edgeIndex = getEdgeIndex(o, key)
		
##### Result:
	
		return int value for edge

# getEdgePlane(iEdge):

	getEdgePlane(iEdge) - returns orientation for the edge, changed axis, as "X", "Y" or "Z".
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iEdge: edge object
		
##### Usage:
	
		plane = getEdgePlane(edge)
		
##### Result:
	
		return string "X", "Y" or "Z".

# getFaceIndex(iObj, iFace):

	getFaceIndex(iObj, iFace) - returns face index for given object and face.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object of the face
		iFace: face object
	
##### Usage:
	
		faceIndex = getFaceIndex(gObj, gFace)
		
##### Result:
	
		return int value for face

# getFaceIndexByKey(iObj, iBoundBox):

	getFaceIndexByKey(iObj, iBoundBox) - returns face index for given face BoundBox.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object of the face
		iBoundBox: face BoundBox as key
	
##### Usage:
	
		faceIndex = getFaceIndexByKey(o, key)
		
##### Result:
	
		return int value for face

# getFaceVertices(iFace):

	getFaceVertices(iFace) - get all vertices values for face.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iFace: face object
		
##### Usage:
	
		[ v1, v2, v3, v4 ] = getFaceVertices(gFace)
		
##### Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 2, 2, 2 ], [ 3, 3, 3 ], [ 4, 4, 4 ] ]
# getFaceType(iObj, iFace):

	getFaceType(iObj, iFace) - get face type, if this is "edge" or "surface".
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object where is the face
		iFace: face object

##### Usage:
	
		faceType = getFaceType(gObj, gFace)
		
##### Result:
	
		Return string "surface" or "edge".

# getFaceEdges(iObj, iFace):

	getFaceEdges(iObj, iFace) - get all edges for given face grouped by sizes.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object where is the face
		iFace: face object

##### Usage:
	
		[ faceType, arrAll, arrThick, arrShort, arrLong ] = getFaceEdges(gObj, gFace)
		
##### Result:
	
		Return arrays like [ faceType, arrAll, arrThick, arrShort, arrLong ] with edges objects, 
		
		faceType - string "surface" or "edge"
		arrAll - array with all edges
		arrThick - array with the thickness edges
		arrShort - array with the short edges (if type is edge this will be the same as arrThick)
		arrLong - array with the long edges

# getFacePlane(iFace):

	getFacePlane(iFace) - get face plane in notation "XY", "XZ", "YZ". 

	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iFace: face object
	
##### Usage:
	
		plane = getFacePlane(face)
		
##### Result:
	
		string "XY", "XZ", or "YZ".
		
# getFaceSink(iObj, iFace):

	getFaceSink(iObj, iFace) - get face sink axis direction in notation "+", or "-".

	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object with the face
		iFace: face object
	
##### Usage:
	
		sink = getFaceSink(obj, face)
		
##### Result:
	
		string "+" if the object at face should go along axis forward, 
		or "-" if the object at face should go along axis backward
		
# getFaceObjectRotation(iObj, iFace):

	getFaceObjectRotation(iObj, iFace) - get face object rotation to apply to the new created object at face. 
	Object created at face with this rotation should be up from the face.

	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object with the face
		iFace: face object
	
##### Usage:
	
		r = getFaceObjectRotation(obj, face)
		
##### Result:
	
		FreeCAD.Rotation object that can be directly pass to the setPlacement or object.Placement
		
# getFaceDetails(iObj, iFace):

	getFaceDetails(iObj, iFace) - allow to get detailed information for face direction.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: selected object
		iFace: selected face object
	
##### Usage:
	
		getFaceDetails(gObj, gFace)
		
##### Result:
	
		[ "XY", "surface" ] - if the direction is XY and it is surface, no thickness edge
		[ "XY", "edge" ] - if the direction is XY and it is edge, there is thickness edge
		[ "XY", "equal" ] - if the direction is XY and both edges are equal
		
		Note: The first argument can be "XY", "YX", "XZ", "ZX", "YZ", "ZY". 
		This is related to face not to object. The object direction will be different.
		
# getReference(iObj="none"):

	getReference(iObj="none") - get reference to the selected or given object.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj (optional): object to get reference (to return base object)
	
##### Usage:
	
		gObj = getReference()
		
##### Result:
	
		obj - reference to the base object

# getSizes(iObj):

	getSizes(iObj) - allow to get sizes for object (iObj), according to the object type. The values are not sorted.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object to get sizes
	
##### Usage:
	
		[ size1, size2, size3 ] = getSizes(obj)
		
##### Result:
	
		Returns [ Length, Width, Height ] for Cube.
# getSizesFromVertices(iObj):

	getSizesFromVertices(iObj) - get occupied space by the object from vertices.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object
	
##### Usage:
	
		[ sx, sy, sz ] = getSizesFromVertices(obj)
		
##### Result:
	
		Returns array with [ mX, mY, mZ ] where: 
		mX - occupied space along X axis
		mY - occupied space along Y axis
		mZ - occupied space along Z axis
		
# showMeasure(iP1, iP2, iRef=""):

	showMeasure(iP1, iP2, iRef="") - create measurements object, I mean draw it. Now it use FreeCAD function 
	to create and draw object. But in the future this can be changed to more beautiful drawing without changing
	tools. 
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iP1: starting point vertex object
		iP2: ending point vertex object
		iRef (optional): string for future TechDraw import or any other use, other tools
	
##### Usage:
	
		m = MagicPanels.showMeasure(gP1, gP2, "Pad")
		
##### Result:
	
		Create measure object, draw it and return measure object for further proccessing. 
# getModelRotation(iX, iY, iZ):

	getModelRotation() - transform given iX, iY, iZ values to the correct vector, if the user rotated 3D model.

	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iX: X value to transform
		iY: Y value to transform
		iY: Z value to transform
	
##### Usage:
	
		[x, y, z ] = getModelRotation(x, y, z)
		
##### Result:
	
		[ X, Y, Z ] - transformed vector of given values

# getDirection(iObj):

	getDirection(iObj) - allow to get Cube object direction (iType).
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: selected object
	
##### Usage:
	
		getDirection(obj)
		
##### Result:
	
		Returns iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"
# getPlacement(iObj):

	getPlacement(iObj) - get placement with rotation info for given object.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object to get placement

##### Usage:
	
		[ x, y, z, r ] = getPlacement(gObj)
		
##### Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

# setPlacement(iObj, iX, iY, iZ, iR, iAnchor=""):

	setPlacement(iObj, iX, iY, iZ, iR, iAnchor="") - set placement with rotation for given object.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object to set custom placement and rotation
		iX: X Axis object position
		iX: Y Axis object position
		iZ: Z Axis object position
		iR: Rotation object
		iAnchor="" (optional): anchor for placement instead of 0 vertex, FreeCAD.Vector(x, y, z)

##### Usage:
	
		setPlacement(gObj, 100, 100, 200, r)
		
##### Result:
	
		Object gObj should be moved into 100, 100, 200 position without rotation.

# resetPlacement(iObj):

	resetPlacement(iObj) - reset placement for given object. Needed to set rotation for object at face.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object to reset placement

##### Usage:
	
		resetPlacement(obj)
		
##### Result:
	
		Object obj return to base position.

# convertPosition(iObj, iX, iY, iZ):

	convertPosition(iObj, iX, iY, iZ) - convert given position vector to correct position values according 
	to the object direction.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object
		iX: x position
		iY: y position
		iZ: z position
	
##### Usage:
	
		[ x, y, z ] = convertPosition(obj, 0, 400, 0)
		
##### Result:
	
		For Pad object in XZ direction return the AttachmentOffset order [ 0, 0, -400 ]
# getObjectCenter(iObj):

	getObjectCenter(iObj) - return Shape.CenterOfMass for the object or calculates center from vertices. 
	However, for Cone the CenterOfMass is not the center of object. More reliable is calculation 
	from vertices but some objects do not have all vertices to calculation. So, for now to handle 
	simple Pad objects and LinkGroups the CenterOfMass will be returned first.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object
	
##### Usage:
	
		[ cx, cy, cz ] = getObjectCenter(obj)
		
##### Result:
	
		Returns array with [ cx, cy, cz ] values for center point.
		
# sizesToCubePanel(iObj, iType):

	sizesToCubePanel(iObj, iType) - converts selected object (iObj) sizes to Cube panel sizes into given direction (iType). 
	So, the returned values can be directly assigned to Cube object in order to create 
	panel in exact direction.

	Note: This is internal function, so there is no error pop-up or any error handling.

##### Args:

		iObj: selected object
		iType direction: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

##### Usage:

		[ Length, Width, Height ] = sizesToCubePanel(obj, "YZ")
		
##### Result:

		Returns [ Length, Width, Height ] for YZ object placement".
# makePad(iObj, iPadLabel="Pad"):

	makePad(iObj, iPadLabel="Pad") - allows to create Part, Plane, Body, Pad, Sketch objects.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObj: object Cube to change into Pad
		iPadLabel: Label for the new created Pad, the Name will be Pad
		
##### Usage:
	
		import MagicPanels
		[ part, body, sketch, pad ] = MagicPanels.makePad(obj, "myPanel")
		
##### Result:
	
		Created Pad with correct placement, rotation and return [ part, body, sketch, pad ].
# makeCuts(iObjects):

	makeCuts(iObjects) - allows to create multi bool cut operation at given objects. First objects 
	from iObjects is the base element and all other will cut the base. The copies will be created for cut. 
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObjects: objects to parse by multi bool cut

##### Usage:
	
		import MagicPanels
		MagicPanels.makeCuts(objects)
		
##### Result:
	
		Array of cut objects will be returned.
# makeFrame45cut(iObjects, iFaces):

	makeFrame45cut(iObjects, iFaces) - makes 45 frame cut with PartDesing Chamfer. 
	For each face the ends will be cut.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iObjects: array of objects to cut
		iFaces: dict() of faces for Chamfer cut direction, the key is iObjects value (object), 
				if there are more faces for object, the first one will be get as direction.
		
##### Usage:
	
		import MagicPanels
		frames = MagicPanels.makeFrame45cut(objects, faces)
		
##### Result:
	
		Created Frames with correct placement, rotation and return array with Chamfer frame objects.
# makeHoles(iObj, iFace, iCylinders):

	makeHoles(iObj, iFace, iCylinders) - make holes

	Note: This is internal function, so there is no error pop-up or any error handling.

##### Args:

		iObj: base object to make hole
		iFace: face of base object to make hole
		iCylinders: list of cylinders to make holes below each one

##### Usage:

		import MagicPanels
		holes = MagicPanels.makeHoles(obj, face, cylinders)
		
##### Result:

		Make holes and return list of holes.
# makeCountersinks(iObj, iFace, iCones):

	makeCountersinks(iObj, iFace, iCones) - make countersinks

	Note: This is internal function, so there is no error pop-up or any error handling.

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		import MagicPanels
		holes = MagicPanels.makeCountersinks(obj, face, cones)
		
##### Result:

		Make holes and return list of holes. 
# makeCounterbores(iObj, iFace, iCones):

	makeCounterbores(iObj, iFace, iCones) - make counterbores

	Note: This is internal function, so there is no error pop-up or any error handling.

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		import MagicPanels
		holes = MagicPanels.makeCounterbores(obj, face, cones)
		
##### Result:

		Make holes and return list of holes. 
# makePocketHoles(iObj, iFace, iCones):

	makePocketHoles(iObj, iFace, iCones) - make pocket holes for invisible connections

	Note: This is internal function, so there is no error pop-up or any error handling.

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		import MagicPanels
		holes = MagicPanels.makePocketHoles(obj, face, cones)
		
##### Result:

		Make holes and return list of holes. 
# makeCounterbores2x(iObj, iFace, iCones):

	makeCounterbores2x(iObj, iFace, iCones) - make counterbores from both sides

	Note: This is internal function, so there is no error pop-up or any error handling.

##### Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

##### Usage:

		import MagicPanels
		holes = MagicPanels.makeCounterbores2x(obj, face, cones)
		
##### Result:

		Make holes and return list of holes. 
# copyColors(iSource, iTarget):

	copyColors(iSource, iTarget) - allows to copy colors from iSource object to iTarget object

	Note: This is internal function, so there is no error pop-up or any error handling.

##### Args:

		iSource: source object
		iTarget: target object
		
##### Usage:

		import MagicPanels
		MagicPanels.copyColors(panel, copy)
		
##### Result:

		All colors structure should be copied from source to target.
# sheetGetKey(iC, iR):

	sheetGetKey(iC, iR) - allow to get key as letters for spreadsheet from given column and row index.

	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iC: column index
		iR: row index
	
##### Usage:
	
		key = sheetGetKey(1, 2)
		
##### Result:
	
		return key string
# showInfo(iCaller, iInfo, iNote="yes"):

	showInfo(iCaller, iInfo, iNote="yes") - allow to show Gui info box for all available function and multiple calls.

	Note: This is internal function, so there is no error pop-up or any error handling.
	
##### Args:
	
		iCaller: window title
		iInfo: HTML text to show
		iNote: additional tutorial ("yes" or "no"), by default is "yes".
	
##### Usage:
	
		showInfo("panel"+iType, info)
		
##### Result:
	
		Show info Gui.
