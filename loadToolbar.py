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
			"panelMoveXp",
			"panelMoveXm",
			"panelMoveYp",
			"panelMoveYm",
			"panelMoveZp",
			"panelMoveZm",
			"magicMove",
			"magicAngle",
			"fitModel",
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
			"panel2profile"
		]

	if iType == "Furniture Parts":
		
		parts = [
			"Std_Part",
			"PartDesign_Body", 
			"PartDesign_NewSketch",
			"PartDesign_Pad", 
			"Part_Box" 
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
			"PartDesign_Hole",
			"PartDesign_Pocket",
			"PartDesign_Fillet",
			"PartDesign_Chamfer",
			"PartDesign_Thickness",
			"Part_Torus",
			"Part_Cone",
			"Part_Sphere",
			"Part_Cylinder",
			"Part_Boolean"
		]

	if iType == "Dimensions":
		
		parts = [
			"Part_Measure_Linear",
			"getDimensions",
			"Std_Print",
			"sheet2export"
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
			"Std_TextureMapping",
			"setTextures",
			"colorManager",
			"makeTransparent"
		]

	if iType == "Code and Debug":
		
		parts = [
			"Std_DlgMacroRecord",
			"Std_MacroStopRecord",
			"Std_DlgMacroExecute",
			"Std_DlgMacroExecuteDirect",
			"Std_DependencyGraph",
			"scanObjects",
			"debugInfo"
		]
		
	return parts
