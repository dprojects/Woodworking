import FreeCAD, FreeCADGui
import os, glob
from PySide import QtGui, QtCore

import MagicPanels

MagicPanels.initConfig()
translate = FreeCAD.Qt.translate


CLEAR_LABEL = "(none / clear)"


def materialDir():
	"""Find the user's FreeCAD Material/ folder (Flatpak / standard / XDG)."""
	for p in (
		"~/.var/app/org.freecad.FreeCAD/data/FreeCAD/v1-1/Material",
		"~/.var/app/org.freecad.FreeCAD/data/FreeCAD/Material",
		"~/.FreeCAD/Material",
		"~/.local/share/FreeCAD/Material",
	):
		p = os.path.expanduser(p)
		if os.path.isdir(p):
			return p
	return os.path.expanduser("~/.FreeCAD/Material")


def parseFCMat(path):
	"""Returns (name, (r,g,b,a) floats 0-1) parsed from a YAML .FCMat file."""
	name = os.path.splitext(os.path.basename(path))[0]
	color = (0.8, 0.8, 0.8, 1.0)
	in_general = False
	in_appearance = False
	try:
		with open(path) as f:
			for raw in f:
				line = raw.rstrip("\n")
				stripped = line.strip()
				# track top-level section
				if not line.startswith(" ") and stripped.endswith(":"):
					section = stripped[:-1]
					in_general = (section == "General")
					in_appearance = (section == "AppearanceModels")
					continue
				if in_general and stripped.startswith("Name:"):
					v = stripped.split(":", 1)[1].strip().strip('"').strip("'")
					if v:
						name = v
				if in_appearance and stripped.startswith("DiffuseColor:"):
					v = stripped.split(":", 1)[1].strip().strip('"').strip("'").strip("()")
					try:
						parts = [float(p.strip()) for p in v.split(",")]
						while len(parts) < 4:
							parts.append(1.0)
						color = tuple(parts[:4])
					except:
						pass
	except:
		pass
	return name, color


def scanMaterials():
	"""Returns sorted list of (relpath, fullpath, name, color)."""
	base = materialDir()
	if not os.path.isdir(base):
		return []
	out = []
	for full in sorted(glob.glob(os.path.join(base, "**", "*.FCMat"), recursive=True)):
		rel = os.path.relpath(full, base)
		name, color = parseFCMat(full)
		out.append((rel, full, name, color))
	return out


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

	sel = FreeCADGui.Selection.getSelection()
	if not sel:
		raise Exception("no selection")

	materials = scanMaterials()


	class QtMainClass(QtGui.QDialog):

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.setWindowTitle(translate("panelMaterial", "Apply material & appearance"))
			self.resize(440, 170)

			self.infoL = QtGui.QLabel(
				translate("panelMaterial", "Apply to ") + str(len(sel))
				+ translate("panelMaterial", " panel(s). Sets ShapeMaterial.Name and paints the whole panel with the material's DiffuseColor."),
				self)
			self.infoL.setWordWrap(True)

			self.matL = QtGui.QLabel(translate("panelMaterial", "Material:"), self)
			self.matO = QtGui.QComboBox(self)
			self.matO.addItem(CLEAR_LABEL)
			for rel, full, name, color in materials:
				self.matO.addItem(rel)
			if not materials:
				self.matO.setEnabled(False)
				self.infoL.setText(self.infoL.text() + "\n\n"
					+ translate("panelMaterial",
					"No .FCMat files found in ") + materialDir()
					+ translate("panelMaterial",
					". Create materials first via View > Appearance > Material."))

			self.applyB = QtGui.QPushButton(translate("panelMaterial", "Apply"), self)
			self.applyB.clicked.connect(self.applyMaterial)
			self.cancelB = QtGui.QPushButton(translate("panelMaterial", "Cancel"), self)
			self.cancelB.clicked.connect(self.reject)

			row = QtGui.QHBoxLayout()
			row.addWidget(self.matL)
			row.addWidget(self.matO, 1)

			bar = QtGui.QHBoxLayout()
			bar.addStretch(1)
			bar.addWidget(self.applyB)
			bar.addWidget(self.cancelB)

			layout = QtGui.QVBoxLayout(self)
			layout.addWidget(self.infoL)
			layout.addLayout(row)
			layout.addLayout(bar)

		def applyMaterial(self):
			choice = self.matO.currentText()

			if choice == CLEAR_LABEL:
				# clear material + restore a neutral grey color
				neutral = [204, 204, 204, 255]
				for obj in sel:
					try:
						if hasattr(obj, "ShapeMaterial"):
							m = obj.ShapeMaterial
							m.Name = "Default"
							obj.ShapeMaterial = m
					except:
						pass
					try:
						MagicPanels.setColor(obj, 0, neutral, "color", "RGBA")
					except:
						pass
				FreeCAD.ActiveDocument.recompute()
				self.accept()
				return

			# find selected entry
			idx = self.matO.currentIndex() - 1  # offset for clear entry
			if idx < 0 or idx >= len(materials):
				return
			rel, full, name, color = materials[idx]
			rgba255 = [int(round(c * 255)) for c in color]

			for obj in sel:
				# set ShapeMaterial.Name (legacy + reported by setDBApproximation)
				try:
					if hasattr(obj, "ShapeMaterial"):
						m = obj.ShapeMaterial
						m.Name = name
						obj.ShapeMaterial = m
				except Exception as e:
					FreeCAD.Console.PrintWarning(
						"panelMaterial: ShapeMaterial skip on " + obj.Label
						+ ": " + str(e) + "\n")

				# paint all faces with the material's diffuse color
				try:
					MagicPanels.setColor(obj, 0, rgba255, "color", "RGBA")
				except Exception as e:
					FreeCAD.Console.PrintWarning(
						"panelMaterial: color skip on " + obj.Label
						+ ": " + str(e) + "\n")

			FreeCAD.ActiveDocument.recompute()
			self.accept()


	dlg = QtMainClass()
	dlg.exec_()

except Exception as e:

	info = translate("panelMaterial",
		"<b>Select one or more panels, then run this tool.</b><br><br>"
		"Lists every .FCMat file in your FreeCAD user Material folder "
		"and, in one click, applies the chosen material's name to "
		"<code>ShapeMaterial.Name</code> (read by getDimensions for the "
		"Material column in mode 'a') AND paints the panel with the "
		"material's DiffuseColor.<br><br>"
		"Choose '(none / clear)' to reset material name and color.")
	MagicPanels.showInfo("panelMaterial", info)
