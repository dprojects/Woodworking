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
	# tools - not using MagicPanels library
	# #################################################################################################################################

	"", "debugInfo", "png", "debugInfo", "Copy platform details to clipboard for bug report purposes.",

	# #################################################################################################################################
	# tools - linked standalone macros (should not use MagicPanels library or be moved)
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
	# tools - using MagicPanels library
	# #################################################################################################################################

	"MagicPanels", "magicMove", "png", "magicMove", "If you have problem with unexpected result of panel movements via dedicated icons, you can use this tool to precisely move panel into desired direction. This tool allow to turn off and on axis cross and resize corner cross size.",

	"MagicPanels", "magicManager", "png", "magicManager", "If you have problem with unexpected result of Magic Panels, you can use this tool to preview panel before creation. It may take more time to create panel, but you can select exact panel to apply, also the edge and vertex position. This tool allows to create panel at selected face or between two faces.",

	"MagicPanels", "magicDowels", "png", "magicDowels", "Allows to add mounting points to the furniture. For example you can easily add screws, dowels, shelf supporter pins or custom mounting points.",

	"MagicPanels", "magicFixture", "png", "magicFixture", "Allows to add fixture reference points to the furniture. Later you will be able to replace the cube fixture reference points with realistic fixture elements.",

	"MagicPanels", "fitModel", "png", "fitModel", "Fit 3D model to the screen and set base orientation (XY, 0 key).",

	# #################################################################################################################################
	# Magic Panels - default
	# #################################################################################################################################
	
	"MagicPanels", "panelDefaultXY", "png", "panel, XY, 600x300, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultYX", "png", "panel, YX, 300x600, 18 thickness", "Click to see info.",
	
	"MagicPanels", "panelDefaultXZ", "png", "panel, XZ, 600x300, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultZX", "png", "panel, ZX, 300x600, 18 thickness", "Click to see info.",
	
	"MagicPanels", "panelDefaultYZ", "png", "panel, YZ, 600x300, 18 thickness", "Click to see info.",
	"MagicPanels", "panelDefaultZY", "png", "panel, ZY, 300x600, 18 thickness", "Click to see info.",

	# #################################################################################################################################
	# Magic Panels - copy
	# #################################################################################################################################
	
	"MagicPanels", "panelCopyXY", "png", "copy panel, XY", "Click to see info.",
	"MagicPanels", "panelCopyYX", "png", "copy panel, YX", "Click to see info.",
	
	"MagicPanels", "panelCopyXZ", "png", "copy panel, XZ", "Click to see info.",
	"MagicPanels", "panelCopyZX", "png", "copy panel, ZX", "Click to see info.",
	
	"MagicPanels", "panelCopyYZ", "png", "copy panel, YZ", "Click to see info.",
	"MagicPanels", "panelCopyZY", "png", "copy panel, ZY", "Click to see info.",

	# #################################################################################################################################
	# Magic Panels - move
	# #################################################################################################################################
	
	"MagicPanels", "panelMoveXp", "png", "panel, move, back", "Click to see info.",
	"MagicPanels", "panelMoveXm", "png", "panel, move, forward", "Click to see info.",
	
	"MagicPanels", "panelMoveYp", "png", "panel, move, right", "Click to see info.",
	"MagicPanels", "panelMoveYm", "png", "panel, move, left", "Click to see info.",
	
	"MagicPanels", "panelMoveZp", "png", "panel, move, up", "Click to see info.",
	"MagicPanels", "panelMoveZm", "png", "panel, move, down", "Click to see info.",

	"MagicPanels", "panelMove2Face", "png", "panel, move, to face", "Click to see info.",

	# #################################################################################################################################
	# Magic Panels - resize
	# #################################################################################################################################
	
	"MagicPanels", "panelResize1", "png", "panel, bigger, long+", "Click to see info.",
	"MagicPanels", "panelResize2", "png", "panel, smaller, long-", "Click to see info.",
	"MagicPanels", "panelResize3", "png", "panel, bigger, short+", "Click to see info.",
	"MagicPanels", "panelResize4", "png", "panel, smaller, short-", "Click to see info.",

	# #################################################################################################################################
	# Magic Panels - special
	# #################################################################################################################################
	
	"MagicPanels", "panelSideLeft", "png", "panel, side, left", "Click to see info.",
	"MagicPanels", "panelSideLeftUP", "png", "panel, side, left, up", "Click to see info.",
	
	"MagicPanels", "panelSideRight", "png", "panel, side, right", "Click to see info.",
	"MagicPanels", "panelSideRightUP", "png", "panel, side, right, up", "Click to see info.",

	"MagicPanels", "panelBackOut", "png", "panel, back, out", "Click to see info.",
	
	"MagicPanels", "panelCoverXY", "png", "panel, top, cover", "Click to see info.",
	
	# #################################################################################################################################
	# Magic Panels - replace
	# #################################################################################################################################
	
	"MagicPanels", "panel2pad", "png", "replace, cube to pad", "Click to see info.",
	
	"MagicPanels", "panel2profile", "png", "replace, cubes to construction profiles", "Click to see info.",

	"MagicPanels", "panel2frame", "png", "replace, cubes to frames", "Click to see info.",

	"MagicPanels", "panel2link", "png", "replace, cubes to links", "Click to see info.",

	# #################################################################################################################################
	# Magic Panels - face
	# #################################################################################################################################
	
	"MagicPanels", "panelFaceXY", "png", "copy panel, face, XY", "Click to see info.",
	"MagicPanels", "panelFaceYX", "png", "copy panel, face, YX", "Click to see info.",
	
	"MagicPanels", "panelFaceXZ", "png", "copy panel, face, XZ", "Click to see info.",
	"MagicPanels", "panelFaceZX", "png", "copy panel, face, ZX", "Click to see info.",
	
	"MagicPanels", "panelFaceYZ", "png", "copy panel, face, YZ", "Click to see info.",
	"MagicPanels", "panelFaceZY", "png", "copy panel, face, ZY", "Click to see info.",
		
	# #################################################################################################################################
	# Magic Panels - between
	# #################################################################################################################################
	
	"MagicPanels", "panelBetweenXY", "png", "panel, between, XY", "Click to see info.",
	"MagicPanels", "panelBetweenYX", "png", "panel, between, YX", "Click to see info.",
	
	"MagicPanels", "panelBetweenXZ", "png", "panel, between, XZ", "Click to see info.",
	"MagicPanels", "panelBetweenZX", "png", "panel, between, ZX", "Click to see info.",
	
	"MagicPanels", "panelBetweenYZ", "png", "panel, between, YZ", "Click to see info.",
	"MagicPanels", "panelBetweenZY", "png", "panel, between, ZY", "Click to see info." # no comma

	# #################################################################################################################################	
]

