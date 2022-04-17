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
				"ToolTip" : "store textures URL or load stored"}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "setTextures"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
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

# ######################################################################################################################
class DEBUGINFO():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "debugInfo.xpm"),
				"Accel"   : "",
				"MenuText": "DEBUGINFO",
				"ToolTip" : "copy platform details to clipboard for bug report purposes"}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "debugInfo"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("DEBUGINFO", DEBUGINFO())

# ######################################################################################################################
class panelXY():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelXY.xpm"),
				"Accel"   : "",
				"MenuText": "panelXY",
				"ToolTip" : "Creates default XY panel. If You select any Cube object this panel get the dimensions from this object and transform them into described direction. This can be some kind of copy with exact rotation. Change dimensions at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelXY"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelXY", panelXY())

# ######################################################################################################################
class panelXZ():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelXZ.xpm"),
				"Accel"   : "",
				"MenuText": "panelXZ",
				"ToolTip" : "Creates default XZ panel. If You select any Cube object this panel get the dimensions from this object and transform them into described direction. This can be some kind of copy with exact rotation. Change dimensions at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelXZ"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelXZ", panelXZ())

# ######################################################################################################################
class panelYZ():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelYZ.xpm"),
				"Accel"   : "",
				"MenuText": "panelYZ",
				"ToolTip" : "Creates default YZ panel. If You select any Cube object this panel get the dimensions from this object and transform them into described direction. This can be some kind of copy with exact rotation. Change dimensions at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelYZ"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelYZ", panelYZ())

# ######################################################################################################################
class panelXYFace():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelXYFace.xpm"),
				"Accel"   : "",
				"MenuText": "panelXYFace",
				"ToolTip" : "Creates XY panel at selected face. Dimensions are taken from selected object. So, the selection is important to get desired result. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelXYFace"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelXYFace", panelXYFace())

# ######################################################################################################################
class panelXZFace():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelXZFace.xpm"),
				"Accel"   : "",
				"MenuText": "panelXZFace",
				"ToolTip" : "Creates XZ panel at selected face. Dimensions are taken from selected object. So, the selection is important to get desired result. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelXZFace"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelXZFace", panelXZFace())

# ######################################################################################################################
class panelYZFace():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelYZFace.xpm"),
				"Accel"   : "",
				"MenuText": "panelYZFace",
				"ToolTip" : "Creates YZ panel at selected face. Dimensions are taken from selected object. So, the selection is important to get desired result. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelYZFace"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelYZFace", panelYZFace())

# ######################################################################################################################
class panelXYBetween():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelXYBetween.xpm"),
				"Accel"   : "",
				"MenuText": "panelXYBetween",
				"ToolTip" : "Creates XY panel between 2 selected faces. Dimensions are taken from 1st selected object. So, the selection order is important to get desired result. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelXYBetween"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelXYBetween", panelXYBetween())

# ######################################################################################################################
class panelXZBetween():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelXZBetween.xpm"),
				"Accel"   : "",
				"MenuText": "panelXZBetween",
				"ToolTip" : "Creates XZ panel between 2 selected faces. Dimensions are taken from 1st selected object. So, the selection order is important to get desired result. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelXZBetween"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelXZBetween", panelXZBetween())

# ######################################################################################################################
class panelYZBetween():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelYZBetween.xpm"),
				"Accel"   : "",
				"MenuText": "panelYZBetween",
				"ToolTip" : "Creates YZ panel between 2 selected faces. Dimensions are taken from 1st selected object. So, the selection order is important to get desired result. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelYZBetween"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelYZBetween", panelYZBetween())

# ######################################################################################################################
class panelXYCover():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelXYCover.xpm"),
				"Accel"   : "",
				"MenuText": "panelXYCover",
				"ToolTip" : "Creates XY panel on top of 3 selected faces. Dimensions are taken from 1st and 3rd selected object. So, the selection order is important to get desired result. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelXYCover"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelXYCover", panelXYCover())

# ######################################################################################################################
class panelXZCover():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelXZCover.xpm"),
				"Accel"   : "",
				"MenuText": "panelXZCover",
				"ToolTip" : "Creates XZ panel on top of 3 selected faces. Dimensions are taken from 1st and 3rd selected object. So, the selection order is important to get desired result. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelXZCover"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelXZCover", panelXZCover())

# ######################################################################################################################
class panelYZCover():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelYZCover.xpm"),
				"Accel"   : "",
				"MenuText": "panelYZCover",
				"ToolTip" : "Creates YZ panel on top of 3 selected faces. Dimensions are taken from 1st and 3rd selected object. So, the selection order is important to get desired result. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelYZCover"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelYZCover", panelYZCover())

# ######################################################################################################################
class panelSideLeft():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelSideLeft.xpm"),
				"Accel"   : "",
				"MenuText": "panelSideLeft",
				"ToolTip" : "Creates furniture left side at selected face. Dimensions are taken from selected object. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelSideLeft"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelSideLeft", panelSideLeft())

# ######################################################################################################################
class panelSideLeftUP():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelSideLeftUP.xpm"),
				"Accel"   : "",
				"MenuText": "panelSideLeftUP",
				"ToolTip" : "Creates furniture left side at selected face but raised up. Dimensions are taken from selected object. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelSideLeftUP"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelSideLeftUP", panelSideLeftUP())

# ######################################################################################################################
class panelSideRight():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelSideRight.xpm"),
				"Accel"   : "",
				"MenuText": "panelSideRight",
				"ToolTip" : "Creates furniture right side at selected face. Dimensions are taken from selected object. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelSideRight"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelSideRight", panelSideRight())

# ######################################################################################################################
class panelSideRightUP():

	def GetResources(self):
		return {"Pixmap"  : os.path.join(iconPath, "panelSideRightUP.xpm"),
				"Accel"   : "",
				"MenuText": "panelSideRightUP",
				"ToolTip" : "Creates furniture right side at selected face but raised up. Dimensions are taken from selected object. Adjust dimensions and position at object property window, if needed."}

	def Activated(self):

		import os, sys
		import fakemodule

		modulePath = sys.path
		
		module = "panelSideRightUP"
		
		path = os.path.dirname(fakemodule.__file__)
		path = os.path.join(path, "Tools")
		sys.path.append(path)

		if module in sys.modules:
			del sys.modules[module]

		__import__(module, globals(), locals(), [], 0)
		
		sys.path = modulePath

		return

	def IsActive(self):
		# not needed now, maybe in the future
		return True

FreeCADGui.addCommand("panelSideRightUP", panelSideRightUP())
