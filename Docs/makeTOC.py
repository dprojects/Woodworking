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
	if line.startswith("#") == True:
		
		if line.startswith("# ") == True:
			
			link = line.replace("\n","")
			link = link.lower()
			link = link.replace("# ","")
			link = link.replace(" ","-")
			link = link.replace(",","")
			
			head = line.replace("\n","")
			head = head.replace("# ","")
			
			entry = "* [" + head + "](#" + link + ")"
		
			toc.append(entry)
			
		if line.startswith("## ") == True:
			
			link = line.replace("\n","")
			link = link.lower()
			link = link.replace("## ","")
			link = link.replace(" ","-")
			link = link.replace(",","")
			
			head = line.replace("\n","")
			head = head.replace("## ","")
			
			entry = "\t" + "* [" + head + "](#" + link + ")"
		
			toc.append(entry)
			
		if line.startswith("### ") == True:
			
			link = line.replace("\n","")
			link = link.lower()
			link = link.replace("### ","")
			link = link.replace(" ","-")
			link = link.replace(",","")
			
			head = line.replace("\n","")
			head = head.replace("### ","")
			
			entry = "\t\t" + "* [" + head + "](#" + link + ")"
		
			toc.append(entry)
			
		if line.startswith("#### ") == True:
			
			link = line.replace("\n","")
			link = link.lower()
			link = link.replace("#### ","")
			link = link.replace(" ","-")
			link = link.replace(",","")
			
			head = line.replace("\n","")
			head = head.replace("#### ","")
			
			entry = "\t\t\t" + "* [" + head + "](#" + link + ")"
		
			toc.append(entry)
			
		if line.startswith("##### ") == True:
			
			link = line.replace("\n","")
			link = link.lower()
			link = link.replace("##### ","")
			link = link.replace(" ","-")
			link = link.replace(",","")
			
			head = line.replace("\n","")
			head = head.replace("##### ","")
			
			entry = "\t\t\t\t" + "* [" + head + "](#" + link + ")"
		
			toc.append(entry)


for t in toc:
	print(t)
