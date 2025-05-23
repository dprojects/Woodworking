import FreeCAD
from PySide import QtGui
from PySide import QtCore

import MagicPanels

translate = FreeCAD.Qt.translate

gChange = dict()
gFaces = dict()

try:

	objects = FreeCAD.ActiveDocument.Objects

	if len(objects) < 1:
		raise

	for o in objects:
		
		try:
			
			# since new color schema if you change Body transparency
			# the Pad inherits color from Body... 
			if (
				o.isDerivedFrom("App::LinkGroup") or 
				o.isDerivedFrom("App::Link") or 
				o.isDerivedFrom("App::Part") or 
				o.isDerivedFrom("PartDesign::Body") or 
				o.isDerivedFrom("Sketcher::SketchObject")
			):
				continue
			
			gFaces[str(o.Name)] = []
			
			trans = MagicPanels.getColor(o, 0, "trans", "RGBA")
			if trans == "":
				
				gChange[str(o.Name)] = "faces"
				
				for i in range(0, len(o.Shape.Faces)):
					
					face = MagicPanels.getColor(o, i+1, "trans", "RGBA")
					
					if face == 0:
						gFaces[str(o.Name)].append(83)
					elif face == 83:
						gFaces[str(o.Name)].append(0)
					else:
						gFaces[str(o.Name)].append(face)
						
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
			
			if gChange[str(o.Name)] == "faces":
				for i in range(0, len(o.Shape.Faces)):
					face = gFaces[str(o.Name)][i]
					MagicPanels.setColor(o, i+1, face, "trans", "RGBA")
		except:
			skip = 1

except:
	
	info = translate('makeTransparent', '<b>Please create an active document and at least one object to make it transparent. </b><br><br><b>Note:</b> This tool sets all available objects to transparent or restores normal visibility if they are already transparent. This allows you to temporarily set all furniture parts to transparent so that you can see all the dowels, screws, pilot holes or countersinks. If you click again, all furniture parts will return to normal. The transparency value used by this tool is 83, so do not set any furniture part to this number if you want to keep the glass part of the furniture transparent after this preview, for example.')

	MagicPanels.showInfo("makeTransparent", info)
