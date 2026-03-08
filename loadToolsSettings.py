# This is setting file for loadToolsAuto generator. 
#
# If you want to add new macro and create command Class for it, 
# add here the new entry and run: 
# 
# python3 ./loadToolsAuto.py
#
# There is no need to add it to workbench startup.
#
# Macro row order:
#
# 0, 1, 2, 3
#
# 0 - macro filename, this will be also registered command name
# 1 - icon filename extension (only extension, filename will be get from macro filename)
# 2 - MenuText - command name visible for user after icon mouse hover
# 3 - ToolTip - description visible for user after icon mouse hover
#
# example: 
#
# "panelDefaultXY", "png", "panel, XY, 600x300, 18 thickness", "Click to see info.",


Tools = [

	# #################################################################################################################################
	# Woodworking - start
	# #################################################################################################################################
	
	"magicStart", "png", "magicStart, tool for easier start", "This tool was created to make it easier to start designing furniture. It contains some structures that I often use personally, as well as other carpentry solutions suggested by users. However, this tool does not contain a complete list of solutions, because there are too many of them in the world of carpentry, practically every carpenter and manufacturer of furniture or accessories has their own standards. I try to adjust the contents of this tool in such a way that it gives the greatest possible possibilities for later processing and adapting the initial structure to your own needs.",
	"panelDefaultXY", "png", "panelDefaultXY, to create simple default panel XY", "This tool allows you to create simple panel based on magicSettings settings.",
	"panelDefaultYX", "png", "panelDefaultYX, to create simple default panel YX", "This tool allows you to create simple panel based on magicSettings settings.",
	"panelDefaultXZ", "png", "panelDefaultXZ, to create simple default panel XZ", "This tool allows you to create simple panel based on magicSettings settings.",
	"panelDefaultZX", "png", "panelDefaultZX, to create simple default panel ZX", "This tool allows you to create simple panel based on magicSettings settings.",
	"panelDefaultYZ", "png", "panelDefaultYZ, to create simple default panel YZ", "This tool allows you to create simple panel based on magicSettings settings.",
	"panelDefaultZY", "png", "panelDefaultZY, to create simple default panel ZY", "This tool allows you to create simple panel based on magicSettings settings.",
	
	# #################################################################################################################################
	# Woodworking - move and copy
	# #################################################################################################################################
	
	"magicMove", "png", "magicMove, to move or copy panels or other objects", "This tool allows you to move, copy, and mirror furniture parts. This tool also allows you to animate movement, such as moving a container with a drawer.",
	"panelMoveXp", "png", "panelMoveXp, move back", "Click to see info.",
	"panelMoveXm", "png", "panelMoveXm, move forward", "Click to see info.",
	"panelMoveYp", "png", "panelMoveYp, move right", "Click to see info.",
	"panelMoveYm", "png", "panelMoveYm, move left", "Click to see info.",
	"panelMoveZp", "png", "panelMoveZp, move up", "Click to see info.",
	"panelMoveZm", "png", "panelMoveZm, move down", "Click to see info.",
	"magicAngle", "png", "magicAngle, to rotate", "This tool allows you to rotate objects, containers and whole furniture modules.",

	# #################################################################################################################################
	# Woodworking - resize
	# #################################################################################################################################
	
	"magicResizer", "png", "magicResizer, smart resizer tool", "This tool allows you to resize object via selected edge or to the nearest face of other object.",
	"panelResize1", "png", "panel, bigger, long+", "Click to see info.",
	"panelResize2", "png", "panel, smaller, long-", "Click to see info.",
	"panelResize3", "png", "panel, bigger, short+", "Click to see info.",
	"panelResize4", "png", "panel, smaller, short-", "Click to see info.",
	"panelResize5", "png", "panel, bigger, thickness+", "Click to see info.",
	"panelResize6", "png", "panel, smaller, thickness-", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - face
	# #################################################################################################################################
	
	"panelFaceXY", "png", "panelFaceXY, to create panel XY on selected face", "Click to see info.",
	"panelFaceYX", "png", "panelFaceYX, to create panel YX on selected face", "Click to see info.",
	"panelFaceXZ", "png", "panelFaceXZ, to create panel XZ on selected face", "Click to see info.",
	"panelFaceZX", "png", "panelFaceZX, to create panel ZX on selected face", "Click to see info.",
	"panelFaceYZ", "png", "panelFaceYZ, to create panel YZ on selected face", "Click to see info.",
	"panelFaceZY", "png", "panelFaceZY, to create panel ZY on selected face", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - between
	# #################################################################################################################################

	"panelBetweenXY", "png", "panelBetweenXY, to create panel XY between selected faces", "Click to see info.",
	"panelBetweenYX", "png", "panelBetweenYX, to create panel YX between selected faces", "Click to see info.",
	"panelBetweenXZ", "png", "panelBetweenXZ, to create panel XZ between selected faces", "Click to see info.",
	"panelBetweenZX", "png", "panelBetweenZX, to create panel ZX between selected faces", "Click to see info.",
	"panelBetweenYZ", "png", "panelBetweenYZ, to create panel YZ between selected faces", "Click to see info.",
	"panelBetweenZY", "png", "panelBetweenZY, to create panel ZY between selected faces", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - irregular shapes
	# #################################################################################################################################

	"magicManager", "png", "magicManager, to create custom panels", "This tool allows you to create a panel on a selected surface, between two surfaces, or a custom panel with a vertex-based shape. It also allows you to preview the panel before creating it.",
	"panelSideLeft", "png", "panelSideLeft, to create left side of the furniture", "Click to see info.",
	"panelSideLeftUP", "png", "panelSideLeftUP, to create left side of the furniture above", "Click to see info.",
	"panelSideRight", "png", "panelSideRight, to create right side of the furniture", "Click to see info.",
	"panelSideRightUP", "png", "panelSideRightUP, to create right side of the furniture above", "Click to see info.",
	"panelBackOut", "png", "panelBackOut, to create back side of the furniture outside", "Click to see info.",
	"panelCoverXY", "png", "panelCoverXY, to create top side of the furniture", "Click to see info.",
	"addExternal", "png", "addExternal, to create external geometry", "This tool allows you to create sketch with external geometry from selected surfaces or edges.",
	"sketch2pad", "png", "sketch2pad, to create objects from selected sketches", "This tool allows you to quickly create objects from selected sketches with one click, applying predefined settings.",
	"wires2pad", "png", "wires2pad, to create panels from closed edges in sketch", "This tool allows you to create objects from each closed edge based on selected sketches.",

	# #################################################################################################################################
	# Woodworking - position
	# #################################################################################################################################

	"panelMove2Anchor", "png", "panelMove2Anchor, move objects to selected anchor", "Click to see info.",
	"showVertex", "png", "showVertex, makes vertices more visible", "Click to see info.",
	"selectVertex", "png", "selectVertex, help to select vertices", "Click to see info.",
	"panelMove2Face", "png", "panelMove2Face, move objects to surface", "Click to see info.",
	"mapPosition", "png", "mapPosition, move objects to the first selected object", "Click to see info.",
	"panelMove2Center", "png", "panelMove2Center, move objects to center", "Click to see info.",
	"shelvesEqual", "png", "shelvesEqual, make equal space between shelves", "Click to see info.",
	
	# #################################################################################################################################
	# Woodworking - preview
	# #################################################################################################################################

	"fitModel", "png", "fitModel, set default model view", "Click to see info.",
	"makeTransparent", "png", "makeTransparent, set all objects to transparent or normal for quick preview", "Click to see info.",
	"frontsOpenClose", "png", "frontsOpenClose, open or close all fronts of the furniture", "Click to see info.",
	"magicView", "png", "magicView, create different model views and export to TechDraw", "This tool allows you to create views and export views to TechDraw.",	
	
	# #################################################################################################################################
	# Woodworking - project manage
	# #################################################################################################################################

	"magicSettings", "png", "magicSettings, tool for Woodworking workbench settings", "This tool allows you to set default settings for Woodworking workbench.",
	"selected2LinkGroup", "png", "selected2LinkGroup, to create container", "This tool allows you to move selected objects to LinkGroup container.",
	"selected2Link", "png", "selected2Link, to create link to container", "This tool allows you to create link to selected objects.",
	"selected2Group", "png", "selected2Group, to create folder", "This tool allows you to move selected objects to simple folder.",
	"selected2Assembly", "png", "selected2Assembly, to export to Assembly", "This tool allows you to convert selected objects to Assembly.",
	"selected2Outside", "png", "selected2Outside, to move objects out from selected container", "This tool allows you to move selected objects outside the container and keep global position.",
	"eyeRa", "png", "eyeRa, allows you to show objects tree structure", "This tool allows you to expand objects tree structure for each container and show its content.",
	"eyeHorus", "png", "eyeHorus, allows you to hide objects tree structure", "This tool allows you to close objects tree structure for each container and hide its content.",

	# #################################################################################################################################
	# Woodworking - decorations
	# #################################################################################################################################

	"magicColors", "png", "magicColors, to add or change colors", "This tool allows you to set colors for selected surfaces or objects in real-time. Also you can set colors from spreadsheet.",
	"setTextures", "png", "setTextures, to set textures", "This tool allows to store textures information and load textures. Also solves problem with huge project file size because this tool allows to store only link to texture not texture.",
	"makeBeautiful", "png", "makeBeautiful, make all objects more beautiful", "This tool change visible properties of all objects to look better at the picture. It can be used to make better looking screenshot. If you click again all objects will be changed back to default settings.",

	# #################################################################################################################################
	# Woodworking - dimensions
	# #################################################################################################################################

	"getDimensions", "png", "getDimensions, to create a cut-list", "This tool allows you to create cutting lists. Multiple report types are available.",
	"sheet2export", "png", "sheet2export, to export a cut-list", "This tool allows you to export cut lists to many popular file formats.",
	"showMeasurements", "png", "showMeasurements, to show the dimensions of all edges", "Click to see info.",
	"magicMeasure", "png", "magicMeasure, to show the dimensions of selected edges", "This tool allows you to obtain the dimensions of selected edges, distances to selected surfaces, distances between holes, as well as many other measurements useful when designing furniture.",

	# #################################################################################################################################
	# Woodworking - dowels and screws
	# #################################################################################################################################

	"magicDowels", "png", "magicDowels, to add dowels", "This tool allows to add mounting points to the furniture. For example you can easily add dowels or reference points for screws, shelves supporters or custom mounting points.",
	"panel2link", "png", "panel2link, to replace selected objects with links", "Click to see info.",
	"panel2clone", "png", "panel2clone, to replace selected objects with clones", "Click to see info.",
	"sketch2dowel", "png", "sketch2dowel, to create dowel from sketch hole and surface", "Click to see info.",
	"edge2dowel", "png", "edge2dowel, to create dowel from selected edge of hole", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - fixture
	# #################################################################################################################################

	"magicFixture", "png", "magicFixture, to add furniture fixture", "This tool allows you to add any type of detailed furniture fixture. You can create Link or Clone to the realistic looking part.",
	"edge2drillbit", "png", "edge2drillbit, to create drill bit from selected edge of hole", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - drilling holes
	# #################################################################################################################################

	"magicDriller", "png", "magicDriller, to drill holes", "This tool allows you to drill holes, countersinks or counterbores in a series with predefined or custom sequences.",
	"drillHoles", "png", "drillHoles, to create drill bit or drill simple holes", "Click to see info.",
	"drillCountersinks", "png", "drillCountersinks, to create drill bit or drill countersinks", "Click to see info.",
	"drillCounterbores", "png", "drillCounterbores, to create drill bit or drill counterbores", "Click to see info.",
	"drillCounterbores2x", "png", "drillCounterbores2x, to create drill bit or drill counterbores from both sides", "Click to see info.",
	"magicCNC", "png", "magicCNC, to create custom holes and export to CNC", "This tool allows you to move drill bit along selected surface and dill holes.",
	"cutDowels", "png", "cutDowels, to cut dowels from panel", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - convert
	# #################################################################################################################################
	
	"panel2pad", "png", "panel2pad, to convert a simple panel to a sketch based object", "This tool allows you to convert in-place simple panels Part::Box to PartDesign::Pad objects.",
	"panelCopyXY", "png", "panelCopyXY, to create panel XY from selected object", "This tool allows you to create simple panel in exact direction based on PartDesign object. It is some kind of backward conversion of panel2pad.",
	"panelCopyYX", "png", "panelCopyYX, to create panel YX from selected object", "This tool allows you to create simple panel in exact direction based on PartDesign object. It is some kind of backward conversion of panel2pad.",
	"panelCopyXZ", "png", "panelCopyXZ, to create panel XZ from selected object", "This tool allows you to create simple panel in exact direction based on PartDesign object. It is some kind of backward conversion of panel2pad.",
	"panelCopyZX", "png", "panelCopyZX, to create panel ZX from selected object", "This tool allows you to create simple panel in exact direction based on PartDesign object. It is some kind of backward conversion of panel2pad.",
	"panelCopyYZ", "png", "panelCopyYZ, to create panel YZ from selected object", "This tool allows you to create simple panel in exact direction based on PartDesign object. It is some kind of backward conversion of panel2pad.",
	"panelCopyZY", "png", "panelCopyZY, to create panel ZY from selected object", "This tool allows you to create simple panel in exact direction based on PartDesign object. It is some kind of backward conversion of panel2pad.",
	
	# #################################################################################################################################
	# Woodworking - parameterization
	# #################################################################################################################################

	"magicGlue", "png", "magicGlue, to add parameterization", "This tool allows you to add or remove expressions.",
	"sketch2clone", "png", "sketch2clone, to convert sketches to clones", "Click to see info.",
	"showAlias", "png", "showAlias, to show objects with alias", "Click to see info.",
	
	# #################################################################################################################################
	# Woodworking - construction
	# #################################################################################################################################

	"panel2profile", "png", "panel2profile, to create construction profiles", "Click to see info.",
	"panel2angle", "png", "panel2angle, to create construction angles", "Click to see info.",
	"panel2angle45cut", "png", "panel2angle45cut, to cut construction profile, angle 45 cut", "Click to see info.",
	"panel2frame", "png", "panel2frame, to convert panels into frame", "Click to see info.",
	"cornerBlock", "png", "cornerBlock, to create furniture table corner block", "Click to see info.",
	"cornerBrace", "png", "cornerBrace, to create furniture table corner brace", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - joinery
	# #################################################################################################################################

	"magicJoints", "png", "magicJoints, to create joints based on sketch", "This tool allows you to move or copy joints created from sketch pattern, create mortise and tenon.",
	"jointTenonCut", "png", "jointTenonCut, to create tenon by cut", "Click to see info.",
	"jointMortiseCut", "png", "jointMortiseCut, to create mortise for jointTenonCut", "Click to see info.",
	
	"grainH", "png", "grainH, to create horizontal grain direction", "Click to see info.",
	"grainV", "png", "grainV, to create vertical grain direction", "Click to see info.",
	"grainX", "png", "grainX, to create a empty of grain direction", "Click to see info.",

	"magicCut", "png", "magicCut, to cut single panel by many knives with copies", "Click to see info.",
	"magicKnife", "png", "magicKnife, to cut many panels by single knife with copies", "Click to see info.",
	"jointTenonDowel", "png", "jointTenonDowel, to create tenon as dowel", "Click to see info.",
	"cutTenonDowels", "png", "cutTenonDowels, to cut all tenons as dowels from panel with copies", "Click to see info.",
	
	"magicCorner", "png", "magicCorner, to create corner connection", "Click to see info.",
	
	"magicCutLinks", "png", "magicCutLinks, to cut single panel by many knives using link (parametric version)", "Click to see info.",
	"magicKnifeLinks", "png", "magicKnifeLinks, to cut many panels by single knife using link (parametric version)", "Click to see info.",
	"jointTenonDowelP", "png", "jointTenonDowelP, to create tenon as dowel (parametric version)", "Click to see info.",
	"cutTenonDowelsP", "png", "cutTenonDowelsP, to cut all tenons as dowels from panel using link (parametric version)", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - router
	# #################################################################################################################################

	"routerCove", "png", "routerCove, to create cove from selected edge, panel thickness", "Click to see info.",
	"routerCove2", "png", "routerCove2, to create cove from selected edge, 1/2 panel thickness", "Click to see info.",
	"routerCove4", "png", "routerCove4, to create cove from selected edge, 1/4 panel thickness", "Click to see info.",
	"routerRoundOver", "png", "routerRoundOver, to create round over from selected edge, panel thickness", "Click to see info.",
	"routerRoundOver2", "png", "routerRoundOver2, to create round over from selected edge, 1/2 panel thickness", "Click to see info.",
	"routerRoundOver4", "png", "routerRoundOver4, to create round over from selected edge, 1/4 panel thickness", "Click to see info.",
	"routerStraight2", "png", "routerStraight2, to create straight cut from selected edge, 1/2 panel thickness", "Click to see info.",
	"routerStraight3", "png", "routerStraight3, to create straight cut from selected edge, 1/3 panel thickness", "Click to see info.",
	"routerStraight4", "png", "routerStraight4, to create straight cut from selected edge, 1/4 panel thickness", "Click to see info.",
	"routerChamfer", "png", "routerChamfer, to create chamfer from selected edge, panel thickness", "Click to see info.",
	"routerChamfer2", "png", "routerChamfer2, to create chamfer from selected edge, 1/2 panel thickness", "Click to see info.",
	"routerChamfer4", "png", "routerChamfer4, to create chamfer from selected edge, 1/4 panel thickness", "Click to see info.",
	"multiPocket", "png", "multiPocket, to create pocket from selected sketch, panel thickness", "Click to see info.",
	"multiPocket2", "png", "multiPocket2, to create pocket from selected sketch, 1/2 panel thickness", "Click to see info.",
	"multiPocket4", "png", "multiPocket4, to create pocket from selected sketch, 1/4 panel thickness", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - advanced
	# #################################################################################################################################

	"addVeneer", "png", "addVeneer, to create simulation of veneer", "This tool allows you to simulate needed offset for veneer.",
	"align2Curve", "png", "align2Curve, to align panel to selected curve", "Click to see info.",
	"roundCurve", "png", "roundCurve, to render curve precisely", "Click to see info.",
	"showOccupiedSpace", "png", "showOccupiedSpace, to show occupied space", "This tool allows you to calculate the overall occupied space in 3D by the selected parts or whole model, if nothing is selected.",
	"showConstraints", "png", "showConstraints, to select edges equal to constraints", "Click to see info.",
	
	# #################################################################################################################################
	# Woodworking - code and debug
	# #################################################################################################################################

	"scanObjects", "png", "scanObjects, for development purposes", "Inspection tool for FreeCAD macro development & project debug (live API).",
	"showPlacement", "png", "showPlacement, for development purposes", "This tool allows you to see objects anchor placement for selected objects or for all objects, if nothing was selected. Also allows for quick global placement function debugging and further improvements.",
	"debugInfo", "png", "debugInfo, to show system info and update Woodworking workbench", "This tool allows you to show installation information and update Woodworking workbench, if there is new version available."  # no comma at the end

	# #################################################################################################################################	
]

