class WoodworkingWorkbench (Workbench):

	import os, sys
	import fakemodule
	path = os.path.dirname(fakemodule.__file__)
	iconPath = os.path.join(path, "Icons")

	MenuText = "Woodworking"
	ToolTip = "Workbech for woodworking."
	Icon = os.path.join(iconPath, "Woodworking.xpm")

	def Initialize(self):

		import FreeCADGui, PartGui, PartDesignGui, SketcherGui, SpreadsheetGui
		import DraftTools

		import loadToolbar
		import loadMenu

		self.appendToolbar("Woodworking - Magic Panels - default", loadToolbar.getItems("Magic Panels - default"))
		self.appendToolbar("Woodworking - Magic Panels - copy", loadToolbar.getItems("Magic Panels - copy"))
		self.appendToolbar("Woodworking - Magic Panels - move", loadToolbar.getItems("Magic Panels - move"))
		self.appendToolbar("Woodworking - Magic Panels - resize", loadToolbar.getItems("Magic Panels - resize"))
		self.appendToolbar("Woodworking - Magic Panels - special", loadToolbar.getItems("Magic Panels - special"))
		self.appendToolbar("Woodworking - Magic Panels - face", loadToolbar.getItems("Magic Panels - face"))
		self.appendToolbar("Woodworking - Magic Panels - between", loadToolbar.getItems("Magic Panels - between"))
		self.appendToolbar("Woodworking - Magic Panels - replace", loadToolbar.getItems("Magic Panels - replace"))
		
		self.appendToolbar("Woodworking - Project manage", loadToolbar.getItems("Project manage"))
		self.appendToolbar("Woodworking - Code and Debug", loadToolbar.getItems("Code and Debug"))
		self.appendToolbar("Woodworking - Dimensions", loadToolbar.getItems("Dimensions"))
		self.appendToolbar("Woodworking - Preview", loadToolbar.getItems("Preview"))
				
		self.appendToolbar("Woodworking - Furniture Parts", loadToolbar.getItems("Furniture Parts"))
		self.appendToolbar("Woodworking - Parameterization", loadToolbar.getItems("Parameterization"))
		self.appendToolbar("Woodworking - Transformations", loadToolbar.getItems("Transformations"))
		self.appendToolbar("Woodworking - Decorations", loadToolbar.getItems("Decorations"))

		self.appendMenu("Woodworking", loadMenu.getItems())
		
	def Activated(self):
		# not needed now, maybe in the future
		return

	def Deactivated(self):
		# not needed now, maybe in the future
		return

	def ContextMenu(self, recipient):
		# not needed now, maybe in the future
		return

	def GetClassName(self): 
		return "Gui::PythonWorkbench"
       
Gui.addWorkbench(WoodworkingWorkbench())
