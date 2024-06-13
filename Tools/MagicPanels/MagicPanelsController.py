# ###################################################################################################################
#
# Functions to handle many toolbar icons without code duplication. Should not be used for single icon click. 
# For single icon use dedicated file to not make this library too big, and slow to load.
#
# The functions below have error handling and pop-ups, so not call it in loop, or from other functions 
# because you get many pop-ups in case of error. No need to return anything for further processing.
#
# ###################################################################################################################


import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate


# ###################################################################################################################
def panelDefault(iType):
	
	try:

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panel"+iType)

		if iType == "XY":
			panel.Length = 600
			panel.Width = 300
			panel.Height = 18

		if iType == "YX":
			panel.Length = 300
			panel.Width = 600
			panel.Height = 18

		if iType == "XZ":
			panel.Length = 600
			panel.Width = 18
			panel.Height = 300

		if iType == "ZX":
			panel.Length = 300
			panel.Width = 18
			panel.Height = 600

		if iType == "YZ":
			panel.Length = 18
			panel.Width = 600
			panel.Height = 300

		if iType == "ZY":
			panel.Length = 18
			panel.Width = 300
			panel.Height = 600

		color = (247 / 255, 185 / 255, 108 / 255, 0.0)
		panel.ViewObject.ShapeColor = color

		FreeCAD.ActiveDocument.recompute()
	
	except:
	
		info = ""
		
		info += translate('panelDefault', '<b>To create default panel, first create active document. </b><br><br><b>Note:</b> This tool creates default panel that can be easily resized. You can clearly see where should be the thickness to keep exact panel XYZ axis orientation. All furniture elements should be created according to the XYZ axis plane, if possible. Avoid building whole furniture with rotated elements. If you want to rotate panel with dowels, better create panel with dowels without rotation, pack panel with dowels into LinkGroup, and use magicAngle to rotate whole LinkGroup. You can rotate whole furniture like this with single click.')

		MagicPanels.showInfo("panelDefault"+iType, info)


# ###################################################################################################################
def panelCopy(iType):
	
	try:

		objRef = MagicPanels.getReference()
		
		[ Length, Width, Height ] = MagicPanels.sizesToCubePanel(objRef, iType)
		
		panel = FreeCAD.activeDocument().addObject("Part::Box", "panel"+iType)
		[ panel.Length, panel.Width, panel.Height ] = [ Length, Width, Height ]

		try:
			MagicPanels.copyColors(objRef, panel)
		except:
			skip = 1

		FreeCAD.ActiveDocument.recompute()

	except:

		info = ""
		
		info += translate('panelCopy', '<b>To create copy of panel in exact direction, select valid panel first. </b><br><br><b>Note:</b> This tool copy selected panel into exact XYZ axis orientation. By default you can copy any panel based on Cube object. If you want to copy Pad, you need to have Constraints named "SizeX" and "SizeY" at the Sketch. For custom objects types you need to have Length, Width, Height properties at object (Group: "Base", Type: "App::PropertyLength"). The new panel will be created at (0, 0, 0) coordinate XYZ axis position. You can use mapPosition tool to move the new panel to the original panel position. To copy panel without changing orientation, you can use magicMove tool or CTRL-C and CTRL-V keys with arrows to move the copy.') 

		MagicPanels.showInfo("panelCopy"+iType, info)


