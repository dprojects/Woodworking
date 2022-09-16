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
	# tools - linked standalone macros (not use MagicPanels library, not move anywhere)
	# #################################################################################################################################
	
	"", "getDimensions", "png", "getDimensions, BOM, cutlist", "Creates spreadsheet with dimensions to cut.",
	
	"", "sheet2export", "png", "sheet2export", "Exports spreadsheet to chosen file format.",
	
	"", "scanObjects", "png", "scanObjects", "Inspection tool for FreeCAD macro development & project debug (live API).",
	
	"", "setTextures", "png", "setTextures", "Store textures information and allows to load textures. Solves problem with texture sharing without huge project file size.",

	"", "makeTransparent",  "png","transparent or normal mode", "Make all parts transparent, so you can see all the joints, pilot holes, screws, countersinks. If you click next one all parts will back to normal. The transparent default is 83, so do not set any part to this number if you want e.g. to keep glass part of the furniture transparent after this preview.",

	"", "colorManager", "png", "colorManager", "Allows to set face colors for all objects from spreadsheet. Also you can browse colors for manually selected face, object or many faces or objects and see the effect at 3D model in real-time.",

	"", "magicAngle", "png", "magicAngle", "Allows to rotate panels and even other more complicated objects, like construction profiles.",

	"", "showSpaceModel", "png", "show, model, space", "This tool allows you to calculate the overall occupied space in 3D by the model.",
	
	"", "showSpaceSelected", "png", "show, selected, space", "This tool allows you to calculate the overall occupied space in 3D by the selected parts.",

	# #################################################################################################################################
	# tools - using MagicPanels library with GUI
	# #################################################################################################################################

	"MagicPanels", "magicMove", "png", "magicMove", "If you have problem with unexpected result of panel movements via dedicated icons, you can use this tool to precisely move panel into desired direction. This tool allow to turn off and on axis cross and resize corner cross size.",

	"MagicPanels", "magicManager", "png", "magicManager", "If you have problem with unexpected result of Magic Panels, you can use this tool to preview panel before creation. It may take more time to create panel, but you can select exact panel to apply, also the edge and vertex position. This tool allows to create panel at selected face or between two faces.",

	"MagicPanels", "magicDowels", "png", "magicDowels", "Allows to add mounting points to the furniture. For example you can easily add screws, dowels, shelf supporter pins or custom mounting points.",

	"MagicPanels", "magicDriller", "png", "magicDriller", "Allows to drill holes, countersinks or counterbores in a series with predefined or custom sequences.",

	"MagicPanels", "magicCNC", "png", "magicCNC, drill bit move machine", "This tool allows to move drill bit at the selected face and drill holes.",
	
	"MagicPanels", "magicFixture", "png", "magicFixture", "Allows to add any type of detailed fixture to the furniture. You can create Link to the realistic looking part or Clone it.",

	# #################################################################################################################################
	# tools - not using MagicPanels library, no GUI
	# #################################################################################################################################

	"", "debugInfo", "png", "debugInfo", "Copy platform details to clipboard for bug report purposes.",

	# #################################################################################################################################
	# tools - using MagicPanels library, no GUI
	# #################################################################################################################################

	# drilling
	
	"MagicPanels", "drillHoles", "png", "drill bit, drill simple holes", "Click to see info.",
	"MagicPanels", "drillCountersinks", "png", "drill bit, drill countersinks", "Click to see info.",
	"MagicPanels", "drillCounterbores", "png", "drill bit, drill counterbores", "Click to see info.",
	"MagicPanels", "drillCounterbores2x", "png", "drill bit, drill counterbores from both sides", "Click to see info.",
	"MagicPanels", "edge2drillbit", "png", "drill bit from edge hole", "Click to see info.",
	
	# mount
	
	"MagicPanels", "panel2link", "png", "replace with links", "Click to see info.",
	"MagicPanels", "panel2clone", "png", "replace with clones", "Click to see info.",
	"MagicPanels", "sketch2dowel", "png", "dowel from sketch hole and face", "Click to see info.",
	"MagicPanels", "edge2dowel", "png", "dowel from edge hole", "Click to see info.",
	
	# joinery
	
	"MagicPanels", "magicCut", "png", "magicCut, single panel cut by many knives", "Click to see info.",
	"MagicPanels", "magicKnife", "png", "magicKnife, single knife cut many panels", "Click to see info.",
	"MagicPanels", "jointTenon", "png", "joint, Tenon", "Click to see info.",
	"MagicPanels", "jointCustom", "png", "joint, Custom", "Click to see info.",
	"MagicPanels", "panel2frame", "png", "cubes to frames", "Click to see info.",
	
	# dimensions
	
	"MagicPanels", "showAlias", "png", "select objects with alias", "Click to see info.",
	"MagicPanels", "showConstraints", "png", "select edges equal to constraints", "Click to see info.",
	
	# default
	
	"MagicPanels", "panelDefaultXY", "png", "panel, XY, 600x300, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultYX", "png", "panel, YX, 300x600, 18 thickness", "Click to see info.",
	
	"MagicPanels", "panelDefaultXZ", "png", "panel, XZ, 600x300, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultZX", "png", "panel, ZX, 300x600, 18 thickness", "Click to see info.",
	
	"MagicPanels", "panelDefaultYZ", "png", "panel, YZ, 600x300, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultZY", "png", "panel, ZY, 300x600, 18 thickness", "Click to see info.",

	# copy
	
	"MagicPanels", "panelCopyXY", "png", "copy panel, XY", "Click to see info.",
	"MagicPanels", "panelCopyYX", "png", "copy panel, YX", "Click to see info.",
	
	"MagicPanels", "panelCopyXZ", "png", "copy panel, XZ", "Click to see info.",
	"MagicPanels", "panelCopyZX", "png", "copy panel, ZX", "Click to see info.",
	
	"MagicPanels", "panelCopyYZ", "png", "copy panel, YZ", "Click to see info.",
	"MagicPanels", "panelCopyZY", "png", "copy panel, ZY", "Click to see info.",

	# move
	
	"MagicPanels", "panelMoveXp", "png", "panel, move, back", "Click to see info.",
	"MagicPanels", "panelMoveXm", "png", "panel, move, forward", "Click to see info.",
	
	"MagicPanels", "panelMoveYp", "png", "panel, move, right", "Click to see info.",
	"MagicPanels", "panelMoveYm", "png", "panel, move, left", "Click to see info.",
	
	"MagicPanels", "panelMoveZp", "png", "panel, move, up", "Click to see info.",
	"MagicPanels", "panelMoveZm", "png", "panel, move, down", "Click to see info.",

	"MagicPanels", "panelMove2Face", "png", "panel, move, to face", "Click to see info.",
	"MagicPanels", "panelMove2Center", "png", "panel, move, to center", "Click to see info.",
	"MagicPanels", "mapPosition", "png", "move to 1st selected", "Click to see info.",
	
	"MagicPanels", "fitModel", "png", "fitModel", "Click to see info.",

	# resize
	
	"MagicPanels", "panelResize1", "png", "panel, bigger, long+", "Click to see info.",
	"MagicPanels", "panelResize2", "png", "panel, smaller, long-", "Click to see info.",
	"MagicPanels", "panelResize3", "png", "panel, bigger, short+", "Click to see info.",
	"MagicPanels", "panelResize4", "png", "panel, smaller, short-", "Click to see info.",
	"MagicPanels", "panelResize5", "png", "panel, bigger, thickness+", "Click to see info.",
	"MagicPanels", "panelResize6", "png", "panel, smaller, thickness-", "Click to see info.",

	# special
	
	"MagicPanels", "panelSideLeft", "png", "panel, side, left", "Click to see info.",
	"MagicPanels", "panelSideLeftUP", "png", "panel, side, left, up", "Click to see info.",
	
	"MagicPanels", "panelSideRight", "png", "panel, side, right", "Click to see info.",
	"MagicPanels", "panelSideRightUP", "png", "panel, side, right, up", "Click to see info.",

	"MagicPanels", "panelBackOut", "png", "panel, back, out", "Click to see info.",
	
	"MagicPanels", "panelCoverXY", "png", "panel, top, cover", "Click to see info.",
	
	# advanced
	
	"MagicPanels", "panel2pad", "png", "cube to pad", "Click to see info.",
	
	# construction profiles
	
	"MagicPanels", "panel2profile", "png", "construction profile", "Click to see info.",
	"MagicPanels", "panel2angle", "png", "construction angle", "Click to see info.",
	"MagicPanels", "panel2angle45cut", "png", "construction angle 45 cut", "Click to see info.",

	# face
	
	"MagicPanels", "panelFaceXY", "png", "copy panel, face, XY", "Click to see info.",
	"MagicPanels", "panelFaceYX", "png", "copy panel, face, YX", "Click to see info.",
	
	"MagicPanels", "panelFaceXZ", "png", "copy panel, face, XZ", "Click to see info.",
	"MagicPanels", "panelFaceZX", "png", "copy panel, face, ZX", "Click to see info.",
	
	"MagicPanels", "panelFaceYZ", "png", "copy panel, face, YZ", "Click to see info.",
	"MagicPanels", "panelFaceZY", "png", "copy panel, face, ZY", "Click to see info.",

	# between
	
	"MagicPanels", "panelBetweenXY", "png", "panel, between, XY", "Click to see info.",
	"MagicPanels", "panelBetweenYX", "png", "panel, between, YX", "Click to see info.",
	
	"MagicPanels", "panelBetweenXZ", "png", "panel, between, XZ", "Click to see info.",
	"MagicPanels", "panelBetweenZX", "png", "panel, between, ZX", "Click to see info.",
	
	"MagicPanels", "panelBetweenYZ", "png", "panel, between, YZ", "Click to see info.",
	"MagicPanels", "panelBetweenZY", "png", "panel, between, ZY", "Click to see info." # no comma

	# #################################################################################################################################	
]

