# Crude Python script to convert RRF Dozuki wiki into individual MD files per code
# hard-coded for source.txt as input
# for use with github pages, Jekyll theme based on tomjoht - documentation-theme-jekyll
# Aim is ~80% converted. Assumption that manual polish would be required per page



import re
import datetime

NETWORKS = ["M552", "M586", "M540", "M550", "M553", "M554", "M586", "M587", "M588", "M589"]
GENERAL = ["G90", "M83", "M550"]
DRIVES = ["M569", "M584", "M92", "M566", "M203" "M201", "M906", "M84" ]
AXIS = ["M208"]
ENDSTOPS = ["M574"]
ZPROBE = ["M558", "G31", "M557" ]
HEATERS = ["M305", "M143", "M305", "M143"]
FANS = ["M106"]
TOOLS = ["M564", "G10"]
CUSTOM = []

CODES = []

# Get a list of G/M code heading from file using REGEX 
inFile = open('source.txt').read()
header = re.compile('==== [M|G][0-9].*:.*')
headings = []
for match in header.finditer(inFile):
	s=match.start()
	e=match.end()
	headings.append(inFile[s:e].replace('\n',''))
headings.append("== T: Select Tool ==")

# Special case for T-code
tHeadings = []
tHeadings.append("== T: Select Tool ==")
tHeadings.append("== G-Code Background Information ==")

# Special case for Index
iHeadings = []
iHeadings.append("This page describes the RepRapFirmware")
iHeadings.append("== G-commands")



