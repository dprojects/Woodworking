import FreeCAD, FreeCADGui
import math
import Draft
from PySide import QtGui, QtCore

import MagicPanels

MagicPanels.initConfig()
translate = FreeCAD.Qt.translate


LIBRARY_NAME = "EdgeBandLibrary"


def bandLabelString(obj, faceIdx):
	# label format used to find/remove the band's Draft Text object
	return str(obj.Label) + ", Face" + str(faceIdx) + ", EdgeBand "


def removeBandLabel(obj, faceIdx):
	label = bandLabelString(obj, faceIdx)
	try:
		for rmo in FreeCAD.ActiveDocument.getObjectsByLabel(label):
			FreeCAD.ActiveDocument.removeObject(rmo.Name)
	except:
		pass


def faceTextRotation(face):
	"""Rotation that lays the text on the face plane. The reading direction
	(text's local +X) is taken from the face's longest edge, so the label
	always runs along the long side of the panel face."""
	try:
		z = FreeCAD.Vector(face.normalAt(0.5, 0.5))
		if z.Length < 1e-6:
			return FreeCAD.Rotation()
		z.normalize()
	except:
		return FreeCAD.Rotation()

	# pick the longest straight-ish edge as the reading direction
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

	# project x onto the face plane to guarantee it's perpendicular to z
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


def drawBandLabel(obj, faceIdx, face, side, bandName):
	# remove any previous label for this face
	removeBandLabel(obj, faceIdx)

	rotation = faceTextRotation(face)
	fontSize = max(math.sqrt(face.Area) / 6, 14)

	# Draft Text is anchored at the baseline, so the glyph's visual centre
	# sits ~0.4 * FontSize above the placement origin. Push the origin down
	# along the text's local -Y axis so the label is centred on the face.
	offset = rotation.multVec(FreeCAD.Vector(0, -fontSize * 0.4, 0))
	base = face.CenterOfMass.add(offset)

	p = FreeCAD.Placement(base, rotation)

	text = side.upper() + ": " + bandName
	txt = Draft.make_text(text, placement=p)
	txt.Label = bandLabelString(obj, faceIdx)

	try:
		txt.ViewObject.FontSize = fontSize
		txt.ViewObject.Justification = "Center"
		txt.ViewObject.TextColor = (0.0, 0.0, 0.0, 1.0)
	except:
		pass

	# anchor the label to follow the face's center, keeping the vertical-centre offset
	centerExpr = obj.Name + ".Shape.Face" + str(faceIdx) + ".CenterOfMass"
	try:
		txt.setExpression('.Placement.Base.x', centerExpr + ".x + (" + str(offset.x) + ")")
		txt.setExpression('.Placement.Base.y', centerExpr + ".y + (" + str(offset.y) + ")")
		txt.setExpression('.Placement.Base.z', centerExpr + ".z + (" + str(offset.z) + ")")
	except:
		pass

	try:
		MagicPanels.moveToFirst([txt], obj)
	except:
		pass

	return txt


def parseRGBA(s):
	try:
		parts = [int(p.strip()) for p in s.split(",")]
		while len(parts) < 4:
			parts.append(255)
		return parts[:4]
	except:
		return [200, 200, 200, 255]


def ensureBandProps(obj):
	if not hasattr(obj, "EdgeBand"):
		obj.addProperty("App::PropertyStringList", "EdgeBand", "Woodworking",
			"Edge band per side: [Top, Left, Bottom, Right]")
		obj.EdgeBand = ["", "", "", ""]
	elif len(obj.EdgeBand) != 4:
		obj.EdgeBand = ["", "", "", ""]

	if not hasattr(obj, "EdgeBandFaces"):
		obj.addProperty("App::PropertyIntegerList", "EdgeBandFaces", "Woodworking",
			"Face index (1-based) for each side, 0 if not assigned")
		obj.EdgeBandFaces = [0, 0, 0, 0]
	elif len(obj.EdgeBandFaces) != 4:
		obj.EdgeBandFaces = [0, 0, 0, 0]


