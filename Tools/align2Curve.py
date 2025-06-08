import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate
curvePoints = []

# ###################################################################################################################
def searchCurve(iCurve, iObj, iSubName, iAnchor, iAxis, iDirection, iAngle=0, iVertexIndex=""):
	
	if iDirection == "+":
		if iAngle == 0:
			angle = 1
		else:
			angle = iAngle
			
	if iDirection == "-":
		if iAngle == 0:
			angle = -1
		else:
			angle = -iAngle
	
	rotation = iObj.Placement.Rotation
	
	if iAngle == 0:
		end = 101
	else:
		end = 2
	
	for index in range(1, end):
		rot = FreeCAD.Rotation(iAxis, angle)
		iObj.Placement.Rotation = iObj.Placement.Rotation * rot
		iObj.recompute()
		
		# get actual values
		sub = FreeCAD.ActiveDocument.getObject(iObj.Name).getSubObject(iSubName)
		subVector = FreeCAD.Vector(sub.X, sub.Y, sub.Z)

		if iCurve.Shape.isInside(subVector, 1, True):
			FreeCADGui.Selection.clearSelection()
			return True
	
	iObj.Placement.Rotation = rotation
	FreeCADGui.Selection.clearSelection()
	return False

# ###################################################################################################################
try:

	selection = FreeCADGui.Selection.getSelection()
	selectionEx = FreeCADGui.Selection.getSelectionEx()

	if len(selection) < 2:
		raise

	curve = selection[0]
	objects = selection[1:]

	curvePoints = curve.Shape.getPoints(1)[0]

	oIndex = 1
	for o in objects:

		sub = selectionEx[oIndex].SubObjects[0]
		subName = selectionEx[oIndex].SubElementNames[0]
		oIndex = oIndex + 1
		
		if sub.ShapeType == "Vertex":

			[ x, y, z, r ] = MagicPanels.getContainerPlacement(o, "clean")
			anchor = FreeCAD.Vector(x, y, z)
			
			axis = FreeCAD.Vector(1, 0, 0)
			result = searchCurve(curve, o, subName, anchor, axis, "+")
			if result == True:
				continue

			axis = FreeCAD.Vector(1, 0, 0)
			result = searchCurve(curve, o, subName, anchor, axis, "-")
			if result == True:
				continue

			axis = FreeCAD.Vector(0, 1, 0)
			result = searchCurve(curve, o, subName, anchor, axis, "+")
			if result == True:
				continue

			axis = FreeCAD.Vector(0, 1, 0)
			result = searchCurve(curve, o, subName, anchor, axis, "-")
			if result == True:
				continue
				
			axis = FreeCAD.Vector(0, 0, 1)
			result = searchCurve(curve, o, subName, anchor, axis, "+")
			if result == True:
				continue

			axis = FreeCAD.Vector(0, 0, 1)
			result = searchCurve(curve, o, subName, anchor, axis, "-")
			if result == True:
				continue

		if sub.ShapeType == "Edge":
			
			import math
			
			[ x, y, z, r ] = MagicPanels.getContainerPlacement(o, "clean")
			vxs = MagicPanels.touchTypo(sub)
			v1 = vxs[0]
			v2 = vxs[1]
			
			if MagicPanels.equal(x, v1.X) and MagicPanels.equal(y, v1.Y) and MagicPanels.equal(z, v1.Z):
				anchorVertex = v1
				subVertex = v2
				subVector = FreeCAD.Vector(v2.X, v2.Y, v2.Z)
			else:
				anchorVertex = v2
				subVertex = v1
				subVector = FreeCAD.Vector(v1.X, v1.Y, v1.Z)
			
			subIndex = MagicPanels.getVertexIndex(o, subVertex)
			subName = "Vertex"+str(subIndex)
			
			anchorIndex = MagicPanels.getOnCurve(anchorVertex, curve)
			if anchorIndex == -1:
				continue

			anchorVector = curvePoints[anchorIndex]

			length = sub.Length
			scope = 2 * int(length)
			
			targetIndex = -1
			for i in range(1, scope):
				index = anchorIndex + i
				try:
					dist = curvePoints[anchorIndex].distanceToPoint(curvePoints[index])
				except:
					continue

				if dist > length:
					break
				else:
					targetIndex = index
					targetVector = curvePoints[index]
			
			if targetIndex != -1:
				angle = (targetVector - anchorVector).getAngle(subVector - anchorVector)
				angle = math.degrees(angle)

				axis = FreeCAD.Vector(0, 1, 0)
				result = searchCurve(curve, o, subName, anchorVector, axis, "+", angle)
				if result == True:
					continue

				axis = FreeCAD.Vector(0, 1, 0)
				result = searchCurve(curve, o, subName, anchorVector, axis, "-", angle)
				if result == True:
					continue
				
				axis = FreeCAD.Vector(1, 0, 0)
				result = searchCurve(curve, o, subName, anchorVector, axis, "+", angle)
				if result == True:
					continue

				axis = FreeCAD.Vector(1, 0, 0)
				result = searchCurve(curve, o, subName, anchorVector, axis, "-", angle)
				if result == True:
					continue

				axis = FreeCAD.Vector(0, 0, 1)
				result = searchCurve(curve, o, subName, anchorVector, axis, "+", angle)
				if result == True:
					continue

				axis = FreeCAD.Vector(0, 0, 1)
				result = searchCurve(curve, o, subName, anchorVector, axis, "-", angle)
				if result == True:
					continue

	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""

	info += "<b>" + translate('align2Curve', 'Possible selection methods') + ": " + "</b><ul>"
	info += "<li>"
	info += translate('align2Curve', 'First select curve, next select edge at each object you want to align.')
	info += "</li>"
	info += "<li>"
	info += translate('align2Curve', 'First select curve, next select vertex at each object you want to align, this might be slower but more precise.')
	info += "</li></ul>"
	info += "<b>" + translate('align2Curve', 'Note') + ": </b>"
	info += translate('align2Curve', 'This tool allows to align panels to the curve. It has been created for magicMove Copy Path option, to align panels to the curve. To select more objects hold left CTRL key during selection. To use this tool the panel need to have only single axis rotation offset. For example if you rotate panel 35 degrees around Y axis and the vertex will touch the curve. This tool not works if you need to rotate the panel additionally, for example 15 degrees around X axis. For more details see description at documentation page.')
	
	MagicPanels.showInfo("align2Curve", info)

