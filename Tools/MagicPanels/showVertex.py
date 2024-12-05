import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	
	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 1:
		if len(FreeCAD.ActiveDocument.Objects) < 1:
			raise
		else:
			objects = FreeCAD.ActiveDocument.Objects

	# settings
	setPointSize = 10
	setPointColor = (1.0, 0.0, 0.0, 0.0)

	restorePointSize = 2
	restorePointColor = (0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.0)

	# variables
	toChange = []
	pointSize = dict()
	pointColor = dict()

	# prepare db for objects to change
	for o in objects:

		try:
			test = o.ViewObject.PointSize
			test = o.ViewObject.PointColor
		except:
			continue

		key = str(o.Name)
		toChange.append(o)

		pointSize[key] = o.ViewObject.PointSize
		pointColor[key] = o.ViewObject.PointColor

	# change
	for o in toChange:
		try:
			key = str(o.Name)
			
			# size
			if pointSize[key] == setPointSize:
				o.ViewObject.PointSize = restorePointSize
			else:
				o.ViewObject.PointSize = setPointSize

			# color
			if pointColor[key] == setPointColor:
				o.ViewObject.PointColor = restorePointColor
			else:
				o.ViewObject.PointColor = setPointColor

		except:
			skip = 1

except:
	
	info = translate('showVertex', '<b>Please create object to resize vertices for easier selection. </b><br><br><b>Note:</b> This tool allows you to resize all vertices for selected objects or for all objects if there is no selected objects. Resized vertices are easier to select. This tool also change vertices color to red for better visibility. If the object have already resized or red vertices it will be changed back to normal. So, you can keep the model good looking with small vertices and if you have problem with vertices selection, you can quickly resize vertices for selection purposes only and back to normal later.')
	
	MagicPanels.showInfo("showVertex", info)