def classifyPanelFaces(obj):
	"""
	Geometric classification of the 6 faces of a panel.
	Returns (bigFaceIdxs_set, sideMap_dict) where:
	  - bigFaceIdxs: 1-based indices of the 2 widest faces (the "grain" faces).
	  - sideMap: {face_index: "Top"|"Left"|"Bottom"|"Right"} for the 4 lateral faces.

	Convention:
	  - The 2 faces with the largest area are the "big" (grain) faces.
	  - Of the 4 lateral faces, the 2 with greater area are Top/Bottom
	    (long sides), the 2 with lesser area are Left/Right (short sides).
	  - Within each opposite pair, the face whose center is "higher" in the
	    panel's local frame is Top / Right respectively; the other is
	    Bottom / Left.

	Returns (set(), {}) if the panel does not have at least 6 faces.
	"""
	faces = obj.Shape.Faces
	n = len(faces)
	if n < 6:
		return set(), {}

	# (1-based index, area) sorted by area desc
	areas = sorted(
		[(i + 1, faces[i].Area) for i in range(n)],
		key=lambda x: -x[1],
	)

	big = {areas[0][0], areas[1][0]}

	# The next 4 (sorted desc) are the lateral faces.
	# If the shape has > 6 faces (chamfers, fillets, holes, ...) we still
	# pick the 4 largest non-big as the lateral candidates.
	lateral = areas[2:6]
	lateralSortedDesc = sorted(lateral, key=lambda x: -x[1])
	longSidesIdxs = [lateralSortedDesc[0][0], lateralSortedDesc[1][0]]
	shortSidesIdxs = [lateralSortedDesc[2][0], lateralSortedDesc[3][0]]

	panelCenter = obj.Shape.BoundBox.Center
	rot = obj.Placement.Rotation

	def localCenter(faceIdx):
		c = faces[faceIdx - 1].CenterOfMass.sub(panelCenter)
		return rot.inverted().multVec(c)

	def assignPair(idxA, idxB, labelPos, labelNeg):
		"""Assign labelPos to the face that is 'further along' the axis
		of greatest variation between the two opposite faces."""
		lA = localCenter(idxA)
		lB = localCenter(idxB)
		diff = lA.sub(lB)
		# pick the axis where the two faces differ the most
		axes = [("x", abs(diff.x)), ("y", abs(diff.y)), ("z", abs(diff.z))]
		axes.sort(key=lambda t: -t[1])
		axis = axes[0][0]
		vA = getattr(lA, axis)
		vB = getattr(lB, axis)
		if vA >= vB:
			return {idxA: labelPos, idxB: labelNeg}
		else:
			return {idxA: labelNeg, idxB: labelPos}

	sideMap = {}
	if len(longSidesIdxs) == 2:
		sideMap.update(assignPair(longSidesIdxs[0], longSidesIdxs[1], "Top", "Bottom"))
	if len(shortSidesIdxs) == 2:
		sideMap.update(assignPair(shortSidesIdxs[0], shortSidesIdxs[1], "Right", "Left"))

	return big, sideMap


SIDE_TO_INDEX = {"Top": 0, "Left": 1, "Bottom": 2, "Right": 3}


