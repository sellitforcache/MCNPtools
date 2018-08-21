#! /usr/bin/env python
#  Script to convert newer MCNP inputs which have 'read file' cards 
#  into a single file for use with MCNPX 2.4.0, which is openly distributed.
#  Can be useful in situations where people are waiting for license approval.
#  ---- Ryan M. Bergmann, Paul Scherrer Institut, Nov. 10, 2014.

import sys
import re
import datetime

def print_in_file(outputfile,fname,linenum):
	# try to open read-in file
	try:
		readfile = open(fname,"r")
	except:
		print "Could not open read-in file '"+fname+"'. "

	#  print statement to terminal
	print "   -> writing file '"+fname+"' at line "+str(linenum)

	# blank line regex
	search_prog2 = re.compile("\s*\n")

	#  write the file in at this line, write start delimiter
	outputfile.write("c START OF BLOCK WRITTEN BY convert2singlefile.py FROM FILE "+fname+"\n")
	outputfile.write("c --> DATE AND TIME: "+datetime.datetime.isoformat(datetime.datetime.today())+"\n")
	for line in readfile:
		blankline = search_prog2.match(line)
		if blankline:
			print "          - skipping blank line in file "+fname
		else: 
			outputfile.write(line)

	# check to make sure last character is a return
	if line[line.__len__()-1] != "\n":
		print "          + appending final carriage return to inserted file "+fname
		outputfile.write("\n")

	# write end delimiter
	outputfile.write("c END OF BLOCK WRITTEN BY convert2singlefile.py FROM FILE "+fname+"\n")
	outputfile.write("c --> DATE AND TIME: "+datetime.datetime.isoformat(datetime.datetime.today())+"\n")

	# close read-in file
	readfile.close()


### get inputs
if len(sys.argv) == 1:
	print "ERROR - You must specify an input file"
	exit(0)
elif len(sys.argv) == 2:
	inputname = sys.argv[1]
	outputname = inputname.split('.')[0]+"s.i"
elif len(sys.argv) == 3:
	inputname = sys.argv[1]
	outputname = sys.argv[2]
elif len(sys.argv) > 3:
    print "ERROR - Too Many arguments.  USAGE:  convert2singlefile.py input_file [output_file]"
    exit(0)

print "* Converting input '"+inputname+"' (and read-in files) into SINGLE FILE '"+outputname+"' ..."

### test input file
try:
	inputfile = open(inputname,"r")
except:
	print "Could not open file '"+inputname+"'. "

### open output file
try:
	outputfile = open(outputname,"w")
except:
	print "Could not open file '"+outputname+"' for writing. "

### make and compile regex
search_prog = re.compile("read +file +([0-9a-zA-Z_.+-/]+)")

### scan lines, looking for 'read'
linenum = 1
for line in inputfile:
	results = search_prog.match(line)
	if results:
		fname = results.group(1) 
		print_in_file(outputfile,fname,linenum)
		#print(line)
	else:
		outputfile.write(line)
	linenum = linenum + 1


### close files, print done
inputfile.close()
outputfile.close()
print "* DONE."
