import loadTools

def getItems(iType):

	parts = []

	if iType == "Parameterization":
		
		parts = [
			"Spreadsheet_CreateSheet",
			"Spreadsheet_MergeCells"
		]

	if iType == "Magic Panels":
		
		parts = [
			"panelXY",
			"panelXZ",
			"panelYZ",
			"panelXYFace",
			"panelXZFace",
			"panelYZFace",
			"panelXYBetween",
			"panelXZBetween",
			"panelYZBetween",
			"panelXYCover",
			"panelXZCover",
			"panelYZCover"
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
			"Part_Torus",
			"Part_Cone",
			"Part_Sphere",
			"Part_Cylinder",
			"Part_Boolean"
		]

	if iType == "Dimensions":
		
		parts = [
			"Part_Measure_Linear",
			"BOM",
			"Std_Print",
			"HTML"
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
			"Std_ViewFitAll",
			"Std_TextureMapping",
			"SETTEXTURES"
		]

	if iType == "Code and Debug":
		
		parts = [
			"Std_DlgMacroExecute",
			"Std_DlgMacroExecuteDirect",
			"Std_DependencyGraph",
			"CODE",
			"DEBUGINFO"
		]
		
	return parts
