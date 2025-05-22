import FreeCAD
from PySide import QtGui
from PySide import QtCore

import MagicPanels

translate = FreeCAD.Qt.translate

gChange = dict()

try:

	objects = FreeCAD.ActiveDocument.Objects

	if len(objects) < 1:
		raise

	for o in objects:
		
		try:

			trans = MagicPanels.getColor(o, 0, "trans", "RGBA")

			if trans == 0:
				gChange[str(o.Name)] = "set"

			if trans == 83:
				gChange[str(o.Name)] = "unset"

		except:
			skip = 1

	for o in objects:

		try:

			if gChange[str(o.Name)] == "set":
				MagicPanels.setColor(o, 0, 83, "trans", "RGBA")

			if gChange[str(o.Name)] == "unset":
				MagicPanels.setColor(o, 0, 0, "trans", "RGBA")

		except:
			skip = 1

except:
	
	info = translate('makeTransparent', '<b>Please create an active document and at least one object to make it transparent. </b><br><br><b>Note:</b> This tool sets all available objects to transparent or restores normal visibility if they are already transparent. This allows you to temporarily set all furniture parts to transparent so that you can see all the dowels, screws, pilot holes or countersinks. If you click again, all furniture parts will return to normal. The transparency value used by this tool is 83, so do not set any furniture part to this number if you want to keep the glass part of the furniture transparent after this preview, for example.')

	MagicPanels.showInfo("makeTransparent", info)
