import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCADGui.Selection.getSelection()

	if len(objects) < 1:
		raise

	FreeCAD.ActiveDocument.openTransaction("selected2Assembly")

	assemblyParts = []

	for o in objects:
		
		if o.isDerivedFrom("Part::Box"):
			
			# switch object to global position
			[ x, y, z ] = MagicPanels.getPosition(o, "global")
			MagicPanels.setPosition(o, x, y, z, "global")
			
			# convert to Pad
			alabel = str(o.Label)
			o.Label = "old_"+alabel
			[ part, body, sketch, pad ] = MagicPanels.makePad(o, alabel)
			FreeCAD.ActiveDocument.removeObject(o.Name)
			FreeCAD.ActiveDocument.recompute()
		
			# move Body out from Part container
			part.ViewObject.dragObject(body)
			FreeCAD.ActiveDocument.removeObject(part.Name)
			FreeCAD.ActiveDocument.recompute()
			
			# final clean, remove empty LinkGroups
			for linkgroup in FreeCAD.ActiveDocument.Objects:
				if linkgroup.isDerivedFrom("App::LinkGroup"):
					if linkgroup.ElementList == []:
						FreeCAD.ActiveDocument.removeObject(linkgroup.Name)

			assemblyParts.append(body)

	# create assembly
	assembly = FreeCAD.ActiveDocument.addObject('Assembly::AssemblyObject', "Assembly")
	joints = FreeCAD.ActiveDocument.addObject('Assembly::JointGroup','Joints')
	assemblyParts.append(joints)
	assembly.Group = assemblyParts

	assembly.recompute()
	FreeCAD.ActiveDocument.recompute()
	FreeCADGui.ActiveDocument.ActiveView.setActiveObject('part', assembly)

	FreeCAD.ActiveDocument.commitTransaction()

except:
	
	info = ""
	
	info += translate('selected2Assembly', '<b>To convert a model to an Assembly object, you must first select FreeCAD Part :: Box objects to convert.</b><br><br>This tool allows you to convert a simple model based on simple panels, i.e. FreeCAD Part :: Box objects, to an Assembly model. Manually, such conversion could be done by converting Part :: Box objects to PartDesign :: Pad objects using the panel2pad tool and then extracting PartDesign :: Body objects using selected2Outside to keep global position and moving them to the Assembly :: AssemblyObject object. In this tool, these two tools are combined for ease and speed of conversion. However, if you have a problem with converting the model, you can still do such conversion manually.')

	MagicPanels.showInfo("selected2Assembly", info)

