# this is my API MarkDown doc generator
# usage: python3 ./makeAPI.py ../Tools/MagicPanels.py > ./MagicPanelsAPI.md


import sys

data = ""
api = []

file =  open(sys.argv[1], 'r')
data = file.readlines()

openHeader = False
openFunction = False
openComment = False
openGlobals = False
openGitHub = False
out = ""

for line in data:
	
	# open and close section
	
	if line.startswith("# Globals") == True:
		if openGlobals == False:
			openGlobals = True
		else:
			openGlobals = False
	
	if line.startswith("# ####") == True:
		if openHeader == False:
			openHeader = True
		else:
			openHeader = False

	if line.startswith("def ") == True:
		if line.endswith("#\n") == False:
			openFunction = True
		if openHeader == True:
			openHeader = False

	if line.find("'''") != -1:
		if openComment == False:
			openComment = True
		else:
			openComment = False
			if openFunction == True:
				openFunction = False
	
	if openGitHub == True:
		openGitHub = False
	
	if line.startswith("# >") == True:
		openGitHub = True

	# create output section
	
	if openGlobals == True:
		if line.find(" = ") != -1:
			out = line
			out = out.replace("\n","")
			out = out.replace("   ","")
			out = out.replace("  ","")
			out = out.replace("# ","`: ")
			out = "*" + " `" + out
			api.append(out)
	
	if openHeader == True:
		if line.find("# #######") == -1:
			out = line
			out = out.replace("\n","")
			out = out.replace("#\n","")
			out = out.replace("'''","")
			api.append(out)
	
	if openFunction == True:
		out = line
		out = out.replace("'''","")
		out = out.replace("\n","")
		out = out.replace("def ","### ")
		out = out.replace("\tDescription:","##### Description:")
		out = out.replace("\tArgs:","##### Args:")
		out = out.replace("\tUsage:","##### Usage:")
		out = out.replace("\tResult:","##### Result:")
		api.append(out)
		
	if openGitHub == True:
		out = line
		out = out.replace("\n","")
		out = out.replace("# > [!","\n> [!")
		out = out.replace("# >",">")
		api.append(out)
	
	
for txt in api:
	print(txt)
