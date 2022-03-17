def getItems(iType):

	parts = []

	if iType == "Structure":
		
		parts = [ 
			"PartDesign_Body", 
			"PartDesign_NewSketch", 
			"PartDesign_Pad" 
		]
		
	if iType == "Furniture Parts":
		
		parts = [ 
			"Part_Box", 
		]
	
	if iType == "Transformations":
		
		parts = [
			"Spreadsheet_CreateSheet",
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

	return parts

