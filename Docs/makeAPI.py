# this is my API MarkDown doc generator
# usage: python3 ./makeAPI.py ../Tools/MagicPanels.py > ./MagicPanelsAPI.md


import sys

data = ""
api = []

file =  open(sys.argv[1], 'r')
data = file.readlines()

openGlobals = False
openHeaderOpen = False
openHeaderBody = False
openFunctionHeader = False
openFunctionBody = False
openDeprecated = False
openGitHub = False

out = ""

for line in data:
	
	# ##############################################################
	# open and close section - only unique line starts sections
	# ##############################################################
	
	if line.startswith("# Globals") == True:
		
		if openGlobals == False:
			openGlobals = True
		else:
			openGlobals = False
	
	if line.startswith("# ####") == True:
		
		if openFunctionHeader == False and openFunctionBody == False:
			if openHeaderOpen == False and openHeaderBody == False:
				openHeaderOpen = True
	
	if line.startswith("'''") == True:
		
		if openHeaderOpen == True:
			if openHeaderBody == False:
				openHeaderBody = True
			else:
				openHeaderOpen = False
				openHeaderBody = False
			
	if line.startswith("def ") == True:
		
		if line.endswith("#\n") == False:
			openFunctionHeader = True
		
	if line.startswith("\t'''") == True:
		
		if openFunctionHeader == True:
			if openFunctionBody == False:
				openFunctionBody = True
			else:
				openFunctionHeader = False
				openFunctionBody = False
	
	if line.find("# > ") != -1:
		openGitHub = True
	else:
		openGitHub = False
		
	if line.startswith("# DEPRECATED BEGIN") == True:
		openDeprecated = True
	
	if line.startswith("# DEPRECATED END") == True:
		openDeprecated = False
		
	# ##############################################################
	# create output section
	# ##############################################################
	
	out = line
	
	if openGlobals == True and openGitHub == False:
		
		if line.find(" = ") != -1:
			out = out.replace("\n","")
			out = out.replace("   ","")
			out = out.replace("  ","")
			out = out.replace("# ","`: ")
			out = "*" + " `" + out
			api.append(out)

	if openHeaderBody == True:
		if line.find("# #######") == -1:
			out = out.replace("\n","")
			out = out.replace("#\n","")
			out = out.replace("'''","")
			
			if line.startswith("# ") == True:
				out = out + "\n"
			
			api.append(out)
	
	if openFunctionHeader == True and openFunctionBody == False:
		out = out.replace("def ","### ")
		api.append(out)
	
	if openFunctionHeader == True and openFunctionBody == True and openGitHub == False and openDeprecated == False:
		out = out.replace("'''","")
		out = out.replace("\n","")
		out = out.replace("\tDescription:","##### Description:")
		out = out.replace("\tArgs:","##### Args:")
		out = out.replace("\tUsage:","##### Usage:")
		out = out.replace("\tResult:","##### Result:")
		api.append(out)
	
	if openGitHub == True and openDeprecated == False:
		out = out.replace("# >",">")
		out = out.lstrip()
		out = out.replace("\n","")
		out = out.replace("> [!","\n> [!")
		api.append(out)


# ##############################################################
# end file create
# ##############################################################

for txt in api:
	print(txt)
