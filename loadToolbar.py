import loadTools

def getItems(iType):

	parts = []

	if iType == "Woodworking - Parameterization":
		
		parts = [
			"Spreadsheet_CreateSheet"
		]

	if iType == "Woodworking - Magic Panels - default":
		
		parts = [
			"panelDefaultXY",
			"panelDefaultYX",
			"panelDefaultXZ",
			"panelDefaultZX",
			"panelDefaultYZ",
			"panelDefaultZY"
		]

	if iType == "Woodworking - Magic Panels - copy":
		
		parts = [
			"panelCopyXY",
			"panelCopyYX",
			"panelCopyXZ",
			"panelCopyZX",
			"panelCopyYZ",
			"panelCopyZY"
		]

	if iType == "Woodworking - Magic Panels - move":
		
		parts = [
			"magicMove",
			"magicAngle",
			"panelMove2Face",
			"panelMoveXp",
			"panelMoveXm",
			"panelMoveYp",
			"panelMoveYm",
			"panelMoveZp",
			"panelMoveZm",
			"fitModel"
		]

	if iType == "Woodworking - Magic Panels - resize":
		
		parts = [
			"panelResize1",
			"panelResize2",
			"panelResize3",
			"panelResize4"
		]

	if iType == "Woodworking - Magic Panels - face":
		
		parts = [
			"panelFaceXY",
			"panelFaceYX",
			"panelFaceXZ",
			"panelFaceZX",
			"panelFaceYZ",
			"panelFaceZY"
		]

	if iType == "Woodworking - Magic Panels - between":
		
		parts = [
			"panelBetweenXY",
			"panelBetweenYX",
			"panelBetweenXZ",
			"panelBetweenZX",
			"panelBetweenYZ",
			"panelBetweenZY"
		]
		
	if iType == "Woodworking - Magic Panels - special":
		
		parts = [
			"magicManager",
			"panelSideLeft",
			"panelSideRight",
			"panelSideLeftUP",
			"panelSideRightUP",
			"panelBackOut",
			"panelCoverXY"
		]

	if iType == "Woodworking - Magic Panels - replace":
		
		parts = [
			"panel2pad",
			"panel2profile",
			"panel2frame",
			"panel2link"
		]

	if iType == "Woodworking - Magic Panels - mounting":
		
		parts = [
			"magicDowels",
			"Part_Cylinder",
			"PartDesign_Hole",
			"makeTransparent"
		]

	if iType == "Woodworking - Furniture Parts":
		
		parts = [
			"Part_Box",
			"Std_Part",
			"PartDesign_Body", 
			"PartDesign_NewSketch",
			"PartDesign_Pad"
		]
	
	if iType == "Woodworking - Transformations":
		
		parts = [
			"Draft_Array",
			"Draft_PolarArray",
			"PartDesign_LinearPattern",
			"PartDesign_Plane",
			"Part_Mirror",
			"PartDesign_Mirrored",
			"PartDesign_MultiTransform",
			"Draft_Clone"
		]

	if iType == "Woodworking - Decorations":
		
		parts = [
			"Part_Boolean",
			"Part_Torus",
			"Part_Cone",
			"Part_Sphere",
			"PartDesign_Fillet",
			"PartDesign_Chamfer",
			"PartDesign_Pocket"
		]

	if iType == "Woodworking - Dimensions":
		
		parts = [
			"getDimensions",
			"Std_Print",
			"sheet2export",
			"showSpaceModel",
			"showSpaceSelected",
			"Part_Measure_Linear"
		]

	if iType == "Woodworking - Project manage":
		
		parts = [
			"Std_New",
			"Std_Save",
			"Std_Open",
			"Std_MergeProjects",
			"Std_Group",
			"Std_LinkMakeGroup",
			"Std_LinkMake"
		]

	if iType == "Woodworking - Preview":
		
		parts = [
			"colorManager",
			"Std_TextureMapping",
			"setTextures"
		]

	if iType == "Woodworking - Code and Debug":
		
		parts = [
			"scanObjects",
			"debugInfo",
			"Std_DependencyGraph",
			"Std_DlgMacroRecord",
			"Std_MacroStopRecord",
			"Std_DlgMacroExecute",
			"Std_DlgMacroExecuteDirect"
		]
		
	return parts
