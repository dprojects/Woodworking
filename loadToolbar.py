import loadTools

def getItems(iType):

	parts = []

	if iType == "Parameterization":
		
		parts = [
			"Spreadsheet_CreateSheet"
		]

	if iType == "Magic Panels - default":
		
		parts = [
			"panelDefaultXY",
			"panelDefaultYX",
			"panelDefaultXZ",
			"panelDefaultZX",
			"panelDefaultYZ",
			"panelDefaultZY"
		]

	if iType == "Magic Panels - copy":
		
		parts = [
			"panelCopyXY",
			"panelCopyYX",
			"panelCopyXZ",
			"panelCopyZX",
			"panelCopyYZ",
			"panelCopyZY"
		]

	if iType == "Magic Panels - move":
		
		parts = [
			"magicMove",
			"magicAngle",
			"panelMoveXp",
			"panelMoveXm",
			"panelMoveYp",
			"panelMoveYm",
			"panelMoveZp",
			"panelMoveZm",
			"fitModel"
		]

	if iType == "Magic Panels - resize":
		
		parts = [
			"panelResize1",
			"panelResize2",
			"panelResize3",
			"panelResize4"
		]

	if iType == "Magic Panels - face":
		
		parts = [
			"panelFaceXY",
			"panelFaceYX",
			"panelFaceXZ",
			"panelFaceZX",
			"panelFaceYZ",
			"panelFaceZY"
		]

	if iType == "Magic Panels - between":
		
		parts = [
			"panelBetweenXY",
			"panelBetweenYX",
			"panelBetweenXZ",
			"panelBetweenZX",
			"panelBetweenYZ",
			"panelBetweenZY"
		]
		
	if iType == "Magic Panels - special":
		
		parts = [
			"magicManager",
			"panelSideLeft",
			"panelSideRight",
			"panelSideLeftUP",
			"panelSideRightUP",
			"panelBackOut",
			"panelCoverXY"
		]

	if iType == "Magic Panels - replace":
		
		parts = [
			"rpanelPad",
			"panel2profile",
			"PartDesign_Thickness",
			"panel2frame"
		]

	if iType == "Magic Panels - mounting":
		
		parts = [
			"magicDowels",
			"Part_Cylinder",
			"PartDesign_Hole",
			"makeTransparent"
		]

	if iType == "Furniture Parts":
		
		parts = [
			"Part_Box",
			"Std_Part",
			"PartDesign_Body", 
			"PartDesign_NewSketch",
			"PartDesign_Pad"
		]
	
	if iType == "Transformations":
		
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

	if iType == "Decorations":
		
		parts = [
			"Part_Boolean",
			"Part_Torus",
			"Part_Cone",
			"Part_Sphere",
			"PartDesign_Fillet",
			"PartDesign_Chamfer",
			"PartDesign_Pocket"
		]

	if iType == "Dimensions":
		
		parts = [
			"getDimensions",
			"Std_Print",
			"sheet2export",
			"Part_Measure_Linear"
		]

	if iType == "Project manage":
		
		parts = [
			"Std_New",
			"Std_Save",
			"Std_Open",
			"Std_MergeProjects",
			"Std_Group",
			"Std_LinkMakeGroup",
			"Std_LinkMake"
		]

	if iType == "Preview":
		
		parts = [
			"colorManager",
			"Std_TextureMapping",
			"setTextures"
		]

	if iType == "Code and Debug":
		
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
