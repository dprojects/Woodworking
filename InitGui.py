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
		
		self.appendToolbar("Project manage", loadToolbar.getItems("Project manage"))
		self.appendToolbar("Code and Debug", loadToolbar.getItems("Code and Debug"))
		self.appendToolbar("Dimensions", loadToolbar.getItems("Dimensions"))
		self.appendToolbar("Preview", loadToolbar.getItems("Preview"))
		
		
		
		self.appendToolbar("Magic Panels - default", loadToolbar.getItems("Magic Panels - default"))
		self.appendToolbar("Magic Panels - copy", loadToolbar.getItems("Magic Panels - copy"))
		self.appendToolbar("Magic Panels - special", loadToolbar.getItems("Magic Panels - special"))
		self.appendToolbar("Furniture Parts", loadToolbar.getItems("Furniture Parts"))
		
		self.appendToolbar("Magic Panels - move", loadToolbar.getItems("Magic Panels - move"))
		self.appendToolbar("Magic Panels - resize", loadToolbar.getItems("Magic Panels - resize"))
		self.appendToolbar("Magic Panels - face", loadToolbar.getItems("Magic Panels - face"))
		self.appendToolbar("Magic Panels - between", loadToolbar.getItems("Magic Panels - between"))
		self.appendToolbar("Magic Panels - replace", loadToolbar.getItems("Magic Panels - replace"))
		self.appendToolbar("Parameterization", loadToolbar.getItems("Parameterization"))
		self.appendToolbar("Transformations", loadToolbar.getItems("Transformations"))
		self.appendToolbar("Decorations", loadToolbar.getItems("Decorations"))
		

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
