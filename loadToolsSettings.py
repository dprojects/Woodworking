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
# 0, 1, 2, 3, 4
#
# 0 - sub-directory name
# 1 - macro filename, this will be also registered command name
# 2 - icon filename extension (only extension, filename will be get from macro filename)
# 3 - MenuText - command name visible for user after icon mouse hover
# 4 - ToolTip - description visible for user after icon mouse hover
#
# example: 
#
# "", "getDimensions", "png", "getDimensions, BOM, cutlist", "Creates spreadsheet with dimensions to cut.", # no comma if last


Tools = [

	# #################################################################################################################################
	# Woodworking - default
	# #################################################################################################################################
	
	"MagicPanels", "magicStart", "png", "magicStart, tool for easier start", "This tool was created to make it easier to start designing furniture. It contains some structures that I often use personally, as well as other carpentry solutions suggested by users. However, this tool does not contain a complete list of solutions, because there are too many of them in the world of carpentry, practically every carpenter and manufacturer of furniture or accessories has their own standards. I try to adjust the contents of this tool in such a way that it gives the greatest possible possibilities for later processing and adapting the initial structure to your own needs.",
	"MagicPanels", "panelDefaultXY", "png", "panel, XY, 600x300, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultYX", "png", "panel, YX, 300x600, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultXZ", "png", "panel, XZ, 600x300, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultZX", "png", "panel, ZX, 300x600, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultYZ", "png", "panel, YZ, 600x300, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultZY", "png", "panel, ZY, 300x600, 18 thickness", "Click to see info.",
	
	# #################################################################################################################################
	# Woodworking - copy
	# #################################################################################################################################
	
	"MagicPanels", "panelCopyXY", "png", "copy panel, XY", "Click to see info.",
	"MagicPanels", "panelCopyYX", "png", "copy panel, YX", "Click to see info.",
	"MagicPanels", "panelCopyXZ", "png", "copy panel, XZ", "Click to see info.",
	"MagicPanels", "panelCopyZX", "png", "copy panel, ZX", "Click to see info.",
	"MagicPanels", "panelCopyYZ", "png", "copy panel, YZ", "Click to see info.",
	"MagicPanels", "panelCopyZY", "png", "copy panel, ZY", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - move
	# #################################################################################################################################
	
	"MagicPanels", "magicMove", "png", "magicMove", "Tool to move, copy and mirror parts of the furniture.",
	"MagicPanels", "magicAngle", "png", "magicAngle", "Tool to rotate, for example open furniture fronts.",
	"MagicPanels", "mapPosition", "png", "move to 1st selected", "Click to see info.",
	"MagicPanels", "panelMove2Face", "png", "panel, move, to face", "Click to see info.",
	"MagicPanels", "panelMove2Anchor", "png", "panel, move, to anchor", "Click to see info.",
	"MagicPanels", "panelMove2Center", "png", "panel, move, to center", "Click to see info.",
	"MagicPanels", "shelvesEqual", "png", "make equal space between shelves", "Click to see info.",
	"MagicPanels", "align2Curve", "png", "align panel to curve", "Click to see info.",
	"MagicPanels", "panelMoveXp", "png", "panel, move, back", "Click to see info.",
	"MagicPanels", "panelMoveXm", "png", "panel, move, forward", "Click to see info.",
	"MagicPanels", "panelMoveYp", "png", "panel, move, right", "Click to see info.",
	"MagicPanels", "panelMoveYm", "png", "panel, move, left", "Click to see info.",
	"MagicPanels", "panelMoveZp", "png", "panel, move, up", "Click to see info.",
	"MagicPanels", "panelMoveZm", "png", "panel, move, down", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - resize
	# #################################################################################################################################
	
	"MagicPanels", "magicResizer", "png", "magicResizer, smart resizer tool", "This tool allows to resize object via selected edge or to the nearest face of other object.",
	"MagicPanels", "showConstraints", "png", "select edges equal to constraints", "Click to see info.",
	"MagicPanels", "panelResize1", "png", "panel, bigger, long+", "Click to see info.",
	"MagicPanels", "panelResize2", "png", "panel, smaller, long-", "Click to see info.",
	"MagicPanels", "panelResize3", "png", "panel, bigger, short+", "Click to see info.",
	"MagicPanels", "panelResize4", "png", "panel, smaller, short-", "Click to see info.",
	"MagicPanels", "panelResize5", "png", "panel, bigger, thickness+", "Click to see info.",
	"MagicPanels", "panelResize6", "png", "panel, smaller, thickness-", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - face
	# #################################################################################################################################
	
	"MagicPanels", "panelFaceXY", "png", "copy panel, face, XY", "Click to see info.",
	"MagicPanels", "panelFaceYX", "png", "copy panel, face, YX", "Click to see info.",
	"MagicPanels", "panelFaceXZ", "png", "copy panel, face, XZ", "Click to see info.",
	"MagicPanels", "panelFaceZX", "png", "copy panel, face, ZX", "Click to see info.",
	"MagicPanels", "panelFaceYZ", "png", "copy panel, face, YZ", "Click to see info.",
	"MagicPanels", "panelFaceZY", "png", "copy panel, face, ZY", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - between
	# #################################################################################################################################

	"MagicPanels", "panelBetweenXY", "png", "panel, between, XY", "Click to see info.",
	"MagicPanels", "panelBetweenYX", "png", "panel, between, YX", "Click to see info.",
	"MagicPanels", "panelBetweenXZ", "png", "panel, between, XZ", "Click to see info.",
	"MagicPanels", "panelBetweenZX", "png", "panel, between, ZX", "Click to see info.",
	"MagicPanels", "panelBetweenYZ", "png", "panel, between, YZ", "Click to see info.",
	"MagicPanels", "panelBetweenZY", "png", "panel, between, ZY", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - special
	# #################################################################################################################################

	"MagicPanels", "magicManager", "png", "magicManager", "If you have problem with unexpected result of face or between Magic Panels, you can use this tool to preview panel before creation. It may take more time to create panel, but you can select exact panel to apply, also the edge and vertex position. This tool allows to create panel at selected face or between two faces.",
	"MagicPanels", "panelSideLeft", "png", "panel, side, left", "Click to see info.",
	"MagicPanels", "panelSideLeftUP", "png", "panel, side, left, up", "Click to see info.",
	"MagicPanels", "panelSideRight", "png", "panel, side, right", "Click to see info.",
	"MagicPanels", "panelSideRightUP", "png", "panel, side, right, up", "Click to see info.",
	"MagicPanels", "panelBackOut", "png", "panel, back, out", "Click to see info.",
	"MagicPanels", "panelCoverXY", "png", "panel, top, cover", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - construction
	# #################################################################################################################################

	"MagicPanels", "panel2profile", "png", "construction profile", "Click to see info.",
	"MagicPanels", "panel2angle", "png", "construction angle", "Click to see info.",
	"MagicPanels", "panel2angle45cut", "png", "construction angle 45 cut", "Click to see info.",
	"MagicPanels", "cornerBlock", "png", "table corner block", "Click to see info.",
	"MagicPanels", "cornerBrace", "png", "table corner brace", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - dowels and screws
	# #################################################################################################################################

	"MagicPanels", "magicDowels", "png", "magicDowels", "This tool allows to add mounting points to the furniture. For example you can easily add dowels or reference points for screws, shelves supporter pins or custom mounting points.",
	"MagicPanels", "panel2link", "png", "replace with links", "Click to see info.",
	"MagicPanels", "panel2clone", "png", "replace with clones", "Click to see info.",
	"MagicPanels", "sketch2dowel", "png", "dowel from sketch hole and face", "Click to see info.",
	"MagicPanels", "edge2dowel", "png", "dowel from edge hole", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - fixture
	# #################################################################################################################################

	"MagicPanels", "magicFixture", "png", "magicFixture", "Allows to add any type of detailed fixture to the furniture. You can create Link or Clone to the realistic looking part.",
	"MagicPanels", "edge2drillbit", "png", "drill bit from edge hole", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - joinery
	# #################################################################################################################################

	"MagicPanels", "magicJoints", "png", "magicJoints", "Allows to move, copy joint Sketch pattern and create Mortise and Tenon.",
	"MagicPanels", "magicCut", "png", "single panel cut by many knives with copies", "Click to see info.",
	"MagicPanels", "magicCutLinks", "png", "single panel cut by many knives with links", "Click to see info.",
	"MagicPanels", "magicKnife", "png", "single knife cut many panels with copies", "Click to see info.",
	"MagicPanels", "magicKnifeLinks", "png", "single knife cut many panels with links", "Click to see info.",
	"MagicPanels", "jointTenon", "png", "joint, Tenon", "Click to see info.",
	"MagicPanels", "cutTenons", "png", "cut all tenons from panel", "Click to see info.",
	"MagicPanels", "jointCustom", "png", "joint, Custom", "Click to see info.",
	"MagicPanels", "panel2frame", "png", "cubes to frames", "Click to see info.",
	"MagicPanels", "grainH", "png", "grain direction marker, horizontal", "Click to see info.",
	"MagicPanels", "grainV", "png", "grain direction marker, vertical", "Click to see info.",
	"MagicPanels", "grainX", "png", "grain direction marker, no grain", "Click to see info.",
	"MagicPanels", "magicCorner", "png", "create corner connection", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - drilling holes
	# #################################################################################################################################

	"MagicPanels", "magicDriller", "png", "magicDriller", "Allows to drill holes, countersinks or counterbores in a series with predefined or custom sequences.",
	"MagicPanels", "drillHoles", "png", "drill bit, drill simple holes", "Click to see info.",
	"MagicPanels", "drillCountersinks", "png", "drill bit, drill countersinks", "Click to see info.",
	"MagicPanels", "drillCounterbores", "png", "drill bit, drill counterbores", "Click to see info.",
	"MagicPanels", "drillCounterbores2x", "png", "drill bit, drill counterbores from both sides", "Click to see info.",
	"MagicPanels", "magicCNC", "png", "magicCNC, drill bit move machine", "This tool allows to move drill bit at the selected face and drill holes.",
	"MagicPanels", "cutDowels", "png", "cut dowels from panel", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - router
	# #################################################################################################################################

	"MagicPanels", "routerCove", "png", "edge to cove, thickness", "Click to see info.",
	"MagicPanels", "routerCove2", "png", "edge to cove, 1/2 thickness", "Click to see info.",
	"MagicPanels", "routerCove4", "png", "edge to cove, 1/4 thickness", "Click to see info.",
	"MagicPanels", "routerRoundOver", "png", "edge to round over, thickness", "Click to see info.",
	"MagicPanels", "routerRoundOver2", "png", "edge to round over, 1/2 thickness", "Click to see info.",
	"MagicPanels", "routerRoundOver4", "png", "edge to round over, 1/4 thickness", "Click to see info.",
	"MagicPanels", "routerStraight2", "png", "edge to straight, 1/2 thickness", "Click to see info.",
	"MagicPanels", "routerStraight3", "png", "edge to straight, 1/3 thickness", "Click to see info.",
	"MagicPanels", "routerStraight4", "png", "edge to straight, 1/4 thickness", "Click to see info.",
	"MagicPanels", "routerChamfer", "png", "edge to chamfer, thickness", "Click to see info.",
	"MagicPanels", "routerChamfer2", "png", "edge to chamfer, 1/2 thickness", "Click to see info.",
	"MagicPanels", "routerChamfer4", "png", "edge to chamfer, 1/4 thickness", "Click to see info.",
	"MagicPanels", "multiPocket", "png", "multi Sketch to Pocket, thickness", "Click to see info.",
	"MagicPanels", "multiPocket2", "png", "multi Sketch to Pocket, 1/2 thickness", "Click to see info.",
	"MagicPanels", "multiPocket4", "png", "multi Sketch to Pocket, 1/4 thickness", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - decorations
	# #################################################################################################################################

	"MagicPanels", "magicColors", "png", "magicColors", "This tool allows you to browse colors for manually selected faces or objects and see the effect at 3D model in real-time. Also you can set face colors for all objects from spreadsheet. ",
	"", "setTextures", "png", "setTextures", "This tool allows to store textures information and load textures. Also solves problem with huge project file size because this tool allows to store only link to texture not texture.",
	"MagicPanels", "makeBeautiful", "png", "make all objects more beautiful", "This tool change all objects to look better at the picture. It can be used to make better looking screenshot. If you click again all objects will be changed back to default settings.",

	# #################################################################################################################################
	# Woodworking - dimensions
	# #################################################################################################################################

	"", "getDimensions", "png", "getDimensions, BOM, cutlist", "Creates spreadsheet with dimensions to cut.",
	"", "sheet2export", "png", "sheet2export", "Exports spreadsheet to chosen file format.",
	"MagicPanels", "showOccupiedSpace", "png", "show, selected, space", "This tool allows you to calculate the overall occupied space in 3D by the selected parts or whole model, if nothing is selected.",
	"MagicPanels", "magicMeasure", "png", "magicMeasure", "Quick measurement preview on hover or by selection.",

	# #################################################################################################################################
	# Woodworking - project manage
	# #################################################################################################################################

	"MagicPanels", "selected2Group", "png", "selected to Group", "Click to see info.",
	"MagicPanels", "selected2LinkGroup", "png", "selected to LinkGroup", "Click to see info.",
	"MagicPanels", "selected2Link", "png", "selected to Link", "Click to see info.",
	"MagicPanels", "selected2Outside", "png", "move outside the container", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - code and debug
	# #################################################################################################################################

	"", "scanObjects", "png", "scanObjects", "Inspection tool for FreeCAD macro development & project debug (live API).",
	"MagicPanels", "showPlacement", "png", "showPlacement", "Allows to see objects anchor placement for selected objects or for all objects, if nothing was selected. Also allows for quick global placement function debugging and further improvements.",
	"", "debugInfo", "png", "debugInfo", "This tool shows installation information and allows to update if there is new version available.",

	# #################################################################################################################################
	# Woodworking - parameterization
	# #################################################################################################################################

	"MagicPanels", "magicGlue", "png", "magicGlue", "This tool allows to add or remove expressions.",
	"MagicPanels", "sketch2clone", "png", "Convert sketches to clones.", "Click to see info.",
	"MagicPanels", "showAlias", "png", "Select objects with alias.", "Click to see info.",
	
	# #################################################################################################################################
	# Woodworking - advanced
	# #################################################################################################################################

	"MagicPanels", "panel2pad", "png", "cube to pad", "Click to see info.",

	# #################################################################################################################################
	# Woodworking - preview
	# #################################################################################################################################

	"MagicPanels", "fitModel", "png", "fitModel", "Click to see info.",
	"MagicPanels", "makeTransparent", "png", "make objects transparent or normal", "Click to see info.",
	"MagicPanels", "showVertex", "png", "showVertex", "Click to see info.",
	"MagicPanels", "selectVertex", "png", "selectVertex", "Click to see info.",
	"MagicPanels", "roundCurve", "png", "render curve precisely", "Click to see info." # no comma at the end

	# #################################################################################################################################	
]