# ###################################################################################################################
def panelFace(iType):
	
	try:

		selection = FreeCADGui.Selection.getSelection()[0]
		
		objRef = MagicPanels.getReference(selection)
		face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		
		[ L, W, H ] = MagicPanels.sizesToCubePanel(objRef, iType)
		
		if objRef.isDerivedFrom("Part::Box"):
			[ x, y, z ] = MagicPanels.getVertex(face, 0, 1)
		else:
			[ x, y, z ] = MagicPanels.getVertex(face, 1, 0)
		
		if selection.isDerivedFrom("Part::Cut"):
			[ x, y, z ] = MagicPanels.getVertex(face, 2, 0)

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelFace"+iType)
		panel.Length, panel.Width, panel.Height = L, W, H

		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(objRef)
		x = x + coX
		y = y + coY
		z = z + coZ
		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
		
		MagicPanels.addRotation(objRef, [ panel ])
		
		try:
			MagicPanels.copyColors(objRef, panel)
		except:
			skip = 1
			
		FreeCAD.ActiveDocument.recompute()
		MagicPanels.moveToFirst([ panel ], objRef)

	except:
		
		info = ""
		
		info += translate('panelFace', '<b>Please select face to create panel. </b><br><br><b>Note:</b> This tool creates new panel at selected face. The blue panel represents the selected object and the red one represents the new created object. The icon refers to base XY model view (0 key position). Click fitModel to set model into referred view. The new created panel will get the same dimensions as panel of the selected face. If you have problem with unpredicted result, use magicManager tool to preview panel before creation.')

		MagicPanels.showInfo("panelFace"+iType, info)


# ###################################################################################################################
def panelBetween(iType):
	
	try:

		obj1Ref = MagicPanels.getReference(FreeCADGui.Selection.getSelection()[0])
		obj2Ref = MagicPanels.getReference(FreeCADGui.Selection.getSelection()[1])

		face1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		face2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
	
		[ x1, y1, z1 ] = MagicPanels.getVertex(face1, 0, 1)
		[ x2, y2, z2 ] = MagicPanels.getVertex(face2, 0, 1)

		# add cointainer offset for PartDesign object and skip Cut
		if not obj1Ref.isDerivedFrom("Part::Cut"):
			[[ x1, y1, z1 ]] = MagicPanels.getVerticesOffset([[ x1, y1, z1 ]], obj1Ref, "array")
		
		if not obj2Ref.isDerivedFrom("Part::Cut"):
			[[ x2, y2, z2 ]] = MagicPanels.getVerticesOffset([[ x2, y2, z2 ]], obj2Ref, "array")

		L = abs(x2 - x1)
		W = abs(y2 - y1)
		H = abs(z2 - z1)

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelBetween"+iType)
		[ panel.Length, panel.Width, panel.Height ] = MagicPanels.sizesToCubePanel(obj1Ref, iType)

		z1 = z1 + obj1Ref.Height.Value - panel.Height.Value
		
		if L > 0:
			panel.Length = L
		
		if W > 0:
			panel.Width = W
			
		if H > 0:
			panel.Height = H

		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z1), FreeCAD.Rotation(0, 0, 0))
		
		try:
			MagicPanels.copyColors(obj1Ref, panel)
		except:
			skip = 1

		FreeCAD.ActiveDocument.recompute()
		MagicPanels.moveToFirst([ panel ], obj1Ref)

	except:
		
		info = ""
		
		info += translate('panelBetween', '<b>Please select two valid faces at two different valid objects, to create panel between them. </b><br><br><b>Note:</b> This tool creates new panel between two selected faces. Selection faces order is important. To select more than one face, hold left CTRL key during second face selection. The blue panels represents the selected objects and the red one represents the new created object. The icon refers to base XY model view (0 key position). Click fitModel to set model into referred view.  If the two selected panels will be matching the icon, the new created panel should fill the gap between the selected faces. You can experiment with selection faces outside to resize the new panel. If you have problem with unpredicted result, use magicManager tool to preview panel before creation.')

		MagicPanels.showInfo("panelBetween"+iType, info)


