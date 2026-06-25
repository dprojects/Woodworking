import FreeCAD, FreeCADGui, math
import Draft
import MagicPanels

MagicPanels.initConfig()
translate = FreeCAD.Qt.translate


def faceTextRotation(face):
	"""Rotation that lays the text on the face plane with reading direction
	(local +X) along the face's longest edge."""
	try:
		z = FreeCAD.Vector(face.normalAt(0.5, 0.5))
		if z.Length < 1e-6:
			return FreeCAD.Rotation()
		z.normalize()
	except:
		return FreeCAD.Rotation()
	longest = None
	longestLen = 0.0
	for e in face.Edges:
		if e.Length > longestLen:
			longestLen = e.Length
			longest = e
	if longest is None or len(longest.Vertexes) < 2:
		return FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), z)
	x = longest.Vertexes[-1].Point.sub(longest.Vertexes[0].Point)
	if x.Length < 1e-6:
		return FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), z)
	x.normalize()
	d = x.dot(z)
	x = FreeCAD.Vector(x.x - z.x * d, x.y - z.y * d, x.z - z.z * d)
	if x.Length < 1e-6:
		return FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), z)
	x.normalize()
	y = z.cross(x)
	m = FreeCAD.Matrix(
		x.x, y.x, z.x, 0,
		x.y, y.y, z.y, 0,
		x.z, y.z, z.z, 0,
		0,   0,   0,   1,
	)
	return FreeCAD.Placement(m).Rotation


try:

	objects = FreeCADGui.Selection.getSelection()
	subObjects = FreeCADGui.Selection.getSelectionEx()

	if len(objects) < 1:
		raise

	i = 0
	for o in objects:

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

		txt = None
		for face in faces:

			faceIndex = MagicPanels.getFaceIndex(o, face)

			rotation = faceTextRotation(face)
			fontSize = max(math.sqrt(face.Area)/6, 20)
			offset = rotation.multVec(FreeCAD.Vector(0, -fontSize * 0.4, 0))
			p = FreeCAD.Placement(face.CenterOfMass.add(offset), rotation)

			# remove any previous grain label for this face
			for suffix in ("Grain Horizontal", "Grain Vertical", "No Grain"):
				label = str(o.Label) + ", Face" + str(faceIndex) + ", " + suffix + " "
				try:
					for rmo in FreeCAD.ActiveDocument.getObjectsByLabel(label):
						FreeCAD.ActiveDocument.removeObject(rmo.Name)
				except:
					pass

			arrows = "X"
			txt = Draft.make_text(arrows, placement=p)
			txt.Label = str(o.Label) + ", Face" + str(faceIndex) + ", No Grain "

			txt.ViewObject.FontSize = fontSize
			txt.ViewObject.Justification = "Center"
			txt.ViewObject.TextColor = (0.0, 0.0, 0.0, 1.0)

			centerExpr = o.Name + ".Shape.Face" + str(faceIndex) + ".CenterOfMass"
			txt.setExpression('.Placement.Base.x', centerExpr + ".x + (" + str(offset.x) + ")")
			txt.setExpression('.Placement.Base.y', centerExpr + ".y + (" + str(offset.y) + ")")
			txt.setExpression('.Placement.Base.z', centerExpr + ".z + (" + str(offset.z) + ")")

			try:
				MagicPanels.moveToFirst([ txt ], o)
			except:
				pass

			grain[faceIndex-1] = "x"

		o.Grain = grain

	FreeCAD.ActiveDocument.recompute()
	FreeCADGui.Selection.clearSelection()

except:

	info = ""

	info += translate('grainX', '<b>Please select face to create direction description about no grain. </b><br><br><b>Note:</b> This tool creates direction description  about no grain at selected face. You can select multiple faces and multiple objects. Hold left CTRL key during selection. The Grain attribute will be added to the object. After adding grain direction description the object can be moved and the grain description will be moved together with the object.')

	MagicPanels.showInfo("grainX", info)
