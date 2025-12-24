import FreeCAD, FreeCADGui
import Draft
import MagicPanels

translate = FreeCAD.Qt.translate

# ########################################################################################################################
def setAttributes(iObj, iRefObjName, iRefEdgeName, iAxis, iAngleStep):

	if not hasattr(iObj, "Woodworking_Type"):
		info = translate("frontsOpenClose", "Object type for script parsing.")
		iObj.addProperty("App::PropertyString", "Woodworking_Type", "Woodworking", info)
		iObj.Woodworking_Type = "Front"

	if not hasattr(iObj, "Woodworking_Open"):
		info = translate("frontsOpenClose", "Allows to skip open simple front inside LinkGroup container and rotate whole LinkGroup container instead.")
		iObj.addProperty("App::PropertyBool", "Woodworking_Open", "Woodworking", info)
		iObj.Woodworking_Open = True

	if not hasattr(iObj, "Woodworking_OpenObj"):
		info = translate("frontsOpenClose", "Object name of the edge to open front. By default all objects with name starting with Front or front will be opened to left.")
		iObj.addProperty("App::PropertyString", "Woodworking_OpenObj", "Woodworking", info)
		iObj.Woodworking_OpenObj = iRefObjName
		
	if not hasattr(iObj, "Woodworking_OpenEdge"):
		info = translate("frontsOpenClose", "Edge name to open front as the CenterOfMass vector reference. Edge1 for left open. Edge5 for right open.")
		iObj.addProperty("App::PropertyString", "Woodworking_OpenEdge", "Woodworking", info)
		iObj.Woodworking_OpenEdge = iRefEdgeName
	
	if not hasattr(iObj, "Woodworking_OpenAxis"):
		info = translate("Woodworking_OpenAxis", "Axis to rotate front around. Possible strings: X, Y, Z.")
		iObj.addProperty("App::PropertyString", "Woodworking_OpenAxis", "Woodworking", info)
		iObj.Woodworking_OpenAxis = iAxis
		
	if not hasattr(iObj, "Woodworking_OpenAngleStep"):
		info = translate("Woodworking_OpenAngleStep", "Angle step to rotate front around. Negative value for left open rotate to other direction.")
		iObj.addProperty("App::PropertyFloat", "Woodworking_OpenAngleStep", "Woodworking", info)
		iObj.Woodworking_OpenAngleStep = iAngleStep

# ########################################################################################################################

try:

	selection = MagicPanels.getSelectedSubs(iConvert="no")

	if len(selection) == 0:
		
		objects = FreeCAD.ActiveDocument.Objects
		
		for o in objects:
			
			parse = False
			
			if o.Name.startswith("front") or o.Name.startswith("Front"):
				try:
					edgeObj = o
					edgeName = "Edge1"
					edge = o.getSubObject(edgeName)
					angle = -45
					axis = FreeCAD.Vector(0, 0, 1)
					v = edge.CenterOfMass
					
					parse = True
				except:
					skip = 1
		
			if hasattr(o, "Woodworking_Type") and o.Woodworking_Type == "Front":
				try:
					edgeObjName = o.Woodworking_OpenObj
					edgeName = o.Woodworking_OpenEdge
					edgeObj = FreeCAD.ActiveDocument.getObject(edgeObjName)
					edge = edgeObj.getSubObject(edgeName)
					angle = o.Woodworking_OpenAngleStep
					axis = o.Woodworking_OpenAxis
					
					if axis == "X":
						axis = FreeCAD.Vector(1, 0, 0)
					elif axis == "Y":
						axis = FreeCAD.Vector(0, 1, 0)
					else:
						axis = FreeCAD.Vector(0, 0, 1)
					
					v = edge.CenterOfMass
			
					parse = True
				except:
					skip = 1
				
			if hasattr(o, "Woodworking_Open") and o.Woodworking_Open == False:
				parse = False

			if parse == True:
				Draft.rotate(o, angle, v, axis, False)
	else:
		
		parse = True
		
		# selected LinkGroup with front and handle inside
		obs = FreeCADGui.Selection.getSelection()
		if len(obs) == 2:
			if obs[0].isDerivedFrom("App::LinkGroup"):
				
				o = obs[0]
				refObjName = str(obs[1].Name)
				sub = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				subIndex = MagicPanels.getEdgeIndex(obs[1], sub)
				subName = "Edge" + str(subIndex)
				angle = -45
				if subName == "Edge5":
					angle = 45
		
				setAttributes(o, refObjName, subName, "Z", angle)
				
				FreeCADGui.Selection.clearSelection()
				FreeCAD.ActiveDocument.recompute()
				parse = False

		# only selected edges for simple fronts
		if parse == True:
			
			[ subs, objects ] = MagicPanels.getSelectedSubs(iConvert="no")

			i = -1
			for sub in subs:
				i = i + 1
				if sub.ShapeType != "Edge":
					continue
				
				o = objects[i]
				
				subIndex = MagicPanels.getEdgeIndex(o, sub)
				subName = "Edge" + str(subIndex)
				angle = -45
				if subName == "Edge5":
					angle = 45
			
				setAttributes(o, str(o.Name), subName, "Z", angle)
			
	FreeCADGui.Selection.clearSelection()
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""
	
	info += translate('frontsOpenClose', 'Possible selection methods: <ul><li><b>no selection</b> - allows you to open all fronts. If the objects name starts with "front" or "Front" this front will be open by default via Edge1 to the left side.</li><li><b>edges</b> - you have to select single edge for each front to add open front attributes to each front. This allows you to change default left open to right open.</li><li><b>LinkGroup + edge of simple front inside</b> - allows you to set rotation attributes to LinkGroup container with handle and simple front inside, to rotate whole LinkGroup container with handle but via edge of simple front inside. In this case you must also set attributes to simple front inside but turn off open of the simple front inside to not duplicate rotation.</li></ul><br><br><b>Note:</b> This tool allows you to open and close all cabinet fronts simultaneously. This allows you to quickly view the cabinets internal structure without having to search for each front in the object tree and hide or rotate them individually. The fronts rotate with a default rotation increment of 45 degrees. This allows you to select the front opening angle, from a simple tilt to an open inner front that can open beyond 90 degrees. Rotating the fronts around the Z axis avoids the issue of maximum opening angles for different hinge types. However, the opening of the fronts can be customized by editing the attributes for each front. Opening attributes can also be added to each front using this tool. To select more edges or objects hold left CTRL key during selection.')

	MagicPanels.showInfo("frontsOpenClose", info)

