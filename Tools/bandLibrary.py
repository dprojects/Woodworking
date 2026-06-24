import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore

import MagicPanels

MagicPanels.initConfig()
translate = FreeCAD.Qt.translate


LIBRARY_NAME = "EdgeBandLibrary"


def getOrCreateLibrary(doc):
	obj = doc.getObject(LIBRARY_NAME)
	if obj is None:
		obj = doc.addObject("App::FeaturePython", LIBRARY_NAME)
		obj.Label = "EdgeBand Library"
		obj.addProperty("App::PropertyStringList", "Names", "EdgeBand",
			"Names of the edge band types defined in this document")
		obj.addProperty("App::PropertyStringList", "Colors", "EdgeBand",
			"Colors as 'R,G,B,A' (0-255) parallel to Names")
		obj.Names = []
		obj.Colors = []
	return obj


def parseRGBA(s):
	try:
		parts = [int(p.strip()) for p in s.split(",")]
		while len(parts) < 4:
			parts.append(255)
		return parts[:4]
	except:
		return [200, 200, 200, 255]


def formatRGBA(rgba):
	return ",".join(str(int(c)) for c in rgba)


try:

	doc = FreeCAD.ActiveDocument
	if doc is None:
		raise Exception("no active document")

	lib = getOrCreateLibrary(doc)


	class QtMainClass(QtGui.QDialog):

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.lib = lib

			self.setWindowTitle(translate("bandLibrary", "EdgeBand Library"))
			self.resize(420, 360)

			self.table = QtGui.QTableWidget(self)
			self.table.setColumnCount(2)
			self.table.setHorizontalHeaderLabels([
				translate("bandLibrary", "Name"),
				translate("bandLibrary", "Color"),
			])
			self.table.horizontalHeader().setStretchLastSection(False)
			self.table.setColumnWidth(0, 240)
			self.table.setColumnWidth(1, 130)
			self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

			self.addB = QtGui.QPushButton(translate("bandLibrary", "Add"), self)
			self.addB.clicked.connect(self.addRow)
			self.colorB = QtGui.QPushButton(translate("bandLibrary", "Pick color"), self)
			self.colorB.clicked.connect(self.pickColor)
			self.removeB = QtGui.QPushButton(translate("bandLibrary", "Remove"), self)
			self.removeB.clicked.connect(self.removeRow)

			self.okB = QtGui.QPushButton(translate("bandLibrary", "Save"), self)
			self.okB.clicked.connect(self.saveAndClose)
			self.cancelB = QtGui.QPushButton(translate("bandLibrary", "Cancel"), self)
			self.cancelB.clicked.connect(self.reject)

			topBar = QtGui.QHBoxLayout()
			topBar.addWidget(self.addB)
			topBar.addWidget(self.colorB)
			topBar.addWidget(self.removeB)
			topBar.addStretch(1)

			bottomBar = QtGui.QHBoxLayout()
			bottomBar.addStretch(1)
			bottomBar.addWidget(self.okB)
			bottomBar.addWidget(self.cancelB)

			layout = QtGui.QVBoxLayout(self)
			layout.addLayout(topBar)
			layout.addWidget(self.table)
			layout.addLayout(bottomBar)

			self.loadFromLib()

		def loadFromLib(self):
			names = list(self.lib.Names)
			colors = list(self.lib.Colors)
			self.table.setRowCount(len(names))
			for i, name in enumerate(names):
				rgba = parseRGBA(colors[i]) if i < len(colors) else [200, 200, 200, 255]
				self.setRow(i, name, rgba)

		def setRow(self, i, name, rgba):
			nameItem = QtGui.QTableWidgetItem(name)
			self.table.setItem(i, 0, nameItem)

			colorItem = QtGui.QTableWidgetItem(formatRGBA(rgba))
			colorItem.setBackground(QtGui.QColor(rgba[0], rgba[1], rgba[2]))
			colorItem.setFlags(colorItem.flags() & ~QtCore.Qt.ItemIsEditable)
			self.table.setItem(i, 1, colorItem)

		def addRow(self):
			i = self.table.rowCount()
			self.table.insertRow(i)
			self.setRow(i, "EdgeBand " + str(i + 1), [200, 200, 200, 255])
			self.table.selectRow(i)

		def pickColor(self):
			rows = self.table.selectionModel().selectedRows()
			if not rows:
				return
			i = rows[0].row()
			current = self.table.item(i, 1)
			rgba = parseRGBA(current.text()) if current else [200, 200, 200, 255]
			initial = QtGui.QColor(rgba[0], rgba[1], rgba[2])
			picked = QtGui.QColorDialog.getColor(initial, self,
				translate("bandLibrary", "Pick band color"))
			if picked.isValid():
				newRgba = [picked.red(), picked.green(), picked.blue(), 255]
				name = self.table.item(i, 0).text()
				self.setRow(i, name, newRgba)

		def removeRow(self):
			rows = sorted([r.row() for r in self.table.selectionModel().selectedRows()],
				reverse=True)
			for r in rows:
				self.table.removeRow(r)

		def saveAndClose(self):
			names = []
			colors = []
			for i in range(self.table.rowCount()):
				nameItem = self.table.item(i, 0)
				colorItem = self.table.item(i, 1)
				if nameItem is None:
					continue
				name = nameItem.text().strip()
				if name == "":
					continue
				if name in names:
					QtGui.QMessageBox.warning(self,
						translate("bandLibrary", "Duplicate name"),
						translate("bandLibrary", "Band names must be unique: ") + name)
					return
				names.append(name)
				colors.append(colorItem.text() if colorItem else "200,200,200,255")
			self.lib.Names = names
			self.lib.Colors = colors
			FreeCAD.ActiveDocument.recompute()
			self.accept()


	dlg = QtMainClass()
	dlg.exec_()

except Exception as e:

	info = translate("bandLibrary",
		"<b>EdgeBand Library</b><br><br>"
		"Manages the named edge band types available in this document. "
		"Each band has a name (used in the cutlist output) and a color "
		"(used to paint the panel face when the band is applied).<br><br>"
		"Open a document and run this tool to create / edit the library. "
		"The bands defined here are selectable in bandApply.")
	MagicPanels.showInfo("bandLibrary", info)
