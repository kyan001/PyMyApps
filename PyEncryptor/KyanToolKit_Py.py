##################################################################
# Version 1.3
##################################################################
import os
import sys
import time
class KyanToolKit_Py(object):
	def __init__(self,trace_file_="trace.xml"):
		self.trace_file = trace_file_
		pass
	def __del__(self):
		pass
	def banner(self,content_="Well Come"):
		# char def
		self.special_char = "#"
		self.space_char = " "
		self.GOLDENSECTION = 0.618
		# length calc
		itsays = content_.strip()
		effective_length = int(len(itsays))
		# gen contents
		content_line = self.special_char \
						+ str(self.space_char * int(effective_length/self.GOLDENSECTION*(1-self.GOLDENSECTION)/2)) \
						+ itsays \
						+ str(self.space_char * int(effective_length/self.GOLDENSECTION*(1-self.GOLDENSECTION)/2)) \
						+ self.special_char
		content_line_lenght = len(content_line)
		banner_border = self.special_char * content_line_lenght
		return banner_border + '\n' + content_line + '\n' + banner_border

	def clearScreen(self):
		if "win32" == sys.platform:
			os.system('cls')
		elif "linux" in sys.platform:
			os.system('clear')
		else:
			os.system('clear')
			self.Err("No clearScreen for " + sys.platform)

	def pressToContinue(self,input_="..."):
		#PY2# raw_input(input_)
		input(input_)

	def getInput(self,question_,prompt_='> '):
		print(question_)
		#PY2# return raw_input(prompt_).strip()
		return input(prompt_).strip()

	def getChoice(self,choices_):
		out_print = ""
		index = 1
		for i in choices_:
			out_print += "\n" + str(index) + " - " + str(i)
			index += 1
		numerical_choice = int(self.getInput(out_print))
		if numerical_choice > len(choices_):
			self.byeBye("[ERR] Invalid Choice")
		return choices_[numerical_choice-1]

	def byeBye(self,input_="See you later."):
		exit(input_)

	def TRACE(self,input_,trace_type='INFO'):
		trace_content = ''.join(input_)
		current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		current_function = sys._getframe().f_back
		current_function_name = current_function.f_code.co_name
		current_line = current_function.f_code.co_firstlineno
		current_filename = current_function.f_code.co_filename
		trace_header = "\n<" + trace_type \
				+ ' FILE="' + current_filename + '"' \
				+ ' LINE="' + str(current_line) + '"' \
				+ ' TIME="' + current_time + '"' \
				+ ' FUNC="' + current_function_name + '()">\n'
		trace = open(self.trace_file,'a')
		trace.write(trace_header + trace_content + "\n</" + trace_type + ">\n")

	def RunCmd(self, words):
		print(self.banner(words))
		result = os.system(words)
		self.CheckResult(result)

	def CheckResult(self, result):
		if 0 == result:
			self.Info("Done")
		else:
			self.Warn("Failed")

	def Info(self, words):
		print("[INFO] " + words)

	def Warn(self, words):
		print("[WARNING] " + words)

	def Err(self, words):
		print("[ERROR] " + words)
