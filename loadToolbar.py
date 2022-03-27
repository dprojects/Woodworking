def getItems(iType):

	parts = []

	if iType == "Parameterization":
		
		parts = [
			"Spreadsheet_CreateSheet",
			"Spreadsheet_MergeCells"
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

	if iType == "Operations":
		
		parts = [
			"PartDesign_Hole",
			"Part_Boolean"
		]

	if iType == "Manage":
		
		parts = [
			"Std_ViewFitAll",
			"Std_Group",
			"Std_LinkMakeGroup",
			"Std_LinkMake",
			"Std_MergeProjects"
		]

	if iType == "Coding":
		
		parts = [
			"Std_DlgMacroExecute",
			"Std_DlgMacroExecuteDirect",
			"Std_About",
			"Std_DependencyGraph"
		]
		
	return parts
