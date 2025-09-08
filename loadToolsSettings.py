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
	# Woodworking - default
	# #################################################################################################################################
	
	"magicStart", "png", "magicStart, tool for easier start", "This tool was created to make it easier to start designing furniture. It contains some structures that I often use personally, as well as other carpentry solutions suggested by users. However, this tool does not contain a complete list of solutions, because there are too many of them in the world of carpentry, practically every carpenter and manufacturer of furniture or accessories has their own standards. I try to adjust the contents of this tool in such a way that it gives the greatest possible possibilities for later processing and adapting the initial structure to your own needs.",
	"panelDefaultXY", "png", "panelDefaultXY, to create simple default panel XY", "Click to see info.",
	"panelDefaultYX", "png", "panelDefaultYX, to create simple default panel YX", "Click to see info.",
	"panelDefaultXZ", "png", "panelDefaultXZ, to create simple default panel XZ", "Click to see info.",
	"panelDefaultZX", "png", "panelDefaultZX, to create simple default panel ZX", "Click to see info.",
	"panelDefaultYZ", "png", "panelDefaultYZ, to create simple default panel YZ", "Click to see info.",
	"panelDefaultZY", "png", "panelDefaultZY, to create simple default panel ZY", "Click to see info.",
	
	# #################################################################################################################################
	# Woodworking - copy
	# #################################################################################################################################
	
	"panelCopyXY", "png", "panelCopyXY, to create panel XY from selected object", "Click to see info.",
	"panelCopyYX", "png", "panelCopyYX, to create panel YX from selected object", "Click to see info.",
	"panelCopyXZ", "png", "panelCopyXZ, to create panel XZ from selected object", "Click to see info.",
	"panelCopyZX", "png", "panelCopyZX, to create panel ZX from selected object", "Click to see info.",
	"panelCopyYZ", "png", "panelCopyYZ, to create panel YZ from selected object", "Click to see info.",
	"panelCopyZY", "png", "panelCopyZY, to create panel ZY from selected object", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - move
	# #################################################################################################################################
	
	"magicMove", "png", "magicMove, to move or copy panels or other objects", "Tool to move, copy and mirror parts of the furniture. This tool also allows to animate move, for example move drawer container.",
	"magicAngle", "png", "magicAngle, to rotate objects", "Tool to rotate, for example open furniture fronts. This tool also allows to animate rotations, for example open front.",
	"mapPosition", "png", "mapPosition, move to 1st selected", "Click to see info.",
	"panelMove2Face", "png", "panelMove2Face, move panel to face", "Click to see info.",
	"panelMove2Anchor", "png", "panelMove2Anchor, move to anchor", "Click to see info.",
	"panelMove2Center", "png", "panelMove2Center, move to center", "Click to see info.",
	"shelvesEqual", "png", "shelvesEqual, make equal space between shelves", "Click to see info.",
	"align2Curve", "png", "align2Curve, align panel to curve", "Click to see info.",
	"panelMoveXp", "png", "panelMoveXp, move back", "Click to see info.",
	"panelMoveXm", "png", "panelMoveXm, move forward", "Click to see info.",
	"panelMoveYp", "png", "panelMoveYp, move right", "Click to see info.",
	"panelMoveYm", "png", "panelMoveYm, move left", "Click to see info.",
	"panelMoveZp", "png", "panelMoveZp, move up", "Click to see info.",
	"panelMoveZm", "png", "panelMoveZm, move down", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - resize
	# #################################################################################################################################
	
	"magicResizer", "png", "magicResizer, smart resizer tool", "This tool allows to resize object via selected edge or to the nearest face of other object.",
	"showConstraints", "png", "showConstraints, select edges equal to constraints", "Click to see info.",
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
	# Woodworking - special
	# #################################################################################################################################

	"magicManager", "png", "magicManager, to create custom panels", "If you have problem with unexpected result of face or between Magic Panels, you can use this tool to preview panel before creation. It may take more time to create panel, but you can select exact panel to apply, also the edge and vertex position. This tool allows to create panel at selected face or between two faces.",
	"panelSideLeft", "png", "panelSideLeft, to create side left panel", "Click to see info.",
	"panelSideLeftUP", "png", "panelSideLeftUP, to create side left up panel", "Click to see info.",
	"panelSideRight", "png", "panelSideRight, to create side right panel", "Click to see info.",
	"panelSideRightUP", "png", "panelSideRightUP, to create side right up panel", "Click to see info.",
	"panelBackOut", "png", "panelBackOut, to create back out panel", "Click to see info.",
	"panelCoverXY", "png", "panelCoverXY, to create top cover panel", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - construction
	# #################################################################################################################################

	"panel2profile", "png", "panel2profile, to create construction profile", "Click to see info.",
	"panel2angle", "png", "panel2angle, to create construction angle", "Click to see info.",
	"panel2angle45cut", "png", "panel2angle45cut, to cut construction profile, angle 45 cut", "Click to see info.",
	"panel2frame", "png", "panel2frame, to convert panels into frame", "Click to see info.",
	"cornerBlock", "png", "cornerBlock, to create table corner block", "Click to see info.",
	"cornerBrace", "png", "cornerBrace, to create table corner brace", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - dowels and screws
	# #################################################################################################################################

	"magicDowels", "png", "magicDowels, to add dowels", "This tool allows to add mounting points to the furniture. For example you can easily add dowels or reference points for screws, shelves supporter pins or custom mounting points.",
	"panel2link", "png", "panel2link, replace selected objects with links", "Click to see info.",
	"panel2clone", "png", "panel2clone, replace selected objects with clones", "Click to see info.",
	"sketch2dowel", "png", "sketch2dowel, dowel from sketch hole and face", "Click to see info.",
	"edge2dowel", "png", "edge2dowel, dowel from edge hole", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - fixture
	# #################################################################################################################################

	"magicFixture", "png", "magicFixture, to add fixture", "Allows to add any type of detailed fixture to the furniture. You can create Link or Clone to the realistic looking part.",
	"edge2drillbit", "png", "edge2drillbit, drill bit from edge hole", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - joinery
	# #################################################################################################################################

	"magicJoints", "png", "magicJoints, custom joints based on Sketch", "Allows to move or copy joints created from Sketch pattern and create Mortise and Tenon.",
	"jointTenonCut", "png", "jointTenonCut, joint tenon by cut", "Click to see info.",

	"grainH", "png", "grainH, grain direction marker, horizontal", "Click to see info.",
	"grainV", "png", "grainV, grain direction marker, vertical", "Click to see info.",
	"grainX", "png", "grainX, grain direction marker, no grain", "Click to see info.",

	"magicCut", "png", "magicCut, single panel cut by many knives with copies", "Click to see info.",
	"magicKnife", "png", "magicKnife, single knife cut many panels with copies", "Click to see info.",
	"jointTenonDowel", "png", "jointTenonDowel, joint tenon as dowel", "Click to see info.",
	"cutTenonDowels", "png", "cutTenonDowels, cut all tenon dowels from panel with copies", "Click to see info.",
	
	"magicCorner", "png", "magicCorner, create corner connection", "Click to see info.",
	
	"magicCutLinks", "png", "magicCutLinks, single panel cut by many knives with links (parametric version)", "Click to see info.",
	"magicKnifeLinks", "png", "magicKnifeLinks, single knife cut many panels with links (parametric version)", "Click to see info.",
	"jointTenonDowelP", "png", "jointTenonDowelP, joint tenon as dowel (parametric version)", "Click to see info.",
	"cutTenonDowelsP", "png", "cutTenonDowelsP, cut all tenon dowels from panel with links (parametric version)", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - drilling holes
	# #################################################################################################################################

	"magicDriller", "png", "magicDriller, to drill holes", "Allows to drill holes, countersinks or counterbores in a series with predefined or custom sequences.",
	"drillHoles", "png", "drillHoles, drill bit, drill simple holes", "Click to see info.",
	"drillCountersinks", "png", "drillCountersinks, drill bit, drill countersinks", "Click to see info.",
	"drillCounterbores", "png", "drillCounterbores, drill bit, drill counterbores", "Click to see info.",
	"drillCounterbores2x", "png", "drillCounterbores2x, drill bit, drill counterbores from both sides", "Click to see info.",
	"magicCNC", "png", "magicCNC, drill bit move machine", "This tool allows to move drill bit at the selected face and drill holes.",
	"cutDowels", "png", "cutDowels, cut dowels from panel", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - router
	# #################################################################################################################################

	"routerCove", "png", "routerCove, edge to cove, thickness", "Click to see info.",
	"routerCove2", "png", "routerCove2, edge to cove, 1/2 thickness", "Click to see info.",
	"routerCove4", "png", "routerCove4, edge to cove, 1/4 thickness", "Click to see info.",
	"routerRoundOver", "png", "routerRoundOver, edge to round over, thickness", "Click to see info.",
	"routerRoundOver2", "png", "routerRoundOver2, edge to round over, 1/2 thickness", "Click to see info.",
	"routerRoundOver4", "png", "routerRoundOver4, edge to round over, 1/4 thickness", "Click to see info.",
	"routerStraight2", "png", "routerStraight2, edge to straight, 1/2 thickness", "Click to see info.",
	"routerStraight3", "png", "routerStraight3, edge to straight, 1/3 thickness", "Click to see info.",
	"routerStraight4", "png", "routerStraight4, edge to straight, 1/4 thickness", "Click to see info.",
	"routerChamfer", "png", "routerChamfer, edge to chamfer, thickness", "Click to see info.",
	"routerChamfer2", "png", "routerChamfer2, edge to chamfer, 1/2 thickness", "Click to see info.",
	"routerChamfer4", "png", "routerChamfer4, edge to chamfer, 1/4 thickness", "Click to see info.",
	"multiPocket", "png", "multiPocket, multi Sketch to Pocket, thickness", "Click to see info.",
	"multiPocket2", "png", "multiPocket2, multi Sketch to Pocket, 1/2 thickness", "Click to see info.",
	"multiPocket4", "png", "multiPocket4, multi Sketch to Pocket, 1/4 thickness", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - decorations
	# #################################################################################################################################

	"magicColors", "png", "magicColors, to add or change colors", "This tool allows you to browse colors for manually selected faces or objects and see the effect at 3D model in real-time. Also you can set face colors for all objects from spreadsheet. ",
	"setTextures", "png", "setTextures", "This tool allows to store textures information and load textures. Also solves problem with huge project file size because this tool allows to store only link to texture not texture.",
	"makeBeautiful", "png", "makeBeautiful, make all objects more beautiful", "This tool change all objects to look better at the picture. It can be used to make better looking screenshot. If you click again all objects will be changed back to default settings.",

	# #################################################################################################################################
	# Woodworking - dimensions
	# #################################################################################################################################

	"getDimensions", "png", "getDimensions, to create cut-list and BOM", "Creates spreadsheet with dimensions to cut.",
	"sheet2export", "png", "sheet2export, to export cut-list", "Exports spreadsheet to chosen file format.",
	"showOccupiedSpace", "png", "showOccupiedSpace, show occupied space", "This tool allows you to calculate the overall occupied space in 3D by the selected parts or whole model, if nothing is selected.",
	"magicMeasure", "png", "magicMeasure, custom measurement", "Quick measurement preview on hover or by selection.",

	# #################################################################################################################################
	# Woodworking - project manage
	# #################################################################################################################################

	"magicSettings", "png", "magicSettings, tool for Woodworking workbench settings", "This tool allows you to set default settings for Woodworking workbench.",
	"selected2LinkGroup", "png", "selected2LinkGroup, to create container", "This tool allows you to move selected objects to LinkGroup container.",
	"selected2Link", "png", "selected2Link, to create link to container", "This tool allows you to create link to selected objects.",
	"selected2Group", "png", "selected2Group, to create folder", "This tool allows you to move selected objects to simple folder.",
	"selected2Assembly", "png", "selected2Assembly, to export to Assembly", "This tool allows you to convert selected objects to Assembly.",
	"selected2Outside", "png", "selected2Outside, to move out from container", "This tool allows you to move selected objects outside the container and keep global position.",

	# #################################################################################################################################
	# Woodworking - code and debug
	# #################################################################################################################################

	"scanObjects", "png", "scanObjects, for development", "Inspection tool for FreeCAD macro development & project debug (live API).",
	"showPlacement", "png", "showPlacement, for development", "Allows to see objects anchor placement for selected objects or for all objects, if nothing was selected. Also allows for quick global placement function debugging and further improvements.",
	"debugInfo", "png", "debugInfo, to show system info and update Woodworking workbench", "This tool shows installation information and allows to update if there is new version available.",

	# #################################################################################################################################
	# Woodworking - parameterization
	# #################################################################################################################################

	"magicGlue", "png", "magicGlue, for parameterization", "This tool allows to add or remove expressions.",
	"sketch2clone", "png", "sketch2clone, to convert sketches to clones", "Click to see info.",
	"showAlias", "png", "showAlias, to show objects with alias", "Click to see info.",
	
	# #################################################################################################################################
	# Woodworking - advanced
	# #################################################################################################################################

	"panel2pad", "png", "panel2pad, to convert panel to object with Sketch", "This tool allows you to convert in-place simple panels Part::Box to PartDesign::Pad objects.",
	"addExternal", "png", "addExternal, to create external geometry", "This tool allows you to create sketch with external geometry from selected faces or edges.",
	"wires2pad", "png", "wires2pad, to create panels from wires in Sketch", "This tool allows you to create Pad from each wire in selected Sketches.",

	# #################################################################################################################################
	# Woodworking - preview
	# #################################################################################################################################

	"fitModel", "png", "fitModel, to view model", "Click to see info.",
	"makeTransparent", "png", "makeTransparent, make objects transparent or normal", "Click to see info.",
	"magicView", "png", "magicView, create views and export to TechDraw", "This tool allows you to create views and export views to TechDraw.",
	"showVertex", "png", "showVertex, makes vertices more visible", "Click to see info.",
	"selectVertex", "png", "selectVertex, help to select vertices", "Click to see info.",
	"roundCurve", "png", "roundCurve, render curve precisely", "Click to see info." # no comma at the end

	# #################################################################################################################################	
]

