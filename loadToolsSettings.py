# This is setting file for loadToolsAuto generator. 
# If you want to add new macro and create command Class for it, 
# add here the macro name and run loadToolsAuto.py once.
# There is no need to add loadToolsAuto.py to workbench startup.

# Macro row order:
# "macro name", "special directory name", "command name", "MenuText", "ToolTip"

Tools = [
	
	# #################################################################################################################################
	# tools
	# #################################################################################################################################
	
	"getDimensions", "", "getDimensions", "getDimensions, BOM, cutlist", "Creates spreadsheet with dimensions to cut.",
	
	"sheet2export", "", "sheet2export", "sheet2export", "Exports spreadsheet to chosen file format.",
	
	"scanObjects", "", "scanObjects", "scanObjects", "Inspection tool for FreeCAD macro development & project debug.",
	
	"setTextures", "", "setTextures", "setTextures", "Store textures URL at object's property and allows to load textures from stored URL.",
	
	"debugInfo", "", "debugInfo", "debugInfo", "Copy platform details to clipboard for bug report purposes.",
	
	# #################################################################################################################################
	# Magic Panels - default
	# #################################################################################################################################
	
	"panelDefaultXY", "MagicPanels", "panelDefaultXY", "panel, XY, 600x300, 18 thickness", "Create default panel with dimensions 600 mm x 300 mm and 18 mm thickness in the XY direction, described by the icon. Change dimensions and placement at object property window, if needed.",
	
	"panelDefaultYX", "MagicPanels", "panelDefaultYX", "panel, YX, 300x600, 18 thickness", "Create default panel with dimensions 300 mm x 600 mm and 18 mm thickness in the YX direction, described by the icon. Change dimensions and placement at object property window, if needed.",
		
	"panelDefaultXZ", "MagicPanels", "panelDefaultXZ", "panel, XZ, 600x300, 18 thickness", "Create default panel with dimensions 600 mm x 300 mm and 18 mm thickness in the XZ direction, described by the icon. Change dimensions and placement at object property window, if needed.",
	
	"panelDefaultZX", "MagicPanels", "panelDefaultZX", "panel, ZX, 300x600, 18 thickness", "Create default panel with dimensions 300 mm x 600 mm and 18 mm thickness in the ZX direction, described by the icon. Change dimensions and placement at object property window, if needed.",
		
	"panelDefaultYZ", "MagicPanels", "panelDefaultYZ", "panel, YZ, 600x300, 18 thickness", "Create default panel with dimensions 600 mm x 300 mm and 18 mm thickness in the YZ direction, described by the icon. Change dimensions and placement at object property window, if needed.",

	"panelDefaultZY", "MagicPanels", "panelDefaultZY", "panel, ZY, 300x600, 18 thickness", "Create default panel with dimensions 300 mm x 600 mm and 18 mm thickness in the ZY direction, described by the icon. Change dimensions and placement at object property window, if needed.",

	# #################################################################################################################################
	# Magic Panels - copy
	# #################################################################################################################################
	
	"panelCopyXY", "MagicPanels", "panelCopyXY", "copy panel to XY", "Copy selected panel to XY direction, described by the icon. If you select any supported panel in other direction, e.g. XZ, this will be some kind of copy panel with exact rotation. Change dimensions and placement at object property window, if needed.",
	
	"panelCopyYX", "MagicPanels", "panelCopyYX", "copy panel to YX", "Copy selected panel to YX direction, described by the icon.  If you select any supported panel in other direction, e.g. XZ, this will be some kind of copy panel with exact rotation. Change dimensions and placement at object property window, if needed.",
		
	"panelCopyXZ", "MagicPanels", "panelCopyXZ", "copy panel to XZ", "Copy selected panel to XZ direction, described by the icon.  If you select any supported panel in other direction, e.g. XY, this will be some kind of copy panel with exact rotation. Change dimensions and placement at object property window, if needed.",
	
	"panelCopyZX", "MagicPanels", "panelCopyZX", "copy panel to ZX", "Copy selected panel to ZX direction, described by the icon.  If you select any supported panel in other direction, e.g. XY, this will be some kind of copy panel with exact rotation. Change dimensions and placement at object property window, if needed.",
		
	"panelCopyYZ", "MagicPanels", "panelCopyYZ", "copy panel to YZ", "Copy selected panel to YZ direction, described by the icon.  If you select any supported panel in other direction, e.g. XY, this will be some kind of copy panel with exact rotation. Change dimensions and placement at object property window, if needed.",

	"panelCopyZY", "MagicPanels", "panelCopyZY", "copy panel to ZY", "Copy selected panel to ZY direction, described by the icon.  If you select any supported panel in other direction, e.g. XY, this will be some kind of copy panel with exact rotation. Change dimensions and placement at object property window, if needed.",

	# #################################################################################################################################
	# Magic Panels - face
	# #################################################################################################################################
	
	"panelFaceXY", "MagicPanels", "panelFaceXY", "copy panel at face to XY", "Copy selected panel at selected face to XY direction, described by the icon.",

	"panelFaceYX", "MagicPanels", "panelFaceYX", "copy panel at face to YX", "Copy selected panel at selected face to YX direction, described by the icon.",
	
	"panelFaceXZ", "MagicPanels", "panelFaceXZ", "copy panel at face to XZ", "Copy selected panel at selected face to XZ direction, described by the icon.",

	"panelFaceZX", "MagicPanels", "panelFaceZX", "copy panel at face to ZX", "Copy selected panel at selected face to ZX direction, described by the icon.",
	
	"panelFaceYZ", "MagicPanels", "panelFaceYZ", "copy panel at face to YZ", "Copy selected panel at selected face to YZ direction, described by the icon.",

	"panelFaceZY", "MagicPanels", "panelFaceZY", "copy panel at face to ZY", "Copy selected panel at selected face to ZY direction, described by the icon.",
		
	# #################################################################################################################################
	# Magic Panels - between
	# #################################################################################################################################
	
	"panelBetweenXY", "MagicPanels", "panelBetweenXY", "panel between 2 faces to XY", "Copy 1st selected panel between 1st and 2nd selected faces according to the XY direction, described by the icon.",

	"panelBetweenYX", "MagicPanels", "panelBetweenYX", "panel between 2 faces to YX", "Copy 1st selected panel between 1st and 2nd selected faces according to the YX direction, described by the icon.",
	
	"panelBetweenXZ", "MagicPanels", "panelBetweenXZ", "panel between 2 faces to XZ", "Copy 1st selected panel between 1st and 2nd selected faces according to the XZ direction, described by the icon.",

	"panelBetweenZX", "MagicPanels", "panelBetweenZX", "panel between 2 faces to ZX", "Copy 1st selected panel between 1st and 2nd selected faces according to the ZX direction, described by the icon.",
	
	"panelBetweenYZ", "MagicPanels", "panelBetweenYZ", "panel between 2 faces to YZ", "Copy 1st selected panel between 1st and 2nd selected faces according to the YZ direction, described by the icon.",

	"panelBetweenZY", "MagicPanels", "panelBetweenZY", "panel between 2 faces to ZY", "Copy 1st selected panel between 1st and 2nd selected faces according to the ZY direction, described by the icon.",
	
	# #################################################################################################################################
	# Magic Panels - move
	# #################################################################################################################################
	
	"panelMoveXp", "MagicPanels", "panelMoveXp", "panel, move, X+", "Allow to move panel in the described direction. The move step is the selected panel thickness.",

	"panelMoveXm", "MagicPanels", "panelMoveXm", "panel, move, X-", "Allow to move panel in the described direction. The move step is the selected panel thickness.",
	
	"panelMoveYp", "MagicPanels", "panelMoveYp", "panel, move, Y+", "Allow to move panel in the described direction. The move step is the selected panel thickness.",

	"panelMoveYm", "MagicPanels", "panelMoveYm", "panel, move, Y-", "Allow to move panel in the described direction. The move step is the selected panel thickness.",
	
	"panelMoveZp", "MagicPanels", "panelMoveZp", "panel, move, Z+", "Allow to move panel in the described direction. The move step is the selected panel thickness.",

	"panelMoveZm", "MagicPanels", "panelMoveZm", "panel, move, Z-", "Allow to move panel in the described direction. The move step is the selected panel thickness.",

	# #################################################################################################################################
	# Magic Panels - resize
	# #################################################################################################################################
	
	"panelResize1", "MagicPanels", "panelResize1", "panel, bigger, long+", "Allow to make bigger the long side of the panel. The resize step is the selected panel thickness.",

	"panelResize2", "MagicPanels", "panelResize2", "panel, smaller, long-", "Allow to make smaller the long side of the panel. The resize step is the selected panel thickness.",

	"panelResize3", "MagicPanels", "panelResize3", "panel, bigger, short+", "Allow to make bigger the short side of the panel. The resize step is the selected panel thickness.",

	"panelResize4", "MagicPanels", "panelResize4", "panel, smaller, short-", "Allow to make smaller the short side of the panel. The resize step is the selected panel thickness.",

	# #################################################################################################################################
	# Magic Panels - special
	# #################################################################################################################################
	
	"panelSideLeft", "MagicPanels", "panelSideLeft", "panel, side, left", "Creates furniture left side at selected face. Dimensions are taken from selected object. Adjust dimensions and position at object property window, if needed.",
	
	"panelSideLeftUP", "MagicPanels", "panelSideLeftUP", "panel, side, left, up", "Creates furniture left side at selected face but raised up. Dimensions are taken from selected object. Adjust dimensions and position at object property window, if needed.",
	
	"panelSideRight", "MagicPanels", "panelSideRight", "panel, side, right", "Creates furniture right side at selected face. Dimensions are taken from selected object. Adjust dimensions and position at object property window, if needed.",
	
	"panelSideRightUP", "MagicPanels", "panelSideRightUP", "panel, side, right, up", "Creates furniture right side at selected face but raised up. Dimensions are taken from selected object. Adjust dimensions and position at object property window, if needed.",

	"panelBackOut", "MagicPanels", "panelBackOut", "panel, back, out", "Creates furniture back panel at 3 selected faces. Adjust dimensions and position at object property window, if needed.",
	
	"panelCoverXY", "MagicPanels", "panelCoverXY", "panel on top 3 faces to XY", "Copy 1st selected object and resize it with 3rd selected object thickness according to the XY direction, described by the icon. You need to select 3 faces. Dimensions are taken from 1st and 3rd selected object. So, the selection order is important to get desired result. Adjust dimensions and position at object property window, if needed.",
	
	# #################################################################################################################################
	# Magic Panels - replace
	# #################################################################################################################################
	
	"rpanelPad", "MagicPanels", "rpanelPad", "panel, replace Cube to Pad", "This is replace panel and it will remove the selected Cube object and replace it with exactly the same Pad object. So, you will be able to use more transformations on that Pad."
]