try:

	doc = FreeCAD.ActiveDocument
	if doc is None:
		raise Exception("no active document")

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

	lib = doc.getObject(LIBRARY_NAME)
	if lib is None or len(lib.Names) == 0:
		QtGui.QMessageBox.information(None,
			translate("bandApply", "No bands defined"),
			translate("bandApply",
				"There are no bands in the EdgeBand Library yet. "
				"Run the 'bandLibrary' tool first to define at least one "
				"named band (with its color)."))
		raise Exception("empty library")


	class QtMainClass(QtGui.QDialog):

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.pairs = pairs
			self.lib = lib

			self.setWindowTitle(translate("bandApply", "Apply edge band"))
			self.resize(380, 150)

			info = translate("bandApply",
				"Selected: ") + str(len(self.pairs)) + translate("bandApply",
				" face(s). The side (Top/Bottom/Left/Right) is auto-detected "
				"per face. A text label is placed on each valid face; the "
				"panel color is not changed. Wide grain faces are skipped.")
			self.infoL = QtGui.QLabel(info, self)
			self.infoL.setWordWrap(True)

			self.bandL = QtGui.QLabel(translate("bandApply", "Band:"), self)
			self.bandO = QtGui.QComboBox(self)
			for n in self.lib.Names:
				self.bandO.addItem(n)

			self.applyB = QtGui.QPushButton(translate("bandApply", "Apply"), self)
			self.applyB.clicked.connect(self.apply)
			self.cancelB = QtGui.QPushButton(translate("bandApply", "Cancel"), self)
			self.cancelB.clicked.connect(self.reject)

			topBar = QtGui.QHBoxLayout()
			topBar.addWidget(self.bandL)
			topBar.addWidget(self.bandO, 1)

			bottomBar = QtGui.QHBoxLayout()
			bottomBar.addStretch(1)
			bottomBar.addWidget(self.applyB)
			bottomBar.addWidget(self.cancelB)

			layout = QtGui.QVBoxLayout(self)
			layout.addWidget(self.infoL)
			layout.addLayout(topBar)
			layout.addLayout(bottomBar)

		def apply(self):
			bandName = self.bandO.currentText()
			if bandName == "":
				return

			# group selected faces by panel object
			byObj = {}
			for obj, faceIdx in self.pairs:
				byObj.setdefault(obj.Name, {"obj": obj, "faces": []})["faces"].append(faceIdx)

			skippedBig = []  # (panelLabel, faceIdx) for faces that were wide
			applied = 0

			for name, data in byObj.items():
				obj = data["obj"]
				bigIdxs, sideMap = classifyPanelFaces(obj)

				if not sideMap:
					skippedBig.extend([(obj.Label, idx) for idx in data["faces"]])
					continue

				ensureBandProps(obj)
				bands = list(obj.EdgeBand)
				faces = list(obj.EdgeBandFaces)

				for faceIdx in data["faces"]:
					if faceIdx in bigIdxs:
						skippedBig.append((obj.Label, faceIdx))
						continue
					side = sideMap.get(faceIdx)
					if side is None:
						# Face is neither big nor among the 4 detected sides
						# (e.g. a chamfer/fillet). Skip it.
						skippedBig.append((obj.Label, faceIdx))
						continue
					sideIdx = SIDE_TO_INDEX[side]
					# if this side was previously bound to a different face,
					# remove its old visual label
					oldFaceIdx = faces[sideIdx]
					if oldFaceIdx and oldFaceIdx != faceIdx:
						removeBandLabel(obj, oldFaceIdx)

					bands[sideIdx] = bandName
					faces[sideIdx] = faceIdx
					try:
						drawBandLabel(obj, faceIdx, obj.Shape.Faces[faceIdx - 1], side, bandName)
						applied += 1
					except Exception as e:
						FreeCAD.Console.PrintWarning(
							"bandApply: could not label face " + str(faceIdx)
							+ " of " + obj.Label + ": " + str(e) + "\n")

				obj.EdgeBand = bands
				obj.EdgeBandFaces = faces

			FreeCAD.ActiveDocument.recompute()
			FreeCADGui.Selection.clearSelection()

			if skippedBig:
				msg = translate("bandApply",
					"Applied band to ") + str(applied) + translate("bandApply",
					" face(s).\n\nSkipped (wide face or unrecognized lateral, "
					"bands must go on the thin edges):\n")
				for label, idx in skippedBig:
					msg += " - " + label + " Face" + str(idx) + "\n"
				QtGui.QMessageBox.information(self,
					translate("bandApply", "Some faces were skipped"), msg)
			self.accept()


	dlg = QtMainClass()
	dlg.exec_()

except Exception as e:

	info = translate("bandApply",
		"<b>Please select one or more thin edge faces of panels, "
		"then run this tool.</b><br><br>"
		"The side (Top / Left / Bottom / Right) is detected automatically "
		"from the panel geometry: the 2 widest faces of the panel are the "
		"grain faces (skipped), the 2 longest lateral faces are Top/Bottom, "
		"the 2 shortest lateral faces are Left/Right.<br><br>"
		"Each valid face is painted with the band color and the cutlist "
		"(getDimensions in 'a' mode) reports the band name in the "
		"corresponding column.<br><br>"
		"Define bands first with the bandLibrary tool.")
	MagicPanels.showInfo("bandApply", info)