# ###################################################################################################################
def panelSide(iType):
	
	try:

		objRef = MagicPanels.getReference()
		face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

		[ Length, Width, Height ] = MagicPanels.sizesToCubePanel(objRef, "ZY")

		if objRef.isDerivedFrom("Part::Box"):
			[ x, y, z ] = MagicPanels.getVertex(face, 0, 1)

		else:

			if iType == "1" or iType == "2":
				[ x, y, z ] = MagicPanels.getVertex(face, 0, 0)

			if iType == "3" or iType == "4":
				[ x, y, z ] = MagicPanels.getVertex(face, 1, 0)

		if iType == "1":
			x = x - Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideLeft")
		
		if iType == "2":
			z = z + Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideLeftUP")
		
		if iType == "3":
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideRight")
		
		if iType == "4":
			x = x - Length
			z = z + Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideRightUP")

		panel.Length = Length
		panel.Width = Width
		panel.Height = Height
		
		[ coX, coY, coZ, coR ] = MagicPanels.getContainersOffset(objRef)
		x = x + coX
		y = y + coY
		z = z + coZ
		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
		
		MagicPanels.addRotation(objRef, [ panel ])
		
		try:
			MagicPanels.copyColors(objRef, panel)
		except:
			skip = 1

		FreeCAD.ActiveDocument.recompute()
		MagicPanels.moveToFirst([ panel ], objRef)
		
	except:
		
		info = ""
		
		info += translate('panelSide', '<b>Please select valid face, to create panel. </b><br><br><b>Note:</b> This tool creates new panel at selected face. The blue panel represents the selected object and the red one represents the new created object. The arrow describe if the panel will be created up or down. The icon refers to base XY model view (0 key position). Click fitModel to set model into referred view. If you have problem with unpredicted result, use magicManager tool to preview panel before creation.')

		if iType == "1":
			MagicPanels.showInfo("panelSideLeft", info)
		if iType == "2":
			MagicPanels.showInfo("panelSideLeftUP", info)
		if iType == "3":
			MagicPanels.showInfo("panelSideRight", info)
		if iType == "4":
			MagicPanels.showInfo("panelSideRightUP", info)


# ###################################################################################################################
def panelBackOut():
	
	try:

		obj1Ref = MagicPanels.getReference(FreeCADGui.Selection.getSelection()[0])
		obj2Ref = MagicPanels.getReference(FreeCADGui.Selection.getSelection()[1])
		obj3Ref = MagicPanels.getReference(FreeCADGui.Selection.getSelection()[2])

		face1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		face2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
		face3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]

		[ L, W, H ] = MagicPanels.sizesToCubePanel(obj1Ref, "ZX")
		
		[ x1, y1, z1 ] = MagicPanels.getVertex(face1, 0, 1)
		[ x2, y2, z2 ] = MagicPanels.getVertex(face2, 0, 0)
		[ x3, y3, z3 ] = MagicPanels.getVertex(face3, 0, 1)
		
		[[ x1, y1, z1 ]] = MagicPanels.getVerticesOffset([[ x1, y1, z1 ]], obj1Ref, "array")
		[[ x2, y2, z2 ]] = MagicPanels.getVerticesOffset([[ x2, y2, z2 ]], obj2Ref, "array")
		[[ x3, y3, z3 ]] = MagicPanels.getVerticesOffset([[ x3, y3, z3 ]], obj3Ref, "array")

		L = abs(x2 - x1)
		H = H - z3

		if L > 0 and W > 0 and H > 0:

			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelBackOut")
			panel.Length = L
			panel.Width = W
			panel.Height = H

			panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z3), FreeCAD.Rotation(0, 0, 0))
			
			MagicPanels.addRotation(obj1Ref, [ panel ])
			
			try:
				MagicPanels.copyColors(obj1Ref, panel)
			except:
				skip = 1

			FreeCAD.ActiveDocument.recompute()
			MagicPanels.moveToFirst([ panel ], obj1Ref)
			
		else:
		
			raise

	except:
			
		info = ""
		
		info += translate('panelBackOut', '<b>Please select three faces according to the icon. </b><br><br><b>Note:</b> This tool allows to create back of the furniture with single click. To create back of the furniture you have to select 3 faces in the order described by the icon. To select more than one face, hold left CTRL key during face selection. The red edges at blue panels represents the selected faces. The transparent red panel represents the new created object. The icon refers to the back of the furniture.')
		
		MagicPanels.showInfo("panelBackOut", info)


