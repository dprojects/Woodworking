# usage: python3 ./makeAPI.py ../Tools/MagicPanels/MagicPanels.py > ./MagicPanelsAPI.md


import sys

data = ""
api = []

file =  open(sys.argv[1], 'r')
data = file.readlines()

commentOpen = False
out = ""

for line in data:
	
	if line.startswith("def ") == True:
		out = line
		out = out.replace("def ","# ")
		api.append(out)
		continue

	if line.find("'''") != -1 and commentOpen == False:
		commentOpen = True
		continue
	
	if line.find("'''") != -1 and commentOpen == True:
		commentOpen = False
		continue
	
	if commentOpen == True:
		out = line
		out = out.replace("\n","")
		out = out.replace("\tArgs:","##### Args:")
		out = out.replace("\tUsage:","##### Usage:")
		out = out.replace("\tResult:","##### Result:")
		api.append(out)
		continue
	
	
	
for t in api:
	print(t)
