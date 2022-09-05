import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate


try:

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 1:
		raise

	FreeCADGui.Selection.clearSelection()
	
	for o in objects:
		
		try:
			
			base = MagicPanels.getReference(o)
			sketch = base.Profile[0]
			
		except:
			continue
		
		for c in sketch.Constraints:
			if not MagicPanels.equal(float(c.Value), float(0)):
				
				i = 0
				for e in o.Shape.Edges:
					
					edge = o.Shape.Edges[i]
					i = i + 1
					
					if MagicPanels.equal(float(edge.Length), float(c.Value)):
						FreeCADGui.Selection.addSelection(o, 'Edge'+str(i))

except:
	
	info = ""
	
	info += translate('showConstraints', '<b>Please select objects to see edges with the same size as defined constraints. </b><br><br><b>Note:</b> This tool search all constraints for selected objects. If the constraints is non-zero this tool search for all edges with the same size. It allows for quick preview if all the edges are defined by the Sketch. However, in some cases, if the constraints is offset and it is equal edge size this will give false result. To select more objects hold left CTRL key during selection. ')

	MagicPanels.showInfo("showConstraints", info)
