import csv
import os
import sys

#call in form python ./filterscript.py <directoryFileName>
#directoryFileName should be without ./ (just like "data" etc)
#loops through the files in data and modifies them to exclude patents, remove the fields of
	# Source
	# Publisher
	# CitesURL
	# GSRank
	# QueryDate
	# Type

def wordChecker(row, word):
	for element in row:
		if word in element.lower():
			return True
	return False

def citedChecker(row):
	if int(row[0]) == 0:
		return False
	return True

def removeFieldsFromFile(fileName, directoryName):
	unSortedList = []
	with open("./" + directoryName + "/" + fileName, "rb") as infile:
		reader = csv.reader(infile, delimiter = ",")
		header = next(reader)
		unSortedList.append(header[1:4] +[header[6]] + [header[0]])
		for row in reader:
			if not wordChecker(row, "patent") and citedChecker(row):
 				unSortedList.append(row[1:4] + [row[6]] + [row[0]])
 	sortedList = sorted(unSortedList[1:], key = lambda row: row[2], reverse = True)
 	with open("./clean_" + directoryName + "/" + fileName, "wb") as outfile:
 		writer = csv.writer(outfile)
 		writer.writerow(unSortedList[0])
 		for row in sortedList:
 			writer.writerow(row)

def createXMLFromFile(fileName, directoryName):
	csvdata = []
	XMLFileName = "xml_" + directoryName + "/" + fileName[:-3] + "xml"
	with open("clean_" + directoryName + "/" + fileName, "rb") as infile:
		reader = csv.reader(infile, delimiter = ",")
		next(reader)
		for row in reader:
			csvdata.append(row)
	with open(XMLFileName, "wb") as outfile:
		outfile.write("<?xml version='1.0' encoding='UTF-8' ?>\n")
		outfile.write("<rss version = '2.0'>\n")
		outfile.write("<channel>\n")
		outfile.write("<title>EY Labs Papers by Lectin</title>\n")
		outfile.write("<link>./rssfeed.xml</link> \n")
		outfile.write("<description>New Papers by Lectin</description>\n")
		for row in csvdata:
			outfile.write("<item>\n")
			outfile.write("<title>" + row[1] +"</title>\n")
			outfile.write("<link>" + row[3] + "</link>\n")
			outfile.write("<description> Citations: " + row[4] + "</description>\n")
			outfile.write("<author>" + row[0] + "</author>\n")
			outfile.write("<pubDate>" + row[2] + "</pubDate>\n")
			outfile.write("</item>\n")
			outfile.write("\n")
		outfile.write("</channel>\n")
		outfile.write("</rss>\n")
		outfile.close()
	print XMLFileName
	return XMLFileName

def main():
	directoryName = sys.argv[1]
	rootdir = "./" + directoryName
	cleandir = "./clean_" + directoryName
	xmldir = "./xml_" + directoryName
	try:
		os.makedirs(cleandir)
	except OSError:
		pass
	for subdir, dirs, files in os.walk(rootdir):
		for fileName in files:
			removeFieldsFromFile(fileName, directoryName)
			print fileName
	print "done with cleaning"
	try:
		os.makedirs("./xml_" + directoryName)
	except OSError:
		pass
	for subdir, dirs, files in os.walk(cleandir):
		for fileName in files:
			createXMLFromFile(fileName, directoryName)
	print "done with creating XML Files"

main()