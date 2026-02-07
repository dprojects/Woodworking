import loadTools

def getItems(iType):

	parts = []
	# #######################################################################
	
	if iType == "Woodworking - start":
		parts = [
			"magicStart",
			"panelDefaultXY",
			"panelDefaultYX",
			"panelDefaultXZ",
			"panelDefaultZX",
			"panelDefaultYZ",
			"panelDefaultZY"
		]

	if iType == "Woodworking - move and copy":
		parts = [
			"magicMove",
			"panelMoveXp",
			"panelMoveXm",
			"panelMoveYp",
			"panelMoveYm",
			"panelMoveZp",
			"panelMoveZm",
			"magicAngle"
		]
	
	if iType == "Woodworking - resize":
		parts = [
			"magicResizer",
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

	if iType == "Woodworking - irregular shapes":
		parts = [
			"magicManager",
			"panelSideLeft",
			"panelSideRight",
			"panelSideLeftUP",
			"panelSideRightUP",
			"panelBackOut",
			"panelCoverXY",
			"addExternal",
			"sketch2pad",
			"wires2pad"
		]

	if iType == "Woodworking - position":
		parts = [
			"panelMove2Anchor",
			"showVertex",
			"selectVertex",
			"panelMove2Face",
			"mapPosition",
			"panelMove2Center",
			"shelvesEqual"
		]

	if iType == "Woodworking - preview":
		parts = [
			"fitModel",
			"makeTransparent",
			"frontsOpenClose",
			"magicView"
		]
	
	if iType == "Woodworking - project manage":
		parts = [
			"magicSettings",
			"Std_New",
			"Std_Save",
			"Std_Open",
			"Std_MergeProjects",
			"selected2LinkGroup",
			"selected2Link",
			"selected2Group",
			"selected2Assembly",
			"selected2Outside",
			"eyeRa",
			"eyeHorus"
		]

	if iType == "Woodworking - decorations":
		parts = [
			"magicColors",
			"setTextures",
			"makeBeautiful"
		]

	if iType == "Woodworking - dimensions":
		parts = [
			"getDimensions",
			"sheet2export",
			"showMeasurements",
			"magicMeasure"
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

	if iType == "Woodworking - convert":
		parts = [
			"panel2pad",
			"panelCopyXY",
			"panelCopyYX",
			"panelCopyXZ",
			"panelCopyZX",
			"panelCopyYZ",
			"panelCopyZY"
		]

	if iType == "Woodworking - parameterization":
		parts = [
			"magicGlue", 
			"sketch2clone",
			"Spreadsheet_CreateSheet",
			"showAlias",
			"Std_VarSet"
		]

	if iType == "Woodworking - construction":
		parts = [
			"panel2profile",
			"panel2angle",
			"panel2angle45cut",
			"panel2frame",
			"cornerBlock",
			"cornerBrace"
		]

	if iType == "Woodworking - joinery":
		parts = [
			"magicJoints",
			"jointTenonCut",
			"jointMortiseCut",
			"grainH",
			"grainV",
			"grainX",
			"magicCut",
			"magicKnife",
			"jointTenonDowel",
			"cutTenonDowels",
			"magicCorner",
			"magicCutLinks",
			"magicKnifeLinks",
			"jointTenonDowelP",
			"cutTenonDowelsP"
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

	if iType == "Woodworking - advanced":
		parts = [
			"addVeneer",
			"align2Curve",
			"roundCurve",
			"showOccupiedSpace",
			"showConstraints",
			"Std_Part",
			"PartDesign_Body", 
			"PartDesign_NewSketch",
			"PartDesign_Pad"
		]

	if iType == "Woodworking - code and debug":
		parts = [
			"scanObjects",
			"showPlacement",
			"debugInfo",
			"Std_DependencyGraph",
			"Std_DlgMacroExecute",
			"Std_DlgMacroExecuteDirect",
			"Std_DlgMacroRecord"
		]

	# #######################################################################
	return parts
