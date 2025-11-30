import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	objects = FreeCAD.ActiveDocument.Objects

	for o in objects:
		try:
			FreeCADGui.ActiveDocument.toggleTreeItem(o, 1)
		except:
			skip = 1

except:

	info = translate('eyeHorus', "<b>Please create active document and at least one object inside container to close tree for container.</b><br><br><b>Note:</b> This tool allows you to close all containers in tree view to have cleaner tree structure. Personally I use auto-expand tree after object selection in 3D view option but after modeling and selecting many objects the objects tree look less readable if you have many deeply nested containers. So this simple tool allows you to make it cleaner with single click. <br><br><b>About icon:</b> I did not have any ideas for an icon related to carpentry, and quite by chance I came up with the idea that the Eye of Ra and Horus would be cool in this case. Personally, I love stories about ancient Egyptian gods and the icon represents the eye of the god Horus, whose power was limited. So, in a sense, it is the opposite of the Eye of Ra.")

	MagicPanels.showInfo("eyeHorus", info)
