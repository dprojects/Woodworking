import FreeCAD, FreeCADGui, Draft
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()
	
	if len(objects) < 2:
		raise
	
	i = 0
	for o in objects:
		
		FreeCAD.ActiveDocument.openTransaction("panel2clone "+str(o.Label))
		
		i = i + 1
		
		if i == 1:
			base = o
			continue
		
		clone = Draft.make_clone(base)
		clone.Label = MagicPanels.getNestingLabel(o, "Clone")
		
		[ x, y, z, r ] = MagicPanels.getPlacement(o)
		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(o)
		x = x + coX
		y = y + coY
		z = z + coZ
		MagicPanels.setPlacement(clone, x, y, z, r)
		MagicPanels.moveToFirst([ clone ], o)
		
		FreeCAD.ActiveDocument.removeObject(str(o.Name))
		FreeCAD.ActiveDocument.commitTransaction()
		
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('panel2clone', '<b>Please select valid object to be cloned, next selected objects will be replaced with clones. </b><br><br><b>Note:</b> This tool allows to replace simple objects with any detailed object, e.g. Cylinders with realistic looking screws. First you have to select detailed object and than simple object that will be replaced with Clones. The first selected detailed object can be Part, LinkGroup or any other created manually or merged with your project. You can replace more than one simple object at once with Clone. To select more objects hold left CTRL key during selection. The simple objects should imitate the detailed object to replace all of them in-place with realistic looking one. This tool works with the same way as panel2link but instead of Link it creates Clone objects. It can be useful if you want to remove the base object and have clean objects Tree. Also if you want to change each copy separately. ')

	info += translate('panel2clone', 'For more details please see:')
	info += ' ' + '<a href="https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture">'
	info += translate('panel2clone', 'fixture.')
	info += '</a>'

	MagicPanels.showInfo("panel2clone", info)
