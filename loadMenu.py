import FreeCADGui

import os, sys
import fakemodule
path = os.path.dirname(fakemodule.__file__)
iconPath = os.path.join(path, "Icons")


# ######################################################################################################################
class DOCS():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.xpm"),
				"Accel"   : "",
				"MenuText": "Woodworking at FreeCAD - basic tutorial (getDimensions Docs)",
				"ToolTip" : "Opens web browser with external link."}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://github.com/dprojects/getDimensions/tree/master/Docs")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("DOCS", DOCS())


# ######################################################################################################################
class EXAMPLES():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.xpm"),
				"Accel"   : "",
				"MenuText": "Woodworking at FreeCAD - fully parametric examples",
				"ToolTip" : "Opens web browser with external link."}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://github.com/dprojects/Woodworking/tree/master/Examples")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("EXAMPLES", EXAMPLES())


# ######################################################################################################################
class TEXTURES():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "Docs.xpm"),
				"Accel"   : "",
				"MenuText": "Woodworking at FreeCAD - free woodworking textures",
				"ToolTip" : "Opens web browser with external link."}

	def Activated(self):

		import webbrowser
		webbrowser.open("https://commons.wikimedia.org/w/index.php?title=Special:ListFiles/Dprojects&ilshowall=1")

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("TEXTURES", TEXTURES())


# ######################################################################################################################
class AUTOUPDATE():

	gUpdated = ""
	gSkipped = ""

	def updateTool(self, iTool, iRoot="https://raw.githubusercontent.com/dprojects/"):
		
		import urllib.request
		
		try:
			module = iTool
		
			filePath = os.path.join(path, "Tools")
			filePath = os.path.join(filePath, module)
			filePath = os.path.join(filePath, module+".py")
			
			httplink = iRoot
			httplink += module + "/master/" + module + ".py"
			urllib.request.urlretrieve(httplink, filePath)
			
			self.gUpdated += "\t + " + module + "\t\n"
		except:
			self.gSkipped += "\t - " + module + "\t\n"
		
		return

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "autoupdate.xpm"),
				"Accel"   : "",
				"MenuText": "Download and update all macro tools",
				"ToolTip" : "Download latest versions for all macro tools."}

	def Activated(self):

		self.gUpdated = ""
		self.gSkipped = ""

		self.updateTool("getDimensions")
		self.updateTool("sheet2export")
		self.updateTool("scanObjects")
		self.updateTool("setTextures")

		info = ""
		
		if self.gUpdated != "":
			info += "Updated macro tools:"
			info += "\n\n"
			info += self.gUpdated
			info += "\n\n"
		
		if self.gSkipped != "":
			info += "Skipped macro tools:"
			info += "\n\n"
			info += self.gSkipped
			info += "\n\n"
		
		from PySide import QtGui, QtCore
		QtGui.QMessageBox.information(None,"Macro tools - autoupdate",str(info))
		
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
		"TEXTURES",
		"AUTOUPDATE"
	]

	return parts
