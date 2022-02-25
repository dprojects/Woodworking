def getItems(iType):

	parts = []

	if iType == "Structure":
		
		parts = [ 
			"PartDesign_Body", 
			"Sketcher_NewSketch", 
			"PartDesign_Pad" 
		]
		
	if iType == "Furniture Parts":
		
		parts = [ 
			"Part_Box", 
		]
	
	if iType == "Transformations":
		
		parts = [ 
			"Part_Mirror",
			"Draft_Array",
			"Draft_PolarArray",
			"Draft_Clone",
			"PartDesign_Hole",
			"PartDesign_LinearPattern",
			"PartDesign_Mirrored",
			"PartDesign_MultiTransform"
		]
		
	if iType == "Operations":
		
		parts = [
			"Part_Boolean"
		]

	return parts

