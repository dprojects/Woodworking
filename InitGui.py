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
		self.appendToolbar("Parameterization", loadToolbar.getItems("Parameterization"))
		self.appendToolbar("Furniture Parts", loadToolbar.getItems("Furniture Parts"))
		self.appendToolbar("Transformations", loadToolbar.getItems("Transformations"))
		self.appendToolbar("Decorations", loadToolbar.getItems("Decorations"))
		self.appendToolbar("Dimensions", loadToolbar.getItems("Dimensions"))
		self.appendToolbar("Preview", loadToolbar.getItems("Preview"))

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