# ###################################################################################################################
def panelCover(iType):
	
	try:

		obj1Ref = MagicPanels.getReference(FreeCADGui.Selection.getSelection()[0])
		obj2Ref = MagicPanels.getReference(FreeCADGui.Selection.getSelection()[1])
		obj3Ref = MagicPanels.getReference(FreeCADGui.Selection.getSelection()[2])

		face1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		face2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
		face3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]

		[ L, W, H ] = MagicPanels.sizesToCubePanel(obj1Ref, iType)

		[ x1, y1, z1 ] = MagicPanels.getVertex(face1, 0, 1)
		[ x2, y2, z2 ] = MagicPanels.getVertex(face2, 2, 1)
		[ x3, y3, z3 ] = MagicPanels.getVertex(face3, 0, 1)

		[[ x1, y1, z1 ]] = MagicPanels.getVerticesOffset([[ x1, y1, z1 ]], obj1Ref, "array")
		[[ x2, y2, z2 ]] = MagicPanels.getVerticesOffset([[ x2, y2, z2 ]], obj2Ref, "array")
		[[ x3, y3, z3 ]] = MagicPanels.getVerticesOffset([[ x3, y3, z3 ]], obj3Ref, "array")

		L = abs(x2 - x1)
		W = W + H

		if L > 0 and W > 0 and H > 0:
		
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelCover"+iType)
			panel.Length = L
			panel.Width = W
			panel.Height = H

			panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z3), FreeCAD.Rotation(0, 0, 0))
			
			MagicPanels.addRotation(obj1Ref, [ panel ])
			
			try:
				MagicPanels.copyColors(obj1Ref, panel)
			except:
				skip = 1

			FreeCAD.ActiveDocument.recompute()
			MagicPanels.moveToFirst([ panel ], obj1Ref)

	except:
		
		info = ""
		
		info += translate('panelCover', '<b>Please select three faces according to the icon. </b><br><br><b>Note:</b> This tool allows to create top cover of the furniture with single click. To create top cover of the furniture you have to select 3 faces in the order described by the icon. To select more than one face, hold left CTRL key during face selection. The red edges at blue panels represents the selected faces. The transparent red panel represents the new created object. The icon refers to the base XY model view (0 key position). Click fitModel to set model into referred view.')

		MagicPanels.showInfo("panelCover"+iType, info)


# ###################################################################################################################
def panelMove(iType):
	
	try:

		selection = FreeCADGui.Selection.getSelection()
		
		if len(selection) < 1:
			raise

		for o in selection:

			sizes = []
			sizes = MagicPanels.getSizes(o)
			sizes.sort()

			x = 0
			y = 0
			z = 0
			
			if iType == "Xp":
				x = sizes[0]
			
			if iType == "Xm":
				x = - sizes[0]

			if iType == "Yp":
				y = sizes[0]

			if iType == "Ym":
				y = - sizes[0]

			if iType == "Zp":
				z = sizes[0]

			if iType == "Zm":
				z = - sizes[0]

			try:
				[ x, y, z ] = MagicPanels.convertPosition(o, x, y, z)
			except:
				skip = 1
				
			[ x, y, z ] = MagicPanels.getModelRotation(x, y, z)

			[ px, py, pz, r ] = MagicPanels.getPlacement(o)
			MagicPanels.setPlacement(o, px+x, py+y, pz+z, r)

			FreeCAD.ActiveDocument.recompute()
	
	except:
		
		info = ""
		
		info += translate('panelMove', '<b>Please select valid objects to move. </b><br><br><b>Note:</b> With the arrows you can quickly move many Cube panels or even any other objects at once. If the thickness of the selected object can be recognized, the move step will be the thickness. So, you can solve common furniture problem with thickness offset. If the thickness will not be recognized the step will be 100. This allow you to move whole furniture segments very quickly. The arrows recognize the view model rotation. If you want precisely move object, use magicMove tool, instead. ')
		
		MagicPanels.showInfo("panelMove"+iType, info)


