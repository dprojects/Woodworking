import loadTools

def getItems(iType):

	parts = []

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
			"panel2profile",
			"panel2frame",
			"magicFixture"
		]

	if iType == "Woodworking - Magic Panels - mounting":
		
		parts = [
			"magicDowels",
			"panel2link",
			"sketch2dowel",
			"makeTransparent"
		]

	if iType == "Woodworking - Magic Panels - drilling":
		
		parts = [
			"magicCNC",
			"drillHoles",
			"drillCountersinks",
			"drillCounterbores"
		]

	if iType == "Woodworking - Decorations":
		
		parts = [
			"panel2pad",
			"PartDesign_Fillet",
			"PartDesign_Chamfer",
			"PartDesign_Pocket",
			"Part_Boolean"
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
		
	if iType == "Woodworking - Advanced":
		
		parts = [
			"Spreadsheet_CreateSheet",
			"Std_Part",
			"PartDesign_Body", 
			"PartDesign_NewSketch",
			"PartDesign_Pad"
		]
		
	return parts
