import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	
	objects = FreeCADGui.Selection.getSelection()
	
	if len(objects) < 2:
		raise
	
	i = 0
	for o in objects:
		
		i = i + 1
		
		if i == 1:
			base = o
			continue
		
		linkName = "Link_" + str(o.Name)
		link = FreeCAD.activeDocument().addObject('App::Link', linkName)
		link.setLink(base)
		link.Label = "Link, " + o.Label
		
		[ x, y, z, r ] = MagicPanels.getPlacement(o)
		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(o)
		x = x + coX
		y = y + coY
		z = z + coZ
		MagicPanels.setPlacement(link, x, y, z, r)
		MagicPanels.moveToFirst([ link ], o)
		
		FreeCAD.ActiveDocument.removeObject(str(o.Name))
		FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('panel2linkInfo', '<b>Please select valid object to be linked, next selected objects will be replaced with Links. </b><br><br><b>Note:</b> This tool allows to replace simple objects with any detailed object, e.g. Cylinders with realistic looking screws. First you have to select detailed object and than simple object that will be replaced with Link. The first selected detailed object can be Part, LinkGroup or any other created manually or merged with your project. You can replace more than one simple object at once with Link. To select more objects hold left CTRL key during selection. The simple objects should imitate the detailed object to replace all of them in-place with realistic looking one. ')

	info += translate('panel2linkInfo', 'For more details please see:')
	info += ' ' + '<a href="https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture">'
	info += translate('panel2linkInfo', 'fixture.')
	info += '</a>'

	MagicPanels.showInfo("panel2link", info)
