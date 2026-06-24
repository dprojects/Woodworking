import FreeCAD, FreeCADGui

import MagicPanels

MagicPanels.initConfig()
translate = FreeCAD.Qt.translate


def baseColorRGBA(obj):
	try:
		c = obj.ViewObject.ShapeAppearance[0].DiffuseColor
	except:
		try:
			c = obj.ViewObject.DiffuseColor[0]
		except:
			c = (0.8, 0.8, 0.8, 1.0)
	return [int(round(c[0] * 255)), int(round(c[1] * 255)),
		int(round(c[2] * 255)),
		int(round(c[3] * 255)) if len(c) > 3 else 255]


try:

	selectionEx = FreeCADGui.Selection.getSelectionEx()
	pairs = []
	for selObj in selectionEx:
		obj = selObj.Object
		for face in selObj.SubObjects:
			try:
				idx = MagicPanels.getFaceIndex(obj, face)
				pairs.append((obj, idx))
			except:
				pass

	if len(pairs) == 0:
		raise Exception("no faces selected")

	byObj = {}
	for obj, faceIdx in pairs:
		byObj.setdefault(obj.Name, (obj, []))[1].append(faceIdx)

	touched = 0
	for name, (obj, faceIdxs) in byObj.items():
		if not hasattr(obj, "EdgeBand") or not hasattr(obj, "EdgeBandFaces"):
			continue
		bands = list(obj.EdgeBand)
		faces = list(obj.EdgeBandFaces)
		restoreColor = baseColorRGBA(obj)
		for faceIdx in faceIdxs:
			# find which side(s) this face was assigned to
			for side in range(4):
				if side < len(faces) and faces[side] == faceIdx:
					bands[side] = ""
					faces[side] = 0
					try:
						MagicPanels.setColor(obj, faceIdx, restoreColor, "color", "RGBA")
					except Exception as e:
						FreeCAD.Console.PrintWarning(
							"bandRemove: could not restore color of face "
							+ str(faceIdx) + " of " + obj.Label + ": "
							+ str(e) + "\n")
					# remove the visual band label created by bandApply
					label = str(obj.Label) + ", Face" + str(faceIdx) + ", EdgeBand "
					try:
						for rmo in FreeCAD.ActiveDocument.getObjectsByLabel(label):
							FreeCAD.ActiveDocument.removeObject(rmo.Name)
					except:
						pass
					touched += 1
		obj.EdgeBand = bands
		obj.EdgeBandFaces = faces

	FreeCAD.ActiveDocument.recompute()
	FreeCADGui.Selection.clearSelection()

	if touched == 0:
		MagicPanels.showInfo("bandRemove", translate("bandRemove",
			"None of the selected faces had a band assigned."))

except Exception as e:

	info = translate("bandRemove",
		"<b>Please select one or more faces with an applied band, "
		"then run this tool.</b><br><br>"
		"The band is cleared from the panel's EdgeBand property and the "
		"face is repainted with the panel's base color.")
	MagicPanels.showInfo("bandRemove", info)
