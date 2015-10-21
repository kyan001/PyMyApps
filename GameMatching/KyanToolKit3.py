import os
import sys
import time
def banner(content_="Well Come",printable_=True):
	# char def
	special_char = "#"
	space_char = " "
	GOLDENSECTION = 0.618
	# length calc
	itsays = content_.strip()
	effective_length = int(len(itsays))
	# gen contents
	content_line = special_char \
					+ str(space_char * int(effective_length/GOLDENSECTION*(1-GOLDENSECTION)/2)) \
					+ itsays \
					+ str(space_char * int(effective_length/GOLDENSECTION*(1-GOLDENSECTION)/2)) \
					+ special_char
	content_line_lenght = len(content_line)
	banner_border = special_char * content_line_lenght
	# print
	if printable_ == True:
		print(banner_border)
		print(content_line)
		print(banner_border)
	else:
		return banner_border + '\n' + content_line + '\n' + banner_border

def clearScreen():
	if sys.platform == "win32":
		os.system('cls')
	elif sys.platform == "linux2":
		os.system('clear')
	else:
		os.system('cls')
		print("[ No clearScreen for " + sys.platform + " ]")

def pressToContinue(input_="..."):
	input(input_) # raw_input() in V2

def getInput(question_,prompt_='> '):
	print(question_)
	return input(prompt_).strip() # raw_input() in V2

def getChoice(*choices_):
	out_print = ""
	index = 1
	for i in choices_:
		out_print += "\n" + str(index) + " - " + str(i)
		index += 1
	numerical_choice = int(getInput(out_print))
	if numerical_choice > len(choices_):
		byeBye("[ERR] Invalid Choice")
	return choices_[numerical_choice-1]

def byeBye(input_="Fuck off."):
	exit(input_)

def TRACE(type_, *input_):
	if type_ in ['INFO','ERR','WARNING']:
		content_ = "".join(input_)
	else:
		content_ = type_ + "".join(input_)
		type_ = 'INFO'
	current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	current_function = sys._getframe().f_back
	current_function_name = current_function.f_code.co_name
	if current_function_name == "<module>":
		current_function_name = "CONSOLE"
	current_line = current_function.f_code.co_firstlineno	
	current_filename = current_function.f_code.co_filename
	_header = "\n<" + type_ \
			+ ' FILE="' + current_filename + '"' \
			+ ' LINE="' + str(current_line) + '"' \
			+ ' TIME="' + current_time + '"' \
			+ ' FUNC="' + current_function_name + '()">\n'
	traceFile = open('trace.xml','a')
	traceFile.write(_header + content_ + "\n</" + type_ + ">\n")
