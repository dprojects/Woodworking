import FreeCAD
translate = FreeCAD.Qt.translate

def QT_TRANSLATE_NOOP(context, text):
	return text

import FreeCADGui

import os, sys
import fakemodule
path = os.path.dirname(fakemodule.__file__)
iconPath = os.path.join(path, "Icons")


# ######################################################################################################################
class DOCS():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.png"),
				"MenuText": QT_TRANSLATE_NOOP('Workbench', 'Woodworking at FreeCAD - woodworking workbench documentation'),
				"ToolTip" : QT_TRANSLATE_NOOP('Workbench', 'Opens web browser with external link.'),
				"Accel"   : ""}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://github.com/dprojects/Woodworking/tree/master/Docs")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("DOCS", DOCS())


# ######################################################################################################################
class EXAMPLES():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.png"),
				"MenuText": QT_TRANSLATE_NOOP('Workbench', 'Woodworking at FreeCAD - fully parametric examples'),
				"ToolTip" : QT_TRANSLATE_NOOP('Workbench', 'Opens web browser with external link.'),
				"Accel"   : ""}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://github.com/dprojects/Woodworking/tree/master/Examples/Parametric")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("EXAMPLES", EXAMPLES())


# ######################################################################################################################
class FIXTURE():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.png"),
				"MenuText": QT_TRANSLATE_NOOP('Workbench', 'Woodworking at FreeCAD - fixture examples'),
				"ToolTip" : QT_TRANSLATE_NOOP('Workbench', 'Opens web browser with external link.'),
				"Accel"   : ""}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("FIXTURE", FIXTURE())


# ######################################################################################################################
class TEXTURES():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.png"),
				"MenuText": QT_TRANSLATE_NOOP('Workbench', 'Woodworking at FreeCAD - free woodworking textures'),
				"ToolTip" : QT_TRANSLATE_NOOP('Workbench', 'Opens web browser with external link.'),
				"Accel"   : ""}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://commons.wikimedia.org/w/index.php?title=Special:ListFiles/Dprojects&ilshowall=1")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("TEXTURES", TEXTURES())


# ######################################################################################################################
class DOCSgetDimensions():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.png"),
				"MenuText": QT_TRANSLATE_NOOP('Workbench', 'Tool documentation - getDimensions, cut-list, BOM'),
				"ToolTip" : QT_TRANSLATE_NOOP('Workbench', 'Opens web browser with external link.'),
				"Accel"   : ""}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://github.com/dprojects/getDimensions/tree/master/Docs")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("DOCSgetDimensions", DOCSgetDimensions())


# ######################################################################################################################
class DOCSsheet2export():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.png"),
				"MenuText": QT_TRANSLATE_NOOP('Workbench', 'Tool documentation - sheet2export'),
				"ToolTip" : QT_TRANSLATE_NOOP('Workbench', 'Opens web browser with external link.'),
				"Accel"   : ""}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://github.com/dprojects/sheet2export")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("DOCSsheet2export", DOCSsheet2export())


# ######################################################################################################################
class DOCSsetTextures():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.png"),
				"MenuText": QT_TRANSLATE_NOOP('Workbench', 'Tool documentation - setTextures'),
				"ToolTip" : QT_TRANSLATE_NOOP('Workbench', 'Opens web browser with external link.'),
				"Accel"   : ""}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://github.com/dprojects/setTextures")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("DOCSsetTextures", DOCSsetTextures())


# ######################################################################################################################
class DOCSscanObjects():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.png"),
				"MenuText": QT_TRANSLATE_NOOP('Workbench', 'Tool documentation - scanObjects'),
				"ToolTip" : QT_TRANSLATE_NOOP('Workbench', 'Opens web browser with external link.'),
				"Accel"   : ""}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://github.com/dprojects/scanObjects")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("DOCSscanObjects", DOCSscanObjects())


# ######################################################################################################################
class AUTOUPDATE():

	gUpdated = ""
	gSkipped = ""

	def updateTool(self, iTool, iRoot="https://raw.githubusercontent.com/dprojects/"):
		
		import urllib.request
		
		try:
			module = iTool
		
			filePath = os.path.join(path, "Tools")
			filePath = os.path.join(filePath, module+".py")
			
			httplink = iRoot
			httplink += module + "/master/" + module + ".py"
			urllib.request.urlretrieve(httplink, filePath)
			
			self.gUpdated += "\t + " + module + "\t\n"
		except:
			self.gSkipped += "\t - " + module + "\t\n"
		
		return

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "autoupdate.png"),
				"MenuText": QT_TRANSLATE_NOOP('Workbench', 'Download and update all macro tools'),
				"ToolTip" : QT_TRANSLATE_NOOP('Workbench', 'Download latest versions for all macro tools.'),
				"Accel"   : ""}

	def Activated(self):

		self.gUpdated = ""
		self.gSkipped = ""

		self.updateTool("getDimensions")
		self.updateTool("sheet2export")
		self.updateTool("scanObjects")
		self.updateTool("setTextures")

		info = ""
		
		if self.gUpdated != "":
			info += translate('manuAutoupdate', 'Updated macro tools:')
			info += "\n\n"
			info += self.gUpdated
			info += "\n\n"
		
		if self.gSkipped != "":
			info += translate('manuAutoupdate', 'Skipped macro tools:')
			info += "\n\n"
			info += self.gSkipped
			info += "\n\n"
		
		from PySide import QtGui, QtCore
		title = translate('manuAutoupdate', 'Macro tools - autoupdate')
		QtGui.QMessageBox.information(None, title, str(info))
		
		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("AUTOUPDATE", AUTOUPDATE())


# ######################################################################################################################
def getItems():

	parts = []

	parts = [ 
		"DOCS",
		"EXAMPLES",
		"FIXTURE",
		"TEXTURES",
		"DOCSgetDimensions",
		"DOCSsheet2export",
		"DOCSsetTextures",
		"DOCSscanObjects",
		"AUTOUPDATE"
	]

	return parts
