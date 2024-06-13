import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	
	gObserver = ""
	
	if len(FreeCAD.ActiveDocument.Objects) < 1:
		raise

	# ###############################################################
	# Observer class
	# ###############################################################

	class SelectionObserver:
		
		def addSelection(self, doc, obj, sub, pos):
			
			if sub.find("Edge") != -1 or sub.find("Face") != -1:
				
				vpos = FreeCAD.Vector(pos)
				o = FreeCAD.ActiveDocument.getObject(obj)
				
				ves = MagicPanels.touchTypo(o.Shape)
				ves = MagicPanels.getVerticesPosition(ves, o)
				
				minVertexName = ""
				minOffset = ""
				
				i = 0
				for v in ves:

					fv = FreeCAD.Vector(v.X, v.Y, v.Z)
					offset = vpos.distanceToPoint(fv)

					if minOffset == "":
						minOffset = offset
						minVertexName = "Vertex"+str(i+1)

					else:
						if offset < minOffset:
							minOffset = offset
							minVertexName = "Vertex"+str(i+1)

					i = i + 1

				FreeCADGui.Selection.removeSelection(o, sub)
				FreeCADGui.Selection.addSelection(o, minVertexName)
				if gObserver != "":
					FreeCADGui.Selection.removeObserver(gObserver)

			else:
				if gObserver != "":
					FreeCADGui.Selection.removeObserver(gObserver)
			
		def setPreselection(self, doc, obj, sub):
			skip = 1

	# ###############################################################
	# main call
	# ###############################################################

	gObserver = SelectionObserver()
	FreeCADGui.Selection.addObserver(gObserver)

except:
	
	if gObserver != "":
		FreeCADGui.Selection.removeObserver(gObserver)
	
	info = translate('selectVertex', '<b>Please select Face or Edge to select nearest Vertex. </b><br><br><b>Note:</b> This tool helps vertex selection. If you click this tool icon the tool activates observer and listen for your selection. If you select Face or Edge the nearest Vertex will be selected instead. If you select Vertex the Vertex will stay selected. The observer is closed after selection so this help works only once to not disturb face or edge selection later. If you want select more vertices with help of this tool, you have to hold left CTRL key during Edge or Face selection, you can also hold it during icon click. ')
	
	MagicPanels.showInfo("selectVertex", info)
