class WoodworkingWorkbench (Workbench):

	# ################################################################################################
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
	ToolTip = QT_TRANSLATE_NOOP("Workbench", "Workbench for woodworking.")
	Icon = os.path.join(iconPath, "Woodworking.png")

	# ################################################################################################
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

		# ################################################################################################
		# toolbar
		# ################################################################################################
		
		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - default"), 
			loadToolbar.getItems("Woodworking - default"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - move"), 
			loadToolbar.getItems("Woodworking - move"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - resize"), 
			loadToolbar.getItems("Woodworking - resize"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - preview"), 
			loadToolbar.getItems("Woodworking - preview"))
		
		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - dowels and screws"), 
			loadToolbar.getItems("Woodworking - dowels and screws"))
		
		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - drilling holes"), 
			loadToolbar.getItems("Woodworking - drilling holes"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - project manage"), 
			loadToolbar.getItems("Woodworking - project manage"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - dimensions"), 
			loadToolbar.getItems("Woodworking - dimensions"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - decorations"), 
			loadToolbar.getItems("Woodworking - decorations"))
		
		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - advanced"), 
			loadToolbar.getItems("Woodworking - advanced"))
	
		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - copy"), 
			loadToolbar.getItems("Woodworking - copy"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - parameterization"), 
			loadToolbar.getItems("Woodworking - parameterization"))
	
		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - fixture"), 
			loadToolbar.getItems("Woodworking - fixture"))
	
		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - construction"), 
			loadToolbar.getItems("Woodworking - construction"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - joinery"), 
			loadToolbar.getItems("Woodworking - joinery"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - router"), 
			loadToolbar.getItems("Woodworking - router"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - face"), 
			loadToolbar.getItems("Woodworking - face"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - between"), 
			loadToolbar.getItems("Woodworking - between"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - special"), 
			loadToolbar.getItems("Woodworking - special"))

		self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "Woodworking - code and debug"), 
			loadToolbar.getItems("Woodworking - code and debug"))

		# ################################################################################################
		# menu
		# ################################################################################################
		
		self.appendMenu(QT_TRANSLATE_NOOP("Workbench", "Woodworking"), loadMenu.getItems())
	
		# ################################################################################################
		# configure Woodworking at first run
		# ################################################################################################
		
		FreeCAD.Console.PrintMessage("\n")
		try:
			pref = 'User parameter:BaseApp/Preferences/Woodworking'
			test = FreeCAD.ParamGet(pref).GetString('wInit')
			if test == "" or test == "True":
				
				# set default workbench
				FreeCAD.Console.PrintMessage("\n")
				try:
					msg = QT_TRANSLATE_NOOP("Workbench", "Setting Woodworking wokbench as default ...")
					pref = 'User parameter:BaseApp/Preferences/General'
					FreeCAD.ParamGet(pref).SetString('AutoloadModule', 'WoodworkingWorkbench')
					msg += "ok."
				except:
					msg += "fail."
				FreeCAD.Console.PrintMessage(msg)

				# set order of groups with icons
				FreeCAD.Console.PrintMessage("\n")
				try:
					msg = QT_TRANSLATE_NOOP("Workbench", "Setting icons position ...")
					pref = 'User parameter:Tux/PersistentToolbars/User/WoodworkingWorkbench'
					
					pos = 'Break,Workbench,Woodworking - project manage,Woodworking - dimensions,Woodworking - router,Woodworking - decorations,Break,Woodworking - copy,Woodworking - face,Woodworking - between,Woodworking - special,Woodworking - construction,Woodworking - parameterization,Break,Woodworking - default,Woodworking - resize,Woodworking - move,Woodworking - preview'
					FreeCAD.ParamGet(pref).SetString('Top', pos)
					
					pos = 'Woodworking - advanced,Woodworking - code and debug'
					FreeCAD.ParamGet(pref).SetString('Left', pos)
					
					pos = 'Woodworking - joinery,Break,Woodworking - dowels and screws,Woodworking - drilling holes,Woodworking - fixture'
					FreeCAD.ParamGet(pref).SetString('Right', pos)
					
					FreeCAD.ParamGet(pref).SetString('Bottom', '')
					FreeCAD.ParamGet(pref).SetBool('Saved', True)
					msg += "ok."
				except:
					msg += "fail."
				FreeCAD.Console.PrintMessage(msg)

				# turn off duplicated groups of icons
				# not works because FreeCAD overwrite
				FreeCAD.Console.PrintMessage("\n")
				try:
					msg = QT_TRANSLATE_NOOP("Workbench", "Turn off duplicated groups of icons ...")
					pref = 'User parameter:BaseApp/MainWindow/Toolbars'
					FreeCAD.ParamGet(pref).SetBool('Clipboard', False)
					FreeCAD.ParamGet(pref).SetBool('Edit', False)
					FreeCAD.ParamGet(pref).SetBool('File', False)
					FreeCAD.ParamGet(pref).SetBool('Help', False)
					FreeCAD.ParamGet(pref).SetBool('Individual views', False)
					FreeCAD.ParamGet(pref).SetBool('Macro', False)
					FreeCAD.ParamGet(pref).SetBool('Structure', False)
					FreeCAD.ParamGet(pref).SetBool('View', False)
					msg += "ok."
				except:
					msg += "fail."
				FreeCAD.Console.PrintMessage(msg)
				
			pref = 'User parameter:BaseApp/Preferences/Woodworking'
			FreeCAD.ParamGet(pref).SetString('wInit', "False")
		except:
			skip = 1
		FreeCAD.Console.PrintMessage("\n\n")
		
	# ################################################################################################
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

# ################################################################################################
Gui.addWorkbench(WoodworkingWorkbench())
