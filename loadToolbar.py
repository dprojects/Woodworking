import loadTools

def getItems(iType):

	parts = []

	if iType == "Woodworking - default":
		
		parts = [
			"panelDefaultXY",
			"panelDefaultYX",
			"panelDefaultXZ",
			"panelDefaultZX",
			"panelDefaultYZ",
			"panelDefaultZY"
		]

	if iType == "Woodworking - copy":
		
		parts = [
			"panelCopyXY",
			"panelCopyYX",
			"panelCopyXZ",
			"panelCopyZX",
			"panelCopyYZ",
			"panelCopyZY"
		]

	if iType == "Woodworking - move":
		
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

	if iType == "Woodworking - resize":
		
		parts = [
			"panelResize1",
			"panelResize2",
			"panelResize3",
			"panelResize4",
			"panelResize5",
			"panelResize6"
		]

	if iType == "Woodworking - face":
		
		parts = [
			"panelFaceXY",
			"panelFaceYX",
			"panelFaceXZ",
			"panelFaceZX",
			"panelFaceYZ",
			"panelFaceZY"
		]

	if iType == "Woodworking - between":
		
		parts = [
			"panelBetweenXY",
			"panelBetweenYX",
			"panelBetweenXZ",
			"panelBetweenZX",
			"panelBetweenYZ",
			"panelBetweenZY"
		]
		
	if iType == "Woodworking - special":
		
		parts = [
			"magicManager",
			"panelSideLeft",
			"panelSideRight",
			"panelSideLeftUP",
			"panelSideRightUP",
			"panelBackOut",
			"panelCoverXY"
		]

	if iType == "Woodworking - construction":
		
		parts = [
			"panel2profile"
		]

	if iType == "Woodworking - dowels and screws":
		
		parts = [
			"magicDowels",
			"panel2link",
			"sketch2dowel",
			"edge2dowel",
			"makeTransparent"
		]

	if iType == "Woodworking - fixture":
		
		parts = [
			"magicFixture",
			"edge2drillbit"
		]
	

	if iType == "Woodworking - joinery":
		
		parts = [
			"magicCut",
			"jointTenon",
			"jointCustom",
			"panel2frame"
		]
		
	if iType == "Woodworking - drilling holes":
		
		parts = [
			"magicCNC",
			"drillHoles",
			"drillCountersinks",
			"drillCounterbores"
		]

	if iType == "Woodworking - decorations":
		
		parts = [
			"panel2pad",
			"PartDesign_Fillet",
			"PartDesign_Chamfer",
			"PartDesign_Pocket",
			"Part_Boolean"
		]

	if iType == "Woodworking - dimensions":
		
		parts = [
			"getDimensions",
			"Std_Print",
			"sheet2export",
			"showSpaceModel",
			"showSpaceSelected",
			"Part_Measure_Linear"
		]

	if iType == "Woodworking - project manage":
		
		parts = [
			"Std_New",
			"Std_Save",
			"Std_Open",
			"Std_MergeProjects",
			"Std_Group",
			"Std_LinkMakeGroup",
			"Std_LinkMake"
		]

	if iType == "Woodworking - preview":
		
		parts = [
			"colorManager",
			"Std_TextureMapping",
			"setTextures"
		]

	if iType == "Woodworking - code and debug":
		
		parts = [
			"scanObjects",
			"debugInfo",
			"Std_DependencyGraph",
			"Std_DlgMacroRecord",
			"Std_MacroStopRecord",
			"Std_DlgMacroExecute",
			"Std_DlgMacroExecuteDirect"
		]
		
	if iType == "Woodworking - advanced":
		
		parts = [
			"Spreadsheet_CreateSheet",
			"Std_Part",
			"PartDesign_Body", 
			"PartDesign_NewSketch",
			"PartDesign_Pad"
		]
		
	return parts
