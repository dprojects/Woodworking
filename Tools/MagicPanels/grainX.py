import FreeCAD, FreeCADGui, math
import Draft
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()
	subObjects = FreeCADGui.Selection.getSelectionEx()

	if len(objects) < 1:
		raise

	i = 0
	for o in objects:

		rotated = MagicPanels.isRotated(o)
		if rotated:
			angle = o.Placement.Rotation.Angle
			o.Placement.Rotation.Angle = 0

		faces = subObjects[i].SubObjects
		i = i + 1
		
		if not hasattr(o, "Grain"):
			info = translate("grainX", "face grain direction, h - horizontal, v - vertical, x - no grain")
			o.addProperty("App::PropertyStringList", "Grain", "Woodworking", info)

		if len(o.Grain) == len(o.Shape.Faces):
			grain = o.Grain
		else:
			grain = []
			for f in o.Shape.Faces:
				grain.append("x")

		for face in faces:

			faceIndex = MagicPanels.getFaceIndex(o, face)
			[ plane, faceType ] = MagicPanels.getFaceDetails(o, face)
			sink = MagicPanels.getFaceSink(o, face)

			p = FreeCAD.Placement()
			p.Base = face.CenterOfMass

			if plane == "XY":
				if sink == "-":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
				if sink == "+":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(-1.00, 0.00, 0.00), 180.00)
					
			if plane == "YX":
				if sink == "-":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 90.00)
				if sink == "+":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(-0.71, -0.71, 0.00), 180.00)
				
			if plane == "XZ":
				if sink == "-":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1.00, 0.00, 0.00), 270.00)
				if sink == "+":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1.00, 0.00, 0.00), 90.00)

			if plane == "ZX":
				if sink == "-":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(-0.58, -0.58, -0.58), 120.00)
				if sink == "+":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(-58.00, 58.00, -58.00), 240.00)

			if plane == "YZ":
				if sink == "-":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0.58, 0.58, 0.58), 120.00)
				if sink == "+":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(-0.58, -0.58, 0.58), 120.00)

			if plane == "ZY":
				if sink == "-":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(-0.71, 0.00, -0.71), 180.00)
				if sink == "+":
					p.Rotation = FreeCAD.Rotation(FreeCAD.Vector(-0.71, 0.00, 0.71), 180.00)

			try:
				label = str(o.Label) + ", " + "Face" + str(faceIndex) + ", " + "Grain Horizontal" + " "
				rmo = FreeCAD.ActiveDocument.getObjectsByLabel(label)[0]
				FreeCAD.ActiveDocument.removeObject(str(rmo.Name))
			except:
				skip = 1
				
			try:
				label = str(o.Label) + ", " + "Face" + str(faceIndex) + ", " + "Grain Vertical" + " "
				rmo = FreeCAD.ActiveDocument.getObjectsByLabel(label)[0]
				FreeCAD.ActiveDocument.removeObject(str(rmo.Name))
			except:
				skip = 1
			
			try:
				label = str(o.Label) + ", " + "Face" + str(faceIndex) + ", " + "No Grain" + " "
				rmo = FreeCAD.ActiveDocument.getObjectsByLabel(label)[0]
				FreeCAD.ActiveDocument.removeObject(str(rmo.Name))
			except:
				skip = 1

			arrows = "No Grain"
			txt = Draft.make_text(arrows, placement=p)
			txt.Label = str(o.Label) + ", " + "Face" + str(faceIndex) + ", " + "No Grain" + " "
			
			txt.ViewObject.FontSize = math.sqrt(face.Area)/6
			txt.ViewObject.Justification = "Center"
			txt.ViewObject.TextColor = (1.0, 0.0, 0.0, 0.0)
			
			targetX = o.Name + ".Shape.Face" + str(faceIndex) + ".CenterOfMass.x"
			targetY = o.Name + ".Shape.Face" + str(faceIndex) + ".CenterOfMass.y"
			targetZ = o.Name + ".Shape.Face" + str(faceIndex) + ".CenterOfMass.z"
			txt.setExpression('.Placement.Base.x', targetX)
			txt.setExpression('.Placement.Base.y', targetY)
			txt.setExpression('.Placement.Base.z', targetZ)
			
			grain[faceIndex-1] = "x"

		o.Grain = grain
		
		if rotated:
			o.Placement.Rotation.Angle = angle

		MagicPanels.moveToFirst([ txt ], o)
		MagicPanels.addRotation(o, [ txt ])

	FreeCAD.ActiveDocument.recompute()
	FreeCADGui.Selection.clearSelection()

except:
	
	info = ""
	
	info += translate('grainX', '<b>Please select face to create no grain direction description. </b><br><br><b>Note:</b> This tool creates no grain direction description at selected face. You can select multiple faces and multiple objects. Hold left CTRL key during selection. The Grain attribute will be added to the object. After adding grain direction description the object can be moved and the grain description will be moved together with the object.')

	MagicPanels.showInfo("grainX", info)