def processSection(headings):

	# Loop through headings and capture text between 

	counter = 0
	#loop from second to n
	for i in range(1, len(headings)):
		print(headings[i-1])
		counter = counter + 1
		# Extract fileName 
		# ----------------

		# Is heading an index?
		if re.search("This page describes the RepRapFirmware", headings[i-1]):
			fileName = "index.md"
			permaLink = "index.html"
			headerText = "Gcode"
			codeName = "Gcode"
		# Is heading a combination (G0/G1 and G2/G3) ?
		elif re.search("T:", headings[i -1]):
			fileName = "T.md"
			permaLink = "T.html"
			headerText = "Select Tool"
			codeName = "T"
		
		elif re.search("&", headings[i -1]):
			headerText = re.search('(.*?): (.*?)====',headings[i -1]).group(2)

			codeName = re.search('[M|G][0-9].*:', headings[i -1]).group(0)
			codeName = codeName[:-1]	
			codes = codeName.replace(' ','').split('&')
			codeString = ''.join(map(str, codes))
			fileName = codeString + ".md"
			permaLink = codeString + ".html"
		else:
			headerText = re.search('(.*?): (.*?)====',headings[i -1]).group(2)

			codeName = re.search('[M|G][0-9]*', headings[i -1]).group(0)	
			CODES.append(codeName)

			x = CODES.count(codeName)
			if x > 1:
				fileName = codeName + "_" + str(x) + ".md"
				permaLink = codeName + "_" + str(x) + ".html"
			else:
				fileName = codeName + ".md"
				permaLink = codeName + ".html"

		print(codeName)		
		
		# Extract the sectionText for each command 
		# ----------------------------------------
		sectionStart = inFile.index(headings[i - 1])
		sectionEnd = inFile.index(headings[i])

		if codeName is not "Gcode":
			sectionStart = sectionStart + len(headings[i - 1])
		sectionText = inFile[sectionStart:sectionEnd]



		# Parse the sectionText based on MD
		# ---------------------------------
	
		sectionText = sectionText.replace("== G-commands ==", '')
		sectionText = sectionText.replace("== M-commands ==",'')
	
		sectionText = sectionText.replace("\n# ", '\n* ')
		sectionText = sectionText.replace("\'\'\'Usage\'\'\'", '## Usage')
		sectionText = sectionText.replace("\'\'\'Examples\'\'\'", '## Examples')
		sectionText = sectionText.replace("\'\'\'Example\'\'\'", '## Examples')
		sectionText = sectionText.replace("\'\'\'Example:\'\'\'", '## Examples')
		sectionText = sectionText.replace("\'\'\'Examples:\'\'\'", '## Examples')
		sectionText = sectionText.replace("\'\'\'Parameters\'\'\'", '### Parameters')
		sectionText = sectionText.replace("\'\'\'Parameters:\'\'\'", '### Parameters')
		sectionText = sectionText.replace("\'\'\'Extra Parameters\'\'\'", '### Extra Parameters')
		sectionText = sectionText.replace("\'\'\'Notes\'\'\'", '## Notes')
		sectionText = sectionText.replace("\'\'\'Order dependency\'\'\'", '## Order Dependency')
		sectionText = sectionText.replace("\'\'\'Order dependence\'\'\'", '## Order Dependency')
		sectionText = sectionText.replace("\'\'\'", "`")
		sectionText = sectionText.replace("^^1^^", "<sub>1</sub>")
		sectionText = sectionText.replace("^^2^^", "<sub>2</sub>")
		sectionText = sectionText.replace("[code]", "```\n")
		sectionText = sectionText.replace("[/code]", "\n```")
		sectionText = sectionText.replace("===== ", "## ")
		sectionText = sectionText.replace("=====", "")	

		# Tidy up Index page
		sectionText = sectionText.replace("====", "####")
		sectionText = sectionText.replace("===", "###")
		sectionText = sectionText.replace("==", "##")


		# try and wrap some of the commands. if start with M|G and ;
		sectionText = re.sub(r"/* [/M|G|T][0-9]+.*[/ ;]", " `\g<0> ` ", sectionText)
		

		# Replace section links with permalinks (and may be mulitple..
		# ------------------------------------------------------------

		linkMatch =  re.search(r"(\[\[Gcode#Section_([M|G|T]\d*)(_)\S*[M|G|T]\d*\]\])", sectionText)
		while linkMatch is not None:
			sectionText = re.sub(r"(\[\[Gcode#Section_([M|G|T]\d*)(_)\S*[M|G|T]\d*\]\])", r"[\g<2>](\g<2>).html", sectionText)
			linkMatch =  re.search(r"(\[\[Gcode#Section_([M|G|T]\d*)(_)\S*[M|G|T]\d*\]\])", sectionText)


		# try and convert the tables
		tPattern = re.compile(r'((.*)\n)')	
		tableText = re.search(r"({table)(.|\n)*(})", sectionText)
		if tableText is not None:	
			tableMD = ""
			for tRow in tPattern.finditer(tableText.group()):
				tRowData = tRow.group()
				if re.search(r"<<[^>]*>>",tRowData):
					tRowData = re.sub(r"<<[^>]*>>", "", tRowData)
					#tRowData = re.sub(r"<<(colspan=\")(\d+)[^>]*>>", " <td colspan=\g<2>>", tRowData)
				if tRowData.startswith("|!"):
					tRowData = tRowData.replace("! ", "")
				if tRowData.startswith('{table'):
					rowText = ""
					continue 
				if tRowData.startswith('|width'):
					continue
				if tRowData.startswith('|format'):
					continue
				if tRowData.startswith('|--'):
					rowText = rowText + "|\n"	
					tableMD = tableMD + rowText
					rowText = ""	
					continue
				if tRowData.startswith('!'):
					rowText = rowText.replace("!", "*")
	
				rowText = rowText + tRowData.rstrip()
			sectionText = sectionText.replace(tableText.group(), tableMD)

		# Some logic around tags
		# ----------------------
		tags = "["
		if codeName is "Gcode":
			tags = tags
		elif codeName.startswith("M"):
			tags = tags + "M-Commands"
		elif codeName.startswith("G"):	
			tags = tags + "G-Commands"
		else:
			tags = tags + "T-Commands"

		if re.search('deprecated', sectionText, re.IGNORECASE):
			tags = tags + ", Deprecated"

		if re.search('order dependent', sectionText, re.IGNORECASE):
			tags = tags + ", Order-Dependent"

		if codeName in NETWORKS:
			tags = tags + ", Network"
		if codeName in GENERAL:
			tags = tags + ", General"
		if codeName in DRIVES:
			tags = tags + ", Drives"
		if codeName in AXIS:
			tags = tags + ", Axis"
		if codeName in ENDSTOPS:
			tags = tags + ", Endstops"
		if codeName in ZPROBE:
			tags = tags + ", Zprobe"
		if codeName in HEATERS:
			tags = tags + ", Heaters"
		if codeName in FANS:
			tags = tags + ", Fans"
		if codeName in TOOLS:
			tags = tags + ", Tools"
		if codeName in CUSTOM:  
			tags = tags + ", Custom"
	
		tags = tags + "]"
		# Write the Jekyll theme front matter
		# -----------------------------------
		frontMatter = ["---\n"]
		frontMatter.append("counter: " + str(counter) + "\n" )
		frontMatter.append("available_since: " + "version_999" + "\n" )
		frontMatter.append("title: " + codeName + "\n")
		frontMatter.append("tags: " + tags + " \n" )
		frontMatter.append("keywords: beta \n" )
		frontMatter.append("last_updated: " + datetime.date.today().strftime("%B %d, %Y") + " \n" )
		if codeName is not "Gcode":
			frontMatter.append("summary: " + headerText + "\n")
		frontMatter.append("permalink: " + permaLink + "\n")
		frontMatter.append("toc: false \n")
	
		frontMatter.append("---\n")

		# Write to File
		# -------------

		with open(fileName, "w") as myFile:
			for j in (frontMatter):
				myFile.write(j)

			myFile.write(sectionText)
	
processSection(iHeadings)
processSection(headings)
processSection(tHeadings)
