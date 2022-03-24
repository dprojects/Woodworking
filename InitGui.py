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

		import loadTools
		self.appendToolbar("Macro tools", [ "BOM", "HTML", "CODE" ])
		
		import loadToolbar
		self.appendToolbar("Parameterization", loadToolbar.getItems("Parameterization"))
		self.appendToolbar("Structure", loadToolbar.getItems("Structure"))
		self.appendToolbar("Furniture Parts", loadToolbar.getItems("Furniture Parts"))
		self.appendToolbar("Transformations", loadToolbar.getItems("Transformations"))
		self.appendToolbar("Operations", loadToolbar.getItems("Operations"))
		self.appendToolbar("Manage", loadToolbar.getItems("Manage"))
		
		import loadMenu
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
