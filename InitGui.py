class WoodworkingWorkbench (Workbench):

	import FreeCAD
	translate = FreeCAD.Qt.translate

	def QT_TRANSLATE_NOOP(context, text):
		return text

	import os, sys
	import fakemodule
	path = os.path.dirname(fakemodule.__file__)
	iconPath = os.path.join(path, "Icons")
	translationsPath = os.path.join(path, "translations")

	MenuText = QT_TRANSLATE_NOOP("Workbench", "Woodworking")
	ToolTip = QT_TRANSLATE_NOOP("Workbench", "Workbech for woodworking.")
	Icon = os.path.join(iconPath, "Woodworking.png")

	def Initialize(self):

		import FreeCAD, FreeCADGui
		
		def QT_TRANSLATE_NOOP(context, text):
			return text

		FreeCADGui.addLanguagePath(self.translationsPath)
		
		# uncomment those lines below if you want to add icon from other workbenches
		# however the DraftTools will slow down the FreeCAD loading
		# for woodworking purposes there will be new tools, so do not cry ;-)
		
		import PartGui, PartDesignGui
		import SketcherGui, SpreadsheetGui
		#import DraftTools

		import loadToolbar
		import loadMenu

		# toolbar
		# ################################################################################################
		
		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Magic Panels - default"), 
			loadToolbar.getItems("Woodworking - Magic Panels - default"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Magic Panels - copy"), 
			loadToolbar.getItems("Woodworking - Magic Panels - copy"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Magic Panels - move"), 
			loadToolbar.getItems("Woodworking - Magic Panels - move"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Magic Panels - resize"), 
			loadToolbar.getItems("Woodworking - Magic Panels - resize"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Magic Panels - special"), 
			loadToolbar.getItems("Woodworking - Magic Panels - special"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Magic Panels - face"), 
			loadToolbar.getItems("Woodworking - Magic Panels - face"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Magic Panels - between"), 
			loadToolbar.getItems("Woodworking - Magic Panels - between"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Magic Panels - replace"), 
			loadToolbar.getItems("Woodworking - Magic Panels - replace"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Magic Panels - mounting"), 
			loadToolbar.getItems("Woodworking - Magic Panels - mounting"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Magic Panels - drilling"), 
			loadToolbar.getItems("Woodworking - Magic Panels - drilling"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Project manage"), 
			loadToolbar.getItems("Woodworking - Project manage"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Code and Debug"), 
			loadToolbar.getItems("Woodworking - Code and Debug"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Dimensions"), 
			loadToolbar.getItems("Woodworking - Dimensions"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Preview"), 
			loadToolbar.getItems("Woodworking - Preview"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Decorations"), 
			loadToolbar.getItems("Woodworking - Decorations"))
		
		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - Advanced"), 
			loadToolbar.getItems("Woodworking - Advanced"))
		
		# menu
		# ################################################################################################
		
		self.appendMenu(QT_TRANSLATE_NOOP("Workbench", "Woodworking"), loadMenu.getItems())
		
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
