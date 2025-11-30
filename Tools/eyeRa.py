import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCAD.ActiveDocument.Objects

	for o in objects:
		try:
			FreeCADGui.ActiveDocument.toggleTreeItem(o, 3)
		except:
			skip = 1

except:

	info = ""
	info += translate('eyeRa', "<b>Please create active document and at least one object inside container to expand tree for container and show its content.</b><br><br><b>Note:</b> This tool allows you to expand all containers in tree view to see quickly full tree structure of your model. Personally I use auto-expand tree after object selection in 3D view option but to exapand full structure you have to select all abject at 3D model or manually expand each container what is time-consuming. This simple tool allows you to make it with single click and together with eyeHorus tool allows you to quickly view and hide full structure. <br><br><b>About icon:</b> I did not have any ideas for an icon related to carpentry, and quite by chance I came up with the idea that the Eye of Ra and Horus would be cool in this case. Personally, I love stories about ancient Egyptian gods and the icon represents the eye of the god Ra, who saw everything, so it perfectly fits to the expanding the entire object tree structure and displaying all objects.")

	MagicPanels.showInfo("eyeRa", info)
