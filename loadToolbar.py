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
			"mapPosition",
			"panelMove2Face",
			"panelMove2Anchor",
			"panelMove2Center",
			"panelMoveXp",
			"panelMoveXm",
			"panelMoveYp",
			"panelMoveYm",
			"panelMoveZp",
			"panelMoveZm"
		]

	if iType == "Woodworking - resize":
		
		parts = [
			"magicResizer",
			"showConstraints",
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
			"panel2profile",
			"panel2angle",
			"panel2angle45cut",
			"cornerBlock",
			"cornerBrace"
		]

	if iType == "Woodworking - dowels and screws":
		
		parts = [
			"magicDowels",
			"panel2link",
			"panel2clone",
			"sketch2dowel",
			"edge2dowel"
		]

	if iType == "Woodworking - fixture":
		
		parts = [
			"magicFixture",
			"edge2drillbit"
		]
	

	if iType == "Woodworking - joinery":
		
		parts = [
			"magicJoints",
			"magicCut",
			"magicKnife",
			"jointTenon",
			"jointCustom",
			"panel2frame"
		]
		
	if iType == "Woodworking - drilling holes":
		
		parts = [
			"magicDriller",
			"drillHoles",
			"drillCountersinks",
			"drillCounterbores",
			"drillCounterbores2x",
			"magicCNC",
			"cutDowels"
		]

	if iType == "Woodworking - router":
		
		parts = [
			"routerCove",
			"routerCove2",
			"routerCove4",
			"routerRoundOver",
			"routerRoundOver2",
			"routerRoundOver4",
			"routerStraight2",
			"routerStraight3",
			"routerStraight4",
			"routerChamfer",
			"routerChamfer2",
			"routerChamfer4",
			"multiPocket",
			"multiPocket2",
			"multiPocket4"
		]

	if iType == "Woodworking - decorations":
		
		parts = [
			"colorManager",
			"setTextures"
		]

	if iType == "Woodworking - dimensions":
		
		parts = [
			"getDimensions",
			"Std_Print",
			"sheet2export",
			"showSpaceModel",
			"showSpaceSelected",
			"magicMeasure"
		]

	if iType == "Woodworking - project manage":
		
		parts = [
			"Std_New",
			"Std_Save",
			"Std_Open",
			"Std_MergeProjects",
			"selected2LinkGroup",
			"selected2Link",
			"selected2Group",
			"selected2Outside"
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
			"panel2pad",
			"sketch2clone",
			"Spreadsheet_CreateSheet",
			"showAlias",
			"Std_Part",
			"PartDesign_Body", 
			"PartDesign_NewSketch",
			"PartDesign_Pad"
		]
		
	if iType == "Woodworking - preview":
		
		parts = [
			"fitModel",
			"makeTransparent"
		]

	return parts
