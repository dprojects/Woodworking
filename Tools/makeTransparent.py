import FreeCAD

gChange = []
gType = ""

for o in FreeCAD.activeDocument().Objects:
	
	try:

		if str(o.ViewObject.Transparency) == "0":
			gChange.append(o)
			gType = "set"

		if str(o.ViewObject.Transparency) == "83":
			gChange.append(o)
			gType = "unset"

	except:
		skip = 1

for o in gChange:

	try:

		if gType == "set":
			o.ViewObject.Transparency = 83

		if gType == "unset":
			o.ViewObject.Transparency = 0

	except:
		skip = 1