# ###################################################################################################################
def panelResize(iType):
	
	try:

		objects = FreeCADGui.Selection.getSelection()
		
		if len(objects) < 1:
			raise
		
		for o in objects:

			objRef = MagicPanels.getReference(o)

			sizes = []
			sizes = MagicPanels.getSizes(objRef)
			sizes.sort()
			thick = sizes[0]

			if objRef.isDerivedFrom("Part::Cylinder"):
				
				R, H = objRef.Radius.Value, objRef.Height.Value
				
				if iType == "1":
					objRef.Height = objRef.Height.Value + thick

				if iType == "2":
					if H - thick > 0:
						objRef.Height = objRef.Height.Value - thick

				if iType == "3":
					objRef.Radius = objRef.Radius.Value + thick
					
				if iType == "4":
					if R - thick > 0:
						objRef.Radius = objRef.Radius.Value - thick

				if iType == "5":
					objRef.Radius = objRef.Radius.Value + thick/2

				if iType == "6":
					if R - thick/2 > 0:
						objRef.Radius = objRef.Radius.Value - thick/2

			if objRef.isDerivedFrom("Part::Cone"):
				
				R1, R2, H = objRef.Radius1.Value, objRef.Radius2.Value, objRef.Height.Value
				
				if iType == "1":
					objRef.Height = objRef.Height.Value + thick

				if iType == "2":
					if H - thick > 0:
						objRef.Height = objRef.Height.Value - thick

				if iType == "3":
					objRef.Radius2 = objRef.Radius2.Value + thick/2

				if iType == "4":
					if R2 - thick/2 > 0:
						objRef.Radius2 = objRef.Radius2.Value - thick/2

				if iType == "5":
					objRef.Radius1 = objRef.Radius1.Value + thick/2

				if iType == "6":
					if R1 - thick/2 > 0:
						objRef.Radius1 = objRef.Radius1.Value - thick/2

			if objRef.isDerivedFrom("Part::Box"):

				L, W, H = objRef.Length.Value, objRef.Width.Value, objRef.Height.Value
					
				if iType == "1":
					if L == sizes[2]:
						objRef.Length = objRef.Length.Value + thick

					if W == sizes[2]:
						objRef.Width = objRef.Width.Value + thick
						
					if H == sizes[2]:
						objRef.Height = objRef.Height.Value + thick

				if iType == "2":
					if L == sizes[2]:
						if objRef.Length.Value - thick > 0:
							objRef.Length = objRef.Length.Value - thick
						
					if W == sizes[2]:
						if objRef.Width.Value - thick > 0:
							objRef.Width = objRef.Width.Value - thick
						
					if H == sizes[2]:
						if objRef.Height.Value - thick > 0:
							objRef.Height = objRef.Height.Value - thick

				if iType == "3":
					if L == sizes[1]:
						objRef.Length = objRef.Length.Value + thick

					if W == sizes[1]:
						objRef.Width = objRef.Width.Value + thick

					if H == sizes[1]:
						objRef.Height = objRef.Height.Value + thick

				if iType == "4":
					if L == sizes[1]:
						if objRef.Length.Value - thick > 0:
							objRef.Length = objRef.Length.Value - thick

					if W == sizes[1]:
						if objRef.Width.Value - thick > 0:
							objRef.Width = objRef.Width.Value - thick

					if H == sizes[1]:
						if objRef.Height.Value - thick > 0:
							objRef.Height = objRef.Height.Value - thick

				if iType == "5":
					if L == sizes[0]:
						objRef.Length = objRef.Length.Value + 1

					if W == sizes[0]:
						objRef.Width = objRef.Width.Value + 1

					if H == sizes[0]:
						objRef.Height = objRef.Height.Value + 1

				if iType == "6":
					if L == sizes[0]:
						if objRef.Length.Value - 1 > 0:
							objRef.Length = objRef.Length.Value - 1

					if W == sizes[0]:
						if objRef.Width.Value - 1 > 0:
							objRef.Width = objRef.Width.Value - 1

					if H == sizes[0]:
						if objRef.Height.Value - 1 > 0:
							objRef.Height = objRef.Height.Value - 1

			if objRef.isDerivedFrom("PartDesign::Pad"):
			
				[ sizeX, sizeY, thick ] = MagicPanels.getSizes(objRef)
				
				if iType == "1":
					
					if sizeX > sizeY:
						objRef.Profile[0].setDatum("SizeX", FreeCAD.Units.Quantity(sizeX + thick))
					else:
						objRef.Profile[0].setDatum("SizeY", FreeCAD.Units.Quantity(sizeY + thick))
			
				if iType == "2":
					
					if sizeX > sizeY:
						if sizeX - thick > 0:
							objRef.Profile[0].setDatum("SizeX", FreeCAD.Units.Quantity(sizeX - thick))
					else:
						if sizeY - thick > 0:
							objRef.Profile[0].setDatum("SizeY", FreeCAD.Units.Quantity(sizeY - thick))

				if iType == "3":
					
					if sizeX < sizeY:
						objRef.Profile[0].setDatum("SizeX", FreeCAD.Units.Quantity(sizeX + thick))
					else:
						objRef.Profile[0].setDatum("SizeY", FreeCAD.Units.Quantity(sizeY + thick))
			
				if iType == "4":
					
					if sizeX < sizeY:
						if sizeX - thick > 0:
							objRef.Profile[0].setDatum("SizeX", FreeCAD.Units.Quantity(sizeX - thick))
					else:
						if sizeY - thick > 0:
							objRef.Profile[0].setDatum("SizeY", FreeCAD.Units.Quantity(sizeY - thick))
				
				if iType == "5":
					
					if o.isDerivedFrom("PartDesign::Thickness"):
						o.Value.Value = o.Value.Value + 1
					else:
						objRef.Length = objRef.Length.Value + 1
				
				if iType == "6":
					
					if o.isDerivedFrom("PartDesign::Thickness"):
						if o.Value.Value -1 > 0:
							o.Value.Value = o.Value.Value - 1
					else:
						if objRef.Length.Value - 1 > 0:
							objRef.Length = objRef.Length.Value - 1
					

		FreeCAD.ActiveDocument.recompute()
	
	except:
		
		info = ""
		
		info += translate('panelResize', '<b>Please select valid panels to resize. </b><br><br><b>Note:</b> This tool allows to resize quickly panels or even other objects. The resize step is the panel thickness. Panel is resized into direction described by the icon for XY panel. However, in some cases the panel may be resized into opposite direction, if the panel is not supported or the sides are equal. You can also resize Cylinders (drill bits), the long side will be Height, the short will be diameter, the thickness will be Radius. For Cone objects (drill bits - countersinks, counterbore) the long side will be Height, the thickness will be Radius1 (bottom radius) and the short will be Radius2 (top radius).')
		
		MagicPanels.showInfo("panelResize"+iType, info)


