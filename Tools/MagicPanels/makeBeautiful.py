import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	
	objects = FreeCAD.ActiveDocument.Objects

	if len(objects) < 1:
		raise
		
	# settings
	origLineWidth = 2
	origPointSize = 2
	
	newLineWidth = 1
	newPointSize = 1

	# variables
	toChange = []
	dbLineWidth = dict()
	dbPointSize = dict()

	# prepare db for objects to change
	for o in objects:

		try:
			test = o.ViewObject.LineWidth
			test = o.ViewObject.PointSize
		except:
			continue

		key = str(o.Name)
		toChange.append(o)

		dbLineWidth[key] = o.ViewObject.LineWidth
		dbPointSize[key] = o.ViewObject.PointSize

	# change
	for o in toChange:
		try:
			key = str(o.Name)
			
			# LineWidth
			if dbLineWidth[key] == origLineWidth:
				o.ViewObject.LineWidth = newLineWidth
			else:
				o.ViewObject.LineWidth = origLineWidth

			# PointSize
			if dbPointSize[key] == origPointSize:
				o.ViewObject.PointSize = newPointSize
			else:
				o.ViewObject.PointSize = origPointSize

		except:
			skip = 1

except:
	
	info = translate('makeBeautiful', 'This tool change all objects look, make edges and vertices smaller to look better at screenshots. If you click it again all objects will be changed to default values.')
	
	MagicPanels.showInfo("makeBeautiful", info)
