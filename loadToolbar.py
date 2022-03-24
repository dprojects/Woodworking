def getItems(iType):

	parts = []

	if iType == "Parameterization":
		
		parts = [
			"Spreadsheet_CreateSheet",
			"Spreadsheet_MergeCells"
		]

	if iType == "Structure":
		
		parts = [
			"Std_LinkMakeGroup",
			"PartDesign_Body", 
			"PartDesign_NewSketch"
		]
		
	if iType == "Furniture Parts":
		
		parts = [ 
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

	if iType == "Preview":
		
		parts = [
			"Std_TextureMapping"
		]

	return parts
