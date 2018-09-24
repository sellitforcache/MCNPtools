#! /usr/bin/env python
#  Script to convert newer MCNP inputs which have 'read file' cards
#  into a single file for use with MCNPX 2.4.0, which is openly distributed.
#  Can be useful in situations where people are waiting for license approval.
#  Also will wrap lines at 80 characters iteratively, which can be useful when
#  dealing with inputs that have segmented volumes and column highlighting makes
#  life easier.
#  ---- Ryan M. Bergmann, Paul Scherrer Institut, 2014, 2018.

import sys
import re
import datetime
import string
import os

def wrap_at_80(input_line):
	this_re = re.compile('.+([^.eE0-9+-]+)',flags=re.DOTALL)
	# recursive way, split line if longer than 80 characters
	if len(input_line) <= 80:
		return input_line
	else:
		mo = this_re.match(input_line[:80]) # find last index of non-numeric so as not to split in a surface/cell number
		if mo:
			dex = mo.end(1) # end of match 1 is safe
		else:
			print "ERROR!"
			exit(0)
		if input_line[dex:].isspace():
			return input_line[0:dex]+'\n'
		else:
			return input_line[0:dex]+wrap_at_80('\n     '+input_line[dex:])
		


def wrap_check(input_line):
	# iterative way, split line if longer than 80 characters
	if len(input_line)<=80:
		return input_line
	else:
		split_string = input_line.split(' ')
		out_string = ''
		test_out = ''
		for chunk in split_string:
			if len(test_out + chunk + ' ') > 80:
				out_string = out_string + test_out + '\n'
				test_out = '     ' + chunk + ' '
			else:
				test_out = test_out + chunk + ' '
		out_string = out_string + test_out[:-1]  # line should already have /n at the end, don't include last space appended...
		return out_string

def print_in_file(outputfile,fname,linenum):
	# go to location, if any
	fname_split = fname.split('/')
	fname_local = fname_split[ -1]
	fname_path  = string.join(fname_split[:-1])
	origi_dir   = os.getcwd()
	if len(fname_path)>0:
		os.chdir(fname_path)

	# try to open read-in file
	try:
		readfile = open(fname_local,"r")
	except:
		print "\n!!!!!!!\n Could not open read-in file '"+fname+"'. \n!!!!!!!\n"
		exit()

	#  print statement to terminal
	print "   -> writing file '"+fname_local+"' at line "+str(linenum)

	# blank line regex
	search_prog2 = re.compile("\s*\n")

	### read file regex
	search_prog = re.compile("read +file +([0-9a-zA-Z_.+-/]+)")

	#  write the file in at this line, write start delimiter
	outputfile.write("c START OF BLOCK WRITTEN BY convert2singlefile.py FROM FILE "+fname+"\n")
	outputfile.write("c --> DATE AND TIME: "+datetime.datetime.isoformat(datetime.datetime.today())+"\n")
	for line in readfile:
		blankline = search_prog2.match(line)
		readline  = search_prog.match(line)
		if blankline:
			print "          - skipping blank line in file "+fname_local
		elif readline:
			fname2 = readline.group(1)
			print_in_file(outputfile,fname2,linenum)
		else:
			outputfile.write(wrap_at_80(line))

	# check to make sure last character is a return
	if line[line.__len__()-1] != "\n":
		print "          + appending final carriage return to inserted file "+fname_local
		outputfile.write("\n")

	# write end delimiter
	outputfile.write("c END OF BLOCK WRITTEN BY convert2singlefile.py FROM FILE "+fname_local+"\n")
	outputfile.write("c --> DATE AND TIME: "+datetime.datetime.isoformat(datetime.datetime.today())+"\n")

	# close read-in file
	readfile.close()

	# return to original directory
	os.chdir(origi_dir)


### get inputs
if len(sys.argv) == 1:
	print "ERROR - You must specify an input file"
	exit(0)
elif len(sys.argv) == 2:
	inputname = sys.argv[1]
	print "ERROR - You must specify an output file"
	exit(0)
elif len(sys.argv) == 3:
	inputname = sys.argv[1]
	outputname = sys.argv[2]
elif len(sys.argv) > 3:
    print "ERROR - Too Many arguments.  USAGE:  convert2singlefile.py input_file output_file"
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
		outputfile.write(wrap_at_80(line))
	linenum = linenum + 1


### close files, print done
inputfile.close()
outputfile.close()
print "* DONE."
