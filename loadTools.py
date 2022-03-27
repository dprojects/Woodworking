import FreeCADGui

import os, sys
import fakemodule
path = os.path.dirname(fakemodule.__file__)
iconPath = os.path.join(path, "Icons")


# ######################################################################################################################
class BOM():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "getDimensions.xpm"),
				"Accel"   : "",
				"MenuText": "BOM",
				"ToolTip" : "creates spreadsheet with dimensions to cut"}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "getDimensions"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		path = os.path.join(path, module)
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("BOM", BOM())


# ######################################################################################################################
class HTML():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "sheet2export.xpm"),
				"Accel"   : "",
				"MenuText": "HTML",
				"ToolTip" : "exports spreadsheet to chosen file format"}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "sheet2export"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		path = os.path.join(path, module)
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("HTML", HTML())


# ######################################################################################################################
class CODE():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "scanObjects.xpm"),
				"Accel"   : "",
				"MenuText": "CODE",
				"ToolTip" : "inspection tool for FreeCAD macro development & project debug"}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "scanObjects"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		path = os.path.join(path, module)
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("CODE", CODE())


# ######################################################################################################################
class SETTEXTURES():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "setTextures.xpm"),
				"Accel"   : "",
				"MenuText": "SETTEXTURES",
				"ToolTip" : "set textures stored as URL at objects"}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "setTextures"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		path = os.path.join(path, module)
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("SETTEXTURES", SETTEXTURES())

