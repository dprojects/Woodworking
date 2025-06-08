# usage: python3 ./makeAPI.py ../Tools/MagicPanels.py > ./MagicPanelsAPI.md


import sys

data = ""
api = []

file =  open(sys.argv[1], 'r')
data = file.readlines()

commentOpen = False
globalsOpen = False
out = ""

for line in data:
	
	if line.startswith("# #") == True:
		continue
	
	if line.startswith("def ") == True and line.endswith("#\n") == False:
		out = line
		out = out.replace("def ","### ")
		api.append(out)
		continue

	if line.find("'''") != -1 and commentOpen == False:
		commentOpen = True
		continue
	
	if line.find("'''") != -1 and commentOpen == True:
		commentOpen = False
		continue
	
	if line.find("# Globals") != -1 and globalsOpen == False:
		globalsOpen = True
	
	if line.find("# end globals") != -1 and globalsOpen == True:
		globalsOpen = False
		continue
	
	if commentOpen == True or globalsOpen == True:
		out = line
		out = out.replace("\n","")
		out = out.replace("\tArgs:","##### Description:")
		out = out.replace("\tArgs:","##### Args:")
		out = out.replace("\tUsage:","##### Usage:")
		out = out.replace("\tResult:","##### Result:")
		api.append(out)
		continue
	
	
	
for t in api:
	print(t)
