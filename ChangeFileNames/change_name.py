# -*- coding: utf-8 -*-
import os
import re
import sys
# set keyword for rename
kywrd = ""
if "" == kywrd:
	kywrd = (sys.argv[0].split('\\')[-2]).replace(' ','_')
print("Keyword  =>  " + kywrd)
# set pattern for matching
pttrn = r'\[([0-9][0-9])\]'
print("Pattern  =>  " + pttrn)
dir = os.getcwd()
if not sys.argv[1:]:
	print("Drag & Drop files on me")
for f in sys.argv[1:]:
	# get file append.
	fappend = f.split('.')[-1]
	# get file name from full path.
	fname = f.split('\\')[-1]
	# match pattern
	m = re.search(pttrn,fname)
	if None == m:
		continue
	target_name = kywrd + "_" + m.group(1) + "." + fappend
	if sys.argv[1] == f:
		print("[  " + f + "  ]")
		print("Filename =>	" + fname)
		print("Matched  =>	" + m.group(1))
		print("Keyword  =>	" + kywrd)
		print("Append   =>	" + fappend)
		print("Target   =>	" + target_name)
		input("Press enter to rename all the files ...")
	cmmnd = 'rename "' + f + '" "' + target_name + '"'
	os.system(cmmnd)
	print(fname + " ==> " + target_name)
input("[	Done	]")

