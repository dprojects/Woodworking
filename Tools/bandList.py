import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore

import MagicPanels

MagicPanels.initConfig()
translate = FreeCAD.Qt.translate


SIDES = ["Top", "Left", "Bottom", "Right"]


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


def removeBandLabel(obj, faceIdx):
	label = str(obj.Label) + ", Face" + str(faceIdx) + ", EdgeBand "
	try:
		for rmo in FreeCAD.ActiveDocument.getObjectsByLabel(label):
			FreeCAD.ActiveDocument.removeObject(rmo.Name)
	except:
		pass


def clearAllBandsOnObject(obj):
	"""Clear every assigned band on obj, restore color and remove labels."""
	if not hasattr(obj, "EdgeBand") or not hasattr(obj, "EdgeBandFaces"):
		return 0
	bands = list(obj.EdgeBand)
	faces = list(obj.EdgeBandFaces)
	restoreColor = baseColorRGBA(obj)
	cleared = 0
	for side in range(min(4, len(faces))):
		faceIdx = faces[side]
		if faceIdx and bands[side] != "":
			try:
				MagicPanels.setColor(obj, faceIdx, restoreColor, "color", "RGBA")
			except Exception as e:
				FreeCAD.Console.PrintWarning(
					"bandList: could not restore color of face "
					+ str(faceIdx) + " of " + obj.Label + ": "
					+ str(e) + "\n")
			removeBandLabel(obj, faceIdx)
			bands[side] = ""
			faces[side] = 0
			cleared += 1
	obj.EdgeBand = bands
	obj.EdgeBandFaces = faces
	return cleared


def collectBandedObjects(doc):
	"""Returns list of dicts: {obj, bands[4], faces[4]} for every object with
	at least one assigned band."""
	out = []
	for obj in doc.Objects:
		if not hasattr(obj, "EdgeBand"):
			continue
		bands = list(obj.EdgeBand)
		if len(bands) < 4:
			continue
		if not any(b for b in bands):
			continue
		faces = list(obj.EdgeBandFaces) if hasattr(obj, "EdgeBandFaces") else [0, 0, 0, 0]
		while len(faces) < 4:
			faces.append(0)
		out.append({"obj": obj, "bands": bands, "faces": faces})
	return out


try:

	doc = FreeCAD.ActiveDocument
	if doc is None:
		raise Exception("no active document")

	entries = collectBandedObjects(doc)


	class QtMainClass(QtGui.QDialog):

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.entries = entries

			self.setWindowTitle(translate("bandList", "Edge bands in document"))
			self.resize(640, 420)

			self.infoL = QtGui.QLabel(
				translate("bandList", "Panels with at least one edge band assigned: ")
				+ str(len(self.entries)), self)

			self.table = QtGui.QTableWidget(self)
			headers = ["Panel", "Top", "Left", "Bottom", "Right"]
			self.table.setColumnCount(len(headers))
			self.table.setHorizontalHeaderLabels(headers)
			self.table.setColumnWidth(0, 240)
			for i in range(1, 5):
				self.table.setColumnWidth(i, 90)
			self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
			self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
			self.populateTable()

			self.selectB = QtGui.QPushButton(
				translate("bandList", "Select in 3D"), self)
			self.selectB.clicked.connect(self.selectIn3D)

			self.clearB = QtGui.QPushButton(
				translate("bandList", "Clear bands on selected rows"), self)
			self.clearB.clicked.connect(self.clearSelected)

			self.refreshB = QtGui.QPushButton(
				translate("bandList", "Refresh"), self)
			self.refreshB.clicked.connect(self.refresh)

			self.closeB = QtGui.QPushButton(
				translate("bandList", "Close"), self)
			self.closeB.clicked.connect(self.accept)

			bar = QtGui.QHBoxLayout()
			bar.addWidget(self.selectB)
			bar.addWidget(self.clearB)
			bar.addWidget(self.refreshB)
			bar.addStretch(1)
			bar.addWidget(self.closeB)

			layout = QtGui.QVBoxLayout(self)
			layout.addWidget(self.infoL)
			layout.addWidget(self.table)
			layout.addLayout(bar)

		def populateTable(self):
			self.table.setRowCount(len(self.entries))
			for i, e in enumerate(self.entries):
				panelItem = QtGui.QTableWidgetItem(e["obj"].Label)
				self.table.setItem(i, 0, panelItem)
				for j, side in enumerate(SIDES):
					b = e["bands"][j]
					f = e["faces"][j]
					if b:
						txt = b + "  (F" + str(f) + ")"
					else:
						txt = "—"
					item = QtGui.QTableWidgetItem(txt)
					if not b:
						item.setForeground(QtGui.QColor(150, 150, 150))
					self.table.setItem(i, 1 + j, item)

		def selectedEntries(self):
			rows = sorted({idx.row() for idx in self.table.selectionModel().selectedRows()})
			return [self.entries[r] for r in rows if r < len(self.entries)]

		def selectIn3D(self):
			sel = self.selectedEntries()
			if not sel:
				return
			FreeCADGui.Selection.clearSelection()
			for e in sel:
				FreeCADGui.Selection.addSelection(e["obj"])

		def clearSelected(self):
			sel = self.selectedEntries()
			if not sel:
				return
			ans = QtGui.QMessageBox.question(self,
				translate("bandList", "Clear bands"),
				translate("bandList",
					"Clear all bands on ") + str(len(sel)) + translate("bandList",
					" panel(s)? This also removes the visual labels and "
					"restores the face color."),
				QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
			if ans != QtGui.QMessageBox.Yes:
				return
			total = 0
			for e in sel:
				total += clearAllBandsOnObject(e["obj"])
			FreeCAD.ActiveDocument.recompute()
			self.refresh()
			QtGui.QMessageBox.information(self,
				translate("bandList", "Done"),
				translate("bandList", "Cleared ") + str(total)
				+ translate("bandList", " band assignment(s)."))

		def refresh(self):
			self.entries = collectBandedObjects(FreeCAD.ActiveDocument)
			self.infoL.setText(
				translate("bandList", "Panels with at least one edge band assigned: ")
				+ str(len(self.entries)))
			self.populateTable()


	dlg = QtMainClass()
	dlg.exec_()

except Exception as e:

	info = translate("bandList",
		"<b>Edge Band List</b><br><br>"
		"Lists every panel in the active document that has at least one edge "
		"band assigned, with the band name and side. Use the buttons to "
		"select the affected panel(s) in the 3D view, or to clear all bands "
		"on selected rows (restores face color and removes the visual label)."
		"<br><br>"
		"Open a document first.")
	MagicPanels.showInfo("bandList", info)
