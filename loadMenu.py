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
				"MenuText": "Basic tutorial for FreeCAD woodworking",
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
class AUTOUPDATE():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "autoupdate.xpm"),
				"Accel"   : "",
				"MenuText": "Download and update all macro tools (experimental)",
				"ToolTip" : "Download latest versions for all macro tools (experimental)."}

	def Activated(self):

		import FreeCAD

		module = "getDimensions"
		FreeCAD.Console.PrintMessage("\n")
		FreeCAD.Console.PrintMessage("Update: "+module+" ...")

		filePath = os.path.join(path, "Tools")
		filePath = os.path.join(filePath, module)
		filePath = os.path.join(filePath, module+".py")

		import urllib.request
		httplink = "https://raw.githubusercontent.com/dprojects/"
		httplink += module + "/master/" + module + ".py"
		urllib.request.urlretrieve(httplink, filePath)
		FreeCAD.Console.PrintMessage("done.")

		module = "sheet2export"
		FreeCAD.Console.PrintMessage("\n")
		FreeCAD.Console.PrintMessage("Update: "+module+" ...")

		filePath = os.path.join(path, "Tools")
		filePath = os.path.join(filePath, module)
		filePath = os.path.join(filePath, module+".py")

		import urllib.request
		httplink = "https://raw.githubusercontent.com/dprojects/"
		httplink += module + "/master/" + module + ".py"
		urllib.request.urlretrieve(httplink, filePath)
		FreeCAD.Console.PrintMessage("done.")

		module = "scanObjects"
		FreeCAD.Console.PrintMessage("\n")
		FreeCAD.Console.PrintMessage("Update: "+module+" ...")

		filePath = os.path.join(path, "Tools")
		filePath = os.path.join(filePath, module)
		filePath = os.path.join(filePath, module+".py")

		import urllib.request
		httplink = "https://raw.githubusercontent.com/dprojects/"
		httplink += module + "/master/" + module + ".py"
		urllib.request.urlretrieve(httplink, filePath)
		FreeCAD.Console.PrintMessage("done.")
		
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
		"AUTOUPDATE"
	]

	return parts
