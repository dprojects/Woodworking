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
	"panelDefaultXY", "png", "panel, XY, 600x300, 18 thickness", "Click to see info.",
	"panelDefaultYX", "png", "panel, YX, 300x600, 18 thickness", "Click to see info.",
	"panelDefaultXZ", "png", "panel, XZ, 600x300, 18 thickness", "Click to see info.",
	"panelDefaultZX", "png", "panel, ZX, 300x600, 18 thickness", "Click to see info.",
	"panelDefaultYZ", "png", "panel, YZ, 600x300, 18 thickness", "Click to see info.",
	"panelDefaultZY", "png", "panel, ZY, 300x600, 18 thickness", "Click to see info.",
	
	# #################################################################################################################################
	# Woodworking - copy
	# #################################################################################################################################
	
	"panelCopyXY", "png", "copy panel, XY", "Click to see info.",
	"panelCopyYX", "png", "copy panel, YX", "Click to see info.",
	"panelCopyXZ", "png", "copy panel, XZ", "Click to see info.",
	"panelCopyZX", "png", "copy panel, ZX", "Click to see info.",
	"panelCopyYZ", "png", "copy panel, YZ", "Click to see info.",
	"panelCopyZY", "png", "copy panel, ZY", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - move
	# #################################################################################################################################
	
	"magicMove", "png", "magicMove", "Tool to move, copy and mirror parts of the furniture.",
	"magicAngle", "png", "magicAngle", "Tool to rotate, for example open furniture fronts.",
	"mapPosition", "png", "move to 1st selected", "Click to see info.",
	"panelMove2Face", "png", "panel, move, to face", "Click to see info.",
	"panelMove2Anchor", "png", "panel, move, to anchor", "Click to see info.",
	"panelMove2Center", "png", "panel, move, to center", "Click to see info.",
	"shelvesEqual", "png", "make equal space between shelves", "Click to see info.",
	"align2Curve", "png", "align panel to curve", "Click to see info.",
	"panelMoveXp", "png", "panel, move, back", "Click to see info.",
	"panelMoveXm", "png", "panel, move, forward", "Click to see info.",
	"panelMoveYp", "png", "panel, move, right", "Click to see info.",
	"panelMoveYm", "png", "panel, move, left", "Click to see info.",
	"panelMoveZp", "png", "panel, move, up", "Click to see info.",
	"panelMoveZm", "png", "panel, move, down", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - resize
	# #################################################################################################################################
	
	"magicResizer", "png", "magicResizer, smart resizer tool", "This tool allows to resize object via selected edge or to the nearest face of other object.",
	"showConstraints", "png", "select edges equal to constraints", "Click to see info.",
	"panelResize1", "png", "panel, bigger, long+", "Click to see info.",
	"panelResize2", "png", "panel, smaller, long-", "Click to see info.",
	"panelResize3", "png", "panel, bigger, short+", "Click to see info.",
	"panelResize4", "png", "panel, smaller, short-", "Click to see info.",
	"panelResize5", "png", "panel, bigger, thickness+", "Click to see info.",
	"panelResize6", "png", "panel, smaller, thickness-", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - face
	# #################################################################################################################################
	
	"panelFaceXY", "png", "copy panel, face, XY", "Click to see info.",
	"panelFaceYX", "png", "copy panel, face, YX", "Click to see info.",
	"panelFaceXZ", "png", "copy panel, face, XZ", "Click to see info.",
	"panelFaceZX", "png", "copy panel, face, ZX", "Click to see info.",
	"panelFaceYZ", "png", "copy panel, face, YZ", "Click to see info.",
	"panelFaceZY", "png", "copy panel, face, ZY", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - between
	# #################################################################################################################################

	"panelBetweenXY", "png", "panel, between, XY", "Click to see info.",
	"panelBetweenYX", "png", "panel, between, YX", "Click to see info.",
	"panelBetweenXZ", "png", "panel, between, XZ", "Click to see info.",
	"panelBetweenZX", "png", "panel, between, ZX", "Click to see info.",
	"panelBetweenYZ", "png", "panel, between, YZ", "Click to see info.",
	"panelBetweenZY", "png", "panel, between, ZY", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - special
	# #################################################################################################################################

	"magicManager", "png", "magicManager", "If you have problem with unexpected result of face or between Magic Panels, you can use this tool to preview panel before creation. It may take more time to create panel, but you can select exact panel to apply, also the edge and vertex position. This tool allows to create panel at selected face or between two faces.",
	"panelSideLeft", "png", "panel, side, left", "Click to see info.",
	"panelSideLeftUP", "png", "panel, side, left, up", "Click to see info.",
	"panelSideRight", "png", "panel, side, right", "Click to see info.",
	"panelSideRightUP", "png", "panel, side, right, up", "Click to see info.",
	"panelBackOut", "png", "panel, back, out", "Click to see info.",
	"panelCoverXY", "png", "panel, top, cover", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - construction
	# #################################################################################################################################

	"panel2profile", "png", "construction profile", "Click to see info.",
	"panel2angle", "png", "construction angle", "Click to see info.",
	"panel2angle45cut", "png", "construction angle 45 cut", "Click to see info.",
	"cornerBlock", "png", "table corner block", "Click to see info.",
	"cornerBrace", "png", "table corner brace", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - dowels and screws
	# #################################################################################################################################

	"magicDowels", "png", "magicDowels", "This tool allows to add mounting points to the furniture. For example you can easily add dowels or reference points for screws, shelves supporter pins or custom mounting points.",
	"panel2link", "png", "replace with links", "Click to see info.",
	"panel2clone", "png", "replace with clones", "Click to see info.",
	"sketch2dowel", "png", "dowel from sketch hole and face", "Click to see info.",
	"edge2dowel", "png", "dowel from edge hole", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - fixture
	# #################################################################################################################################

	"magicFixture", "png", "magicFixture", "Allows to add any type of detailed fixture to the furniture. You can create Link or Clone to the realistic looking part.",
	"edge2drillbit", "png", "drill bit from edge hole", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - joinery
	# #################################################################################################################################

	"magicJoints", "png", "magicJoints", "Allows to move, copy joint Sketch pattern and create Mortise and Tenon.",
	"magicCut", "png", "single panel cut by many knives with copies", "Click to see info.",
	"magicCutLinks", "png", "single panel cut by many knives with links", "Click to see info.",
	"magicKnife", "png", "single knife cut many panels with copies", "Click to see info.",
	"magicKnifeLinks", "png", "single knife cut many panels with links", "Click to see info.",
	"jointTenon", "png", "joint, Tenon", "Click to see info.",
	"cutTenons", "png", "cut all tenons from panel", "Click to see info.",
	"jointCustom", "png", "joint, Custom", "Click to see info.",
	"panel2frame", "png", "cubes to frames", "Click to see info.",
	"grainH", "png", "grain direction marker, horizontal", "Click to see info.",
	"grainV", "png", "grain direction marker, vertical", "Click to see info.",
	"grainX", "png", "grain direction marker, no grain", "Click to see info.",
	"magicCorner", "png", "create corner connection", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - drilling holes
	# #################################################################################################################################

	"magicDriller", "png", "magicDriller", "Allows to drill holes, countersinks or counterbores in a series with predefined or custom sequences.",
	"drillHoles", "png", "drill bit, drill simple holes", "Click to see info.",
	"drillCountersinks", "png", "drill bit, drill countersinks", "Click to see info.",
	"drillCounterbores", "png", "drill bit, drill counterbores", "Click to see info.",
	"drillCounterbores2x", "png", "drill bit, drill counterbores from both sides", "Click to see info.",
	"magicCNC", "png", "magicCNC, drill bit move machine", "This tool allows to move drill bit at the selected face and drill holes.",
	"cutDowels", "png", "cut dowels from panel", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - router
	# #################################################################################################################################

	"routerCove", "png", "edge to cove, thickness", "Click to see info.",
	"routerCove2", "png", "edge to cove, 1/2 thickness", "Click to see info.",
	"routerCove4", "png", "edge to cove, 1/4 thickness", "Click to see info.",
	"routerRoundOver", "png", "edge to round over, thickness", "Click to see info.",
	"routerRoundOver2", "png", "edge to round over, 1/2 thickness", "Click to see info.",
	"routerRoundOver4", "png", "edge to round over, 1/4 thickness", "Click to see info.",
	"routerStraight2", "png", "edge to straight, 1/2 thickness", "Click to see info.",
	"routerStraight3", "png", "edge to straight, 1/3 thickness", "Click to see info.",
	"routerStraight4", "png", "edge to straight, 1/4 thickness", "Click to see info.",
	"routerChamfer", "png", "edge to chamfer, thickness", "Click to see info.",
	"routerChamfer2", "png", "edge to chamfer, 1/2 thickness", "Click to see info.",
	"routerChamfer4", "png", "edge to chamfer, 1/4 thickness", "Click to see info.",
	"multiPocket", "png", "multi Sketch to Pocket, thickness", "Click to see info.",
	"multiPocket2", "png", "multi Sketch to Pocket, 1/2 thickness", "Click to see info.",
	"multiPocket4", "png", "multi Sketch to Pocket, 1/4 thickness", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - decorations
	# #################################################################################################################################

	"magicColors", "png", "magicColors", "This tool allows you to browse colors for manually selected faces or objects and see the effect at 3D model in real-time. Also you can set face colors for all objects from spreadsheet. ",
	"setTextures", "png", "setTextures", "This tool allows to store textures information and load textures. Also solves problem with huge project file size because this tool allows to store only link to texture not texture.",
	"makeBeautiful", "png", "make all objects more beautiful", "This tool change all objects to look better at the picture. It can be used to make better looking screenshot. If you click again all objects will be changed back to default settings.",

	# #################################################################################################################################
	# Woodworking - dimensions
	# #################################################################################################################################

	"getDimensions", "png", "getDimensions, BOM, cutlist", "Creates spreadsheet with dimensions to cut.",
	"sheet2export", "png", "sheet2export", "Exports spreadsheet to chosen file format.",
	"showOccupiedSpace", "png", "show, selected, space", "This tool allows you to calculate the overall occupied space in 3D by the selected parts or whole model, if nothing is selected.",
	"magicMeasure", "png", "magicMeasure", "Quick measurement preview on hover or by selection.",

	# #################################################################################################################################
	# Woodworking - project manage
	# #################################################################################################################################

	"magicSettings", "png", "magicSettings, tool for Woodworking workbench settings", "This tool allows you to set default settings for Woodworking workbench.",
	"selected2Group", "png", "selected to Group", "Click to see info.",
	"selected2LinkGroup", "png", "selected to LinkGroup", "Click to see info.",
	"selected2Link", "png", "selected to Link", "Click to see info.",
	"selected2Outside", "png", "move outside the container", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - code and debug
	# #################################################################################################################################

	"scanObjects", "png", "scanObjects", "Inspection tool for FreeCAD macro development & project debug (live API).",
	"showPlacement", "png", "showPlacement", "Allows to see objects anchor placement for selected objects or for all objects, if nothing was selected. Also allows for quick global placement function debugging and further improvements.",
	"debugInfo", "png", "debugInfo", "This tool shows installation information and allows to update if there is new version available.",

	# #################################################################################################################################
	# Woodworking - parameterization
	# #################################################################################################################################

	"magicGlue", "png", "magicGlue", "This tool allows to add or remove expressions.",
	"sketch2clone", "png", "Convert sketches to clones.", "Click to see info.",
	"showAlias", "png", "Select objects with alias.", "Click to see info.",
	
	# #################################################################################################################################
	# Woodworking - advanced
	# #################################################################################################################################

	"panel2pad", "png", "cube to pad", "Click to see info.",
	"addExternal", "png", "add external geometry", "Click to see info.",
	"wires2pad", "png", "create Pad from wires in sketch", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - preview
	# #################################################################################################################################

	"fitModel", "png", "fitModel", "Click to see info.",
	"makeTransparent", "png", "make objects transparent or normal", "Click to see info.",
	"magicView", "png", "magicView, create views and export to TechDraw", "This tool allows you to create views and export views to TechDraw.",
	"showVertex", "png", "showVertex", "Click to see info.",
	"selectVertex", "png", "selectVertex", "Click to see info.",
	"roundCurve", "png", "render curve precisely", "Click to see info." # no comma at the end

	# #################################################################################################################################	
]