# ###################################################################################################################
def routerBitSelect(iType):
	
	import PartDesign, Sketcher, Part
	import RouterPatterns

	try:

		# ###########################################################################################################
		# init database for call
		# ###########################################################################################################

		selectedObjects = FreeCADGui.Selection.getSelection()

		if len(selectedObjects) == 0:
			raise

		selectedSubs = dict()
		selectedKeys = dict()

		i = 0
		for o in selectedObjects:

			selectedSubs[o] = FreeCADGui.Selection.getSelectionEx()[i].SubObjects
			selectedKeys[o] = dict()
			for s in selectedSubs[o]:
				selectedKeys[o][s] = s.BoundBox

			i = i + 1

		# ###########################################################################################################
		# main call
		# ###########################################################################################################

		i = 0
		for o in selectedObjects:
			
			oRef = MagicPanels.getReference(o)
			if MagicPanels.isRotated(oRef):
				sizes = MagicPanels.getSizes(oRef)
				sizes.sort()
				thick = sizes[0]
			else:
				sizes = MagicPanels.getSizesFromVertices(oRef)
				sizes.sort()
				thick = sizes[0]

			subs = []
			
			if o.isDerivedFrom("Part::Box"):
			
				[ part, body, sketch, pad ] = MagicPanels.makePad(o, "panel2pad")
				
				for s in selectedSubs[o]:
					
					if s.ShapeType == "Edge":
						[ edge, edgeName, edgeIndex ] = MagicPanels.getSubByKey(pad, [ s.BoundBox ], "BoundBox", "edge")
						subs.append(edge)

					if s.ShapeType == "Face":
						[ face, faceName, faceIndex ] = MagicPanels.getSubByKey(pad, [ s.BoundBox ], "BoundBox", "face")
						subs.append(face)
					
				FreeCAD.ActiveDocument.removeObject(o.Name)
				FreeCAD.ActiveDocument.recompute()
			
			else:
			
				body = o._Body
				pad = o
				
				for s in selectedSubs[o]:
					subs.append(s)

			for s in subs:
				
				if s != "":

					if iType == "Cove":
						bit = float(thick)
					if iType == "Cove2":
						bit = float(thick/2)
					if iType == "Cove4":
						bit = float(thick/4)
					
					if iType == "RoundOver":
						bit = float(thick)
					if iType == "RoundOver2":
						bit = float(thick/2)
					if iType == "RoundOver4":
						bit = float(thick/4)
					
					if iType == "Straight2":
						bit = float(thick/2)
					if iType == "Straight3":
						bit = float(thick/3)
					if iType == "Straight4":
						bit = float(thick/4)
					
					if iType == "Chamfer":
						bit = float(thick)
					if iType == "Chamfer2":
						bit = float(thick/2)
					if iType == "Chamfer4":
						bit = float(thick/4)

					sketchPattern = body.newObject('Sketcher::SketchObject','routerPattern')
					RouterPatterns.setRouterPattern(sketchPattern, [ bit ], iType)
					FreeCAD.ActiveDocument.recompute()
					
					router = MagicPanels.edgeRouter(pad, s, sketchPattern, 0, iType, "simple")
					FreeCAD.ActiveDocument.recompute()
					
					MagicPanels.addRotation(pad, [ sketchPattern ])
					FreeCAD.ActiveDocument.recompute()

	except:
		
		info = ""
		
		info += translate('routerBitSelect', '<b>Please select edges or faces to use router. </b><br><br><b>Note:</b> This tool allows to create decoration router bits effect. You can select many edges or faces. The selected edges or faces do not have to be at the same object. You can select edges or faces at any object. But each edge or face need to be according to the XYZ coordinate axis to get correct plane of the edge or face. For face the routing path is the CenterOfMass of the face and also along the longest edge. Hold left CTRL key during edges or faces selection. The router bits get size from object thickness. If the router bit is for example Cove2, it means the size of the Cove will be 1/2 of the object thickness.')

		MagicPanels.showInfo("router"+iType, info)
	

# ###################################################################################################################
def multiPocket(iType):
	
	try:

		selectedObjects = FreeCADGui.Selection.getSelection()

		if len(selectedObjects) == 0:
			raise

		length = 0
		
		if iType != "":
			
			sizes = MagicPanels.getSizesFromVertices(selectedObjects[0])
			sizes.sort()
			thick = sizes[0]
			length = thick / int(iType)

		pocket = MagicPanels.makePockets(selectedObjects, length)

	except:
		
		info = ""
		
		info += translate('multiPocket', '<b>Please select object, next Sketches to create Pockets. </b><br><br><b>Note:</b> This tool allows to create custom decoration from Sketches. You can select many Sketches at once. The selected Sketches will make Pockets at the first selected object. The Sketches need to be correctly aligned at the object. Hold left CTRL key during Sketches selection. For 2 and 4 variant this tool gets first selected object size and create Pocket with 1/2 thickness or 1/4 thickness.')

		MagicPanels.showInfo("multiPocket"+iType, info)

# ###################################################################################################################
