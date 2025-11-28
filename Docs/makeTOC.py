# tool to generate Table Of Contents for README.md file from content
# supports 5 levels
#
# usage: python3 ./makeTOC.py README.md > ./toc.md


import sys

data = ""
toc = []

file =  open(sys.argv[1], 'r')
data = file.readlines()

for line in data:
		
		# ########################################
		# common rules
		# ########################################
		
		if line.startswith("#") == True:
			
			line = line.replace("\n","")
			
			head = line
			link = line
			
			link = link.lower()
			link = link.replace(",","")
			link = link.replace(".","")
			link = link.replace(" ","-")
			link = link.replace("#-","# ")
		
			# debug
			#toc.append(link)
			#continue
			
		# ########################################
		# individual rules
		# ########################################
		
		if line.startswith("# ") == True:
			link = link.replace("# ","")
			head = head.replace("# ","")
			entry = "* [" + head + "](#" + link + ")"
			toc.append(entry)
			
		if line.startswith("## ") == True:
			link = link.replace("## ","")
			head = head.replace("## ","")
			entry = "\t" + "* [" + head + "](#" + link + ")"
			toc.append(entry)
			
		if line.startswith("### ") == True:
			link = link.replace("### ","")
			head = head.replace("### ","")
			entry = "\t\t" + "* [" + head + "](#" + link + ")"
			toc.append(entry)
			
		if line.startswith("#### ") == True:
			link = link.replace("#### ","")
			head = head.replace("#### ","")
			entry = "\t\t\t" + "* [" + head + "](#" + link + ")"
			toc.append(entry)
			
		if line.startswith("##### ") == True:
			link = link.replace("##### ","")
			head = head.replace("##### ","")
			entry = "\t\t\t\t" + "* [" + head + "](#" + link + ")"
			toc.append(entry)

# ########################################
# final print
# ########################################
		
for t in toc:
	print(t)
